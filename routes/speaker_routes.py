from flask import Blueprint, request, jsonify
from datetime import datetime
from models.speaker import Speaker
from app import db

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

# 📌 Belirli bir konferans ve konuşmacıya ait bildirileri getir
@speaker_routes.route('/<int:conference_id>/speaker/<int:speaker_id>', methods=['GET'])
def get_conference_speaker(conference_id, speaker_id):
    speaker = Speaker.query.get(speaker_id)
    if speaker and not speaker.IsDeleted:
        speaker.delete()  # Using the delete method from BaseModel
        return jsonify({"message": "Speaker deleted successfully"})
    return jsonify({"message": "Speaker not found"}), 404
