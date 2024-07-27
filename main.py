import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Function to connect to Google Sheets
def connect_to_gsheets(json_keyfile_name, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_name, scope)
    client = gspread.authorize(creds)
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
        json_keyfile_name = "key.json"
        sheet_name = "Streamlit-trial"
        
        try:
            sheet = connect_to_gsheets(json_keyfile_name, sheet_name)
            write_to_gsheets(sheet, session_id, question, response)
            st.success("Data written to Google Sheets successfully!")
        except Exception as e:
            st.error(f"Error writing to Google Sheets: {e}")

if __name__ == "__main__":
    main()
