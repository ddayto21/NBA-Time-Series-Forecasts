# NBA Game Outcome Prediction with Machine Learning

## Overview

This project leverages NBA statistics to predict game outcomes using machine learning. The workflow integrates **data scraping**, **feature engineering**, and **predictive modeling** to provide insights into team performance and outcomes. The key focus is on analyzing historical performance, team metrics, and advanced statistics to make accurate predictions.

---

## Key Features

1. **Data Collection**: Gather and preprocess historical NBA game data.
2. **Feature Engineering**: Create game-specific features, advanced metrics, and rolling averages.
3. **Machine Learning**: Train models like Random Forest and Ridge Regression for game outcome prediction.
4. **Evaluation**: Assess model performance using classification and regression metrics.

---

## Project Workflow

### 1. Data Collection

**Sources**:

- [Basketball Reference](https://www.basketball-reference.com/): Historical game data, box scores, and advanced metrics.
- [NBA Stats API](https://www.nba.com/stats/): Player and team statistics.
- [ESPN](https://www.espn.com/nba/): Injury reports and roster updates.

**Data Extracted**:

- **Game Metadata**: Date, season, location (home/away).
- **Team Stats**: Offensive/defensive ratings, average points, turnovers, and rebounds.
- **Player Stats**: Points, assists, rebounds, and player efficiency (PER).
- **Advanced Metrics**: Pace, eFG%, TS%, rolling averages, and game context.

### 2. Feature Engineering

**Steps**:

- **Preprocessing**: Clean data, handle missing values, and normalize features.
- **Derived Features**:
  - Home/Away status
  - Days of rest for each team
  - Rolling averages for metrics like scoring trends and defensive efficiency
  - Rivalry indicators and travel fatigue
- **Target Variables**:
  - Total Score: Regression target for combined game scores.
  - Winner: Classification target (binary: 1 = Win, 0 = Loss).

---

### 3. Machine Learning

#### Models

- **Classification**: Predict game winners using Random Forest, Logistic Regression, or Gradient Boosting.
- **Regression**: Predict total game scores using Ridge Regression, XGBoost, or Neural Networks.

#### Workflow

1. Split data into training (70%), validation (15%), and testing (15%) sets.
2. Train models with key features like team stats, home-court advantage, and rolling averages.
3. Evaluate performance using metrics like Accuracy, MAE, RMSE, Precision, Recall, and F1-Score.

---

## Tools and Technologies

- **Languages**: Python
- **Libraries**: `pandas`, `BeautifulSoup`, `sklearn`, `nba-api`
- **Utilities**: Selenium for dynamic scraping, Google ChromeDriver
- **Environment**: Python 3.10+

---

## How to Run the Project

### Prerequisites

1. Install **Python 3.10+**.
2. Install Google Chrome and [ChromeDriver](https://chromedriver.chromium.org/downloads).

   ```bash
   brew install --cask chromedriver
   ```

## Steps

1. Clone the repository:

```bash
git clone htthttps://github.com/ddayto21/NBA-Time-Series-Forecastst.git
cd NBA-Game-Prediction
```

2. Set up a virtual environment:

```bash
python3.10 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure .env file:

Add the ChromeDriver path:

```plaintext
CHROMEDRIVER_PATH=/absolute/path/to/chromedriver
```

5. Run the pipeline:

```bash
python main.py
```

6. Train the model:

```bash
python src/training/train.py
```

### Future Enhancements

1. Add support for asynchronous scraping for faster data retrieval.
2. Incorporate ensemble models like Random Forest or XGBoost for better predictions.
3. Create visual dashboards for exploratory data analysis.
4. Introduce real-time game prediction based on live data.

### Contributing

Contributions are welcome! Open an issue or submit a pull request to contribute to this project.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgments

- Data sourced from Basketball Reference, NBA Stats, and ESPN.
- Inspired by the rich history of the NBA and the power of data-driven analysis.
