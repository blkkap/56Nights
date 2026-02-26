import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import pandas as pd

df = pd.read_csv('../data/preprocess/Team_Matchups.csv')

features = ['NetRtgDiff','TOVDiff','RebDiff','eFGDiff','SeedDiff','WinDiff','MarginDiff']
target = 'Target'


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
            nn.Linear(64,32),
            nn.ReLU(),
            nn.Linear(32,1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layers(x)


def trainModel(model, X_train, y_train, device, lr=0.01, epochs=50):
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    X_train = X_train.to(device)
    y_train = y_train.to(device)

    dataset = TensorDataset(X_train, y_train)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    for epoch in range(epochs):
        for xb, yb in loader:
            optimizer.zero_grad()
            pred = model(xb).squeeze()
            loss = criterion(pred, yb)
            loss.backward()
            optimizer.step()

    return model


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

allSeasons = df['Season'].unique()
res = {}

for testSeason in allSeasons:
    train_seasons = [s for s in allSeasons if s != testSeason]

    X_train, y_train, X_test, y_test = getTrainTest(df, train_seasons, testSeason)

    model = BasketballNN(len(features)).to(device)
    model = trainModel(model, X_train, y_train, device)

    model.eval()
    with torch.no_grad():
        preds = model(X_test.to(device)).squeeze().round()
        acc = (preds.cpu() == y_test).float().mean().item()
        res[testSeason] = acc

print(res)