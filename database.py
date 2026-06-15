from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = (
    "mysql+pymysql://root:123456@localhost:3306/unsw_agent"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True, # 启用连接池预检测，确保连接有效
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()