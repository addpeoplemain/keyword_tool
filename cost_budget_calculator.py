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

def spend_per_conversion_with_condition(cpc, monthly_budget, monthly_searches, cta_missing):
    # Constant Conversion Rate
    ctr = 0.05  # 5% Click-Through Rate
    conversion_rate = 0.02  # 2% Conversion Rate
    #yes_no_count = 1

    # Calculate the number of clicks that can be afforded based on the monthly budget and CPC
    clicks_affordable = monthly_budget / cpc
    
    # Calculate the number of clicks generated from the budget (assuming every dollar spent gives a click)
    clicks = min(clicks_affordable, monthly_searches * ctr)
    
    # Calculate the number of conversions (leads)
    conversions = clicks * conversion_rate
    additional_cost_no_cta = 0
    total_budget = monthly_budget
    # Count occurrences of 'no' in cta_list
   
    if cta_missing[0]=="yes":
        # If 'no' was found, reduce total conversions by 25% for each 'no'
        conversions = conversions * (1 - 0.25)  # Reduce conversions by 25% for each 'no'
        additional_cost_no_cta = monthly_budget * (0.25)  # 25% additional cost if ctas missing 
        
        #total_budget = monthly_budget + additional_cost
    else:
        # If no 'no' in the list, keep the conversions and budget as is
        total_budget = monthly_budget
    
    if conversions == 0:
        return float('inf'), 0  # Return infinity for cost per conversion if no leads, and 0 for leads
    
    # Calculate the spend per conversion (cost per lead)
    cost_per_conversion = (total_budget / conversions)+additional_cost_no_cta

#    st.write("DEBUG MENU")
 #   st.write("Total Budget =")
 #   st.write(total_budget)
 #   st.write("conversions =")
 #   st.write(conversions)
 #   st.write("cost per conversion")
 #   st.write(cost_per_conversion)
  
    return conversions, cost_per_conversion


def df_on_change(cpc_month_df):
    state = st.session_state["df_editor"]
    for index, updates in state["edited_rows"].items():
        st.session_state["cpc_month_df"].loc[st.session_state["cpc_month_df"].index == index, "Complete"] = True
        for key, value in updates.items():
            st.session_state["cpc_month_df"].loc[st.session_state["cpc_month_df"].index == index, key] = value

def cost_budget_editor():
    if "cpc_month_df" not in st.session_state:
        st.session_state["cpc_month_df"] = cpc_month_df
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
    
st.title("Cost Per Click To Budget Calculator")

cta_missing=[]

st.subheader("CTA Selector")
st.write("Are Any CTAS missing from the landing page ?")
cta_check = st.radio(
    "If any CTAs are missing please click yes",
    ["Yes","No"],
    captions=[
        "Missing a CTA",
        "No missing CTAs",
    ],
    index = 1,
)

if cta_check =="No":
    cta_missing.append("no")
else:
    cta_missing.append("yes")

if cta_missing[0] =="yes":
    st.warning("You have CTAS missing from your webpage you can improve your conversion rate. To see your possible conversion with no missing ctas select no")
    

st.subheader("CPC & Monthly Budget")
st.write("Please enter monthly budget and cost per click")
rows = st.columns(2)

cpc_month_df = pd.DataFrame(
{
    "Type": ["Cost Per Click","Monthly Budget","Monthly Searches"],
    "Num": [1.50, 1.50,10],
}
)
lower_month_df = pd.DataFrame(
{
    "Type": ["Lower Cost Per Click","Monthly Budget","Monthly Searches"],
    "Num": [1.50, 1.50,10],
}
)

cost_budget_editor()


cpc_month__edited_df = st.session_state["cpc_month_df"]
cpc = cpc_month__edited_df['Num'].iloc[0]
month_cost = cpc_month__edited_df['Num'].iloc[1]
monthly_searches = cpc_month__edited_df['Num'].iloc[2]


conversion_cpc = spend_per_conversion_with_condition(cpc, month_cost,monthly_searches, cta_missing)
rounded_cpc= round(cpc,3)
rounded_month_cost = round(month_cost,3)
rounded_conversions_cpc_0 = round(conversion_cpc[0],2)
rounded_conversions_cpc_1 = round(conversion_cpc[1],2)

st.info(f"With a cost per click of  £{rounded_cpc} and a monthly budget of £{rounded_month_cost}  You are expected to receive {rounded_conversions_cpc_0} conversions with a cost per conversion of £{rounded_conversions_cpc_1}")

if cta_missing[0] =="yes":
    st.warning("You have CTAS missing to see the cpc and conversions you could be receiving select no")
