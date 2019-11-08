import numpy as np
import pandas as pd 
import os

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
    
    df = df.groupby(['program', 'gender','watIam']).size().reset_index(name='counts')
    
    #teamdf = pd.DataFrame(columns=['program', 'gender', 'watIam'])
    s = df.shape[0]-1
    #need to make dynamic in future to change number of programs
    j=0
    k=0
    n=1
    numberofprograms = 11
    StudentFinaldf = pd.DataFrame(columns=['program', 'gender', 'watIam', 'team number'])
    teamdf = pd.DataFrame(columns=['program', 'gender', 'watIam'])
    for n in range(1,numberofprograms):
        teamdf = pd.DataFrame(columns=['program', 'gender', 'watIam'])
        while df.iat[j,0] == df.iat[j+1,0]:
            teamdf.loc[j] = [df.iat[k,0],df.iat[k,1],df.iat[k,2]]
            j=j+1
            k=k+1
            if j == df.shape[0]-1:
                break
        teamdf.loc[j] = [df.iat[k,0],df.iat[k,1],df.iat[k,2]]
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



