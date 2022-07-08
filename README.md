# PROBLEM: PREDICT THE NEXT NATIONAL BASKETBALL ASSOCIATION MVP

# STEP 1: WEB SCRAPING
The first section of this application involves scraping NBA statistics from Basketball Reference in order to train a machine learning model we can use to generate time-series predictions for each player, in regards to their chance of winning the MVP for a certain year. 
- SOURCE: https://www.basketball-reference.com/
  DATASETS (MVPS, PLAYER STATS, TEAM STATS) BY WEBSCRAPING 

- Avoid overloading website by sending too many requests
- Google Chrome Version: 102.0.5.005.61
- Selenium Chrome Driver: https://chromedriver.storage.googleapis.com/index.html?path=102.0.5005.61/
 
 Run in Command-Line:
 >>> xattr -d com.apple.quarantine /Users/danieldayto/Downloads/chromedriver

 # STEP 2: DATA CLEANING - COMBINE ALL 3 CSV FILES INTO ONE DATASET