import os
import pandas as pd
import numpy as np

def moreFeatures(file):
    path = '../data/preprocess/'
    df = pd.read_csv(f'{path}merged_team_matchups.csv')
    #with open(os.path.join(path,file), 'r') as f:
        #df = pd.read_csv(f)
        #print(df.head())
    '''
    We already have majority of new features needed
        - SeedDiff
        - Elo_LowerTeam1
        - Elo_HigherTeam2
        - Seed_LowerTeam1
        - Seed_higherTeam2 
        Need to calculate
        - Elo * abs(SeedDiff)
        - EloDiffSQRD
        - SeedSum
        More Features To ADD:
        - SeedProduct : SeedL * SeedHi   X
        - Pythag : PF**11.5 / (PF**11.5 + PA**11.5)
        - PythagLower
        - PythagHigher
        - PythagDiff 
        - OffVsDefLow : OffRtgLower - OffRtgHigher   X
        - OffVsDefHi : OffRtgHigher - OffRtgLow   X 
        - eFGmatchupLow  X 
        - eFGmatchupHi   X
        - TempoLow : Poss
        - TempoHi
        - TempoDiff
        - TempoGap
        - MarginSTDLow X
        - MarginSTDHi X
        - OffRtgSTD   
        - DefRtgSTF    
        - MarginSTDDiff  X
        - PythagDiff * SeedDiff 
        - CoachTourWins
        - MarginDiffSQ   X
    '''
    df['interaction'] = df['EloDiff'] * np.absolute(df['SeedDiff'])
    df['ESQUARE'] = np.square(df['EloDiff']) 
    df['SeedGap'] = np.absolute(df['SeedDiff'])
    df['EloGap'] = np.absolute(df['EloDiff'])
    df['SeedProduct'] = (df['Seed_LowerTeamID'] * df['Seed_HigherTeamID']).round(6)
    df['OffvsDefLow'] = (df['avgOffRtg_LowerTeamID'] - df['avgDefRtg_HigherTeamID']).round(6)
    df['OffvsDefHi'] = (df['avgOffRtg_HigherTeamID'] - df['avgDefRtg_LowerTeamID']).round(6)
    df['eFGMatchupLow'] = (df['avgeFG_LowerTeamID'] - df['avgeFG_HigherTeamID']).round(6)
    df['eFGMatchupHi'] = (df['avgeFG_HigherTeamID'] - df['avgeFG_LowerTeamID']).round(6)
    df['MarginSQ'] = np.square(df['MarginDiff']).round(6)
    
    

    #df = df.drop(['MarginSTDLow', 'MarginSTDHi', 'MarginDiffSTD'], axis=1)

    df.to_csv(f'{path}merged_team_matchups.csv', index=False)
    
    def getTemp():
        
        file = 'M_Team_games_stats.csv'
        file1 = 'W_Team_games_stats.csv'

        df1 = pd.read_csv(f'../data/preprocess/{file}')
        df2 = pd.read_csv(f'../data/preprocess/{file1}')
        df3 = pd.read_csv('../data/preprocess/merged_team_matchups.csv')

        games = pd.concat([df1,df2], ignore_index=True)
        tempo = (
                games.groupby(['Season', 'TeamID'])['Poss']
                .mean()
                .reset_index()
                )
        tempo =  tempo.rename(columns={'Poss':'Tempo'})
        print(tempo.head())
        dff = df3.merge(
                tempo,
                left_on = ['Season', 'LowerTeamID'],
                right_on = ['Season', 'TeamID'],
                how='left',
                suffixes = ('','_Lower')
                )

        #df = df.drop(columns=['TeamID'], inplace=True)

        df = dff.merge(
                tempo,
                left_on = ['Season', 'HigherTeamID'],
                right_on = ['Season', 'TeamID'],
                how = 'left',
                suffixes = ('', '_Higher')
                )
        df.drop(columns=['TeamID'])
        
        df = df.rename(columns={'Tempo': 'Tempo_Lower'})
        print(df.head())

        df['TempoDiff'] = df['Tempo_Lower'] - df['Tempo_Higher']
        df['TempoGap'] = abs(df['TempoDiff'])
        df = df.round({
            'TempoDiff' : 6,
            'TempoGap' : 6,
            'Tempo_Lower': 6,
            'Tempo_Higher': 6
            })
        df.to_csv('../data/preprocess/merged_team_matchups.csv', index=False)
    return getTemp()


if __name__=='__main__':
    file = ('merged_team_matchups.csv')
    
    df3 = pd.read_csv(f'../data/preprocess/{file}')

    df = df3.drop(['TeamID', 'Tempo_Lower','Tempo_Higher', 'TempoDiff', 'TempoGap','TeamID_Higher'], axis=1)
    df.to_csv(f'../data/preprocess/{file}')
    print(df.head())
    moreFeatures(file)





'''
LifeSAVER:
    git fetch origin main
    git reset --hard FETCH_HEAD
'''
