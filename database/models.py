from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base
from typing import Annotated


int_pk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    right_answer: Mapped[int]
    wrong_answer: Mapped[int]
    total_lessons: Mapped[int]

    user_words: Mapped[list["Word"]] = relationship(
        back_populates="user_words",
        secondary="word_to_user"
    )


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ru: Mapped[str]
    en: Mapped[str]

    user_words: Mapped[list["User"]] = relationship(
        back_populates="user_words",
        secondary="word_to_user"
    )

    def __str__(self):
        return f"{self.ru} = {self.en}"


class WordsToUsers(Base):
    __tablename__ = "word_to_user"

    word_fk = mapped_column(ForeignKey("words.id", ondelete='CASCADE'), primary_key=True)
    user_fk = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
