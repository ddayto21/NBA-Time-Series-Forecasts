# NBA MVP Prediction using Machine Learning

## Overview

This repository showcases a project aimed at leveraging NBA statistics to predict MVP winners for a given season using machine learning techniques. The project combines web scraping, data preprocessing, and machine learning model development to provide insightful predictions based on historical data. This repository is structured to demonstrate advanced technical skills in Python programming, data analysis, and predictive modeling.

---

## Key Features

1. **Data Collection:** Scrape historical NBA data from Basketball Reference.
2. **Data Preparation:** Clean and transform data for model training.
3. **Machine Learning:** Implement ridge regression for time-series predictions.

---

## Data Collection

### Source

Basketball Reference: [basketball-reference.com](https://www.basketball-reference.com/)

### Datasets

- **MVP Data**: Historical MVP award data spanning 30 years (1991-2022).
- **Player Statistics**: Individual player performance metrics.
- **Team Statistics**: Team-level statistics.

### Web Scraping Techniques

#### Scraping MVP Data

Python and libraries such as `requests` and `BeautifulSoup` are used to scrape and process MVP data efficiently. Below is a sample function that retrieves and saves MVP data:

```python
import requests

def scrape_mvp_data():
    years = range(1991, 2022)
    url_template = "https://www.basketball-reference.com/awards/awards_{}.html"
    for year in years:
        url = url_template.format(year)
        response = requests.get(url)
        with open(f"mvp/{year}.html", "w+") as file:
            file.write(response.text)
```

#### Scraping Player Statistics

To handle dynamic content, Selenium is utilized with a Chrome WebDriver to load and interact with pages. This allows the extraction of player statistics that are not readily accessible via static HTML parsing.

> **Technical Note:** Ensure proper handling of request rates to avoid overloading the source website.

---

## Data Preparation

Once the raw data is collected, it is transformed into structured CSV files for further analysis. The process involves:

1. Parsing HTML files to extract relevant data tables.
2. Using `pandas` for data manipulation and conversion to CSV format.

### Example: Parsing MVP Data

The following function demonstrates parsing and transforming MVP data:

```python
import pandas as pd
from bs4 import BeautifulSoup

def parse_mvp_data():
    dfs = []
    years = range(1991, 2022)
    for year in years:
        with open(f"mvp/{year}.html", "r") as file:
            content = file.read()
        soup = BeautifulSoup(content, "html.parser")
        soup.find('tr', class_="over_header").decompose()
        mvp_table = soup.find(id="mvp")
        mvp_df = pd.read_html(str(mvp_table))[0]
        mvp_df["Year"] = year
        dfs.append(mvp_df)
    mvps = pd.concat(dfs)
    mvps.to_csv("mvp/mvps.csv", index=False)
```

---

## Machine Learning

The machine learning component of the project leverages `scikit-learn` for model training and evaluation.

### Ridge Regression

Ridge regression, a regularization technique, is employed to predict MVP shares based on player statistics. Regularization helps mitigate overfitting by penalizing large coefficients.

#### Example Implementation

```python
from sklearn.linear_model import Ridge

def train_and_predict(stats, predictors):
    train = stats[stats["Year"] < 2021]
    test = stats[stats["Year"] == 2021]

    reg = Ridge(alpha=0.1)
    reg.fit(train[predictors], train["Share"])

    predictions = reg.predict(test[predictors])
    return pd.DataFrame(predictions, columns=["Predictions"], index=test.index)
```

---

## Tools and Technologies

- **Languages**: Python
- **Libraries**: `requests`, `BeautifulSoup`, `pandas`, `scikit-learn`, `selenium`
- **Utilities**: Selenium ChromeDriver for dynamic content scraping
- **Development Environment**: Python 3.9, Google Chrome 102.0.5.005.61

---

## How to Run the Project

1. Clone the repository.
2. Install required dependencies using `pip install -r requirements.txt`.
3. Configure Selenium ChromeDriver:
   ```bash
   xattr -d com.apple.quarantine /path/to/chromedriver
   ```
4. Run the scripts for data scraping and parsing.
   ```bash
   python scrape_data.py
   python parse_data.py
   ```
5. Train the machine learning model and evaluate predictions.

---

## Future Improvements

1. Enhance scraping efficiency using asynchronous techniques.
2. Expand dataset to include advanced player metrics.
3. Experiment with additional machine learning models such as gradient boosting and neural networks.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you'd like to contribute to this project.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Data sourced from [Basketball Reference](https://www.basketball-reference.com/).
- Inspired by the NBA's rich history of exceptional players and data-driven decision-making.

---

Elevate your data analysis and machine learning projects by exploring this comprehensive approach to predicting MVP winners. Feedback and collaborations are greatly appreciated!
