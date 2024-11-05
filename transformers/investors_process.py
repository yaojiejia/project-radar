import pandas as pd
import re
import numpy as np

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def filter_school(text):
    '''
    This function removes schools that are not in NYU
    '''
    ar = text.split(', ')
    pattern = re.compile(r'^(NYU|New York University)')
    result = [s.replace('New York University', 'NYU') for s in ar if pattern.match(s)]
    return result if result else np.nan

def fill_name(row):
    if pd.isna(row['Full Name']):
        return row['Full Name_y']
    else: 
        return row['Full Name']
    
def fill_linkedIn(row):
    if pd.isna(row['Linkedin']):
        return row['LinkedIn_y']
    else: 
        return row['Linkedin']

def fill_location(row):
    if pd.isna(row['Location']):
        return row['Location_y']
    else: 
        return row['Location']
    
def fill_facebook(row):
    if pd.isna(row['Facebook']):
        return row['Facebook_y']
    else: 
        return row['Facebook']
    
def fill_number_of_investments(row):
    if pd.isna(row['Number of Investments']):
        return row['Number of Investments_y']
    else: 
        return row['Number of Investments']
    
def fill_number_of_partner_investments(row):
    if pd.isna(row['Number of Partner Investments']):
        return row['Number of Partner Investments_y']
    else: 
        return row['Number of Partner Investments']
    
def fill_number_of_lead_investments(row):
    if pd.isna(row['Number of Lead Investments']):
        return row['Number of Lead Investments_y']
    else: 
        return row['Number of Lead Investments']
    
def fill_primary_job_title(row):
    if pd.isna(row['Primary Job Title']):
        return row['Primary Job Title_y']
    else: 
        return row['Primary Job Title']

def fill_organization_url(row):
    if pd.isna(row['Primary Organization URL']):
        return row['Primary Organization URL_y']
    else: 
        return row['Primary Organization URL']

def fill_organization(row):
    if str(row['Primary Organization']) in str(row['Primary Organization_y']): return str(row['Primary Organization_y'])
    elif str(row['Primary Organization']) not in str(row['Primary Organization_y']): return str(row['Primary Organization_y']) + str(row['Primary Organization'])
    else: return str(row['Primary Organization_y'])

def fill_school(row):
    if pd.isna(row['Schools Attended']):
        return row['Schools Attended_y']
    else: 
        return row['Schools Attended']


@transformer
def transform_investors(data, *args, **kwargs):
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
    small_inv = data[0]
    big_inv = data[1]
    if args[0].empty: investors_existing = pd.DataFrame()
    else: investors_existing = args[0]
    merged_investor = pd.DataFrame() 

    print(small_inv.shape, big_inv.shape,investors_existing.shape)

    if small_inv.empty and big_inv.empty:
        print('no investors found')
        return [pd.DataFrame(), pd.DataFrame()]
    elif not small_inv.empty and not big_inv.empty: 
        # small_inv.rename(columns={'Organization/Person Name': 'Full Name'}, inplace=True)
        # small_inv.rename(columns={'Organization/Person Name URL': 'Full Name URL'}, inplace=True)

        big_inv.rename(columns={'Organization/Person Name': 'Full Name'}, inplace=True)
        big_inv.rename(columns={'Organization/Person Name URL': 'Full Name URL'}, inplace=True)
        big_inv['Schools Attended'] = 'NYU'

        merged_investor = pd.merge(small_inv, big_inv,how='outer', on='Full Name URL')

        merged_investor.rename(columns={'Full Name_x': 'Full Name'}, inplace=True)
        merged_investor['Full Name'] = merged_investor.apply(fill_name,axis=1)

        merged_investor.rename(columns={'LinkedIn_x': 'Linkedin'}, inplace=True)
        merged_investor['Linkedin'] = merged_investor.apply(fill_linkedIn,axis=1)
        
        merged_investor.rename(columns={'Location_x': 'Location'}, inplace=True)
        merged_investor['Location'] = merged_investor.apply(fill_location,axis=1)

        merged_investor.rename(columns={'Facebook_x': 'Facebook'}, inplace=True)
        merged_investor['Facebook'] = merged_investor.apply(fill_facebook,axis=1)

        merged_investor.rename(columns={'Number of Investments_x': 'Number of Investments'}, inplace=True)
        merged_investor['Number of Investments'] = merged_investor.apply(fill_number_of_investments,axis=1)
        
        merged_investor.rename(columns={'Number of Partner Investments_x': 'Number of Partner Investments'}, inplace=True)
        merged_investor['Number of Partner Investments'] = merged_investor.apply(fill_number_of_partner_investments,axis=1)

        merged_investor.rename(columns={'Number of Lead Investments_x': 'Number of Lead Investments'}, inplace=True)
        merged_investor['Number of Lead Investments'] = merged_investor.apply(fill_number_of_lead_investments,axis=1)

        merged_investor.rename(columns={'Schools Attended_x': 'Schools Attended'}, inplace=True)
        merged_investor['Schools Attended'] = merged_investor.apply(fill_school,axis=1)

        merged_investor.rename(columns={'Primary Job Title_x': 'Primary Job Title'}, inplace=True)
        merged_investor['Primary Job Title'] = merged_investor.apply(fill_primary_job_title,axis=1)

        merged_investor.rename(columns={'Primary Organization URL_x': 'Primary Organization URL'}, inplace=True)
        merged_investor['Primary Organization URL'] = merged_investor.apply(fill_organization_url,axis=1)

        merged_investor.rename(columns={'Primary Organization_x': 'Primary Organization'}, inplace=True)
        merged_investor['Primary Organization'] = merged_investor.apply(fill_organization,axis=1)

        merged_investor = merged_investor.drop(['LinkedIn_y','Schools Attended_y','Primary Job Title_y','Primary Organization_y','Primary Organization URL_y','Number of Lead Investments_y','Number of Investments_y','Number of Partner Investments_y','Location_y','Facebook_y','Founded Date','Founded Date Precision','Industry Groups','CB Rank (Person)_x','Full Name_y','CB Rank (Person)_y'], axis=1)
        
    merged_investor = merged_investor.reset_index(drop=True)

    
    if investors_existing.empty: 
        unique_investors = merged_investor
    else:
        unique_investors = merged_investor[~merged_investor['Full Name URL'].isin(investors_existing['Full Name URL'])]
    
    unique_investors = unique_investors.sort_values(by='Full Name')
    
    # create primary key
    unique_investors.reset_index(inplace=True, names='person_id')

    # # process schools column
    unique_investors['nyu_school'] = unique_investors['Schools Attended'].astype(str).apply(filter_school)
    
    unique_investors = unique_investors.loc[unique_investors['nyu_school'].notnull()]
    unique_investors = unique_investors.sort_values('nyu_school',ascending=False)
    unique_investors = unique_investors[~(unique_investors['Current Organizations'].isna() & unique_investors.duplicated(subset='Full Name URL', keep=False) == True)]
    
    # create investor_school join table
    unique_investors['person_id'] = ['INV_' + str(i) for i in range(len(investors_existing)+1, len(unique_investors) + 1 + len(investors_existing))]
    investor_school = unique_investors[['person_id', 'nyu_school']].explode('nyu_school', ignore_index=True)
    
    unique_investors = unique_investors.reset_index(drop=True)
    investor_school = investor_school.reset_index(drop=True)
    
    return [unique_investors, investor_school]

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'