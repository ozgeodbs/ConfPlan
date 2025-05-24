from flask import Blueprint, request, jsonify
from models import db
from models.similarity import Similarity
from models.paper import Paper
import similarity
import config

similarity_routes = Blueprint('similarity', __name__)

@similarity_routes.route('/similarities', methods=['GET'])
def get_similarities():
    similarities = Similarity.query.all()
    return jsonify([{
        'Id': similarity.Id,
        'PaperId': similarity.PaperId,
        'SimilarPaperId': similarity.SimilarPaperId,
        'SimilarityScore': similarity.SimilarityScore,
        'PaperTitle': similarity.PaperTitle,
        'SimilarPaperTitle': similarity.SimilarPaperTitle
    } for similarity in similarities]), 200

@similarity_routes.route('/similarities', methods=['POST'])
def create_similarity():
    data = request.get_json()

    paper_id = data['PaperId']
    similar_paper_id = data['SimilarPaperId']
    similarity_score = data['SimilarityScore']

    paper = Paper.query.get(paper_id)
    similar_paper = Paper.query.get(similar_paper_id)

    if not paper or not similar_paper:
        return jsonify({'message': 'Not valid PaperId or SimilarPaperId.'}), 404

    similarity = Similarity(
        PaperId=paper_id,
        SimilarPaperId=similar_paper_id,
        SimilarityScore=similarity_score,
        PaperTitle=paper.Title,
        SimilarPaperTitle=similar_paper.Title
    )

    db.session.add(similarity)
    db.session.commit()

    return jsonify({
        'message': 'Similarity record saved successfully.',
        'Similarity': similarity.to_dict()
    }), 201

@similarity_routes.route('/similarities/<int:id>', methods=['GET'])
def get_similarity(id):
    similarity = Similarity.query.get(id)
    if similarity:
        return jsonify({
            'PaperId': similarity.PaperId,
            'SimilarPaperId': similarity.SimilarPaperId,
            'SimilarityScore': similarity.SimilarityScore,
            'PaperTitle': similarity.PaperTitle,
            'SimilarPaperTitle': similarity.SimilarPaperTitle
        }), 200
    return jsonify({"message": "Similarity record could not found"}), 404

@similarity_routes.route('/similarities/<int:id>', methods=['PUT'])
def update_similarity(id):
    similarity = Similarity.query.get(id)
    if similarity:
        data = request.get_json()
        similarity_score = data.get('SimilarityScore', similarity.SimilarityScore)
        similarity.SimilarityScore = similarity_score

        db.session.commit()

        return jsonify({
            'message': 'Similarity record could not be updated.',
            'Similarity': similarity.to_dict()
        }), 200
    return jsonify({"message": "Similarity record could not found"}), 404

@similarity_routes.route('/similarities/<int:id>', methods=['DELETE'])
def delete_similarity(id):
    similarity = Similarity.query.get(id)
    if similarity:
        db.session.delete(similarity)
        db.session.commit()
        return jsonify({'message': 'Similarity record deleted'}), 200
    return jsonify({"message": "Similarity record could not found"}), 404


@similarity_routes.route('/<int:conference_id>/papers/save_similarities', methods=['POST'])
def save_similarities(conference_id):

    token = request.headers.get('token')
    if not token or token != config.Config.API_SECRET_TOKEN:
        return jsonify({'message': 'Unauthorized'}), 401

    papers = Paper.query.filter_by(ConferenceId=conference_id, IsDeleted=False).all()
    if not papers:
        return jsonify({"message": "No papers found for this conference"}), 404

    similarity.save_similarities(papers)

    return jsonify({
        'message': f'Similarities saved successfully.'
    }), 201

@similarity_routes.route('/<int:conference_id>/papers/get/similarities', methods=['GET'])
def get_similarities_by_conference_id(conference_id):

    papers = Paper.query.filter_by(ConferenceId=conference_id, IsDeleted=False).all()

    similarities = Similarity.query.filter(
        (Similarity.PaperId.in_([paper.Id for paper in papers])) |
        (Similarity.SimilarPaperId.in_([paper.Id for paper in papers]))
    ).all()

    return jsonify([similarity.to_dict() for similarity in similarities])