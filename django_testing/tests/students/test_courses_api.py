import pytest

from students.models import Course


@pytest.mark.django_db
def test_get_one_course_api(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/{courses[5].id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == courses[5].name

@pytest.mark.django_db
def test_courses_api(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    data = response.json()
    assert response.status_code == 200
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name

@pytest.mark.django_db
def test_id_filter(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/', {'id': courses[0].id})
    data = response.json()
    assert response.status_code == 200
    assert data[0]['id'] == courses[0].id

@pytest.mark.django_db
def test_name_filter(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/', {'name': courses[0].name})
    data = response.json()
    assert response.status_code == 200
    assert data[0]['name'] == courses[0].name

@pytest.mark.django_db
def test_post_courses_api(client):
    c = Course.objects.count()
    response = client.post('/api/v1/courses/', {'name': 'Python'})
    assert response.status_code == 201
    assert Course.objects.count() == c + 1

@pytest.mark.django_db
def test_patch_course_api(client, course_factory):
    course = course_factory(_quantity=5)
    response = client.patch(f'/api/v1/courses/{course[3].id}/', {'name': 'Python'})
    data = response.json()
    assert response.status_code == 200
    data_2 = Course.objects.get(pk=course[3].id)
    assert data_2.name == data['name']


@pytest.mark.django_db
def test_delete_course_api(client, course_factory):
    course = course_factory(_quantity=5)
    c = Course.objects.count()
    response = client.delete(f'/api/v1/courses/{course[4].id}/')
    assert response.status_code == 204
    assert Course.objects.count() == c - 1