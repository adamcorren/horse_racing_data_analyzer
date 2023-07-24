# Horse Racing Data Analyzer 

Horse Racing Data Analyzer is a Python program that scrapes UK, Ireland bookmaker and Betfair exchange horse racing data and combines this data with pre race hourly bookmaker and exchange data. It then will analyse the data collected and produce 149 unique data points for every horse running in every race in the UK and Ireland.

These data points cover topics such as:
- Key time morning prices (currently 1am, 6am ,10am)
- Comparison of prices between different times and sources
- Non runner analysis
- Favourite and predicting position metrics
- Analysing result of races

The program will then export daily data csv files containing data from all racing that day.

Currently used sites (more to come):
- [Sporting Life](https://www.sportinglife.com/racing)
- [Timeform](https://www.timeform.com/horse-racing)
- [Betfair](https://www.betfair.com/sport/)

## Prerequisite Software

- [Python 3](https://www.python.org/) (make sure to add Python to PATH/environment variables when installing)
- [pandas 2.0.1 or newer](https://pandas.pydata.org/)
- [Selenium 4.9.1 or newer](https://github.com/SeleniumHQ/selenium/)
- [Beautiful Soup 4.12.2 or newer](https://pypi.org/project/beautifulsoup4/)


### Windows installation

You can install the prerequisites double-clicking `install_prerequesites.bat` after installing Python 3.

### Updating Chromedriver

I will try my best to keep the included Chromedriver up to date with the latest stable version of Chrome, but sometimes 
I may miss an update by a few days. If you wish to update it yourself, please download the relevant version of
Chromedriver from [here](https://chromedriver.chromium.org/downloads) and replace the correct file.

## Program Installation

Horse Racing Data Analyzer can be installed by downloading the repository from [the GitHub page](https://github.com/adamcorren/horse_racing_data_analyzer)

## Usage
     
Follow the instructions for your operating system below.

### Windows

Once you've installed the [prerequisites](#prerequisite-software), double click `start_windows.bat`. That's it. Bish 
bash bosh.

### Using the program

Hourly data, stored in individual daily folders within the 'daily_data' folder will contain hourly prices scraped from the websites [Sporting Life](https://www.sportinglife.com/racing) and [Timeform](https://www.timeform.com/horse-racing). These will contain prices from all the major bookmakers as well as Betfair Exchange prices each hour for the 24 hours preceding the races start time. A program that collects this data can be found from [the GitHub page](https://github.com/adamcorren/horse_racing_data_collecter).

The program will ask which date you want to analyse data from. This is done by asking for the year, month, day. NOTE ONLY THE DATE 2023, 7, 1 WILL WORK WITHOUT ADDITIONAL HOURLY DATA IMPORTED BY USER.

The program will then guide you through the rest of the process yourself.

Once exported, the daily data file will be stored in the 'daily_data' folder, as well as a master file named 'ALL' that will contain all data you have analysed.

# Other Horse Racing repositories

[Study of various price sources in the UK and Ireland horse racing markets](https://github.com/adamcorren/horse_racing_study_1)

[Study of the accuracy of price ranges and how they differ across various price suppliers in the UK and Ireland horse racing markets](https://github.com/adamcorren/horse_racing_study_2)

[Study on the impact of cross-platform discrepancies on market uncertainty in UK and Ireland horse racing markets](https://github.com/adamcorren/horse_racing_study_3)

[Study on the effect of price movements on market reliability in UK and Ireland horse racing markets](https://github.com/adamcorren/horse_racing_study_4)

[Project Report]()

## License

Horse Racing Data Analyzer is licensed under Licensed under [MIT]((https://opensource.org/license/mit/)).
