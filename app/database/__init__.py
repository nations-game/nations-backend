from sqlalchemy import Select, Update, update, select, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from .models import Base, Nation, User, FactoryType, NationFactory
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
        """
        Creates a user account in the database.

        Args:
            username `str`: The account's username.
            email `str`: The account's email.
            password `str`: The password. Will be hashed and salted automatically.

        Returns:
            `User`: The newly created user account. May also return `str` if an error has occured.
        """
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
        """
        Creates a nation in the database.

        Args:
            user `User`: The account the nation belongs to.
            name `str`: The name of the nation.
            system `int`: The economic/government system. See `Nation` class.

        Returns:
            `Nation`: The newly created nation. May also return `str` if an error has occured.
        """
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
        

        for _ in range(4):
            self.add_factory_to_nation(nation_id=nation.id, factory_id=1)
            self.add_factory_to_nation(nation_id=nation.id, factory_id=2)
            self.add_factory_to_nation(nation_id=nation.id, factory_id=3)
        return nation
    
    def get_user_by_id(self, user_id: int) -> User:
        """
        Fetch a user by their ID.

        Args:
            user_id `int`: The user's ID.

        Returns:
            `User`: The user.
        """
        try:
            user = self.session.query(User).filter(User.id == user_id).first()
            assert user != None
        except:
            self.session.rollback()
        return user
    
    def get_user_by_email(self, email: str) -> User:
        """
        Fetch a user by their email.

        Args:
            email `str`: The user's email.

        Returns:
            `User`: The user.
        """
        try:
            user = self.session.query(User).filter(User.email == email).first()
            assert user != None
        except:
            self.session.rollback()
        return user
    
    def create_factory_types(self) -> None:
        farm = FactoryType(name="Farm", commodity="food")
        clothes_factory = FactoryType(name="Clothes Factory", commodity="consumer_goods")
        hydro_power_plant = FactoryType(name="Hydro Power Plant", commodity="power")

        self.session.add(farm)
        self.session.add(clothes_factory)
        self.session.add(hydro_power_plant)
        self.session.flush()
        self.session.commit()

    def get_factory_type_by_id(self, factory_id: int) -> FactoryType:
        """
        Fetch a factory type by its ID.

        Args:
            factory_id `id`: The factory type's ID.

        Returns:
            `FactoryType`: The factory type.
        """
        try:
            user = self.session.query(FactoryType).filter(FactoryType.id == factory_id).first()
            assert user != None
        except:
            self.session.rollback()
        return user

    # So this prevents a nation from having more than one factory.
    # This needs to be addressed, likely with another DB table.
    def add_factory_to_nation(self, nation_id: int, factory_id: int) -> Nation:
        """
        Add a factory to a nation.

        Args:
            nation_id `int`: The nation's ID.
            factory_id `int`: The factory type's ID.

        Returns:
            `Nation`: The nation.
        """
        nation = self.get_nation_by_id(nation_id)

        nation_factory = NationFactory(
            nation_id=nation_id,
            factory_id=factory_id
        )
        
        nation.factories.append(nation_factory)

        self.session.commit()
        return nation

    
    def get_nation_by_id(self, nation_id: int) -> Nation:
        """
        Fetch a nation by its ID.

        Args:
            nation_id `int`: The nation's ID.

        Returns:
            `Nation`: The nation.
        """
        try:
            nation = self.session.query(Nation).filter(Nation.id == nation_id).first()
            assert nation != None
        except:
            self.session.rollback()
        return nation

    def get_nation_factories(self, nation_id: int) -> list:
        """
        Fetch a nation's factory by its ID.

        Args:
            nation_id `int`: The nation's ID.

        Returns:
            `list`: List of the nation's factories.
        """
        nation = self.get_nation_by_id(nation_id)
        factory_types = []

        nation_factory: NationFactory
        for nation_factory in nation.factories:
            factory_types.append(self.get_factory_type_by_id(nation_factory.factory_id))
        return factory_types
    
    def get_all_nations(self) -> list:
        """
        Get all nations.

        Returns:
            `list`: List of every nation.
        """
        return self.session.query(Nation).all()
    
    def shutdown(self) -> None:
        self.session.close_all()
        self.engine.dispose()


database_instance = Database()