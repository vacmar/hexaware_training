"""
Leave Management Tests for Leave Management System.
"""

import pytest
from datetime import date, timedelta


class TestEmployeeLeave:
    """Employee leave operations tests."""

    def test_apply_leave(self, client, employee_headers):
        """Test employee applying for leave."""
        response = client.post("/employee/leaves", json={
            "start_date": str(date.today() + timedelta(days=5)),
            "end_date": str(date.today() + timedelta(days=7)),
            "reason": "Personal leave"
        }, headers=employee_headers)
        assert response.status_code == 200
        assert response.json()["status"] == "PENDING"
        assert response.json()["reason"] == "Personal leave"

    def test_apply_leave_invalid_dates(self, client, employee_headers):
        """Test applying leave with end date before start date."""
        response = client.post("/employee/leaves", json={
            "start_date": str(date.today() + timedelta(days=10)),
            "end_date": str(date.today() + timedelta(days=5)),
            "reason": "Invalid dates"
        }, headers=employee_headers)
        assert response.status_code == 400

    def test_apply_leave_past_date(self, client, employee_headers):
        """Test applying leave for past dates."""
        response = client.post("/employee/leaves", json={
            "start_date": str(date.today() - timedelta(days=5)),
            "end_date": str(date.today() - timedelta(days=3)),
            "reason": "Past date leave"
        }, headers=employee_headers)
        assert response.status_code == 400

    def test_get_my_leaves(self, client, employee_headers, leave_request):
        """Test employee viewing their leaves."""
        response = client.get("/employee/leaves", headers=employee_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) >= 1

    def test_get_leave_details(self, client, employee_headers, leave_request):
        """Test getting specific leave details."""
        response = client.get(f"/employee/leaves/{leave_request.id}", headers=employee_headers)
        assert response.status_code == 200
        assert response.json()["id"] == leave_request.id

    def test_cancel_leave(self, client, employee_headers, leave_request):
        """Test cancelling a pending leave."""
        response = client.delete(f"/employee/leaves/{leave_request.id}", headers=employee_headers)
        assert response.status_code == 200

    def test_unauthorized_access(self, client):
        """Test accessing leaves without authentication."""
        response = client.get("/employee/leaves")
        assert response.status_code == 401


class TestManagerLeave:
    """Manager leave operations tests."""

    def test_get_department_leaves(self, client, manager_headers, leave_request):
        """Test manager viewing department leaves."""
        response = client.get("/manager/leaves", headers=manager_headers)
        assert response.status_code == 200
        assert "items" in response.json()

    def test_approve_leave(self, client, manager_headers, leave_request):
        """Test manager approving a leave."""
        response = client.put(f"/manager/leaves/{leave_request.id}/approve", headers=manager_headers)
        assert response.status_code == 200
        assert response.json()["status"] == "APPROVED"

    def test_reject_leave(self, client, manager_headers, leave_request):
        """Test manager rejecting a leave."""
        response = client.put(f"/manager/leaves/{leave_request.id}/reject", headers=manager_headers)
        assert response.status_code == 200
        assert response.json()["status"] == "REJECTED"

    def test_get_department_employees(self, client, manager_headers, employee_user):
        """Test manager viewing department employees."""
        response = client.get("/manager/employees", headers=manager_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_leave_stats(self, client, manager_headers, leave_request):
        """Test manager viewing department leave stats."""
        response = client.get("/manager/reports/leaves", headers=manager_headers)
        assert response.status_code == 200
        assert "total_leaves" in response.json()
        assert "department_name" in response.json()

    def test_employee_cannot_approve(self, client, employee_headers, leave_request):
        """Test that employee cannot approve leaves."""
        response = client.put(f"/manager/leaves/{leave_request.id}/approve", headers=employee_headers)
        assert response.status_code == 403


class TestAdminLeave:
    """Admin leave operations tests."""

    def test_get_all_leaves(self, client, admin_headers, leave_request):
        """Test admin viewing all leaves."""
        response = client.get("/admin/leaves", headers=admin_headers)
        assert response.status_code == 200
        assert "items" in response.json()

    def test_override_leave_status(self, client, admin_headers, leave_request):
        """Test admin overriding leave status."""
        response = client.put(f"/admin/leaves/{leave_request.id}/status", json={
            "status": "APPROVED"
        }, headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["status"] == "APPROVED"

    def test_get_company_leave_stats(self, client, admin_headers, leave_request):
        """Test admin viewing company-wide leave stats."""
        response = client.get("/admin/reports/leaves", headers=admin_headers)
        assert response.status_code == 200
        assert "total_leaves" in response.json()
        assert "pending_leaves" in response.json()

    def test_employee_cannot_access_admin_routes(self, client, employee_headers):
        """Test that employee cannot access admin routes."""
        response = client.get("/admin/leaves", headers=employee_headers)
        assert response.status_code == 403


class TestDepartmentOperations:
    """Department CRUD tests."""

    def test_create_department(self, client, admin_headers):
        """Test creating a department."""
        response = client.post("/admin/departments", json={
            "name": "Sales"
        }, headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["name"] == "Sales"

    def test_get_all_departments(self, client, admin_headers, department):
        """Test getting all departments."""
        response = client.get("/admin/departments", headers=admin_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_duplicate_department(self, client, admin_headers, department):
        """Test creating department with existing name."""
        response = client.post("/admin/departments", json={
            "name": "Engineering"
        }, headers=admin_headers)
        assert response.status_code == 400


class TestUserManagement:
    """User management tests for admin."""

    def test_get_all_users(self, client, admin_headers, employee_user):
        """Test admin getting all users."""
        response = client.get("/admin/users", headers=admin_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_assign_user_to_department(self, client, admin_headers, department):
        """Test assigning user to department."""
        # First create a user
        register_response = client.post("/auth/register", json={
            "name": "New Employee",
            "email": "newemp@test.com",
            "password": "pass123",
            "role": "EMPLOYEE"
        })
        user_id = register_response.json()["id"]
        
        response = client.put(
            f"/admin/users/{user_id}/department/{department.id}",
            headers=admin_headers
        )
        assert response.status_code == 200
        assert response.json()["department_id"] == department.id
