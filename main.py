from fastapi import FastAPI

from routers import router
from utils.allow_all_cors import allow_all_cors
from utils.serve_files import serve_files

# Create the FastAPI app
app = FastAPI()

# Allow all CORS requests
allow_all_cors(app)

# Add the files serving
serve_files(app)

# Add routers
app.include_router(router)
