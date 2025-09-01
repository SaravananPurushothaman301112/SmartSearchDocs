from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from typing import List
from app.utils import process_document, search_documents
from app.models import DocumentIndex
from fastapi.responses import FileResponse

app = FastAPI(title="AI Document Search")



# Add this route to your main.py
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/images/mainlogo.png")

# Setup static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global variable for document index (in production, use a proper database)
document_index = DocumentIndex()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        file_path = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Process document
        document_id, chunks = process_document(file_path, file.filename)
        
        # Add to index
        document_index.add_document(document_id, file.filename, chunks)
        
        return {"message": f"File '{file.filename}' uploaded and processed successfully", "document_id": document_id}
    
    except Exception as e:
        return {"message": f"Error uploading file: {str(e)}"}

@app.post("/search/")
async def search(query: str = Form(...)):
    try:
        results = search_documents(query, document_index)
        return {"results": results}
    except Exception as e:
        return {"message": f"Error searching: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)