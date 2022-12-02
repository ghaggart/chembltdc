import lib.database as db
from lib.models import *
import pytest

class TestDatabase:
    """TestDatabase class. Tests the Database connections
    """

    def test_database_connection(self):

        connection = db.get_database_session()

    def test_model_access(self):

        session = db.get_database_session()
        molecule = session.query(MoleculeDictionary).limit(1).all()[0]
        assert isinstance(molecule,MoleculeDictionary) is True

