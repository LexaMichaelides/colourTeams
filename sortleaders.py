import numpy as np
import pandas as pd

def create_leader_groups(path):
    inputdf = pd.read_csv(path)

    num_groups = 18

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

    # sorting by gender and program
    df = df.sort_values(by=['program', 'gender'])
    # assign leaders based on unif distribution [1,19)
    m = 0
    for l, row in df.iterrows():
        if m == 18:
            m = 1
            df.at[l, 'group'] = m
        else:
            m = m + 1
            df.at[l, 'group'] = m

            # software engineering into 6 teams
    n = 0
    for l, row in df.loc[df['program'] == 'SE'].iterrows():
        if n == 6:
            n = 1
            df.at[l, 'group'] = n
        else:
            n = n + 1
            df.at[l, 'group'] = n

    df['group'] = df['group'].round(0).astype(int)

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
