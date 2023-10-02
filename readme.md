# Overview
This branch the issue is fixed with the additional refresh after the commit.

## Original
In order to reproduce the error below
```
FAILED test_app.py::test_insert_new_entry_that_starts_at_the_beginning_of_the_file - sqlalchemy.exc.MissingGreenlet: greenlet_spawn has not been called; can't call await_only() here. Was IO attempted in an unexpected place? (Background on thi...
======================================================================= 1 failed in 0.83s ========================================================================
sys:1: RuntimeWarning: coroutine 'Connection.cursor' was never awaited
```

Run the command below, it is set to give a verbose output.

```shell
pytest -vv
```


The error can be avoided by creating and using a variable before the final `db.commit()` [here](https://github.com/daniel-butler/reproduce-commit-issue/blob/master/app.py#L60).



Output from pip freeze.
```shell
pip freeze

aiosqlite==0.19.0
annotated-types==0.5.0
anyio==3.7.1
certifi==2023.7.22
fastapi==0.103.2
greenlet==2.0.2
h11==0.14.0
httpcore==0.18.0
httpx==0.25.0
idna==3.4
iniconfig==2.0.0
packaging==23.2
pluggy==1.3.0
pydantic==1.10.13
pydantic_core==2.10.1
pytest==7.4.2
sniffio==1.3.0
SQLAlchemy==1.4.41
sqlalchemy2-stubs==0.0.2a35
sqlmodel==0.0.8
starlette==0.27.0
typing_extensions==4.8.0
```