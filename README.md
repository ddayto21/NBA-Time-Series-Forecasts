# NBA MVP Prediction using Machine Learning

## Overview

This repository showcases a project leveraging NBA statistics to predict MVP winners for a given season using machine learning. The workflow integrates **web scraping**, **data preprocessing**, and **predictive modeling** to generate actionable insights.

---

## Key Features

1. **Data Collection:** Scrape and gather historical NBA data from [Basketball Reference](https://www.basketball-reference.com/).
2. **Data Preparation:** Clean and transform raw data into structured datasets.
3. **Machine Learning:** Train machine learning models, including ridge regression, to forecast MVP outcomes.

---

## Project Structure

```
NBA-Time-Series-Forecasts/
├── data_collection/
│   ├── __init__.py          # Package initialization
│   ├── constants.py         # Centralized constants for directories and years
│   ├── utils.py             # Helper functions for file operations
│   ├── scraping.py          # Web scraping logic
│   ├── parsing.py           # Data parsing and transformation
│   ├── driver.py            # Selenium WebDriver configuration
├── tests/
│   ├── __init__.py          # Test package initialization
│   ├── test_utils.py        # Tests for utility functions
│   ├── test_scraping.py     # Tests for scraping functions
│   ├── test_parsing.py      # Tests for parsing logic
├── main.py                  # Entry point for running the pipeline
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
```

## Project Workflow

## 1. Data Collection

### Datasets

- **MVP Data**: Historical MVP award data (1991–2024).
- **Player Statistics**: Individual player performance metrics.
- **Team Statistics**: Team-level performance data.

### Techniques

- **Static Content Scraping**: Leverage `requests` and `BeautifulSoup` modules for scraping `MVP Data` and `Team Statistics`.
- **Dynamic Content Scraping**: Use `Selenium WebDriver` for player stats.

**Note**: Note: Adhere to Basketball Reference’s terms of use and manage request rates responsibly.

---

## 2. Data Preparation

Transform raw HTML data into structured CSV files using pandas. This step ensures compatibility with machine learning pipelines.

### Example: Parsing MVP Data

```python
def parse_mvp_data():
    dfs = []
    for year in range(1991, 2024):
        with open(f"mvp/{year}.html", "r") as file:
            content = file.read()
        soup = BeautifulSoup(content, "html.parser")
        soup.find('tr', class_="over_header").decompose()
        mvp_table = soup.find(id="mvp")
        mvp_df = pd.read_html(str(mvp_table))[0]
        mvp_df["Year"] = year
        dfs.append(mvp_df)
    mvps = pd.concat(dfs, ignore_index=True)
    mvps.to_csv("mvp/mvps.csv", index=False)
```

---

## 3. Machine Learning

### Ridge Regression

Ridge regression predicts MVP shares based on player statistics. Regularization mitigates overfitting and improves generalization.

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
- **Utilities**: `Selenium ChromeDriver` for dynamic scraping.
- **Environment**: Python 3.10+, Google Chrome 102+

---

## How to Run the Project

### Prerequisites

1. Install `Python 3.10+`
2. Install `Google Chrome` and [ChromeDriver](https://chromedriver.chromium.org/downloads)

```bash
brew install --cask chromedriver
```

### Steps

1. Clone the repository:

```bash
git clone https://github.com/yourusername/NBA-Time-Series-Forecasts.git
cd NBA-Time-Series-Forecasts
```

2. Create and activate a virtual environment:

```bash
python3.10 -m venv venv
source venv/bin/activate

```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure the `.env` file:

```plaintext
CHROMEDRIVER_PATH=/absolute/path/to/chromedriver
```

**Tip**: You can find your `CHROMEDRIVER_PATH` by running: `which chromedriver`.

5. Run the pipeline or individual steps:

```bash
python main.py
```

6. Train the machine learning model and evaluate predictions.

---

## Configuring Proxy Server

https://free-proxy-list.net/

## Future Enhancements

1. Optimize scraping using `asynchronous` techniques.
2. Add advanced metrics and features for improved predictions.
3. Incorporate `visualizations` for exploratory data analysis (`EDA`).
4. Experiment with ensemble models like `random forests` or `gradient boosting`.

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
