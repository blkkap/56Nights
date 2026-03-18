import pandas as pd




def features(file):
    df = pd.read_csv(f'../data/preprocess/{file}')


    df['MatchupAdv'] = (df['avgOffRtg_LowerTeamID'] - df['avgDefRtg_HigherTeamID']) - (df['avgOffRtg_HigherTeamID'] - df['avgDefRtg_LowerTeamID'])
    df
    print(df.head(()
    df.to_csv(f'../data/preprocess/{file}')





if __name__=='__main__':
    file = 'merged_team_matchups.csv'
    features(file)
