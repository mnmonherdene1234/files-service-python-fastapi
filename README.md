# video-security-files-service

## Development run

```bash
uvicorn main:app --reload
```

## Production run

```bash
uvicorn main:app --host 0.0.0.0 --port 7798 --workers 4
```
