
from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO

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

    # 2. Set maximum file size
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

    # 6. Parse CSV content
    try:
        df = pd.read_csv(BytesIO(contents))

        if len(df.columns) == 0:
            raise HTTPException(
                status_code=400,
                detail="CSV must contain columns"
            )

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

    # 7. Return metadata
    return {
        "filename": file.filename,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "status": "uploaded"
    }
