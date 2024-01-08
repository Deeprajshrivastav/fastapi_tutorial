def test_vote_on_post(authorized_client, create_test_post):
    response = authorized_client.post('/vote/', json={'post_id':create_test_post[0].id, 'dir': 1})
    assert response.status_code == 201
    print(response.json())
    
def test_unauthorized_vote_on_post(client, create_test_post):
    response = client.post('/vote/', json={'post_id':create_test_post[0].id, 'dir': 1})
    assert response.status_code == 401
    print(response.json())
    
def test_vote_on_not_exitspost(authorized_client, create_test_post):
    response = authorized_client.post('/vote/', json={'post_id':11111, 'dir': 1})
    assert response.status_code == 404
    print(response.status_code)