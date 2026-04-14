import os
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
import seaborn as ss
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import joblib

def preprocess_data():
    os.makedirs('metrics',exist_ok=True)
    os.makedirs('models',exist_ok=True)

    data=pd.read_csv('data/water_potability.csv')
    missing_values=data.isnull().sum()
    missing_values.to_csv('metrics/missing_values.csv')

    stats=data.describe()
    stats.to_csv('metrics/data_statistics.csv')

    ss.pairplot(data,hue='Potability')
    plt.savefig('metrics/pairplot.png')

    plt.figure(figsize=(10,8))
    ss.heatmap(data.corr(),annot=True,cmap='coolwarm')
    plt.savefig('metrics/correlation_heatmap.png')

    imputer=SimpleImputer(strategy='mean')
    data_imputed=pd.DataFrame(imputer.fit_transform(data),columns=data.columns)
    scaler=StandardScaler()
    features=data_imputed.drop('Potability',axis=1)
    target=data_imputed['Potability']
    data_scaled=scaler.fit_transform(features)
    joblib.dump(scaler,'models/scaled.joblib')

    data_preprocessed=pd.DataFrame(data_scaled,columns=features.columns)
    data_preprocessed['Potability']=target
    data_preprocessed.to_csv("metrics/preprocessed_data.csv",index=False)

if __name__=="__main__":
    preprocess_data()


