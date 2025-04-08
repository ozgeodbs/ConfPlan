from flask import Blueprint, request, jsonify
from models.paper import Paper
import pandas as pd
import requests

paper_routes = Blueprint('paper', __name__)

# Tüm bildirileri listele
@paper_routes.route('/papers', methods=['GET'])
def get_papers():
    papers = Paper.query.filter_by(IsDeleted=False).all()  # Assuming IsDeleted field exists
    return jsonify([paper.to_dict() for paper in papers]), 200

# Yeni bir bildiri oluştur
@paper_routes.route('/papers', methods=['POST'])
def create_paper():
    data = request.get_json()
    new_paper = Paper(
        Title=data['Title'],
        SpeakerId=data['SpeakerId'],
        CategoryId=data['CategoryId'],
        Duration=data['Duration'],
        Description=data.get('Description', '')
    )
    new_paper.save()  # Assuming save() is defined in your base model
    return jsonify(new_paper.to_dict()), 201

# ID'ye göre bildiri getir
@paper_routes.route('/papers/<int:id>', methods=['GET'])
def get_paper(id):
    paper = Paper.query.get(id)
    if paper and not paper.IsDeleted:
        return jsonify(paper.to_dict())
    return jsonify({"message": "Paper not found"}), 404

# Bildiriyi güncelle
@paper_routes.route('/papers/<int:id>', methods=['PUT'])
def update_paper(id):
    paper = Paper.query.get(id)
    if paper and not paper.IsDeleted:
        data = request.get_json()
        paper.Title = data.get('Title', paper.Title)
        paper.SpeakerId = data.get('SpeakerId', paper.SpeakerId)
        paper.CategoryId = data.get('CategoryId', paper.CategoryId)
        paper.Duration = data.get('Duration', paper.Duration)
        paper.Description = data.get('Description', paper.Description)

        paper.update()  # Assuming update() is defined in your base model
        return jsonify(paper.to_dict())
    return jsonify({"message": "Paper not found"}), 404

# Bildiriyi sil
@paper_routes.route('/papers/<int:id>', methods=['DELETE'])
def delete_paper(id):
    paper = Paper.query.get(id)
    if paper and not paper.IsDeleted:
        paper.delete()  # Assuming delete() is defined in your base model
        return jsonify({"message": "Paper deleted successfully"})
    return jsonify({"message": "Paper not found"}), 404

# 📌 Belirli bir konferansa ait bildirileri getir
@paper_routes.route('/<int:conference_id>/papers/get/all', methods=['GET'])
def get_papers_by_conference(conference_id):
    papers = Paper.query.filter_by(ConferenceId=conference_id, IsDeleted=False).all()
    if papers:
        return jsonify([paper.to_dict() for paper in papers]), 200
    return jsonify({"message": "No papers found for this conference"}), 404

# 📌 Belirli bir konferans ve konuşmacıya ait bildirileri getir
@paper_routes.route('/<int:conference_id>/papers/speaker/<int:speaker_id>/get/all', methods=['GET'])
def get_papers_by_conference_and_speaker(conference_id, speaker_id):
    papers = Paper.query.filter_by(ConferenceId=conference_id, SpeakerId=speaker_id, IsDeleted=False).all()
    if papers:
        return jsonify([paper.to_dict() for paper in papers]), 200
    return jsonify({"message": "No papers found for this conference and speaker"}), 404

@paper_routes.route('/import/papers', methods=['POST'])
def import_papers():
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

        title = row.get('Title')
        conference_id = row.get('ConferenceId')
        speaker_id = row.get('SpeakerId')
        category_id = row.get('CategoryId')
        duration = row.get('Duration')
        description = row.get('Description')
        hall_id = row.get('HallId')

        # Zorunlu alanlar validasyonu
        if not title or not isinstance(title, str):
            errors.append(f"Row {row_number}: Title is required and must be a string.")
            continue

        conference_response = requests.get(f"/conference/{conference_id}")
        if conference_response.status_code != 200:
            errors.append(f"Row {row_number}: Conference with ID {conference_id} not found or deleted.")
            continue

        # Speaker Kontrolü
        speaker_response = requests.get(f"/speaker/{speaker_id}")
        if speaker_response.status_code != 200:
            errors.append(f"Row {row_number}: Speaker with ID {speaker_id} not found or deleted.")
            continue

        # Category Kontrolü
        category_response = requests.get(f"/category/{category_id}")
        if category_response.status_code != 200:
            errors.append(f"Row {row_number}: Category with ID {category_id} not found or deleted.")
            continue

        # Hall Kontrolü
        hall_response = requests.get(f"/hall/{hall_id}")
        if hall_response.status_code != 200:
            errors.append(f"Row {row_number}: Hall with ID {hall_id} not found or deleted.")
            continue

        # Duration kontrolü (isteğe bağlı ama sayısal olmalı)
        if duration and not isinstance(duration, (int, float)):
            errors.append(f"Row {row_number}: Duration must be a number.")
            continue

        paper = Paper(
            Title=title.strip(),
            ConferenceId=conference_id,
            SpeakerId=speaker_id,
            CategoryId=category_id,
            Duration=int(duration) if duration else None,
            Description=description.strip() if isinstance(description, str) else None,
            HallId=hall_id
        )

        try:
            paper.save()
            created.append(title)
        except Exception as e:
            errors.append(f"Row {row_number}: Database error - {str(e)}")

    return jsonify({
        'message': f'{len(created)} papers imported successfully.',
        'created': created,
        'errors': errors
    }), 200

