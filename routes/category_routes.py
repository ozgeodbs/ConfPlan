from flask import Blueprint, request, jsonify
from models.category import Category
from app import db

category_routes = Blueprint('category', __name__)

# Tüm kategorileri listele
@category_routes.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.__repr__() for category in categories])

# Yeni bir kategori oluştur
@category_routes.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    new_category = Category(
        Title=data['Title'],
        CreatedDate=data['CreatedDate'],
        CreatedBy=data['CreatedBy']
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify(new_category.__repr__()), 201

# ID'ye göre kategori getir
@category_routes.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get(id)
    if category:
        return jsonify(category.__repr__())
    return jsonify({"message": "Category not found"}), 404

# Kategoriyi güncelle
@category_routes.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get(id)
    if category:
        data = request.get_json()
        category.Title = data.get('Title', category.Title)
        category.ChangedDate = data.get('ChangedDate', category.ChangedDate)
        category.ChangedBy = data.get('ChangedBy', category.ChangedBy)

        db.session.commit()
        return jsonify(category.__repr__())
    return jsonify({"message": "Category not found"}), 404

# Kategoriyi sil
@category_routes.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "Category deleted successfully"})
    return jsonify({"message": "Category not found"}), 404
