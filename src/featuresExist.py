import pandas as pd




def features(file):
    df = pd.read_csv(f'../data/preprocess/{file}')
    Mgames = pd.read_csv('../data/preprocess/M_Team_games_stats.csv')
    Wgames = pd.read_csv('../data/preprocess/W_Team_games_stats.csv')
    games = pd.concat([Mgames,Wgames], ignore_index=True)
    '''
    df['MatchupAdv'] = (df['avgOffRtg_LowerTeamID'] - df['avgDefRtg_HigherTeamID']) - (df['avgOffRtg_HigherTeamID'] - df['avgDefRtg_LowerTeamID'])
    df['NetRtgSquared'] = df['NetRtgDiff'] ** 2
    df['MarginStdDiff'] = df['MarginStd_Lower'] - df['MarginStd_Higher']
    df['OffRtgDiff'] = df['OffRtgStd_Lower'] - df['OffRtgStd_Higher']
    

    '''
    df['NetMatchup_LH'] = (df['avgNetRtg_LowerTeamID'] - df['avgNetRtg_HigherTeamID']).round(6)
    df['NetMatchup_HL'] = -df['NetMatchup_LH'].round(6)
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
    

def flipData(file):
    df = pd.read_csv(f'../data/preprocess/{file}')
    df_flip = df.copy()
    df['Target'] = 1 - df_flip['Target']
    diff_cols = [
            'TempoDiff',
            'NetRtgDiff',
            'TOVDiff',
            'RebDiff',
            'eFGDiff',
            'SeedDiff',
            'WinDiff',
            'MarginDiff',
            'EloDiff',
            'OffRtgDiff',
            'MarginStdDiff'
            ]
    for col in diff_cols:
        df_flip[col] = -df_flip[col]
    swap_pairs = [
            
            ('avgOffRtg_LowerTeamID', 'avgOffRtg_HigherTeamID'),
            ('avgDefRtg_LowerTeamID', 'avgDefRtg_HigherTeamID'),
            ('avgNetRtg_LowerTeamID', 'avgNetRtg_HigherTeamID'),
            ('MarginStd_Lower', 'MarginStd_Higher'),
            ('OffRtgStd_Lower', 'OffRtgStd_Higher'),
            ]
    for a,b in swap_pairs:
        df_flip[a], df_flip[b] = df_flip[b], df_flip[a]

    
    df = pd.concat([df,df_flip], ignore_index=True)

    df.to_csv('../data/preprocess/merged2.csv')


def moreFeatures(file):
    df = pd.read_csv(f'../data/preprocess/{file}')

    df['OffDef_Int_Str'] = (df['OffvsDefLow'] * df['NetRtgDiff']).round(6)
    df['TotStr'] = (df['avgNetRtg_LowerTeamID'] + df['avgNetRtg_HigherTeamID']).round(6)
    df['StrGapABS'] = abs(df['NetRtgDiff']).round(6)
    df['SeedEloMismatch'] = (df['SeedDiff'] * df['EloDiff']).round(6)
    
    print(df.head())
    df.to_csv(f'../data/preprocess/{file}')

if __name__=='__main__':
    file = 'merged_team_matchups.csv'
    file2 = 'merged2.csv'
    df = pd.read_csv(f'../data/preprocess/{file}')
    '''
    df = df.round({
        'MarginStd_Lower' : 6,
        'MarginStd_Higher' : 6,
        'OffRtgStd_Lower' : 6,
        'OffRtgStd_Higher' : 6,
        'OffRtgDiff' : 6,
        'MarginStdDiff' : 6,
        'MatchupAdv' : 6,
        'NetRtgSquared' : 6
        })

    df.to_csv(f'../data/preprocess/{file}')
    print(df.head())
    '''
    #features(file)
    #flipData(file)
    moreFeatures(file2)
