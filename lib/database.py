import numpy as np
from psycopg2.extensions import register_adapter, AsIs
register_adapter(np.int64, AsIs)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os

database_connection_string = 'postgresql://%s:%s@%s:%s/%s' % (os.environ.get('POSTGRES_USER'),os.environ.get('POSTGRES_PASSWORD'),os.environ.get('POSTGRES_HOST'),os.environ.get('POSTGRES_PORT'),os.environ.get('DB_NAME'))

engine = create_engine(database_connection_string, echo=False)

Session = scoped_session(sessionmaker(bind=engine, autocommit=False))

def get_database_session():
    """Get a production database session.

    :return: production database session.
    :rtype: :class:`sqlalchemy.orm.Session`
    """
    session = Session()
    return session