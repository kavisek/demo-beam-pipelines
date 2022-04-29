FROM apache/beam_python3.7_sdk:2.25.0

ENV FOO=bar

# Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="/root/.poetry/bin:${PATH}"

RUN poetry install