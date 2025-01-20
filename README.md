# NBA MVP Prediction using Machine Learning

## Overview

This repository demonstrates a project that uses NBA statistics to predict MVP winners for a given season through machine learning techniques. It combines **web scraping**, **data preprocessing**, and **predictive modeling** to provide data-driven insights. This project showcases advanced skills in Python programming, **data analysis**, and **machine learning**.

---

## Key Features

1. **Data Collection:** Scrape and gather historical NBA data from [Basketball Reference](https://www.basketball-reference.com/).
2. **Data Preparation:** Clean, transform, and structure the data for analysis.
3. **Machine Learning:** Build and train predictive models using ridge regression for MVP prediction.

---

## Project Workflow

## 1. Data Collection

### Datasets

- **MVP Data**: Historical MVP award data spanning 30+ years (1991–2024).
- **Player Statistics**: Individual player performance metrics.
- **Team Statistics**: Team-level performance data.

### Techniques

- **Static Content Scraping**: Leverage requests and BeautifulSoup to scrape MVP and team statistics.
- **Dynamic Content Scraping**: Use Selenium WebDriver for extracting player stats.

**Note**: Ensure compliance with Basketball Reference’s terms of use and manage request rates responsibly.

---

## 2. Data Preparation

Raw HTML data is parsed and transformed into structured CSV files using pandas. This ensures the data is ready for machine learning workflows.

Example: Parsing MVP Data◊

```python
import pandas as pd
from bs4 import BeautifulSoup

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

The predictive model uses ridge regression to predict MVP shares based on player statistics. Regularization is applied to mitigate overfitting and enhance generalization.

### Ridge Regression Implementation

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
- **Utilities**: Selenium `ChromeDriver` for dynamic content scraping.
- **Development Environment**: Python 3.9+, Google Chrome 102.0.5.005.61

---

## How to Run the Project

### Prerequisites

1. Install Python 3.10
2. Install `Chrome` and `ChromeDriver`

- Download `ChromeDriver`: https://chromedriver.chromium.org/downloads
- Install via `Homebrew` on macOS:

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
# On Windows: venv\\Scripts\\activate
```

3. Install required dependencies:

```bash
pip install -r requirements.txt
```

4. Configure the `.env` file with your ChromeDriver path:

```plaintext
CHROMEDRIVER_PATH=/absolute/path/to/chromedriver
```

**Tip**: You can find your `CHROMEDRIVER_PATH` by running: `which chromedriver`.

5. Run the scripts for data scraping and parsing.

```bash
python scrape_data.py
python parse_data.py
```

6. Train the machine learning model and evaluate predictions.

---

## Future Enhancements

1. Improve scraping efficiency using parallel and `asynchronous` processing.
2. Incorporate advanced player statistics and metrics for better predictions.
3. Experiment with additional models like `gradient boosting`, `random forests`, or `neural networks`.
4. Add visualizations for exploratory data analysis (`EDA`) and model insights.

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
