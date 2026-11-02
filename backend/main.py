
import csv
from io import BytesIO

import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException

from app.services.profiling import profile_dataset


app = FastAPI(
    title="Dataset Doctor",
    description="AI/ML Dataset Health and Experiment Platform",
    version="1.0.0"
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


@app.post("/api/datasets/upload")
async def upload_dataset(file: UploadFile = File(...)):

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

    # 6. Parse CSV and generate profile
    try:
        # Decode CSV content
        decoded_contents = contents.decode("utf-8-sig")

        # Read original CSV headers before Pandas modifies them
        csv_reader = csv.reader(decoded_contents.splitlines())
        headers = next(csv_reader, [])

        # Check for duplicate column names
        if len(headers) != len(set(headers)):
            raise ValueError(
                "Duplicate column names found in CSV"
            )

        # Read CSV using Pandas
        df = pd.read_csv(BytesIO(contents))

        if len(df.columns) == 0:
            raise ValueError("CSV must contain columns")

        # Generate dataset profile
        profile = profile_dataset(df)

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

    # 7. Return metadata and profile
    return {
        "filename": file.filename,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "profile": profile,
        "status": "uploaded"
    }
