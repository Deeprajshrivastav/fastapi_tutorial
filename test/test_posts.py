

def test_all_posts(authorized_client, create_test_post):
    res = authorized_client.get('/post/')
    print(res.json())
    assert res.status_code == 200
