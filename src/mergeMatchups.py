import pandas as pd
import os


def mergeMatchups(file, file2):
    file = pd.read_csv(f'../data/preprocess/{file}')
    file2 = pd.read_csv(f'../data/preprocess/{file2}')
    df = pd.concat([file, file2])
    df.to_csv('../data/preprocess/merged_team_matchups.csv', index=False)
    print(df.head())



if __name__=='__main__':
    file1 = 'M_Team_Matchups.csv'
    file2 = 'W_Team_Matchups.csv'

    mergeMatchups(file1, file2)
