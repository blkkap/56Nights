import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import pandas as pd
import numpy as np
from sklearn.metrics import log_loss
from sklearn.preprocessing import StandardScaler
import joblib


from sklearn.metrics import log_loss

#Parameters
BATCH_SIZE = 256
LR = 5e-4
WEIGHT_DECAY = 1e-2 
EPOCHS = 100 
SHUFFLE = True
LOSS = nn.BCEWithLogitsLoss()

scaler = StandardScaler()
df = pd.read_csv('../data/preprocess/merged_team_matchups.csv')


features = ['SeedProduct','OffvsDefLow','OffvsDefHi','eFGMatchupLow','eFGMatchupHi','MarginSQ','avgOffRtg_LowerTeamID','avgOffRtg_HigherTeamID','avgDefRtg_LowerTeamID','avgDefRtg_HigherTeamID','avgNetRtg_LowerTeamID','avgNetRtg_HigherTeamID','interaction','ESQUARE','Seed_LowerTeamID','Seed_HigherTeamID','SeedGap','EloGap','NetRtgDiff','TOVDiff','RebDiff','eFGDiff','SeedDiff','WinDiff','MarginDiff','EloDiff']
target = 'Target'

df = df.dropna()
df[features] = scaler.fit_transform(df[features])
def getTrainTest(df, train_seasons, test_season):
    train_df = df[df['Season'].isin(train_seasons)]
    test_df = df[df['Season'] == test_season]

    X_train = torch.tensor(train_df[features].values, dtype=torch.float32)
    y_train = torch.tensor(train_df[target].values, dtype=torch.float32)

    X_test = torch.tensor(test_df[features].values, dtype=torch.float32)
    y_test = torch.tensor(test_df[target].values, dtype=torch.float32)

    return X_train, y_train, X_test, y_test

class BasketballNN(nn.Module):
    def __init__(self, inputsize):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(inputsize, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.layers(x)

def trainModel(model, X_train, y_train, device, lr=LR, epochs=EPOCHS):
    criterion = LOSS
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=WEIGHT_DECAY)

    X_train = X_train.to(device)
    y_train = y_train.to(device)

    dataset = TensorDataset(X_train, y_train)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=SHUFFLE)

    for epoch in range(epochs):
        for xb, yb in loader:
            optimizer.zero_grad()
            logits = model(xb).squeeze(1)
            loss = criterion(logits, yb)
            loss.backward()
            optimizer.step()

    return model


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

allSeasons = sorted(df['Season'].unique())
acc_results = {}
logloss_results = {}

for i in range(4,len(allSeasons)):   #Inital value: 3
    testSeason = allSeasons[i]
    train_seasons = allSeasons[:i]
    X_train, y_train, X_test, y_test = getTrainTest(df, train_seasons, testSeason)

    model = BasketballNN(len(features)).to(device)
    model = trainModel(model, X_train, y_train, device)

    model.eval()
    with torch.no_grad():
        logits = model(X_test.to(device)).squeeze()
        probs = torch.sigmoid(logits).cpu().numpy()

        preds = (probs > 0.5).astype(int)

        acc = (preds == y_test.numpy()).mean()
        ll = log_loss(y_test.numpy(), probs)

        acc_results[testSeason] = acc
        logloss_results[testSeason] = ll

print("Accuracy per season:")
print(acc_results)

print("\nLog Loss per season:")
print(logloss_results)

print("\nAverage Accuracy:", np.mean(list(acc_results.values())))
print("Average Log Loss:", np.mean(list(logloss_results.values())))

print("Length of features:", len(features))
print("\nTraining final model on all seasons...")

X_full = torch.tensor(df[features].values, dtype=torch.float32)
y_full = torch.tensor(df[target].values, dtype=torch.float32)

final_model = BasketballNN(len(features)).to(device)
final_model = trainModel(final_model, X_full, y_full, device)

final_model.eval()
joblib.dump(scaler, '../Nets/scaler.pkl')
torch.save(final_model.state_dict(), '../Nets/MM_model.pth')


import sys
import os
o = sys.stdout
path = '../logs/'

with open(os.path.join(path, 'logs.txt'), 'a') as f:
    sys.stdout = f
    print("-----------Start of the log------------")
    print("\nAcc per season:")
    print(acc_results)

    print("\nLog Loss per season:")
    print(logloss_results)
    print("\nAvg Accuracy:" , np.mean(list(acc_results.values())))
    print("\nAvg Log loss:", np.mean(list(logloss_results.values())))

    print("\nParameters used for current iteration:")
    print("LR:", LR)
    print("epochs:", EPOCHS)
    print("Batch size:", BATCH_SIZE)
    print("Weight decay:", WEIGHT_DECAY)
    print("Shuffle:", SHUFFLE)
    print("Loss:", LOSS)
    print("----------End of iteration---------------")
