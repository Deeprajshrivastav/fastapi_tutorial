import pytest
from app import schemas


def test_all_posts(authorized_client, create_test_post):
    res = authorized_client.get('/post/')
    assert res.status_code == 200
    assert len(res.json()) == len(create_test_post)


def test_one_posts(authorized_client, create_test_post):
    res = authorized_client.get(f'/post/{create_test_post[0].id}')
    assert res.status_code == 200
    # assert len(res.json()) == len(create_test_post)

@pytest.mark.parametrize('id', (i for i in range(100000, 100000+10)))
def test_not_exist_post(authorized_client, create_test_post, id):
    res = authorized_client.get(f'/post/{id}')
    assert res.status_code == 404
    assert res.json()['detail'] == f'No post found with id {id} '
    # assert len(res.json()) == len(create_test_post)


def test_unauthorized_post(client, create_test_post):
    res = client.get('/post/')
    assert res.status_code == 401
    assert res.json()['detail'] == 'Not authenticated'
    
def test_unauthorized_one_post(client, create_test_post):
    res = client.get(f'/post/{create_test_post[0].id}')
    assert res.status_code == 401
    assert res.json()['detail'] == 'Not authenticated'
    
@pytest.mark.parametrize('title, content, published', [('title 1', 'content 1', True),
                                                       ('title 2', 'content 2', False),
                                                       ('title 3', 'content 3', True),
                                                       ('title 4', 'content 4', True),
                                                       ('title 5', 'content 4', False)])
def test_post(authorized_client, title, content, published):
    response = authorized_client.post('/post', json={'title': title, 'content': content, 'published': published})
    
    assert response.status_code == 201
    created_post = schemas.Post(**response.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    