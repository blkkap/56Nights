import pandas as pd




def features(file):
    df = pd.read_csv(f'../data/preprocess/{file}')
    Mgames = pd.read_csv('../data/preprocess/M_Team_games_stats.csv')
    Wgames = pd.read_csv('../data/preprocess/W_Team_games_stats.csv')
    games = pd.concat([Mgames,Wgames], ignore_index=True)

    df['MatchupAdv'] = (df['avgOffRtg_LowerTeamID'] - df['avgDefRtg_HigherTeamID']) - (df['avgOffRtg_HigherTeamID'] - df['avgDefRtg_LowerTeamID'])
    df['NetRtgSquared'] = df['NetRtgDiff'] ** 2
    df['MarginStdDiff'] = df['MarginStd_Lower'] - df['MarginStd_Higher']
    df['OffRtgDiff'] = df['OffRtgStd_Lower'] - df['OffRtgStd_Higher']

    ''' 
    games['Margin'] = games['PointsFor'] - games['PointsAgainst']

    team_std = games.groupby(['Season','TeamID']).agg({
        'Margin' : 'std',
        'OffRtg' : 'std'
        }).reset_index()

    team_std.columns = [
            'Season',
            'TeamID',
            'MarginStd',
            'OffRtgStd'
            ]
    print(team_std.head())


    dff = df.merge(
            team_std,
            left_on=['Season','LowerTeamID'],
            right_on=['Season','TeamID'],
            how='left'
            )
    dff = dff.rename(columns={
        'MarginStd' : 'MarginStd_Lower',
        'OffRtgStd' : 'OffRtgStd_Lower'
        })
    dff = dff.drop(columns=['TeamID'])
    df1 = dff.merge(
            team_std,
            left_on=['Season','HigherTeamID'],
            right_on=['Season','TeamID'],
            how='left'
            )
    df1 = df1.rename(columns={
        'MarginStd': 'MarginStd_Higher',
        'OffRtgStd': 'OffRtgStd_Higher'
        })
    df1 = df1.drop(columns=['TeamID'])
    

    print(df1.head())
    '''
    df.to_csv(f'../data/preprocess/{file}')
    




if __name__=='__main__':
    file = 'merged_team_matchups.csv'
 
    df = pd.read_csv(f'../data/preprocess/{file}')
    '''
    df = df.drop(columns=[
        'MarginStd_Lower',
        'OffRtgStd_Lower',
        'MarginStd_x',
        'OffRtgStd_x',
        'MarginStd_y',
        'OffRtgStd_y',
        'MarginStd_Higher',
        'OffRtgStd_Higher',
        'Unnamed: 0.4',
        'Unnamed: 0.3',
        'Unnamed: 0.2',
        'Unnamed: 0.1',
        'Unnamed: 0'
        ]
    )
    df.to_csv(f'../data/preprocess/{file}')
    print(df.head())
    '''
    df = df.drop(columns=['Unnamed: 0', 'Unnamed: 0.5'])
    df.to_csv(f'../data/preprocess/{file}')
    print(df.head())
    features(file)
