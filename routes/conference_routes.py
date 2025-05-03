from flask import Blueprint, request, jsonify
from datetime import datetime

import config
from models.conference import Conference
import pandas as pd
import schedule_papers

conference_routes = Blueprint('conference', __name__)

# Tüm konferansları listele
@conference_routes.route('/conferences', methods=['GET'])
def get_conferences():
    conferences = Conference.query.filter_by(IsDeleted=False).all()
    return jsonify([conference.to_dict() for conference in conferences]), 200

# Yeni bir konferans oluştur
@conference_routes.route('/conferences', methods=['POST'])
def create_conference():
    data = request.get_json()
    new_conference = Conference(
        Title=data['Title'],
        StartDate=datetime.strptime(data['StartDate'], "%Y-%m-%d"),
        EndDate=datetime.strptime(data['EndDate'], "%Y-%m-%d"),
        Location=data['Location'],
        Organizer=data['Organizer'],
        PhotoUrl=data['PhotoUrl'],
        VideoUrl=data['VideoUrl'],
    )
    new_conference.save()  # Assuming `save()` is defined in your base model
    return jsonify(new_conference.to_dict()), 201

# ID'ye göre konferans getir
@conference_routes.route('/conferences/<int:id>', methods=['GET'])
def get_conference(id):
    conference = Conference.query.get(id)
    if conference and not conference.IsDeleted:
        return jsonify(conference.to_dict())
    return jsonify({"message": "Conference not found"}), 404

# Konferansı güncelle
@conference_routes.route('/conferences/<int:id>', methods=['PUT'])
def update_conference(id):
    conference = Conference.query.get(id)
    if conference and not conference.IsDeleted:
        data = request.get_json()
        conference.Title = data.get('Title', conference.Title)
        conference.StartDate = datetime.strptime(data.get('StartDate', conference.StartDate.strftime("%Y-%m-%d")), "%Y-%m-%d")
        conference.EndDate = datetime.strptime(data.get('EndDate', conference.EndDate.strftime("%Y-%m-%d")), "%Y-%m-%d")
        conference.Location = data.get('Location', conference.Location)
        conference.Organizer = data.get('Organizer', conference.Organizer)
        conference.PhotoUrl = data.get('PhotoUrl', conference.PhotoUrl)
        conference.VideoUrl = data.get('VideoUrl', conference.VideoUrl)

        conference.update()  # Assuming `update()` is defined in your base model
        return jsonify(conference.to_dict())
    return jsonify({"message": "Conference not found"}), 404

# Konferansı sil
@conference_routes.route('/conferences/<int:id>', methods=['DELETE'])
def delete_conference(id):
    conference = Conference.query.get(id)
    if conference and not conference.IsDeleted:
        conference.delete()  # Assuming `delete()` is defined in your base model
        return jsonify({"message": "Conference deleted successfully"})
    return jsonify({"message": "Conference not found"}), 404

@conference_routes.route('/import/conferences', methods=['POST'])
def import_conferences():
    token = request.headers.get('token')
    if not token or token != config.Config.API_SECRET_TOKEN:
        return jsonify({'message': 'Unauthorized'}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        df = pd.read_excel(file)
    except Exception as e:
        return jsonify({'error': f'Invalid Excel file: {str(e)}'}), 400

    errors = []
    created = []

    required_fields = ['Title', 'StartDate', 'EndDate', 'Location', 'Organizer']

    for index, row in df.iterrows():
        missing_fields = [field for field in required_fields if pd.isna(row.get(field))]
        if missing_fields:
            errors.append(f"Row {index + 2}: Missing fields - {', '.join(missing_fields)}")
            continue

        try:
            # Attempt to preprocess the dates
            start_date_str = row['StartDate']
            end_date_str = row['EndDate']

            # Normalize any time with AM/PM to 24-hour format
            def normalize_time(date_str):
                try:
                    # Try to parse the date directly
                    return pd.to_datetime(date_str, errors='raise')
                except Exception:
                    # Handle conversion for cases like '14:00:00 AM'
                    if 'AM' in date_str or 'PM' in date_str:
                        # Strip the AM/PM and convert it to a 24-hour format
                        date_str = date_str.replace('AM', '').replace('PM', '')
                        return pd.to_datetime(date_str, errors='raise')
                    else:
                        return pd.to_datetime(date_str, errors='coerce')

            # Convert StartDate and EndDate
            start_date = normalize_time(start_date_str)
            end_date = normalize_time(end_date_str)

            # If conversion failed, it will be NaT (Not a Time), check for that
            if pd.isna(start_date) or pd.isna(end_date):
                errors.append(f"Row {index + 2}: Invalid date format in StartDate or EndDate")
                continue
        except Exception:
            errors.append(f"Row {index + 2}: Invalid date format in StartDate or EndDate")
            continue

        conference = Conference(
            Title=str(row['Title']).strip(),
            StartDate=start_date,
            EndDate=end_date,
            Location=str(row['Location']).strip(),
            Organizer=str(row['Organizer']).strip(),
            PhotoUrl=str(row['PhotoUrl']).strip(),
            VideoUrl=str(row['VideoUrl']).strip(),
            LogoUrl=str(row['LogoUrl']).strip(),
        )

        try:
            conference.save()
            created.append(conference.Title)
        except Exception as e:
            errors.append(f"Row {index + 2}: Database error - {str(e)}")

    return jsonify({
        'message': f'{len(created)} conferences imported successfully.',
        'created': created,
        'errors': errors
    }), 200

@conference_routes.route('/<int:conference_id>/schedule', methods=['POST'])
def schedule_conference_papers(conference_id):
    token = request.headers.get('token')
    if not token or token != config.Config.API_SECRET_TOKEN:
        return jsonify({'message': 'Unauthorized'}), 401

    try:
        result = schedule_papers.schedule_papers(conference_id)
        return jsonify({"message": "📅 Scheduling completed successfully.", "details": result}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500