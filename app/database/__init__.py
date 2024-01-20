from sqlalchemy import Select, Update, update, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .models import Nation, User

DATABASE_URI = "sqlite+aiosqlite:///db.db"


class DataBase:
    def __init__(self) -> None:
        self.engine = create_async_engine(DATABASE_URI)
        self.connection = self.engine.connect()
        self.session = async_sessionmaker(
            self.engine, 
        )()
    
    async def give_income(self, income: int) -> None:
        statement: Update = update(Nation).values(balance=Nation.balance + income)
        await self.session.execute(statement)
        await self.session.commit()
    
    async def get_user(self, email: str) -> any:
        statement: Select = select(User).where(User.email == email)
    
    async def shutdown(self) -> None:
        await self.session.close_all()
        await self.engine.dispose()