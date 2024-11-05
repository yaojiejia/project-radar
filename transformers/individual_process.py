import pandas as pd
import numpy as np

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    org = pd.DataFrame()
    fund = pd.DataFrame()   
    founder = pd.DataFrame()

    if data.empty:
        print('nothing to append')
        return [data,org,fund,founder]
    
    # org_columns = all_columns[:10]
    # fund_columns = all_columns[10:20]
    # founder_columns = all_columns[20:]

    all_columns = data.columns

    org_columns = all_columns[2:20]
    funding_columns_1 = all_columns[2:20]# + all_columns[64:]
    funding_columns_2 = all_columns[64:]

    founder1 = data[all_columns[20:31]]
    founder2 = data[all_columns[31:42]]
    founder3 = data[all_columns[42:53]]
    founder4 = data[all_columns[53:64]]

    
    founder1 = founder1.rename(columns={col: col.replace(' 1', '') for col in founder1.columns})
    founder2 = founder2.rename(columns={col: col.replace(' 2', '') for col in founder2.columns})
    founder3 = founder3.rename(columns={col: col.replace(' 3', '') for col in founder3.columns})
    founder4 = founder4.rename(columns={col: col.replace(' 4', '') for col in founder4.columns})

    founder = pd.DataFrame()
    founder = pd.concat([founder1,founder2,founder3,founder4])

    cols_to_add_founder = ['Full Name URL', 'Primary Organization URL', 'Number of Investments', 
               'Twitter', 'Number of Partner Investments', 'Number of Founded Organizations',
               'Number of Lead Investments', 'Facebook', 'Biography', 
               'Number of Portfolio Companies', 'Number of Diversity Investments',
               'First Name', 'Last Name']

#    Add the missing columns with NaN values
    for col in cols_to_add_founder:
        founder[col] = np.nan

    founder = founder.dropna(subset=['Full Name'])
    founder = founder.rename(columns={"Primary Org": "Primary Organization","LinkedIn (Founder)":"LinkedIn"})

    companies = data[org_columns]
    companies = companies.dropna(subset=['Organization Name'])
    companies['Organization Name URL'] = companies['Website']

    cols_to_add_companies = ['Number of Contacts', 'Last Funding Type', 'Total Funding Amount', 
                'Last Funding Date', 'Full Description', 'Industries', 'Founded Date Precision']

    for col in cols_to_add_companies:
        companies[col] = np.nan

    companies = companies.rename(columns={'Total Funding Amount Currency (in USD)': 'Total Funding Amount (in USD)'})
    companies = companies.drop(['Number of Employees','Number of Founders','Number of Funding Rounds'], axis=1)
    companies.reset_index(drop=True, inplace=True)
    companies = companies.astype('str')


    fundraise = data[funding_columns_1.append(funding_columns_2)]
    fundraise = fundraise.dropna(subset=['Announced Date'])

    return [data,companies,founder,fundraise]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
