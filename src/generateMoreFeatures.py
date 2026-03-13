import os
import pandas as pd
import numpy as np

def moreFeatures(file):
    path = '../data/preprocess/'
    df = pd.read_csv(f'{path}merged_team_matchups.csv')
    #with open(os.path.join(path,file), 'r') as f:
        #df = pd.read_csv(f)
        #print(df.head())
    '''
    We already have majority of new features needed
        - SeedDiff
        - Elo_LowerTeam1
        - Elo_HigherTeam2
        - Seed_LowerTeam1
        - Seed_higherTeam2 
        Need to calculate
        - Elo * abs(SeedDiff)
        - EloDiffSQRD
        - SeedSum- 
    '''
    df['interaction'] = df['EloDiff'] * np.absolute(df['SeedDiff'])
    
    df.to_csv(f'{path}merged_team_matchups.csv', index=False)



if __name__=='__main__':
    file = ('merged_team_matchups.csv')
    moreFeatures(file)





'''
LifeSAVER:
    git fetch origin main
    git reset --hard FETCH_HEAD
'''
