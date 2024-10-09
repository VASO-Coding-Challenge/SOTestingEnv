import polars as pl


"""
Dev Notes:
    Right now, the corpus is saved and edited in the 'unique_words.csv' file.
    In the future, this should probably be kept and maintained in the database 
    as its own, unrelated table.

    Therefore, these should not be considered ready to be deployed functions, 
    but rather code to use in the interim.
"""


class TeamService:

    # def generate_teams(level: str, number_teams: int, path: str | None):
    #     if path is None:
    #         path = '/workspaces/SOTestingEnv/backend/ES_Files/teams.csv'

    #     user_table = pl.read_csv(path)
    #     if user_table.is_empty():
    #         df = pl.DataFrame({"Team Number": None, "Start Time": None, "End Time": None, "Password": None})
    #     current_user_count = df.

    #     #PATH or DEFAULT_PATH
    #     #If path exists, open file and append new users
    #     #Otherwise, create blank csv

    def generate_team(self, level: str, team_number: int) -> pl.DataFrame:
        team_df = pl.DataFrame(
            {
                "Team Number": f"{level}{team_number}",
                "Start Time": None,
                "End Time": None,
                "Password": self.generate_password(),
            }
        )
        return team_df

    def save_teams_from_csv(self, userTable, path: str):
        """Update User Table with new passwords and users"""
        newUserTable = self.generate_passwords(userTable)
        # TODO -- step to load new users into actual db
        newUserTable.write_csv(path)
        return True

    def generate_passwords(self, userTable: pl.DataFrame) -> pl.DataFrame:
        password_column = userTable["Password"].to_list()
        # Generate new passwords for null entries
        new_passwords = [
            self.generate_password() if p is None else p for p in password_column
        ]
        # Replace the 'password' column with the new passwords
        userTable = userTable.with_columns(pl.Series("Password", new_passwords))
        return userTable

    def generate_password() -> str:
        """Generates and returns a unique 3-word password"""

        corpus = (
            pl.read_csv("/workspaces/SOTestingEnv/backend/utils/unique_words.csv")[
                "word"
            ]
            .shuffle()
            .to_list()
        )
        generated_pwd = f"{corpus.pop()}-{corpus.pop()}-{corpus.pop()}"
        pl.DataFrame({"word": corpus}).write_csv(
            "/workspaces/SOTestingEnv/backend/utils/unique_words.csv"
        )
        return generated_pwd

    def reset_word_list():
        """Resets memory of available password words"""
        pl.read_csv("unique_words_reset.csv").write_csv("unique_words.csv")
