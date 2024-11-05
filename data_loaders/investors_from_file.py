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
small_investor = []
big_investor = []

@data_loader
def load_investors_data(*args, **kwargs):
    if 'investors' not in os.listdir(PATH + '/' + parent_dir):
        print('no investor folder found, please upload data')
        return [pd.DataFrame(),pd.DataFrame()]
    try:
        small_inv, big_inv = pd.DataFrame(), pd.DataFrame()
        for path in os.listdir(PATH + '/' + parent_dir + '/investors'): 
            file_path = os.path.join(PATH + '/' + parent_dir + '/investors', path)
            
            if 'small_investor' in file_path:
                df = pd.read_csv(file_path)
                small_investor.append(df)
            if 'big_investor' in file_path:
                df = pd.read_csv(file_path)
                big_investor.append(df)

        if small_investor: small_inv = pd.concat(small_investor, ignore_index=True)
        if big_investor: big_inv = pd.concat(big_investor, ignore_index=True)
    
        return [small_inv,big_inv]
    except Exception as e: 
        print('no investors found \n',e)