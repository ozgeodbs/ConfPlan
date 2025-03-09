from flask import Blueprint, request, jsonify
from models.conference import Conference
from app import db

conference_routes = Blueprint('conference', __name__)

# Tüm konferansları listele
@conference_routes.route('/conferences', methods=['GET'])
def get_conferences():
    conferences = Conference.query.all()
    return jsonify([conference.__repr__() for conference in conferences])

# Yeni bir konferans oluştur
@conference_routes.route('/conferences', methods=['POST'])
def create_conference():
    data = request.get_json()
    new_conference = Conference(
        Title=data['Title'],
        StartDate=data['StartDate'],
        EndDate=data['EndDate'],
        Location=data['Location'],
        Organizer=data['Organizer'],
        CreatedDate=data['CreatedDate'],
        CreatedBy=data['CreatedBy']
    )
    db.session.add(new_conference)
    db.session.commit()
    return jsonify(new_conference.__repr__()), 201

# ID'ye göre konferans getir
@conference_routes.route('/conferences/<int:id>', methods=['GET'])
def get_conference(id):
    conference = Conference.query.get(id)
    if conference:
        return jsonify(conference.__repr__())
    return jsonify({"message": "Conference not found"}), 404

# Konferansı güncelle
@conference_routes.route('/conferences/<int:id>', methods=['PUT'])
def update_conference(id):
    conference = Conference.query.get(id)
    if conference:
        data = request.get_json()
        conference.Title = data.get('Title', conference.Title)
        conference.StartDate = data.get('StartDate', conference.StartDate)
        conference.EndDate = data.get('EndDate', conference.EndDate)
        conference.Location = data.get('Location', conference.Location)
        conference.Organizer = data.get('Organizer', conference.Organizer)
        conference.ChangedDate = data.get('ChangedDate', conference.ChangedDate)
        conference.ChangedBy = data.get('ChangedBy', conference.ChangedBy)

        db.session.commit()
        return jsonify(conference.__repr__())
    return jsonify({"message": "Conference not found"}), 404

# Konferansı sil
@conference_routes.route('/conferences/<int:id>', methods=['DELETE'])
def delete_conference(id):
    conference = Conference.query.get(id)
    if conference:
        db.session.delete(conference)
        db.session.commit()
        return jsonify({"message": "Conference deleted successfully"})
    return jsonify({"message": "Conference not found"}), 404
