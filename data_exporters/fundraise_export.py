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
    funding_founders = data[0]
    funding_investors = data[1]
    activity_investor = data[2]

    if funding_founders.empty and funding_investors.empty:
        print('nothing to append')
        return

    funding_founders.reset_index(drop=True, inplace=True)
    funding_founders = funding_founders.astype('str')
    funding_founders.to_sql('fundraise_companies_founders',con=engine, if_exists='append',index=False)

    print(funding_founders.columns)

    funding_investors.reset_index(drop=True, inplace=True)
    funding_investors = funding_investors.astype('str')
    funding_investors.to_sql('fundraise_companies_investors',con=engine, if_exists='append',index=False)

    activity_investor.reset_index(drop=True, inplace=True)
    activity_investor = activity_investor.astype('str')
    activity_investor.to_sql('activity_investor',con=engine, if_exists='append',index=False)