import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time

years = range(1991, 2022)

def ChromeDriver():
    driver = webdriver.Chrome(executable_path="/Users/danieldayto/Downloads/chromedriver")
    return driver

def Scrape_MVP():    
    url_start = "https://www.basketball-reference.com/awards/awards_{}.html"
    for year in years:
        url = url_start.format(year)
        data = requests.get(url)
        
        with open("mvp/{}.html".format(year), "w+") as f:
            f.write(data.text)

def Parse_MVP(years):
    dfs = []
    for year in years:
        with open(f"mvp/{year}.html") as f:
            page = f.read()
        soup = BeautifulSoup(page, "html.parser")
        soup.find('tr', class_="over_header").decompose()
        mvp_table = soup.find(id="mvp")
        mvp_df = pd.read_html(str(mvp_table))[0]
        # Create a 'Year' Column
        mvp_df["Year"] = year        
        dfs.append(mvp_df)
    mvps = pd.concat(dfs)
    mvps.to_csv("mvp/mvps.csv")

def Scrape_Player(years):
    for year in years:
        player_stats_url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"
        url = player_stats_url.format(year)
        driver = ChromeDriver()
        driver.get(url)
        driver.execute_script("window.scrollTo(1,10000)")
        time.sleep(2)
        html = driver.page_source
        with open(f"player/{year}.html", "w+") as f:
            f.write(html)
def Parse_Player(years):
    dfs = []
    for year in years:
        with open(f"player/{year}.html") as f:
            page = f.read()
        soup = BeautifulSoup(page, "html.parser")
        soup.find('tr', class_="thead").decompose()
        player_table = soup.find(id="per_game_stats")
        player_df = pd.read_html(str(player_table))[0]
        # Create a 'Year' Column
        player_df["Year"] = year        
        dfs.append(player_df)
    players = pd.concat(dfs)
    players.to_csv("player/players.csv")

def Scrape_Team(years):
    for year in years:
        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"
        data = requests.get(url)
        with open(f"team/{year}.html", "w+") as f:
            f.write(data.text)

def Parse_Team(years):
    dfs = []
    for year in years:
        with open(f"team/{year}.html") as f:
            page = f.read()
        soup = BeautifulSoup(page, "html.parser")
        soup.find('tr', class_="thead").decompose()
        
        east_table = soup.find(id="divs_standings_E")
        east_teams = pd.read_html(str(east_table))[0]
        east_teams["Year"] = year
        east_teams["Team"] = east_teams["Eastern Conference"]
        dfs.append(east_teams)

        west_table = soup.find(id="divs_standings_W")
        west_teams = pd.read_html(str(west_table))[0]
        west_teams["Year"] = year
        west_teams["Team"] = west_teams["Western Conference"]
        dfs.append(west_teams)
    teams = pd.concat(dfs)
    teams.to_csv("team/teams.csv")

if __name__ == '__main__':
    # Scrape_MVP() 
    # Scrape_Player()
    # Scrape_Team()
    # 


