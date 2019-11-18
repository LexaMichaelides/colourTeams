import numpy as np
import pandas as pd 

def create_leader_summary(sorted_leader_data_path):
    leaderdf = pd.read_csv(sorted_leader_data_path)
    summary = leaderdf.groupby(['group', 'program','returnBig', 'returnHuge','gender']).size().reset_index(name='counts')
    return summary

def initial_leader_summary(leaderdf):
    summary = leaderdf.groupby(['group', 'program','returnBig', 'returnHuge','gender']).size().reset_index(name='counts')
    return summary    

def create_first_year_summary(groupdf):
    summary = groupdf.groupby(['group', 'program']).size().reset_index(name='counts')
    return summary

