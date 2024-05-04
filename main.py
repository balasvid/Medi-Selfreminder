import streamlit as st
import pandas as pd
import os

# Title of the app
st.title('Medi-Selfreminder💊')
st.sidebar.title("Medicine information")

# Define the radio button options
DaysOptions = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
TimeOptions = ['Morning','Noon','Evening','Night']

# User inputs
medicine_name = st.sidebar.text_input('Enter the name of the medicine')
dosage_amount = st.sidebar.text_input('Enter the dosage')
selected_DaysOption = st.sidebar.selectbox('Select a day:', DaysOptions)
selected_TimeOption = st.sidebar.selectbox('Select a time:', TimeOptions)       

# Button to add medicine to the list
if st.sidebar.button('Add medicine to list'):
    if medicine_name and dosage_amount and selected_DaysOption and selected_TimeOption:
        new_entry = {'Name': medicine_name, 'Dosage': dosage_amount, 'Day': selected_DaysOption, 'Time': selected_TimeOption}
        st.session_state.data.append(new_entry)
        # Save the updated data to a CSV file
        pd.DataFrame(st.session_state.data).to_csv('medication_data.csv', index=False)
    else:
        st.error('Please fill in all the fields!')

def init_dataframe():
    """Initialize or load the dataframe."""
    if 'data' not in st.session_state:
        # Check if file exists
        if os.path.exists('medication_data.csv'):
            # Check if file is not empty
            if os.path.getsize('medication_data.csv') > 0:
                try:
                    filesize = pd.read_csv('medication_data.csv')
                    if not filesize.empty:
                        # Load the data from the CSV file
                        st.session_state.data = pd.read_csv('medication_data.csv').to_dict('records')
                except pd.errors.EmptyDataError:
                    st.session_state.data = []
            else:
                st.session_state.data = []
        else:
            st.session_state.data = []

def display_medication():
    """Display the medication DataFrame in the app."""
    if st.session_state.data:
        # Convert the data to a DataFrame
        df = pd.DataFrame(st.session_state.data)

        # Display column headers
        cols = st.columns([1, 1, 1, 1, 1])  # Add an extra column for the delete button
        cols[0].subheader('Name')
        cols[1].subheader('Dosage')
        cols[2].subheader('Day')
        cols[3].subheader('Time')
        cols[4].subheader('Action')  # Header for the delete button column

        # Iterate over the DataFrame and display each row with a delete button
        for i in df.index:
            row_data = df.loc[i]
            cols = st.columns([1, 1, 1, 1, 1])  # Add an extra column for the delete button
            cols[0].text(row_data['Name'])
            cols[1].text(row_data['Dosage'])
            cols[2].text(row_data['Day'])
            cols[3].text(row_data['Time'])
            if cols[4].button('Delete', key=str(i)):
                # Delete the row from the data
                del st.session_state.data[i]

                # Save the updated data to a CSV file
                pd.DataFrame(st.session_state.data).to_csv('medication_data.csv', index=False)
                # Refresh the page after deleting a row to update the table
                st.rerun()

    else:
        st.write("No medication data to display.")

def main():
    init_dataframe()
    display_medication()

if __name__ == "__main__":
    main()
