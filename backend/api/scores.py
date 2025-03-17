from fastapi import APIRouter, Response
import csv
import io
import subprocess
from pathlib import Path

api = APIRouter(prefix="/api/score", tags=["Score"])

CSV_PATH = Path("/workspaces/SOTestingEnv/es_files/teams/final_scores.csv")


def refresh_scores():
    """Run grading script to update scores"""
    try:
        subprocess.run(
            [
                "/usr/bin/python3",
                "/workspaces/SOTestingEnv/backend/script/grade_submissions.py",
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running grading script: {e}")


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
