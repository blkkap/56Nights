import pandas as pd
import os


def getData(file):
    dirName = 'data/'
    for contents in os.listdir(dirName):
            with open(os.path.join(dirName, file),'r') as f:

                df = pd.read_csv(f)
    print(df.head())
    return 


if __name__=='__main__':
    file = 'MRegularSeasonDetailedResults.csv'
    getData(file)

    
    
