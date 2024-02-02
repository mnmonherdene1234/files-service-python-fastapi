# Files service

This service is responsible for managing files. It is built with FastAPI and uses the file system to store files.

fastapi link: https://fastapi.tiangolo.com/

## Requirements

```bash
pip install -r requirements.txt
```

### Development run

## How to run

```bash
uvicorn main:app --reload
```

### Production run

```bash
uvicorn main:app --host 0.0.0.0 --port 7798 --workers 4
```

### Docker build

```bash
docker build -t video-security-files-service .
```

### Docker compose run

Default port is 7798

```bash
./deploy.sh
```

## Endpoints

### Service info

/ - GET

### Upload file

/upload - POST

body file (multipart/form-data)

### Get file

/file/{filename} - GET