import numpy as np
import pandas as pd 
import os


class sortingalgo:
    
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


    def create_student(path):

        #read in data from CSV file 
        data = pd.read_csv(path)

        data['gender'] = data['gender'].replace('A','F')
        data['gender'] = data['gender'].replace('U','F')

        df = data

        df['group'] = np.random.randint(1, 19, df.shape[0])

        summary = df.groupby(['group', 'gender']).size().reset_index(name='counts')
        
        return df

    
    local_directory = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + os.sep + os.pardir)
    

    leader_data = create_leader_groups(os.path.join(local_directory, 'test_files/Simulated Leader Data.csv'))
    
    student_data = create_student(os.path.join(local_directory, 'test_files/Simulated First Year Data.csv'))
    

    combined_data = pd.merge(leader_data, student_data, how='outer', on=['id', 'last_name', 'first_name', 'program',
                                                                         'gender', 'email', 'watIam', 'group'])

    combined_data.to_csv((os.path.join(local_directory, 'sorted_output.csv')), index=False)
