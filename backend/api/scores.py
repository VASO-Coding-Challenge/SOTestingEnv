import sys
import logging
from fastapi import APIRouter, HTTPException, Response
import csv
import subprocess
from pathlib import Path

api = APIRouter(prefix="/api/score", tags=["Score"])

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CSV_PATH = Path("/workspaces/SOTestingEnv/es_files/teams/final_scores.csv")


def refresh_scores():
    """Run grading script to update scores"""
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "backend.script.grade_submissions",
            ],
            check=True,
            cwd="/workspaces/SOTestingEnv",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        logger.info("Grading script output:\n%s", result.stdout)

        if result.stderr:
            logger.error("Script errors:\n%s", result.stderr)

    except subprocess.CalledProcessError as e:
        logger.error(
            "Script failed with code %d:\n%s\n%s", e.returncode, e.stdout, e.stderr
        )
        raise HTTPException(
            status_code=500, detail=f"Grading script failed: {e.stderr}"
        )


@api.get("/download", response_class=Response)
def download_scores():
    """Generate and return updated CSV file"""
    refresh_scores()

    with open(CSV_PATH, "r") as file:
        csv_data = file.read()

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=scores.csv"},
    )


@api.get("")
def get_scores():
    """Return scores for frontend display"""
    refresh_scores()

    with open(CSV_PATH, "r") as file:
        reader = csv.DictReader(file)
        return list(reader)
