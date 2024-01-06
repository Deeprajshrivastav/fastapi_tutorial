import pytest

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