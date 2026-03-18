import torch
from xgboost import XGBClassifier 
from sklearn.metrics import log_loss
import pandas as pd
import numpy as np




df = pd.read_csv('../data/preprocess/merged_team_matchups.csv')

features = [
        'TempoDiff',
        'OffvsDefLow',
        'OffvsDefHi',
        'interaction',
        'ESQUARE',
        'SeedGap',
        'NetRtgDiff',
        'TOVDiff',
        'RebDiff',
        'eFGDiff',
        'SeedDiff',
        'WinDiff',
        'MarginDiff',
        'EloDiff',
        'avgOffRtg_LowerTeamID',
        'avgOffRtg_HigherTeamID',
        'avgDefRtg_LowerTeamID',
        'avgDefRetg_HigherTeamID',
        'avgNetRtg_LowerTeamID',
        'avgNetRtg_HigherTeamID',
        'MatchupAdv'
        ]
target = 'Target'

df = df.dropna()
allSeasons = sorted(df['Season'].unique())

logloss_res = {}
for i in range(4, len(allSeasons)):
    testSeason = allSeasons[i]
    train_seasons = allSeasons[:i-1]

    train_df = df[df['Season'].isin(train_seasons)]
    test_df = df[df['Season'] == testSeason]

    X_train = train_df[features]
    y_train = train_df[target]

    X_test = test_df[features]
    y_test = test_df[target]


    NESTIMATOR= 1200
    MAXDEPTH = 3
    MINCHILDWEIGHT = 5 
    LR = 0.02
    OBJ = 'binary:logistic'
    SUBSAMPLE = 0.8
    COLSAMPLEBYTREE = 0.8
    EVALMETRICS = 'logloss'
    RANDOMSTATE = 42
    TREEMETHOD = 'hist'
    EARLYSTOPPINGROUNDS = 200
    VERBOSE=False
    GAMMA = 0.2
    REG_LAMBDA = 2
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
            #early_stopping_rounds=EARLYSTOPPINGROUNDS,
            #gamma = GAMMA,
            #reg_lambda = REG_LAMBDA
        )
    model.fit(X_train, y_train, 
              eval_set=[(X_test,y_test)],
              verbose=VERBOSE
              )
    preds = model.predict_proba(X_test)[:, 1]
    preds = np.clip(preds, 0.025, 0.975)
    LL = log_loss(y_test, preds)

    logloss_res[testSeason] = LL

print('Features count:', len(features))
print('\nLog Loss per season:', logloss_res)
print('\nAvg Log Loss per season:', sum(logloss_res.values())/ len(logloss_res))



