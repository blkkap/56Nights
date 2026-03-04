import torch
from xgboost import XGBClassifier 
from sklearn.metrics import log_loss






df = pd.read_csv('../data/preprocess/merged_team_matchups.csv')

features = ['NetRtgDiff','TOVDiff','RebDiff','eFGDiff','SeedDiff','WinDiff','MarginDiff','EloDiff']
target = 'Target'

df = df.dropna()
allSeasons = sorted(df['Season'].unique())

for i in range(4, len(allSeasons))
    testSeason = allSeasons[i]
    train_seasons = allSeason[:i]

    train_df = df[df['Season'].isin(train_seasons)]
    test_df = df[df['Season'] == testSeason]

    X_train = train_df[features]
    y_train = train_df[target]

    X_test = test_df[features]
    y_test = test_df[target]


    NESTIMATOR = 1500
    MAXDEPTH = 4
    LR = 1
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
            colsample_bytree = COLSAMPLE,
            eval_metrics = EVALMETRICS,
            random_state = RANDOMSTATE,
            tree_method = TREEMETHOD
        )
    model.fit(X_train, y_train)
    pred = model.predict_proba(X_test)[:, 1]
    LL = log_loss(y_test, preds)

    logloss_res[testseason] = LL

print('Log Loss per season:', logloss_res)
print('Avg Log Loss per season:', sum(logloss_res.values())/ len(logloss_res))



