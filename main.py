import streamlit as st
import gspread
from google.oauth2 import service_account

# Function to connect to Google Sheets
def connect_to_gsheets(sheet_name):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )
    client = gspread.authorize(credentials)
    sheet = client.open(sheet_name).sheet1
    return sheet

    
# Function to write data to Google Sheets
def write_to_gsheets(sheet, session_id, question, response):
    sheet.append_row([session_id, question, response])

# Streamlit interface
def main():
    st.title("Streamlit to Google Sheets")

    # Input fields
    session_id = st.text_input("Session ID")
    question = st.text_input("Question")
    response = st.text_input("Response")

    # Button to submit data
    if st.button("Submit"):
        sheet_name = "Streamlit-trial"
        
        try:
            sheet = connect_to_gsheets(sheet_name)
            write_to_gsheets(sheet, session_id, question, response)
            st.success("Data written to Google Sheets successfully!")
        except Exception as e:
            st.error(f"Error writing to Google Sheets: {e}")

if __name__ == "__main__":
    main()
