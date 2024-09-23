import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import locale
import math
from streamlit import session_state
from streamlit_extras.app_logo import add_logo
from streamlit_extras.stylable_container import stylable_container 

st.set_page_config(initial_sidebar_state="auto", page_title="Cost Budget Calculator", page_icon="👋", layout="centered", menu_items=None)
with st.sidebar:
    st.image("logo.png")
    st.write("""
                 
         **Cost Budget Calculator 1.0**
         
         Cost Budget Application 1.0
                 
        

            """
         )
# Define a function to check if the user is being limited by search volume
def is_limited_by_search_volume(budget, cpc, ctr, searches):
    # Calculate the number of clicks the budget can afford
    clicks_affordable = budget / cpc
    
    # Calculate the expected clicks based on CTR and monthly searches
    expected_clicks = ctr * searches
    
    # Check if affordable clicks exceed the available clicks based on search volume
    if clicks_affordable > expected_clicks:
        return True  # User is limited by search volume
    else:
        return False  # User is not limited by search volume

def limited_by_low(budget,cpc, searches):
    ctr= 0.02
    clicks_affordable = budget / cpc
    
    # Calculate the expected clicks based on CTR and monthly searches
    expected_clicks = ctr * searches
    limiting_searches = clicks_affordable / ctr
    return limiting_searches

def limited_by_high(budget,cpc, searches):
    ctr= 0.09
    clicks_affordable = budget / cpc
    
    # Calculate the expected clicks based on CTR and monthly searches
    expected_clicks = ctr * searches
    limiting_searches = clicks_affordable / ctr
    return limiting_searches

def high_intent(upper_cpc, upper_monthly_budget, upper_monthly_searches):
    ctr = 0.09  # 9% CTR
    conversion_rate = 0.05  # 5% conversion rate
    
    # Calculate clicks based on CTR and monthly searches
    potential_clicks = upper_monthly_searches * ctr
    
    # Calculate the number of clicks affordable based on the budget and CPC
    clicks_affordable = upper_monthly_budget / upper_cpc
    
    # Use the minimum of clicks affordable and potential clicks
    actual_clicks = min(clicks_affordable, potential_clicks)
    
    # Calculate conversions
    conversions = actual_clicks * conversion_rate
    cost_per_conversion = upper_monthly_budget / conversions
    limit = is_limited_by_search_volume(upper_monthly_budget, upper_cpc, ctr, upper_monthly_searches)
    return conversions, cost_per_conversion,limit
    
def low_intent( cpc,monthly_budget, monthly_searches):
    ctr = 0.05  # 9% CTR
    conversion_rate = 0.02  # 5% conversion rate
   # Calculate clicks based on CTR and monthly searches
    potential_clicks = monthly_budget * ctr
    
    # Calculate the number of clicks affordable based on the budget and CPC
    clicks_affordable = monthly_budget / cpc
    
    # Use the minimum of clicks affordable and potential clicks
    actual_clicks = min(clicks_affordable, potential_clicks)
    
    # Calculate conversions
    conversions = actual_clicks * conversion_rate
    cost_per_conversion = monthly_budget / conversions
    limit = is_limited_by_search_volume(monthly_budget, cpc, ctr, monthly_searches)
    
    return conversions, cost_per_conversion , limit
    
def df_on_change(cpc_month_df):
    state = st.session_state["df_editor"]
    for index, updates in state["edited_rows"].items():
        st.session_state["cpc_month_df"].loc[st.session_state["cpc_month_df"].index == index, "Complete"] = True
        for key, value in updates.items():
            st.session_state["cpc_month_df"].loc[st.session_state["cpc_month_df"].index == index, key] = value
            
def df_on_change_upper(upper_cpc_month_df):
    upper_state = st.session_state["df_editor_upper"]
    for index, updates in upper_state ["edited_rows"].items():
        st.session_state["upper_cpc_month_df"].loc[st.session_state["upper_cpc_month_df"].index == index, "Complete"] = True
        for key, value in updates.items():
            st.session_state["upper_cpc_month_df"].loc[st.session_state["upper_cpc_month_df"].index == index, key] = value

def cost_budget_editor():
    if "cpc_month_df" not in st.session_state:
        st.session_state["cpc_month_df"] = cpc_month_df
    if "upper_cpc_month_df" not in st.session_state:
        st.session_state["upper_cpc_month_df"] = upper_cpc_month_df
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Low Intent Keywords")
        st.data_editor(st.session_state["cpc_month_df"], key="df_editor", on_change=df_on_change, args=[cpc_month_df],
            column_config={
                "Type": st.column_config.Column(
                    disabled=True
                )
            },
            disabled=["Complete"],
            use_container_width=True,
            hide_index=True
        )
    with col2:
        st.subheader("High Intent Keywords")
        st.data_editor(st.session_state["upper_cpc_month_df"], key="df_editor_upper", on_change=df_on_change_upper, args=[upper_cpc_month_df],
            column_config={
                "Type": st.column_config.Column(
                    disabled=True
                )
            },
            disabled=["Complete"],
            use_container_width=True,
            hide_index=True
        )
    
st.title("Cost Per Click To Budget Calculator")

cta_missing=["no"]

    
with stylable_container(
    key="cpc_monthly_budget",
    css_styles="""
        {
            margin: auto;
            width: 50%;
        }
    """,
):
    st.subheader("CPC & Monthly Budget")
    st.write("Please enter monthly budget and cost per click")
rows = st.columns(2)

cpc_month_df = pd.DataFrame(
{
    "Type": ["Cost Per Click","Monthly Budget","Monthly Searches"],
    "Num": [0.001, 0.001,10000],
}
)

upper_cpc_month_df = pd.DataFrame(
{
    "Type": ["Cost Per Click","Monthly Budget","Monthly Searches"],
    "Num": [0.001, 0.001,10000],
}
)

#lower value keyword calculation
cost_budget_editor()

#lower value intent  keyword calculation
cpc_month__edited_df = st.session_state["cpc_month_df"]
low_cpc = cpc_month__edited_df['Num'].iloc[0]
low_month_cost = cpc_month__edited_df['Num'].iloc[1]
low_monthly_searches = cpc_month__edited_df['Num'].iloc[2]
low_conversion_cpc = low_intent(low_cpc,low_month_cost, low_monthly_searches)
#is_limited_by_search_volume(budget, cpc, ctr, searches):
  

rounded_cpc= round(low_cpc,3)
rounded_month_cost = round(low_month_cost,3)
rounded_conversions_cpc_0 = round(low_conversion_cpc[0],2)
rounded_conversions_cpc_1 = round(low_conversion_cpc[1],2)

#upper value intent  keyword calculation
upper_cpc_month__edited_df = st.session_state["upper_cpc_month_df"]
upper_cpc = upper_cpc_month__edited_df['Num'].iloc[0]
upper_month_cost = upper_cpc_month__edited_df['Num'].iloc[1]
upper_monthly_searches = upper_cpc_month__edited_df['Num'].iloc[2]
upper_conversion_cpc = high_intent(upper_cpc, upper_month_cost , upper_monthly_searches)

upper_limit = upper_conversion_cpc[2]

upper_rounded_cpc= round(upper_cpc,3)
upper_rounded_month_cost = round(upper_month_cost,3)
upper_rounded_conversions_cpc_0 = round(upper_conversion_cpc[0],2)
upper_rounded_conversions_cpc_1 = round(upper_conversion_cpc[1],2)



col1,col2 = st.columns(2)
with col1:
    st.subheader("Lower Intent Keywords")
   
    if rounded_conversions_cpc_0 >= 1:
        st.info(f"With a cost per click of  £{rounded_cpc} and a monthly budget of £{rounded_month_cost}  You are expected to receive {rounded_conversions_cpc_0} conversions with a cost per conversion of £{rounded_conversions_cpc_1}")
        if low_conversion_cpc[2] == True:
            search_limit = round(limited_by_low(low_month_cost, low_cpc, low_monthly_searches),2)
            st.info(f"You are being limited by the search volume for this keyword to increase conversions you would need more than {search_limit} searches ")
            with st.expander(":information_source:"):
                 st.markdown("""

                 The cost per conversion increases when you raise your budget because you are paying more without gaining additional conversions.

                """)
    else:
        st.warning(f"With a cost per click of  £{rounded_cpc} and a monthly budget of £{rounded_month_cost}  You are expected to receive 0 conversions. You will need to increase your budget")
        
with col2:
    st.subheader("High Intent Keywords")

    if upper_rounded_conversions_cpc_0 >= 1:
        st.info(f"With a cost per click of  £{upper_rounded_cpc}  and a monthly budget of £{upper_rounded_month_cost}  You are expected to receive {upper_rounded_conversions_cpc_0} conversions with a cost per conversion of £{upper_rounded_conversions_cpc_1}")
        if upper_conversion_cpc[2] == True:
            search_limit = round(limited_by_high(upper_month_cost, upper_cpc, upper_monthly_searches),2)
            st.info(f"You are being limited by the search volume for this keyword to increase conversions you would need more than {search_limit} searches ")
            with st.expander(":information_source:"):
                 st.markdown("""

                 The cost per conversion increases when you raise your budget because you are paying more without gaining additional conversions.

                """)
    else:
        st.warning(f"With a cost per click of  £{upper_rounded_cpc} and a monthly budget of £{upper_rounded_month_cost}  You are expected to receive 0 conversions. You will need to increase your budget")
if cta_missing[0] =="yes":
    st.warning("You have CTAS missing to see the cpc and conversions you could be receiving select no")
