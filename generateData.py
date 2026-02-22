import pandas as pd
import numpy as np
import os


def getTeamStats(file):
    dirName = 'data/raw/'
    for contents in os.listdir(dirName):
            with open(os.path.join(dirName, file),'r') as f:

                df = pd.read_csv(f)
                winners = pd.DataFrame({
                    'Season': df['Season'],
                    'DayNum': df['DayNum'],
                    'TeamID': df['WTeamID'],
                    'OppID': df['LTeamID'],
                    'PointsFor': df['WScore'],
                    'PointsAgainst': df['LScore'],
                    'Poss': df['WFGA'] - df['WOR'] + df['LTO'] + 0.475 * df['WFTA'],
                    'FGM': df['WFGM'],
                    'FGA': df['WFGA'],
                    'FGM3': df['WFGM3'],
                    'FGA3': df['WFGA3'],
                    'FTM': df['WFTM'],
                    'FTA': df['WFTA'],
                    'OR': df['WOR'],
                    'DR': df['WDR'],
                    'Ast': df['WAst'],
                    'TO' : df['WTO'],
                    'Stl': df['WStl'],
                    'Blk': df['WBlk'],
                    'PF': df['WPF'],
                    'Win': 1
                    })


                losers = pd.DataFrame({
                    'Season': df['Season'],
                    'DayNum': df['DayNum'],
                    'TeamID': df['LTeamID'],
                    'OppID': df['WTeamID'],
                    'PointsFor': df['LScore'],
                    'PointsAgainst': df['WScore'],
                    'Poss': df['LFGA'] - df['LOR'] + df['LTO'] + 0.475 * df['LFTA'],
                    'FGM': df['LFGM'],
                    'FGA': df['LFGA'],
                    'FGM3': df['LFGM3'],
                    'FGA3': df['LFGA3'],
                    'FTM': df['LFTM'],
                    'FTA': df['LFTA'],
                    'OR': df['LOR'],
                    'DR': df['LDR'],
                    'Ast': df['LAst'],
                    'TO' : df['LTO'],
                    'Stl': df['LStl'],
                    'Blk': df['LBlk'],
                    'PF': df['LPF'],
                    'Win': 0
                    })

                team_games = pd.concat([winners,losers], ignore_index=True)
                team_games.to_csv('data/preprocess/M_Team_games_stats.csv', index=False)

    df = pd.DataFrame(df)
    num_rows = len(df.index)
    print(f'Num of rows for raw file: {num_rows}')

    df1 = pd.DataFrame(team_games)
    num_rows1 = len(df1.index)
    print(f'Num of rows for team games: {num_rows1}')
    return 


if __name__=='__main__':
    file = 'MRegularSeasonDetailedResults.csv'
    getTeamStats(file)

    
    
