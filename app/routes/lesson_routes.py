from flask import Blueprint, request, jsonify, current_app
from app.services.openai_service import generate_openai_lesson
from app.services.firestore_service import store_lesson, fetch_lessons

lesson_bp = Blueprint('lesson_bp', __name__)

@lesson_bp.route('/generate_lesson', methods=['POST'])
def generate_lesson():
    data = request.json
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    lesson_text = generate_openai_lesson(prompt)
    lesson_id = store_lesson(current_app.db, prompt, lesson_text)

    return jsonify({"lesson_id": lesson_id, "lesson": lesson_text})

@lesson_bp.route('/lessons', methods=['GET'])
def get_lessons():
    lessons_list = fetch_lessons(current_app.db)
    return jsonify(lessons_list)