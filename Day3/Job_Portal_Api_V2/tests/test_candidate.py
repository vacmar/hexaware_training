"""
Candidate Tests - Essential test cases only.
"""

import pytest


class TestCandidate:
    """Core candidate tests."""

    def test_view_jobs(self, client, candidate_headers, job):
        """Test candidate can view jobs."""
        response = client.get("/candidate/jobs", headers=candidate_headers)
        assert response.status_code == 200

    def test_apply_for_job(self, client, candidate_headers, job):
        """Test candidate can apply for a job."""
        response = client.post(f"/candidate/apply/{job.id}", headers=candidate_headers)
        assert response.status_code == 200

    def test_view_applications(self, client, candidate_headers, application):
        """Test candidate can view their applications."""
        response = client.get("/candidate/applications", headers=candidate_headers)
        assert response.status_code == 200

    def test_unauthorized_access(self, client, job):
        """Test unauthenticated access is blocked."""
        response = client.get("/candidate/jobs")
        assert response.status_code == 401

    def test_wrong_role_blocked(self, client, employer_headers):
        """Test employer cannot access candidate endpoints."""
        response = client.get("/candidate/jobs", headers=employer_headers)
        assert response.status_code == 403
