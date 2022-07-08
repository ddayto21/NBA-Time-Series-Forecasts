import pandas as pd
import csv
import matplotlib.pyplot as plt

plt.style.use('ggplot')

stats = pd.read_csv('player_mvp_stats.csv')

def Plot_Stats(df):
    highest_scoring = df[df["G"]>70].sort_values("PTS", ascending=False).head(10)
    highest_scoring = df.groupby("Year").apply(lambda x: x.sort_values("PTS", ascending=False).head(1))
    
    
if __name__ == '__main__':
    Plot_Stats(stats)
    stats.corr()["Share"].plot.bar()