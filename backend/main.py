
import csv
from io import BytesIO, StringIO

import pandas as pd
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.services.profiling import profile_dataset
from app.services.quality import run_quality_checks
from app.services.ml_experiment import run_experiment


app = FastAPI(
    title="Dataset Doctor",
    description="AI/ML Dataset Health and Experiment Platform",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://dataset-doctor-frontend-k9oe.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Shared CSV validation and loading function
async def load_csv_file(file: UploadFile):

    # 1. Validate filename and extension
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed"
        )

    # 2. Set maximum file size (10 MB)
    max_size = 10 * 1024 * 1024

    # 3. Read at most 10 MB + 1 byte
    contents = await file.read(max_size + 1)

    # 4. Validate file size
    if len(contents) > max_size:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds 10 MB limit"
        )

    # 5. Reject empty files
    if not contents.strip():
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    # 6. Parse and validate CSV
    try:
        decoded_contents = contents.decode("utf-8-sig")

        # Check CSV headers
        csv_reader = csv.reader(StringIO(decoded_contents))
        headers = next(csv_reader, [])

        if not headers:
            raise ValueError("CSV must contain column headers")

        # Reject blank column names
        if any(not header.strip() for header in headers):
            raise ValueError("CSV contains blank column names")

        # Reject duplicate column names
        if len(headers) != len(set(headers)):
            raise ValueError("Duplicate column names found in CSV")

        # Load CSV into DataFrame
        df = pd.read_csv(BytesIO(contents))

        if len(df.columns) == 0:
            raise ValueError("CSV must contain columns")

        # Reject datasets without data rows
        if df.empty:
            raise ValueError("CSV must contain at least one data row")

        return df

    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=400,
            detail="CSV file contains no data"
        )

    except (pd.errors.ParserError, UnicodeDecodeError):
        raise HTTPException(
            status_code=400,
            detail="Invalid CSV content"
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@app.get("/")
def home():
    return {"message": "Welcome to Dataset Doctor API"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "Dataset Doctor"
    }


# Dataset upload and profiling endpoint
@app.post("/api/datasets/upload")
async def upload_dataset(file: UploadFile = File(...)):

    df = await load_csv_file(file)

    profile = profile_dataset(df)
    quality_report = run_quality_checks(df)

    return {
        "filename": file.filename,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "profile": profile,
        "quality_report": quality_report,
        "status": "uploaded"
    }


# ML experiment endpoint
@app.post("/api/experiments/run")
async def run_ml_experiment(
    file: UploadFile = File(...),
    target_column: str = Form(...),
    task_type: str = Form(...)
):

    # 1. Load and validate CSV
    df = await load_csv_file(file)

    # 2. Run ML experiments
    try:
        results = run_experiment(
            df=df,
            target_column=target_column,
            task_type=task_type
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    # 3. Return experiment results
    return {
        "filename": file.filename,
        "status": "completed",
        "experiment_results": results
    }
