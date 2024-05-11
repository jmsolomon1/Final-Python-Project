#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 21:36:39 2024

@author: jasonsolomon
"""

import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import openpyxl
import statsmodels.api as sm
import statsmodels.formula.api as smf
import plotly.express as px
import os
from shiny import App, ui, render
from prettytable import PrettyTable
import pdfplumber
import re

## Part 4; Analysis

## I want to examine unemployment, free lunch participation and science scores
## before, during and after the Great Recession (2009-2015)

## I'm going to do the following:
    ##  (1) I'm going to extract data for the years 2009, 2011 and 2015 from
    ##  the three data sets.  For free lunch participation, I'm going to 
    ##  use 2000-01 as a proxy for 2009.  I have data for science test scores
    ##  specifically for those three years.  For unemployment, that is reported
    ##  monthly I'm going to use the Dec 2009, 2011 and 2015 values.  Once I've
    ##  isolated the data I'll run an OLS regression to see how these different
    ##  variables track.  My hypothesis: the great recession caused a massive
    ##  increase in unemployment, this should have resulted in corresponding
    ##  increase in free lunch participation and a decrease in science test scores.
    ##  The loss of a parents job, as referenced in the NYT article, would impact
    ##  household income and the parents ability to provide meals as well as their
    ##  eligibility for free lunch.  Additionally, the stress of a household losing
    ##  income is also expected to negatively impact student's ability to prepare for tests
    ##  for many reasons (access to tutoring, tranquility of home environment for example).
    ##  There's also an argument to be made that a parent without a job would be more 
    ##  available to help their child with their education but only if they weren't
    ##  busy/worried with replacing the income from their lost job.  Most families
    ##  who lost jobs during the Great Recession didn't voluntary leave the workforce to
    ##  focus on child-care but rather they were laid off and that economic shock
    ##  wasn't planned or desired.
    
## Data Extraction and merging

##  December Unemployment Data for 2009, 2011 and 2015
csv_file_path = '/Users/jasonsolomon/Documents/GitHub/final-project-python_edu/Data/Unemployment Data_2007-2015.csv'
unemployment_data = pd.read_csv(csv_file_path)

unemployment_data['Year'] = pd.to_datetime(unemployment_data['Label'], format='%Y %b').dt.year
unemployment_data['Month'] = pd.to_datetime(unemployment_data['Label'], format='%Y %b').dt.strftime('%b')

dec_unemployment = unemployment_data[(unemployment_data['Month'] == 'Dec') & (unemployment_data['Year'].isin([2009, 2011, 2015]))]
dec_unemployment = dec_unemployment[['Year', 'Value']].rename(columns={'Value': 'Unemployment Rate'})


#      Year  Unemployment Rate
# 35   2009                9.7
# 59   2011                8.3
# 107  2015                4.8


##  I'm curious how this regression might change if I use all the unemployment data, 
##  all 12 months instead of just December
##  and all the years (2007 - 2015) instead of just the three years corresponding with the free lunch
##  and national science scores.  This doesn't really make sense though without corresponding data
##  for monthly free lunch and monthly science scores (don't exist).  The problem seems to be 
##  in how little testing data exists for the students compared to other metrics.  We have regular, monthly
##  unemployment data, yearly free lunch participation and sporadic, every other year science scores.
## one more thought, I want to take an average of the monthly unemployment for 24 months
## instead of using the end of year (dec) data point for my three years and compare


unemployment_data['Year'] = pd.to_datetime(unemployment_data['Label']).dt.year
unemployment_data['Month'] = pd.to_datetime(unemployment_data['Label']).dt.month

periods = {
    (2008, 2009): 2009,
    (2010, 2011): 2011,
    (2014, 2015): 2015
}

frames = []

for years, label_year in periods.items():
    mask = unemployment_data['Year'].isin(years)
    temp_df = unemployment_data[mask]

    avg_unemployment = temp_df['Value'].mean()
    
    frames.append(pd.DataFrame({
        'Year': [label_year],
        'Average Unemployment Rate': [avg_unemployment]
    }))

averaged_unemployment = pd.concat(frames).reset_index(drop=True)
averaged_unemployment['Year'] = averaged_unemployment['Year'].astype(int)

#    Year  Average Unemployment Rate
# 0  2009                   7.520833
# 1  2011                   9.283333
# 2  2015                   5.729167


## Free Lunch Participation
years_str = "2000-01, 2010-11, 2014-15, 2015-16"
numbers_str = "17839867, 23544479, 25826297, 25900186" 

years_list = years_str.split(", ")
numbers_list = numbers_str.split(", ")

year_mapping = {'2000-01': 2009, '2010-11': 2011, '2014-15': 2015}

data_entries = []

for proxy_year, actual_year in year_mapping.items():
    if proxy_year in years_list:
     
        index = years_list.index(proxy_year)
    
        number = numbers_list[index]
       
        data_entries.append({
            'Year': actual_year,
            'Number of Students Eligible for Free/Reduced Lunch': int(number)
        })

cleaned_freelunch_df = pd.DataFrame(data_entries)

## Science Test Scores (National)
excel_file_path = '/Users/jasonsolomon/Documents/GitHub/final-project-python_edu/Data/NDECoreExcel_Science, Grade 8, All students - 2_20240409023345.Xls'
science_scores_df = pd.read_excel(excel_file_path, header=8)
filtered_science_scores = science_scores_df[
    (science_scores_df['Jurisdiction'] == 'National') &
    (science_scores_df['Year'].isin([2009, 2011, 2015]))
][['Year', 'Average scale score']]

## Merging Data Sets for OLS
dec_unemployment['Year'] = dec_unemployment['Year'].astype(int)
cleaned_freelunch_df['Year'] = cleaned_freelunch_df['Year'].astype(int)
filtered_science_scores['Year'] = filtered_science_scores['Year'].astype(int)
OLS_df = pd.merge(dec_unemployment, cleaned_freelunch_df, on='Year', how='inner')
OLS_df = pd.merge(OLS_df, filtered_science_scores, on='Year', how='inner')
OLS_df = OLS_df.rename(columns={'Average scale score': 'National Science Test Score (scaled)'})

## OLS Regression on isolated data for unemployment, science test scores
## and free lunch participation for the United States in 2009, 2011 and 2015

model = smf.ols('Q("National Science Test Score (scaled)") ~ Q("Unemployment Rate") + Q("Number of Students Eligible for Free/Reduced Lunch")', data=OLS_df)
results = model.fit()

OLS_df['National Science Test Score (scaled)'] = pd.to_numeric(OLS_df['National Science Test Score (scaled)'], errors='coerce')
OLS_df['Unemployment Rate'] = pd.to_numeric(OLS_df['Unemployment Rate'], errors='coerce')
OLS_df['Number of Students Eligible for Free/Reduced Lunch'] = pd.to_numeric(OLS_df['Number of Students Eligible for Free/Reduced Lunch'], errors='coerce')

model = smf.ols('Q("National Science Test Score (scaled)") ~ Q("Unemployment Rate") + Q("Number of Students Eligible for Free/Reduced Lunch")', data=OLS_df)
results = model.fit()

# Year                                                    int64
# Unemployment Rate                                     float64
# Number of Students Eligible for Free/Reduced Lunch      int64
# National Science Test Score (scaled)                   object
# dtype: object
# Year                                                    int64
# Unemployment Rate                                     float64
# Number of Students Eligible for Free/Reduced Lunch      int64
# National Science Test Score (scaled)                  float64
# dtype: object
#                                         OLS Regression Results                                       
# =====================================================================================================
# Dep. Variable:     Q("National Science Test Score (scaled)")   R-squared:                       1.000
# Model:                                                   OLS   Adj. R-squared:                    nan
# Method:                                        Least Squares   F-statistic:                       nan
# Date:                                       Wed, 08 May 2024   Prob (F-statistic):                nan
# Time:                                               17:48:55   Log-Likelihood:                 53.952
# No. Observations:                                          3   AIC:                            -101.9
# Df Residuals:                                              0   BIC:                            -104.6
# Df Model:                                                  2                                         
# Covariance Type:                                   nonrobust                                         
# ===========================================================================================================================
#                                                               coef    std err          t      P>|t|      [0.025      0.975]
# ---------------------------------------------------------------------------------------------------------------------------
# Intercept                                                 151.8093        inf          0        nan         nan         nan
# Q("Unemployment Rate")                                     -0.5131        inf         -0        nan         nan         nan
# Q("Number of Students Eligible for Free/Reduced Lunch")  1.777e-07        inf          0        nan         nan         nan
# ==============================================================================
# Omnibus:                          nan   Durbin-Watson:                   0.094
# Prob(Omnibus):                    nan   Jarque-Bera (JB):                0.407
# Skew:                          -0.502   Prob(JB):                        0.816
# Kurtosis:                       1.500   Cond. No.                     4.91e+08
# ==============================================================================

##  *** The OLS Regression is not particularly useful when there are so few data points.  However, the
##  quality of results is secondary to the Python coding for this assignment.  

