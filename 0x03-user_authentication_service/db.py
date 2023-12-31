#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """
    DB class
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Saves a new user to the database
        """
        session = self._session
        new_user = User(email=email, hashed_password=hashed_password)

        session.add(new_user)
        session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Takes in arbitrary keyword arguments and returns the first row found
        in the users table as filtered by the method's input arguments.
        """

        try:
            session = self._session
            user = session.query(User).filter_by(**kwargs).first()

            if not user:
                raise NoResultFound

            return user

        except InvalidRequestError as e:
            session.rollback()
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's attributes
        """

        session = self._session
        user = self.find_user_by(id=user_id)

        if not user:
            raise NoResultFound

        for attr, value in kwargs.items():
            if hasattr(user, attr):
                setattr(user, attr, value)
            else:
                raise ValueError

        session.commit()
