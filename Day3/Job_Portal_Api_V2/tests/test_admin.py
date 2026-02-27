"""
Admin Tests - Essential test cases only.
"""

import pytest


class TestAdmin:
    """Core admin tests."""

    def test_create_company(self, client, admin_headers):
        """Test admin can create a company."""
        response = client.post("/admin/companies", headers=admin_headers, json={
            "name": "New Company",
            "description": "Description"
        })
        assert response.status_code == 200
        assert response.json()["name"] == "New Company"

    def test_list_companies(self, client, admin_headers, company):
        """Test admin can list companies."""
        response = client.get("/admin/companies", headers=admin_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_view_all_jobs(self, client, admin_headers, job):
        """Test admin can view all jobs."""
        response = client.get("/admin/jobs", headers=admin_headers)
        assert response.status_code == 200

    def test_delete_job(self, client, admin_headers, job):
        """Test admin can delete any job."""
        response = client.delete(f"/admin/jobs/{job.id}", headers=admin_headers)
        assert response.status_code == 200

    def test_view_all_applications(self, client, admin_headers, application):
        """Test admin can view all applications."""
        response = client.get("/admin/applications", headers=admin_headers)
        assert response.status_code == 200

    def test_wrong_role_blocked(self, client, employer_headers):
        """Test employer cannot access admin endpoints."""
        response = client.post("/admin/companies", headers=employer_headers, json={
            "name": "Test"
        })
        assert response.status_code == 403
