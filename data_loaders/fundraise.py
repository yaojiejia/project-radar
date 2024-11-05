import os 
import pandas as pd
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
PATH = '/home/ubuntu/data'
parent_dir = os.listdir(PATH)[0]
founder_raise = []
investor_raise = []

@data_loader
def load_fundraise_data(*args, **kwargs):
    try:
        for path in os.listdir(PATH + '/' + parent_dir + '/funding'): 
            file_path = os.path.join(PATH + '/' + parent_dir + '/funding', path)
            if 'founder_raise' in path:
                df = pd.read_csv(file_path)
                founder_raise.append(df)
            if 'investor_raise' in path: 
                df = pd.read_csv(file_path)
                investor_raise.append(df)


        founder_fundraise_df = pd.concat(founder_raise, ignore_index=True)
        investor_fundraise_df = pd.concat(investor_raise, ignore_index=True)
    
        return [founder_fundraise_df, investor_fundraise_df]
    except Exception as e: 
        print('no funding found \n',e)