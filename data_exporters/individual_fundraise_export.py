from sqlalchemy import create_engine
import pandas as pd

db_user = 'berkleycenter'
db_password = 'BerkleyCenterDB1//'
db_host = '18.225.36.8'
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
    funding_founders = data

    if funding_founders.empty:
        print('nothing to append')
        return

    funding_founders.reset_index(drop=True, inplace=True)
    funding_founders = funding_founders.astype('str')
    funding_founders.to_sql('fundraise_companies_founders',con=engine, if_exists='append',index=False)