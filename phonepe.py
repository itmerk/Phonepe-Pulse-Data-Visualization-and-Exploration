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

def Transaction_amount_count_year(df,year):
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
    
    coll1,coll2 =st.columns(2)
    with coll1:
        fig_amount = px.bar(TAPYG, x="States", y = "Transaction_Amount",title = f"{year} Transaction Amount",
                        color_discrete_sequence= px.colors.sequential.algae, height= 700, width= 600)
        st.plotly_chart(fig_amount)
        
        fig_india_1 = px.choropleth(TAPYG, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                       color= "Transaction_Amount", color_continuous_scale= "Rainbow",
                                       range_color= (TAPYG["Transaction_Amount"].min(), TAPYG["Transaction_Amount"].max()),
                                       hover_name= "States",title = f"{year} Transaction Amount", fitbounds= "locations", 
                                       height= 600, width= 600)
    
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)

    with coll2:
        fig_amount = px.bar(TAPYG, x="States", y = "Transaction_Count",title = f"{year} Transaction Count",
                        color_discrete_sequence= px.colors.sequential.Agsunset, height= 700, width= 600)
        st.plotly_chart(fig_amount)
    
        fig_india_2 = px.choropleth(TAPYG, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                        color= "Transaction_Count", color_continuous_scale= "tealrose",
                                        range_color= (TAPYG["Transaction_Count"].min(), TAPYG["Transaction_Count"].max()),
                                        hover_name= "States",title = f"{year} Transaction_Count", fitbounds= "locations", 
                                        height= 600, width= 600)
        
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)
        
    return TAPY
        
def Transaction_amount_count_quater(df, quater):
    #transaction_amount_per_quater
    TAPQ = df[df["Quater"] == quater]
    TAPQ.reset_index(drop = True, inplace = True)

    #transaction_amount_per_quater_group
    TAPQG = TAPQ.groupby("States")[["Transaction_Amount","Transaction_Count"]].sum()
    TAPQG.reset_index(inplace = True)
    
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    states_name =[]
    for feature in data1['features']:
        states_name.append(feature["properties"]['ST_NM'])
        
    states_name.sort()
    
    coll1,coll2 =st.columns(2)
    with coll1:
        fig_amount = px.bar(TAPQG, x="States", y = "Transaction_Amount",title = f"{TAPQ['Years'].min()} YEAR {quater} quater Transaction Amount",
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,height= 600, width= 600)
        st.plotly_chart(fig_amount)
        
        fig_india_1 = px.choropleth(TAPQG, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_Amount", color_continuous_scale= "Rainbow",
                                    range_color= (TAPQG["Transaction_Amount"].min(), TAPQG["Transaction_Amount"].max()),
                                    hover_name= "States",title = f"{TAPQ['Years'].min()} YEAR {quater} quater Transaction Amount", fitbounds= "locations", 
                                    height= 600, width= 600)
    
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)
        
    with coll2:
        fig_amount = px.bar(TAPQG, x="States", y = "Transaction_Count",title = f"{TAPQ['Years'].min()} YEAR {quater} quater Transaction Count",
                            color_discrete_sequence= px.colors.sequential.Aggrnyl_r,height= 600, width= 600)
        st.plotly_chart(fig_amount)

        fig_india_2 = px.choropleth(TAPQG, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_Count", color_continuous_scale= "tealrose",
                                    range_color= (TAPQG["Transaction_Count"].min(), TAPQG["Transaction_Count"].max()),
                                    hover_name= "States",title = f"{TAPQ['Years'].min()} YEAR {quater} quater Transaction_Count", fitbounds= "locations", 
                                    height= 600, width= 600)
    
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)
        
    return TAPQ
            
def Transaction_Type(df,state):
    #trans_per_type
    TAPT = df[df["States"] == state]
    TAPT.reset_index(drop = True, inplace = True)
    #trans_per_brand_group
    TAPTG = TAPT.groupby("Transaction_Type")[["Transaction_Amount","Transaction_Count"]].sum()
    TAPTG.reset_index(inplace = True)
    
    coll1,coll2 =st.columns(2)
    with coll1:
        fig_pie_1 = px.pie(data_frame= TAPTG, names="Transaction_Type", values= "Transaction_Amount",
                                width= 600, title=f"{state.upper()} Transaction Amount",
                                hole= 0.5)
        st.plotly_chart(fig_pie_1)
    with coll2:
        fig_pie_2 = px.pie(data_frame= TAPTG, names="Transaction_Type", values= "Transaction_Count",
                                width= 600, title=f"{state.upper()} Transaction Count",
                                hole= 0.5)
        st.plotly_chart(fig_pie_2)
        
#agg_user data analysis function       
def User_Transaction_Brand_Per_Year(df,year):
    #trans_per_brand_year
    TPBY = df[df["Years"] == year]
    TPBY.reset_index(drop = True,inplace =True)
    #trans_per_brand__year_group
    TPBYG=pd.DataFrame(TPBY.groupby("List_of_Brand")["Transaction_Count"].sum())
    TPBYG.reset_index(inplace=True)

    fig_bar_1 = px.bar(TPBYG, x="List_of_Brand", y="Transaction_Count", title= f"{year} Transaction Count Per Brand",
                    width = 800, color_discrete_sequence = px.colors.sequential.haline_r, hover_name="List_of_Brand")

    st.plotly_chart(fig_bar_1)
    
    return TPBY

def User_Transaction_Brand_Per_Quater(df, quater):
    #transaction_brand_per_quater = TAPY
    TPBQ = df[df["Quater"] == quater]
    TPBQ.reset_index(drop = True, inplace = True)

    #transaction_brand_per_year_group
    TPBQG = pd.DataFrame(TPBQ.groupby("List_of_Brand")["Transaction_Count"].sum())
    TPBQG.reset_index(inplace = True)
    
    fig_bar_1 =px.bar(TPBQG, x="List_of_Brand", y="Transaction_Count", title= f"{quater} quater Transaction Count Per Brand",
                    width = 800, color_discrete_sequence = px.colors.sequential.haline_r, hover_name = "List_of_Brand")

    st.plotly_chart(fig_bar_1)
    
    return TPBQ
    
def User_Transaction_Per_State(df,state):
    #Trans_brand_per_state
    TBQS = df[df["States"]== state]
    TBQS.reset_index(drop = True,inplace =True)

    fig_line_1 =px.line(TBQS, x = "List_of_Brand", y = "Transaction_Count", hover_data= "No_of_Percentage_Usage",
                    title = "Transaction Count per Brand with Percentage_Usage", width =500, markers= True)

    st.plotly_chart(fig_line_1)
    
def Map_Insurance_Per_District(df,states):
    #map_insurance
    MID= df[df["States"] == states]
    MID.reset_index(drop = True, inplace = True)

    MIDG = MID.groupby("District_Name")[["Transaction_Amount","Transaction_Count"]].sum()
    MIDG.reset_index(inplace = True)

    coll1,coll2 =st.columns(2)
    with coll1:
        fig_bar_1 = px.bar(MIDG, x= "Transaction_Count", y ="District_Name", orientation="h", height= 600,width=600,
                                title=f"{states} Transaction Count")
        st.plotly_chart(fig_bar_1)

    with coll2:
        fig_bar_2 = px.bar(MIDG, x= "Transaction_Amount", y ="District_Name", orientation="h", height= 600, width= 500,
                                title=f"{states} Transaction Amount")
        st.plotly_chart(fig_bar_2)
        
def Map_User_Per_Year(df,year):
    #Map_user_per_year
    MUPY = df[df["Years"] == year]
    MUPY.reset_index(drop = True,inplace =True)
    #Map_user_per_year_group
    MUPYG=MUPY.groupby("States")[["No_of_registered_user","Total_of_time_appopen"]].sum()
    MUPYG.reset_index(inplace=True)

    fig_line_1 =px.line(MUPYG, x = "States", y = ["No_of_registered_user","Total_of_time_appopen"],
                    title = f"{year} year Register user and Total of time appopen", height= 800, width =1000, markers= True)
    st.plotly_chart(fig_line_1)

    return MUPY
def Map_User_Per_Quater(df,quater):
     #Map_user_per_quater
    MUPQ = df[df["Quater"] == quater]
    MUPQ.reset_index(drop = True,inplace =True)
    #Map_user_per_quater_group
    MUPQG=MUPQ.groupby("States")[["No_of_registered_user","Total_of_time_appopen"]].sum()
    MUPQG.reset_index(inplace=True)

    fig_line_1 =px.line(MUPQG, x = "States", y = ["No_of_registered_user","Total_of_time_appopen"],
                    title = f"{df["Years"].min()} year {quater} quater Register user and Total of time appopen", height= 800,width =1000, markers= True)

    st.plotly_chart(fig_line_1)

    return MUPQ

def Map_User_Per_State(df,state):
    MUPS = df[df["States"] == state]
    MUPS.reset_index(drop = True,inplace =True)
    #Map_user_per_year_group
    MUPSG=MUPS.groupby("District_Name")[["No_of_registered_user","Total_of_time_appopen"]].sum()
    MUPSG.reset_index(inplace=True)

    coll1,coll2 =st.columns(2)
    with coll1:
        fig_map_user_bar_1 =px.bar(MUPSG, x = "No_of_registered_user", y = "District_Name",orientation= "h",
                        title = f"{state.upper()} No of Register user", height= 600 ,width =500)
        st.plotly_chart(fig_map_user_bar_1)
        
    with coll2:
        fig_map_user_bar_2 =px.bar(MUPSG, x = "Total_of_time_appopen", y = "District_Name",orientation= "h",
                        title = f"{state.upper()} Total_of_time_appopen", height= 600 ,width =500)
        st.plotly_chart(fig_map_user_bar_2)
        
def Top_Insurance_Per_State(df,states):
    TIPS = df[df["States"] == states]
    TIPS.reset_index(drop = True,inplace =True)
    
    coll1,coll2 =st.columns(2)
    with coll1:
        fig_top_ins_bar_1 =px.bar(TIPS, x = "Quater", y = "Transaction_Amount", hover_data= "Pincode",
                        title = "Transaction_Amount", height= 600 ,width =500)

        st.plotly_chart(fig_top_ins_bar_1)
    
    with coll2:
        fig_top_ins_bar_2 =px.bar(TIPS, x = "Quater", y = "Transaction_Count", hover_data= "Pincode",
                        title = "Transaction_Amount", height= 600 ,width =500)

        st.plotly_chart(fig_top_ins_bar_2)
        
def Top_User_Per_Year(df,year):
    #Top_User_Per_Year
    TUPY= df[df["Years"] == year]
    TUPY.reset_index(drop= True, inplace= True)

    #Top_User_Per_Year_Group
    TUPYG= pd.DataFrame(TUPY.groupby(["States","Quater"])["Total_of_User"].sum())
    TUPYG.reset_index(inplace= True)

    fig_top_plot_1= px.bar(TUPYG, x= "States", y= "Total_of_User", barmode= "group", color= "Quater",
                                width=1000, height= 800, color_continuous_scale= px.colors.sequential.OrRd)

    st.plotly_chart(fig_top_plot_1)
    
    return TUPY

def Top_User_Per_State(df,state):
    #Top_User_Per_State
    TUPS= df[df["States"] == state]
    TUPS.reset_index(drop= True, inplace= True)

    #Top_User_Per_State_Group
    TUPSG= pd.DataFrame(TUPS.groupby("Quater")["Total_of_User"].sum())
    TUPSG.reset_index(inplace= True)

    fig_top_plot_1= px.bar(TUPSG, x= "Quater", y= "Total_of_User", barmode= "group", color= "Quater",
                                width=1000, height= 800, color_continuous_scale= px.colors.sequential.Magenta)

    st.plotly_chart(fig_top_plot_1)
    
#Query Part
def question_1():
    #Top Brands Of Mobiles Used
    Brand = aggregated_user[["List_of_Brand","Transaction_Count"]]
    Total_brand = pd.DataFrame(Brand.groupby("List_of_Brand")["Transaction_Count"].sum())
    Total_brand.reset_index(inplace= True)

    fig_1 = px.bar(Total_brand, x='List_of_Brand', y='Transaction_Count', color='List_of_Brand',
                title='Transaction Count per Brand',width=1200, height= 1000,
                labels={'List_of_Brand': 'Brand', 'Transaction_Count': 'Transaction Count'})
    return st.plotly_chart(fig_1)

def question_2():
    #State With Highest Transaction Amount
    Trans_Amount = aggregated_transaction[["States","Transaction_Amount"]]
    Total_Trans_Amount =pd.DataFrame(Trans_Amount.groupby("States")["Transaction_Amount"].sum().sort_values(ascending = False).head(10).reset_index())

    fig_2 = px.pie(Total_Trans_Amount, values= "Transaction_Amount",names="States",
                title='States With Highest Transaction Amount',
                labels={'States': 'States', 'Transaction_Amount': 'Transaction Amount'})

    fig_2.update_traces(textposition='inside', textinfo='percent+label') # Display percentage and label inside pie slices

    return st.plotly_chart(fig_2)

def question_3():
    #District With Highest Transaction Amount
    Trans_Amount_District_high = map_transaction[["District_Name","Transaction_Amount"]]
    Total_Trans_Amount_District_high =(Trans_Amount_District_high.groupby("District_Name")["Transaction_Amount"].sum().sort_values(ascending = True).head(10).reset_index())

    fig_3 = px.bar(Total_Trans_Amount_District_high, x = "District_Name", y = "Transaction_Amount", color='District_Name',
                title='District With Highest Transaction Amount',
                labels={'District_Name': 'District Name', 'Transaction_Amount': 'Transaction Amount'})
    return st.plotly_chart(fig_3)

def question_4():
    #States With Lowest Transaction Amount
    Trans_Amount = aggregated_transaction[["States","Transaction_Amount"]]
    Total_Trans_Amount =pd.DataFrame(Trans_Amount.groupby("States")["Transaction_Amount"].sum().sort_values(ascending=True).head(10).reset_index())

    fig_4 = px.pie(Total_Trans_Amount, values= "Transaction_Amount",names="States",
                title='States With Lowest Transaction Amount',
                labels={'States': 'States', 'Transaction_Amount': 'Transaction Amount'})

    fig_4.update_traces(textposition='inside', textinfo='percent+label') # Display percentage and label inside pie slices
    return st.plotly_chart(fig_4)

def question_5():
    #District With Lowest Transaction Amount
    No_of_time_apppopen = map_user[["States","No_of_registered_user"]]
    Total_No_of_time_apppopen =(No_of_time_apppopen.groupby("States")["No_of_registered_user"].sum().sort_values(ascending = False).head(10).reset_index())

    fig_6 = px.bar(Total_No_of_time_apppopen, x='States', y='No_of_registered_user', color='States',
                labels={ 'No_of_registered_user': 'No_of_registered_user', 'States': 'States'}, 
                title='Top 10 Registered Users by State')
    return st.plotly_chart(fig_6)

def question_6():
    #Top 10 no of registered user
    No_of_time_apppopen = map_user[["States","No_of_registered_user"]]
    Total_No_of_time_apppopen =(No_of_time_apppopen.groupby("States")["No_of_registered_user"].sum().sort_values(ascending = False).head(10).reset_index())

    fig_6 = px.bar(Total_No_of_time_apppopen, x='States', y='No_of_registered_user', color='States',
                labels={ 'No_of_registered_user': 'No_of_registered_user', 'States': 'States'}, 
                title='Top 10 Registered Users by State')
    return st.plotly_chart(fig_6)

def question_7():
    #Top 10 Total_of_time_appopen
    No_of_time_apppopen = map_user[["States","Total_of_time_appopen"]]
    Total_No_of_time_apppopen = No_of_time_apppopen.groupby("States")["Total_of_time_appopen"].sum().sort_values(ascending = False).head(10).reset_index()

    fig_7 = px.bar(Total_No_of_time_apppopen, x = "States", y = "Total_of_time_appopen",color='States',
                title='Top 10 States With AppOpens',
                labels={'States': 'States Name', 'Total_of_time_appopen': 'Total of time appopen'})
    return st.plotly_chart(fig_7)

def question_8():
    #Transaction Amount per type
    Type = aggregated_transaction[["Transaction_Type", "Transaction_Amount"]]
    Total_Amount_Type = (Type.groupby("Transaction_Type")["Transaction_Amount"].sum().reset_index())

    fig_8 = px.pie(data_frame=Total_Amount_Type, names="Transaction_Type", values= "Transaction_Amount",
                                    width= 600, title=" Total of Transaction Amount",hole= 0.25)

    return st.plotly_chart(fig_8)

def question_9():
    #Transaction Count per type
    Type = aggregated_transaction[["Transaction_Type", "Transaction_Count"]]
    Total_Amount_Type = (Type.groupby("Transaction_Type")["Transaction_Count"].sum().reset_index())

    fig_9 = px.pie(data_frame=Total_Amount_Type, names="Transaction_Type", values= "Transaction_Count",
                                    width= 600, title=" Total of Transaction Count",hole= 0.25)

    return st.plotly_chart(fig_9)

def question_10():
    #DISTRICTS WITH 50 LOWEST TRANSACTION AMOUNT
    List_of_District= map_transaction[["District_Name", "Transaction_Amount"]]
    Total_Trans_Amount_District =(List_of_District.groupby("District_Name")["Transaction_Amount"].sum().sort_values(ascending=True).head(50).reset_index())

    fig_10 = px.bar(Total_Trans_Amount_District, x="District_Name", y="Transaction_Amount", title="DISTRICTS WITH 50 LOWEST TRANSACTION AMOUNT")
    return st.plotly_chart(fig_10)

#streamlit_part
st.set_page_config(layout = "wide")
st.title("Phonepe Pulse Data Visualization and Exploration")

with st.sidebar:
    st.write("Welcome to Phonepe web app")
    select = option_menu("Main Menu",["Home", "Data Anaylsis", "Top charts"])
    
if select == "HOME":
    pass

elif select == 'Data Anaylsis':
    tab1, tab2, tab3 = st.tabs(["Aggreated Analysis"," Map Analysis", "Top Analysis"])
    
    with tab1:
        method_1 = st.radio("Select the method" ,["Aggreated Insurance Data", "Aggreated Transaction Data", "Aggreated User Data"])
        
        if method_1 == "Aggreated Insurance Data":
            coll1,coll2 =st.columns(2)
            with coll1:
                years = st.slider("Select Year", aggregated_insurance["Years"].min(),aggregated_insurance["Years"].max(), aggregated_insurance["Years"].min())
            #Aggregated_User_Amount_Per_Year
            AIAPY = Transaction_amount_count_year(aggregated_insurance,years)
            
            coll1,coll2 =st.columns(2) 
            with coll1:
                quater = st.slider("Select Quater", AIAPY["Quater"].min(),AIAPY["Quater"].max(), AIAPY["Quater"].min())   
            #Aggregated_User_Amount_Per_state
            Transaction_amount_count_quater(AIAPY, quater)
            
        elif method_1 == "Aggreated Transaction Data":
            coll1,coll2 =st.columns(2)
            with coll1:
                years = st.slider("Select Year", aggregated_transaction["Years"].min(),aggregated_transaction["Years"].max(), aggregated_transaction["Years"].min())
            #Aggregated_Transaction_Amount_Per_Year
            ATAPY = Transaction_amount_count_year(aggregated_transaction,years)
            
            coll1,coll2 =st.columns(2) 
            with coll1:
                quater = st.slider("Select Quater", ATAPY["Quater"].min(),ATAPY["Quater"].max(), ATAPY["Quater"].min())
            #Aggregated_Transaction_Amount_Per_Quater   
            ATTYQ = Transaction_amount_count_quater(ATAPY, quater)
            
            coll1,coll2 =st.columns(2) 
            with coll1:
                state = st.selectbox("Select State", ATTYQ["States"].unique()) 
            #Aggregated_Transaction_Amount_Per_state 
            Transaction_Type(ATTYQ, state)
            
        elif method_1 == "Aggreated User Data":
            coll1,coll2 =st.columns(2)
            with coll1:
                years = st.slider("Select Year", aggregated_user["Years"].min(),aggregated_user["Years"].max(), aggregated_user["Years"].min())
            #Aggregated_User_Brand_Per_Year
            AUBPY = User_Transaction_Brand_Per_Year(aggregated_user,years)
            
            coll1,coll2 =st.columns(2) 
            with coll1:
                quater = st.slider("Select Quater", AUBPY["Quater"].min(),AUBPY["Quater"].max(), AUBPY["Quater"].min())  
            #Aggregated_User_Brand_Per_Quater
            AUBPQ=User_Transaction_Brand_Per_Quater(AUBPY, quater)
            
            coll1,coll2 =st.columns(2) 
            with coll1:
                state = st.selectbox("Select State", AUBPQ["States"].unique())
            #Aggregated_User_Brand_Per_State   
            User_Transaction_Per_State(AUBPQ,state)
              
    with tab2:
        method_2 = st.radio("Select the method" ,["Map Insurance Data", "Map Transaction Data", "Map User Data"])
        if method_2 == "Map Insurance Data":
            coll1,coll2 =st.columns(2)
            with coll1:
                years = st.slider("Select Year mi", map_insurance["Years"].min(),map_insurance["Years"].max(), map_insurance["Years"].min())
            #Map_Insurance_Amount_Per_Year
            MIAPY = Transaction_amount_count_year(map_insurance,years)
            
            coll1,coll2 =st.columns(2) 
            with coll1:
                state = st.selectbox("Select the State mi", MIAPY["States"].unique())
            #Map_Insurance_Brand_Per_State   
            Map_Insurance_Per_District(MIAPY,state)
            
            coll1,coll2 =st.columns(2) 
            with coll1:
                quater = st.slider("Select the Quater mi", MIAPY["Quater"].min(),MIAPY["Quater"].max(), MIAPY["Quater"].min())
            #Map_Insurance_Amount_Per_Quater   
            MIAPQ = Transaction_amount_count_quater(MIAPY, quater)
            
            coll1,coll2 =st.columns(2) 
            with coll1:
                state = st.selectbox("Select the State mia", MIAPY["States"].unique())
            #Map_Insurance_Brand_Per_State   
            Map_Insurance_Per_District(MIAPQ,state)
            
            
        elif method_2 == "Map Transaction Data":
            coll1,coll2 =st.columns(2)
            with coll1:
                years = st.slider("Select Year mt", map_transaction["Years"].min(),map_transaction["Years"].max(), map_transaction["Years"].min())
            #Map_Transaction_Amount_Per_Year
            MTAPY = Transaction_amount_count_year(map_transaction,years)
            
            coll1,coll2 =st.columns(2) 
            with coll1:
                state = st.selectbox("Select the State mt", MTAPY["States"].unique())
            #Map_Transaction_Brand_Per_State   
            Map_Insurance_Per_District(MTAPY,state)
            
            coll1,coll2 =st.columns(2) 
            with coll1:
                quater = st.slider("Select the Quater mt", MTAPY["Quater"].min(),MTAPY["Quater"].max(), MTAPY["Quater"].min())
            #Map_Transaction_Amount_Per_Quater   
            MTAPQ = Transaction_amount_count_quater(MTAPY, quater)
            
            coll1,coll2 =st.columns(2) 
            with coll1:
                state = st.selectbox("Select the State mta", MTAPQ["States"].unique())
            #Map_Transaction_Brand_Per_State   
            Map_Insurance_Per_District(MTAPQ,state)
            
        elif method_2 == "Map User Data":
            coll1,coll2 =st.columns(2)
            with coll1:
                years = st.slider("Select Year mt", map_user["Years"].min(),map_user["Years"].max(), map_user["Years"].min())
            #Map_user_Amount_Per_Year
            MUAPY = Map_User_Per_Year(map_user,years)
            
            coll1,coll2 =st.columns(2) 
            with coll1:
                quater = st.slider("Select the Quater mu", MUAPY["Quater"].min(),MUAPY["Quater"].max(), MUAPY["Quater"].min())
            #Map_user_Amount_Per_Quater   
            MUAPQ = Map_User_Per_Quater(MUAPY, quater)
            
            coll1,coll2 =st.columns(2) 
            with coll1:
                state = st.selectbox("Select State mu", MUAPQ["States"].unique()) 
            #Aggregated_Transaction_Amount_Per_state 
            Map_User_Per_State(MUAPQ, state)
            
    with tab3:
        method_3 = st.radio("Select the method" ,["Top Insurance Data", "Top Transaction Data", "Top User Data"])
        if method_3 == "Top Insurance Data":
            coll1,coll2 =st.columns(2)
            with coll1:
                years = st.slider("Select Year ti", top_insurance["Years"].min(),top_insurance["Years"].max(), top_insurance["Years"].min())
            #Top_Insurance_Amount_Per_Year
            TIAPY = Transaction_amount_count_year(top_insurance,years)
            
            coll1,coll2 =st.columns(2) 
            with coll1:
                state = st.selectbox("Select the State ti", TIAPY["States"].unique())
            #Top_Insurance_Brand_Per_District  
            Top_Insurance_Per_State(TIAPY,state)
            
            coll1,coll2 =st.columns(2) 
            with coll1:
                quater = st.slider("Select the Quater ti", TIAPY["Quater"].min(), TIAPY["Quater"].max(), TIAPY["Quater"].min())
            #Map_user_Amount_Per_Quater   
            Transaction_amount_count_quater(TIAPY, quater)

        elif method_3 == "Top Transaction Data":
            coll1,coll2 =st.columns(2)
            with coll1:
                years = st.slider("Select Year ti", top_transaction["Years"].min(),top_transaction["Years"].max(), top_transaction["Years"].min())
            #Top_Transaction_Amount_Per_Year
            TTAPY = Transaction_amount_count_year(top_transaction,years)
            
            coll1,coll2 =st.columns(2) 
            with coll1:
                state = st.selectbox("Select the State ti", TTAPY["States"].unique())
            #Top_Transaction_Brand_Per_District  
            Top_Insurance_Per_State(TTAPY,state)
            
            coll1,coll2 =st.columns(2) 
            with coll1:
                quater = st.slider("Select the Quater ti", TTAPY["Quater"].min(), TTAPY["Quater"].max(), TTAPY["Quater"].min())
            #Top_Transaction_Amount_Per_Quater   
            Transaction_amount_count_quater(TTAPY, quater)
            
        elif method_3 == "Top User Data":
            coll1,coll2 =st.columns(2)
            with coll1:
                years = st.slider("Select Year ti", top_user["Years"].min(),top_user["Years"].max(), top_user["Years"].min())
            #Top_User_Amount_Per_Year
            TUAPY = Top_User_Per_Year(top_user,years)
            
            coll1,coll2 =st.columns(2) 
            with coll1:
                state = st.selectbox("Select the State ti", TUAPY["States"].unique())
            #Top_Transaction_Brand_Per_District  
            Top_User_Per_State(TUAPY,state)        
          
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
        question_1()

    elif question =="2) State With Highest Transaction Amount":
        question_2()

    elif question =="3) Top 10 District With Highest Transaction Amount":
        question_3()

    elif question =="4) States With Lowest Transaction Amount":
        question_4()

    elif question =="5) Top 10 District With Lowest Transaction Amount":
        question_5()

    elif question =="6) Top 10 No of Registered User":
        question_6()

    elif question =="7) Top 10 Total_of_Time_App_Open":
        question_7()

    elif question =="8) Transaction Amount Per Type":
        question_8()

    elif question =="9) Transaction Count Per Type":
        question_9()

    elif question =="10) Top 50 Districts With Lowest Transaction Amount":
        question_10()
