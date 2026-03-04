import torch
from xgboost import XGBClassifier 
from sklearn.metrics import log_loss
import pandas as pd





df = pd.read_csv('../data/preprocess/merged_team_matchups.csv')

features = ['NetRtgDiff','TOVDiff','RebDiff','eFGDiff','SeedDiff','WinDiff','MarginDiff','EloDiff']
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


    NESTIMATOR = 1500
    MAXDEPTH = 4
    LR = 0.01
    OBJ = 'binary:logistic'
    SUBSAMPLE = 0.8
    COLSAMPLEBYTREE = 0.8 
    EVALMETRICS = 'logloss'
    RANDOMSTATE = 42
    TREEMETHOD = 'hist'

    model = XGBClassifier(
            n_esitmator = NESTIMATOR,
            max_depth = MAXDEPTH,
            learning_rate = LR,
            objective = OBJ,
            subsample = SUBSAMPLE,
            colsample_bytree = COLSAMPLEBYTREE,
            eval_metrics = EVALMETRICS,
            random_state = RANDOMSTATE,
            tree_method = TREEMETHOD
        )
    model.fit(X_train, y_train)
    preds = model.predict_proba(X_test)[:, 1]
    LL = log_loss(y_test, preds)

    logloss_res[testSeason] = LL

print('\nLog Loss per season:', logloss_res)
print('\nAvg Log Loss per season:', sum(logloss_res.values())/ len(logloss_res))



