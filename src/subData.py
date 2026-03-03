import os
import pandas as pd 

def subCSV(file1,file2):
    sample = pd.read_csv(f'../data/raw/{file1}')
    season = pd.read_csv(f'../data/preprocess/{file2}')
    sample[['Season','Team1', 'Team2']] = sample['ID'].str.split('_', expand=True)
    sample['Season'] = sample['Season'].astype(int)
    sample['Team1'] = sample['Team1'].astype(int)
    sample['Team2'] = sample['Team2'].astype(int)
    sample.to_csv('../data/preprocess/sampleSub.csv', index=False)
    #with open(os.path.join(path1,file1), 'r') as f:
    print(sample.head())
    print(season.head())
    return





if __name__=='__main__':
    file1 = 'SampleSubmissionStage1.csv'
    file2 = 'merged_team_matchups.csv'
    

    subCSV(file1,file2)







