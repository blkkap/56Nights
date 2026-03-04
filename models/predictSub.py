import torch
import torch.nn as nn
import pandas as pd
import numpy as np 
from sklearn.preprocessing import StandardScaler
import joblib


features = ['NetRtgDiff','TOVDiff','RebDiff','eFGDiff','SeedDiff','WinDiff','MarginDiff','EloDiff']
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


df = pd.read_csv('../data/preprocess/sampleSub.csv')

ids = df['ID']

scaler = StandardScaler()
train_df = pd.read_csv('../data/preprocess/merged_team_matchups.csv')
train_df = train_df.dropna()
scaler.fit(train_df[features])

scaler = joblib.load('../Nets/scaler.pkl')
df[features] = scaler.transform(df[features])

X_test = torch.tensor(df[features].values(), dtype=torch.float32).to(device)

class BasketballNN(nn.Module):
    def __init__(self, inputsize):
        super().__init__()
        self.layers = nn.Sequnetial(
            nn.Linear(inputsize, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64,32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32,1)
        )

    def forward(self, x):
        return self.layers(x)


model = BasketballNN(len(features)).to(device)
model.load_state_dict(torch.load('../Nets/MM_model.pth', map_loaction=device))
model.eval()


with torch.no_grad():
    logits = model(X_test).squeeze()
    probs = torch.sigmoid(logits).cpu().numpy()

submission = pd.DataFrame({
    'ID' : ids,
    'Pred' : probs
})

submission.to_csv('../data/pred/sub.csv', index=False)

print('Submission completed')

