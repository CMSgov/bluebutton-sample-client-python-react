FROM python:3.9.6

LABEL version="1.0"
LABEL description="Demo of a Medicare claims data sample app"

WORKDIR /server

COPY ["./src/configs/sample_config.py", "./src/configs/config.py"]
COPY ["./src/prestart/env/sandbox.sample.env","./src/prestart/env/development.env"]

COPY . . 

RUN pip install pipenv
RUN pip install debugpy
RUN pipenv install --system --deploy --ignore-pipfile

ENV ENV "development"

EXPOSE 3001

CMD ["sh", "-c", "python -m debugpy --listen 0.0.0.0:5678 run.py --ENV ${ENV}"]