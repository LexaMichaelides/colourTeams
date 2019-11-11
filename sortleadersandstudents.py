import numpy as np
import pandas as pd 

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

    #sorting by gender and program 
    df=df.sort_values(by =['program','gender']) 
    #assign leaders based on unif distribution [1,19)
    m=0
    for l, row in df.iterrows():
        if m == 18:
            m=1
            df.at[l,'group']=m 
        else:
            m=m+1
            df.at[l,'group']=m 

    #software engineering into 6 teams 
    n=0
    for l, row in df.loc[df['program'] == 'SE'].iterrows():
        if n == 6:
            n=1
            df.at[l,'group']=n
        else:
            n=n+1
            df.at[l,'group']=n

    #anti requests
    df['watIam'] = df['watIam']

    antiDF = df[df['anti1'].notnull()]
    antiDF['anti1group'] = ""

    #get the group that your anti request belongs
    for i, row in antiDF.iterrows():
        #searches df for name and fetches their respective group
        antiDF['anti1group'][i] = df[df['watIam'] == row['anti1']]['group'].values
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

    return anti_free_df

def create_student_groups(first_year_data, leader_summary):

     #read in data from CSV file 
     data = pd.read_csv(first_year_data)
     leaders = pd.read_csv(leader_summary)

     data['gender'] = data['gender'].replace('A','F')
     data['gender'] = data['gender'].replace('U','F')

     #program bins
     arch = ["AE", "ARCH"]
     civ = ["CIVE", "GEO", "ENV"]
     ece = ["COMP", "ECE"]
     mech = ["MECH", "TRON"]

     bins = [arch, civ, ece, mech]

     #use anonymous function to rename program to their parent programs concatenated by "/"
     for bin in bins:
         data['program'] = data.apply(lambda x: "/".join(bin) if x['program'] in bin else x['program'], axis=1)

     program = ['AE/ARCH', 'BME', 'CHE', 'CIVE/GEO/ENV', 'COMP/ECE', 'MECH/TRON',
         'MGTE', 'NANO', 'SE', 'SYDE']

     groups = range(1,19)

     df = data

     df['group'] = np.random.randint(1, 19, df.shape[0])

     df = df.groupby(['program', 'gender','watIam', 'first_name', 'last_name', 'email', 'id']).size().reset_index(name='counts')

     #teamdf = pd.DataFrame(columns=['program', 'gender', 'watIam'])
     s = df.shape[0]-1
     #need to make dynamic in future to change number of programs
     j=0
     k=0
     n=1
     numberofprograms = 11
     StudentFinaldf = pd.DataFrame(columns=['program', 'gender', 'watIam', 'first_name', 'last_name', 'email', 'id', 'team number'])
     teamdf = pd.DataFrame(columns=['program', 'gender', 'watIam', 'first_name', 'last_name', 'email', 'id'])
     for n in range(1,numberofprograms):
         teamdf = pd.DataFrame(columns=['program', 'gender', 'watIam', 'first_name', 'last_name', 'email', 'id'])
         while df.iat[j,0] == df.iat[j+1,0]:
             teamdf.loc[j] = [df.iat[k,0],df.iat[k,1],df.iat[k,2],df.iat[k,3],df.iat[k,4],df.iat[k,5],df.iat[k,6]]
             j=j+1
             k=k+1
             if j == df.shape[0]-1:
                 break
         teamdf.loc[j] = [df.iat[k,0],df.iat[k,1],df.iat[k,2],df.iat[k,3],df.iat[k,4],df.iat[k,5],df.iat[k,6]]
         j=j+1
         k=k+1

         h=0
         availteamsdf = pd.DataFrame(columns=['team number'])
         for i, row in leaders.iterrows():
             if row['program'] == teamdf.iat[0,0]:
                 availteamsdf.loc[h] = row['group']
                 h=h+1
         l=0
         m=0
         studentAssigndf = pd.DataFrame(columns=['team number'])        
         for l, row in teamdf.iterrows():
             studentAssigndf.loc[l] = availteamsdf.iat[m,0]
             if m == availteamsdf.shape[0]-1:
                 m=0
             else:
                 m=m+1

         mergeddf = pd.concat([teamdf, studentAssigndf], axis = 1)

         StudentFinaldf = pd.concat([StudentFinaldf, mergeddf], axis = 0)
     StudentFinaldf.to_csv('StudentSummary.csv')
     return StudentFinaldf
