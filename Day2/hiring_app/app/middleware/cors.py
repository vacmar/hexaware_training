from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    """
    Configure CORS middleware for the application.
    Allows cross-origin requests from any origin.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for development
        allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],  # Allow all headers
        allow_credentials=True,  # Allow cookies and credentials
    )
