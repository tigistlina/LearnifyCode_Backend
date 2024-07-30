import pytest

def test_generate_lesson(client):
    response = client.post(
        '/generate_lesson', json={'prompt': 'Explain Binary Trees'})
    assert response.status_code == 200
    assert 'lesson_id' in response.json
    assert 'lesson' in response.json


def test_get_lessons(client):
    response = client.get('/lessons')
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_get_lesson_by_id(client, setup_firestore_emulator):
    lesson_id = 'test_id'
    response = client.get(f'/lessons/{lesson_id}')
    assert response.status_code == 200
    response_json = response.json
    assert 'prompt' in response_json['data']
    assert 'lesson' in response_json['data']
    assert 'id' in response_json
    assert response_json['id'] == lesson_id


def test_search_lessons(client, app, setup_firestore_emulator):
    # Insert test data using the app fixture
    test_lesson_data = {
        'prompt': 'Binary Trees Overview',
        'lesson': [
            "A binary tree is a tree data structure in which each node has at most two children, referred to as the left child and the right child."
        ]
    }
    lesson_id = 'binary_tree_test_id'
    app.db.collection('lessons').document(lesson_id).set(test_lesson_data)

    # Search for the inserted data
    response = client.get('/lessons/search?title=binary tree')

    # Assert the response
    assert response.status_code == 200
    assert len(response.json) > 0
    assert any(
        'Binary Trees Overview' in lesson['prompt'] for lesson in response.json)


def test_generate_lesson_missing_prompt(client):
    response = client.post('/generate_lesson', json={})
    assert response.status_code == 400
    assert 'error' in response.json


def test_get_lesson_by_invalid_id(client):
    response = client.get('/lessons/invalid_id')
    assert response.status_code == 404


def test_search_lessons_no_matches(client):
    response = client.get('/lessons/search?title=nonexistent')
    assert response.status_code == 200
    assert len(response.json) == 0
