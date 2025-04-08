from flask import Blueprint, request, jsonify
from models.hall import Hall
import pandas as pd

hall_routes = Blueprint('hall', __name__)

# Tüm salonları listele
@hall_routes.route('/halls', methods=['GET'])
def get_halls():
    halls = Hall.query.filter_by(IsDeleted=False).all()  # Filter out deleted halls
    return jsonify([hall.to_dict() for hall in halls]), 200

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

# Salonu sil
@hall_routes.route('/halls/<int:id>', methods=['DELETE'])
def delete_hall(id):
    hall = Hall.query.get(id)
    if hall and not hall.IsDeleted:
        hall.delete()  # Using the delete method from BaseModel
        return jsonify({"message": "Hall deleted successfully"})
    return jsonify({"message": "Hall not found"}), 404

@hall_routes.route('/import/halls', methods=['POST'])
def import_halls():
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
        capacity = row.get('Capacity')

        if pd.isna(capacity) or not isinstance(capacity, (int, float)):
            errors.append(f"Row {index + 2}: Capacity is required and must be a number.")
            continue

        hall = Hall(Capacity=int(capacity))
        try:
            hall.save()
            created.append(f"Hall (Capacity: {int(capacity)})")
        except Exception as e:
            errors.append(f"Row {index + 2}: Database error - {str(e)}")

    return jsonify({
        'message': f'{len(created)} halls imported successfully.',
        'created': created,
        'errors': errors
    }), 200
