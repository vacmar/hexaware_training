"""
Employer Tests - Essential test cases only.
"""

import pytest


class TestEmployer:
    """Core employer tests."""

    def test_create_job(self, client, employer_headers, company):
        """Test employer can create a job."""
        response = client.post("/employer/jobs", headers=employer_headers, json={
            "title": "Senior Dev",
            "description": "Build products",
            "salary": 150000,
            "company_id": company.id
        })
        assert response.status_code == 200
        assert response.json()["title"] == "Senior Dev"

    def test_update_job(self, client, employer_headers, job):
        """Test employer can update a job."""
        response = client.put(f"/employer/jobs/{job.id}", headers=employer_headers, json={
            "salary": 120000
        })
        assert response.status_code == 200

    def test_delete_job(self, client, employer_headers, job):
        """Test employer can delete a job."""
        response = client.delete(f"/employer/jobs/{job.id}", headers=employer_headers)
        assert response.status_code == 200

    def test_view_applications(self, client, employer_headers, application):
        """Test employer can view applications."""
        response = client.get("/employer/applications", headers=employer_headers)
        assert response.status_code == 200

    def test_wrong_role_blocked(self, client, candidate_headers, company):
        """Test candidate cannot create jobs."""
        response = client.post("/employer/jobs", headers=candidate_headers, json={
            "title": "Dev",
            "description": "Test",
            "salary": 100000,
            "company_id": company.id
        })
        assert response.status_code == 403
