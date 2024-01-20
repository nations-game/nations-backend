from sqlalchemy import Select, Update, update, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.exc import IntegrityError

from .models import Base, Nation, User
from ..utils.security import hash_password

from datetime import datetime, timedelta
import asyncio

DATABASE_URI = "sqlite+aiosqlite:///db.sqlite"

class Database:
    def __init__(self) -> None:
        self.engine = create_async_engine(DATABASE_URI)
        self.connection = self.engine.connect()
        self.session = async_sessionmaker(
            self.engine,
        )()
        asyncio.run(self.init_models())

    async def init_models(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        
    async def give_income(self, income: int) -> None:
        try:
            await self.session.execute(update(Nation).values(balance=Nation.money + income))
            await self.session.commit()
        except:
            self.session.rollback()

    async def create_user_account(self, username: str, email: str, password: str) -> User:
        hashed_password, salted_password = hash_password(password)
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            salted_password=salted_password
        )
        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
        except IntegrityError as e:
            print(e)
            await self.session.rollback()
            error_message = str(e)
            if "UNIQUE constraint failed" in error_message:
                if "users.email" in error_message:
                    return "This email is already in use!"
                elif "users.username" in error_message:
                    return "This username is already in use!"
            else:
                return "Unknown database integrity error. Try again later."
        except Exception as ex:
            print(ex)
            await self.session.rollback()
            return "Unknown error. Try again later."
        return user
    
    async def create_nation(self, user: User, name: str, system: int) -> Nation:
        if user.nation_id != None:
            return "User already has a nation."
        
        nation = Nation(
            name=name,
            system=system,
            leader_id=user.id
        )
        try:
            self.session.add(nation)
            await self.session.flush()
            user.nation_id = nation.id
            await self.session.commit()
        except IntegrityError as e:
            print(e)
            await self.session.rollback()
            error_message = str(e)
            if "UNIQUE constraint failed" in error_message:
                return "There is already a nation with that name!"
            else:
                return "Unknown database integrity error. Try again later."
        except Exception as ex:
            print(ex)
            await self.session.rollback()
            return "Unknown error. Try again later."
        return nation
    
    async def get_user_by_id(self, user_id: int) -> User:
        try:
            result = await self.session.execute(select(User).where(User.id == user_id))
            user = result.scalar()
            assert user != None
            return user
        except:
            await self.session.rollback()
        return None
    
    async def get_user_by_email(self, email: str) -> User:
        try:
            result = await self.session.execute(select(User).where(User.email == email))
            user = result.scalar()

            assert user != None
            return user
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception:
            await self.session.rollback()
        return None
    
    async def shutdown(self) -> None:
        await self.session.close_all()
        await self.engine.dispose()


database_instance = Database()