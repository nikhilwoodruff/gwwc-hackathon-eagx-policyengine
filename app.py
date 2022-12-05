from policyengine_us import Simulation
import streamlit as st

# This is an app which tells people how much money they'd need to donate to lower their net income (after taxes and benefits) by x%.

# First, the title, subtitle and introduction.

st.title("How much should I donate to charity?")
st.subheader("A tool to help you decide how much to donate to charity")

st.write("This tool will tell you how much you should donate to charity to lower your net income by a certain amount. It's based on the [PolicyEngine](https://policyengine.org) project, which is an open-source tool for exploring the effects of tax and benefit policies.")

# Now, we ask the user for their income and the amount they want to lower it by.

income = st.number_input("What is your annual income?", min_value=0, max_value=1000000, value=50000, step=1000)

# Give people the option of inputting a percent or absolute amount to lower their net income by.

lower_by = st.selectbox("Lower my net income by", ["a percentage", "an absolute amount"])

if lower_by == "a percentage":
    lower_by_amount = st.number_input("Lower my net income by what percentage?", min_value=0, max_value=100, value=10, step=1)
    lower_by_amount = income * lower_by_amount / 100
else:
    lower_by_amount = st.number_input("Lower my net income by what amount?", min_value=0, max_value=1000000, value=10000, step=1000)

simulation = Simulation(
    situation=dict(
        people=dict(
            person=dict(
                employment_income={2022: income},
            ),
        ),
        tax_units=dict(
            tax_unit=dict(
                premium_tax_credit={2022: 0},
                members=["person"],
            )
        ),
        axes=[[
            dict(
                name="charitable_cash_donations",
                min=0,
                max=lower_by_amount * 2,
                count=101,
            )
        ]]
    ),
)

net_income_by_donation = simulation.calculate("household_net_income")
donations = simulation.calculate("charitable_cash_donations")

import plotly.express as px

fig = px.line(
    x=donations,
    y=net_income_by_donation - donations,
).update_layout(
    title="Net income after taxes, benefits and donations",
    xaxis_title="Donation amount",
    yaxis_title="Net income",
    yaxis_tickformat="$,.0f",
    xaxis_tickformat="$,.0f",
)

st.write(fig)

