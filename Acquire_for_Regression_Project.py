import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

import env

        ####################################################################################
                                    # ACQUIRE DATA #
#####################################################################################

def get_db_url(db, user = env.user, password = env.password, host = env.host):
    ''' This function takes in the name of a database, and imported 
            username, password, and host from an env file and returns
            the url that accesses that database'''
    
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'
            
        
    
        
def new_zillow_data():
    ''' 
    This function uses a SQL query to select desired features from the zillow dataset 
    from the Codeup database and returns them in a dataframe
    '''
    
    sql_query = '''
        SELECT bathroomcnt,
            bedroomcnt,
            taxvaluedollarcnt,
            calculatedfinishedsquarefeet,
            yearbuilt,
            fips,
            lotsizesquarefeet
        FROM properties_2017 
        JOIN predictions_2017 USING (parcelid)
        JOIN propertylandusetype USING (propertylandusetypeid)
        WHERE propertylandusedesc IN ('Single Family Residential' , 'Inferred Single Family Residential')
                AND YEAR(transactiondate) = 2017;
                '''
    df = pd.read_sql(sql_query, get_db_url(db= 'zillow'))
    
    return df


def aquire_zillow_data(new = False):
    ''' 
    Checks to see if there is a local copy of the data, 
    if not or if new = True then go get data from Codeup database
    '''
    
    filename = 'zillow.csv'
    
    #if we don't have cached data or we want to get new data go get it from server
    if (os.path.isfile(filename) == False) or (new == True):
        df = new_zillow_data()
        #save as csv
        df.to_csv(filename,index=False)

    #else used cached data
    else:
        df = pd.read_csv(filename)
          
    return df


#####################################################################################
                               # CLEAN DATA #
#####################################################################################

def clean_data(df):
    
    #create column to calculate the age of the property
    df['property_age'] = 2017 - df['yearbuilt']
    
    #rename columns
    df = df.rename(columns = {'bedroomcnt':'bed_rooms', 
                          'bathroomcnt':'bath_rooms',
                          'calculatedfinishedsquarefeet':'house_square_feet',
                          'taxvaluedollarcnt':'property_value', 
                          'lotsizesquarefeet':'property_square_feet'}) 
    
    # replace whitespace with null value
    df = df.replace(r'^\s*$', np.nan, regex=True)
    
    # drop null values
    df = df.dropna()
    
    
    # change datatypes
    df["year_built"] = df["yearbuilt"].astype(int)
    df["bed_rooms"] = df["bed_rooms"].astype(int)  
    df["bath_rooms"] = df["bath_rooms"].astype(int) 
    df["house_square_feet"] = df["house_square_feet"].astype(int)
    df["property_age"] = df["property_age"].astype(int)
    df["property_square_feet"] = df["property_square_feet"].astype(int)
    
    # Killing off outliers
    df=df[df.bed_rooms <=5]
    df=df[df.bath_rooms <=5]
    df=df[df.house_square_feet <= 7000]
    df=df[df.property_value <= 1300000]    
    
    
    # rename fips to county names
    df['county'] = df.fips.replace({6037:'LA', 6059:'Orange', 6111:'Ventura'})
    
    #get dummies for counties
    dummy_df = pd.get_dummies(df[['county']], dummy_na=False, drop_first=[True, True])
    df = pd.concat([df, dummy_df], axis=1)
    
    # drop unwanted columns
    df = df.drop(columns = ["fips", "yearbuilt"])
    # using .loc to delete all rows where bath_room = 0
    df = df.loc[df["bath_rooms"] !=0]
    
    return df



###################################################################################
                                    #SPLIT DATA#
###################################################################################

def split_data(df):
    train_validate, test = train_test_split(df, test_size=.2, 
                                        random_state=1989)
    train, validate = train_test_split(train_validate, test_size=.3, 
                                   random_state=1989)
    return train, validate, test





