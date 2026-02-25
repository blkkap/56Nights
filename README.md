# Thought process
- The first thing that comes to mind is "holy hell thats going to be alot of computing if each tteam has to play each team once. 
- I forgot the algo used in the tennis match up example
- Losers play loser so on blah blah blah i forgot the algo
- Okay 
- Everything is wrong here except the first point
- I lied that was also wrong 
# First DATA
- Lets figure out how and what data is needed
  - MSeasonDetailed.csv will do for the start
  - More data will be added as iteration goes on
- I suspect not all data will be needed
  - Yes this is in fact true


# Step 1 PreProcess
- Get data and turn each team details into in row/feature
  - EX:
    - Winning team should have all its stats dispalyed on one row plus the team they played and the score of each team and vice versa
    - Add on to this dataset (Compute Possessions) poss = FGA - OR + TO + 0.475 * FTA : New COL
    - Compute Opponents Possossions
    - Compute efficiency Metrics per game
      - OffRtg = PointsFor/Poss
      - DefRtg = PointsAgainst/OppPoss
      - NetRtg = OffRtg - DefRtg

      - eFG% = (FGM + 0.5*FGM3) / FGA
      - TOV% = TO/Poss
      - Reb% = (OR+DR)/(OR+DR+Opp OR + Opp DR)

# Step 2 Aggregate
- Group by : Season + TeamID
  - Mean OffRtg
  - Mean DefRtg
  - Mean NetRtg
  - Mean eFG
  - Mean TOV%
  - Mean Reb%
  - Win%
  - Avg Margin (PointsFor - PointsAgainst)
- Season Stats / One row per team per season 
  - Get the avg for each team for that whole season
# Step 3 Rankings  (Come back to this)
- MMasseyOrdinals
- RankingDayNum = 134 - 1 filter 133
- Ordinal Ranking to calculate the match up diff for future DS
  - Merge this into Season Stats
  - 2 Rows : Efficiency and Ranking


# Step 4 Tourny Seeds
- TourneySeeds.CSV 
  - Convert Seeds X01 -> 1 
- Merge into Season Stats


# Step 5 Matchup
- TourneyDetailResults 
- Identify both teams
- Pull season Stats
- Lower Team = Team1 :: Higher Team = Team2
  - Groupby season and teamid to pull stats from team season : (this may need to change)
    - First pull from TourneyDetailRes Marking lower TeamID with team1 higher TeamID with team2 and target based off WScore Vs. LScore
    - Target = who won if lower mark 1 else 0
  - Find way to pull stats from season stats 
  - We need to create all matchups
  - look at the team with the lowest teamID and mark them team1 higher teamID with team2
  - Calculate diff based off each team stats
  - Create new Target col if team1 won mark 1 else 0 -> team2

 
- Create more Features
  - OffRtgDiff
  - DefRtgDiff
  - NetRtgDiff
  - eFGDiff = Team1_eFGD - Team2_eFGD
  - SeedDiff = Team1_seed - Team2_seed
- Targets : 1 -> Team1 won else Team2 won 0
- One row per Tournament game



# Step 6 Cross Validation
- Split by season
- EX: 
  - Train: Season <= 2022
  - Validate on 2023
- Better Strat
  - Leave on season out cross val
    - 2010-2015 Val on 2017



# Step 7 Model X,y
- X:feature col
  - No teamID, No Season
  - Numerical features only
- y:target


# Step 8 Train
- Logistic Reg
  - Brier Score -> calibrated probabilities
- Evaluate using Brier Score -> MSE

# Step 9 Calibration
- If overconfident
  - Platt or Isotonic

# Step 10 Test
- Train on Historical seasons
- Validate on held out season
- Evaluate Brier Score

- Note:
  - If performance improves when adding features keep else remove them




## Future Iterations
- Generate all 2026 tean pairs
- Compute feature diff
- Predict Prob 
- Clean data:
  - Decimal place 3-4
  - Round last digit only (Normal rounding)





# TODO List Based Dates:

## Feb 25, 26
- Create new file that cleans all csv files
  - Rounding by 3-4 decimals
- Create more Features
