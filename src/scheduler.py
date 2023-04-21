import datetime
from typing import Dict

import holidays
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from st_aggrid import AgGrid


import updated_protocols
from updated_protocols import *


def ColourWidgetText(wgt_txt, wch_colour = '#000000'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('*'), i;
                    for (i = 0; i < elements.length; ++i) { if (elements[i].innerText == |wgt_txt|) 
                        elements[i].style.color = ' """ + wch_colour + """ '; } </script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + wgt_txt + "'")
    components.html(f"{htmlstr}", height=0, width=0)

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
    payments = st.sidebar.selectbox(
        "Payment Schedule 🔁",
        [
            "Weekly",
            "Bi-Weekly",
            "Monthly",
            "Bi-Monthly",
            "Quarterly",
            "Semi-Annually",
            "Annually",
            "Custom",
        ],
        help='Select the payment schedule. Default is "Weekly".',
    )

    if payments == "Custom":
        # Map each custom payment to the max frequency
        frequency_mappings = {
            "Day(s)": 365,
            "Week(s)": 52,
            "Month(s)": 12,
            "Year(s)": 50,
        }
        cols = st.sidebar.columns(2)

        custom_payments = cols[1].selectbox(
            "Unit of Time",
            [
                "Day(s)",
                "Week(s)",
                "Month(s)",
                "Year(s)",
            ],
            help="Select the unit of time for the custom payment range.",
        )
        custom_frequency = cols[0].number_input(
            "Value",
            min_value=1,  # 1 day, 1 week, 1 month, etc, 1 is the shortest frequency
            max_value=frequency_mappings[custom_payments],
            value=1,
            help="Enter the frequency of the custom payment schedule.",
        )
    else:
        custom_payments = None
        custom_frequency = None

        

    holiday_select = st.sidebar.selectbox(
        "Holiday Calendar (🇺🇸, 🇪🇺, 🇨🇳, 🇧🇷, 🇦🇺, 🇳🇬)",
        [
            "New York Stock Exchange",
            "European Central Bank",
            "China",
            "Brazil",
            "Australia",
            "Nigeria",
        ],
        help='Select the holiday calendar. Default is "New York Stock Exchange"',
    )

    rules = st.sidebar.selectbox(  # TODO no adjustment is purely calculating the date without any rules
        "Payment Rule",
        [
            "No Adjustment",
            "Following Business Day",
            "Preceding Business Day",
            "Modified Following Business Day",
            "Modified Preceding Business Day",
        ],
        help='Select the payment rule. Default is "No Adjustment".',
    )

    if payments != "Weekly" or payments != "Bi-Weekly":
        end_of_month_rule = st.sidebar.checkbox("End of Month Rule", value=False)

        # Max frequency for each is the amount of times it happens before the next frequency
        # For example, Days min value is 1 and max value is 365
        # Weeks min value is 1 and max value is 52
        # Months min value is 1 and max value is 12
        # Years min value is 1 and max value is 50

    start_date = st.date_input("Start Date 📅")
    end_date = st.date_input("End Date 📅", min_value=start_date, value=start_date)

    bus_protocol: BusinessDayRule = updated_protocols.BusinessDayRule(
        turn_to_date_class(start_date),
        turn_to_date_class(end_date),
        payments,
        rules,
        holiday_selection(holiday_select),
        end_of_month_rule,
        custom_val=custom_frequency,
        custom_freq=custom_payments
    )
    cal: Calendar = updated_protocols.Calendar(
        holidays.WEEKEND, holiday_selection(holiday_select)
    )

    # SEND TO PROTOCOL FOR COMPUTATION
    payment_dates = []
    payment_dates = bus_protocol.calc_payment_dates(turn_to_date_class(start_date))

    # convert payment_dates to dataframe with month, day, and year columns
    payment_dates = pd.DataFrame(
        {
            "Month": [date.strftime("%B") for date in payment_dates],
            "Day": [date.day for date in payment_dates],
            "Year": [date.year for date in payment_dates],
        }
    )

    # Display the payment schedule with the payment dates and date range
    cols = st.columns(3)
    if len(payment_dates) > 0:
        with cols[0]:
            st.write("Number of Payments: ")
            st.metric(label="Number of Payments: ", value=len(payment_dates), label_visibility="collapsed") 
            ColourWidgetText(str(len(payment_dates)), '#00B050')

        with cols[1]:
            st.write("Start Date: ")
            st.metric(label="Start Date: ", value=start_date.strftime("%m-%d-%Y"), label_visibility="collapsed")
            ColourWidgetText(start_date.strftime("%m-%d-%Y"), '#00B050')

        with cols[2]:
            st.write("End Date: ")
            st.metric(label="End Date: ", value=end_date.strftime("%m-%d-%Y"), label_visibility="collapsed")
            ColourWidgetText(end_date.strftime("%m-%d-%Y"), '#00B050')
        # with cols[3]:
        #     st.write("Frequency: ")
        #     st.metric(label="Frequency: ", value=custom_frequency if custom_payments else payments, label_visibility="collapsed")
        AgGrid(payment_dates, fit_columns_on_grid_load=True)

        # Convert month to number
        payment_dates["Month"] = payment_dates["Month"].apply(
            lambda x: datetime.datetime.strptime(x, "%B").month
        )
        # Calculate file_name from start_date and end_date
        file_name = f"payments_{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}.csv"

        # Download button
        st.download_button(
            label="Download data as CSV",
            data=payment_dates.to_csv(index=False),
            file_name=file_name,
            mime="text/csv",
        )
    else:
        st.write("No payments in the date range")



if __name__ == "__main__":
    main()
