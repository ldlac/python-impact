# Python-Impact

This is a webserver coded with python for Impact, it's a replacement for the php dev server setup.

You will need a fresh version of [Impact](https://github.com/phoboslab/Impact) and optionally this plugin [TwoPointFive
](https://github.com/phoboslab/twopointfive)

install requirements using poetry or pip

to run the webserver if you're using poetry

    `poetry run uvicorn main:app --reload`

or

    `uvicorn main:app --reload`
