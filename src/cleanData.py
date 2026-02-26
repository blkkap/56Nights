import os 
import pandas as pd


path = '../data/preprocess'

def cleanCSV1(file):
    with open(os.path.join(path, file), 'r') as f:
        df = pd.read_csv(f)
        print(df.avgOffRtg.dtypes)
        df = df.round({'avgOffRtg': 4, 'avgDefRtg': 4, 'avgNetRtg': 4, 'avgeFG': 4, 'avgTOV': 4, 'avgReb': 4, 'AvgWin': 4})

        df.to_csv(f'../data/preprocess/{file}', index=False) 
        print(df.head())

def cleanCSV2(file):
    with open(os.path.join(path,file), 'r') as f:
        df = pd.read_csv(f)
        df = df.round({
            'avgOffRtg_LowerTeamID': 4,
            'avgDefRtg_LowerTeamID': 4,
            'avgNetRtg_LowerTeamID': 4,
            'avgeFG_LowerTeamID': 4,
            'avgTOV_LowerTeamID': 4,
            'avgReb_LowerTeamID': 4,
            'AvgWin_LowerTeamID': 4,
            'avgOffRtg_HigherTeamID': 4,
            'avgDefRtg_HigherTeamID': 4,
            'avgNetRtg_HigherTeamID': 4,
            'avgeFG_HigherTeamID': 4,
            'avgTOV_HigherTeamID': 4,
            'avgReb_HigherTeamID': 4,
            'AvgWin_HigherTeamID': 4,
            'OffRtgDIff': 4,
            'DefRtgDiff': 4 ,
            'NetRtgDiff': 4,
            'TOVDiff': 4,
            'RebDiff': 4,
            'eFGDiff' : 4,
            'WinDiff' : 4
            })
        df.to_csv(f'../data/preprocess/{file}', index=False)


def cleanCSV3(file):
    with open(os.path.join(path,file), 'r') as f:
        df = pd.read_csv(f)
        df = df.round({
            'OffRtg': 4,
            'DefRtg': 4,
            'NetRtg': 4,
            'eFG%': 4,
            'TOV%': 4,
            'Reb%': 4
            })
        df.to_csv(f'../data/preprocess/{file}', index=False)



if __name__=='__main__':
    file1 = 'W_Team_season_stats.csv'
    file2 = 'W_Team_Matchups.csv'
    file3 = 'W_Team_games_stats.csv'
    
    #cleanCSV1(file1)
    cleanCSV2(file2)
    #cleanCSV3(file3)
