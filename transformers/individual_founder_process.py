if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import re
import numpy as np
def filter_school(text):
    '''
    This function removes schools that are not in NYU
    '''
    ar = text.split(', ')
    pattern = re.compile(r'^(NYU|New York University)')
    result = [s.replace('New York University', 'NYU') for s in ar if pattern.match(s)]
    return result if result else np.nan



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
    founders_new = data[2]
    founders_existing = args[0]

    if founders_new.empty: 
        print('no founder to proecess')
        return [pd.DataFrame(),pd.DataFrame()]


    # rows which are unique
    if not founders_existing.empty: 
        unique_founders = founders_new[~founders_new['Full Name URL'].isin(founders_existing['Full Name URL'])]
    else: 
        unique_founders = founders_new
    # rows which are same
    # repeated_founder = load_founder[load_founder['Full Name URL'].isin(existing_founder_db['full_name_url'])]
    
    # Specify your transformation logic here
    unique_founders.sort_values(by='Full Name')

    # process school
    unique_founders['nyu_school'] = unique_founders['Schools Attended'].astype(str).apply(filter_school)

    # give unique key
    unique_founders['person_id'] = range(founders_existing.shape[0]+1,founders_existing.shape[0]+1+len(unique_founders))
    person_columns = unique_founders.pop('person_id')
    unique_founders.insert(0,'person_id',person_columns)
    unique_founders['person_id'] = 'FOUND_' + unique_founders['person_id'].astype(str)
    unique_founders.reset_index(drop=True)

    # create founder_school join table
    founder_school = unique_founders[['person_id', 'nyu_school']].explode('nyu_school', ignore_index=True)
    
    unique_founders.reset_index(drop=True,inplace=True)
    return [unique_founders,founder_school]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
