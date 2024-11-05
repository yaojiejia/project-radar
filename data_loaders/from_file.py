import os 
import pandas as pd
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
PATH = '/home/ubuntu/data'
parent_dir = os.listdir(PATH)
parent_dir.sort()
parent_dir = parent_dir[0]
df_list = []


@data_loader
def load_founder_data(*args, **kwargs):
    if 'founders' not in os.listdir(PATH + '/' + parent_dir):
        print('no founders folder found, please upload data')
        return [pd.DataFrame()]
    try:
        for path in os.listdir(PATH + '/' + parent_dir + '/founders'): 
            file_path = os.path.join(PATH + '/' + parent_dir + '/founders', path)
            df = pd.read_csv(file_path)
            df_list.append(df)

        founder_list = pd.concat(df_list, ignore_index=True)
    
        print(founder_list.columns)
        return founder_list
    except Exception as e: 
        print('no founders found \n',e)