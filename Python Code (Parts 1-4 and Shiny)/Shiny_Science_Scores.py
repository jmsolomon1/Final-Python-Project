#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 19:10:37 2024

@author: jasonsolomon
"""
import pandas as pd
from shiny import App, ui, render, reactive
import matplotlib.pyplot as plt
import seaborn as sns

## Cleaning Up Science Data for Shiny
file_path = '/Users/jasonsolomon/Documents/GitHub/final-project-python_edu/Data/NDECoreExcel_Science, Grade 8, All students - 2_20240409023345.Xls'
data = pd.read_excel(file_path, header=8)
selected_data = data.iloc[0:13]  
selected_data = selected_data.drop([2, 3]).reset_index(drop=True)
csv_file_path = '/Users/jasonsolomon/Documents/GitHub/final-project-python_edu/Data/Cleaned_Science_Scores.csv'
selected_data.to_csv(csv_file_path, index=False)

csv_file_path = '/Users/jasonsolomon/Documents/GitHub/final-project-python_edu/Data/Cleaned_Science_Scores.csv'
science_data = pd.read_csv(csv_file_path)

app_ui = ui.page_fluid(
    ui.input_text("year_input", "Enter a Year for US Science Scores:"),
    ui.output_plot("ts"),
    ui.output_table("score_table")
)

def server(input, output, session):
    @reactive.Calc
    def get_filtered_data():
  
        try:
            year = int(input.year_input())
            filtered_data = science_data[science_data['Year'] == year]
        except ValueError:
           
            filtered_data = pd.DataFrame()  
        return filtered_data

    @output
    @render.plot
    def ts():
        df = get_filtered_data()
        if not df.empty:
            sns.set()
            ax = sns.barplot(x='Jurisdiction', y='Average scale score', data=df, errorbar=None)
            ax.set_title(f'Science Scores in {input.year_input()}')
            ax.set_xlabel('Jurisdiction')
            ax.set_ylabel('Average Scale Score')
            plt.xticks(rotation=45)
            return ax

    @output
    @render.table
    def score_table():
        return get_filtered_data()

app = App(app_ui, server)
