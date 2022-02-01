# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import data_science_support as dss
import re

games_df = pd.read_csv(r"C:/Users/albre/Downloads/archive/Video_Games_Sales_as_at_22_Dec_2016.csv")

# Generate groups of columns with similar information
sales_cols = ['Global_Sales', 'NA_Sales', 'JP_Sales', 'EU_Sales', 'Other_Sales']
critics_cols = ['Critic_Score', 'Critic_Count']
user_cols = ['User_Score', 'User_Count']


def generate_bar_plot_maps():
    # Generate plots to help understandthe variable relationships
    dss.barplot_group_by_df(sns.barplot, games_df, ['Platform'], sales_cols, 'Platform Sales')
    dss.barplot_group_by_col(sns.barplot, games_df, ['Platform'], sales_cols, 'Platform Sales')
    
    dss.barplot_group_by_df(sns.barplot, games_df, ['Year_of_Release'], sales_cols, 'Year over Year Sales Data')
    dss.barplot_group_by_col(sns.barplot, games_df, ['Year_of_Release'], sales_cols, 'Year over Year Sales Data')
    
    dss.barplot_group_by_col(sns.barplot, games_df, ['Genre'], sales_cols, 'Genre Sales')
    
    #dss.barplot_group_by_df(sns.barplot, games_df, ['Year_of_Release', 'Genre'], sales_cols, 'Genre and Year Sales')

def generate_heatmaps():
    dss.plot_heatmap(games_df[['Year_of_Release', 'Genre', 'Global_Sales']], 'Year_of_Release', 'Genre', 'Global_Sales')
    dss.plot_heatmap(games_df[['Platform', 'Genre', 'Global_Sales']], 'Platform', 'Genre', 'Global_Sales')
    dss.plot_heatmap(games_df[['Publisher', 'Platform', 'Global_Sales']], 'Publisher', 'Platform', 'Global_Sales')
    dss.plot_heatmap(games_df[['Platform', 'Genre', 'Name']], 'Platform', 'Genre', 'Name', unique=True)
    dss.plot_heatmap(games_df[['Year_of_Release', 'Genre', 'Name']], 'Year_of_Release', 'Genre', 'Name', unique=True)
    
def generate_modified_heatmap(index_col, col, first_col="Name", first_unique=True, second_col="Global_Sales", second_unique=False):
    if first_unique:
        first_df = games_df[[index_col, col, first_col]].groupby([index_col, col]).nunique().reset_index()
    else:
        first_df = games_df[[index_col, col, first_col]].groupby([index_col, col]).sum().reset_index()
    if second_unique:
        second_df = games_df[[index_col, col, second_col]].groupby([index_col, col]).nunique().reset_index()
    else:
        second_df = games_df[[index_col, col, second_col]].groupby([index_col, col]).sum().reset_index()
    new_df = pd.merge(first_df, second_df, how='left', left_on=[index_col, col], right_on=[index_col, col])
    new_name = first_col+" per "+second_col
    new_df[new_name] = new_df[second_col]/new_df[first_col]
    new_df = new_df.drop([first_col, second_col], axis=1)
    dss.plot_heatmap(new_df, index_col, col, new_name)

def generate_plots(list_of_cols:list, output_metrics:list=['Global_Sales', 'Critic_Score', 'User_Score']):
    for metric in output_metrics:
        for x in range(0, len(list_of_cols)):
            if metric != list_of_cols[x]:
                temp_df = games_df.copy()
                temp_df.dropna(subset=[list_of_cols[x]], inplace=True)
                dss.barplot_group_by_df(sns.barplot, temp_df, [list_of_cols[x]], [metric] , str(list_of_cols[x]))
    for metric in output_metrics:
        for x in range(0, len(list_of_cols)):
            for y in range(x+1, len(list_of_cols)):
                if metric != list_of_cols[x] and metric != list_of_cols[y]:
                    dss.plot_heatmap(games_df[[list_of_cols[x], list_of_cols[y], metric]], list_of_cols[x], list_of_cols[y], metric)
                    generate_modified_heatmap(list_of_cols[x], list_of_cols[y])
                    dss.plot_heatmap(games_df[[list_of_cols[x], list_of_cols[y], metric]], list_of_cols[x], list_of_cols[y], metric, sum_true=False)

DS = "DS"
XBOX = "XBOX"
PS = "Playstation"
PC = "Computer"
GB = "Gameboy"
NINTENDO = "Nintendo"
WII="Wii"
OTHER="Other"
platform_mapping = {
    "2600":OTHER,
    "3DO":DS,
    "3DS":DS,
    "DC":DS,
    "DS":DS,
    "GB":GB,
    "GBA":GB,
    "GC":OTHER,
    "GEN":OTHER,
    "GG":OTHER,
    "N64":NINTENDO,
    "NES":NINTENDO,
    "NG":OTHER,
    "PC":PC,
    "PCFX":PC,
    "PS":PS,
    "PS2":PS,
    "PS3":PS,
    "PS4":PS,
    "PSP":PS,
    "PSV":PS,
    "SAT":OTHER,
    "SCD":OTHER,
    "SNES":NINTENDO,
    "TG16":OTHER,
    "WS":OTHER,
    "Wii":WII,
    "WiiU":WII,
    "X360":XBOX,
    "XB":XBOX,
    "XOne":XBOX
    }

franchise_list=[
"mario",
"pokemon",
"call_of_duty",
"gran turismo",
"grand theft auto",
"animal crossing",
"halo",
"final fantasy",
"donkey kong",
"fifa",
"sims",
"zelda",
"007",
"battlefield",
"star wars",
'just dance',
'fallout',
'crash bandicoot',
'medal of honor',
'uncharted',
"assassin's creed",
'gears of war',
'street fighter',
'world of warcraft',
'sonic',
'metal gear solid',
'forza',
'destiny',
'resident evil',
'batman',
'monster hunter'
]

# lambda function to apply franchise
def find_franchise(name:str):
    name = str(name)
    for franchise in franchise_list:
        if franchise in name.lower():
            return franchise
        
def modify_user_score(user_score):
    if pd.notna(user_score) and [] == re.findall("[a-zA-z]", user_score):
        return float(user_score)-float(user_score)%0.5

games_df["Business_Platform"] = games_df['Platform'].apply(lambda x: platform_mapping[x])
games_df["Decade"] = games_df["Year_of_Release"].apply(lambda x: x - (x % 10))
games_df["Franchise"] = games_df["Name"].apply(lambda x: find_franchise(x))
games_df["Critic_Score"] = games_df["Critic_Score"].apply(lambda x: x-x%5.0)
games_df["User_Score"] = games_df["User_Score"].apply(lambda x: modify_user_score(x))
games_df["Develop_Publish"] = np.where(games_df["Developer"]==games_df["Publisher"], True, False)
games_df["User_Score_Ratio"] = np.divide(games_df["User_Score"], games_df["User_Count"])
games_df["Critic_Score_Ratio"] = np.divide(games_df["Critic_Score"], games_df["Critic_Count"])
games_df["Critic_Score_Ratio"] = games_df["Critic_Score_Ratio"].apply(lambda x: f"{x:.1f}")
games_df["User_Score_Ratio"] = games_df["User_Score_Ratio"].apply(lambda x: f"{x:.1f}")

# do the base graphical analysis
#os.mkdir("Initial Plots")
os.chdir("./Initial Plots")
generate_plots(['Franchise', 'Business_Platform', 'Platform', 'Genre', 'Critic_Score', 'Critic_Score_Ratio', 'User_Score', 'User_Score_Ratio', 'Rating', 'Develop_Publish', 'Year_of_Release', 'Decade'])

# Add platform to the dataset
#os.mkdir("../Group By Platform")
#os.chdir("../Group By Platform")
#generate_plots(['Business_Platform', 'Genre', 'Publisher', 'Year_of_Release'])

#os.mkdir("../Group by Decade")
#os.chdir("../Group by Decade")
#generate_plots(['Business_Platform', 'Genre', 'Publisher', 'Decade'])

#os.mkdir("../Group by Franchise")
#os.chdir("../Group By Franchise")
#generate_plots(['Business_Platform', 'Genre', 'Franchise', 'Publisher', 'Year_of_Release'])