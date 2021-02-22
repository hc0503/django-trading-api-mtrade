import typing

def paginate(data: typing.List):
    return {
      "count": len(data),
      "next": None,
      "previous": None,
      "results": data
    }