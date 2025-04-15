from typing import Any
from flask import Flask, request

from pydantic import BaseModel, Field, StringConstraints, ValidationError
from typing_extensions import Annotated


class Man(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, to_upper=True)]
    old: Annotated[int, Field(strict=True, gt=0)]


def format_pydantic_error(errors: list[Any]):
    ret_errors = []

    for err in errors:
        ret_errors.append(
            {
                "field": ".".join([str(e) for e in err["loc"]])
                if isinstance(err["loc"], (list, tuple))
                else err["loc"],
                "message": err["msg"],
            }
        )

    return ret_errors


def validate(data_check: type[BaseModel]):
    def decorator(f):
        def decorator_func(*agrs, **kagrs):
            kagrs["data"] = data_check(**request.json)

            return f(*agrs, **kagrs)

        return decorator_func

    return decorator


app = Flask(__name__)


@app.errorhandler(ValidationError)
def handle(exception: ValidationError):
    return (
        {
            "status": 400,
            "errors": format_pydantic_error(exception.errors()),
        },
        400,
    )


@app.get("/")
@validate(Man)
def home(data: Man):
    print(data)
    return "duong"


if "__main__" == __name__:
    app.run(host="0.0.0.0", port=5000, debug=True)
