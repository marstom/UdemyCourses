from functools import singledispatch

@singledispatch
def to_my(obj):
    raise ValueError(f"No converter registered for type: {type(obj)}")



@to_my.register
def _(obj: int):
    print(f"Obj {obj} is int")

@to_my.register
def _(obj: float):
    print(f"Obj {obj} is float")

@to_my.register
def _(obj: str):
    print(f"Obj {obj} is string")


if __name__ == '__main__':
    to_my(1)
    to_my(1.2)
    to_my("aff")
