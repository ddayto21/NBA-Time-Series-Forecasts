# Repository Overview
The first section of this application involves scraping NBA statistics from Basketball Reference in order to train a machine learning model we can use to generate time-series predictions for each player, in regards to their chance of winning the MVP for a certain year. 

## Section 1: Data Collection
We use Python to scrape data from Basketball Reference, a website that provides basketball statistics and player data from the past 30 years in the NBA. 

- Source: https://www.basketball-reference.com/
- Datasets: MVP Data, Player Statistics, Team Statistics

### Scraping MVP Data
The following block of code scrapes MVP data from the past 30 years (1991 to 2022), then creates an HTML file for each year. After we are finished webscraping, we will extract the relevant data from each HTML file, and convert those files into individual CSV files.

```python
def Scrape_MVP():   
    years = range(1991, 2022)
    url_start = "https://www.basketball-reference.com/awards/awards_{}.html"
    for year in years:
        url = url_start.format(year)
        data = requests.get(url)        
        with open("mvp/{}.html".format(year), "w+") as f:
            f.write(data.text)
```

- Avoid overloading website by sending too many requests
- Google Chrome Version: 102.0.5.005.61
- Selenium Chrome Driver: https://chromedriver.storage.googleapis.com/index.html?path=102.0.5005.61/
 
 Run in Command-Line:
 >>> xattr -d com.apple.quarantine /Users/danieldayto/Downloads/chromedriver

 ## Section 2: Data Cleaning
 -  - COMBINE ALL 3 CSV FILES INTO ONE DATASET