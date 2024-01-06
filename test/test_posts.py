

def test_all_posts(authorized_client, create_test_post):
    res = authorized_client.get('/post/')
    assert res.status_code == 200
    assert len(res.json()) == len(create_test_post)