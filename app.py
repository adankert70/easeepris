from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from logic import get_report_data

load_dotenv()

app = FastAPI(title="easeepris Web UI")

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.get("/api/report")
async def report(
    year: int = Query(..., description="The year"),
    month: int = Query(..., description="The month (1-12)"),
    region: str = Query(..., description="The price region (e.g., NO2)")
):
    try:
        data = get_report_data(year, month, region)
        return data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
