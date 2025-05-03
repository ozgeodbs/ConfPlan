from flask import Blueprint, request, jsonify

import config
from models.hall import Hall
import pandas as pd
import requests

hall_routes = Blueprint('hall', __name__)


# Tüm salonları listele
@hall_routes.route('/halls', methods=['GET'])
def get_halls():
    halls = Hall.query.filter_by(IsDeleted=False).all()  # Filter out deleted halls
    return jsonify([hall.to_dict() for hall in halls]), 200


@hall_routes.route('/<int:conference_id>/halls', methods=['GET'])
def get_conference_halls(conference_id):
    halls = Hall.query.filter_by(ConferenceId=conference_id, IsDeleted=False).all()
    if halls:
        return jsonify([hall.to_dict() for hall in halls]), 200
    return jsonify({"message": "No hall found for this conference"}), 404


# Yeni bir salon oluştur
@hall_routes.route('/halls', methods=['POST'])
def create_hall():
    data = request.get_json()
    new_hall = Hall(
        Capacity=data['Capacity']
    )
    new_hall.save()  # Using the save method from BaseModel
    return jsonify(new_hall.to_dict()), 201


# ID'ye göre salon getir
@hall_routes.route('/halls/<int:id>', methods=['GET'])
def get_hall(id):
    hall = Hall.query.get(id)
    if hall and not hall.IsDeleted:
        return jsonify(hall.to_dict())
    return jsonify({"message": "Hall not found"}), 404


# Salonu güncelle
@hall_routes.route('/halls/<int:id>', methods=['PUT'])
def update_hall(id):
    hall = Hall.query.get(id)
    if hall and not hall.IsDeleted:
        data = request.get_json()
        hall.Capacity = data.get('Capacity', hall.Capacity)
        hall.update()  # Using the update method from BaseModel
        return jsonify(hall.to_dict())
    return jsonify({"message": "Hall not found"}), 404


@hall_routes.route('/halls/<int:id>', methods=['DELETE'])
def delete_hall(id):
    hall = Hall.query.get(id)
    if hall and not hall.IsDeleted:
        hall.delete()  # Using the delete method from BaseModel
        return jsonify({"message": "Hall deleted successfully"})
    return jsonify({"message": "Hall not found"}), 404


@hall_routes.route('/import/halls', methods=['POST'])
def import_halls():
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
        row_number = index + 2

        capacity = row.get('Capacity')

        if pd.isna(capacity) or not isinstance(capacity, (int, float)):
            errors.append(f"Row {row_number}: Capacity is required and must be a number.")
            continue


        conference_id = row.get('ConferenceId')

        conference_response = requests.get(f"{config.Config.BASE_URL}/conferences/{conference_id}")
        if conference_response.status_code != 200:
            errors.append(f"Row {row_number}: Conference with ID {conference_id} not found or deleted.")
            continue

        hall = Hall(
            Capacity=int(capacity),
            ConferenceId=conference_id,
            Title = str(row['Title']).strip()
        )

        try:
            hall.save()
            created.append(f"Hall (Capacity: {int(capacity)})")
        except Exception as e:
            errors.append(f"Row {row_number}: Database error - {str(e)}")

    return jsonify({
        'message': f'{len(created)} halls imported successfully.',
        'created': created,
        'errors': errors
    }), 200
