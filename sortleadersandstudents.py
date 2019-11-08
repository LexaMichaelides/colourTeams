import numpy as np
import pandas as pd 
import os

def create_leader_groups(path):
    inputdf = pd.read_csv(path)

    num_groups = 18
    
    #replace "U" and "A" genders with a random choice of {"F", "M"}
    genders = ["M", "F"]
    inputdf['gender'] = inputdf['gender'].replace("U", np.random.choice(genders, 1)[0])
    inputdf['gender'] = inputdf['gender'].replace("A", np.random.choice(genders, 1)[0])

    #program bins
    arch = ["AE", "ARCH"]
    civ = ["CIVE", "GEO", "ENV"]
    ece = ["COMP", "ECE"]
    mech = ["MECH", "TRON"]

    bins = [arch, civ, ece, mech]

    #use anonymous function to rename program to their parent programs concatenated by "/"
    for bin in bins:
        inputdf['program'] = inputdf.apply(lambda x: "/".join(bin) if x['program'] in bin else x['program'], axis=1)

    df = inputdf

    #assign leaders based on rand unif distribution [1,19)
    df['group'] = np.random.randint(1, 19, df.shape[0]) 

    #anti requests
    df['name'] = df['last_name'] + ", " + df['first_name']

    antiDF = df[df['anti1'].notnull()]
    antiDF['anti1group'] = ""

    #get the group that your anti request belongs
    for i, row in antiDF.iterrows():
        #searches df for name and fetches their respective group
        antiDF['anti1group'][i] = df[df['name'] == row['anti1']]['group'].values
        #handle case when name not found
        if antiDF['anti1group'][i].size == 0:
            antiDF['anti1group'][i] = [0]
        antiDF['anti1group'][i] = antiDF['anti1group'][i][0]

    #move anti-requests in antiDF
    groups = list(range(1,num_groups+1))
    antiDF['group'] = antiDF.apply(lambda x: np.random.choice(list(set(groups) - {(antiDF['anti1group'][7])}), 1)[0] if x['group'] == x['anti1group'] else x['group'], axis=1)

    #apply changes to entire dataframe
    anti_free_df = df.copy()

    for i, row in antiDF.iterrows():
        anti_free_df['group'][i] = antiDF['group'][i]

    anti_free_df = anti_free_df.drop(['name'], axis = 1)

    return anti_free_df


def create_student_groups(path):

    #read in data from CSV file 
    data = pd.read_csv(path)

    data['gender'] = data['gender'].replace('A','F')
    data['gender'] = data['gender'].replace('U','F')

    df = data

    df['group'] = np.random.randint(1, 19, df.shape[0])

    summary = df.groupby(['group', 'gender']).size().reset_index(name='counts')
    
    return df


