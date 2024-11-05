import os 
import pandas as pd
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
PATH = '/home/ubuntu/data'
parent_dir = os.listdir(PATH)
parent_dir.sort()
if len(parent_dir)>1: 
    parent_dir = parent_dir[1]
df_list = []

@data_loader
def load_founder_data(*args, **kwargs):
    if 'manual_entry.csv' not in os.listdir(PATH + '/'):
        print('no manual entry found found, please upload data')
        return pd.DataFrame()
    try:
        file_path = PATH + '/' + parent_dir
        df = pd.read_csv(file_path)
        os.remove(file_path)

        print(df.shape)
    
        return df
    except Exception as e: 
        print('no manual entry found \n',e)