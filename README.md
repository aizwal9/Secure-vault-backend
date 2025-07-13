# Secure Vault Backend

Django-based backend for the File Hub application, providing a robust API for file management.

## 🚀 Technology Stack

- Python 3.9+
- Django 4.x
- Django REST Framework
- SQLite (Development database)
- Docker
- WhiteNoise for static file serving
- AWS S3 for file storage
- DRF Pagination

## 📋 Prerequisites

- Python 3.9 or higher
- pip
- Docker (if using containerized setup)
- virtualenv or venv (recommended)
- AWS account & S3 bucket (for file storage)

## 🛠️ Installation & Setup

### Local Development

1. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**
   Create a `.env` file in the backend directory:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=localhost,127.0.0.1
   # AWS S3 settings
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret-key
   AWS_STORAGE_BUCKET_NAME=your-bucket-name
   AWS_S3_REGION_NAME=your-region
   ```

4. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
   Note: SQLite database will be automatically created at `db.sqlite3`

5. **Run Development Server**
   ```bash
   python manage.py runserver
   ```
   Access the API at http://localhost:8000/api

### Docker Setup

```bash
# Build the image
docker build -t file-hub-backend .

# Run the container
docker run -p 8000:8000 file-hub-backend
```

## 📁 Project Structure

```
backend/
├── core/           # Project settings and main URLs
├── files/          # File management app
│   ├── models.py   # Data models
│   ├── views.py    # API views
│   ├── urls.py     # URL routing
│   └── tests.py    # Unit tests
├── db.sqlite3      # SQLite database
└── manage.py       # Django management script
```

## 🔌 API Endpoints

### Files API (`/api/files/`)

- `GET /api/files/`: List all files
  - Query Parameters:
    - `search`: Search files by name
    - `sort`: Sort by created_at, name, or size
    - `page`: Page number for pagination 
    - `page_size`: Number of items per page
  - `Response`: JSON list of files with pagination info

- `POST /api/files/`: Upload new file
  - Request: Multipart form data
  - Fields:
    - `file`: File to upload
    - `description`: Optional file description

- `GET /api/files/<uuid>/`: Get file details
- `DELETE /api/files/<uuid>/`: Delete file

## 🔒 Security Features

- UUID-based file identification
- WhiteNoise for secure static file serving
- CORS configuration for frontend integration
- AWS S3 access control for file storage (ensure proper IAM permissions and bucket policies)
- Django's built-in security features:
  - CSRF protection
  - XSS prevention
  - SQL injection protection