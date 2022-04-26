import pandas as pd
import numpy as np

def load_data(name):
    df = pd.read_csv(name, index_col=0,
    dtype = { # indicate categorical variables
        'A': 'category',
        'B': 'category',
        'C': 'category',
        'D': 'category',
        'E': 'category',
        'F': 'category',
        'G': 'category',
        'car_value': 'category',
        'state': 'category'
    })
    df = df.dropna()
    return df

def onehot_encode_attribute(df, attr):
    oh_dict = {}
    values = df[attr].unique() 
    for i in range(len(values)):
        key = values[i]
        value = df[df[attr] == values[i]][attr]
        oh_dict[key] = value
    
    oh_dict = pd.DataFrame(oh_dict)
        
    oh_dict_nnan = {}
    for v in values:
        categories = list(oh_dict[v].cat.categories)
        if('0' not in categories and '1' not in categories):
            oh_dict_nnan[v] = oh_dict[v].cat.add_categories(["0", "1"])
            oh_dict_nnan[v].loc[pd.isna(oh_dict_nnan[v])] = '0'
            oh_dict_nnan[v].loc[oh_dict_nnan[v] == v] = '1'
        elif('0' not in categories and '1' in categories):
            oh_dict_nnan[v] = oh_dict[v].cat.add_categories("0")
            oh_dict_nnan[v].loc[pd.isna(oh_dict_nnan[v])] = '0'
            oh_dict_nnan[v].loc[oh_dict_nnan[v] == v] = '1'
        elif('0' in categories and '1' not in categories):
            oh_dict_nnan[v] = oh_dict[v].cat.add_categories("1")
            oh_dict_nnan[v].loc[pd.isna(oh_dict_nnan[v])] = '0'
            oh_dict_nnan[v].loc[oh_dict_nnan[v] == v] = '1'
        else:
            oh_dict_nnan[v] = oh_dict[v]
            oh_dict_nnan[v].loc[pd.isna(oh_dict_nnan[v])] = '0'
            oh_dict_nnan[v].loc[oh_dict_nnan[v] == v] = '1'
    
    oh_dict = oh_dict_nnan
    dfres = df.drop(attr, axis=1)
    
    for cv in oh_dict:
        k = f"{attr}_{cv}"
        if(not k in dfres):
            dfres[k] = oh_dict[cv]
            #print(dfres[k])
            replaced = dfres[k].replace(['1','0'], [1,0], inplace=True)
            #print(replaced)
    
    # print(dfres)
    return dfres

def split_data(df,seed, ratio): 
    np.random.seed(seed)
    r = np.random.rand(len(df)) < ratio
    train = df[r]
    test = df[~r]
    return train, test

def categorical_to_int(df): 
    non_categorical = df.drop(df.select_dtypes(exclude=["number","bool_","object_"]).columns, axis=1)
    categorical = df.drop(df.select_dtypes(exclude=["category"]).columns, axis=1)
    for c in categorical:
        col = categorical[c].to_numpy()
        categorical = categorical.drop(c, axis=1)
        categorical[c] = col.astype("int64")

    newdf = pd.concat([non_categorical, categorical], axis=1)
    return newdf

def preprocess_data(df_original):
    state_regions = pd.read_csv('https://raw.githubusercontent.com/cphalpert/census-regions/master/us%20census%20bureau%20regions%20and%20divisions.csv')
    
    # Modifiying dataset again
    regions = {}
    for state in df_original["state"].unique():
        s = state_regions[state_regions["State Code"] == state]["Region"]
        # help(s)
        #print(s.index)
        # print(s[s.index])
        regions[state] = s
    
    df_original["region"] = df_original["state"]
    
    for r in regions:
        regions[r] = list(regions[r])[0]
    
    df_original["region"] = df_original["region"].map(regions)
    df_original = df_original.drop("state", axis=1)
    df_original["region"] = df_original["region"].astype("category")
    
    # ENCODE CATEGORICAL AGAIN
    df_encoded = onehot_encode_attribute(df_original, "car_value")
    df_encoded = onehot_encode_attribute(df_encoded, "region")
    df_encoded = onehot_encode_attribute(df_encoded, "A")
    df_encoded = onehot_encode_attribute(df_encoded, "B")
    df_encoded = onehot_encode_attribute(df_encoded, "C")
    df_encoded = onehot_encode_attribute(df_encoded, "D")
    df_encoded = onehot_encode_attribute(df_encoded, "E")
    df_encoded = onehot_encode_attribute(df_encoded, "F")
    df_encoded = onehot_encode_attribute(df_encoded, "G")
    
    df_encoded = categorical_to_int(df_encoded)
    
    # Add interactions
    df_encoded['age_youngest_sq'] = df_encoded["age_youngest"] ** 2
    df_encoded['car_age_sq'] = df_encoded["car_age"] ** 2

    # Interactions car_value
    car_values = ['f','d','e','h','g','c','i','a','b']
    for cv in car_values:
        new_ft = f'I_age_youngest_car_value_{cv}'
        it_1 = "age_youngest" # interactor 1
        it_2 = f"car_value_{cv}" # interactor 2
        df_encoded[new_ft] = df_encoded[it_1] * df_encoded[it_2]
    
    print(df_encoded.columns)
    train, test = split_data(df_encoded,1337, 0.7)

    return train
