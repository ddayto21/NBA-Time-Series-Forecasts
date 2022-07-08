import pandas as pd
import csv

# DELETE "EASTERN CONFERENCE" AND "WESTERN CONFERENCE" COLUMNS IN 'TEAMS.CSV' DATASET
del_columns = ["Eastern Conference", "Western Conference"]
def Remove_Columns(del_columns):
    df = pd.read_csv("team/teams.csv")
    for x in del_columns:
        del df[x]
    # SET THE TEAM NAME TO THE FIRST COLUMN POSITION IN DATAFRAME:
    col_name = "Team"
    first_col = df.pop(col_name)
    df.insert(0, col_name, first_col)
    # print(df)
    df.to_csv("team/teams.csv")

def Clean_MVP():
    mvps = pd.read_csv("mvp/mvps.csv")
    mvps = mvps[["Player", "Year", "Pts Won", "Pts Max", "Share"]]
    return mvps

def Single_Row(df):
    # print("Single_Row() --> df: ", df)
    if df.shape[0] == 1:
        return df
    else:
        row = df[df["Tm"] == "TOT"]
        # print("row: ", row)
        row["Tm"] = df.iloc[-1,:]["Tm"]
        return row   

def Clean_Players():
    players = pd.read_csv("player/players.csv")
    del players["Rk"]
    players["Player"] = players["Player"].str.replace("*", "", regex=False)
    players = players.groupby(["Player", "Year"]).apply(Single_Row)
    # Drop 2 Index Levels
    players.index = players.index.droplevel()
    players.index = players.index.droplevel()
    print(players.head(30))
    return players

def Clean_Teams():
    teams = pd.read_csv("team/teams.csv")
    teams = teams[~teams["W"].str.contains("Division")]
    teams["Team"] = teams["Team"].str.replace("*", "", regex=False)
    # print(teams["Team"].unique())
    return teams    


def Clean_Nick_Names():
    df = pd.read_csv("team/nicknames.csv")
    del df["prefix_2"]
    df = df.rename(columns={"name": "Name", "prefix_1": "Abbreviation"})
    col_name = "Abbreviation"
    column = df.pop(col_name)
    df.insert(0, col_name, column)
    df["Abbreviation"] = df["Abbreviation"].str.upper()
    df["Name"] = df["Name"].str.title()
    print(df)
    df.to_csv("team/nicknames.csv")

def Nick_Names():
    nicknames = {}
    with open("team/nicknames.csv") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            print(row)
            abbrev, name = row[1], row[2]
            nicknames[abbrev] = name
    # print("nicknames: ", nicknames)
    return nicknames
   

def Merge_Datasets(players, mvps):
    combined = players.merge(mvps, how="outer", on=["Player", "Year"])
    combined[["Pts Won", "Pts Max", "Share"]] = combined[["Pts Won", "Pts Max", "Share"]].fillna(0)
    print(combined["Tm"].unique())
    nicknames = Nick_Names()
    print("Nicknames: ", nicknames)
    combined["Team"] = combined["Tm"].map(nicknames)
    
    return combined

if __name__ == '__main__':
    # Remove_Columns(del_columns)
    mvps = Clean_MVP()
    players = Clean_Players()
    teams = Clean_Teams()
    combined = Merge_Datasets(players, mvps)
    stats = combined.merge(teams, how="outer", on=["Team", "Year"])
    # del stats["Unnamed: 0"]
    del stats["Unnamed: 0_x"]
    del stats["Unnamed: 0.1"]
    del stats["Unnamed: 0_y"]
    print(stats.head())
    # del stats["Unnamed: 0"]
    stats["GB"] = stats["GB"].str.replace("—", "0")
    # Tries to convert every column in Stats Dataframe into Number Type
    stats = stats.apply(pd.to_numeric, errors="ignore")
    stats.to_csv("player_mvp_stats.csv", index=False)
   
   


    


