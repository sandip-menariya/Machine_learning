import json
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score,roc_curve, auc
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as ss
import skops.io as sio
import joblib


def evaluate_model():
    data=pd.read_csv(r'metrics/preprocessed_data.csv')
    features=data.drop('Potability',axis=1)
    target=data['Potability']
    X_train,X_test,Y_train,Y_test=train_test_split(features,target,test_size=0.2,random_state=42,stratify=target)

    model=sio.load('models/water_quality_model.skops')
    Y_pred=model.predict(X_test)
    Y_prob=model.predict_proba(X_test)[:,1]

    report=classification_report(Y_test,Y_pred,output_dict=True)
    with open('metrics/classification_report.json','w') as f:
        json.dump(report,f,indent=4)
    conf_matrix=confusion_matrix(Y_test,Y_pred)
    ss.heatmap(conf_matrix,annot=True,cmap='Blues',fmt='d')
    plt.title("Confusion Matrix")
    plt.ylabel("Actual Label")
    plt.xlabel("Predicted Label")
    plt.savefig('metrics/confusion_matrix.png')
    fpr,tpr,_=roc_curve(Y_test,Y_prob)
    roc_auc=roc_auc_score(Y_test,Y_prob)
    plt.figure()
    plt.plot(fpr,tpr,label="AUC = %0.2f" % roc_auc)
    plt.plot([0,1],[0,1],'k--')
    plt.legend(loc='lower right')
    plt.title("Receiver Operating Characteristic")
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.savefig('metrics/roc_curve.png')
    accuracy=model.score(X_test,Y_test)
    print(f"Overall Accuracy: {accuracy*100:.2f}%")

if __name__=="__main__":
    evaluate_model()