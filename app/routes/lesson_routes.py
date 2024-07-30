from flask import Blueprint, request, jsonify, current_app
from app.services.openai_service import generate_openai_lesson
from app.services.firestore_service import store_lesson, fetch_lessons, fetch_lesson_by_id, search_lessons_by_title

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


@lesson_bp.route('/lessons/<lesson_id>', methods=['GET'])
def get_lesson_by_id(lesson_id):
    lesson = fetch_lesson_by_id(current_app.db, lesson_id)
    if not lesson:
        return jsonify({"error": "Lesson not found"}), 404
    return jsonify(lesson), 200


@lesson_bp.route('/lessons/search', methods=['GET'])
def search_lessons():
    title_query = request.args.get('title', '')

    if not title_query:
        return jsonify({"error": "No title query provided"}), 400

    try:
        lessons_list = search_lessons_by_title(current_app.db, title_query)
        return jsonify(lessons_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
