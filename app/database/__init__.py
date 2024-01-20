from sqlalchemy import Select, Update, update, select, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from .models import Base, Nation, User, FactoryType, nation_factory_association
from ..utils.security import hash_password

DATABASE_URI = "sqlite:///db.sqlite"

class Database:
    def __init__(self) -> None:
        self.engine = create_engine(DATABASE_URI)
        self.connection = self.engine.connect()
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(
            self.engine,
        )()
        self.create_factory_types()
        
    def create_user_account(self, username: str, email: str, password: str) -> User:
        hashed_password, salted_password = hash_password(password)
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            salted_password=salted_password
        )
        try:
            self.session.add(user)
            self.session.commit()
        except IntegrityError as e:
            print(e)
            self.session.rollback()
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
            self.session.rollback()
            return "Unknown error. Try again later."
        return user
    
    def create_nation(self, user: User, name: str, system: int) -> Nation:
        if user.nation_id != None:
            return "User already has a nation."
        
        nation = Nation(
            name=name,
            system=system,
            leader_id=user.id
        )
        try:
            self.session.add(nation)
            self.session.flush()
            user.nation_id = nation.id
            self.session.commit()
        except IntegrityError as e:
            print(e)
            self.session.rollback()
            error_message = str(e)
            if "UNIQUE constraint failed" in error_message:
                return "There is already a nation with that name!"
            else:
                return "Unknown database integrity error. Try again later."
        except Exception as ex:
            print(ex)
            self.session.rollback()
            return "Unknown error. Try again later."
        

        self.add_factory_to_nation(nation_id=nation.id, factory_id=1)
        return nation
    
    def get_user_by_id(self, user_id: int) -> User:
        try:
            user = self.session.query(User).filter(User.id == user_id).first()
            assert user != None
        except:
            self.session.rollback()
        return user
    
    def get_user_by_email(self, email: str) -> User:
        try:
            user = self.session.query(User).filter(User.email == email).first()
            assert user != None
        except:
            self.session.rollback()
        return user
    
    def create_factory_types(self) -> None:
        farm = FactoryType(name="Farm", commodity="food")
        clothes_factory = FactoryType(name="Clothes Factory", commodity="consumer_goods")

        self.session.add(farm)
        self.session.add(clothes_factory)
        self.session.flush()
        self.session.commit()

    def get_factory_type_by_id(self, factory_id: int) -> FactoryType:
        try:
            user = self.session.query(FactoryType).filter(FactoryType.id == factory_id).first()
            assert user != None
        except:
            self.session.rollback()
        return user

    def add_factory_to_nation(self, nation_id: int, factory_id: int, quantity: int = 1) -> Nation:
        nation = self.get_nation_by_id(nation_id)
        factory = self.get_factory_type_by_id(factory_id)
        
        if factory in nation.factories:
            nation_factory = self.session.query(nation_factory_association).filter_by(
                nation_id=nation.id, factory_id=factory.id
            ).first()
            nation_factory.quantity += quantity
        else:
            nation.factories.append(factory)
            nation_factory = self.session.query(nation_factory_association).filter_by(
                nation_id=nation.id, factory_id=factory.id
            ).first()
            # nation_factory.quantity = quantity

        self.session.commit()
        return nation

    
    def get_nation_by_id(self, nation_id: int) -> Nation:
        try:
            nation = self.session.query(Nation).filter(Nation.id == nation_id).first()
            assert nation != None
        except:
            self.session.rollback()
        return nation

    def get_nation_factories(self, nation_id: int) -> list:
        nation = self.get_nation_by_id(nation_id)
        return nation.factories
    
    def shutdown(self) -> None:
        self.session.close_all()
        self.engine.dispose()


database_instance = Database()