import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


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

lr_features = [
    'NetRtgDiff',
    'EloDiff',
    'SeedDiff',
    'WinDiff',
    'MarginDiff'
]


df = pd.read_csv('../data/preprocess/sampleSub2.csv')
ids = df['ID']

train_df = pd.read_csv('../data/preprocess/merged2.csv').dropna()


X_train = train_df[features]
y_train = train_df['Target']

model = XGBClassifier(
    n_estimators=5000,
    max_depth=3,
    min_child_weight=3,
    learning_rate=0.02,
    objective='binary:logistic',
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric='logloss',
    random_state=42,
    tree_method='hist',
    gamma=0.1,
    reg_lambda=2,
    reg_alpha=1
)

model.fit(X_train, y_train, verbose=False)

X_train_lr = train_df[lr_features]

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_lr)

lr = LogisticRegression(max_iter=1000)
lr.fit(X_train_scaled, y_train)


X_test = df[features]
X_test_lr = df[lr_features]


preds_xgb = model.predict_proba(X_test)[:, 1]


X_test_scaled = scaler.transform(X_test_lr)
preds_lr = lr.predict_proba(X_test_scaled)[:, 1]


preds = 0.6 * preds_xgb + 0.4 * preds_lr


preds = np.clip(preds, 0.01, 0.99)


submission = pd.DataFrame({
    'ID': ids,
    'Pred': preds
})

submission.to_csv('../data/pred/tree_submission.csv', index=False)

print("Tree submission completed")