from flask import Blueprint, request, jsonify
from models.hall import Hall
from app import db

hall_routes = Blueprint('hall', __name__)

# Tüm salonları listele
@hall_routes.route('/halls', methods=['GET'])
def get_halls():
    halls = Hall.query.all()
    return jsonify([hall.__repr__() for hall in halls])

# Yeni bir salon oluştur
@hall_routes.route('/halls', methods=['POST'])
def create_hall():
    data = request.get_json()
    new_hall = Hall(
        Capacity=data['Capacity'],
        CreatedDate=data['CreatedDate'],
        CreatedBy=data['CreatedBy']
    )
    db.session.add(new_hall)
    db.session.commit()
    return jsonify(new_hall.__repr__()), 201

# ID'ye göre salon getir
@hall_routes.route('/halls/<int:id>', methods=['GET'])
def get_hall(id):
    hall = Hall.query.get(id)
    if hall:
        return jsonify(hall.__repr__())
    return jsonify({"message": "Hall not found"}), 404

# Salonu güncelle
@hall_routes.route('/halls/<int:id>', methods=['PUT'])
def update_hall(id):
    hall = Hall.query.get(id)
    if hall:
        data = request.get_json()
        hall.Capacity = data.get('Capacity', hall.Capacity)
        hall.ChangedDate = data.get('ChangedDate', hall.ChangedDate)
        hall.ChangedBy = data.get('ChangedBy', hall.ChangedBy)

        db.session.commit()
        return jsonify(hall.__repr__())
    return jsonify({"message": "Hall not found"}), 404

# Salonu sil
@hall_routes.route('/halls/<int:id>', methods=['DELETE'])
def delete_hall(id):
    hall = Hall.query.get(id)
    if hall:
        db.session.delete(hall)
        db.session.commit()
        return jsonify({"message": "Hall deleted successfully"})
    return jsonify({"message": "Hall not found"}), 404
