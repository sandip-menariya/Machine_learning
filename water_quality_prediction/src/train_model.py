import os
import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import skops.io as sio

def train_model():
    data=pd.read_csv(r'metrics/preprocessed_data.csv')
    features=data.drop('Potability',axis=1)
    target=data['Potability']
    X_train,X_test,Y_train,Y_test=train_test_split(features,target,test_size=0.2,random_state=42,stratify=target)

    os.makedirs('models',exist_ok=True)
    model=RandomForestClassifier(n_estimators=200,random_state=42)
    model.fit(X_train,Y_train)
    sio.dump(model,'models/water_quality_model.skops')
    metadata={
        'model_name':'RandomForestClassifier',
        'parameters':model.get_params(),
        'training_score':model.score(X_train,Y_train),
    }
    with open('models/metadata.json','w') as f:
        json.dump(metadata,f,indent=4)

if __name__=="__main__":
    train_model()
