#load in Pandas library with alias 'pd'
import pandas as pd
import numpy as np

def create_student(path):

    #read in data from CSV file 
    data = pd.read_csv(path)

    data['gender'] = data['gender'].replace('A','F')
    data['gender'] = data['gender'].replace('U','F')

    df = data

    df['group'] = np.random.randint(1, 19, df.shape[0])

    summary = df.groupby(['group', 'gender']).size().reset_index(name='counts')
    
    return df
