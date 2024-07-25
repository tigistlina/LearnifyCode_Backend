def store_lesson(db, prompt, lesson_text):
    lesson_ref = db.collection('lessons').document()
    lesson_ref.set({
        'prompt': prompt,
        'lesson': lesson_text
    })
    return lesson_ref.id

def fetch_lessons(db):
    lessons = db.collection('lessons').stream()
    lessons_list = [{"id": lesson.id, "data": lesson.to_dict()} for lesson in lessons]
    return lessons_list