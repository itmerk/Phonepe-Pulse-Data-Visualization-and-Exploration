# Import necessary libraries
import streamlit as st  # Streamlit library for building web apps
from streamlit_option_menu import option_menu  # Custom option menu component
import pandas as pd  # Pandas for data manipulation
import mysql.connector  # MySQL connector for interacting with MySQL databases
import plotly.express as px  # Plotly Express for interactive plots
import json  # JSON for handling JSON data
import requests  # Requests for making HTTP requests

# Establish a connection to the MySQL database
connection = mysql.connector.connect(host='localhost', user='root', password='12345', database='phonepe')
# Create a cursor object to execute SQL queries
mycursor = connection.cursor()

# Get data from MySQL tables and store them in DataFrames

# Query and fetch data from 'aggregated_transaction' table
select_query1 = "SELECT * FROM aggregated_transaction"
mycursor.execute(select_query1)

columns1 = [desc[0] for desc in mycursor.description]
rows1 = mycursor.fetchall()
aggregated_transaction = pd.DataFrame(rows1, columns=columns1)

# Query and fetch data from 'aggregated_user_data' table 
select_query2 = "SELECT * FROM aggregated_user"
mycursor.execute(select_query2)

columns2 = [desc[0] for desc in mycursor.description]
rows2 = mycursor.fetchall()
aggregated_user = pd.DataFrame(rows2, columns=columns2)

# Query and fetch data from 'aggregated_insurance_data' table 
select_query3 = "SELECT * FROM aggregated_insurance"
mycursor.execute(select_query3)

columns3 = [desc[0] for desc in mycursor.description]
rows3 = mycursor.fetchall()
aggregated_insurance = pd.DataFrame(rows3, columns=columns3)

# Query and fetch data from 'map_transaction_data' table 
select_query4 = "SELECT * FROM map_transaction"
mycursor.execute(select_query4)

columns4 = [desc[0] for desc in mycursor.description]
rows4 = mycursor.fetchall()
map_transaction = pd.DataFrame(rows4, columns=columns4)

# Query and fetch data from 'map_user_data' table
select_query5 = "SELECT * FROM map_user"
mycursor.execute(select_query5)

columns5 = [desc[0] for desc in mycursor.description]
rows5 = mycursor.fetchall()
map_user = pd.DataFrame(rows5, columns=columns5)

# Query and fetch data from 'map_insurance_data' table 
select_query6 = "SELECT * FROM map_insurance"
mycursor.execute(select_query6)

columns6 = [desc[0] for desc in mycursor.description]
rows6 = mycursor.fetchall()
map_insurance = pd.DataFrame(rows6, columns=columns6)

# Query and fetch data from 'top_transaction_data' table
select_query7 = "SELECT * FROM top_transaction"
mycursor.execute(select_query7)

columns7 = [desc[0] for desc in mycursor.description]
rows7 = mycursor.fetchall()
top_transaction = pd.DataFrame(rows7, columns=columns7)

# Query and fetch data from 'top_user_data' table
select_query8 = "SELECT * FROM top_user"
mycursor.execute(select_query8)

columns8 = [desc[0] for desc in mycursor.description]
rows8 = mycursor.fetchall()
top_user = pd.DataFrame(rows8, columns=columns8)

# Query and fetch data from 'top_insurance_data' table
select_query9 = "SELECT * FROM top_insurance"
mycursor.execute(select_query9)

columns9 = [desc[0] for desc in mycursor.description]
rows9 = mycursor.fetchall()
top_insurance = pd.DataFrame(rows9, columns=columns9)

def Transaction_amount_count_year(df,year):
    #Filter data for the specified year for transaction_amount_per_year
    TAPY = df[df["Years"] == year]
    #Reset the index to ensure continuous index values
    TAPY.reset_index(drop = True, inplace = True)

    #Group by states and transaction amount and count per_year_group    
    TACPYG = TAPY.groupby("States")[["Transaction_Amount","Transaction_Count"]].sum()
    #Reset the index to ensure continuous index values
    TACPYG.reset_index(inplace = True)
    
    #Load GeoJSON data for India's states
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    
    #Extract state names from GeoJSON data
    states_name =[]
    for feature in data1['features']:
        states_name.append(feature["properties"]['ST_NM'])    
    states_name.sort()
     
    #Create two columns for displaying plots side by side
    coll1,coll2 =st.columns(2)
    with coll1:
        #Plot transaction amount for each state
        fig_amount = px.bar(TACPYG, x="States", y = "Transaction_Amount",title = f"{year} Transaction Amount",
                        color_discrete_sequence= px.colors.sequential.algae, height= 700, width= 600)
        st.plotly_chart(fig_amount)
        
        fig_india_1 = px.choropleth(TACPYG, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                       color= "Transaction_Amount", color_continuous_scale= "Rainbow",
                                       range_color= (TACPYG["Transaction_Amount"].min(), TACPYG["Transaction_Amount"].max()),
                                       hover_name= "States",title = f"{year} Transaction Amount", fitbounds= "locations", 
                                       height= 600, width= 600)
    
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)

    with coll2:
        #Plot transaction count for each state
        fig_amount = px.bar(TACPYG, x="States", y = "Transaction_Count",title = f"{year} Transaction Count",
                        color_discrete_sequence= px.colors.sequential.Agsunset, height= 700, width= 600)
        st.plotly_chart(fig_amount)
    
        fig_india_2 = px.choropleth(TACPYG, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                        color= "Transaction_Count", color_continuous_scale= "tealrose",
                                        range_color= (TACPYG["Transaction_Count"].min(), TACPYG["Transaction_Count"].max()),
                                        hover_name= "States",title = f"{year} Transaction_Count", fitbounds= "locations", 
                                        height= 600, width= 600)
        
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)
    #Return filtered DataFrame for the specified year
    return TAPY
        
def Transaction_amount_count_quater(df, quater):
    #Filter data for the specified quater for transaction_amount_per__quater
    TAPQ = df[df["Quater"] == quater]
    #Reset the index to ensure continuous index values
    TAPQ.reset_index(drop = True, inplace = True)

    #Group by states and transaction amount and count per_quater_group
    TACPQG = TAPQ.groupby("States")[["Transaction_Amount","Transaction_Count"]].sum()
    #Reset the index to ensure continuous index values
    TACPQG.reset_index(inplace = True)
    
    #Load GeoJSON data for India's states
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    
    #Extract state names from GeoJSON data
    states_name =[]
    for feature in data1['features']:
        states_name.append(feature["properties"]['ST_NM'])    
    states_name.sort()
    
    #Create two columns for displaying plots side by side
    coll1,coll2 =st.columns(2)
    #Plot transaction amount for each state in the specified quarter
    with coll1:
        fig_amount = px.bar(TACPQG, x="States", y = "Transaction_Amount",title = f"{TAPQ['Years'].min()} YEAR {quater} quater Transaction Amount",
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,height= 600, width= 600)
        st.plotly_chart(fig_amount)
        
        fig_india_1 = px.choropleth(TACPQG, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_Amount", color_continuous_scale= "Rainbow",
                                    range_color= (TACPQG["Transaction_Amount"].min(), TACPQG["Transaction_Amount"].max()),
                                    hover_name= "States",title = f"{TAPQ['Years'].min()} YEAR {quater} quater Transaction Amount", fitbounds= "locations", 
                                    height= 600, width= 600)
    
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)
        
    #Plot transaction count for each state in the specified quarter   
    with coll2:
        fig_amount = px.bar(TACPQG, x="States", y = "Transaction_Count",title = f"{TAPQ['Years'].min()} YEAR {quater} quater Transaction Count",
                            color_discrete_sequence= px.colors.sequential.Aggrnyl_r,height= 600, width= 600)
        st.plotly_chart(fig_amount)

        fig_india_2 = px.choropleth(TACPQG, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                    color= "Transaction_Count", color_continuous_scale= "tealrose",
                                    range_color= (TACPQG["Transaction_Count"].min(), TACPQG["Transaction_Count"].max()),
                                    hover_name= "States",title = f"{TAPQ['Years'].min()} YEAR {quater} quater Transaction_Count", fitbounds= "locations", 
                                    height= 600, width= 600)
    
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)
    #Return filtered DataFrame for the specified Quater  
    return TAPQ
            
def Transaction_Type(df,state):
    #Filter data for the specified state_trans_per_type
    TAPT = df[df["States"] == state]
    #Reset the index to ensure continuous index values
    TAPT.reset_index(drop = True, inplace = True)
    
    #Group by transaction type and aggregate transaction amount and count_group
    TAPTG = TAPT.groupby("Transaction_Type")[["Transaction_Amount","Transaction_Count"]].sum()
    #Reset the index to ensure continuous index values
    TAPTG.reset_index(inplace = True)
    
    #Create two columns for displaying pie charts side by side
    coll1,coll2 =st.columns(2)
    
    #Plot pie chart for transaction amount per transaction type
    with coll1:
        fig_pie_1 = px.pie(data_frame= TAPTG, names="Transaction_Type", values= "Transaction_Amount",
                                width= 600, title=f"{state.upper()} Transaction Amount",
                                hole= 0.5)
        st.plotly_chart(fig_pie_1)
        
    #Plot pie chart for transaction count per transaction type
    with coll2:
        fig_pie_2 = px.pie(data_frame= TAPTG, names="Transaction_Type", values= "Transaction_Count",
                                width= 600, title=f"{state.upper()} Transaction Count",
                                hole= 0.5)
        st.plotly_chart(fig_pie_2)
      
def User_Transaction_Brand_Per_Year(df,year):
    #Filter data for the specified trans_per_brand_year
    TPBY = df[df["Years"] == year]
    #Reset the index to ensure continuous index values
    TPBY.reset_index(drop = True,inplace =True)
    
    #Group by brand and aggregate transaction count per brand for the trans_per_brand__year_group
    TPBYG=pd.DataFrame(TPBY.groupby("List_of_Brand")["Transaction_Count"].sum())
    #Reset the index to ensure continuous index values
    TPBYG.reset_index(inplace=True)

    #Create a bar chart for transaction count per brand
    fig_bar_1 = px.bar(TPBYG, x="List_of_Brand", y="Transaction_Count", title= f"{year} Transaction Count Per Brand",
                    width = 800, color_discrete_sequence = px.colors.sequential.haline_r, hover_name="List_of_Brand")

    #Display the bar chart using Plotly in Streamlit
    st.plotly_chart(fig_bar_1)
    
    #Return filtered DataFrame for the specified year
    return TPBY

def User_Transaction_Brand_Per_Quater(df, quater):
    #Filter data for the specified transaction_brand_per_quater 
    TPBQ = df[df["Quater"] == quater]
    #Reset the index to ensure continuous index values
    TPBQ.reset_index(drop = True, inplace = True)

    #Group by brand and aggregate transaction_brand_per_year_group
    TPBQG = pd.DataFrame(TPBQ.groupby("List_of_Brand")["Transaction_Count"].sum())
    #Reset the index to ensure continuous index values
    TPBQG.reset_index(inplace = True)
    
    #Create a bar chart for transaction count per brand in the specified quarter
    fig_bar_1 =px.bar(TPBQG, x="List_of_Brand", y="Transaction_Count", title= f"{quater} quater Transaction Count Per Brand",
                    width = 800, color_discrete_sequence = px.colors.sequential.haline_r, hover_name = "List_of_Brand")

    #Display the bar chart using Plotly in Streamlit
    st.plotly_chart(fig_bar_1)
    
    #Return filtered DataFrame for the specified Quater
    return TPBQ
    
def User_Transaction_Per_State(df,state):
    #Filter data for the specified Trans_brand_per_state
    TBQS = df[df["States"]== state]
    #Reset the index to ensure continuous index values
    TBQS.reset_index(drop = True,inplace =True)
    
    #Create a line plot
    fig_line_1 =px.line(TBQS, x = "List_of_Brand", y = "Transaction_Count", hover_data= "No_of_Percentage_Usage",
                    title = "Transaction Count per Brand with Percentage_Usage", width =500, markers= True)

    #Display the plot
    st.plotly_chart(fig_line_1)
    
def Map_Insurance_Per_District(df,states):
    #Extract data for the specified map_insurance_district
    MID= df[df["States"] == states]
    #Reset the index to ensure continuous index values
    MID.reset_index(drop = True, inplace = True)

    #Group the data by district name and sum transaction amount and count
    MIDG = MID.groupby("District_Name")[["Transaction_Amount","Transaction_Count"]].sum()
    #Reset the index to ensure continuous index values
    MIDG.reset_index(inplace = True)

    #Create two columns for displaying plots side by side
    coll1,coll2 =st.columns(2)
    with coll1:
        fig_bar_1 = px.bar(MIDG, x= "Transaction_Count", y ="District_Name", orientation="h", height= 600,width=600,
                                title=f"{states} Transaction Count")
        #Display the plot
        st.plotly_chart(fig_bar_1)

    with coll2:
        fig_bar_2 = px.bar(MIDG, x= "Transaction_Amount", y ="District_Name", orientation="h", height= 600, width= 500,
                                title=f"{states} Transaction Amount")
        #Display the plot
        st.plotly_chart(fig_bar_2)
        
def Map_User_Per_Year(df,year): 
    #Extract data for the specified Map_user_per_year
    MUPY = df[df["Years"] == year]
    #Reset the index to ensure continuous index values
    MUPY.reset_index(drop = True,inplace =True)
    #Map_user_per_year_Group the data by states and sum the number of registered users and total time appopen
    MUPYG=MUPY.groupby("States")[["No_of_registered_user","Total_of_time_appopen"]].sum()
    #Reset the index to ensure continuous index values
    MUPYG.reset_index(inplace=True)

    # Create a line chart showing the number of registered users and total time appopen for each state
    fig_line_1 =px.line(MUPYG, x = "States", y = ["No_of_registered_user","Total_of_time_appopen"],
                    title = f"{year} year Register user and Total of time appopen", height= 800, width =1000, markers= True)
    #Display the plot
    st.plotly_chart(fig_line_1)
    #Return the filtered DataFrame for the specified year
    return MUPY

def Map_User_Per_Quater(df,quater):
    #Filter the DataFrame to get data for the specified Map_user_per_quater
    MUPQ = df[df["Quater"] == quater]
    MUPQ.reset_index(drop = True,inplace =True)
    #Map_user_per_quater_group the data by states and sum the number of registered users and total time app open
    MUPQG=MUPQ.groupby("States")[["No_of_registered_user","Total_of_time_appopen"]].sum()
    #Reset the index to ensure continuous index values
    MUPQG.reset_index(inplace=True)
    #Create a line chart showing the number of registered users and total time app open per state
    fig_line_1 =px.line(MUPQG, x = "States", y = ["No_of_registered_user","Total_of_time_appopen"],
                    title = f"{df["Years"].min()} year {quater} quater Register user and Total of time appopen", height= 800,width =1000, markers= True)
    #Display the plot
    st.plotly_chart(fig_line_1)
    #Return the filtered DataFrame for the specified quater
    return MUPQ

def Map_User_Per_State(df,state):
    #Filter data for the specified Map_user_per_State
    MUPS = df[df["States"] == state]
    #Reset the index to ensure continuous index values
    MUPS.reset_index(drop = True,inplace =True)
    #Map_user_per_year_group
    MUPSG=MUPS.groupby("District_Name")[["No_of_registered_user","Total_of_time_appopen"]].sum()
    #Reset the index to ensure continuous index values
    MUPSG.reset_index(inplace=True)

    #Create two columns for displaying plots side by side
    coll1,coll2 =st.columns(2)
    with coll1:
        fig_map_user_bar_1 =px.bar(MUPSG, x = "No_of_registered_user", y = "District_Name",orientation= "h",
                        title = f"{state.upper()} No of Register user", height= 600 ,width =500)
        #Display the plot
        st.plotly_chart(fig_map_user_bar_1)
        
    with coll2:
        fig_map_user_bar_2 =px.bar(MUPSG, x = "Total_of_time_appopen", y = "District_Name",orientation= "h",
                        title = f"{state.upper()} Total_of_time_appopen", height= 600 ,width =500)
        #Display the plot
        st.plotly_chart(fig_map_user_bar_2)
        
def Top_Insurance_Per_State(df,states):
    #Filter data for the specified Top_insurance_per_state
    TIPS = df[df["States"] == states]
    #Reset the index to ensure continuous index values
    TIPS.reset_index(drop = True,inplace =True)
    
    #Create two columns for displaying plots side by side
    coll1,coll2 =st.columns(2)
    with coll1:
        fig_top_ins_bar_1 =px.bar(TIPS, x = "Quater", y = "Transaction_Amount", hover_data= "Pincode",
                        title = "Transaction_Amount", height= 600 ,width =500)
        #Display the plot
        st.plotly_chart(fig_top_ins_bar_1)

    with coll2:
        fig_top_ins_bar_2 =px.bar(TIPS, x = "Quater", y = "Transaction_Count", hover_data= "Pincode",
                        title = "Transaction_Amount", height= 600 ,width =500)
        #Display the plot
        st.plotly_chart(fig_top_ins_bar_2)
        
def Top_User_Per_Year(df,year):
    #Filter data for the specified Top_User_Per_Year
    TUPY= df[df["Years"] == year]
    #Reset the index to ensure continuous index values
    TUPY.reset_index(drop= True, inplace= True)

    #Group the data by states and quarter, and sum the total number of users
    TUPYG= pd.DataFrame(TUPY.groupby(["States","Quater"])["Total_of_User"].sum())
    #Reset the index to ensure continuous index values
    TUPYG.reset_index(inplace= True)
    
    #Create a bar plot showing the total number of users per state, grouped by quarter
    fig_top_plot_1= px.bar(TUPYG, x= "States", y= "Total_of_User", barmode= "group", color= "Quater",
                                width=1000, height= 800, color_continuous_scale= px.colors.sequential.OrRd)
    #Display the plot
    st.plotly_chart(fig_top_plot_1)
    # Return the filtered DataFrame per year
    return TUPY

def Top_User_Per_State(df,state):
    #Filter data for the specified Top_User_Per_State
    TUPS= df[df["States"] == state]
    #Reset the index to ensure continuous index values
    TUPS.reset_index(drop= True, inplace= True)

    #Group the data by quarter and sum the total number of Top_User_Per_State_Group
    TUPSG= pd.DataFrame(TUPS.groupby("Quater")["Total_of_User"].sum())
    #Reset the index to ensure continuous index values
    TUPSG.reset_index(inplace= True)
    #Create a bar plot showing the total number of users per quarter
    fig_top_plot_1= px.bar(TUPSG, x= "Quater", y= "Total_of_User", barmode= "group", color= "Quater",
                                width=1000, height= 800, color_continuous_scale= px.colors.sequential.Magenta)
    #Display the plot
    st.plotly_chart(fig_top_plot_1)
    

#streamlit_part
st.set_page_config(layout = "wide")

with st.sidebar:
    #Add a title to the sidebar
    st.sidebar.title("Navigation")
    #Create a dropdown menu for navigation
    select = option_menu("Main Menu",["HOME", "Data Anaylsis", "Top charts"])

#Check the selection made in the dropdown menu   
if select == "HOME":
    #Display content for the "HOME" selection
    st.title("Phonepe Pulse Data Visualization and Exploration")
    #Display a header
    st.header("""Phonepe Pulse Dashboard""")
    #Display introductory text
    st.write("""This dashboard provides insights and information from the Phonepe pulse Github repository in an interactive and visually appealing manner.
                To get started, please select an option from the sidebar.""")

elif select == 'Data Anaylsis':
    #Display content for the "Data Anaylsis" selection
    tab1, tab2, tab3 = st.tabs(["Aggreated Analysis"," Map Analysis", "Top Analysis"])
    
    with tab1:
        #Present a radio button to select the method
        method_1 = st.radio("Select the method" ,["Aggreated Insurance Data", "Aggreated Transaction Data", "Aggreated User Data"])
        
        if method_1 == "Aggreated Insurance Data":
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2)
            with coll1:
                #Present a slider to select the year within the range of available years in aggregated_insurance
                years = st.slider("Select Year", aggregated_insurance["Years"].min(),aggregated_insurance["Years"].max(), aggregated_insurance["Years"].min())
            #Calculate Aggregated_User_Amount_Per_Year with return filter data per year as AIAPY
            AIAPY = Transaction_amount_count_year(aggregated_insurance,years)
            
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2) 
            with coll1:
                #Present a slider to select the Quater within the range of available Quater in AIAPY filter data for above function
                quater = st.slider("Select Quater", AIAPY["Quater"].min(),AIAPY["Quater"].max(), AIAPY["Quater"].min())   
            #Calculate Aggregated_User_Amount_Per_state using filter data using AIAPY
            Transaction_amount_count_quater(AIAPY, quater)
            
        elif method_1 == "Aggreated Transaction Data":
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2)
            with coll1:
                #Present a slider to select the year within the range of available years in aggregated_transaction
                years = st.slider("Select Year", aggregated_transaction["Years"].min(),aggregated_transaction["Years"].max(), aggregated_transaction["Years"].min())
            #Calculate Aggregated_Transaction_Amount_Per_Year with return filter data per year as ATAPY
            ATAPY = Transaction_amount_count_year(aggregated_transaction,years)
            
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2) 
            with coll1:
                #Present a slider to select the Quater within the range of available Quater in ATAPY filter data for above function
                quater = st.slider("Select Quater", ATAPY["Quater"].min(),ATAPY["Quater"].max(), ATAPY["Quater"].min())
            #Calculate Aggregated_Transaction_Amount_Per_Quater   
            ATTYQ = Transaction_amount_count_quater(ATAPY, quater)
            
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2) 
            with coll1:
                #Present a dropdown to select the state within the available states in ATTYQ filter data for above function
                state = st.selectbox("Select State", ATTYQ["States"].unique()) 
            #Calculate Aggregated_Transaction_Amount_Per_state with return filter data per Quater as ATTYQ
            Transaction_Type(ATTYQ, state)
            
        elif method_1 == "Aggreated User Data":
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2)
            with coll1:
                #Present a slider to select the year within the range of available years in aggregated_user
                years = st.slider("Select Year", aggregated_user["Years"].min(),aggregated_user["Years"].max(), aggregated_user["Years"].min())
            #Calculate Aggregated_User_Brand_Per_Year with return filter data per year as AUBPY 
            AUBPY = User_Transaction_Brand_Per_Year(aggregated_user,years)
            
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2) 
            with coll1:
                #Present a slider to select the year within the range of available Quater in AUBPY
                quater = st.slider("Select Quater", AUBPY["Quater"].min(),AUBPY["Quater"].max(), AUBPY["Quater"].min())  
            #Calculate Aggregated_User_Brand_Per_Quater with return filter data per year as AUBPQ
            AUBPQ = User_Transaction_Brand_Per_Quater(AUBPY, quater)
            
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2) 
            with coll1:
                #Present a dropdown to select the state within the available states in AUBPQ
                state = st.selectbox("Select State", AUBPQ["States"].unique())
            #Calculate Aggregated_User_Brand_Per_State 
            User_Transaction_Per_State(AUBPQ,state)
              
    with tab2:
        method_2 = st.radio("Select the method" ,["Map Insurance Data", "Map Transaction Data", "Map User Data"])
        if method_2 == "Map Insurance Data":
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2)
            with coll1:
                #Present a slider to select the year within the range of available years in map_insurance
                years = st.slider("Select Year mi", map_insurance["Years"].min(),map_insurance["Years"].max(), map_insurance["Years"].min())
            #Calculate Map_Insurance_Amount_Per_Year with return filter data per year as MIAPY
            MIAPY = Transaction_amount_count_year(map_insurance,years)
            
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2) 
            with coll1:
                #Present a dropdown to select the state within the available states in MIAPY
                state = st.selectbox("Select the State mi", MIAPY["States"].unique())
            #Calculate Map_Insurance_Brand_Per_State   
            Map_Insurance_Per_District(MIAPY,state)
            
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2) 
            with coll1:
                #Present a slider to select the Quater within the range of available quater in a map_insurance
                quater = st.slider("Select the Quater mi", MIAPY["Quater"].min(),MIAPY["Quater"].max(), MIAPY["Quater"].min())
            #Calculate Map_Insurance_Amount_Per_Quater with return filter data per Quater as MIAPQ
            MIAPQ = Transaction_amount_count_quater(MIAPY, quater)
            
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2) 
            with coll1:
                #Present a dropdown to select the state within the available states in filter data in MIAPQ
                state = st.selectbox("Select the State mia", MIAPY["States"].unique())
            #Calculate Map_Insurance_Brand_Per_State   
            Map_Insurance_Per_District(MIAPQ,state)
            
            
        elif method_2 == "Map Transaction Data":
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2)
            with coll1:
                #Present a slider to select the year within the range of available years in map_transaction
                years = st.slider("Select Year mt", map_transaction["Years"].min(),map_transaction["Years"].max(), map_transaction["Years"].min())
            #Calculate Map_Transaction_Amount_Per_Year with return filter data per year as MTAPY
            MTAPY = Transaction_amount_count_year(map_transaction,years)
            
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2) 
            with coll1:
                #Present a dropdown to select the state within the available states in filter data in MIAPY 
                state = st.selectbox("Select the State mt", MTAPY["States"].unique())
            #Calculate Map_Transaction_Brand_Per_State   
            Map_Insurance_Per_District(MTAPY,state)
            
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2) 
            with coll1:
                #Present a slider to select the Quater within the range of available Quaters in MTAPY in filter year
                quater = st.slider("Select the Quater mt", MTAPY["Quater"].min(),MTAPY["Quater"].max(), MTAPY["Quater"].min())
            #Calculate Map_Transaction_Amount_Per_Quater with return filter data per year as MTAPQ
            MTAPQ = Transaction_amount_count_quater(MTAPY, quater)
            
            #Calculate Divide the screen into two columns
            coll1,coll2 =st.columns(2) 
            with coll1:
                #Present a dropdown to select the state within the available states in filter data in MTAPQ
                state = st.selectbox("Select the State mta", MTAPQ["States"].unique())
            #Calculate Map_Transaction_Brand_Per_State   
            Map_Insurance_Per_District(MTAPQ,state)
            
        elif method_2 == "Map User Data":
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2)
            with coll1:
                #Present a slider to select the year within the range of available years in map_user
                years = st.slider("Select Year mt", map_user["Years"].min(),map_user["Years"].max(), map_user["Years"].min())
            #Calculate Map_user_Amount_Per_Year with return filter data per year as MUAPY
            MUAPY = Map_User_Per_Year(map_user,years)
            
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2) 
            with coll1:
                #Present a slider to select the Quater within the range of available Quaterd in MUAPY 
                quater = st.slider("Select the Quater mu", MUAPY["Quater"].min(),MUAPY["Quater"].max(), MUAPY["Quater"].min())
            #Calculate Map_user_Amount_Per_Quater with return filter data per Quater as MUAPQ
            MUAPQ = Map_User_Per_Quater(MUAPY, quater)
            
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2) 
            with coll1:
                #Present a dropdown to select the state within the available states in filter data in MUAPQ
                state = st.selectbox("Select State mu", MUAPQ["States"].unique()) 
            #Calculate Map_User_Amount_Per_state 
            Map_User_Per_State(MUAPQ, state)
            
    with tab3:
        method_3 = st.radio("Select the method" ,["Top Insurance Data", "Top Transaction Data", "Top User Data"])
        if method_3 == "Top Insurance Data":
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2)
            with coll1:
                #Present a slider to select the year within the range of available years in top_insurance
                years = st.slider("Select Year ti", top_insurance["Years"].min(),top_insurance["Years"].max(), top_insurance["Years"].min())
            #Calculate Top_Insurance_Amount_Per_Year with return filter data per year as TIAPY 
            TIAPY = Transaction_amount_count_year(top_insurance,years)
            
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2) 
            with coll1:
                #Present a dropdown to select the state within the available states in filter data in TIAPY
                state = st.selectbox("Select the State ti", TIAPY["States"].unique())
            #Calculate Top_Insurance_Brand_Per_District  
            Top_Insurance_Per_State(TIAPY,state)
            
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2) 
            with coll1:
                #Present a slider to select the Quater within the range of available Quaters in TIAPY
                quater = st.slider("Select the Quater ti", TIAPY["Quater"].min(), TIAPY["Quater"].max(), TIAPY["Quater"].min())
            #Calculate Map_user_Amount_Per_Quater   
            Transaction_amount_count_quater(TIAPY, quater)

        elif method_3 == "Top Transaction Data":
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2)
            with coll1:
                #Present a slider to select the year within the range of available years in top_transaction
                years = st.slider("Select Year ti", top_transaction["Years"].min(),top_transaction["Years"].max(), top_transaction["Years"].min())
            #Calculate Top_Transaction_Amount_Per_Year with return filter data per year as TTAPY
            TTAPY = Transaction_amount_count_year(top_transaction,years)
            
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2) 
            with coll1:
                #Present a dropdown to select the state within the available states in TTAPY
                state = st.selectbox("Select the State ti", TTAPY["States"].unique())
            #Calculate Top_Transaction_Brand_Per_District  
            Top_Insurance_Per_State(TTAPY,state)
            
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2) 
            with coll1:
                #Present a slider to select the Quater within the range of available Quater in top_transaction
                quater = st.slider("Select the Quater ti", TTAPY["Quater"].min(), TTAPY["Quater"].max(), TTAPY["Quater"].min())
            #Calculate Top_Transaction_Amount_Per_Quater   
            Transaction_amount_count_quater(TTAPY, quater)
            
        elif method_3 == "Top User Data":
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2)
            with coll1:
                #Present a slider to select the year within the range of available years in top_user
                years = st.slider("Select Year ti", top_user["Years"].min(),top_user["Years"].max(), top_user["Years"].min())
            #Calculate Top_User_Amount_Per_Year with return filter data per year as TUAPY 
            TUAPY = Top_User_Per_Year(top_user,years)
            
            #Divide the screen into two columns
            coll1,coll2 =st.columns(2) 
            with coll1:
                #Present a dropdown to select the state within the available states in TUAPY
                state = st.selectbox("Select the State ti", TUAPY["States"].unique())
            #Calculate Top_Transaction_Brand_Per_District  
            Top_User_Per_State(TUAPY,state)        

#Query Part        
elif select == 'Top charts':
    #Display content for the "Top charts" selection
    
    #Present a dropdown to select the query type
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
        #Extract relevant data by filter data
        Brand = aggregated_user[["List_of_Brand","Transaction_Count"]]
        #Group the data
        Total_brand = pd.DataFrame(Brand.groupby("List_of_Brand")["Transaction_Count"].sum())
        #Reset the index to ensure continuous index values
        Total_brand.reset_index(inplace= True)
        #Plot a bar chart 
        fig_1 = px.bar(Total_brand, x='List_of_Brand', y='Transaction_Count', color='List_of_Brand',
                    title='Transaction Count per Brand',width=1200, height= 1000,
                    labels={'List_of_Brand': 'Brand', 'Transaction_Count': 'Transaction Count'})
        #Display the plot
        st.plotly_chart(fig_1)

    elif question =="2) State With Highest Transaction Amount":
        #Extract relevant data by filter data
        Trans_Amount = aggregated_transaction[["States","Transaction_Amount"]]
        #Reset the index to ensure continuous index values
        Total_Trans_Amount =pd.DataFrame(Trans_Amount.groupby("States")["Transaction_Amount"].sum().sort_values(ascending = False).head(10).reset_index())
        
        #Plot a pie chart 
        fig_2 = px.pie(Total_Trans_Amount, values= "Transaction_Amount",names="States",
                    title='States With Highest Transaction Amount',
                    labels={'States': 'States', 'Transaction_Amount': 'Transaction Amount'})

        fig_2.update_traces(textposition='inside', textinfo='percent+label') # Display percentage and label inside pie slices
         #Display the plot
        st.plotly_chart(fig_2)

    elif question =="3) Top 10 District With Highest Transaction Amount":
        #Extract relevant data by filter data
        Trans_Amount_District_high = map_transaction[["District_Name","Transaction_Amount"]]
        #Reset the index to ensure continuous index values
        Total_Trans_Amount_District_high =(Trans_Amount_District_high.groupby("District_Name")["Transaction_Amount"].sum().sort_values(ascending = True).head(10).reset_index())

        #Plot a bar chart 
        fig_3 = px.bar(Total_Trans_Amount_District_high, x = "District_Name", y = "Transaction_Amount", color='District_Name',
                    title='District With Highest Transaction Amount',
                    labels={'District_Name': 'District Name', 'Transaction_Amount': 'Transaction Amount'})
         #Display the plot
        st.plotly_chart(fig_3)

    elif question =="4) States With Lowest Transaction Amount":
        #Extract relevant data by filter data
        Trans_Amount = aggregated_transaction[["States","Transaction_Amount"]]
        #Reset the index to ensure continuous index values
        Total_Trans_Amount =pd.DataFrame(Trans_Amount.groupby("States")["Transaction_Amount"].sum().sort_values(ascending=True).head(10).reset_index())

        #Plot a pie chart 
        fig_4 = px.pie(Total_Trans_Amount, values= "Transaction_Amount",names="States",
                    title='States With Lowest Transaction Amount',
                    labels={'States': 'States', 'Transaction_Amount': 'Transaction Amount'})

        fig_4.update_traces(textposition='inside', textinfo='percent+label') # Display percentage and label inside pie slices
        #Display the plot
        st.plotly_chart(fig_4)

    elif question =="5) Top 10 Districts With Lowest Transaction Amount":
        #Extract relevant data by filter data
        No_of_time_apppopen = map_user[["States","No_of_registered_user"]]
        #Reset the index to ensure continuous index values
        Total_No_of_time_apppopen =(No_of_time_apppopen.groupby("States")["No_of_registered_user"].sum().sort_values(ascending = False).head(10).reset_index())

        #Plot a bar chart 
        fig_5 = px.bar(Total_No_of_time_apppopen, x='States', y='No_of_registered_user', color='States',
                    labels={ 'No_of_registered_user': 'No_of_registered_user', 'States': 'States'}, 
                    title='Top 10 Registered Users by State')
        #Display the plot
        st.plotly_chart(fig_5)

    elif question =="6) Top 10 No of Registered User":
        #Extract relevant data by filter data
        No_of_time_apppopen = map_user[["States","No_of_registered_user"]]
        #Reset the index to ensure continuous index values
        Total_No_of_time_apppopen =(No_of_time_apppopen.groupby("States")["No_of_registered_user"].sum().sort_values(ascending = False).head(10).reset_index())

        #Plot a bar chart 
        fig_6 = px.bar(Total_No_of_time_apppopen, x='States', y='No_of_registered_user', color='States',
                    labels={ 'No_of_registered_user': 'No_of_registered_user', 'States': 'States'}, 
                    title='Top 10 Registered Users by State')
        #Display the plot
        st.plotly_chart(fig_6)

    elif question =="7) Top 10 Total_of_Time_App_Open":
        #Extract relevant data by filter data
        No_of_time_apppopen = map_user[["States","Total_of_time_appopen"]]
        #Reset the index to ensure continuous index values
        Total_No_of_time_apppopen = No_of_time_apppopen.groupby("States")["Total_of_time_appopen"].sum().sort_values(ascending = False).head(10).reset_index()

        #Plot a bar chart 
        fig_7 = px.bar(Total_No_of_time_apppopen, x = "States", y = "Total_of_time_appopen",color='States',
                    title='Top 10 States With AppOpens',
                    labels={'States': 'States Name', 'Total_of_time_appopen': 'Total of time appopen'})
        #Display the plot
        st.plotly_chart(fig_7)


    elif question =="8) Transaction Amount Per Type":
        #Extract relevant data by filter data
        Type = aggregated_transaction[["Transaction_Type", "Transaction_Amount"]]
        #Reset the index to ensure continuous index values
        Total_Amount_Type = (Type.groupby("Transaction_Type")["Transaction_Amount"].sum().reset_index())
        
        #Plot a pie chart 
        fig_8 = px.pie(data_frame=Total_Amount_Type, names="Transaction_Type", values= "Transaction_Amount",
                                        width= 600, title=" Total of Transaction Amount",hole= 0.25)
        #Display the plot
        st.plotly_chart(fig_8)

    elif question =="9) Transaction Count Per Type":
        #Extract relevant data by filter data
        Type = aggregated_transaction[["Transaction_Type", "Transaction_Count"]]
        #Reset the index to ensure continuous index values
        Total_Amount_Type = (Type.groupby("Transaction_Type")["Transaction_Count"].sum().reset_index())
        
        #Plot a pie chart 
        fig_9 = px.pie(data_frame=Total_Amount_Type, names="Transaction_Type", values= "Transaction_Count",
                                        width= 600, title=" Total of Transaction Count",hole= 0.25)
        #Display the plot
        st.plotly_chart(fig_9)

    elif question =="10) Top 50 Districts With Lowest Transaction Amount":
        #Extract relevant data by filter data
        List_of_District= map_transaction[["District_Name", "Transaction_Amount"]]
        #Reset the index to ensure continuous index values
        Total_Trans_Amount_District =(List_of_District.groupby("District_Name")["Transaction_Amount"].sum().sort_values(ascending=True).head(50).reset_index())

        #Plot a bar chart 
        fig_10 = px.bar(Total_Trans_Amount_District, x="District_Name", y="Transaction_Amount", title="DISTRICTS WITH 50 LOWEST TRANSACTION AMOUNT")
        #Display the plot
        st.plotly_chart(fig_10)
