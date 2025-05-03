import zipfile
import os
from flask import send_file, jsonify
import pandas as pd
from io import BytesIO

def generate_individual_excel(table_name, columns):
    """Helper function to create an Excel file for a given table"""
    df = pd.DataFrame(columns=columns)
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=table_name, index=False)
    buffer.seek(0)
    return buffer

def generate_excel():
    # Table columns for each table
    category_columns = ['Title']
    conference_columns = ['Title', 'StartDate', 'EndDate', 'Location', 'Organizer', 'PhotoUrl', 'VideoUrl','LogoUrl']
    hall_columns = ['Title','ConferenceId','Capacity']
    speaker_columns = ['FirstName', 'LastName', 'Bio', 'Email', 'Phone', 'PhotoUrl']
    paper_columns = ['Title', 'ConferenceId', 'SpeakerId', 'CategoryId', 'Duration', 'Description', 'HallId']

    try:
        # Generate buffers for each table
        category_buffer = generate_individual_excel('Categories', category_columns)
        conference_buffer = generate_individual_excel('Conferences', conference_columns)
        hall_buffer = generate_individual_excel('Halls', hall_columns)
        speaker_buffer = generate_individual_excel('Speakers', speaker_columns)
        paper_buffer = generate_individual_excel('Papers', paper_columns)

        # Create a temporary folder to store files
        temp_folder = "temp_excel_files"
        os.makedirs(temp_folder, exist_ok=True)

        # Save the files temporarily to the temp folder
        category_filename = os.path.join(temp_folder, "Categories.xlsx")
        conference_filename = os.path.join(temp_folder, "Conferences.xlsx")
        hall_filename = os.path.join(temp_folder, "Halls.xlsx")
        speaker_filename = os.path.join(temp_folder, "Speakers.xlsx")
        paper_filename = os.path.join(temp_folder, "Papers.xlsx")

        category_buffer.seek(0)
        with open(category_filename, 'wb') as f:
            f.write(category_buffer.read())

        conference_buffer.seek(0)
        with open(conference_filename, 'wb') as f:
            f.write(conference_buffer.read())

        hall_buffer.seek(0)
        with open(hall_filename, 'wb') as f:
            f.write(hall_buffer.read())

        speaker_buffer.seek(0)
        with open(speaker_filename, 'wb') as f:
            f.write(speaker_buffer.read())

        paper_buffer.seek(0)
        with open(paper_filename, 'wb') as f:
            f.write(paper_buffer.read())

        # Now, zip the files
        zip_filename = "excel_templates.zip"
        zip_filepath = os.path.join(temp_folder, zip_filename)

        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            zipf.write(category_filename, "Categories.xlsx")
            zipf.write(conference_filename, "Conferences.xlsx")
            zipf.write(hall_filename, "Halls.xlsx")
            zipf.write(speaker_filename, "Speakers.xlsx")
            zipf.write(paper_filename, "Papers.xlsx")

        # Send the zip file
        return send_file(zip_filepath, as_attachment=True, download_name=zip_filename, mimetype="application/zip")

    except Exception as e:
        print(f"Error generating Excel files: {e}")
        return jsonify({'error': 'An error occurred while generating the Excel file'}), 500
