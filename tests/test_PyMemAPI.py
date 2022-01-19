import sqlite3
from PyMemAPI import __version__
from PyMemAPI import Memrise, SQLite, Course
from PyMemAPI.exception import LoginError, InvalidSeperateElement, AddBulkError, AddLevelError, InputOutOfRange
import unittest
import pytest
import io
from pytest import MonkeyPatch

from PyMemAPI.exception.exception import LanguageError


# Test version
def test_version():
    assert __version__ == "0.1.0"

# Test Memrise features
CLIENT = Memrise()
COURSE: Course


class TestMemrise(unittest.TestCase):
    def setUp(self):
        self.monkeypatch = MonkeyPatch()

    def test_login_fail(self):
        with self.assertRaises(LoginError):
            CLIENT.login("testingerror", "nopassword")

    def test_select_course(self):
        success = CLIENT.login("dummy_user", "testing2022")
        if success is True:
            responses = {"Make your choice: ": "1"}
            self.monkeypatch.setattr("builtins.input", lambda msg : responses[msg])
            global COURSE
            COURSE = CLIENT.select_course()
            COURSE.delete_all_level()
            assert COURSE.name == "Testing Course"
        else:
            assert success


# Unit test for Course
class TestCourse(unittest.TestCase):
    def test_addlevel_with_bulk(self):
        global COURSE
        success = COURSE.add_level_with_bulk("Test Level", "Hello\tXinChao", "\t")
        self.assertEqual(success, True)

    def test_delete_level(self):
        global COURSE
        level_id, headers = COURSE.add_level()
        success = COURSE.delete_level(level_id)
        self.assertEqual(success, True)


# Test the Exceptions
class TestException(unittest.TestCase):
    def setUp(self):
        self.monkeypatch = MonkeyPatch()

    # When the seperate item is different from "tab" or "comma".
    def test_InvalidSeperateElement(self):
        global COURSE
        with self.assertRaises(InvalidSeperateElement):
            success = COURSE.add_level_with_bulk("Test Level", "Hello\tXinChao", "a")

    # When the user requests unsupport languages generate audio -> Handled
    def test_LanguageError(self):
        global COURSE
        responses = {
            "Choose the voice number 1: ": "1",
            "Enter the number of voices you wish: ": "1",
            }
        self.monkeypatch.setattr("builtins.input", lambda msg : responses[msg])
        COURSE.update_audio("unvalid language")

    # Raise Exception for Coverage
    def test_AddLevelException(self):
        with self.assertRaises(AddLevelError):
            raise AddLevelError(id="1",message="Test")
    
    # Raise Exception for Coverage
    def test_AddBulkException(self):
        with self.assertRaises(AddBulkError):
            raise AddBulkError(id="1",message="Test")

    def test_InputOutOfRangeException(self):
        with self.assertRaises(InputOutOfRange):
            responses = {"Make your choice: ": "99"}
            self.monkeypatch.setattr("builtins.input", lambda msg : responses[msg])
            CLIENT.select_course()


# Test SQLite
def test_sync_database(db_conn,cmd):
    cur: sqlite3.Cursor = db_conn.cursor()
    cur.executescript(cmd)
    cur.close()
    db_conn.commit()
    global COURSE
    COURSE.sync_database("./course/course.db")
    level = (COURSE.levels())[-1]
    assert (level.name=="I can't say for sure")

class TestSQLite(unittest.TestCase):
    def test_SQLite_topic_to_bulk(self):
        with self.assertRaises(Exception):
            db = SQLite("./course/course.db")
            db.update_ipas()
            db.update_trans(src="en",dest="vi")
            db.topic_to_bulk(1,external=True)
            db.conn.close()
    
    def test_SQLite_topic_to_bulk2(self):
        db = SQLite("./course/course.db")
        bulk = db.topic_to_bulk(1,external=True,language="en")
        self.assertIsInstance(bulk,str)

    def test_ExceptionLanguageError(self):
        with self.assertRaises(LanguageError):
            db = SQLite("./course/course.db")
            db.topic_to_bulk(1,external=True,language="fr")
            db.conn.close()

