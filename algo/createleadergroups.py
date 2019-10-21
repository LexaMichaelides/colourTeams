import numpy as np
import pandas as pd 

def create_leader_groups(path):
    inputdf = pd.read_csv(path)

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

    programs = ['AE/ARCH', 'BME', 'CHE', 'CIVE/GEO/ENV', 'COMP/ECE', 'MECH/TRON',
        'MGTE', 'NANO', 'SE', 'SYDE']

    groups = range(1,19)

    df = inputdf

    #assign leaders based on rand unif distribution [1,19)
    df['group'] = np.random.randint(1, 19, df.shape[0]) 

    return df