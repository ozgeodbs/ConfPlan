from flask import Blueprint, request, jsonify

import config
from models import Paper, Conference
from models.speaker import Speaker
import pandas as pd

speaker_routes = Blueprint('speaker', __name__)

@speaker_routes.route('/speakers', methods=['GET'])
def get_speakers():
    speakers = Speaker.query.all()
    return jsonify([speaker.to_dict() for speaker in speakers])

@speaker_routes.route('/speakers', methods=['POST'])
def create_speaker():
    data = request.get_json()

    new_speaker = Speaker(
        FirstName=data['FirstName'],
        LastName=data['LastName'],
        Bio=data.get('Bio', ''),
        Email=data['Email'],
        Phone=data.get('Phone', ''),
        PhotoUrl=data.get('PhotoUrl', '')
    )
    new_speaker.save()
    return jsonify(new_speaker.to_dict()), 201

@speaker_routes.route('/speakers/<int:id>', methods=['GET'])
def get_speaker(id):
    speaker = Speaker.query.get(id)
    if speaker and not speaker.IsDeleted:
        return jsonify(speaker.to_dict())
    return jsonify({"message": "Speaker not found"}), 404

@speaker_routes.route('/speakers/<int:id>', methods=['PUT'])
def update_speaker(id):
    speaker = Speaker.query.get(id)
    if speaker and not speaker.IsDeleted:
        data = request.get_json()
        speaker.FirstName = data.get('FirstName', speaker.FirstName)
        speaker.LastName = data.get('LastName', speaker.LastName)
        speaker.Bio = data.get('Bio', speaker.Bio)
        speaker.Email = data.get('Email', speaker.Email)
        speaker.Phone = data.get('Phone', speaker.Phone)
        speaker.PhotoUrl = data.get('PhotoUrl', speaker.PhotoUrl)
        speaker.update()
        return jsonify(speaker.to_dict())
    return jsonify({"message": "Speaker not found"}), 404

@speaker_routes.route('/speakers/<int:id>', methods=['DELETE'])
def delete_speaker(id):
    speaker = Speaker.query.get(id)
    if speaker and not speaker.IsDeleted:
        speaker.delete()
        return jsonify({"message": "Speaker deleted successfully"})
    return jsonify({"message": "Speaker not found"}), 404

@speaker_routes.route('/import/speakers', methods=['POST'])
def import_speakers():
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

    for index, row in df.iterrows():
        first_name = row.get('FirstName')
        last_name = row.get('LastName')
        email = row.get('Email')
        bio = row.get('Bio')
        phone = row.get('Phone')
        photo_url = row.get('PhotoUrl')

        row_number = index + 2

        if not first_name or not isinstance(first_name, str):
            errors.append(f"Row {row_number}: FirstName is required and must be a string.")
            continue
        if not last_name or not isinstance(last_name, str):
            errors.append(f"Row {row_number}: LastName is required and must be a string.")
            continue
        if not email or not isinstance(email, str):
            errors.append(f"Row {row_number}: Email is required and must be a string.")
            continue

        existing = Speaker.query.filter_by(Email=email).first()
        if existing:
            errors.append(f"Row {row_number}: Email '{email}' already exists.")
            continue

        speaker = Speaker(
            FirstName=first_name.strip(),
            LastName=last_name.strip(),
            Email=email.strip(),
            Bio=bio.strip() if isinstance(bio, str) else None,
            Phone=phone.strip() if isinstance(phone, str) else None,
            PhotoUrl=photo_url.strip() if isinstance(photo_url, str) else None
        )

        try:
            speaker.save()
            created.append(email)
        except Exception as e:
            errors.append(f"Row {row_number}: Database error - {str(e)}")

    return jsonify({
        'message': f'{len(created)} speakers imported successfully.',
        'created': created,
        'errors': errors
    }), 200

@speaker_routes.route('/<int:conference_id>/speakers/get/all')
def get_speakers_by_conference(conference_id):

    papers = Paper.query.filter_by(ConferenceId=conference_id, IsDeleted=False).all()

    speaker_ids = {paper.SpeakerId for paper in papers}

    speakers = Speaker.query.filter(Speaker.Id.in_(speaker_ids), Speaker.IsDeleted == False).all()
    speaker_map = {s.Id: s for s in speakers}

    return jsonify([
        {
            "PaperId": paper.Id,
            "Title": paper.Title,
            "StartTime": paper.StartTime.isoformat() if paper.StartTime else None,
            "EndTime": paper.EndTime.isoformat() if paper.EndTime else None,
            "HallId": paper.HallId,
            "Speaker": {
                "Id": speaker.Id,
                "FirstName": speaker.FirstName,
                "LastName": speaker.LastName,
                "PhotoUrl": speaker.PhotoUrl,
            } if (speaker := speaker_map.get(paper.SpeakerId)) else None
        }
        for paper in papers
    ])


@speaker_routes.route("/speakers/<int:speaker_id>/conferences")
def get_speaker_conferences(speaker_id):
    papers = Paper.query.filter_by(SpeakerId=speaker_id, IsDeleted=False).all()
    conferences= []
    for paper in papers:
            conference = Conference.query.get(paper.ConferenceId)
            conferences.append({
                "conference_title": conference.Title,
                "paper_title": paper.Title,
            })

    return jsonify(conferences)
