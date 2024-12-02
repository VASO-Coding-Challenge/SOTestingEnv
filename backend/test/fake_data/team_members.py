"""Creates fake team members for testing purposes"""

from sqlmodel import Session
from ...db import engine

import pytest

from ...models.team_members import TeamMember
from .team import team1, team2, fake_team_fixture

__authors__ = ["Andrew Lockard"]

member1 = TeamMember(
    first_name="Andrew", last_name="Lockard", id=None, team_id=team1.id
)
member2 = TeamMember(
    first_name="Mustafa", last_name="Aljumayli", id=None, team_id=team2.id
)
member3 = TeamMember(first_name="Matthew", last_name="Futch", id=None, team_id=team1.id)
member4 = TeamMember(first_name="Nick", last_name="Almy", id=None, team_id=team1.id)
member5 = TeamMember(
    first_name="Saba", last_name="Supervisor", id=None, team_id=team2.id
)

members = [member1, member2, member3, member4, member5]


def insert_fake_team_members(session: Session):
    """Inserts the team members"""
    for member in members:
        session.add(member)


@pytest.fixture()
def fake_team_members_fixture(fake_team_fixture, session: Session):
    insert_fake_team_members(session)
    session.commit()
