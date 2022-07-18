# Repository Overview
The first section of this application involves scraping NBA statistics from Basketball Reference in order to train a machine learning model we can use to generate time-series predictions for each player, in regards to their chance of winning the MVP for a certain year. 

## Data Collection
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

### Scraping NBA Player Statistics
The webpages that contain NBA player statistics contain dynamic content, making it a challenge to scrape all of the data we need in order to train our machine learning model. However, we address this problem using a Selenium chrome driver in order to loa  block of code scrapes MVP data from the past 30 years (1991 to 2022), then creates an HTML file for each year. After we are finished webscraping, we will extract the relevant data from each HTML file, and convert those files into individual CSV files.

### Preparing Datasets - CSV Files
After collecting the MVP data from the past 30 years, we iterate every year in our 'mvp' folder and apply the following operations to each HTML file:
- Create an empty array that will be used to store multiple dataframes
- Extract relevant information from each HTML file, specifying the 'id' attribute of the table we need.
- Use Pandas to read the HTML table using Pandas as a dataframe
- Create a CSV file in the "mvp" folder using the .to_csv() operation 

```python
def Parse_MVP(years):
    dfs = []
    years = range(1991, 2022)
    for year in years:
        with open(f"mvp/{year}.html") as f:
            page = f.read()
        soup = BeautifulSoup(page, "html.parser")
        soup.find('tr', class_="over_header").decompose()
        mvp_table = soup.find(id="mvp")
        mvp_df = pd.read_html(str(mvp_table))[0]
        mvp_df["Year"] = year        
        dfs.append(mvp_df)
    mvps = pd.concat(dfs)
    mvps.to_csv("mvp/mvps.csv")    
```

- Avoid overloading website by sending too many requests
- Google Chrome Version: 102.0.5.005.61
- Selenium Chrome Driver: https://chromedriver.storage.googleapis.com/index.html?path=102.0.5005.61/
 
 Run in Command-Line:
 >>> xattr -d com.apple.quarantine /Users/danieldayto/Downloads/chromedriver

## Machine Learning
Scikit-learn is a free software machine learning library for the Python programming language. It features various classification, regression and clustering algorithms. 


### Ridge Regression
Ridge regression is a regularization technique that performs L2 regularization. It modifies the loss function by adding the penalty equivalent to the square of the magnitude of coefficients.

```python
  train = stats[stats["Year"] < 2021]
  test = stats[stats["Year"] == 2021]
  reg = Ridge(alpha=.1)
  reg.fit(train[predictors], train["Share"])
  predictions = reg.predict(test[predictors])
  predictions = pd.DataFrame(predictions, columns=["Predictions"], index=test.index)
```