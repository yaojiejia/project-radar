import numpy as np
import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def inter_array(org_row, df):
    '''
    this function maps the nyu affiliated founders to the company
    '''
    df = df[['Full Name', 'Current Organizations', 'person_id']]

    if type(df['Current Organizations'][0]) != list:
        df['Current Organizations'] = [ind.split(', ') if type(ind) == str else np.nan for ind in df['Current Organizations']]
    
    
    founders = org_row['Founders'].split(', ')
        
    for i in range(len(founders)): 
        founders[i] = ''.join([j if ord(j) < 128 else ' ' for j in founders[i]])
    result = df[df['Full Name'].isin(founders)]
    

    if result['Full Name'].duplicated().any():
        result['dup'] = result['Full Name'].duplicated(keep=False)
        dup_name = result['Full Name'][result['dup'] == True].unique()
        p1 = result[['Full Name', 'person_id']][result['dup'] == False]
        p2 = df[['Full Name', 'person_id']][(df['Full Name'].isin(dup_name)) & (df['Current Organizations'].apply(lambda x: org_row['Organization Name'] in x if isinstance(x, list) else False))]
        result = pd.concat([p1, p2], axis=0)

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


    companies = data[1]
    companies_from_db = args[0]
    unique_companies = pd.DataFrame()

    individual_founder = args[1]
    db_founder = args[2]

    if individual_founder.empty:
        founders = db_founder
    else:
        founders = individual_founder

    if companies.empty:
        print('no companies found, please upload data')
        return [pd.DataFrame(),pd.DataFrame(),pd.DataFrame()]

    if not companies_from_db.empty:
        companies = companies[~companies['Organization Name URL'].isin(companies_from_db['Organization Name URL'])]


    companies = companies.drop_duplicates(subset=['Organization Name URL'])
    non_nyu_founders = founders.loc[founders['nyu_school'].isnull()]['person_id']
    
    if companies.empty:
        print('no companies found, please upload data')
        return [pd.DataFrame(),pd.DataFrame()]

    # create primary key
    companies.reset_index(inplace=True, names='org_id')
    companies['org_id'] = [str(i) for i in range(len(companies_from_db)+1, len(companies_from_db) + 1 + len(companies))]
    
    # process founders column
    result = companies.apply(inter_array, axis=1, args=(founders,))
    companies['affiliates'] = [x[0] for x in result.iloc[:]]
    companies['affiliates_id'] = [x[1] for x in result.iloc[:]]

    com_founder = companies[['org_id', 'affiliates', 'affiliates_id']].explode(['affiliates', 'affiliates_id'], ignore_index=True)
    # create company_industry join table
    companies['Industry Groups'] = [ind.split(', ') if type(ind) == str else np.nan for ind in companies['Industry Groups']]
    com_ind = companies[['org_id', 'Industry Groups']].explode('Industry Groups', ignore_index=True)
    companies['Industry Groups'] = companies['Industry Groups'].apply(lambda x:', '.join(x) if isinstance(x, list) else '')
    companies['affiliates'] = companies['affiliates'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')
    companies['affiliates_id'] = companies['affiliates_id'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')
    
    companies = companies.astype(str)
    com_founder = com_founder.astype(str)
    com_ind = com_ind.astype(str)

    return [companies,com_founder,com_ind]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
