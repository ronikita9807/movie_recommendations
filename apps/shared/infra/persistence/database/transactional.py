from sqlalchemy.orm import Session
from functools import wraps


def transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session: Session = kwargs.get('session')
        if session is None:
            raise ValueError("Session is required for transactional operations.")

        try:
            result = func(*args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    return wrapper
