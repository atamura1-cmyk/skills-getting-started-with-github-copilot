def test_get_activities_structure(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities

    chess_activity = activities["Chess Club"]
    assert chess_activity["description"]
    assert chess_activity["schedule"]
    assert isinstance(chess_activity["max_participants"], int)
    assert isinstance(chess_activity["participants"], list)


def test_post_signup_adds_and_rejects_duplicates(client):
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert signup_response.status_code == 200
    assert email in signup_response.json()["message"]

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert email in activities_response.json()[activity_name]["participants"]

    duplicate_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert duplicate_response.status_code == 400
    assert "already signed up" in duplicate_response.json()["detail"].lower()


def test_delete_removes_and_errors(client):
    activity_name = "Programming Class"
    email = "studenttoRemove@mergington.edu"

    add_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert add_response.status_code == 200

    delete_response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert delete_response.status_code == 200
    assert email in delete_response.json()["message"]

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]

    missing_activity_response = client.delete(
        "/activities/Unknown Club/signup",
        params={"email": email},
    )
    assert missing_activity_response.status_code == 404

    missing_participant_response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": "noone@mergington.edu"},
    )
    assert missing_participant_response.status_code == 404
    assert "participant not found" in missing_participant_response.json()["detail"].lower()
