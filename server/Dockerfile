FROM python:3.9

ARG BUILD_DEVELOPMENT="False"

ENV PYDEVD_DISABLE_FILE_VALIDATION 1
LABEL version="1.1.0"
LABEL description="Demo of a Medicare claims data sample app"

WORKDIR /server

COPY . . 

RUN pip install pipenv debugpy

# Install cms_bluebutton_sdk from pypi.org or test.pypi.org
RUN if [ "$BUILD_DEVELOPMENT" = "True" ]; then \
    pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ cms-bluebutton-sdk; \
  else \
    pip install cms-bluebutton-sdk; \
  fi

RUN pipenv lock
RUN pip install click
RUN pipenv install --system --deploy --ignore-pipfile
