import datetime
from typing import Dict

import holidays
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

import updated_protocols
from updated_protocols import *



def turn_to_date_class(date_input) -> updated_protocols.Date:
    return updated_protocols.Date(date_input.day, date_input.month, date_input.year)


def holiday_selection(selected: str) -> Dict:
    if selected == "New York Stock Exchange":
        holiday = holidays.NYSE()
    elif selected == "European Central Bank":
        holiday = holidays.ECB()
    elif selected == "China":
        holiday = holidays.CN()
    elif selected == "Brazil":
        holiday = holidays.BR()
    elif selected == "Australia":
        holiday = holidays.AUS()
    elif selected == "Nigeria":
        holiday = holidays.NG()
    return holiday

def main():
    st.sidebar.image("./images/msci.png")
    st.sidebar.image("./images/gcoeou.png")
    st.title("Liquid Thunder's Payment Scheduler")

    end_of_month_rule = False
    payments = st.sidebar.selectbox("Select the payment schedule",
                                    ["Weekly", "Bi-Weekly", "Monthly", "Bi-Monthly", "Quarterly", "Semi-Annually",
                                     "Annually"])
    holiday_select = st.sidebar.selectbox("Select the holiday calendar",
                                          ["New York Stock Exchange", "European Central Bank", "China", "Brazil","Australia","Nigeria"])

    rules = st.sidebar.selectbox("Select the payment rule",
                                 ["Following Business Day", "Preceding Business Day", "Modified Following Business Day",
                                  "Modified Preceding Business Day"])

    if payments != "Weekly" or payments != "Bi-Weekly":
        end_of_month_rule = st.sidebar.checkbox("End of Month Rule",
                                                value=False)  
        
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date", min_value=start_date, value=start_date)

    bus_protocol: BusinessDayRule = updated_protocols.BusinessDayRule(turn_to_date_class(start_date), turn_to_date_class(end_date),
                                                                      payments, rules,holiday_selection(holiday_select), end_of_month_rule)
    cal: Calendar = updated_protocols.Calendar(holidays.WEEKEND, holiday_selection(holiday_select))


    # SEND TO PROTOCOL FOR COMPUTATION
    payment_dates = []
    payment_dates = bus_protocol.next_bus_day(turn_to_date_class(start_date))

    # convert payment_dates to dataframe with month, day, and year columns
    payment_dates = pd.DataFrame({"Month": [date.strftime('%B') for date in payment_dates],
                                  "Day": [date.day for date in payment_dates],
                                  "Year": [date.year for date in payment_dates]})


    # Display the payment schedule with the payment dates and date range
    if len(payment_dates) > 0:
        st.write("Payment Schedule: ", payments)
        st.write("Number of Payments: ", len(payment_dates))
        st.write("Date Range: ", start_date, " to ", end_date)
        AgGrid(payment_dates, fit_columns_on_grid_load=True)
    else:
        st.write("No payments in the date range")

        # Button to download the dataframe as a csv file    payment_dates.append(currDate)
    if st.button("Download Payment Schedule"):
        payment_dates.to_csv("payment_schedule.csv", index=False)
        st.write("Downloaded payment schedule as csv file")


if __name__ == "__main__":
    main()
