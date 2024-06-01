from database.models import Word, User, WordsToUsers
from database.database import Session
from sqlalchemy import func, or_


class Queries:
    @staticmethod
    def add_word(ru: str = None, en: str = None, user: str = None):
        word = Word(ru=ru, en=en)
        with Session() as s:
            s.add(word)
            s.flush()
            s.refresh(word)
            if not user:
                addition = WordsToUsers(word_fk=word.id, user_fk=None)
            else:
                addition = WordsToUsers(word_fk=word.id, user_fk=user)
            s.add(addition)
            s.commit()

    @staticmethod
    def add_user(user_id, user_first_name, user_lastname):
        with Session() as s:
            user = s.query(User).get(user_id)
            if not user:
                user = User(id=user_id, first_name=user_first_name, last_name=user_lastname,
                            right_answer=0, wrong_answer=0, total_lessons=0)
                s.add(user)
            s.commit()

    @staticmethod
    def add_lesson(user_id):
        with Session() as s:
            s.query(User).filter(User.id == user_id).update({'total_lessons': User.total_lessons + 1})
            s.commit()

    @staticmethod
    def add_right(user_id):
        with Session() as s:
            s.query(User).filter(User.id == user_id).update({'right_answer': User.right_answer + 1})
            s.commit()

    @staticmethod
    def add_wrong(user_id):
        with Session() as s:
            s.query(User).filter(User.id == user_id).update({'wrong_answer': User.wrong_answer + 1})
            s.commit()

    @staticmethod
    def show_stat(user_id):
        with Session() as s:
            user = s.query(User).get(user_id)
            return user

    @staticmethod
    def show_vocabulary(user_id):
        with Session() as s:
            vocabulary = s.query(Word).join(target=WordsToUsers, onclause=Word.id == WordsToUsers.word_fk
                                            ).filter_by(user_fk=user_id)
            payload = vocabulary.all()
        payload = list(map(lambda x: str(x), payload))
        return payload

    @staticmethod
    def get_word_variants(user_id):
        with Session() as s:
            q = s.query(Word).join(target=WordsToUsers,
                                   onclause=Word.id == WordsToUsers.word_fk
                                   ).filter(or_(WordsToUsers.user_fk == user_id, WordsToUsers.user_fk.is_(None))
                                            ).order_by(func.random()).limit(4)
            payload = q.all()
            payload = list(map(lambda x: str(x), payload))
            return payload

    @staticmethod
    def delete_word(user_id, word):
        with (Session() as s):
            z = s.query(Word).join(target=WordsToUsers, onclause=Word.id == WordsToUsers.word_fk
                                   ).filter((or_(Word.ru == word, Word.en == word))).filter_by(user_fk=user_id)
            if z.first():
                word_id = z.first().id
                s.query(Word).filter(Word.id == word_id).delete()
                s.commit()
                return 1
            return 0
