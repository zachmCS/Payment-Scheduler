import streamlit as st
from st_aggrid import AgGrid
import pandas as pd

def main():
    st.sidebar.image("./images/msci.png")
    st.sidebar.image("./images/gcoeou.png")
    st.title("Liquid Thunders Payment Scheduler")


    payments = st.sidebar.selectbox("Select the payment schedule", ["Weekly", "Bi-Weekly", "Monthly", "Bi-Monthly", "Quarterly", "Semi-Annually", "Annually"])
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date", min_value=start_date, value=start_date)

    # Computer the number of payments and dates of payments based on the payment schedule
    if payments == "Weekly":
        num_payments = (end_date - start_date).days // 7
        payment_dates = [start_date + pd.DateOffset(weeks=i) for i in range(num_payments)]
    elif payments == "Bi-Weekly":
        num_payments = (end_date - start_date).days // 14
        payment_dates = [start_date + pd.DateOffset(weeks=i*2) for i in range(num_payments)]
    elif payments == "Monthly":
        num_payments = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        payment_dates = [start_date + pd.DateOffset(months=i) for i in range(num_payments)]
    elif payments == "Bi-Monthly":
        num_payments = (end_date.year - start_date.year) * 6 + (end_date.month - start_date.month) // 2
        payment_dates = [start_date + pd.DateOffset(months=i*2) for i in range(num_payments)]
    elif payments == "Quarterly":
        num_payments = (end_date.year - start_date.year) * 4 + (end_date.month - start_date.month) // 3
        payment_dates = [start_date + pd.DateOffset(months=i*3) for i in range(num_payments)]
    elif payments == "Semi-Annually":
        num_payments = (end_date.year - start_date.year) * 2 + (end_date.month - start_date.month) // 6
        payment_dates = [start_date + pd.DateOffset(months=i*6) for i in range(num_payments)]
    elif payments == "Annually":
        num_payments = end_date.year - start_date.year
        payment_dates = [start_date + pd.DateOffset(years=i) for i in range(num_payments)]

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

    # Button to download the dataframe as a csv file
    if st.button("Download Payment Schedule"):
        payment_dates.to_csv("payment_schedule.csv", index=False)
        st.write("Downloaded payment schedule as csv file")

if __name__ == "__main__":
    main()
