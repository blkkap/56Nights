import torch
import torch.nn as nn
import torch.utils.data import Dataset, TensorDataset
import os
import pandas as pd


df = pd.read_csv('../data/preprocess/Team_Matchups.csv')

X = ['NetRtgDiff','TOVDiff','RebDiff','eFGDiff','SeedDiff','WinDiff','MarginDiff']
y = ['Target']



def getTrainTest(df, train_season, test_season):
    train_season = list(range(2003,2013))
    test_season = 2013
    train_df = df[df['Season'].isin(train_seasons)]
    test_df = df[df['Season'] == test_season]

    X_train = torch.tensor(train_df[X].values(), dtype=torch.float32)
    y_train = torch.tensor(train_df[y].values(), dtype=torch.float32)

    X_test = torch.tensor(test_df[X].values(), dtype=torch.float32)
    y_test = torch.tensor(test_df[y].values(), dtype=torch.float32)

    return X_train, y_train, X_test, y_test



class BasketballNN(nn.module):
    def __init__(self, inputsize):
        super().__init__():
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




def trainModel(model, X_train, y_train, lr=0.01, epochs=50):
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    dataset = TensorDataset(X_train, y_train)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    for epoch in range(epochs):
        for x,y in loader:
            optimizer.zero_grad()
            pred = model(x).squeeze()
            loss = criterion(pred,y)
            loss.backward()
            optimizer.step()
    return model



allSeasons = df['Season'].unique()
res = {}

for testSeason in allSeasons:
    train_seasons = [s for s in allSeasons if s != testSeason]

    X_train, y_train, X_test, y_test = getTrainTest(df,train_seasons, testSeason)

    model = BasketballNN(len(X))
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model = trainModel(model, X_train, y_train)

    with torch.no_grad():
        preds = model(X_test).round()
        acc = (preds.squeeze() == y_test).float().mean().item()
        res[testSeason] = acc

print(res)



