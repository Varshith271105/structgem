"""
main.py — FastAPI application for Smart Syllabus Topic Segregator.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load .env BEFORE importing modules that use env vars
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from logger_config import get_logger
from parser import parse_file, parse_text
from cleaner import clean_text
from chunker import chunk_text
from llm_engine import extract_topics
from merger import merge_results
from structurer import structure_topics

logger = get_logger("main")

app = FastAPI(
    title="Smart Syllabus Topic Segregator",
    description="Parse syllabi and extract structured topic hierarchies using LLM.",
    version="1.0.0",
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://structgem-90uuhv6gd-varshith271105s-projects.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Smart Syllabus Topic Segregator API"}


@app.post("/process")
async def process_syllabus(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
):
    """
    Process a syllabus file or text input.
    Returns structured JSON with topics, subtopics, and concepts.
    """
    try:
        # --- Step 1: Parse input ---
        if file and file.filename:
            logger.info(f"Processing uploaded file: {file.filename}")
            file_bytes = await file.read()
            if not file_bytes:
                raise HTTPException(status_code=400, detail="Uploaded file is empty.")
            raw_text = parse_file(file_bytes, file.filename)
        elif text and text.strip():
            logger.info("Processing text input")
            raw_text = parse_text(text.strip())
        else:
            raise HTTPException(
                status_code=400,
                detail="Please provide either a file upload or text input.",
            )

        if not raw_text.strip():
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the input.",
            )

        # --- Step 2: Clean text ---
        cleaned = clean_text(raw_text)
        logger.info(f"Cleaned text length: {len(cleaned)} chars")

        # --- Step 3: Chunk text ---
        chunks = chunk_text(cleaned)
        logger.info(f"Created {len(chunks)} chunks")

        # --- Step 4: LLM topic extraction (parallel) ---
        tasks = [extract_topics(chunk, i) for i, chunk in enumerate(chunks)]
        chunk_results = await asyncio.gather(*tasks)
        logger.info(f"LLM extraction complete for {len(chunk_results)} chunks")

        # --- Step 5: Merge results ---
        merged = merge_results(chunk_results)
        logger.info(f"Merged into {len(merged.get('topics', []))} topics")

        # --- Step 6: Structure/order ---
        structured = await structure_topics(merged)
        logger.info(f"Final output: {len(structured.get('topics', []))} topics")

        logger.info("Processing complete — returning structured output")
        return structured

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        logger.error(f"Runtime error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
