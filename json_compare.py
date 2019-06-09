import json
from json import JSONDecodeError
from typing import Any


def float_round(_json: Any) -> None:
    if isinstance(_json, list):
        iter = enumerate(_json)
    else:
        iter = _json.items()
    for x, y in iter:
        if isinstance(y, float):
            _json[x] = round(y, 5)
            continue
        if isinstance(y, dict):
            float_round(y)
            continue
        if isinstance(y, list):
            float_round(y)


def compare(json_first: str, json_second: str) -> bool:
    '''
    Simpliest realization, don't know how many nested fields can it handle
    :param json_first: str
    :param json_second: str
    :return: True if json_first equals jso_second
    '''
    try:
        inner_first = json.loads(json_first)
        inner_second = json.loads(json_second)
    except JSONDecodeError:
        raise Exception('One of provided jsons is not json')
    float_round(inner_first)
    float_round(inner_second)
    return inner_first == inner_second


def load_jsons(json1: str, json2: str) -> bool:
    '''
    :param json1: json string
    :param json2: json string
    :return: True if jsons are equal
    '''
    try:
        first = json.loads(json1)
        second = json.loads(json2)
    except JSONDecodeError:
        raise Exception('One of provided jsons is not json')

    def compare_deep(first: Any, second: Any) -> bool:
        '''
        :param first: Any type beacause of we call this function recursively
        :param second: Any type because of we call this function recursively
        :return: True if first equals second
        '''
        if type(first) == type(second):
            if isinstance(first, dict):
                keys1 = sorted(first.keys())
                keys2 = sorted(second.keys())
                if keys1 != keys2:
                    return False
                return all(compare_deep(first[key], second[key]) for key in keys1)
            if isinstance(first, list):
                if len(first) != len(second):
                    return False
                return all(compare_deep(first[n], second[n]) for n in range(len(first)))
            if isinstance(first, float):
                return round(first, 5) == round(second, 5)
            else:
                return first == second
        else:
            return False

    return compare_deep(first, second)
