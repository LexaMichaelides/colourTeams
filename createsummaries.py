import numpy as np
import pandas as pd 

def create_leader_summary(groupdf):
    summary = groupdf.groupby(['group', 'program']).size().reset_index(name='counts')
    return summary

def create_first_year_summary(groupdf):
    summary = groupdf.groupby(['group', 'program']).size().reset_index(name='counts')
    return summary

