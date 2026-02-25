import os 
import pandas as pd


path = 'data/preprocess'

def cleanCSV1(file):
    with open(os.path.join(path, file), 'r') as f:
        df = pd.read_csv(f)
        print(df.avgOffRtg.dtypes)
        df = df.round({'avgOffRtg': 4, 'avgDefRtg': 4, 'avgNetRtg': 4, 'avgeFG': 4, 'avgTOV': 4, 'avgReb': 4, 'AvgWin': 4})

        df.to_csv(f'data/preprocess/{file}', index=False) 
        print(df.head())

def cleanCSV2(file):
    with open(os.path.join(path,file), 'r') as f:
        df = pd.read_csv(f)
        df = df.round({
            'avgOffRtg_TeamA': 4,
            'avgDefRtg_TeamA': 4,
            'avgNetRtg_TeamA': 4,
            'avgeFG_TeamA': 4,
            'avgTOV_TeamA': 4,
            'avgReb_TeamA': 4,
            'AvgWin_TeamA': 4,
            'avgOffRtg_TeamB': 4,
            'avgDefRtg_TeamB': 4,
            'avgNetRtg_TeamB': 4,
            'avgeFG_TeamB': 4,
            'avgTOV_TeamB': 4,
            'avgReb_TeamB': 4,
            'AvgWin_TeamB': 4,
            'OffRtgDIff': 4,
            'DefRtgDiff': 4 ,
            'NetRtgDiff': 4,
            'eFGDiff' : 4
            })
        df.to_csv(f'data/preprocess/{file}', index=False)


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
        df.to_csv(f'data/preprocess/{file}', index=False)



if __name__=='__main__':
    file1 = 'M_Team_season_stats.csv'
    file2 = 'Team_Matchups.csv'
    file3 = 'M_Team_games_stats.csv'
    
    cleanCSV1(file1)
    cleanCSV2(file2)
    cleanCSV3(file3)
