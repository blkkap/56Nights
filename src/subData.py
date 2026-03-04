import os
import pandas as pd 

def subCSV(file1,file2,file3):
    sample = pd.read_csv(f'../data/raw/{file1}')
    Mseason = pd.read_csv(f'../data/preprocess/{file2}')
    Wseason = pd.read_csv(f'../data/preprocess/{file3}')
    sample[['Season','Team1', 'Team2']] = sample['ID'].str.split('_', expand=True)
    sample['Season'] = sample['Season'].astype(int)
    sample['Team1'] = sample['Team1'].astype(int)
    sample['Team2'] = sample['Team2'].astype(int)
    season_all = pd.concat([Mseason, Wseason], ignore_index=True) 
    
    sample = sample.merge(
            season_all,
            left_on = ['Season', 'Team1'],
            right_on = ['Season', 'TeamID'],
            how = 'left',
            suffixes = ('', '_MTeam1')
            )
    sample = sample.merge(
            season_all,
            left_on = ['Season', 'Team2'],
            right_on = ['Season', 'TeamID'],
            how = 'left',
            suffixes = ('', '_MTeam2')
            )
    '''
    sample = sample.merge(
            Wseason,
            left_on = ['Season','Team1'],
            right_on = ['Season', 'TeamID'],
            how = 'left',
            suffixes = ('', '_WTeam1')
            )
    sample = sample.merge(
            Wseason,
            left_on =['Season', 'Team2'],
            right_on = ['Season', 'TeamID'],
            how = 'left',
            suffixes = ('', '_WTeam2')
            )
    '''         
    #sample.drop(columns=['ID', 'Pred'])
    sample.to_csv('../data/preprocess/sampleSub.csv', index=False)
    print(sample.head())
    print(Mseason.head())
    print(Wseason.head())
    return





if __name__=='__main__':
    file1 = 'SampleSubmissionStage1.csv'
    file2 = 'M_Team_season_stats.csv'
    file3 = 'W_Team_season_stats.csv' 

    subCSV(file1,file2,file3)


# Which csv to use, game or season stats? 




