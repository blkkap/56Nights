import os
import pandas as pd


def moreFeatures(file):
    path = '../data/preprocess/'

    with open(os.path.join(path,file), 'r') as f:
        df = pd.read_csv(f)
        print(df.head())
        '''
        We already have majority of new features needed
        - SeedDiff
        - Elo_LowerTeam1
        - Elo_HigherTeam2
        
        Need to calculate
        - Elo * abs(SeedDiff)
        - EloDiffSQRD
        - SeedSum
        - Seed_LowerTeam1
        - Seed_higherTeam2
        '''






if __name__=='__main__':
    file = ('merged_team_matchups.csv')
    moreFeatures(file)
