from flask import Blueprint, request, jsonify
from models import Paper, Conference
from models.speaker import Speaker
import pandas as pd

speaker_routes = Blueprint('speaker', __name__)

# Tüm speakerları listele
@speaker_routes.route('/speakers', methods=['GET'])
def get_speakers():
    speakers = Speaker.query.all()
    return jsonify([speaker.to_dict() for speaker in speakers])  # ✅ to_dict() ekledik

# Yeni bir speaker oluştur
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
    new_speaker.save()  # Using the save method from BaseModel
    return jsonify(new_speaker.to_dict()), 201

# ID'ye göre speaker getir
@speaker_routes.route('/speakers/<int:id>', methods=['GET'])
def get_speaker(id):
    speaker = Speaker.query.get(id)
    if speaker and not speaker.IsDeleted:
        return jsonify(speaker.to_dict())
    return jsonify({"message": "Speaker not found"}), 404

# Speaker'ı güncelle
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
        speaker.update()  # Using the update method from BaseModel
        return jsonify(speaker.to_dict())
    return jsonify({"message": "Speaker not found"}), 404

# Speaker'ı sil
@speaker_routes.route('/speakers/<int:id>', methods=['DELETE'])
def delete_speaker(id):
    speaker = Speaker.query.get(id)
    if speaker and not speaker.IsDeleted:
        speaker.delete()  # Using the delete method from BaseModel
        return jsonify({"message": "Speaker deleted successfully"})
    return jsonify({"message": "Speaker not found"}), 404

@speaker_routes.route('/import/speakers', methods=['POST'])
def import_speakers():
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

        row_number = index + 2  # Excel rows start at 1, header is row 1

        if not first_name or not isinstance(first_name, str):
            errors.append(f"Row {row_number}: FirstName is required and must be a string.")
            continue
        if not last_name or not isinstance(last_name, str):
            errors.append(f"Row {row_number}: LastName is required and must be a string.")
            continue
        if not email or not isinstance(email, str):
            errors.append(f"Row {row_number}: Email is required and must be a string.")
            continue

        # Check for duplicate email in DB
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
    # İlgili konferanstaki Paper'ları getir
    papers = Paper.query.filter_by(ConferenceId=conference_id, IsDeleted=False).all()

    # Paper'lardaki SpeakerId'leri al
    speaker_ids = {paper.SpeakerId for paper in papers}

    # Speaker tablolarını al
    speakers = Speaker.query.filter(Speaker.Id.in_(speaker_ids), Speaker.IsDeleted == False).all()

    # JSON olarak döndür
    return jsonify([{
        "Id": s.Id,
        "FirstName": s.FirstName,
        "LastName": s.LastName,
        "Email": s.Email,
        "Bio": s.Bio,
        "PhotoUrl": s.PhotoUrl,
        "Title": next((p.Title for p in papers if p.SpeakerId == s.Id), None)
    } for s in speakers])


@speaker_routes.route("/speakers/<int:speaker_id>/conferences")
def get_speaker_conferences(speaker_id):
    papers = Paper.query.filter_by(SpeakerId=speaker_id, IsDeleted=False).all()
    conferences= []
    for paper in papers:  # paper modelinde ilişki kurulmuş varsayımıyla
            conference = Conference.query.get(paper.ConferenceId)
            conferences.append({
                "conference_title": conference.Title,
                "paper_title": paper.Title,
            })

    return jsonify(conferences)
