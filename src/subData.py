import os
import pandas as pd 

def subCSV(file1,file2):
    sample = pd.read_csv(f'../data/raw/{file1}')
    season = pd.read_csv(f'../data/preprocess/{file2}')
    #with open(os.path.join(path1,file1), 'r') as f:
    print(sample.head())
    print(season.head())
    return





if __name__=='__main__':
    file1 = 'SampleSubmissionStage1.csv'
    file2 = 'merged_team_matchups.csv'
    

    subCSV(file1,file2)







