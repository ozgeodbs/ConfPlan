from flask import Blueprint, request, jsonify
import pandas as pd
from models.category import Category

category_routes = Blueprint('Category', __name__)

# Tüm kategorileri listele
@category_routes.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.filter_by(IsDeleted=False).all()
    return jsonify([category.to_dict() for category in categories]), 200

# Yeni bir kategori oluştur
@category_routes.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()

    new_category = Category(Title=data['Title'])
    new_category.save()

    return jsonify(new_category.to_dict()), 201

# ID'ye göre kategori getir
@category_routes.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get(id)
    if category and not category.IsDeleted:
        return jsonify(category.to_dict())
    return jsonify({"message": "Category not found"}), 404

# Kategoriyi güncelle
@category_routes.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get(id)
    if category and not category.IsDeleted:
        data = request.get_json()
        category.Title = data.get('Title', category.Title)
        category.update()
        return jsonify(category.to_dict())
    return jsonify({"message": "Category not found"}), 404

# Kategoriyi sil
@category_routes.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    if category and not category.IsDeleted:
        category.delete()
        return jsonify({"message": "Category deleted successfully"})
    return jsonify({"message": "Category not found"}), 404


@category_routes.route('/import/categories', methods=['POST'])
def import_categories():
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
        title = str(row.get('Title')).strip()

        if not title:
            errors.append(f"Row {index + 2}: Title is required and must be a non-empty string.")
            continue

        if Category.query.filter_by(Title=title).first():
            errors.append(f"Row {index + 2}: Duplicate title '{title}' already exists.")
            continue

        category = Category(Title=title)
        category.save()
        created.append(title)

    return jsonify({
        'message': f'{len(created)} categories imported successfully.',
        'created': created,
        'errors': errors
    }), 200
