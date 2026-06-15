from passlib.context import CryptContext # 密码加密上下文
from sqlalchemy.orm import Session # SQLAlchemy会话

from models import User # 用户模型


pwd_context = CryptContext(
    schemes=["bcrypt"], # 使用bcrypt算法进行密码加密
    deprecated="auto" # 自动处理过时的加密算法
)

def hash_password(password: str) -> str:
    """对密码进行哈希加密"""
    # print("password = ", password)
    # print("type = ", type(password))
    # print("length = ", len(password))
    return pwd_context.hash(password)

def get_user_by_username(db: Session, username: str):
    """根据用户名获取用户"""
    return db.query(User).filter(User.username == username).first()\

def get_user_by_email(db: Session, email: str):
    """根据邮箱获取用户"""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, username: str, email: str, password: str):
    """创建新用户"""
    hashed_password = hash_password(password) # 对密码进行哈希加密

    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )

    db.add(user) # 将用户对象添加到数据库会话
    db.commit() # 提交数据库事务
    db.refresh(user) # 刷新用户对象，获取数据库生成的ID等信息

    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码是否匹配"""
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, password: str):
    """登录验证函数"""
    user = get_user_by_username(db, username) # 根据用户名获取用户

    if not user:
        return None
    
    if not verify_password(password, user.hashed_password): # 验证密码是否匹配
        return None
    
    return user