#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 21:33:48 2024

@author: jasonsolomon
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 08:37:58 2024

@author: jasonsolomon
"""

# I'm going to obtain data on science test scores in Maryland from 2009 and 2015 for 8th
# grade students.  I'm also going to obtain data on the unemployment rate for those
# two years.  Finally, I'm going to look at free/reduced lunch applications and try to see
# how these different data sets overlap.

# Unemployment Data; https://beta.bls.gov/dataViewer/view/timeseries/LNU04000000
# Maryland Science Data; https://www.nationsreportcard.gov/ndecore/xplore/NDE
# Free/Reduced Lunch Data; https://nces.ed.gov/ccd/files.asp#Fiscal:2,LevelId:7,SchoolYearId:29,Page:1

# Part 1; Identifying Data and Opening in Spyder

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

## Unemployment data
## https://beta.bls.gov/dataViewer/view/timeseries/LNU04000000
csv_file_path = '/Users/jasonsolomon/Documents/GitHub/final-project-python_edu/Data/Unemployment Data_2007-2015.csv'
unemployment_data = pd.read_csv(csv_file_path)
######################################################

## Free Lunch Eligibility for the entire United States
## https://nces.ed.gov/programs/digest/d22/tables/dt22_204.10.asp
file_path = '/Users/jasonsolomon/Documents/GitHub/final-project-python_edu/Data/free lunch data.xls'
freelunch_df = pd.read_excel(file_path, header=None)  
free_lunch_title_text = freelunch_df.iloc[0, 0]
specific_values_1 = freelunch_df.iloc[1, [0, 1, 6, 12]]
column_indices_1 = [0, 1, 6, 12]  
column_names_1 = freelunch_df.iloc[1, column_indices_1]  
specific_values_2 = freelunch_df.iloc[2, [1, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16]]
column_indices_2 = [1, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16]  
column_names_2 = freelunch_df.iloc[2, column_indices_2]  
specific_values_3 = freelunch_df.iloc[3, [0, 1, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16]]
column_indices_3 = [0, 1, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16]  
column_names_3 = freelunch_df.iloc[3, column_indices_3]  
freelunch_df.iat[3, 9] = 8  
specific_values_3 = freelunch_df.iloc[3, column_indices_3]
specific_values_4 = freelunch_df.iloc[4, [0, 1, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16]]
column_indices_4 = [0, 1, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16]  
column_names_4 = freelunch_df.iloc[4, column_indices_4]  

## free lunch cleaned up data
cleaned_freelunch_df = pd.DataFrame()
cleaned_freelunch_df.attrs['Title'] = free_lunch_title_text

for i, col in enumerate(column_names_1):
    cleaned_freelunch_df[col] = specific_values_1.iloc[i]

group_1 = specific_values_2[0:4]  
group_2 = specific_values_2[4:8]  
group_3 = specific_values_2[8:12]  

new_index = len(cleaned_freelunch_df)
cleaned_freelunch_df.loc[new_index, 'State'] = None  
cleaned_freelunch_df.loc[new_index, 'Number of students'] = ', '.join(group_1.astype(str))
cleaned_freelunch_df.loc[new_index, 'Number of students eligible for free/reduced-price lunch'] = ', '.join(group_2.astype(str))
cleaned_freelunch_df.loc[new_index, 'Percent of students eligible for free/reduced-price lunch'] = ', '.join(group_3.astype(str))

group_1_3 = specific_values_3[1:5]  
group_2_3 = specific_values_3[5:9]  
group_3_3 = specific_values_3[9:13]  

new_index = len(cleaned_freelunch_df)
cleaned_freelunch_df.loc[new_index, 'State'] = specific_values_3[0]  
cleaned_freelunch_df.loc[new_index, 'Number of students'] = ', '.join(group_1_3.astype(str))
cleaned_freelunch_df.loc[new_index, 'Number of students eligible for free/reduced-price lunch'] = ', '.join(group_2_3.astype(str))
cleaned_freelunch_df.loc[new_index, 'Percent of students eligible for free/reduced-price lunch'] = ', '.join(group_3_3.astype(str))

group_1_4 = specific_values_4[1:5]  
group_2_4 = specific_values_4[5:9]
group_3_4 = specific_values_4[9:13]

new_index = len(cleaned_freelunch_df)
cleaned_freelunch_df.loc[new_index, 'State'] = specific_values_4[0]  
cleaned_freelunch_df.loc[new_index, 'Number of students'] = ', '.join(group_1_4.astype(str))
cleaned_freelunch_df.loc[new_index, 'Number of students eligible for free/reduced-price lunch'] = ', '.join(group_2_4.astype(str))
cleaned_freelunch_df.loc[new_index, 'Percent of students eligible for free/reduced-price lunch'] = ', '.join(group_3_4.astype(str))
############################################################

## free lunch eligibility just for the state of Maryland
file_path = '/Users/jasonsolomon/Documents/GitHub/final-project-python_edu/Data/free lunch data.xls'
freelunch_df = pd.read_excel(file_path, header=None)  
free_lunch_title_text = freelunch_df.iloc[0, 0]
specific_values_1 = freelunch_df.iloc[1, [0, 1, 6, 12]]
column_indices_1 = [0, 1, 6, 12]  
column_names_1 = freelunch_df.iloc[1, column_indices_1]  
specific_values_2 = freelunch_df.iloc[2, [1, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16]]
column_indices_2 = [1, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16]  
column_names_2 = freelunch_df.iloc[2, column_indices_2]  
specific_values_3 = freelunch_df.iloc[3, [0, 1, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16]]
column_indices_3 = [0, 1, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16]  
column_names_3 = freelunch_df.iloc[3, column_indices_3]  
freelunch_df.iat[3, 9] = 8  
specific_values_3 = freelunch_df.iloc[3, column_indices_3]
specific_values_29 = freelunch_df.iloc[29, [0, 1, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16]]
column_indices_29 = [0, 1, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16]  
column_names_29 = freelunch_df.iloc[29, column_indices_29]  

cleaned_freelunch_df = pd.DataFrame()
cleaned_freelunch_df.attrs['Title'] = free_lunch_title_text

for i, col in enumerate(column_names_1):
    cleaned_freelunch_df[col] = specific_values_1.iloc[i]

group_1 = specific_values_2[0:4]  
group_2 = specific_values_2[4:8]  
group_3 = specific_values_2[8:12]  

new_index = len(cleaned_freelunch_df)
cleaned_freelunch_df.loc[new_index, 'State'] = None  
cleaned_freelunch_df.loc[new_index, 'Number of students'] = ', '.join(group_1.astype(str))
cleaned_freelunch_df.loc[new_index, 'Number of students eligible for free/reduced-price lunch'] = ', '.join(group_2.astype(str))
cleaned_freelunch_df.loc[new_index, 'Percent of students eligible for free/reduced-price lunch'] = ', '.join(group_3.astype(str))

group_1_3 = specific_values_3[1:5]  
group_2_3 = specific_values_3[5:9]  
group_3_3 = specific_values_3[9:13]  

new_index = len(cleaned_freelunch_df)
cleaned_freelunch_df.loc[new_index, 'State'] = specific_values_3[0]  
cleaned_freelunch_df.loc[new_index, 'Number of students'] = ', '.join(group_1_3.astype(str))
cleaned_freelunch_df.loc[new_index, 'Number of students eligible for free/reduced-price lunch'] = ', '.join(group_2_3.astype(str))
cleaned_freelunch_df.loc[new_index, 'Percent of students eligible for free/reduced-price lunch'] = ', '.join(group_3_3.astype(str))

group_1_29 = specific_values_29[1:5]  
group_2_29 = specific_values_29[5:9]
group_3_29 = specific_values_29[9:13]

new_index = len(cleaned_freelunch_df)
cleaned_freelunch_df.loc[new_index, 'State'] = specific_values_29[0]  
cleaned_freelunch_df.loc[new_index, 'Number of students'] = ', '.join(group_1_29.astype(str))
cleaned_freelunch_df.loc[new_index, 'Number of students eligible for free/reduced-price lunch'] = ', '.join(group_2_29.astype(str))
cleaned_freelunch_df.loc[new_index, 'Percent of students eligible for free/reduced-price lunch'] = ', '.join(group_3_29.astype(str))
####################################################################

## national science scores data (2009 to 2015)
excel_file_path = '/Users/jasonsolomon/Documents/GitHub/final-project-python_edu/Data/NDECoreExcel_Science, Grade 8, All students - 2_20240409023345.Xls'
science_scores_df = pd.read_excel(excel_file_path)

## Data from API/Web Scraping
## Employment levels from 2007 to 2015
## different measurement than previous data on the unemployment rate
## bls.gov
## https://www.bls.gov/developers/api_python.htm#python1
## https://data.bls.gov/cgi-bin/surveymost

headers = {'Content-type': 'application/json'}
data = json.dumps({
    "seriesid": ['LNS11000000'],
    "startyear": "2007", 
    "endyear": "2015"
})
response = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
json_data = response.json()
if json_data['status'] == 'REQUEST_SUCCEEDED':
    for series in json_data['Results']['series']:
        x = PrettyTable(["series id", "year", "period", "value", "footnotes"])
        seriesId = series['seriesID']
        for item in series['data']:
            year = item['year']
            period = item['period']
            value = item['value']
            footnotes = ""
            for footnote in item['footnotes']:
                if footnote:
                    footnotes += footnote['text'] + ','
            if 'M01' <= period <= 'M12': 
                x.add_row([seriesId, year, period, value, footnotes.rstrip(',')])

        print(x)
else:
    print("Failed to retrieve data:", json_data['message'])
################################

##  I was unable to get the key (meta data) explaining what the data meant 
##  using the Series ID I've elected to harvest the data using the 
##  serial ID/API and getting the key from the downloaded excel document

file_path = '/Users/jasonsolomon/Documents/GitHub/final-project-python_edu/Data/SeriesReport-20240502193534_b5cd12.xlsx'
df = pd.read_excel(file_path)
first_two_columns_first_eight_rows = df.iloc[:8, :2]
######################################################