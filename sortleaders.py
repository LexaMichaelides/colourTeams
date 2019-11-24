import numpy as np
import pandas as pd

def create_leader_groups(path, num_groups,num_se_groups):
    
    inputdf = pd.read_csv(path)

    # replace "U" and "A" genders with a random choice of {"F", "M"}
    genders = ["M", "F"]
    inputdf['gender'] = inputdf['gender'].replace("U", np.random.choice(genders, 1)[0])
    inputdf['gender'] = inputdf['gender'].replace("A", np.random.choice(genders, 1)[0])

    # program bins
    arch = ["AE", "ARCH"]
    civ = ["CIVE", "GEO", "ENV"]
    ece = ["COMP", "ECE"]
    mech = ["MECH", "TRON"]

    bins = [arch, civ, ece, mech]

    # use anonymous function to rename program to their parent programs concatenated by "/"
    for bin in bins:
        inputdf['program'] = inputdf.apply(lambda x: "/".join(bin) if x['program'] in bin else x['program'], axis=1)

    df = inputdf


    # assign leaders to gorups
    df = df.sort_values(by=['program', 'gender', 'returnBig', 'returnHuge'])
    group = 0
    se_group = 0
    group_size = int(inputdf.shape[0]/num_groups)
    group_count = [0] * num_groups

    for i, row in df.iterrows():

        if row['program'] == 'SE':
            df.at[i, 'group'] = se_group + 1
            if se_group == num_se_groups - 1:
                se_group = 0
            else:
                se_group += 1
            
        else:
            if group_count[group] < group_size:
                df.at[i, 'group'] = group + 1
                group_count[group] += 1
            else:
                while group_count[group] > group_size:
                    group += 1
                df.at[i, 'group'] = group + 1
                group_count[group] += 1

            if group == num_groups - 1:
                group = 0
            else:
                group += 1
                
    # anti requests
    df['watIam'] = df['watIam']

    antiDF = df[df['anti1'].notnull()]
    antiDF['anti1group'] = ""
    antiDF['anti2group'] = ""

    # get the group that your anti request belongs
    for i, row in antiDF.iterrows():
        # searches df for name and fetches their respective group
        antiDF['anti1group'][i] = df[df['watIam'] == row['anti1']]['group'].values
        antiDF['anti2group'][i] = df[df['watIam'] == row['anti2']]['group'].values
        # handle case when name not found
        if antiDF['anti1group'][i].size == 0:
            antiDF['anti1group'][i] = [0]
        antiDF['anti1group'][i] = antiDF['anti1group'][i][0]
        if antiDF['anti2group'][i].size == 0:
            antiDF['anti2group'][i] = [0]
        antiDF['anti2group'][i] = antiDF['anti2group'][i][0]

    # move anti-requests in antiDF
    groups = list(range(1, num_groups + 1))
    antiDF['group'] = antiDF.apply(
        lambda x: np.random.choice(list(set(groups) - set(antiDF['anti1group']) - set(antiDF['anti2group'])), 1)[0] if
        x['group'] == x[
            'anti1group'] else x['group'], axis=1)

    # apply changes to entire dataframe
    anti_free_df = df.copy()

    for i, row in antiDF.iterrows():
        anti_free_df['group'][i] = antiDF['group'][i]

    return anti_free_df
