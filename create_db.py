from backend.database import engine, Base
from backend.models import Transaction

Base.metadata.create_all(bind=engine)
print("Database created successfully.")