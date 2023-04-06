import datetime
from typing import Dict

import holidays
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

import updated_protocols
from updated_protocols import Calendar, BusinessDayRule


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

def payment_calc(payment_dates, bus_protocol: BusinessDayRule, currDate, hday) -> None:

    while currDate in hday or currDate in holidays.WEEKEND:
        if bus_protocol.rules == "Following Business Day":
            currDate = bus_protocol.next_bus_day(turn_to_date_class(currDate))
        elif bus_protocol.rules == "Preceding Business Day":
            currDate = bus_protocol.prev_bus_day(turn_to_date_class(currDate))
        elif bus_protocol.rules == "Modified Following Business Day":
            # we can't pass into the next month
            # if we do, revert to last business day of the previous month
            currDate = bus_protocol.next_bus_day_modded(turn_to_date_class(currDate))
        elif bus_protocol.rules == "Modified Preceding Business Day":
            # we can't pass into the previous month. if we do, revert to first business day of the next month
            currDate = bus_protocol.prev_bus_day_modded(turn_to_date_class(currDate))
        payment_dates.append(currDate)


def main():
    st.sidebar.image("./images/msci.png")
    st.sidebar.image("./images/gcoeou.png")
    st.title("Liquid Thunder's Payment Scheduler")

    end_of_month_rule = False
    payments = st.sidebar.selectbox("Select the payment schedule",
                                    ["Weekly", "Bi-Weekly", "Monthly", "Bi-Monthly", "Quarterly", "Semi-Annually",
                                     "Annually"])
    ##desired action is to send response to protocols.py file and have it configure the correct frequency internally
    holiday_select = st.sidebar.selectbox("Select the holiday calendar",
                                          ["New York Stock Exchange", "European Central Bank"])
    hday = holiday_selection(holiday_select)

    ##desired action is to send response to protocols.py file and have it pull up the correct holiday calendar internally
    rules = st.sidebar.selectbox("Select the payment rule",
                                 ["Following Business Day", "Preceding Business Day", "Modified Following Business Day",
                                  "Modified Preceding Business Day"])
    ##desired action is to send response to protocols.py file and have it configure the correct payment rule internally

    if payments == "Monthly" or payments == "Bi-Monthly":
        end_of_month_rule = st.sidebar.checkbox("End of Month Rule",
                                                value=False)  ## needs to appear more (quarterly,etc)
    # desired action is to send response to protocols.py file and have it configure the correct end of month rule
    # internally
    start_date = st.date_input("Start Date")
    ##desired action is to send response to protocols.py file and have it configure the correct start date internally
    end_date = st.date_input("End Date", min_value=start_date, value=start_date)

    ##desired action is to send response to protocols.py file and have it configure the correct end date internally

    start_date_class = turn_to_date_class(start_date)
    end_date_class = turn_to_date_class(end_date)

    day: datetime.date
    hday_class: Dict
    for day, idx in hday:
        hday_class[idx] = turn_to_date_class(day)

    bus_protocol: BusinessDayRule = updated_protocols.BusinessDayRule(start_date_class, end_date_class,
                                                                      rules, hday_class, payments, end_of_month_rule)
    cal: Calendar = updated_protocols.Calendar(holidays.WEEKEND, hday_class)


    # SEND TO PROTOCOL FOR COMPUTATION
    payment_dates = []
    if payments == "Weekly":
        num_payments = (end_date - start_date).days // 7
        for i in range(num_payments):
            currDate = start_date + pd.DateOffset(weeks=(i + 1))
            payment_calc(payment_dates, bus_protocol, currDate, hday)

    elif payments == "Bi-Weekly":
        num_payments = (end_date - start_date).days // 14
        for i in range(num_payments):
            currDate = start_date + pd.DateOffset(weeks=(i + 1) * 2)
            payment_calc(payment_dates, bus_protocol, currDate, hday)

    elif payments == "Monthly":  ##END OF MONTH RULE NEEDS TO BE IMPLEMENTED
        num_payments = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        for i in range(num_payments):
            currDate = start_date + pd.DateOffset(months=i + 1)
            payment_calc(payment_dates, bus_protocol, currDate, hday)

    elif payments == "Bi-Monthly":  ##END OF MONTH RULE NEEDS TO BE IMPLEMENTED
        num_payments = (end_date.year - start_date.year) * 6 + (end_date.month - start_date.month) // 2
        for i in range(num_payments):
            currDate = start_date + pd.DateOffset(months=(i + 1) * 2)
            payment_calc(payment_dates, bus_protocol, currDate, hday)

    elif payments == "Quarterly":
        num_payments = (end_date.year - start_date.year) * 4 + (end_date.month - start_date.month) // 3
        for i in range(num_payments):
            currDate = start_date + pd.DateOffset(months=(i + 1) * 3)
            payment_calc(payment_dates, bus_protocol, currDate, hday)

    elif payments == "Semi-Annually":
        num_payments = (end_date.year - start_date.year) * 2 + (end_date.month - start_date.month) // 6
        for i in range(num_payments):
            currDate = start_date + pd.DateOffset(months=(i + 1) * 6)
            payment_calc(payment_dates, bus_protocol, currDate, hday)

    elif payments == "Annually":
        num_payments = end_date.year - start_date.year
        for i in range(num_payments):
            currDate = start_date + pd.DateOffset(years=(i + 1))
            payment_calc(payment_dates, bus_protocol, currDate, hday)

    # convert payment_dates to dataframe with month, day, and year columns
    payment_dates = pd.DataFrame({"Month": [date.strftime('%B') for date in payment_dates],
                                  "Day": [date.day for date in payment_dates],
                                  "Year": [date.year for date in payment_dates]})


    # Display the payment schedule with the payment dates and date range
    if num_payments > 0:
        st.write("Payment Schedule: ", payments)
        st.write("Number of Payments: ", num_payments)
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
