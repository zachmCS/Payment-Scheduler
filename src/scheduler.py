import streamlit as st
import pandas as pd


def main():
    st.sidebar.image("./images/index.png")
    st.sidebar.image("./images/outransparent.png")
    st.title("Liquid Thunders Payment Scheduler")


    payments = st.sidebar.selectbox("Select the payment schedule", ["Weekly", "Bi-Weekly", "Monthly", "Bi-Monthly", "Quarterly", "Semi-Annually", "Annually"])
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

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

    # Display the payment schedule with the payment dates and date range
    if num_payments > 0:
        st.write("Payment Schedule: ", payments)
        st.write("Number of Payments: ", num_payments)
        st.write("Date Range: ", start_date, " to ", end_date)
        st.table(pd.DataFrame({"Payment Date": payment_dates}))
    else:
        st.write("No payments in the date range") 


if __name__ == "__main__":
    main()

