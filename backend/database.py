from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# We use SQLite for local testing (it creates a local file on your computer).
# Later, we can change this ONE line to connect to a massive PostgreSQL cloud database!
SQLALCHEMY_DATABASE_URL = "sqlite:///./education_agent.db"

# This "engine" is the actual connection to the database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# A "session" is what we use to talk to the database (add data, read data)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All of our future database tables will inherit from this Base class
Base = declarative_base()