from google.cloud import firestore


def store_lesson(db, prompt, lesson_text):
    lesson_ref = db.collection('lessons').document()
    lesson_ref.set({
        'prompt': prompt,
        'lesson': lesson_text
    })
    return lesson_ref.id


def fetch_lessons(db):
    lessons = db.collection('lessons').stream()
    lessons_list = [{"id": lesson.id, "data": lesson.to_dict()}
                    for lesson in lessons]
    return lessons_list


def fetch_lesson_by_id(db, lesson_id):
    lesson_ref = db.collection('lessons').document(lesson_id)
    lesson = lesson_ref.get()
    if lesson.exists:
        return {"id": lesson.id, "data": lesson.to_dict()}
    return None


def search_lessons_by_title(db, title_query):
    # Use a case-insensitive search if you need to
    lessons = db.collection('lessons').stream()

    # Filter lessons that contain the title_query in their prompt
    filtered_lessons = [
        {
            "id": lesson.id,
            "prompt": lesson.to_dict().get('prompt', ''),
            "lesson": lesson.to_dict().get('lesson', '')
        }
        for lesson in lessons
        if title_query.lower() in lesson.to_dict().get('prompt', '').lower()
    ]

    return filtered_lessons

