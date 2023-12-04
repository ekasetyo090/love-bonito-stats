import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import matplotlib as mpl

st.set_page_config(
    page_title="Love Bonito Tokopedia Statistics",
    page_icon="📊",
    layout="wide"
)

# load csv
@st.cache_data
def load_csv(data):
    temp_df = pd.read_csv(data)
    temp_df['dateCreate'] = pd.to_datetime(temp_df['dateCreate'])
    temp_df = temp_df.drop(labels='Unnamed: 0',axis=1)
    return temp_df

# ploting Function
def top_5_plot_sort(df,labels:str,sort_labels:list,title:str):
    temp_df = df.copy()
    temp_df = temp_df.sort_values(sort_labels,ascending=False)
    colors = []
    data_var = temp_df[:5]
    for i in range(0,len(data_var),1):
        if data_var[labels].iloc[i] == data_var[labels].max():
            colors.append('#fc0303')
        else:
            colors.append('#f76565')
    #colors = ['#fc0303', '#f76565', '#f76565', '#f76565', '#f76565']
    #sns.set_palette(palette=colors)
    fig = plt.figure(figsize=(15, 5))
    #fig, ax = plt.figure(figsize=(15, 5))
    ax = sns.barplot(data=temp_df[:5], x=labels, y='product_name',hue='product_name',palette=colors)
    ax.set(ylabel="Product Name")
    ax.set_title(title)
    for p in ax.patches:
        if p.get_width()<1:
            pass
        else:
            ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
            ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) 
    
    for p in ax.patches:
        if p.get_width() <1:
            temp_anotate=round(p.get_width(),2)
        else:
            temp_anotate = f'{p.get_width():,.0f}'
            
        ax.annotate(temp_anotate, (p.get_width()/2, p.get_y() + p.get_height() / 2.),
                    ha='center', va='center', xytext=(10, 0), textcoords='offset points')
    return fig

def top_5_plot_sort_year(df,labels:str,sort_labels:list,years:int,title:str):
    temp_df = df.sort_values(sort_labels,ascending=False)
    temp_df = temp_df.loc[(temp_df['dateCreate'].dt.year == years)]
    colors = []
    data_var = temp_df[:5]
    for i in range(0,len(data_var),1):
        if data_var[labels].iloc[i] == data_var[labels].max():
            colors.append('#fc0303')
        else:
            colors.append('#f76565')
    #colors = ['#fc0303', '#f76565', '#f76565', '#f76565', '#f76565']
    #sns.set_palette(palette=colors)
    fig =plt.figure(figsize=(15, 5))
    #fig, ax = plt.figure(figsize=(15, 5))
    ax = sns.barplot(data=temp_df[:5], x=labels, y='product_name',hue='product_name',palette=colors)
    ax.set(ylabel="Product Name")
    ax.set_title(title)
    for p in ax.patches:
        if p.get_width()<1:
            pass
        else:
            ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
            ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}')) 
    
    for p in ax.patches:
        if p.get_width() <1:
            temp_anotate=round(p.get_width(),2)
        else:
            temp_anotate = f'{p.get_width():,.0f}'
            
        ax.annotate(temp_anotate, (p.get_width()/2, p.get_y() + p.get_height() / 2.),
                    ha='center', va='center', xytext=(10, 0), textcoords='offset points')
    return fig



df = load_csv('getLayoutQueryData.csv')

st.title('📊Love Bonito Tokopedia Statistics')
tab1, tab2 = st.tabs(["Visualization", "Data Preview"])
with tab1:
    st.header('Visualization')
    col1, col2, col3 = st.columns(3,gap="small")
    with col1:
        st.subheader('Total Revenue')
        total_revenue = df['productRevenue'].sum()
        st.metric(label="Total Revenue", value=f'Rp {total_revenue:,.0f}')
    with col2:
        st.subheader('AVG Rating per Product Count')
        avg_rating = round(df['rating'].mean(),3)
        st.metric(label="Average Product Rating", value=avg_rating)
    with col3:
        st.subheader('Product Count')
        product_count = len(df)
        st.metric(label="Average Product Rating", value=f'{product_count:,.0f}')

    st.write('---')
    st.subheader('Top 5 Most View Product')
    temp_plot = top_5_plot_sort(df,labels='countView',sort_labels=['countView'],title='Top 5 Most View Product')
    st.pyplot(fig=temp_plot, clear_figure=None, use_container_width=True)
    st.write('---')
    st.subheader('Top 5 Most Sold Product')
    temp_plot = top_5_plot_sort(df,labels='countSold',sort_labels=['countSold'],title='Top 5 Most Sold Product')
    st.pyplot(fig=temp_plot, clear_figure=None, use_container_width=True)
    st.write('---')
    st.subheader('Top 5 Rating Product Sold')
    temp_plot = top_5_plot_sort(df,labels='countSold',sort_labels=['rating','countReview'],title='Top 5 Highest Rating Product Sold Count')
    st.pyplot(fig=temp_plot, clear_figure=None, use_container_width=True)
    st.write('---')
    st.subheader('Top 5 Sold per View Ratio Product')
    temp_plot = top_5_plot_sort(df,labels='soldPerViewRatio',sort_labels=['soldPerViewRatio'],title='Top 5 Sold per View Ratio Product')
    st.pyplot(fig=temp_plot, clear_figure=None, use_container_width=True)
    st.write('---')
    st.subheader('Top 5 Product Revenue')
    temp_plot = top_5_plot_sort(df,labels='productRevenue',sort_labels=['productRevenue'],title='Top 5 Product Revenue')
    st.pyplot(fig=temp_plot, clear_figure=None, use_container_width=True)
    st.write('---')
    st.subheader('Top 5 Product Revenue by Year Release 2023')
    temp_plot = top_5_plot_sort_year(df,labels='productRevenue',sort_labels=['productRevenue'],title='Top 5 Product Revenue by Year Release 2023', years=2023)
    st.pyplot(fig=temp_plot, clear_figure=None, use_container_width=True)

with tab2:
    st.header('Data Preview')
    st.write('Data mined using Tokopedia backend API, Data Preview below 👇')
    #st.subheader('Data Preview')
    st.dataframe(df)

   
    