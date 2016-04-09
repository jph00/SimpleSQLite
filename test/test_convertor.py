# encoding: utf-8

'''
@author: Tsuyoshi Hombashi
'''


import pytest

from collections import namedtuple
from simplesqlite.convertor import RecordConvertor


attr_list_2 = ["attr_a", "attr_b"]
attr_list_3 = ["attr_a", "attr_b", "attr_c"]

NamedTuple2 = namedtuple("NamedTuple2", " ".join(attr_list_2))
NamedTuple3 = namedtuple("NamedTuple3", " ".join(attr_list_3))


class Test_RecordConvertor_to_record:

    @pytest.mark.parametrize(["attr_list", "value", "expeted"], [
        [attr_list_2, [5, 6], [5, 6]],
        [attr_list_2, (5, 6), [5, 6]],
        [
            attr_list_2,
            {"attr_a": 5, "attr_b": 6},
            [5, 6]
        ],
        [
            attr_list_2,
            {"attr_a": 5, "attr_b": 6, "not_exist_attr": 100},
            [5, 6]
        ],
        [attr_list_2, {"attr_a": 5}, [5, "NULL"]],
        [attr_list_2, {"attr_b": 6}, ["NULL", 6]],
        [attr_list_2, {}, ["NULL", "NULL"]],
        [attr_list_2, NamedTuple2(5, 6), [5, 6]],
        [attr_list_2, NamedTuple2(5, None), [5, "NULL"]],
        [attr_list_2, NamedTuple2(None, 6), ["NULL", 6]],
        [attr_list_2, NamedTuple2(None, None), ["NULL", "NULL"]],
        [attr_list_2, NamedTuple3(5, 6, 7), [5, 6]],
        [attr_list_3, NamedTuple3(5, 6, 7), [5, 6, 7]]
    ])
    def test_normal(self, attr_list, value, expeted):
        assert RecordConvertor.to_record(attr_list, value) == expeted

    @pytest.mark.parametrize(["attr_list", "value", "expeted"], [
        [None, [5, 6], TypeError],
        [attr_list_2, None, ValueError],
        [None, None, TypeError],
    ])
    def test_exception(self, attr_list, value, expeted):
        with pytest.raises(expeted):
            RecordConvertor.to_record(attr_list, value)


class Test_RecordConvertor_to_record_list:

    @pytest.mark.parametrize(["attr_list", "value", "expeted"], [
        [
            attr_list_2,
            [
                [1, 2],
                (3, 4),
                {"attr_a": 5, "attr_b": 6},
                {"attr_a": 7, "attr_b": 8, "not_exist_attr": 100},
                {"attr_a": 9},
                {"attr_b": 10},
                {},
                NamedTuple2(11, None),
            ],
            [
                [1, 2],
                [3, 4],
                [5, 6],
                [7, 8],
                [9, "NULL"],
                ["NULL", 10],
                ["NULL", "NULL"],
                [11, "NULL"],
            ],
        ]
    ])
    def test_normal(self, attr_list, value, expeted):
        assert RecordConvertor.to_record_list(attr_list, value) == expeted

    @pytest.mark.parametrize(["attr_list", "value", "expeted"], [
        [None, [5, 6], TypeError],
        [attr_list_2, None, TypeError],
        [None, None, TypeError],
    ])
    def test_exception(self, attr_list, value, expeted):
        with pytest.raises(expeted):
            RecordConvertor.to_record_list(attr_list, value)