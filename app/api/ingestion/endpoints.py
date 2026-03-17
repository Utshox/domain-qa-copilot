from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from langchain_core.documents import Document
from app.deps import get_current_active_admin
from app.services.chunker import chunker
from app.db.vector import vector_db
import pypdf
import io

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    admin_user=Depends(get_current_active_admin)
):
    if not file.filename.endswith(".pdf") and not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")

    content = await file.read()
    text = ""
    
    if file.filename.endswith(".pdf"):
        pdf_reader = pypdf.PdfReader(io.BytesIO(content))
        for page in pdf_reader.pages:
            text += page.extract_text()
    else:
        text = content.decode("utf-8")

    chunks = chunker.split_text(text, metadata={"source": file.filename})
    vector_db.add_documents(chunks)
    
    return {"message": f"Successfully ingested {len(chunks)} chunks from {file.filename}"}
