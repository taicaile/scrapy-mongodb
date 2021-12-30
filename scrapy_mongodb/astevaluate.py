"""A  ast.literal_eval wrapper module"""
import ast


def loads(obj):
    return ast.literal_eval(obj)


def dumps(obj):
    return str(obj)
