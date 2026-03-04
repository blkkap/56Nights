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
            suffixes = ('', '_Team1')
            )
    sample = sample.merge(
            season_all,
            left_on = ['Season', 'Team2'],
            right_on = ['Season', 'TeamID'],
            how = 'left',
            suffixes = ('', '_Team2')
            )
    
    
       
    
    sample = sample.drop(columns=['ID', 'Pred'])
    sample = sample.rename(columns = {
        'TeamID' : 'TeamID_Team1',
        'avgOffRtg' : 'avgOffRtg_Team1',
        'avgDefRtg' : 'avgDefRtg_Team1',
        'avgNetRtg' : 'avgNetRtg_Team1',
        'avgeFG' : 'avgeFG_Team1' ,
        'avgTOV' : 'avgTOV_Team1' ,
        'avgReb' : 'avgReb_Team1' ,
        'AvgWin' : 'AvgWin_Team1' ,
        'PointsFor' : 'PointsFor_Team1',
        'PointsAgainst' : 'PointsAgainst_Team1',
        'Elo' : 'Elo_Team1',
        'Margin' : 'Margin_Team1',
        'Seed' : 'Seed_Team1'
    })

    # Generate Diff

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




