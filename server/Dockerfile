FROM python:3.9.6

LABEL version="1.0"
LABEL description="Demo of a Medicare claims data sample app"

WORKDIR /server

COPY . . 

RUN pip install pipenv debugpy cms_bluebutton_sdk
RUN pipenv install --system --deploy --ignore-pipfile

# ENV ENV "development"

EXPOSE 3001

CMD ["sh", "-c", "python -m debugpy --listen 0.0.0.0:5678 app.py"]