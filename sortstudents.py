import numpy as np
import pandas as pd

def create_first_year_groups(first_year_data, leader_sorted_data):
    # read in data from CSV file
    data = pd.read_csv(first_year_data)
    leaders = pd.read_csv(leader_sorted_data)
    
    #create leader summary
    leaders = leaders.groupby(['group', 'program']).size().reset_index(name='counts')
    
    #replace genders to be F
    data['gender'] = data['gender'].replace('A', 'F')
    data['gender'] = data['gender'].replace('U', 'F')

    # program bins
    arch = ["AE", "ARCH"]
    civ = ["CIVE", "GEO", "ENV"]
    ece = ["COMP", "ECE"]
    mech = ["MECH", "TRON"]

    bins = [arch, civ, ece, mech]

    # use anonymous function to rename program to their parent programs concatenated by "/"
    for bin in bins:
        data['program'] = data.apply(lambda x: "/".join(bin) if x['program'] in bin else x['program'], axis=1)

    program = ['AE/ARCH', 'BME', 'CHE', 'CIVE/GEO/ENV', 'COMP/ECE', 'MECH/TRON',
               'MGTE', 'NANO', 'SE', 'SYDE']

    df = data
    df = df.groupby(['program', 'gender', 'watIam', 'first_name', 'last_name', 'email', 'id']).size().reset_index(name='counts')

    #set counter variables
    s = df.shape[0] - 1
    j = 0
    k = 0
    n = 1
    numberofprograms = 11

    #create dataframe for final list of students
    StudentFinaldf = pd.DataFrame(
        columns=['program', 'gender', 'watIam', 'first_name', 'last_name', 'email', 'id'])

    #create dataframe to be used for each program
    teamdf = pd.DataFrame(columns=['program', 'gender', 'watIam', 'first_name', 'last_name', 'email', 'id'])
    
    #loop through each program and assign teams
    for n in range(1, numberofprograms):
        
        #make temporary df with all students in one program
        teamdf = pd.DataFrame(columns=['program', 'gender', 'watIam', 'first_name', 'last_name', 'email', 'id'])
        while df.iat[j, 0] == df.iat[j + 1, 0]:
            teamdf.loc[j] = [df.iat[k, 0], df.iat[k, 1], df.iat[k, 2], df.iat[k, 3], df.iat[k, 4], df.iat[k, 5],
                             df.iat[k, 6]]
            j = j + 1
            k = k + 1
            if j == df.shape[0] - 1:
                break
        teamdf.loc[j] = [df.iat[k, 0], df.iat[k, 1], df.iat[k, 2], df.iat[k, 3], df.iat[k, 4], df.iat[k, 5],
                         df.iat[k, 6]]
        j = j + 1
        k = k + 1

        #get all team numbers students of a program can be assigned to based on leaders
        h = 0
        availteamsdf = pd.DataFrame(columns=['group'])
        for i, row in leaders.iterrows():
            if row['program'] == teamdf.iat[0, 0]:
                availteamsdf.loc[h] = row['group']
                h = h + 1
        
        #assign all students in one program to respective teams
        l = 0
        m = 0
        studentAssigndf = pd.DataFrame(columns=['group'])
        for l, row in teamdf.iterrows():
            studentAssigndf.loc[l] = availteamsdf.iat[m, 0]
            if m == availteamsdf.shape[0] - 1:
                m = 0
            else:
                m = m + 1

        #add column of team numbers to student list
        mergeddf = pd.concat([teamdf, studentAssigndf], axis=1)

        #merge temp list of studnts to final list
        StudentFinaldf = pd.concat([StudentFinaldf, mergeddf], axis=0, sort=False)
    return StudentFinaldf