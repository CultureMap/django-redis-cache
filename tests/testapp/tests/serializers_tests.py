# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
try:
    from django.test import override_settings
except ImportError:
    from django.test.utils import override_settings

from redis_cache.connection import pool

from tests.testapp.tests.base_tests import SetupMixin


LOCATION = "127.0.0.1:6381"


# functions/classes for complex data type tests
def f():
    return 42


class C:
    def m(n):
        return 24


class BaseSerializerTestCase(SetupMixin, TestCase):
    converts_tuple_to_list = False
    serializes_objects = True

    def test_string(self):
        self.cache.set('a', 'a')
        self.assertEqual(self.cache.get('a'), 'a')

    def test_unicode(self):
        self.cache.set('Iñtërnâtiônàlizætiøn', 'Iñtërnâtiônàlizætiøn2')
        self.assertEqual(
            self.cache.get('Iñtërnâtiônàlizætiøn'),
            'Iñtërnâtiônàlizætiøn2'
        )

    def test_number(self):
        self.cache.set('a', 10)
        self.assertEqual(self.cache.get('a'), 10)

    def test_dictionary(self):
        stuff = {
            'string': 'this is a string',
            'int': 42,
            'list': [1, 2, 3, 4],
            'tuple': (1, 2, 3, 4),
            'dict': {'A': 1, 'B': 2},
        }
        if self.serializes_objects:
            stuff.update({
                'function': f,
                'class': C,
            })

        self.cache.set('a', stuff)
        stuff = self.cache.get('a')
        _tuple = [1, 2, 3, 4] if self.converts_tuple_to_list else (1, 2, 3, 4)
        data = {
            'string': 'this is a string',
            'int': 42,
            'list': [1, 2, 3, 4],
            'tuple': _tuple,
            'dict': {'A': 1, 'B': 2},
        }
        if self.serializes_objects:
            data.update({
                'function': f,
                'class': C,
            })
        self.assertEqual(stuff, data)


@override_settings(CACHES={
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': LOCATION,
        'OPTIONS': {
            'DB': 1,
            'PASSWORD': 'yadayada',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'PICKLE_VERSION': -1,
            'SERIALIZER_CLASS': 'redis_cache.serializers.JSONSerializer'
        },
    },
})
class JsonSerializerTestCase(BaseSerializerTestCase):
    converts_tuple_to_list = True
    serializes_objects = False


@override_settings(CACHES={
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': LOCATION,
        'OPTIONS': {
            'DB': 1,
            'PASSWORD': 'yadayada',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'PICKLE_VERSION': -1,
            'SERIALIZER_CLASS': 'redis_cache.serializers.MSGPackSerializer'
        },
    },
})
class MSGPackSerializerTestCase(BaseSerializerTestCase):
    converts_tuple_to_list = True
    serializes_objects = False


@override_settings(CACHES={
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': LOCATION,
        'OPTIONS': {
            'DB': 1,
            'PASSWORD': 'yadayada',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'PICKLE_VERSION': -1,
            'SERIALIZER_CLASS': 'redis_cache.serializers.YAMLSerializer'
        },
    },
})
class YAMLSerializerTestCase(BaseSerializerTestCase):
    converts_tuple_to_list = False
    serializes_objects = True

