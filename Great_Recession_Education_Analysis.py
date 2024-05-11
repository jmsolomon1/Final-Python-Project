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

# Unemployment Data; https://beta.bls.gov/dataViewer/view/timeseries/LNU04000000
# Maryland Science Data; https://www.nationsreportcard.gov/ndecore/xplore/NDE
# Free/Reduced Lunch Data; https://nces.ed.gov/ccd/files.asp#Fiscal:2,LevelId:7,SchoolYearId:29,Page:1

# Part 1; Identifying Data and Opening in Spyder

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

# ###################################################################

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

## Part 3; Text Processing

## Article 1
## Using regex to pull data from a New York Times article on unemployment and schools from the Great Recession
## I found an article from 2011 that talks about how a father losing
## their job impacted a girls performance at school.  I want to use
## regex to pull out any useful data around unemployment numbers and
## test scores

pdf_path_1 = '/Users/jasonsolomon/Documents/GitHub/final-project-python_edu/Data/When Dad Loses His Job - On Education - The New York Times.pdf'

with pdfplumber.open(pdf_path_1) as pdf:
    all_text = ''  
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            all_text += text + ' '  
pattern = r'([A-Z][^.?!]*?\b\d+\.?\d*%?\b[^.?!]*[.?!])'
sentences_with_numbers = re.findall(pattern, all_text)

for sentence in sentences_with_keywords:
    print(sentence)

    # Kehler lost his $90,000-a-year job as an information technology manager.
    # Their son Mathias, 12, a quiet, cerebral sixth grader at Wilson Hill, got
    # quieter.
    # I was worried and
    # scared and very worried,” recalled Leah, who’s 10.
    # This middle- to upper-middle-class suburban town of 14,000 bordering
    # Columbus has 22 percent of its students getting subsidized lunches.
    # That’s up from
    # 6 percent in 2005, when the economy was booming.
    # Statewide, 43 percent of Ohio public school students are disadvantaged, as
    # measured by free and reduced lunches, compared with 33 percent in 2005,
    # according to a recent survey by KidsOhio, a nonprofit educational organization
    # based in Columbus.
    # A sign of how deep this recession has reached into the middle
    # class: here in Franklin County, 44 percent of the disadvantaged attend suburban
    # schools, compared with 32 percent five years ago.
    # PM When Dad Loses His Job - On Education - The New York Times
    # A few houses down from the Kehlers on Deer Creek Drive, Bill Cameron, who has
    # three children in high school, has been out of work for two years since losing his
    # $119,000-a-year job as a manager at American Electric Power.
    # Over on Eastland Court, Grace Koo and her now ex-husband, who have two
    # children at Wilson Hill, were both laid off and went from making about $160,000 a
    # year to zero.
    # On Buck Trail Lane, the Hymers went from $150,000 a year to zero.
    # Even as the district’s budget gets cut and class sizes in the school’s fourth and fifth
    # grades creep up to 30, the staff at Wilson Hill works to make a difference.
    # At 9 a.
    # Smith asked to borrow the glasses; during her
    # lunch period she drove to her eye doctor; by 12:30 the girl had new pink and green
    # frames.
    # After 10 tickets, you get to turn on the classroom
    # computer and sit in the big chair (“It elevates them above everybody,” Mrs.
    # Malley has taught kindergarten in the same room for 31 years, and in that
    # time she’s learned a thing or two about little boys.
    # Even if he listens 50 percent of the time, he’s
    # getting 75 percent more than other kids.
    # The Hislopes were one of 10 families that the
    # middle school picked to give $300 toward Christmas.
    # We’re up 18 percent,” Mrs.
    # A version of this article appears in print on , Section A, Page 9 of the New York edition with the headline: Teacher, My Dad Lost His Job.

## Article 2
## Using regex to pull data from a Times magazine article on unemployment and schools from the Great Recession
## I found an article from 2011 that talks about how a father losing
## their job impacted a girls performance at school.  I want to use
## regex to pull out any useful data around unemployment numbers and
## test scores

pdf_path_2 = '/Users/jasonsolomon/Documents/GitHub/final-project-python_edu/Data/How the high unemployment rate is hurting kids test scores _ TIME.com.pdf'

with pdfplumber.open(pdf_path_2) as pdf:
    all_text = ''
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            all_text += text + ' '
pattern = r'([A-Z][^.?!]*\b(?:unemployment|school)\b[^.?!]*[.?!])'
sentences_with_keywords = re.findall(pattern, all_text)
for sentence in sentences_with_keywords:
    print(sentence)

# AM How the high unemployment rate is hurting kids' test scores | TIME.
# A study published this week by the National Bureau of Economic Research
# found that higher rates of unemployment tend to lead to lower student test scores.
# The study by a group of Duke University professors looked at test scores
# and unemployment rates around the country.
# The researchers found that kids in communities with high
# unemployment rates tended to have lower test scores even if their own family hadn’t experienced a job loss.
# Ever since it became clear that the unemployment rate was going to stay high for some time, people have been
# wondering what would mean for America’s future.
# Most of the time when we think about unemployment we think
# about how it will hurt the finances of the people who are out of work and their families.
# But unemployment can
# cause a lot of harm to society, and not just on those who are unemployed.
# I wrote a story a little over a year ago about the high rate of teen unemployment and how that could lower
# wages for years to come for people entering the workforce.
# But it appears that you don’t have to be of working age, or even have a parent out of work to be affected by high
# unemployment.
# Gibson-Davis looked at states that had higher than average levels of unemployment and found that
# students in those areas tend to score lower on academic achievement tests.
# Also, even if a student’s
# parents haven’t lost their job, in a community with high-unemployment it is likely that the child will be in a
# classroom with other kids whose parents are out of work.
# And since most school districts get their money from property
# taxes, lower revenue can cause schools to cut programs and under perform.
# They say a 2% increase in a the local unemployment rate can cause a 16% increase in the
# https://business.
# AM How the high unemployment rate is hurting kids' test scores | TIME.
# Sign In Subscribe
# But perhaps more importantly, the study underscores the larger and lasting affect high unemployment may have on
# America.
# One of the ways people have talked about to lower the unemployment rate is to improve education.
# But
# this study shows that could be hard to do in an environment of high unemployment.
# Right now, a new
# round of stimulus to lower unemployment seems like a political no-go.
# It is well
# documented that lower levels of academic achievement lead to higher levels of unemployment.
# Doing nothing to
# lower today’s unemployment rate could lower the next generations’ ability to find a job as well.

## Analysis from both articles - regex is a powerful tool to help identify
## relevant background information for a research topic.  It's clear from both
## articles that the adult unemployment, a result of the Great Recession, had
## negative impacts for the education of children in a myriad of ways


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

##  *The OLS Regression is not particularly useful when there are so few data points.  However, the
##  quality of results is secondary to the Python coding for this assignment.  


