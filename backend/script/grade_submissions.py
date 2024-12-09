"""This script runs all (or specific) tests on student submitted code"""

from sqlmodel import Session
import polars as pl

from ..services import SubmissionService, TeamService, QuestionService
from ..models import Team, ScoredTest
from ..db import engine

DEFAULT_BY_TEST_FILE = "es_files/teams/scored_tests.csv"
DEFAULT_TOTAL_FILE = "es_files/teams/final_scores.csv"


def main():
    q_svc = QuestionService()
    sub_svc = SubmissionService()
    with Session(engine) as session:
        team_svc = TeamService(session)
        teams = team_svc.get_all_teams()

    # TODO: Could make this multithreaded
    test_list: list[pl.DataFrame] = []
    for team in teams:
        for q_num in range(1, q_svc.get_question_count() + 1):
            dfs = [
                create_test_df(team.name, test)
                for test in sub_svc.grade_submission(q_num, team.name)
            ]
            test_list.extend(dfs)

    test_table = pl.concat(test_list)
    test_table.write_csv(DEFAULT_BY_TEST_FILE)

    # Calculate the Total File
    total_table = test_table.group_by("Team Number").agg(
        pl.col("Score").sum(), pl.col("Max Score").sum()
    )
    total_table.write_csv(DEFAULT_TOTAL_FILE)


def create_test_df(team_name: str, test: ScoredTest) -> pl.DataFrame:
    """Creates a DataFrame for a test case"""
    return pl.DataFrame(
        {
            "Team Number": [team_name],
            "Question Number": [test.question_num],
            "Test Name": [test.test_name],
            "Score": [test.score],
            "Max Score": [test.max_score],
            "Test Output": [test.console_log],
        }
    )


if __name__ == "__main__":
    main()
