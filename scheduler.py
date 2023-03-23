import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
import holidays

def main():
    st.sidebar.image("./images/msci.png")
    st.sidebar.image("./images/gcoeou.png")
    st.title("Liquid Thunder's Payment Scheduler")

    end_of_month_rule = False
    payments = st.sidebar.selectbox("Select the payment schedule", ["Weekly", "Bi-Weekly", "Monthly", "Bi-Monthly", "Quarterly", "Semi-Annually", "Annually"])
    ##desired action is to send response to protocols.py file and have it configure the correct frequency internally
    holiday_select = st.sidebar.selectbox("Select the holiday calendar", ["New York Stock Exchange", "European Central Bank"])
    if(holiday_select == "New York Stock Exchange"):
        hday = holidays.NYSE()
    elif(holiday_select == "European Central Bank"):
        hday = holidays.ECB()
    ##desired action is to send response to protocols.py file and have it pull up the correct holiday calendar internally
    rules = st.sidebar.selectbox("Select the payment rule", ["Following Business Day", "Preceding Business Day", "Modified Following Business Day", "Modified Preceding Business Day"])
    ##desired action is to send response to protocols.py file and have it configure the correct payment rule internally
    if(payments == "Monthly" or payments == "Bi-Monthly"):
        end_of_month_rule = st.sidebar.checkbox("End of Month Rule", value=True)
        ##desired action is to send response to protocols.py file and have it configure the correct end of month rule internally
    start_date = st.date_input("Start Date")
    ##desired action is to send response to protocols.py file and have it configure the correct start date internally
    end_date = st.date_input("End Date", min_value=start_date, value=start_date)
    ##desired action is to send response to protocols.py file and have it configure the correct end date internally

    # SEND TO PROTOCOL FOR COMPUTATION
    payment_dates = []
    if payments == "Weekly":
        num_payments = (end_date - start_date).days // 7
        for i in range(num_payments):
            currDate = start_date + pd.DateOffset(weeks=(i+1))
            while(currDate) in hday or currDate in holidays.WEEKEND:
                if(rules == "Following Business Day"):
                    currDate = currDate + pd.DateOffset(days=1)
                elif(rules == "Preceding Business Day"):
                    currDate = currDate - pd.DateOffset(days=1)
                elif(rules == "Modified Following Business Day"):
                    ##we cant pass into the next month. if we do, revert to last business day of the previous month
                    if(currDate.month != (currDate + pd.DateOffset(days=1)).month):
                        currDate = currDate - pd.DateOffset(days=1)
                    else:
                        currDate = currDate + pd.DateOffset(days=1)
                elif(rules == "Modified Preceding Business Day"):
                    ##we cant pass into the previous month. if we do, revert to first business day of the next month
                    if(currDate.month != (currDate - pd.DateOffset(days=1)).month):
                        currDate = currDate + pd.DateOffset(days=1)
                    else:
                        currDate = currDate - pd.DateOffset(days=1)
            payment_dates.append(currDate)

    elif payments == "Bi-Weekly":
        num_payments = (end_date - start_date).days // 14
        for i in range(num_payments):
            currDate = start_date + pd.DateOffset(weeks=(i+1)*2)
            while(currDate) in hday or currDate in holidays.WEEKEND:
                if(rules == "Following Business Day"):
                    currDate = currDate + pd.DateOffset(days=1)
                elif(rules == "Preceding Business Day"):
                    currDate = currDate - pd.DateOffset(days=1)
                elif(rules == "Modified Following Business Day"):
                    ##we cant pass into the next month. if we do, revert to last business day of the previous month
                    if(currDate.month != (currDate + pd.DateOffset(days=1)).month):
                        currDate = currDate - pd.DateOffset(days=1)
                    else:
                        currDate = currDate + pd.DateOffset(days=1)
                elif(rules == "Modified Preceding Business Day"):
                    ##we cant pass into the previous month. if we do, revert to first business day of the next month
                    if(currDate.month != (currDate - pd.DateOffset(days=1)).month):
                        currDate = currDate + pd.DateOffset(days=1)
                    else:
                        currDate = currDate - pd.DateOffset(days=1)
            payment_dates.append(currDate)

    elif payments == "Monthly": ##END OF MONTH RULE NEEDS TO BE IMPLEMENTED
        num_payments = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        for i in range(num_payments):
            currDate = start_date + pd.DateOffset(months=i+1)
            while(currDate) in hday or currDate in holidays.WEEKEND:
                if(rules == "Following Business Day"):
                    currDate = currDate + pd.DateOffset(days=1)
                elif(rules == "Preceding Business Day"):
                    currDate = currDate - pd.DateOffset(days=1)
                elif(rules == "Modified Following Business Day"):
                    ##we cant pass into the next month. if we do, revert to last business day of the previous month
                    if(currDate.month != (currDate + pd.DateOffset(days=1)).month):
                        currDate = currDate - pd.DateOffset(days=1)
                    else:
                        currDate = currDate + pd.DateOffset(days=1)
                elif(rules == "Modified Preceding Business Day"):
                    ##we cant pass into the previous month. if we do, revert to first business day of the next month
                    if(currDate.month != (currDate - pd.DateOffset(days=1)).month):
                        currDate = currDate + pd.DateOffset(days=1)
                    else:
                        currDate = currDate - pd.DateOffset(days=1)
            payment_dates.append(currDate)

    elif payments == "Bi-Monthly": ##END OF MONTH RULE NEEDS TO BE IMPLEMENTED
        num_payments = (end_date.year - start_date.year) * 6 + (end_date.month - start_date.month) // 2
        for i in range(num_payments):
            currDate = start_date + pd.DateOffset(months=(i+1)*2)
            while(currDate) in hday or currDate in holidays.WEEKEND:
                if(rules == "Following Business Day"):
                    currDate = currDate + pd.DateOffset(days=1)
                elif(rules == "Preceding Business Day"):
                    currDate = currDate - pd.DateOffset(days=1)
                elif(rules == "Modified Following Business Day"):
                    ##we cant pass into the next month. if we do, revert to last business day of the previous month
                    if(currDate.month != (currDate + pd.DateOffset(days=1)).month):
                        currDate = currDate - pd.DateOffset(days=1)
                    else:
                        currDate = currDate + pd.DateOffset(days=1)
                elif(rules == "Modified Preceding Business Day"):
                    ##we cant pass into the previous month. if we do, revert to first business day of the next month
                    if(currDate.month != (currDate - pd.DateOffset(days=1)).month):
                        currDate = currDate + pd.DateOffset(days=1)
                    else:
                        currDate = currDate - pd.DateOffset(days=1)
            payment_dates.append(currDate)


    elif payments == "Quarterly":
        num_payments = (end_date.year - start_date.year) * 4 + (end_date.month - start_date.month) // 3
        for i in range(num_payments):
            currDate = start_date + pd.DateOffset(months=(i+1)*3)
            while(currDate) in hday or currDate in holidays.WEEKEND:
                if(rules == "Following Business Day"):
                    currDate = currDate + pd.DateOffset(days=1)
                elif(rules == "Preceding Business Day"):
                    currDate = currDate - pd.DateOffset(days=1)
                elif(rules == "Modified Following Business Day"):
                    ##we cant pass into the next month. if we do, revert to last business day of the previous month
                    if(currDate.month != (currDate + pd.DateOffset(days=1)).month):
                        currDate = currDate - pd.DateOffset(days=1)
                    else:
                        currDate = currDate + pd.DateOffset(days=1)
                elif(rules == "Modified Preceding Business Day"):
                    ##we cant pass into the previous month. if we do, revert to first business day of the next month
                    if(currDate.month != (currDate - pd.DateOffset(days=1)).month):
                        currDate = currDate + pd.DateOffset(days=1)
                    else:
                        currDate = currDate - pd.DateOffset(days=1)
            payment_dates.append(currDate)

    elif payments == "Semi-Annually":
        num_payments = (end_date.year - start_date.year) * 2 + (end_date.month - start_date.month) // 6
        for i in range(num_payments):
            currDate = start_date + pd.DateOffset(months=(i+1)*6)
            while(currDate) in hday or currDate in holidays.WEEKEND:
                if(rules == "Following Business Day"):
                    currDate = currDate + pd.DateOffset(days=1)
                elif(rules == "Preceding Business Day"):
                    currDate = currDate - pd.DateOffset(days=1)
                elif(rules == "Modified Following Business Day"):
                    ##we cant pass into the next month. if we do, revert to last business day of the previous month
                    if(currDate.month != (currDate + pd.DateOffset(days=1)).month):
                        currDate = currDate - pd.DateOffset(days=1)
                    else:
                        currDate = currDate + pd.DateOffset(days=1)
                elif(rules == "Modified Preceding Business Day"):
                    ##we cant pass into the previous month. if we do, revert to first business day of the next month
                    if(currDate.month != (currDate - pd.DateOffset(days=1)).month):
                        currDate = currDate + pd.DateOffset(days=1)
                    else:
                        currDate = currDate - pd.DateOffset(days=1)
            payment_dates.append(currDate)

    elif payments == "Annually":
        num_payments = end_date.year - start_date.year
        for i in range(num_payments):
            currDate = start_date + pd.DateOffset(years=(i+1))
            while(currDate) in hday or currDate in holidays.WEEKEND:
                if(rules == "Following Business Day"):
                    currDate = currDate + pd.DateOffset(days=1)
                elif(rules == "Preceding Business Day"):
                    currDate = currDate - pd.DateOffset(days=1)
                elif(rules == "Modified Following Business Day"):
                    ##we cant pass into the next month. if we do, revert to last business day of the previous month
                    if(currDate.month != (currDate + pd.DateOffset(days=1)).month):
                        currDate = currDate - pd.DateOffset(days=1)
                    else:
                        currDate = currDate + pd.DateOffset(days=1)
                elif(rules == "Modified Preceding Business Day"):
                    ##we cant pass into the previous month. if we do, revert to first business day of the next month
                    if(currDate.month != (currDate - pd.DateOffset(days=1)).month):
                        currDate = currDate + pd.DateOffset(days=1)
                    else:
                        currDate = currDate - pd.DateOffset(days=1)
            payment_dates.append(currDate)

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

