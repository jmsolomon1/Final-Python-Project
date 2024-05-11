#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 21:34:45 2024

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

## Part 2_a Static Plots

## Static Plot for National Science Test Scores from 2009-2015
df = pd.read_excel(excel_file_path, header=8)
df['Average scale score'] = pd.to_numeric(df['Average scale score'], errors='coerce')
df.dropna(subset=['Average scale score'], inplace=True)
plt.figure(figsize=(12, 8))
for jurisdiction in df['Jurisdiction'].unique():
    subset = df[df['Jurisdiction'] == jurisdiction]
    plt.bar(subset['Year'].astype(str) + ' ' + jurisdiction, subset['Average scale score'], label=jurisdiction)
plt.title('Average Science Scores by Jurisdiction and Year')
plt.xlabel('Year and Jurisdiction')
plt.ylabel('Average Scale Score')
plt.xticks(rotation=45)  
plt.legend(title='Jurisdiction')
plt.tight_layout()
plt.show()

df = df.sort_values(by=['Year'])

plt.figure(figsize=(12, 8))
for jurisdiction in df['Jurisdiction'].unique():
    subset = df[df['Jurisdiction'] == jurisdiction]
    plt.bar(subset['Year'].astype(str) + ' ' + jurisdiction, subset['Average scale score'], label=jurisdiction)
plt.title('Average Science Scores by Jurisdiction and Year')
plt.xlabel('Year and Jurisdiction')
plt.ylabel('Average Scale Score')
plt.xticks(rotation=45)  
plt.legend(title='Jurisdiction')
plt.tight_layout()
plt.show()
##############################

## Static Plot for Unemployment Levels from 2007-2015
csv_file_path = '/Users/jasonsolomon/Documents/GitHub/final-project-python_edu/Data/Unemployment Data_2007-2015.csv'
unemployment_data = pd.read_csv(csv_file_path)
unemployment_data['Date'] = pd.to_datetime(unemployment_data['Label'])

plt.figure(figsize=(12, 6))
plt.plot(unemployment_data['Date'], unemployment_data['Value'], marker='o', linestyle='-', color='b')
plt.title('Unemployment Rate from 2007 to 2015')
plt.xlabel('Year')
plt.ylabel('Unemployment Rate (%)')
plt.grid(True)
plt.tight_layout()
plt.show()
##################################

## Static Plot for Employment levels from 2007 to 2016 (different way of looking at who has a job)
headers = {'Content-type': 'application/json'}
data = json.dumps({
    "seriesid": ['LNS11000000'],
    "startyear": "2007", 
    "endyear": "2015"
})
response = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
json_data = response.json()

if json_data['status'] == 'REQUEST_SUCCEEDED':
    rows = []
    for series in json_data['Results']['series']:
        seriesId = series['seriesID']
        for item in series['data']:
            if 'M01' <= item['period'] <= 'M12':
                rows.append({
                    "Series ID": seriesId,
                    "Year": item['year'],
                    "Period": item['period'],
                    "Value": float(item['value'])
                })
    
    df = pd.DataFrame(rows)
    df['Date'] = pd.to_datetime(df['Year'] + df['Period'].str.strip('M'), format='%Y%m')
    df.sort_values('Date', inplace=True)
    
    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df['Value'], marker='o')
    plt.title('Time Series Plot of BLS Data')
    plt.xlabel('Date')
    plt.ylabel('National Employment Level (in the thousands)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("Failed to retrieve data:", json_data['message'])
##########################################

## Static Plot for Free Lunch for entire United States
years = ['2000-01', '2010-11', '2014-15', '2015-16']

number_of_students_str = "17839867, 23544479, 25826297, 25900186.058569424"
percentage_eligible_str = "38.300180244052974, 48.1076205076587, 51.7928426074792, 52.0023058304732"

number_of_students = [float(num) for num in number_of_students_str.split(', ')]
percentage_eligible = [float(perc) for perc in percentage_eligible_str.split(', ')]

plt.figure(figsize=(14, 8))
plt.subplot(2, 1, 1)  
plt.bar(years, number_of_students, color='blue')
plt.title('Number of Students Eligible for Free/Reduced-Price Lunch in the United States')
plt.xlabel('Year')
plt.ylabel('Number of Students')
plt.gca().set_yticklabels(['{:.1f}M'.format(x / 1e6) for x in plt.gca().get_yticks()])
plt.subplot(2, 1, 2) 
plt.plot(years, percentage_eligible, color='green', marker='o', linestyle='-')
plt.title('Percentage of Students Eligible for Free/Reduced-Price Lunch in the United States')
plt.xlabel('Year')
plt.ylabel('Percentage Eligible')

plt.tight_layout()
plt.show()
#########################################

## Static Plot for Free Lunch for Maryland
years = ['2000-01', '2010-11', '2014-15', '2015-16']
number_of_students = [200000, 250000, 300000, 350000] 
percentage_eligible = [25.0, 30.0, 35.0, 40.0]  

### Plotting the Data
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)  
plt.bar(years, number_of_students, color='blue')
plt.title('Number of Students Eligible for Free/Reduced-Price Lunch in Maryland')
plt.xlabel('Year')
plt.ylabel('Number of Students')
plt.ylim([0, 400000])  

plt.subplot(2, 1, 2) 
plt.plot(years, percentage_eligible, color='green', marker='o', linestyle='-')
plt.title('Percentage of Students Eligible for Free/Reduced-Price Lunch in Maryland')
plt.xlabel('Year')
plt.ylabel('Percentage Eligible')
plt.ylim([0, 50])  
plt.tight_layout()
plt.show()
##########################################

## Part 2_b Interactive Plots with Shiny

## Code is in separate files labeled Shiny_Unemployment.py and Shiny_Science_Scores.py
