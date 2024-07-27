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

# Function to write data to Google Sheets with a separator
def write_to_gsheets(sheet, session_id, question, response, separator=" | "):
    existing_data = sheet.get_all_values()
    
    # Check if session_id already exists
    session_ids = [row[0] for row in existing_data]
    if session_id in session_ids:
        # Find the row index for the session_id
        row_index = session_ids.index(session_id) + 1  # gspread is 1-indexed
        # Append the question and response in the same row with a separator
        new_question = sheet.cell(row_index, 2).value + separator + question
        new_response = sheet.cell(row_index, 3).value + separator + response
        sheet.update_cell(row_index, 2, new_question)
        sheet.update_cell(row_index, 3, new_response)
    else:
        # Add a new row with session_id, question, and response
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
        sheet_name = "Streamlit-trial"  # Replace with your Google Sheet name
        
        try:
            sheet = connect_to_gsheets(sheet_name)
            write_to_gsheets(sheet, session_id, question, response)
            st.success("Data written to Google Sheets successfully!")
        except Exception as e:
            st.error(f"Error writing to Google Sheets: {e}")

if __name__ == "__main__":
    main()
