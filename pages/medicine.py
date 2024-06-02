import streamlit as st
import pandas as pd
import datetime
from menu import menu_with_redirect
from db import open_db_connection
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

# Set the page configuration
st.set_page_config(page_title="Medi-Selfreminder", page_icon="💊", layout="centered")

# Show the navigation menu
menu_with_redirect()

if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

if 'edit_data' not in st.session_state:
    st.session_state.edit_data = None

if 'hide_pdf_download_button' not in st.session_state or st.session_state.hide_pdf_download_button is False:
    st.session_state.hide_pdf_download_button = True

def edit_medication(username, medication_name, dosage, day, time):
    edited_medication_name = st.text_input('Edit the name of the medicine', value=medication_name, key='edit_med_name')
    edited_dosage_amount = st.text_input('Edit the dosage', value=dosage, key='edit_dosage')
    edited_selected_DaysOption = st.selectbox('Edit the day:', DaysOptions, index=DaysOptions.index(day), key='edit_day')
    edited_selected_TimeOption = st.selectbox('Edit the time:', TimeOptions, index=TimeOptions.index(time), key='edit_time')

    # Button to update medication entry
    if st.button('Update medication', key='update_medication'):
        if edited_medication_name and edited_dosage_amount and edited_selected_DaysOption and edited_selected_TimeOption:
            with open_db_connection() as conn:
                c = conn.cursor()
                c.execute('UPDATE medication SET name=?, dosage=?, day=?, time=? WHERE username=? AND name=? AND dosage=? AND day=? AND time=?', 
                            (edited_medication_name, edited_dosage_amount, edited_selected_DaysOption, edited_selected_TimeOption,
                            username, medication_name, dosage, day, time))
                conn.commit()
            st.success('Medication entry updated successfully.')
            st.session_state.edit_mode = False  # Turn off edit mode
            st.rerun()
        else:
            st.warning('Please fill in all the fields.')

def display_medication(username):

        #Display the medication DataFrame in the app
        with open_db_connection() as conn:
            c = conn.cursor()
            c.execute('SELECT name, dosage, day, time FROM medication WHERE username = ?', (username,))
            data = c.fetchall()
            if data:
                # Convert the data to a DataFrame
                df = pd.DataFrame(data, columns=['Name', 'Dosage', 'Day', 'Time'])
    
                # Display column headers
                cols = st.columns([1, 1, 1, 1, 2])  # Add an extra column for the edit and delete buttons
                cols[0].subheader('Name')
                cols[1].subheader('Dosage')
                cols[2].subheader('Day')
                cols[3].subheader('Time')
                cols[4].subheader('Actions')  # Header for the edit and delete buttons

                # Iterate over the DataFrame and display each row with a delete button
                for i in df.index:
                    row_data = df.loc[i]
                    cols = st.columns([1, 1, 1, 1, 2])  # Add an extra column for the edit and delete buttons
                    cols[0].text(row_data['Name'])
                    cols[1].text(row_data['Dosage'])
                    cols[2].text(row_data['Day'])
                    cols[3].text(row_data['Time'])

                    action_col = cols[4]
                    edit_button, delete_button = action_col.columns([1, 1])

                    if edit_button.button('Edit', key=f'edit_{i}'):
                        st.session_state.edit_mode = True  # Turn on edit mode
                        st.session_state.edit_data = {
                            'username': username,
                            'medication_name': row_data['Name'],
                            'dosage': row_data['Dosage'],
                            'day': row_data['Day'],
                            'time': row_data['Time']
                        }
                        st.rerun()
                    
                    if delete_button.button('Delete', key=f'delete_{i}'):
                        # Delete the row from the database
                        with open_db_connection() as conn:
                            c = conn.cursor()
                            c.execute('DELETE FROM medication WHERE username = ? AND name = ? AND dosage = ? AND day = ? AND time = ?', 
                                    (username, row_data['Name'], row_data['Dosage'], row_data['Day'], row_data['Time']))
                            conn.commit()
                        # Refresh the page after deleting a row to update the table
                        st.rerun()
                    
                    if not st.session_state.initial_notification:
                        # Check if the day matches the current day
                        current_day = datetime.datetime.now().strftime('%A')
                        if row_data['Day'] == current_day:
                            if row_data['Time'] == "Morning" or row_data['Time'] == "Evening":
                                st.toast(f"Don't forget to take {row_data['Dosage']} of {row_data['Name']} in the {row_data['Time']}")
                                st.info(f"Don't forget to take {row_data['Dosage']} of {row_data['Name']} in the {row_data['Time']}")
                            else:
                                st.toast(f"Don't forget to take {row_data['Dosage']} of {row_data['Name']} at {row_data['Time']}")
                                st.info(f"Don't forget to take {row_data['Dosage']} of {row_data['Name']} at {row_data['Time']}")
                
                st.session_state.initial_notification = True

                # Add some vertical space between the table and the buttons
                st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)

                # Function to generate PDF using reportlab
                def generate_pdf(df):
                    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                    c = canvas.Canvas(pdf_file.name, pagesize=letter)
                    width, height = letter

                    c.drawString(30, height - 40, "Medication Data")
                    c.drawString(30, height - 60, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                    # Draw table header
                    x_offset = 30
                    y_offset = height - 80
                    c.drawString(x_offset, y_offset, "Name")
                    c.drawString(x_offset + 100, y_offset, "Dosage")
                    c.drawString(x_offset + 200, y_offset, "Day")
                    c.drawString(x_offset + 300, y_offset, "Time")

                    # Draw table rows
                    for i, row in df.iterrows():
                        y_offset -= 20
                        c.drawString(x_offset, y_offset, str(row_data['Name']))
                        c.drawString(x_offset + 100, y_offset, str(row_data['Dosage']))
                        c.drawString(x_offset + 200, y_offset, str(row_data['Day']))
                        c.drawString(x_offset + 300, y_offset, str(row_data['Time']))

                    c.save()
                    return pdf_file.name


                # Add download buttons side by side
                col1, col2, col3 = st.columns(3)
                with col1:
                    # Add a download button for the DataFrame as CSV
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download table as CSV",
                        data=csv,
                        file_name='medication_data.csv',
                        mime='text/csv',
                    )

                # Add a generate PDF button for the table
                with col2:
                    if st.button("Generate PDF"):
                        pdf_file = generate_pdf(df)
                        st.session_state.pdf_file = pdf_file
                        st.session_state.hide_pdf_download_button = False

                # Add a download button for the table as PDF
                with col3:
                    if st.session_state.hide_pdf_download_button == False:
                        if 'pdf_file' in st.session_state:
                            with open(st.session_state.pdf_file, "rb") as f:
                                st.download_button(
                                    label="Download table as PDF",
                                    data=f,
                                    file_name='medication_data.pdf',
                                    mime='application/pdf'
                                )

            else:
                st.write("No medication data to display.")
                image_path = "images/tablets_pills_capsules.jpg"
                st.image(image_path, use_column_width=True)

st.title("🧾 Medicine")
st.header("Medication list")
st.write("Here you can view, add, edit or delete your medication list.")

# Define the radio button options
DaysOptions = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
TimeOptions = ['Morning','Noon','Evening','Night']

# User inputs - 2x2 layout for the fields
col1, col2 = st.columns(2)

with col1:
    medicine_name = st.text_input('Enter the name of the medicine', key='med_name')

with col2:
    dosage_amount = st.text_input('Enter the dosage', key='dosage')

col3, col4 = st.columns(2)

with col3:
    selected_DaysOption = st.selectbox('Select a day:', DaysOptions)

with col4:
    selected_TimeOption = st.selectbox('Select a time:', TimeOptions)

# Button to add medicine to the list
if st.button('Add medicine to list', key='add_medicine'):
    if medicine_name and dosage_amount and selected_DaysOption and selected_TimeOption:
        with open_db_connection() as conn:    
            c = conn.cursor()
            c.execute('INSERT INTO medication(username, name, dosage, day, time) VALUES (?,?,?,?,?)', 
                        (st.session_state.username, medicine_name, dosage_amount, selected_DaysOption, selected_TimeOption))
            conn.commit()
        st.success('Medicine added to the list!')
        #st.rerun()
    else:
        st.warning('Please fill in all the fields!')


if st.session_state.username:
    if st.session_state.edit_mode:
        edit_medication(
            st.session_state.edit_data['username'],
            st.session_state.edit_data['medication_name'],
            st.session_state.edit_data['dosage'],
            st.session_state.edit_data['day'],
            st.session_state.edit_data['time']
        )
    else:
        display_medication(st.session_state.username)
