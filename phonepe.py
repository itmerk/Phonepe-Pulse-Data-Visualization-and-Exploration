import time
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector
import plotly.express as px
import json
import requests

connection = mysql.connector.connect(host='localhost', user='root', password='12345', database='phonepe')
mycursor = connection.cursor()

#get data from Mysql
#aggregated_transaction
select_query1 = "SELECT * FROM aggregated_transaction"
mycursor.execute(select_query1)

columns1 = [desc[0] for desc in mycursor.description]
rows1 = mycursor.fetchall()
aggregated_transaction = pd.DataFrame(rows1, columns=columns1)

#aggregated_user_data
select_query2 = "SELECT * FROM aggregated_user"
mycursor.execute(select_query2)

columns2 = [desc[0] for desc in mycursor.description]
rows2 = mycursor.fetchall()
aggregated_user = pd.DataFrame(rows2, columns=columns2)

#aggregated_insurance_data
select_query3 = "SELECT * FROM aggregated_insurance"
mycursor.execute(select_query3)

columns3 = [desc[0] for desc in mycursor.description]
rows3 = mycursor.fetchall()
aggregated_insurance = pd.DataFrame(rows3, columns=columns3)

#map_transaction_data
select_query4 = "SELECT * FROM map_transaction"
mycursor.execute(select_query4)

columns4 = [desc[0] for desc in mycursor.description]
rows4 = mycursor.fetchall()
map_transaction = pd.DataFrame(rows4, columns=columns4)

#map_user_data
select_query5 = "SELECT * FROM map_user"
mycursor.execute(select_query5)

columns5 = [desc[0] for desc in mycursor.description]
rows5 = mycursor.fetchall()
map_user = pd.DataFrame(rows5, columns=columns5)

#map_insurance_data
select_query6 = "SELECT * FROM map_insurance"
mycursor.execute(select_query6)

columns6 = [desc[0] for desc in mycursor.description]
rows6 = mycursor.fetchall()
map_insurance = pd.DataFrame(rows6, columns=columns6)

#top_transaction_data
select_query7 = "SELECT * FROM top_transaction"
mycursor.execute(select_query7)

columns7 = [desc[0] for desc in mycursor.description]
rows7 = mycursor.fetchall()
top_transaction = pd.DataFrame(rows7, columns=columns7)

#top_user_data
select_query8 = "SELECT * FROM top_user"
mycursor.execute(select_query8)

columns8 = [desc[0] for desc in mycursor.description]
rows8 = mycursor.fetchall()
top_user = pd.DataFrame(rows8, columns=columns8)

#top_insurance_data
select_query9 = "SELECT * FROM top_insurance"
mycursor.execute(select_query9)

columns9 = [desc[0] for desc in mycursor.description]
rows9 = mycursor.fetchall()
top_insurance = pd.DataFrame(rows9, columns=columns9)


def Transaction_Amount_Count_Year_Bar_View(df,year):
    TAPY = df[df["Years"] == year]
    TAPY.reset_index(drop = True, inplace = True)

    #transaction_amount_per_year_group
    TAPYG = TAPY.groupby("States")[["Transaction_Amount","Transaction_Count"]].sum()
    TAPYG.reset_index(inplace = True)
            
    fig_amount = px.bar(TAPYG, x="States", y = "Transaction_Amount",title = f"{year} Transaction Amount",
                    color_discrete_sequence= px.colors.sequential.algae, height= 700, width= 600)

    fig_count = px.bar(TAPYG, x="States", y = "Transaction_Count",title = f"{year} Transaction Count",
                    color_discrete_sequence= px.colors.sequential.Agsunset, height= 700, width= 600)
    
    return fig_amount, fig_count

def Transaction_Amount_Count_Year_Geographic_View(df,year):
    #transaction_amount_per_year
    TAPY = df[df["Years"] == year]
    TAPY.reset_index(drop = True, inplace = True)

    #transaction_amount_per_year_group
    TAPYG = TAPY.groupby("States")[["Transaction_Amount","Transaction_Count"]].sum()
    TAPYG.reset_index(inplace = True)
    
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    states_name =[]
    for feature in data1['features']:
        states_name.append(feature["properties"]['ST_NM'])    
    states_name.sort()
                  
    fig_india_1 = px.choropleth(TAPYG, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_Amount", color_continuous_scale= "Rainbow",
                                    range_color= (TAPYG["Transaction_Amount"].min(), TAPYG["Transaction_Amount"].max()),
                                    hover_name= "States",title = f"{year} Transaction Amount", fitbounds= "locations", 
                                    height= 600, width= 600)

    fig_india_1.update_geos(visible = False)

    fig_india_2 = px.choropleth(TAPYG, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_Count", color_continuous_scale= "tealrose",
                                    range_color= (TAPYG["Transaction_Count"].min(), TAPYG["Transaction_Count"].max()),
                                    hover_name= "States",title = f"{year} Transaction_Count", fitbounds= "locations", 
                                    height= 600, width= 600)
    
    fig_india_2.update_geos(visible = False)
    
    return fig_india_1,fig_india_2

def Transaction_Amount_Count_Year_Quater_Bar_View(df, year, quarter):
    # Filter DataFrame by year and quarter
    df_filtered = df[(df["Years"] == year) & (df["Quater"] == quarter)]
    df_filtered.reset_index(drop=True, inplace=True)

    # Group by state and calculate transaction amount and count
    TAPQG = df_filtered.groupby("States")[["Transaction_Amount", "Transaction_Count"]].sum().reset_index()

    fig_amount = px.bar(TAPQG, x="States", y="Transaction_Amount", title=f"{year} YEAR {quarter} Quarter Transaction Amount",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=600, width=600)

    fig_count = px.bar(TAPQG, x="States", y="Transaction_Count", title=f"{year} YEAR {quarter} Quarter Transaction Count",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=600, width=600)
    
    return fig_amount,fig_count
        
def Transaction_Amount_Count_Year_Quater_Geographic_View(df, year, quarter):
    # Filter DataFrame by year and quarter
    df_filtered = df[(df["Years"] == year) & (df["Quater"] == quarter)]
    df_filtered.reset_index(drop=True, inplace=True)

    # Group by state and calculate transaction amount and count
    TAPQG = df_filtered.groupby("States")[["Transaction_Amount", "Transaction_Count"]].sum().reset_index()

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    states_name =[]
    for feature in data1['features']:
        states_name.append(feature["properties"]['ST_NM'])
        
    states_name.sort()
    
    fig_india_1 = px.choropleth(TAPQG, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color="Transaction_Amount", color_continuous_scale="Rainbow",
                                    range_color=(TAPQG["Transaction_Amount"].min(), TAPQG["Transaction_Amount"].max()),
                                    hover_name="States", title=f"{year} YEAR {quarter} Quarter Transaction Amount", fitbounds="locations",
                                    height=600, width=600)

    fig_india_1.update_geos(visible=False)

    fig_india_2 = px.choropleth(TAPQG, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_Count", color_continuous_scale="tealrose",
                                range_color=(TAPQG["Transaction_Count"].min(), TAPQG["Transaction_Count"].max()),
                                hover_name="States", title=f"{year} YEAR {quarter} Quarter Transaction Count", fitbounds="locations",
                                height=600, width=600)

    fig_india_2.update_geos(visible=False)
    
    return fig_india_1,fig_india_2 
        
def Transaction_Type(df, year, quater, state):
    df_filtered = df[(df["Years"] == year) & (df["Quater"] == quater) & (df["States"] == state)]
    df_filtered.reset_index(drop=True, inplace=True)
    #trans_per_type
    #trans_per_brand_group
    TAPTG = df_filtered.groupby("Transaction_Type")[["Transaction_Amount","Transaction_Count"]].sum()
    TAPTG.reset_index(inplace = True)
    
    fig_pie_1 = px.pie(data_frame= TAPTG, names="Transaction_Type", values= "Transaction_Amount",
                            width= 600, title=f"{state.upper()} Transaction Amount",
                            hole= 0.5)
    

    fig_pie_2 = px.pie(data_frame= TAPTG, names="Transaction_Type", values= "Transaction_Count",
                            width= 600, title=f"{state.upper()} Transaction Count",
                            hole= 0.5)
    return fig_pie_1,fig_pie_2
              
def User_Transaction_Brand_Per_Year(df,year):
    #trans_per_brand_year
    TPBY = df[df["Years"] == year]
    TPBY.reset_index(drop = True,inplace =True)
    #trans_per_brand__year_group
    TPBYG=pd.DataFrame(TPBY.groupby("List_of_Brand")["Transaction_Count"].sum())
    TPBYG.reset_index(inplace=True)

    fig_bar_1 = px.bar(TPBYG, x="List_of_Brand", y="Transaction_Count", title= f"{year} Transaction Count Per Brand",
                       color="List_of_Brand", width = 1000, hover_name="List_of_Brand")
    
    return fig_bar_1

def User_Transaction_Brand_Per_Quater(df, year, quater):
    #transaction_brand_per_quater = TAPY
    df_filtered = df[(df["Years"] == year) & (df["Quater"] == quater)]
    df_filtered.reset_index(drop=True, inplace=True)

    #transaction_brand_per_year_group
    TPBQG = pd.DataFrame(df_filtered.groupby("List_of_Brand")["Transaction_Count"].sum())
    TPBQG.reset_index(inplace = True)
    
    fig_bar_1 =px.bar(TPBQG, x="List_of_Brand", y="Transaction_Count", title= f"{quater} quater Transaction Count Per Brand",
                      color="List_of_Brand",width = 1000,hover_name = "List_of_Brand")

    return fig_bar_1
    
def User_Transaction_Per_State(df,year, quater, state):
    #Trans_brand_per_state
    df_filtered = df[(df["Years"] == year) & (df["Quater"] == quater) & (df["States"] == state)]
    df_filtered.reset_index(drop=True, inplace=True)

    fig_bar_1 =px.bar(df_filtered, x = "List_of_Brand", y = "Transaction_Count",color="List_of_Brand",
                    title = f"{state} Transaction Count per Brand with Percentage_Usage", width =1100)

    return fig_bar_1
    
def Map_Insurance_Per_District(df, year, quater, state):
    #map_insurance
    df_filtered = df[(df["Years"] == year) & (df["Quater"] == quater) & (df["States"] == state)]
    df_filtered.reset_index(drop=True, inplace=True)

    MIDG = df_filtered.groupby("District_Name")[["Transaction_Amount","Transaction_Count"]].sum()
    MIDG.reset_index(inplace = True)
    
    fig_bar_1 = px.bar(MIDG, x= "Transaction_Count", y ="District_Name", orientation="h", height= 600,width= 600,
                            title=f"{state} Transaction Count")
    
    fig_bar_2 = px.bar(MIDG, x= "Transaction_Amount", y ="District_Name", orientation="h", height= 600, width= 500,
                            title=f"{state} Transaction Amount")
    return fig_bar_1,fig_bar_2
        
def Map_User_Per_Year(df,year):
    #Map_user_per_year
    MUPY = df[df["Years"] == year]
    MUPY.reset_index(drop = True,inplace =True)
    #Map_user_per_year_group
    MUPYG=MUPY.groupby("States")[["No_of_registered_user","Total_of_time_appopen"]].sum()
    MUPYG.reset_index(inplace=True)

    fig_line_1 =px.line(MUPYG, x = "States", y = ["No_of_registered_user","Total_of_time_appopen"],
                    title = f"{year} year Register user and Total of time appopen", height= 800, width =1100, markers= True)
    
    return fig_line_1

def Map_User_Per_Quater(df,year,quater):
     #Map_user_per_quater
    df_filtered = df[(df["Years"] == year) & (df["Quater"] == quater)]
    df_filtered.reset_index(drop=True, inplace=True)
    #Map_user_per_quater_group
    MUPQG=df_filtered.groupby("States")[["No_of_registered_user","Total_of_time_appopen"]].sum()
    MUPQG.reset_index(inplace=True)

    fig_line_1 =px.line(MUPQG, x = "States", y = ["No_of_registered_user","Total_of_time_appopen"],
                    title = f"{df["Years"].min()} year {quater} quater Register user and Total of time appopen", height= 800,width =1000, markers= True)
    return fig_line_1

def Map_User_Per_State(df,year, quater ,state):
    MUPS =  df[(df["Years"] == year) & (df["Quater"] == quater) & (df["States"] == state)]
    MUPS.reset_index(drop = True,inplace =True)
    #Map_user_per_year_group
    MUPSG=MUPS.groupby("District_Name")[["No_of_registered_user","Total_of_time_appopen"]].sum()
    MUPSG.reset_index(inplace=True)

    fig_map_user_bar_1 =px.bar(MUPSG, x = "No_of_registered_user", y = "District_Name",orientation= "h",
                    title = f"{state.upper()} No of Register user", height= 600 ,width =500)    

    fig_map_user_bar_2 =px.bar(MUPSG, x = "Total_of_time_appopen", y = "District_Name",orientation= "h",
                    title = f"{state.upper()} Total_of_time_appopen", height= 600 ,width =500)
    
    return fig_map_user_bar_1, fig_map_user_bar_2
        
def Top_Insurance_Per_State(df, year, state, quater):
    
    df_filtered = df[(df["Years"] == year) & (df["Quater"] == quater) & (df["States"] == state)]
    df_filtered.reset_index(drop=True, inplace=True)
    
    fig_top_ins_bar_1 =px.scatter(df_filtered, x = "Quater", y = "Transaction_Amount", hover_data= "Pincode",
                    title = "Transaction_Amount", height= 600 ,width =500)

    st.plotly_chart(fig_top_ins_bar_1)

    fig_top_ins_bar_2 =px.scatter(df_filtered, x = "Quater", y = "Transaction_Count", hover_data= "Pincode",
                    title = "Transaction_Amount", height= 600 ,width =500)

    st.plotly_chart(fig_top_ins_bar_2)
        
    return fig_top_ins_bar_1 ,fig_top_ins_bar_2
        
def Top_User_Per_Year(df,year):
    #Top_User_Per_Year
    TUPY= df[df["Years"] == year]
    TUPY.reset_index(drop= True, inplace= True)

    #Top_User_Per_Year_Group
    TUPYG= pd.DataFrame(TUPY.groupby(["States","Quater"])["Total_of_User"].sum())
    TUPYG.reset_index(inplace= True)

    fig_top_plot_1= px.bar(TUPYG, x= "States", y= "Total_of_User", barmode= "group", color= "Quater",
                                width=1100, height= 600, color_continuous_scale= px.colors.sequential.OrRd)

    return fig_top_plot_1

def Top_User_Per_State(df, year, state):
    #Top_User_Per_State
    df_filtered = df[(df["Years"] == year) & (df["States"] == state)]
    df_filtered.reset_index(drop=True, inplace=True)

    #Top_User_Per_State_Group
    TUPSG= pd.DataFrame(df_filtered.groupby("Quater")["Total_of_User"].sum())
    TUPSG.reset_index(inplace= True)

    fig_top_plot_1= px.bar(TUPSG, x= "Quater", y= "Total_of_User", barmode= "group", color= "Quater",
                                width=1100, height= 500, color_continuous_scale= px.colors.sequential.Magenta)

    return fig_top_plot_1
    
#streamlit_part
st.set_page_config(layout = "wide")

with st.sidebar:
    st.sidebar.title("Navigation")
    select = option_menu("Main Menu",["Home", "Data Anaylsis", "Top charts"])
    
if select == "Home":
    st.title("Phonepe Pulse Data Visualization and Exploration")
    
    st.header("""Phonepe Pulse Dashboard""")
    
    st.write("""This dashboard provides insights and information from the Phonepe pulse Github repository in an interactive and visually appealing manner.
                To get started, please select an option from the sidebar.""")

elif select == 'Data Anaylsis':
    tab1, tab2, tab3 = st.tabs(["Aggreated Analysis"," Map Analysis", "Top Analysis"])
    
    with tab1:
        coll1,coll2,coll3,coll4,coll5 =st.columns(5)
        with coll1:
            method_1 = st.selectbox("Select the Type of Transaction", ["Agg Insurance Data", "Agg Transaction Data", "Agg User Data"])
            if method_1 == "Agg Insurance Data":
                period = st.selectbox("Select Period", ["year", "quarter"])
                if period == "year":
                    years = st.selectbox("Select Year", sorted(aggregated_insurance["Years"].unique()))
                    view_type = st.selectbox("Select the view type", ["Bar View", "Geographic View"])
                    if view_type == "Bar View":
                        if st.button("Get Yearly AI Bar Data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1)
                                    fig_amount, fig_count = Transaction_Amount_Count_Year_Bar_View(aggregated_insurance,years)
                                    st.plotly_chart(fig_amount)
                                with coll4:
                                    st.plotly_chart(fig_count)
                                    
                                    
                    elif view_type == "Geographic View":
                        if st.button("Get Yearly AI Geo Data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1)
                                    fig_india_1,fig_india_2 = Transaction_Amount_Count_Year_Geographic_View(aggregated_insurance,years)
                                    st.plotly_chart(fig_india_1)
                                with coll4:
                                    st.plotly_chart(fig_india_2)
                                    
                            
                elif period == "quarter":
                    year = st.selectbox("Select Year", sorted(aggregated_insurance["Years"].unique()))
                    quater = st.selectbox("Select Quarter", sorted(aggregated_insurance["Quater"].unique())) 
                    view_type = st.selectbox("Select the view type", ["Bar View", "Geographic View"])
                    if view_type == "Bar View":
                        if st.button("Analyze Quater AI Bar Data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1)
                                    fig_amount, fig_count = Transaction_Amount_Count_Year_Quater_Bar_View(aggregated_insurance, year, quater)
                                    st.plotly_chart(fig_amount)
                                with coll4:
                                    st.plotly_chart(fig_count)
                                
                    elif view_type == "Geographic View":
                        if st.button("Get Data Quater AI Geo Data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1)
                                    fig_india_1,fig_india_2 = Transaction_Amount_Count_Year_Quater_Geographic_View(aggregated_insurance, year, quater) 
                                    st.plotly_chart(fig_india_1)
                                with coll4:
                                    st.plotly_chart(fig_india_2) 
                
            elif method_1 == "Agg Transaction Data":
                period = st.selectbox("Select Period", ["year", "quarter","state"])
                if period == "year":
                    years = st.selectbox("Select Year", sorted(aggregated_transaction["Years"].unique()))
                    view_type = st.selectbox("Select the view type", ["Bar View", "Geographic View"])
                    if view_type == "Bar View":
                        if st.button("Get AT Yearly Bar Data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    fig_amount, fig_count = Transaction_Amount_Count_Year_Bar_View(aggregated_transaction,years)
                                    st.plotly_chart(fig_amount)
                                    with coll4:
                                        st.plotly_chart(fig_count)
                                
                    elif view_type == "Geographic View":
                        if st.button("Get AT Yearly GEO Data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    fig_india_1,fig_india_2 = Transaction_Amount_Count_Year_Geographic_View(aggregated_transaction,years)
                                    st.plotly_chart(fig_india_1)
                                    with coll4:
                                        st.plotly_chart(fig_india_2)
                                
                elif period == "quarter":
                    year = st.selectbox("Select Year", sorted(aggregated_transaction["Years"].unique()))
                    quater = st.selectbox("Select Quarter", sorted(aggregated_transaction["Quater"].unique()))
                    
                    view_type = st.selectbox("Select the view type", ["Bar View", "Geographic View"])
                    if view_type == "Bar View":
                        if st.button("Get AT Quater Bar Data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1)
                                    fig_amount, fig_count = Transaction_Amount_Count_Year_Quater_Bar_View(aggregated_transaction, year, quater)
                                    st.plotly_chart(fig_amount)
                                    with coll4:
                                        st.plotly_chart(fig_count)
                                
                    elif view_type == "Geographic View":
                        if st.button("Get AT Quater Geo Data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1)
                                    fig_india_1,fig_india_2 = Transaction_Amount_Count_Year_Quater_Geographic_View(aggregated_transaction, year, quater)
                                    st.plotly_chart(fig_india_1)
                                    with coll4:
                                        st.plotly_chart(fig_india_2) 
        
                elif period == "state":
                    year = st.selectbox("Select Year", sorted(aggregated_transaction["Years"].unique()))
                    quater = st.selectbox("Select Quarter", sorted(aggregated_transaction["Quater"].unique()))
                    state = st.selectbox("Select State", aggregated_transaction["States"].unique()) 
                    if st.button("Get AT State data"):
                        with coll2:
                            with st.spinner("Fetching data..."): 
                                time.sleep(1)
                                fig_pie_1,fig_pie_2 = Transaction_Type(aggregated_transaction, year, quater, state)
                                st.plotly_chart(fig_pie_1)
                                with coll4:
                                    st.plotly_chart(fig_pie_2)
                
            elif method_1 == "Agg User Data":
                period = st.selectbox("Select Period", ["year", "quarter","state"])
                if period == "year":
                    years = st.selectbox("Select Year", sorted(aggregated_user["Years"].unique()))
                    if st.button("Get User data by year"):
                        with coll2:
                            with st.spinner("Fetching data..."):
                                time.sleep(1)
                                fig_bar_1 = User_Transaction_Brand_Per_Year(aggregated_user,years)
                                st.plotly_chart(fig_bar_1)
                
                elif period == "quarter":
                    years = st.selectbox("Select Year", sorted(aggregated_user["Years"].unique()))
                    quater = st.selectbox("Select Quater", sorted(aggregated_user["Quater"].unique()))
                    if st.button("GET User data by Quater"):
                        with coll2:
                            with st.spinner("Fetching data..."):
                                time.sleep(1)
                                fig_bar_1 = User_Transaction_Brand_Per_Quater(aggregated_user, years, quater)
                                st.plotly_chart(fig_bar_1)
                
                elif period == "state":
                    years = st.selectbox("Select Year", sorted(aggregated_user["Years"].unique()))
                    quater = st.selectbox("Select Quater", sorted(aggregated_user["Quater"].unique()))
                    state = st.selectbox("Select State", aggregated_user["States"].unique())
                    if st.button("Get User data by state"):
                        with coll2:
                            with st.spinner("Fetching data..."):
                                fig_bar_1 = User_Transaction_Per_State(aggregated_user, years, quater, state)
                                st.plotly_chart(fig_bar_1)
              
    with tab2:
        coll1,coll2,coll3,coll4,coll5 =st.columns(5)
        with coll1:
            method_2 = st.selectbox("Select the Type of Data" ,["Map Insurance Data", "Map Transaction Data", "Map User Data"])
            if method_2 == "Map Insurance Data":
                period = st.selectbox("Select Period mi", ["Year", "Quater", "State"])
                if period == "Year":
                    years = st.selectbox("Select Year mi", sorted(map_insurance["Years"].unique()))
                    view_type = st.selectbox("Select the view type mi", ["Bar View", "Geographic View"])
                    if view_type == "Bar View":
                        if st.button("GET MI Bar data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1)
                                    fig_amount, fig_count =  Transaction_Amount_Count_Year_Bar_View(map_insurance,years)
                                st.plotly_chart(fig_amount)
                            with coll4:
                                st.plotly_chart(fig_count)
                                
                    elif view_type == "Geographic View":
                        if st.button("Get MI GEO data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1)
                                    fig_india_1,fig_india_2 = Transaction_Amount_Count_Year_Geographic_View(map_insurance,years)
                                    st.plotly_chart(fig_india_1)
                                with coll4:
                                    st.plotly_chart(fig_india_2)
                                
                elif period == "Quater":
                    years = st.selectbox("Select Year mi", sorted(map_insurance["Years"].unique()))
                    quater = st.selectbox("Select Quarter mi", sorted(map_insurance["Quater"].unique()))
                    
                    view_type = st.selectbox("Select the view type mi", ["Bar View", "Geographic View"])
                    if view_type == "Bar View":
                        if st.button("Get Quater MI BAR data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1)
                                    fig_amount, fig_count = Transaction_Amount_Count_Year_Quater_Bar_View(map_insurance, years, quater)
                                    st.plotly_chart(fig_amount)
                                with coll4:
                                    st.plotly_chart(fig_count)
                                
                    elif view_type == "Geographic View":
                        if st.button("Get Quater MI GEO data "):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1)
                                    fig_india_1,fig_india_2 = Transaction_Amount_Count_Year_Quater_Geographic_View(map_insurance, year, quater)
                                    st.plotly_chart(fig_india_1)
                                with coll4:
                                    st.plotly_chart(fig_india_2) 
                
                elif period == "State":
                    years = st.selectbox("Select Year mi", sorted(map_insurance["Years"].unique()))
                    quater = st.selectbox("Select Quarter mi", sorted(map_insurance["Quater"].unique()))
                    state = st.selectbox("Select the State mia", map_insurance["States"].unique())
                    if st.button("Get MI State data"):
                        with coll2:
                            with st.spinner("Fetching data..."): 
                                time.sleep(1)
                            fig_bar_1,fig_bar_2 = Map_Insurance_Per_District(map_insurance, years, quater, state)
                            st.plotly_chart(fig_bar_1)
                            with coll4:
                                st.plotly_chart(fig_bar_2)                
                
            elif method_2 == "Map Transaction Data":
                period = st.selectbox("Select Period OF MT", ["year", "quarter","state"])
                if period == "year":
                    years = st.selectbox("Select Year of MT", sorted(map_transaction["Years"].unique()))
                    view_type = st.selectbox("Select the view type mt", ["Bar View", "Geographic View"])
                    if view_type == "Bar View":
                        if st.button("Get MT Bar Data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    fig_amount, fig_count = Transaction_Amount_Count_Year_Bar_View(map_transaction,years)
                                    st.plotly_chart(fig_amount)
                                    with coll4:
                                        st.plotly_chart(fig_count)
                                
                    elif view_type == "Geographic View":
                        if st.button("Analyze MT GEO Data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    fig_india_1, fig_india_2 = Transaction_Amount_Count_Year_Geographic_View(map_transaction,years)
                                    st.plotly_chart(fig_india_1)
                                    with coll4:
                                        st.plotly_chart(fig_india_2)
                                
                elif period == "quarter":
                    year = st.selectbox("Select Year", sorted(map_transaction["Years"].unique()))
                    quater = st.selectbox("Select Quarter", sorted(map_transaction["Quater"].unique()))
                    
                    view_type = st.selectbox("Select the view type", ["Bar View", "Geographic View"])
                    if view_type == "Bar View":
                        if st.button("Analyze Quater MT BAR data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1)
                                    fig_amount, fig_count = Transaction_Amount_Count_Year_Quater_Bar_View(map_transaction, year, quater)
                                    st.plotly_chart(fig_amount)
                                    with coll4:   
                                        st.plotly_chart(fig_count)
                                
                    elif view_type == "Geographic View":
                        if st.button("Analyze Quater MT GEO data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1)
                                    fig_india_1,fig_india_2 = Transaction_Amount_Count_Year_Quater_Geographic_View(map_transaction, year, quater)
                                    st.plotly_chart(fig_india_1)
                                    with coll4:
                                        st.plotly_chart(fig_india_2) 
            
                elif period == "state":
                    year = st.selectbox("Select Year mi", sorted(map_insurance["Years"].unique()))
                    quater = st.selectbox("Select Quarter mi", sorted(map_insurance["Quater"].unique()))
                    state = st.selectbox("Select the State mta", map_transaction["States"].unique())
                    if st.button("Get MT state data"):
                        with coll2:
                            with st.spinner("Fetching data..."):
                                time.sleep(1)
                                fig_pie_1,fig_pie_2 = Map_Insurance_Per_District(map_transaction,year,quater,state)
                                st.plotly_chart(fig_pie_1)
                                with coll4:
                                    st.plotly_chart(fig_pie_2)
                
            elif method_2 == "Map User Data":
                period = st.selectbox("Select Period of MU", ["Year", "Quarter","State"])
                if period == "Year":
                    years = st.selectbox("Select Year", sorted(map_user["Years"].unique()))
                    if st.button("Get MU Year Data"):
                        with coll2:
                            with st.spinner("Fetching data..."):
                                time.sleep(1)
                                fig_line_1 = Map_User_Per_Year(map_user, years)
                                st.plotly_chart(fig_line_1)
                                
                elif period == "Quarter":
                    year = st.selectbox("Select Year", sorted(map_user["Years"].unique()))
                    quater = st.selectbox("Select Quarter", sorted(map_user["Quater"].unique()))
                    
                    if st.button("Get MU Quater Data"):
                        with coll2:
                            with st.spinner("Fetching data..."):
                                time.sleep(1) 
                                fig_line_1 = Map_User_Per_Quater(map_user, year, quater)
                                st.plotly_chart(fig_line_1)
            
                elif period == "State":
                    year = st.selectbox("Select Year", sorted(map_user["Years"].unique()))
                    quater = st.selectbox("Select Quarter", sorted(map_user["Quater"].unique()))
                    state = st.selectbox("Select State mu", map_user["States"].unique()) 
                    if st.button("Get MU State Data"):
                        with coll2:
                            with st.spinner("Fetching data..."):
                                time.sleep(1)
                                fig_map_user_bar_1, fig_map_user_bar_2 = Map_User_Per_State(map_user,year,quater, state)
                                st.plotly_chart(fig_map_user_bar_1)
                                with coll4:
                                    st.plotly_chart(fig_map_user_bar_2) 
            
    with tab3:
        coll1,coll2,coll3,coll4,coll5 =st.columns(5)
        with coll1:
            method_3 = st.selectbox("Select the Type of Data" ,["Top Insurance Data", "Top Transaction Data", "Top User Data"])
            if method_3 == "Top Insurance Data":
                period = st.selectbox("Select Period", ["year","state","quarter"])
                if period == "year":
                    year = st.selectbox("Select Year for TI", sorted(top_insurance["Years"].unique()))
                    view_type = st.selectbox("Select the view type TI", ["Bar View", "Geographic View"])
                    if view_type == "Bar View":
                        if st.button("Analyze TI Bar Data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1)
                                    fig_amount, fig_count = Transaction_Amount_Count_Year_Bar_View(top_insurance,years)
                                    st.plotly_chart(fig_amount)
                                    with coll4:
                                        st.plotly_chart(fig_count)
                                
                    elif view_type == "Geographic View":
                        if st.button("Analyze TI GEO Data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1)
                                    fig_india_1,fig_india_2 = Transaction_Amount_Count_Year_Geographic_View(top_insurance,years)
                                    st.plotly_chart(fig_india_1)
                                with coll4:
                                    st.plotly_chart(fig_india_2)
                
                elif period == "state":
                    year = st.selectbox("Select Year", sorted(top_insurance["Years"].unique()))
                    state = st.selectbox("Select the State ti", top_insurance["States"].unique())
                    quater = st.selectbox("Select the Quater ti", top_insurance["Quater"].unique())
                    if st.button("Analyze TI Data based on Pincode"):
                        with coll2:
                            with st.spinner("Fetching data..."):
                                fig_top_ins_bar_1 ,fig_top_ins_bar_2 = Top_Insurance_Per_State(top_insurance, year, state, quater)
                                st.plotly_chart(fig_top_ins_bar_1)
                            with coll4:
                                st.plotly_chart(fig_top_ins_bar_2)
                
                elif period == "quarter":
                    year = st.selectbox("Select the Year ti", sorted(top_insurance["Years"].unique()))
                    state = st.selectbox("Select the State ti", top_insurance["States"].unique())
                    quater = st.selectbox("Select the Quater ti", top_insurance["Quater"].unique())
                    
                    view_type = st.selectbox("Select the view type MU", ["Bar View", "Geographic View"])
                    if view_type == "Bar View":
                        if st.button("Analyze MU Bar Data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1) 
                                    fig_amount, fig_count = Transaction_Amount_Count_Year_Quater_Bar_View(top_insurance, year, quater)
                                    st.plotly_chart(fig_amount)
                                    with coll4:
                                        st.plotly_chart(fig_count)
                                
                    elif view_type == "Geographic View":
                        if st.button("Analyze MU GEO Data "):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1)
                                    fig_india_1,fig_india_2 = Transaction_Amount_Count_Year_Quater_Geographic_View(top_insurance, year, quater)
                                    st.plotly_chart(fig_india_1)
                                    with coll4:
                                        st.plotly_chart(fig_india_2)

            elif method_3 == "Top Transaction Data":
                period = st.selectbox("Select Period", ["year","state","quarter"])
                if period == "year":
                    years = st.selectbox("Select Year ti", sorted(top_transaction["Years"].unique()))
                    view_type = st.selectbox("Select the view type mt", ["Bar View", "Geographic View"])
                    if view_type == "Bar View":
                        if st.button("Analyze TT Bar Data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1)
                                    fig_amount, fig_count =Transaction_Amount_Count_Year_Bar_View(top_transaction,years)
                                    st.plotly_chart(fig_amount)
                                with coll4:
                                    st.plotly_chart(fig_count)
                                
                    elif view_type == "Geographic View":
                        if st.button("Analyze TT GEO Data"):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1)
                                    fig_india_1,fig_india_2 = Transaction_Amount_Count_Year_Geographic_View(top_transaction,years)
                                    st.plotly_chart(fig_india_1)
                                    with coll4:
                                        st.plotly_chart(fig_india_2)
                    
                elif period == "state":
                    year = st.selectbox("Select Year ti", top_transaction["Years"].unique())
                    state = st.selectbox("Select the State ti", top_transaction["States"].unique())
                    quater = st.selectbox("Select the Quater ti", top_transaction["Quater"].unique())
                    if st.button("Analyze TT Data based on Pincode"):
                        with coll2:
                            with st.spinner("Fetching data..."):
                                time.sleep(1)
                                fig_top_ins_bar_1, fig_top_ins_bar_2 = Top_Insurance_Per_State(top_transaction, year, state, quater)
                                st.plotly_chart(fig_top_ins_bar_1)
                                with coll4:
                                    st.plotly_chart(fig_top_ins_bar_2)
                
                elif period == "quarter":
                    years = st.selectbox("Select Year ti", top_transaction["Years"].unique())
                    quater = st.selectbox("Select the Quater ti", top_transaction["Quater"].unique()) 
                
                    view_type = st.selectbox("Select the view type Mu", ["Bar View", "Geographic View"])
                    if view_type == "Bar View":
                        if st.button("Analyze TT Bar Data"):
                            with coll2:
                                with st.spinner("Fetching data..."): 
                                    time.sleep(1)
                                    fig_amount, fig_count = Transaction_Amount_Count_Year_Quater_Bar_View(top_insurance, years, quater)
                                    st.plotly_chart(fig_amount)
                                    with coll4:
                                        st.plotly_chart(fig_count)
                                
                    elif view_type == "Geographic View":
                        if st.button("Analyze TT GEO Data "):
                            with coll2:
                                with st.spinner("Fetching data..."):
                                    time.sleep(1)
                                    fig_india_1,fig_india_2 = Transaction_Amount_Count_Year_Quater_Geographic_View(top_insurance, years, quater)
                                    st.plotly_chart(fig_india_1)
                                with coll4:
                                    st.plotly_chart(fig_india_2)
                
            elif method_3 == "Top User Data":
                period = st.selectbox("Select Period", ["Year","State"])
                if period == "Year":
                    year = st.selectbox("Select Year for Top user", sorted(top_user["Years"].unique()))
                    if st.button("Get TU Yearly Data"):
                        with coll2:
                            with st.spinner("Fetching data..."):
                                time.sleep(1)
                                fig_top_plot_1 = Top_User_Per_Year(top_user,year)
                                st.plotly_chart(fig_top_plot_1)
                                
                elif period == "State":
                    year = st.selectbox("Select Year for Top user", sorted(top_user["Years"].unique()))
                    state = st.selectbox("Select the Top user State", top_user["States"].unique())
                    if st.button("GET TU State Data"):
                        with coll2:
                            with st.spinner("Fetching data..."):
                                fig_top_ploted_1 = Top_User_Per_State(top_user, year, state)    
                                st.plotly_chart(fig_top_ploted_1)   
          
elif select == 'Top charts':
    question = st.selectbox("Select the Query", ('1) Top Brands Of Mobiles Used',
                                            '2) State With Highest Transaction Amount',
                                            '3) Top 10 District With Highest Transaction Amount',
                                            '4) States With Lowest Transaction Amount',
                                            '5) Top 10 Districts With Lowest Transaction Amount',
                                            '6) Top 10 No of Registered User',
                                            '7) Top 10 Total_of_Time_App_Open',
                                            '8) Transaction Amount Per Type',
                                            '9) Transaction Count Per Type',
                                            '10) Top 50 Districts With Lowest Transaction Amount'))
    
    if question =="1) Top Brands Of Mobiles Used":
        #Top Brands Of Mobiles Used
        Brand = aggregated_user[["List_of_Brand","Transaction_Count"]]
        Total_brand = pd.DataFrame(Brand.groupby("List_of_Brand")["Transaction_Count"].sum())
        Total_brand.reset_index(inplace= True)

        fig_1 = px.bar(Total_brand, x='List_of_Brand', y='Transaction_Count', color='List_of_Brand',
                    title='Transaction Count per Brand',width=1200, height= 1000,
                    labels={'List_of_Brand': 'Brand', 'Transaction_Count': 'Transaction Count'})
        st.plotly_chart(fig_1)

    elif question =="2) State With Highest Transaction Amount":
        #State With Highest Transaction Amount
        Trans_Amount = aggregated_transaction[["States","Transaction_Amount"]]
        Total_Trans_Amount =pd.DataFrame(Trans_Amount.groupby("States")["Transaction_Amount"].sum().sort_values(ascending = False).head(10).reset_index())

        fig_2 = px.pie(Total_Trans_Amount, values= "Transaction_Amount",names="States",
                    title='States With Highest Transaction Amount',
                    labels={'States': 'States', 'Transaction_Amount': 'Transaction Amount'})

        fig_2.update_traces(textposition='inside', textinfo='percent+label') # Display percentage and label inside pie slices

        st.plotly_chart(fig_2)

    elif question =="3) Top 10 District With Highest Transaction Amount":
        #District With Highest Transaction Amount
        Trans_Amount_District_high = map_transaction[["District_Name","Transaction_Amount"]]
        Total_Trans_Amount_District_high =(Trans_Amount_District_high.groupby("District_Name")["Transaction_Amount"].sum().sort_values(ascending = True).head(10).reset_index())

        fig_3 = px.bar(Total_Trans_Amount_District_high, x = "District_Name", y = "Transaction_Amount", color='District_Name',
                    title='District With Highest Transaction Amount',
                    labels={'District_Name': 'District Name', 'Transaction_Amount': 'Transaction Amount'})
        st.plotly_chart(fig_3)

    elif question =="4) States With Lowest Transaction Amount":
        #States With Lowest Transaction Amount
        Trans_Amount = aggregated_transaction[["States","Transaction_Amount"]]
        Total_Trans_Amount =pd.DataFrame(Trans_Amount.groupby("States")["Transaction_Amount"].sum().sort_values(ascending=True).head(10).reset_index())

        fig_4 = px.pie(Total_Trans_Amount, values= "Transaction_Amount",names="States",
                    title='States With Lowest Transaction Amount',
                    labels={'States': 'States', 'Transaction_Amount': 'Transaction Amount'})

        fig_4.update_traces(textposition='inside', textinfo='percent+label') # Display percentage and label inside pie slices
        st.plotly_chart(fig_4)

    elif question =="5) Top 10 Districts With Lowest Transaction Amount'":
        #District With Lowest Transaction Amount
        No_of_time_apppopen = map_user[["States","No_of_registered_user"]]
        Total_No_of_time_apppopen =(No_of_time_apppopen.groupby("States")["No_of_registered_user"].sum().sort_values(ascending = False).head(10).reset_index())

        fig_5 = px.bar(Total_No_of_time_apppopen, x='States', y='No_of_registered_user', color='States',
                    labels={ 'No_of_registered_user': 'No_of_registered_user', 'States': 'States'}, 
                    title='Top 10 Registered Users by State')
        st.plotly_chart(fig_5)

    elif question =="6) Top 10 No of Registered User":
        #Top 10 no of registered user
        No_of_time_apppopen = map_user[["States","No_of_registered_user"]]
        Total_No_of_time_apppopen =(No_of_time_apppopen.groupby("States")["No_of_registered_user"].sum().sort_values(ascending = False).head(10).reset_index())

        fig_6 = px.bar(Total_No_of_time_apppopen, x='States', y='No_of_registered_user', color='States',
                    labels={ 'No_of_registered_user': 'No_of_registered_user', 'States': 'States'}, 
                    title='Top 10 Registered Users by State')
        st.plotly_chart(fig_6)

    elif question =="7) Top 10 Total_of_Time_App_Open":
        #Top 10 Total_of_time_appopen
        No_of_time_apppopen = map_user[["States","Total_of_time_appopen"]]
        Total_No_of_time_apppopen = No_of_time_apppopen.groupby("States")["Total_of_time_appopen"].sum().sort_values(ascending = False).head(10).reset_index()

        fig_7 = px.bar(Total_No_of_time_apppopen, x = "States", y = "Total_of_time_appopen",color='States',
                    title='Top 10 States With AppOpens',
                    labels={'States': 'States Name', 'Total_of_time_appopen': 'Total of time appopen'})
        st.plotly_chart(fig_7)

    elif question =="8) Transaction Amount Per Type":
        #Transaction Amount per type
        Type = aggregated_transaction[["Transaction_Type", "Transaction_Amount"]]
        Total_Amount_Type = (Type.groupby("Transaction_Type")["Transaction_Amount"].sum().reset_index())

        fig_8 = px.pie(data_frame=Total_Amount_Type, names="Transaction_Type", values= "Transaction_Amount",
                                        width= 600, title=" Total of Transaction Amount",hole= 0.25)

        st.plotly_chart(fig_8)

    elif question =="9) Transaction Count Per Type":
        #Transaction Count per type
        Type = aggregated_transaction[["Transaction_Type", "Transaction_Count"]]
        Total_Amount_Type = (Type.groupby("Transaction_Type")["Transaction_Count"].sum().reset_index())

        fig_9 = px.pie(data_frame=Total_Amount_Type, names="Transaction_Type", values= "Transaction_Count",
                                        width= 600, title=" Total of Transaction Count",hole= 0.25)

        st.plotly_chart(fig_9)

    elif question =="10) Top 50 Districts With Lowest Transaction Amount":
        #DISTRICTS WITH 50 LOWEST TRANSACTION AMOUNT
        List_of_District= map_transaction[["District_Name", "Transaction_Amount"]]
        Total_Trans_Amount_District =(List_of_District.groupby("District_Name")["Transaction_Amount"].sum().sort_values(ascending=True).head(50).reset_index())

        fig_10 = px.bar(Total_Trans_Amount_District, x="District_Name", y="Transaction_Amount", title="DISTRICTS WITH 50 LOWEST TRANSACTION AMOUNT")
        st.plotly_chart(fig_10)
