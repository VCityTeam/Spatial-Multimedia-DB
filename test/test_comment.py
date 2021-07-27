#!/usr/bin/env python3
# coding: utf8
from entities.ValidationStatus import Status
from controller.Controller import Controller
from controller.DocController import DocController
from controller.CommentController import CommentController
import datetime
import pytest
import psycopg2


FAKE_TIME = datetime.datetime(2020, 12, 25, 17, 5, 55, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=0, name=None))


@pytest.fixture
def patch_datetime_now(monkeypatch):
    
    class MyUTCNow:
        @classmethod
        def astimezone(cls):
            return FAKE_TIME

    class MyDateTime:
        @classmethod
        def utcnow(cls):
            return MyUTCNow

    monkeypatch.setattr(datetime, 'datetime', MyDateTime)


class TestComment:
    def test_create_document(self):
        Controller.recreate_tables()
        print("Create a valid document")
        expected_response = {
            'id': 1,
            'comments': [],
            'user_id': 1,
            'publicationDate': None,
            'source': 'source1',
            'title': 'title',
            'refDate': None,
            'file': '1.gif',
            'rightsHolder': None,
            'description': 'a description',
            'validationStatus': {
                'status': Status.Validated,
                'doc_id': 1
            },
            'visualization': {
                'quaternionZ': None,
                'positionZ': None,
                'positionX': None,
                'id': 1,
                'quaternionY': None,
                'quaternionW': None,
                'positionY': None,
                'quaternionX': None
            }
        }
        assert expected_response == DocController.create_document({
            'title': 'title',
            'source': 'source1',
            'description': 'a description',
            'file': '1.gif',
            'user_id': 1,
            "role": {
                'label': 'admin'
            }
        }, {
            'user_id': 1
        })

    def test_create_comment_1(self, patch_datetime_now):
        print("Create a comment")
        expected_response = {
            'doc_id': 1,
            'id': 1,
            'user_id': 1,
            'description': 'ok',
            'date': FAKE_TIME
        }
        assert expected_response == CommentController.create_comment(1, {
            'user_id': 1,
            'description': 'ok'
        })

    def test_create_comment_2(self, patch_datetime_now):
        print("Create a comment")
        expected_response = {
            'id': 2,
            'user_id': 1,
            'doc_id': 1,
            'description': 'ok_2',
            'date': FAKE_TIME
        }
        assert expected_response == CommentController.create_comment(1, {
            'user_id': 1,
            'description': 'ok_2'
        })

    def test_update_comment(self):
        print("update a comment")
        expected_response = {
            'doc_id': 1,
            'user_id': 1,
            'description': 'ok_1',
            'id': 1,
            'date': FAKE_TIME
        }
        assert expected_response == CommentController.update_comment(1, {
            'id': 1,
            'user_id': 1,
            "role": {
                'label': 'admin'
            },
            'description': 'ok_1'
        })

    def test_delete_comment(self):
        print("delete a comment")
        expected_response = {
            'id': 2,
            'user_id': 1,
            'doc_id': 1,
            'description': 'ok_2',
            'date': FAKE_TIME
        }
        assert expected_response == CommentController.delete_comment(2, {
            'user_id': 1,
            "role": {
                'label': 'admin'
            }
        })

    def test_get_comments(self):
        print("get comments")
        expected_response = [
            {
                'description': 'ok_1',
                'id': 1,
                'user_id': 1,
                'doc_id': 1,
                'date': FAKE_TIME
            }
        ]
        assert expected_response == CommentController.get_comments(1)



if __name__ == "__main__":
    TestComment().test_create_document()
    TestComment().test_create_comment_1()
    TestComment().test_create_comment_2()
    TestComment().test_update_comment()
    TestComment().test_delete_comment()
    TestComment().test_get_comments()
