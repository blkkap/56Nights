import torch
from xgboost import XGBClassifier 
from sklearn.metrics import log_loss
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


#df = pd.read_csv('../data/preprocess/merged_team_matchups.csv')
df = pd.read_csv('../data/preprocess/merged2.csv')
'''
features = [
        'TempoDiff',
        'OffvsDefLow',
        'OffvsDefHi',
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
        'avgDefRtg_HigherTeamID',
        'avgNetRtg_LowerTeamID',
        'avgNetRtg_HigherTeamID',
        'MarginStdDiff',
        'OffRtgDiff',
        'NetMatchup_LH',
        'NetMatchup_HL',
        'OffDef_Int_Str',
        'TotStr',  
        'StrGapABS',
        'SeedEloMismatch'
        ]
'''
features = [
    'NetRtgDiff',
    'EloDiff',
    'SeedDiff',
    'MarginDiff',
    'WinDiff',
    'OffRtgDiff',
    'eFGDiff',
    'TOVDiff',
    'RebDiff',
    'OffvsDefLow',
    'OffvsDefHi'
]
target = 'Target'

df = df.dropna()
allSeasons = sorted(df['Season'].unique())

logloss_res = {}
for i in range(4, len(allSeasons)):
    testSeason = allSeasons[i]
    train_seasons = allSeasons[:i]

    train_df = df[df['Season'].isin(train_seasons)]
    test_df = df[df['Season'] == testSeason]

    X_train = train_df[features]
    y_train = train_df[target]

    X_test = test_df[features]
    y_test = test_df[target]


    NESTIMATOR= 5000
    MAXDEPTH = 3
    MINCHILDWEIGHT = 3
    LR = 0.02
    OBJ = 'binary:logistic'
    SUBSAMPLE = 0.8
    COLSAMPLEBYTREE = 0.8
    EVALMETRICS = 'logloss'
    RANDOMSTATE = 42
    TREEMETHOD = 'hist'
    EARLYSTOPPINGROUNDS = 200
    VERBOSE=True
    GAMMA = 0.1
    REG_LAMBDA = 2
    REG_ALPHA = 1
    model = XGBClassifier(
            n_estimators = NESTIMATOR,
            max_depth = MAXDEPTH,
            min_child_weight = MINCHILDWEIGHT,
            learning_rate = LR,
            objective = OBJ,
            subsample = SUBSAMPLE,
            colsample_bytree = COLSAMPLEBYTREE,
            eval_metric = EVALMETRICS,
            random_state = RANDOMSTATE,
            tree_method = TREEMETHOD,
            early_stopping_rounds=EARLYSTOPPINGROUNDS,
            gamma = GAMMA,
            reg_lambda = REG_LAMBDA,
            reg_alpha = REG_ALPHA
        )
    model.fit(X_train, y_train, 
              eval_set=[(X_test,y_test)],
              verbose=VERBOSE
              )
    preds_xgb = model.predict_proba(X_test)[:, 1]
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    lr = LogisticRegression(max_iter=1000)
    lr.fit(X_train_scaled, y_train)
    pred_lr = lr.predict_proba(X_test_scaled)[:,1]
    preds = 0.6 * preds_xgb + 0.4 * pred_lr

    preds = np.clip(preds, 0.01, 0.99)
    LL = log_loss(y_test, preds)

    logloss_res[testSeason] = LL
model.save_model('../Trees/model.bin')
print('Features count:', len(features))
print('\nLog Loss per season:', logloss_res)
print('\nAvg Log Loss per season:', sum(logloss_res.values())/ len(logloss_res))



