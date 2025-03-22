from flask import Blueprint, request, jsonify
from datetime import datetime
from models.category import Category
from app import db

category_routes = Blueprint('Category', __name__)

# Tüm kategorileri listele
@category_routes.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.filter_by(IsDeleted=False).all()
    return jsonify([category.__repr__() for category in categories]), 200

# Yeni bir kategori oluştur
@category_routes.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()

    new_category = Category(Title=data['Title'])
    new_category.save()

    return jsonify(new_category.__repr__()), 201

# ID'ye göre kategori getir
@category_routes.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get(id)
    if category and not category.IsDeleted:
        return jsonify(category.__repr__())
    return jsonify({"message": "Category not found"}), 404

# Kategoriyi güncelle
@category_routes.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get(id)
    if category and not category.IsDeleted:
        data = request.get_json()
        category.Title = data.get('Title', category.Title)
        category.update()
        return jsonify(category.__repr__())
    return jsonify({"message": "Category not found"}), 404

# Kategoriyi sil
@category_routes.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    if category and not category.IsDeleted:
        category.delete()
        return jsonify({"message": "Category deleted successfully"})
    return jsonify({"message": "Category not found"}), 404
