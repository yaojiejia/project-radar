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
def load_company_data(*args, **kwargs):
    if 'companies' not in os.listdir(PATH + '/' + parent_dir):
        print('no companies folder found, please upload data')
        return [pd.DataFrame()]
    try:
        for path in os.listdir(PATH + '/' + parent_dir + '/companies'): 
            file_path = os.path.join(PATH + '/' + parent_dir + '/companies', path)
            df = pd.read_csv(file_path)
            df_list.append(df)

        companies_list = pd.concat(df_list, ignore_index=True)
    
        return companies_list
    except Exception as e: 
        print('no companies found \n',e)