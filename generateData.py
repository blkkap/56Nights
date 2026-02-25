import pandas as pd
import numpy as np
import os
import numpy as np 


def getSeasonStats(file):
    path = 'data/preprocess/'
    for contents in os.listdir(path):
        with open(os.path.join(path, file), 'r') as f:
            df = pd.read_csv(f)
            season_stats = df.groupby(['Season', 'TeamID']).agg(
                    avgOffRtg = ('OffRtg', 'mean'),
                    avgDefRtg = ('DefRtg', 'mean'),
                    avgNetRtg = ('NetRtg', 'mean'),
                    avgeFG = ('eFG%', 'mean'),
                    avgTOV = ('TOV%', 'mean'),
                    avgReb = ('Reb%', 'mean'),
                    AvgWin = ('Win' , 'mean'),
                    PointsFor = ('PointsFor', 'sum'),
                    PointsAgainst = ('PointsAgainst', 'sum')
                    )
            season_stats['Margin'] = (
                    season_stats['PointsFor'] - season_stats['PointsAgainst']
                    )
            season_stats.to_csv('data/preprocess/M_Team_season_stats.csv')
            
            print(season_stats.head())

    return

'''
def getRankings(file, file2):
    path = 'data/raw/'
    #for file in os.listdir(path):
    with open(os.path.join(path, file), 'r') as f:
        df = pd.read_csv(f)
        ranking_stats = df.groupby(['Season', 'TeamID'], as_index=False).combine('RankingDayNum')
        ranking_stats.to_csv('data/preprocess/M_Team_season_stats.csv', mode='a', index=False, header=False) 
        #print(df.head())
    return 
'''

def getRankings(file, file2):
    df = pd.read_csv(f'data/preprocess/{file}') #main
    df1 = pd.read_csv(f'data/raw/{file2}') #Col to add
    
    filtered_stats = df1[df1['RankingDayNum'] == 133]
    filtered_stats = filtered_stats[['Season', 'TeamID','RankingDayNum', 'OrdinalRank']]

    ranking_stats = df.merge(filtered_stats, on=['Season','TeamID'],how='left')

    ranking_stats.to_csv('data/preprocess/M_Team_season_stats.csv')

def getMatchups(file):
    dirName = 'data/raw/'
    with open(os.path.join(dirName, file), 'r') as f:
        df = pd.read_csv(f)
        matchups = pd.DataFrame({
            'TeamA': np.where((df['WTeamID'] < df['LTeamID']),df['WTeamID'],df['LTeamID']),
            'TeamB': np.where((df['WTeamID'] > df['LTeamID']), df['WTeamID'], df['LTeamID']),
            'Target': np.where((df['WTeamID'] < df['LTeamID']),1, 0)
            })
        matchups.to_csv('data/preprocess/Team_Matchups.csv', index=False)
        print(df.head())


def getTeamStats(file):
    path = 'data/raw/'
    for contents in os.listdir(path):
            with open(os.path.join(path, file),'r') as f:

                df = pd.read_csv(f)
                winners = pd.DataFrame({
                    'Season': df['Season'],
                    'DayNum': df['DayNum'],
                    'TeamID': df['WTeamID'],
                    'OppID': df['LTeamID'],
                    'PointsFor': df['WScore'],
                    'PointsAgainst': df['LScore'],
                    'Poss': df['WFGA'] - df['WOR'] + df['WTO'] + 0.475 * df['WFTA'],
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
            
               # Uncommenting this will get the poss_opp for each row but since they are ~similiar we can just use the
               # curr row poss for each future calculation
                team_games = pd.merge(
                        team_games,
                        team_games[['Season', 'DayNum', 'TeamID', 'OppID', 'Poss', 'DR', 'OR']],
                        left_on=['Season', 'DayNum', 'TeamID', 'OppID'],
                        right_on=['Season', 'DayNum', 'OppID', 'TeamID'],
                        suffixes=('','_opp')
                )
            
                team_games.to_csv('data/preprocess/M_Team_games_stats.csv', index=False)

    df = pd.DataFrame(df)
    num_rows = len(df.index)
    print(f'Num of rows for raw file: {num_rows}')

    df1 = pd.DataFrame(team_games)
    num_rows1 = len(df1.index)
    print(f'Num of rows for team games: {num_rows1}')
    return 



def effMetrics(file):
    path = 'data/preprocess/'
    for contents in os.listdir(path):
        with open(os.path.join(path, file), 'r') as f:
            df = pd.read_csv(f)

            df['OffRtg'] = df['PointsFor'] / df['Poss']
            df['DefRtg'] = df['PointsAgainst'] / df['Poss_opp']
            df['NetRtg'] = df['OffRtg'] - df['DefRtg']
            df['eFG%'] = (df['FGM'] + 0.5 * df['FGM3']) / df['FGA'] 
            df['TOV%'] = df['TO'] / df['Poss']
            df['Reb%'] = (df['OR'] + df['DR']) / (df['OR'] + df['DR'] + df['OR_opp'] + df['DR_opp'])  


            df.to_csv('data/preprocess/M_Team_games_stats.csv', index=False)
            print(df.head())
    return


def getTourneyStats(file1, file2):
    df1 = pd.read_csv(f'data/raw/{file1}')
    df2 = pd.read_csv(f'data/preprocess/{file2}')

    mergedSeeds = df1[['Season', 'TeamID', 'Seed']]
    Seeds = df2.merge(mergedSeeds, on=['Season', 'TeamID'], how='left')
    Seeds.to_csv(f'data/preprocess/{file2}', index=False)
    def cleanData():
        df = pd.read_csv(f'data/preprocess/{file2}')
        df['Seed']= df['Seed'].fillna('20')
        df['Seed'] = df['Seed'].str.replace('\D','', regex=True)
        return df.to_csv(f'data/preprocess/{file2}', index=False)
    return cleanData()

if __name__=='__main__':
    file = 'MRegularSeasonDetailedResults.csv'
    file1 = 'M_Team_games_stats.csv'
    fileB = 'MMasseyOrdinals.csv'
    fileA = 'M_Team_season_stats.csv'
    file2 = 'MNCAATourneySeeds.csv'
    file3 = 'MNCAATourneyDetailedResults.csv'
    # STEP 1
    #getTeamStats(file)
    #effMetrics(file1)
    # STEP 2
    #getSeasonStats(file1)
    # STEP 3
    #getRankings(fileA,fileB)
    # STEP 4
    #getTourneyStats(file2, fileA)
    # STEP 5
    getMatchups(file3)
