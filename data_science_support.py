# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 19:13:39 2022

@author: albre
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_heatmap(start_df, index_col:str, column:str, values:str, unique:bool=False, sum_true:bool=True):
    temp_df = start_df.groupby([index_col, column])
    if unique:
        temp_df = temp_df.nunique().reset_index()
        title = "unique_"
    elif not sum_true:
        temp_df = temp_df.mean().reset_index()
        title = "mean_"
    else:
        temp_df = temp_df.sum().reset_index()
        title = "sum_"
    temp_df = temp_df.pivot(index=index_col, columns=column, values=values)
    temp_df.fillna(0, inplace=True)
    plt.figure(figsize=(30,11))
    title+="heatmap_"+index_col+"_"+column+"_"+values
    plt.title(title)
    sns.heatmap(temp_df)
    plt.savefig(title+".png")
    plt.show()


# This section is for barplotting
def barplot_group_by_col(sns_func, start_df:pd.DataFrame, index_cols:list, list_of_cols:list, variable_name:str, x_col:str=None):
    temp_df = start_df.groupby(index_cols).sum().reset_index()
    for col in list_of_cols:
        __barplot(sns_func, start_df, index_cols, [col], variable_name+" " + str(index_cols) +" by "+ str(col))

# plots the data by the specified group
def barplot_group_by_df(sns_func, start_df:pd.DataFrame, index_cols:list, list_of_cols:list, variable_name:str):
    temp_df = start_df.groupby(index_cols).sum().reset_index()
    __barplot(sns_func, temp_df, index_cols, list_of_cols, variable_name+" ["+str(index_cols)+"] by " + str(list_of_cols))
    
def __barplot(sns_func, start_df:pd.DataFrame, index_cols:list, list_of_cols:list, variable_name:str, x_col:str=None):
    plt.figure(figsize=(30,11))
    full_list = list_of_cols.copy()
    full_list.extend(index_cols)
    if x_col is None:
        x_col = index_cols[0]
    title = "barplot_"+variable_name
    plt.title(title)
    sns_func(x=x_col, y='value', hue=variable_name, data=pd.melt(start_df[full_list], x_col, var_name=variable_name))
    plt.savefig(title+".png")
    plt.show()