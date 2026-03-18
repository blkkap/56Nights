import pandas as pd




def features(file):
    df = pd.read_csv(f'../data/preprocess/{file}')
    Mgames = pd.read_csv('../data/preprocess/M_Team_games_stats.csv')
    Wgames = pd.read_csv('../data/preprocess/W_Team_games_stats.csv')
    games = pd.concat([Mgames,Wgames], ignore_index=True)

    df['MatchupAdv'] = (df['avgOffRtg_LowerTeamID'] - df['avgDefRtg_HigherTeamID']) - (df['avgOffRtg_HigherTeamID'] - df['avgDefRtg_LowerTeamID'])
    df['NetRtgSquared'] = df['NetRtgDiff'] ** 2
    
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
    df1.to_csv(f'../data/preprocess/{file}')





if __name__=='__main__':
    file = 'merged_team_matchups.csv'
    features(file)
