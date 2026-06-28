import os
import glob
import pandas as pd
import kagglehub

def fetch_and_load_datasets():
    """
    Automatically downloads the latest versions of the requested Kaggle datasets
    and searches for relevant CSV files to parse into Pandas dataframes.
    """
    # 1. Download NFL Scores and Betting Data
    nfl_path = kagglehub.dataset_download("tobycrabtree/nfl-scores-and-betting-data")
    
    # 2. Download Sports Betting Predictive Analysis Sandbox
    sandbox_path = kagglehub.dataset_download("pratyushpuri/sports-betting-predictive-analysis-dataset")
    
    # Locate tracking csv files inside downloaded directory structures safely
    nfl_csvs = glob.glob(os.path.join(nfl_path, "**/*.csv"), recursive=True)
    sandbox_csvs = glob.glob(os.path.join(sandbox_path, "**/*.csv"), recursive=True)
    
    # Read core data files safely (falling back to blank DataFrames if empty)
    df_nfl = pd.read_csv(nfl_csvs[0]) if nfl_csvs else pd.DataFrame()
    df_sandbox = pd.read_csv(sandbox_csvs[0]) if sandbox_csvs else pd.DataFrame()
    
    return df_nfl, df_sandbox