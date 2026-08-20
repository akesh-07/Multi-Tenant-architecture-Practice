def get_token_headers(client, tenant_id: int):
    # Our /api/v1/token mock endpoint creates the tenant if it doesn't exist
    response = client.post("/api/v1/token", data={"username": str(tenant_id), "password": "password"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_crud_student(client):
    headers = get_token_headers(client, tenant_id=1)

    # 1. Create Student
    student_data = {
        "name": "Alice Smith",
        "age": 22,
        "dept": "Computer Science",
        "mail": "alice@example.com"
    }
    response = client.post("/api/v1/students", json=student_data, headers=headers)
    assert response.status_code == 200
    created_student = response.json()
    assert created_student["name"] == student_data["name"]
    student_id = created_student["id"]

    # 2. Read Student
    response = client.get(f"/api/v1/students/{student_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Alice Smith"

    # 3. Update Student
    student_data["age"] = 23
    response = client.put(f"/api/v1/students/{student_id}", json=student_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["age"] == 23

    # 4. Delete Student
    response = client.delete(f"/api/v1/students/{student_id}", headers=headers)
    assert response.status_code == 200

    # Verify deleted
    response = client.get(f"/api/v1/students/{student_id}", headers=headers)
    assert response.status_code == 404

def test_tenant_isolation(client):
    # Setup headers for two different tenants
    tenant1_headers = get_token_headers(client, tenant_id=1)
    tenant2_headers = get_token_headers(client, tenant_id=2)

    # Tenant 1 creates a student
    student_data = {
        "name": "Bob Jones",
        "age": 20,
        "dept": "Math",
        "mail": "bob@example.com"
    }
    response = client.post("/api/v1/students", json=student_data, headers=tenant1_headers)
    assert response.status_code == 200
    student_id = response.json()["id"]

    # Tenant 1 should see the student in the list
    response = client.get("/api/v1/students", headers=tenant1_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

    # Tenant 2 should NOT see the student in the list
    response = client.get("/api/v1/students", headers=tenant2_headers)
    assert response.status_code == 200
    assert len(response.json()) == 0

    # Tenant 2 should get 404 when trying to fetch Tenant 1's student by ID
    response = client.get(f"/api/v1/students/{student_id}", headers=tenant2_headers)
    assert response.status_code == 404

    # Tenant 2 should get 404 when trying to update Tenant 1's student
    response = client.put(f"/api/v1/students/{student_id}", json=student_data, headers=tenant2_headers)
    assert response.status_code == 404

    # Tenant 2 should get 404 when trying to delete Tenant 1's student
    response = client.delete(f"/api/v1/students/{student_id}", headers=tenant2_headers)
    assert response.status_code == 404

    # Tenant 1 can still fetch and delete their own student
    response = client.get(f"/api/v1/students/{student_id}", headers=tenant1_headers)
    assert response.status_code == 200
