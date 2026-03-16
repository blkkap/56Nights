import torch
from xgboost import XGBClassifier 
from sklearn.metrics import log_loss
import pandas as pd
import numpy as np




df = pd.read_csv('../data/preprocess/merged_team_matchups.csv')

features = ['Tempo_Lower','Tempo_Higher','TempoDiff','TempoGap','SeedProduct','OffvsDefLow','OffvsDefHi','eFGMatchupLow','eFGMatchupHi','MarginSQ','avgOffRtg_LowerTeamID','avgOffRtg_HigherTeamID','avgDefRtg_LowerTeamID','avgDefRtg_HigherTeamID','avgNetRtg_LowerTeamID','avgNetRtg_HigherTeamID','interaction','ESQUARE','Seed_LowerTeamID','Seed_HigherTeamID','SeedGap','EloGap','NetRtgDiff','TOVDiff','RebDiff','eFGDiff','SeedDiff','WinDiff','MarginDiff','EloDiff']
target = 'Target'

df = df.dropna()
allSeasons = sorted(df['Season'].unique())

logloss_res = {}
for i in range(3, len(allSeasons)):
    testSeason = allSeasons[i]
    train_seasons = allSeasons[:i-1]

    train_df = df[df['Season'].isin(train_seasons)]
    test_df = df[df['Season'] == testSeason]

    X_train = train_df[features]
    y_train = train_df[target]

    X_test = test_df[features]
    y_test = test_df[target]


    NESTIMATOR= 4000
    MAXDEPTH = 4
    #MINCHILDWEIGHT = 4 
    LR = 0.03
    OBJ = 'binary:logistic'
    SUBSAMPLE = 0.8
    COLSAMPLEBYTREE = 0.8 
    EVALMETRICS = 'logloss'
    RANDOMSTATE = 42
    TREEMETHOD = 'hist'
    EARLYSTOPPINGROUNDS = 200
    VERBOSE=False
    model = XGBClassifier(
            n_estimators = NESTIMATOR,
            max_depth = MAXDEPTH,
            #min_child_weight = MINCHILDWEIGHT,
            learning_rate = LR,
            objective = OBJ,
            subsample = SUBSAMPLE,
            colsample_bytree = COLSAMPLEBYTREE,
            eval_metric = EVALMETRICS,
            random_state = RANDOMSTATE,
            tree_method = TREEMETHOD,
            early_stopping_rounds=EARLYSTOPPINGROUNDS,
        )
    model.fit(X_train, y_train, 
              eval_set=[(X_test,y_test)],
              verbose=VERBOSE
              )
    preds = model.predict_proba(X_test)[:, 1]
    preds = np.clip(preds, 0.03, 0.97)
    LL = log_loss(y_test, preds)

    logloss_res[testSeason] = LL

print('\nLog Loss per season:', logloss_res)
print('\nAvg Log Loss per season:', sum(logloss_res.values())/ len(logloss_res))



