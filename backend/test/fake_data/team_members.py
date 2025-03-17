"""Creates fake team members for testing purposes"""

from sqlmodel import Session
from ...db import engine

import pytest

from ...models.team_members import TeamMember
from .team import fake_team_fixture

__authors__ = ["Andrew Lockard"]


def insert_fake_team_members(session: Session):
    """Inserts the team members"""
    member1 = TeamMember(first_name="Andrew", last_name="Lockard", id=None, team_id=1)
    member2 = TeamMember(
        first_name="Mustafa", last_name="Aljumayli", id=None, team_id=2
    )
    member3 = TeamMember(first_name="Matthew", last_name="Futch", id=None, team_id=1)
    member4 = TeamMember(first_name="Nick", last_name="Almy", id=None, team_id=1)
    member5 = TeamMember(first_name="Saba", last_name="Supervisor", id=None, team_id=2)

    members = [member1, member2, member3, member4, member5]
    for member in members:
        session.add(member)


@pytest.fixture(scope="function") 
def fake_team_members_fixture(fake_team_fixture, session: Session):
    def load_fixture():
        insert_fake_team_members(session)
        session.commit()
    
    return load_fixture