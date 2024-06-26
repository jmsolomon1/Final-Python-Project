#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 21:36:37 2024

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
