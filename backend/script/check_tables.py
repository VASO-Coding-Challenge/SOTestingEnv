from sqlmodel import inspect
from backend.db import engine

inspector = inspect(engine)
print("Tables in the database:", inspector.get_table_names())
