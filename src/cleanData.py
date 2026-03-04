import os 
import pandas as pd


path = '../data/preprocess'

def cleanCSV1(file):
    with open(os.path.join(path, file), 'r') as f:
        df = pd.read_csv(f)
        print(df.avgOffRtg.dtypes)
        df = df.round({'avgOffRtg': 6, 'avgDefRtg': 6, 'avgNetRtg': 6, 'avgeFG': 6, 'avgTOV': 6, 'avgReb': 6, 'AvgWin': 6, 'Elo': 0})

        df.to_csv(f'../data/preprocess/{file}', index=False) 
        print(df.head())

def cleanCSV2(file):
    with open(os.path.join(path,file), 'r') as f:
        df = pd.read_csv(f)
        df = df.round({
            'avgOffRtg_LowerTeamID': 6,
            'avgDefRtg_LowerTeamID': 6,
            'avgNetRtg_LowerTeamID': 6,
            'avgeFG_LowerTeamID': 6,
            'avgTOV_LowerTeamID': 6,
            'avgReb_LowerTeamID': 6,
            'AvgWin_LowerTeamID': 6,
            'Elo_LowerTeamID': 0,
            'avgOffRtg_HigherTeamID': 6,
            'avgDefRtg_HigherTeamID': 6,
            'avgNetRtg_HigherTeamID': 6,
            'avgeFG_HigherTeamID': 6,
            'avgTOV_HigherTeamID': 6,
            'avgReb_HigherTeamID': 6,
            'AvgWin_HigherTeamID': 6,
            'Elo_HigherTeamID': 0,
            'EloDiff': 0,
            'OffRtgDIff': 6,
            'DefRtgDiff': 6 ,
            'NetRtgDiff': 6,
            'TOVDiff': 6,
            'RebDiff': 6,
            'eFGDiff' : 6,
            'WinDiff' : 6
            })
        df.to_csv(f'../data/preprocess/{file}', index=False)


def cleanCSV3(file):
    with open(os.path.join(path,file), 'r') as f:
        df = pd.read_csv(f)
        df = df.round({
            'OffRtg': 6,
            'DefRtg': 6,
            'NetRtg': 6,
            'eFG%': 6,
            'TOV%': 6,
            'Reb%': 6
            })
        df.to_csv(f'../data/preprocess/{file}', index=False)



if __name__=='__main__':
    file1 = 'M_Team_season_stats.csv'
    file2 = 'M_Team_Matchups.csv'
    file3 = 'M_Team_games_stats.csv'
    
    cleanCSV1(file1)
    cleanCSV2(file2)
    cleanCSV3(file3)
