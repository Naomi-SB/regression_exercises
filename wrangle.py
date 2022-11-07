from env import get_db_url
import pandas as pd
import numpy as np
import os


def acquire_zillow_data(new = False):
    ''' 
    Checks to see if there is a local copy of the data, 
    if not or if new = True then go get data from Codeup database
    '''
    
    filename = 'zillow.csv'
    
    #if we don't have cached data or we want to get new data go get it from server
    if (os.path.isfile(filename) == False) or (new == True):
           # Create SQL query
        query =  'SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips FROM properties_2017 WHERE propertylandusetypeid = 261'
     
        # read in dataframe
        df = pd.read_sql(query, get_db_url('zillow'))
        #save as csv
        df.to_csv(filename,index=False)

    #else used cached data
    else:
        df = pd.read_csv(filename)
          
    return df


def wrangle_zillow():
    '''
    This function reads zillow data from the SQL database into a df.
    '''
    df = acquire_zillow_data()
    
    # Drop nulls
    df = df.dropna()
    
    # Eliminate whitespace
    df = df.replace(r'^\s*$', np.NaN, regex=True)
    
    
    return df


