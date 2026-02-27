Job Portal API V2
=================

A FastAPI-based Job Portal with role-based access control.

Roles:
- Admin: Manage users, companies, jobs, applications
- Employer: Create companies, post jobs, manage applications
- Candidate: Browse jobs, apply for jobs

Endpoints:
- /auth - Authentication (register, login)
- /admin - Admin operations
- /employer - Employer operations
- /candidate - Candidate operations

Run:
    uvicorn app.main:app --reload
