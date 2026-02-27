import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import pandas as pd
import numpy as np
from sklearn.metrics import log_loss

df = pd.read_csv('../data/preprocess/merged_team_matchups.csv')

features = ['NetRtgDiff','TOVDiff','RebDiff','eFGDiff','SeedDiff','WinDiff','MarginDiff']
target = 'Target'

df = df.dropna()

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
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.layers(x)


def trainModel(model, X_train, y_train, device, lr=0.001, epochs=50):
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    X_train = X_train.to(device)
    y_train = y_train.to(device)

    dataset = TensorDataset(X_train, y_train)
    loader = DataLoader(dataset, batch_size=256, shuffle=True)

    for epoch in range(epochs):
        for xb, yb in loader:
            optimizer.zero_grad()
            logits = model(xb).squeeze()
            loss = criterion(logits, yb)
            loss.backward()
            optimizer.step()

    return model


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

allSeasons = sorted(df['Season'].unique())
acc_results = {}
logloss_results = {}

for testSeason in allSeasons:
    train_seasons = [s for s in allSeasons if s != testSeason]

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


print("\nTraining final model on all seasons...")

X_full = torch.tensor(df[features].values, dtype=torch.float32)
y_full = torch.tensor(df[target].values, dtype=torch.float32)

final_model = BasketballNN(len(features)).to(device)
final_model = trainModel(final_model, X_full, y_full, device)

final_model.eval()
