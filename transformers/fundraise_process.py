import numpy as np
import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def inv_activity(org_row, df):
    '''
    this function maps the nyu affiliated investors to the fundraise log
    '''
    df = df[['Full Name', 'person_id']]
    investors = org_row['Investor Names'].split(', ')
    for i in range(len(investors)): 
        investors[i] = ''.join([j if ord(j) < 128 else ' ' for j in investors[i]])
    result = df[['Full Name', 'person_id']][df['Full Name'].isin(investors)]
    return [result['Full Name'].to_list(), result['person_id'].to_list()] if not result['Full Name'].empty else [np.nan, np.nan]

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
    funding_founders = data[0]
    funding_investors = data[1]

    investors = args[0]

    fundraise_from_db_investor = args[1]
    fundraise_from_db_founder = args[2]


    if funding_founders.empty and funding_investors.empty:
        print('no fundraise found, please uplaod the data')
        return [pd.DataFrame(),pd.DataFrame()]

    if not fundraise_from_db_investor.empty:
        funding_investors = funding_investors[~funding_investors['Transaction Name URL'].isin(fundraise_from_db_investor['Transaction Name URL'])]
    else: 
        funding_investors = funding_investors

    if not fundraise_from_db_founder.empty:
        funding_founders = funding_founders[~funding_founders['Transaction Name URL'].isin(fundraise_from_db_founder['Transaction Name URL'])]
    else: 
        funding_founders = funding_founders

    print(funding_founders.columns,funding_investors.columns)
    funding_founders = funding_founders.drop_duplicates(subset=['Transaction Name URL'])
    funding_investors = funding_investors.drop_duplicates(subset=['Transaction Name URL'])

    # Replace "None" with NaN
    funding_founders = funding_founders.replace(' ', value=np.nan)
    funding_investors = funding_investors.replace(' ', value=np.nan)
    
    # process investor column
    result = funding_investors.apply(inv_activity, axis=1, args=(investors,))
    funding_investors['affiliates'] = [x[0] for x in result.iloc[:]]
    funding_investors['affiliates_id'] = [x[1] for x in result.iloc[:]]
    
    #create company_founder join table
    activity_investor = funding_investors[['Transaction Name URL', 'affiliates', 'affiliates_id']].explode(['affiliates', 'affiliates_id'], ignore_index=True)
    funding_founders = funding_founders.sort_values(by='Announced Date', ascending=True)
    funding_investors = funding_investors.sort_values(by='Announced Date', ascending=True)
    
    return [funding_founders,funding_investors,activity_investor]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
