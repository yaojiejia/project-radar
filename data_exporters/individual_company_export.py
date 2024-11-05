from sqlalchemy import create_engine
import pandas as pd

db_user = 'berkleycenter'
db_password = 'BerkleyCenterDB1//'
db_host = '3.135.235.86'
db_port = '3306'
db_name = 'berkleyStartUp'

db_url = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

engine = create_engine(db_url)

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here
    companies = data[0]
    com_founder = data[1]
    com_ind = data[2]
    
    if companies.empty and com_founder.empty: 
        print('nothing to append')
        return
        
    companies.reset_index(drop=True, inplace=True)
    companies = companies.astype('str')
    companies.to_sql('com_table',con=engine, if_exists='append',index=False)

    com_founder.reset_index(drop=True, inplace=True)
    com_founder = com_founder.astype('str')
    com_founder.to_sql('com_founder',con=engine, if_exists='append',index=False)

    com_ind.reset_index(drop=True, inplace=True)
    com_ind = com_ind.astype('str')
    com_ind.to_sql('com_ind',con=engine, if_exists='append',index=False)
