import pandas as pd
from sklearn.linear_model import Ridge # Shrinks Linear Regression Coefficient to avoid Overfitting
from sklearn.metrics import mean_squared_error 

stats = pd.read_csv("player_mvp_stats.csv")

def Clean_Dataset(stats):
    stats = stats.fillna(0)    
    predictors = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P',
       '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB',
       'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'Year',
       'W', 'L', 'W/L%', 'GB', 'PS/G', 'PA/G', 'SRS']
    stats["PF"] = stats["PF"].astype(float)
    return stats, predictors

def Prediction(stats, predictors):
    print("Running Prediction...: ", stats, predictors)
    print(stats.dtypes)
    train = stats[stats["Year"] < 2021]
    print("Training Dataset: ", train)
    test = stats[stats["Year"] == 2021]
    print("Test Dataset: ", test)
    reg = Ridge(alpha=.1)
    print("reg: ", reg)
    # (X,Y) X --> Columns used to make prediction for
    # Y --> "Share" Column
    reg.fit(train[predictors], train["Share"])
    predictions = reg.predict(test[predictors])
    predictions = pd.DataFrame(predictions, columns=["Predictions"], index=test.index)

    # Compare Actual Values to Predictions
    combination = pd.concat([test[["Player", "Share"]], predictions], axis=1)
    
    combination = combination.sort_values("Share", ascending=False).head(50)
    mean_squared_error(combination["Share"], combination["Predictions"])
    # print("Mean Squared Error: ", mean_squared_error)
    actual = combination.sort_values("Share", ascending=False)
    combination["Rk"] = list(range(1,combination.shape[0]+1))
    print(combination.head(10))
    combination = combination.sort_values("Predictions", ascending=False)
    combination["Predicted_Rk"] = list(range(1,combination.shape[0]+1))
    print(combination.head(50))
    
    # ============ DEFINE AN ERROR METRIC ============== #
    # ---- ERROR METRIC: AVERAGE PRECISION  ------
    avg_precision = Average_Precision(combination)
    print("[+] Average Precision: ", avg_precision) # 65% ACCURACY ON FIRST ITERATION!! 

    # BACKTRACK ACROSS THE PREVIOUS YEARS
    Back_Testing(stats)

def Add_Ranks(combination):
    combination = combination.sort_values("Share", ascending=False)
    combination["Rk"] = list(range(1, combination.shape[0]+1))
    combination = combination.sort_values("Predictions", ascending=False)
    combination["Predicted_Rk"] = list(range(1, combination.shape[0]+1))
    combination["Difference"] = combination["Rk"] - combination["Predicted_Rk"]
    return combination

def Average_Precision(combination):
    actual = combination.sort_values("Share", ascending=False).head(5)
    predicted = combination.sort_values("Predictions", ascending=False)
    ps = []
    found = 0
    seen = 1
    for index, row in predicted.iterrows():
        if row["Player"] in actual["Player"].values:
            found += 1
            ps.append(found/seen)
        seen += 1
    return sum(ps) / len(ps)

def Back_Tests(stats, model, year, predictors):
    print("[+] Running Back-Tests....")
    years = list(range(1991, 2022))
    average_precision_scores = []
    all_predictions = []
    for year in years[5:]:
        print("Year: ", year)
        # Previous NBA Seasons will be used as Training Data for Model
        train = stats[stats["Year"]<year]  
        # Current Year will be Test Dataset
        test = stats[stats["Year"]==year]
        reg = Ridge(alpha=.1)
        reg.fit(train[predictors], train["Share"])
        predictions = reg.predict(test[predictors])
        predictions = pd.DataFrame(predictions, columns=["Predictions"], index=test.index)

        # Compare Actual Values to Predictions
        combination = pd.concat([test[["Player", "Share"]], predictions], axis=1)
        combination = Add_Ranks(combination)
        all_predictions.append(combination)
        print("All Predictions: ", all_predictions)
        average_precision_scores.append(Average_Precision(combination))
        print("Average Precision Scores: ", average_precision_scores)
    return sum(average_precision_scores)/len(average_precision_scores), average_precision_scores, pd.concat(all_predictions)
if __name__ == '__main__':
    stats, predictors = Clean_Dataset(stats)   
    # Prediction(stats, predictors)
    Back_Tests(stats)

    