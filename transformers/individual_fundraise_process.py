if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd


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
    fundraise = data[3]

    if fundraise.empty: 
        print('nothing to append')
        return pd.DataFrame()

    fundraise = fundraise.rename(columns={
    'Money Raised Currency (in USD)': 'Money Raised (in USD)',
    'Total Funding Amount Currency (in USD)': 'Total Funding Amount (in USD)',
    'Funding Status (Fundraising)': 'Funding Status',
    })

    fundraise['Transaction Name'] = ''
    fundraise['Transaction Name URL'] = ''
    fundraise['Organization Industries'] = fundraise['Industry Groups']
    fundraise['Organization Location'] = fundraise['Headquarters Location']
    fundraise['Organization Name URL'] = ''
    fundraise['Money Raised'] = ''
    fundraise['Money Raised Currency'] = ''
    fundraise['Total Funding Amount'] = ''
    fundraise['Total Funding Amount Currency'] = ''
    fundraise['Investor Names'] = fundraise['Top 5 Investors']
    fundraise['Funding Stage'] = ''
    fundraise['Number of Partner Investors'] = ''
    fundraise['Organization Revenue Range'] = fundraise['Estimated Revenue Range']
    fundraise['Organization Website'] = fundraise['Website']
    fundraise['Pre-Money Valuation'] = ''
    fundraise['Pre-Money Valuation Currency'] = ''
    fundraise['Pre-Money Valuation (in USD)'] = ''
    fundraise['Organization Description'] = fundraise['Description']
    fundraise['CB Rank (Funding Round)'] = ''

    fundraise = fundraise.drop(['Operating Status','IPO Status','Website','Estimated Revenue Range','Description','Headquarters Location','Contact Email','LinkedIn','Company Type','Top 5 Investors','Founded Date','Founders','Number of Employees','Number of Founders','Industry Groups'], axis=1)



    return fundraise



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
