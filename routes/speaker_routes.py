from flask import Blueprint, request, jsonify
from models.speaker import Speaker
from app import db

speaker_routes = Blueprint('speaker', __name__)

# Tüm speakerları listele
@speaker_routes.route('/speakers', methods=['GET'])
def get_speakers():
    speakers = Speaker.query.all()
    return jsonify([speaker.__repr__() for speaker in speakers])

# Yeni bir speaker oluştur
@speaker_routes.route('/speakers', methods=['POST'])
def create_speaker():
    data = request.get_json()
    new_speaker = Speaker(
        FirstName=data['FirstName'],
        LastName=data['LastName'],
        Bio=data['Bio'],
        Email=data['Email'],
        Phone=data['Phone'],
        PhotoUrl=data['PhotoUrl'],
        CreatedDate=data['CreatedDate'],
        CreatedBy=data['CreatedBy']
    )
    db.session.add(new_speaker)
    db.session.commit()
    return jsonify(new_speaker.__repr__()), 201

# ID'ye göre speaker getir
@speaker_routes.route('/speakers/<int:id>', methods=['GET'])
def get_speaker(id):
    speaker = Speaker.query.get(id)
    if speaker:
        return jsonify(speaker.__repr__())
    return jsonify({"message": "Speaker not found"}), 404

# Speaker'ı güncelle
@speaker_routes.route('/speakers/<int:id>', methods=['PUT'])
def update_speaker(id):
    speaker = Speaker.query.get(id)
    if speaker:
        data = request.get_json()
        speaker.FirstName = data.get('FirstName', speaker.FirstName)
        speaker.LastName = data.get('LastName', speaker.LastName)
        speaker.Bio = data.get('Bio', speaker.Bio)
        speaker.Email = data.get('Email', speaker.Email)
        speaker.Phone = data.get('Phone', speaker.Phone)
        speaker.PhotoUrl = data.get('PhotoUrl', speaker.PhotoUrl)
        speaker.ChangedDate = data.get('ChangedDate', speaker.ChangedDate)
        speaker.ChangedBy = data.get('ChangedBy', speaker.ChangedBy)

        db.session.commit()
        return jsonify(speaker.__repr__())
    return jsonify({"message": "Speaker not found"}), 404

# Speaker'ı sil
@speaker_routes.route('/speakers/<int:id>', methods=['DELETE'])
def delete_speaker(id):
    speaker = Speaker.query.get(id)
    if speaker:
        db.session.delete(speaker)
        db.session.commit()
        return jsonify({"message": "Speaker deleted successfully"})
    return jsonify({"message": "Speaker not found"}), 404
