import pandas as pd
import numpy as np

# load data
file = input("What is the csv file path: ")
if file[-3:] == "csv":
    x = pd.read_csv(file)
else:
    print("Failure: file must be a CSV")

# list of columns to utilize 
columns_of_interest = ["league","created_at","event_name","creative_mode","ad_unit","url","user_agent","creative_width","creative_height","page_type"]

# new df that only contains the columns we care about
df = x[columns_of_interest]

# function for counting nulls 
pct_nuls = []
def count_nulls(x):
    count_nulls = x.isnull().sum()
    return count_nulls

# function for pct of nulls in each column 
def pct_nulls(x):
    nulls_pct = (count_nulls(x)/x.shape[0]) * 100
    pct_nulls_list = nulls_pct.tolist()
    return pct_nulls_list

# function for dropping all nulls if under 5% in each column 
def clean_nulls(x):
    nulls = pct_nulls(x)
    if all(i <= 5.0 for i in nulls):
        df = x.dropna(inplace = True)
    else:
        print("Nulls exceed 5% of total data frame, utilize appropriate data science techniques for replacing null values")

# function for slicing out the platform name from ad unit column
# might need to do some filtering
def get_platform():
    df["platform"] = df["ad_unit"].str.slice(start = 6, stop = 9)
    for i, row in df.iterrows():
        if row["platform"] != "maw" and row["platform"] != "app":
            df.loc[i, "platform"] = row["platform"][0:2]

# function for slicing out the site
# might need to do some filtering
def get_site():
    df['site'] = df['url'].str.split('/').str[2]
    df["site"] = df['site'].str.split(".").str[1]

# function for getting device type
def get_device():
    df["device"] = df["user_agent"].str.split("(").str[1]
    df["device"] = df["device"].str.split(";").str[0]

# function for extracting time of day
def get_time_of_day():
    df["hour"] = df["created_at"].str.slice(start = 10, stop =13)
    df["hour"] = pd.to_numeric(df["hour"])
    for i, row in df.iterrows():
        hour = row["hour"]
        if 0 <= hour < 12:
            df.at[i, "time_of_day"] = "morning"
        elif 12 < hour < 18:
            df.at[i, "time_of_day"] = "afternoon"
        else:
            df.at[i, "time_of_day"] = "night"

# function for converting clicks and impression values 
def convert_outcomes():
    df["outcome"] = 1
    for i, row in df.iterrows():
        if row["event_name"] != "click":
            df.loc[i, "outcome"] = 0


# function that does everything
def cleaner(x):
    count_nulls(df)
    pct_nulls(df)
    get_platform()
    get_site()
    get_device()
    get_time_of_day()
    convert_outcomes()
    clean_nulls(df)


# call to action and filter for only CBS Sports site 
cleaner(df)
site_options = ["cbssports"]
df = df[df["site"].isin(site_options)]


# if run into problems down road with nulls, impute mode for most categorical columns 