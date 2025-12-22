import json
from django.shortcuts import render,redirect
from  sent_app.tasks import stream_and_save_comments,analyze_u_account
from .models import Sentiment,PostSentiment
from wordcloud import WordCloud
from io import BytesIO
import base64
import requests
import xlwt
# import numpy as np
from django.http import HttpResponse

def index(request):
    return render(request,"sent/index.html")

def buttons(request):
    return render(request,"sent/buttons.html")

def cards(request):
    return render(request,"sent/cards.html")

def error_page(request):
    return render(request,"sent/404.html")

def charts(request):
    # return render(request,"sent/charts.html")
    if request.method=="POST":
        url=request.POST.get("url")
        comments=stream_and_save_comments(url)
        if comments is None:
            return render(request,"sent/404.html")
        pos=0;neg=0;neu=0;total_comm=0;pos_sum=0;neg_sum=0;neu_sum=0
        overall_sentiments=[]
        print(type(comments))
        for comm in comments['comments_list']:
            # print(comments[ind]['compound'])
            if comm['sentiment'] == 'positive':
                pos_sum+=comm['positive']
                pos+=1
            elif comm['sentiment']  == 'negative':
                neg_sum+=comm['negative']
                neg+=1
            else:
                neu_sum+=comm['neutral']
                neu+=1
            total_comm+=1
            overall_sentiments.append(comm['comment'])
            # total_compound+=comments[ind]['compound']
        wc=WordCloud(width=800,height=400,max_words=600,background_color='white').generate(" ".join(overall_sentiments))
        buffer=BytesIO()
        wc.to_image().save(buffer,format='PNG')
        img_str=base64.b64encode(buffer.getvalue()).decode()
        pos_avg=pos_sum/pos if pos!=0 else 0
        neg_avg=neg_sum/neg if neg!=0 else 0
        neu_avg=neu_sum/neu if neu!=0 else 0
        sentiment_index=(pos-neg)/total_comm if total_comm!=0 else 0
        overall_sentiment=''
        if pos>neg and pos>neu:
            overall_sentiment='👍'
        elif neg>pos and neg>neu:
            overall_sentiment='👎'
        else:
            overall_sentiment='😐'
        title=comments['title']
        comm_count=comments['total_comments']
        chart_data={"post_img":comments['image'],"pos":pos,"neg":neg,"neu":neu,"total":overall_sentiment,"count":comm_count,'pos_avg':float(pos_avg),'neg_avg':float(neg_avg),'neu_avg':float(neu_avg),'sentiment_index':sentiment_index,'title':title}
        chart_data_json=json.dumps(chart_data)
        return render(request,"sent/charts.html",{"chart_data": chart_data,"chart_data_json":chart_data_json,"wordcloud_img":img_str})
        # return render(request,"sent/charts.html")
    return render(request,"sent/charts.html")

def get_user_account(request):
    if request.method=="POST":
        username=request.POST.get("username")
        analyze_u_account.delay(username)
        return redirect("sent_app:tables")
    return render(request,"sent/index.html")

def login(request):
    return render(request,"sent/login.html")

def data_save(request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Sentiments_analysis.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet1')

        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Comment', 'Positive', 'Negative', 'Neutral', 'Compound'] 
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, subsequent rows
        font_style = xlwt.XFStyle()

        # Retrieving data from model
        data = Sentiment.objects.all() 
        for row in data:
            row_num += 1
            # Replace with your actual model fields
            ws.write(row_num, 0, row.comment, font_style) 
            ws.write(row_num, 1, row.positive, font_style)
            ws.write(row_num, 2, row.negative, font_style)
            ws.write(row_num, 3, row.neutral, font_style)
            ws.write(row_num, 4, row.compound, font_style)
        wb.save(response)
        return response

def forgot_password(request):
    return render(request,"sent/forgot-password.html")

def register(request):
    return render(request,"sent/register.html")

def tables(request):
    comments=Sentiment.objects.all().order_by("-create_time")[:100]
    if(comments.count()==0):
        return render(request,"sent/error.html")
    return render(request,"sent/tables.html",{"sentiments":comments})

def utilities_animation(request):
    return render(request,"sent/utilities-animation.html")

def utilities_border(request):
    return render(request,"sent/utilities-border.html")

def utilities_color(request):
    return render(request,"sent/utilities-color.html")

def utilities_other(request):
    return render(request,"sent/utilities-other.html")

def sentiment(request):
    stream_and_save_comments.delay()
    return redirect("sent_app:tables")
    
def get_user_account_comments(request):
    comms=PostSentiment.objects.all()[:100]
    if not comms:
        print("no comments " )
    return render(request,"sent/tables.html",{"post_sentiments":comms})

# def fetch_comments(request):
#     comments=Sentiment.objects.all().order_by("-create_time")
#     if(comments.count()==0):
#         return render(request,"sent/error.html")
#     return render(request,"sent/sentiment.html",{"sentiments":comments})
