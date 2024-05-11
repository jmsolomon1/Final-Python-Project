from shiny import App, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


csv_file_path = '/Users/jasonsolomon/Documents/GitHub/final-project-python_edu/Data/Unemployment Data_2007-2015.csv'
unemployment_data = pd.read_csv(csv_file_path)

app_ui = ui.page_fluid(
    ui.input_text("year_input", "Enter a Year for US Unemployment:"),
    ui.output_plot("ts"),
    ui.output_table("unemployment_table")
)

def server(input, output, session):
    @reactive.Calc
    def get_filtered_data():
        
        try:
            year = int(input.year_input())
            filtered_data = unemployment_data[unemployment_data['Year'] == year]
        except ValueError:
          
            filtered_data = pd.DataFrame()  
        return filtered_data

    @output
    @render.plot
    def ts():
        df = get_filtered_data()
        if not df.empty:
            sns.set()
            ax = sns.lineplot(data=df, x='Label', y='Value', marker='o', linestyle='-')
            ax.set_title('US Unemployment Rate')
            ax.set_xlabel('Month')
            ax.set_ylabel('Unemployment Rate (%)')
            ax.tick_params(axis='x', rotation=45)
            return ax

    @output
    @render.table
    def unemployment_table():
        return get_filtered_data()

app = App(app_ui, server)
