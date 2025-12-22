from celery import shared_task
from .models import PostSentiment,Sentiment
import praw
import numpy as np
import torch
import re
from transformers import AutoTokenizer,AutoModelForSequenceClassification
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# model name from huggingface model hub trained on 58 million tweets
model_name="cardiffnlp/twitter-roberta-base-sentiment-latest"
# load model and tokenizer, tokenizer is used to convert text to tokens which model can understand it returns tensor of input ids and attention mask
tokenizer=AutoTokenizer.from_pretrained(model_name)
# load pre-trained model
model=AutoModelForSequenceClassification.from_pretrained(model_name)

# random comments fetched from reddit and saved to db
# @shared_task(name="sent_app.tasks.stream_and_save_comments")
# def stream_and_save_comments():
#     reddit=praw.Reddit(
#     client_id="jJ8NZM6QszwyJ00hXpAIcg",
#     client_secret="vRb3XMYoM4eo3UA23l9mIlUCNJUAdw",
#     user_agent="web:SentimentDashboard:v1.0 by u/Which-Test-440" )
#     analyze=SentimentIntensityAnalyzer()
#     count_comments=0
#     for comment in reddit.subreddit("all").comments(limit=100):
#         sentiment=analyze.polarity_scores(comment.body)
#         if not Sentiment.objects.filter(comment=comment.body).exists():
#             comments=Sentiment(
#             comment=comment.body,
#             positive=sentiment['pos'],
#             negative=sentiment['neg'],
#             neutral=sentiment['neu'],
#             compound=sentiment['compound'],
#             )
#             comments.save()
#             count_comments+=1
#     print(f"saved {count_comments} new comments")
#     return True

def clean_text(text):
    text=re.sub(r"http\S+|www\S+|https\S+","",text,flags=re.MULTILINE)
    text=re.sub(r'\@w+|\#','',text)
    text=re.sub(r'\#[A-Z0-9a-z\s]','',text,flags=re.MULTILINE)
    return text.strip()

def get_post_image(submission):
    # Direct image link
    if submission.url.endswith((".jpg", ".jpeg", ".png", ".gif")):
        return [submission.url]

    # Reddit preview
    if hasattr(submission, "preview"):
        try:
            return [submission.preview["images"][0]["source"]["url"]]
        except:
            pass

    # Gallery posts
    if getattr(submission, "is_gallery", False):
        try:
            images = []
            for item in submission.gallery_data["items"]:
                media_id = item["media_id"]
                img_info = submission.media_metadata[media_id]
                images.append(img_info["s"]["u"])
            return images
        except:
            pass
    return []

# url specific comments fetched from reddit and saved to db
# analyzing single post comments based on url
@shared_task(name="sent_app.tasks.stream_and_save_comments")
def stream_and_save_comments(url):
    # initialize reddit instance
    reddit=praw.Reddit(
    client_id="jJ8NZM6QszwyJ00hXpAIcg",
    client_secret="vRb3XMYoM4eo3UA23l9mIlUCNJUAdw",
    user_agent="web:SentimentDashboard:v1.0 by u/Which-Test-440" )
    #if url is None or url not starts with "https://www.reddit.com" return empty list
    if url is None or not url.startswith("https://www.reddit.com"):
        return []
    submission=reddit.submission(url=url)
    title=submission.title
    if submission is None:
        return []
    imgs=get_post_image(submission)
    print("post image: ",imgs)
    submission.comments.replace_more(limit=None) #fetches all comments
    count_comments=0
    comments_list=[]
    labels=['negative','neutral','positive']
    for comment in submission.comments.list():
        clean_txt=clean_text(comment.body)
        inputs=tokenizer(clean_txt,return_tensors="pt",truncation=True,max_length=512)
        with torch.no_grad():
            logits=model(**inputs).logits
        probs=torch.softmax(logits,dim=1).numpy()[0]
        comments_list.append(
            {"comment": comment.body, "positive": probs[2],"negative": probs[0],"neutral": probs[1],"sentiment":labels[np.argmax(probs)]}
        )
        count_comments+=1
    print(f"saved {count_comments} new comments")
    return {"title":title,"image":imgs,"comments_list":comments_list,"total_comments":count_comments}

# @shared_task(name="sent_app.tasks.stream_and_save_comments")
def analyze_u_account(username):
    reddit=praw.Reddit(
    client_id="jJ8NZM6QszwyJ00hXpAIcg",
    client_secret="vRb3XMYoM4eo3UA23l9mIlUCNJUAdw",
    user_agent="web:SentimentDashboard:v1.0 by u/Which-Test-440" )
    if username is None:
        return []
    user=reddit.redditor(name=username)
    print("got user ",user)
    if not user:
        return []
    posts=user.submissions.new(limit=None)
    user_id=user.id
    print(f"analyzing posts of user: {user_id}")
    for post in posts:
        post.comments.replace_more(limit=None) #fetches all comments
        title=post.title
        post_id=post.id
        print("post id ",post_id)
        if PostSentiment.objects.filter(userid=user_id,postid=post_id).exists():
            continue
        pos=0;neg=0;neu=0;total_comm=0;pos_sum=0;neg_sum=0;neu_sum=0
        labels=['negative','neutral','positive']
        for comment in post.comments.list():
            clean_txt=clean_text(comment.body)
            if clean_txt in ["","[deleted]","[removed]"]:
                continue
            inputs=tokenizer(clean_txt,return_tensors="pt",truncation=True,max_length=512)
            with torch.no_grad():
                logits=model(**inputs).logits
            probs=torch.softmax(logits,dim=1).numpy()[0]
            sent=labels[np.argmax(probs)]
            if sent=='positive':
                pos_sum+=probs[2]
                pos+=1
            elif sent=='negative':
                neg_sum+=probs[0]
                neg+=1
            else:
                neu_sum+=probs[1]
                neu+=1
            total_comm+=1
        pos_avg=pos_sum/pos if pos!=0 else 0
        neg_avg=neg_sum/neg if neg!=0 else 0
        neu_avg=neu_sum/neu if neu!=0 else 0
        sentiment_index=(pos-neg)/total_comm if total_comm!=0 else 0
        sentiment=''
        if pos>neg and pos>neu:
            sentiment='positive'
        elif neg>pos and neg>neu:
            sentiment='negative'
        else:
            sentiment='neutral'
        PostSentiment.objects.update_or_create(
        userid=user_id,
        postid=post_id,
        defaults={
        "username":username,
        "post_title":title,
        "sentiment":sentiment,
        "sentiment_index":float(sentiment_index),
        "total_comments":total_comm,
        "pos_sum":float(pos_sum),
        "neg_sum":float(neg_sum),
        "neu_sum":float(neu_sum),
        "total_positive":pos,
        "total_negative":neg,
        "total_neutral":neu,
        })
        print(f"saved {total_comm} new comments")
    print("!!! work done !!!")