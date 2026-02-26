```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
cd Day2/Hiring_app/app
pip install -r requirements.txt
uvicorn main:app --reload
```

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Users
- `POST /users/` - Create a new user
- `GET /users/` - List all users (with pagination)
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Jobs
- `POST /jobs/` - Create a new job
- `GET /jobs/` - List all jobs (with pagination)
- `GET /jobs/{job_id}` - Get job by ID
- `PUT /jobs/{job_id}` - Update job
- `DELETE /jobs/{job_id}` - Delete job

### Applications
- `POST /applications/` - Apply for a job
- `GET /applications/` - List all applications (with pagination)
- `GET /applications/{application_id}` - Get application by ID
- `GET /applications/user/{user_id}` - Get all applications for a user
- `GET /applications/job/{job_id}` - Get all applications for a job
- `PATCH /applications/{application_id}/status` - Update application status
- `DELETE /applications/{application_id}` - Delete application