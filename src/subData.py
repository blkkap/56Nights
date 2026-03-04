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
    
    
       
    # Dont drop cols will need these for sub file
    #sample = sample.drop(columns=['ID', 'Pred'])
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
    sample['NetRtgDiff'] = sample['avgNetRtg_Team1'] - sample['avgNetRtg_Team2']
    sample['TOVDiff'] = sample['avgTOV_Team1'] - sample['avgTOV_Team2']
    sample['RebDiff'] = sample['avgReb_Team1'] - sample['avgReb_Team2']
    sample['eFGDiff'] = sample['avgeFG_Team1'] - sample['avgeFG_Team2']
    sample['SeedDiff'] = sample['Seed_Team1'] - sample['Seed_Team2']
    sample['WinDiff'] = sample['AvgWin_Team1'] - sample['AvgWin_Team2']
    sample['MarginDIff'] = sample['Margin_Team1'] - sample['Margin_Team2'] 
    sample['EloDiff'] = sample['Elo_Team1'] - sample['Elo_Team2']

    sample = sample.round({
        'NetRtgDiff': 6,
        'TOVDiff': 6,
        'RebDiff': 6,
        'eFGDiff': 6,
        'SeedDiff': 6,
        'WinDiff': 6,
        'MarginDiff': 6,
        'EloDiff': 6
        })
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




