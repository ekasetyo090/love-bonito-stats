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


@st.cache_data
def load_csv(data):
    temp_df = pd.read_csv(data)
    temp_df['dateCreate'] = pd.to_datetime(temp_df['dateCreate'])
    temp_df = temp_df.drop(labels='Unnamed: 0',axis=1)
    return temp_df

@st.cache_data
def load_timeline_gtrend_csv(data):
    temp_df = pd.read_csv(data)
    temp_df.drop(index=temp_df.index[0], axis=0, inplace=True)
    temp_df = temp_df.rename(columns={'Kategori: Semua kategori': 'traffic'})
    temp_df['date'] = temp_df.index
    temp_df['date'] = pd.to_datetime(temp_df['date'])
    temp_df = temp_df.sort_values('date',ascending=True)
    temp_df["traffic"] = pd.to_numeric(temp_df["traffic"])
    return temp_df

@st.cache_data
def load_geomap_csv(data):
    temp_df = pd.read_csv(data)
    temp_df.drop(index=temp_df.index[0], axis=0, inplace=True)
    temp_df = temp_df.rename(columns={'Kategori: Semua kategori': 'traffic'})
    temp_df["traffic"] = pd.to_numeric(temp_df["traffic"])
    temp_df['province'] = temp_df.index
    temp_df = temp_df.dropna()
    return temp_df

def timeline_line_plot(df,title:str):
    fig = plt.figure(figsize=(6, 3))
    #fig, ax = plt.figure(figsize=(6, 3))
    ax = sns.lineplot(data=df, x='date', y='traffic')
    ax.set(ylabel="traffic")
    ax.set_title(title)
    return fig

def geoMap_plot(df,title:str):
    temp_df = df.sort_values('traffic',ascending=False) 
    colors = []
    data_var = temp_df
    for i in range(0,len(data_var),1):
        if data_var['traffic'].iloc[i] == data_var['traffic'].max():
            colors.append('#fc0303')
        else:
            colors.append('#f76565')
    fig = plt.figure(figsize=(6, 4.252))
    ax = sns.barplot(data=temp_df, x='traffic', y='province',hue='province',palette=colors)
    ax.set(ylabel="Province")
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


def main_data_plot(temp_df,labels:str,sort_labels:list,ascendings,numbers:int,years,titles:str,category:str):
    if years != "All":
        temp_df = temp_df.loc[(temp_df['dateCreate'].dt.year == years)]

    if category !='All':
        temp_df = temp_df.loc[(temp_df['category_name'] == category)]

    temp_df = temp_df.sort_values(sort_labels,ascending=ascendings)
    temp_df = temp_df[:numbers]
    for i in range(len(temp_df)):
        temp_names = temp_df['product_name'].iloc[i]
        temp_df['product_name'].iloc[i] = f'{temp_names} (rank {i+1})'
    colors = []
    for i in range(0,len(temp_df),1):
        if temp_df[labels].iloc[i] == temp_df[labels].max():
            colors.append('#fc0303')
        else:
            colors.append('#f76565')

    fig = plt.figure(figsize=(9, 6))
    ax = sns.barplot(data=temp_df, x=labels, y='product_name',hue='product_name',palette=colors)
    ax.set(ylabel="Product Name")
    ax.set_title(titles)
    for p in ax.patches:
        if p.get_width()<999:
            temp_anotate=p.get_width()
            pass
        else:
            temp_anotate = f'{p.get_width():,.0f}'
            ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
            ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
            # Rotating X-axis labels
            for tick in ax.get_xticklabels():
                tick.set_rotation(45)
        ax.annotate(temp_anotate, (p.get_width()/2, p.get_y() + p.get_height() / 2.),
                    ha='center', va='center', xytext=(10, 0), textcoords='offset points')      
    return fig

def main():
    df = load_csv('getLayoutQueryData.csv')
    df_timeline = load_timeline_gtrend_csv('multiTimeline.csv')
    df_geomap = load_geomap_csv('geoMap.csv')
    st.title('📊Love Bonito Tokopedia Statistics')

    tab1, tab2 = st.tabs(["Visualization", "Data Preview"])
    with tab1:
        st.header('Visualization')

    # Total Statistics
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
            st.metric(label="Product Count", value=f'{product_count:,.0f}')

    # Search Traffic
        st.write('---')
        col1, col2 = st.columns(2,gap="small")
        with col1:
            st.subheader('Search Traffic Region (ID)')
            temp_plot = timeline_line_plot(df_timeline,title='Traffic Search "Love, Bonito" on Google Trends Past 12 Month')
            st.pyplot(fig=temp_plot, clear_figure=None, use_container_width=True)

        with col2:
            st.subheader('Search Traffic By Province Region (ID)')
            temp_plot = geoMap_plot(df_geomap,title='Search Traffic By Province On Google Trends Past 12 Month ')
            st.pyplot(fig=temp_plot, clear_figure=None, use_container_width=True)

    # Main Data Visualize
        st.write('---')
        st.subheader('Product Statistics')

        col1, col2, col3, col4 = st.columns(4,gap="small")
        with st.container():
            with col1:
                number_data_to_plot = st.number_input("Number of data to visualize", value=5)
                main_catergory_select_box = st.selectbox('Product category', ['All',"Midi Dress","Blouse Wanita","Celana Panjang Wanita",
                                                                    "Tank Top Wanita","Jumpsuit & Playsuit","Rok Wanita",
                                                                    "Mini Dress","Celana Pendek Wanita","Maxi Dress",
                                                                    "Kemeja Wanita","Blazer Wanita","Crop Top Wanita",
                                                                    "Cardigan Wanita","Kaos Wanita","Vest Wanita",
                                                                    "Celana Kulot Wanita","Celana Jeans Wanita","Sweater Wanita",
                                                                    "Jacket Wanita","Setelan Celana Wanita","Coat Wanita",
                                                                    "Kimono Outer Wanita","Anting Wanita","Selempang - Sash",
                                                                    "Sandal Wanita","Shoulder Bag Wanita","Dress Denim Wanita",
                                                                    "Bustier Wanita","Set Piyama Wanita","Rok Denim Wanita",
                                                                    "Palazzo","Clutch Wanita","Celana Training Wanita","BRA",
                                                                    "Celana Dalam Wanita","Masker Kain","Daster Wanita",
                                                                    "Dress & Terusan Hamil","Kaos Polo Wanita",
                                                                    "Jaket Jeans Wanita","Buku Roman","Celana Hamil",
                                                                    "Atasan Hamil","Sneakers Wanita","Overall Denim Wanita",
                                                                    "Jumpsuit Anak Perempuan","Celana Batik Wanita",
                                                                    "Bridesmaid Dress","Bikini","Coat Muslim",
                                                                    "Celana Tidur Wanita","Blouse Anak Perempuan",
                                                                    "Scarf & Shawl Wanita","Blouse Muslim Wanita",
                                                                    "Abaya","Kemeja Denim Pria"], index=0,)
            with col2:
                colomnn_to_plot_select_box = st.selectbox('Select data to visualize', ['Rating', 'Views', 'Review Count', 'Sold Count','Transaction Reject', 'Discussion Count','Price','Stock Avaiable','Sold Per View Ratio','Product Revenue'], index=9,)
                year_filter_select_box = st.selectbox('Select year of product release', ['All',2020,2021,2022,2023], index=0,)

            with col3:
                sort_filter_by_column = st.multiselect('Sort by',['Rating', 'Views', 'Review Count', 'Sold Count','Transaction Reject', 'Discussion Count','Product Name','Price','Stock Avaiable','Sold Per View Ratio','Product Revenue'],default=['Rating','Review Count'])
            
            with col4:
                sort_filter_order = st.radio("Sort terms", ["A-Z", "Z-A"], captions = ["Ascending","Descending"],index=1)
        
        colomnn_to_plot_select_box_dict = {'Rating':'rating', 
                                            'Views':'countView', 
                                            'Review Count':'countReview', 
                                            'Sold Count':'countSold',
                                            'Transaction Reject':'transactionReject', 
                                            'Discussion Count':'countTalk',
                                            'Price':'product_price',
                                            'Stock Avaiable':'stockValue',
                                            'Sold Per View Ratio':'soldPerViewRatio',
                                            'Product Revenue':'productRevenue'}

        sort_filter_by_column_dict = {'Rating':'rating',
                                'Product Name':'product_name',
                                'Views':'countView', 
                                'Review Count':'countReview', 
                                'Sold Count':'countSold',
                                'Transaction Reject':'transactionReject', 
                                'Discussion Count':'countTalk',
                                'Price':'product_price',
                                'Stock Avaiable':'stockValue',
                                'Sold Per View Ratio':'soldPerViewRatio',
                                'Product Revenue':'productRevenue'}

        sort_filter_order_dict = {"A-Z":True,"Z-A":False}
        plot_title_sort_order_dict = {"A-Z":'Botom',"Z-A":'Top'}
        column_to_plot_value = colomnn_to_plot_select_box_dict.get(colomnn_to_plot_select_box)
        sort_filter_by_column_list = []

        for i in sort_filter_by_column:
            temp_data = sort_filter_by_column_dict.get(i)
            sort_filter_by_column_list.append(temp_data)

        plot_title = f'{plot_title_sort_order_dict.get(sort_filter_order)} {number_data_to_plot} {colomnn_to_plot_select_box} Product Statistics (Year: {year_filter_select_box})'
        
        if len(sort_filter_by_column)>0:
            temp_plot = main_data_plot(df,labels=column_to_plot_value,sort_labels=sort_filter_by_column_list,ascendings=sort_filter_order_dict.get(sort_filter_order),numbers=number_data_to_plot,years=year_filter_select_box,titles=plot_title,category=main_catergory_select_box)
            st.pyplot(fig=temp_plot, clear_figure=None, use_container_width=True)

        else:
            pass


        

    with tab2:
        st.header('Data Preview')
        st.write('Google search data obtained use google trends')
        st.write('Tokopedia data obtained use browser backend API, Data Preview below 👇')
        #st.subheader('Data Preview')
        st.dataframe(df)


   
    
if __name__ == "__main__":
    main()