from flask import Blueprint, request, jsonify
from datetime import datetime
from models.conference import Conference
from app import db

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
