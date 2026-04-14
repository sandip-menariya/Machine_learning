import os

def download_data():
    os.makedirs('data',exist_ok=True)
    os.system('kaggle datasets download -d adityakadiwal/water-potability -p data --unzip')

if __name__=="__main__":
    download_data()