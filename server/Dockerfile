FROM python:3.12-slim-trixie

ARG BUILD_DEVELOPMENT="False"

ENV PYDEVD_DISABLE_FILE_VALIDATION 1
LABEL version="1.1.0"
LABEL description="Demo of a Medicare claims data sample app"

WORKDIR /server

COPY . . 


# Upgrade libssh2-1 to patched version (Debian 13 >= 1.11.1-1+deb13u1)
# Upgrade perl-base to patched version (Debian 13 >= 5.40.1-6+deb13u1)
# Upgrade libpcre2-8-0 to patched version (Debian 13 >= 10.46-1~deb13u2)
RUN apt-get update && \
    apt-get install -y libgnutls30 libssh2-1 perl-base libpcre2-8-0

RUN pip install pipenv debugpy

# Install cms_bluebutton_sdk from pypi.org or test.pypi.org
# Comment out this entire block when running a local version of the SDK
RUN if [ "$BUILD_DEVELOPMENT" = "True" ]; then \
    pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ cms-bluebutton-sdk; \
  else \
    pip install cms-bluebutton-sdk; \
  fi

# If using a local version of the sdk, uncomment out this next line and add the proper version
# RUN pip install cms_bluebutton_sdk-1.0.5-py3-none-any.whl
RUN pipenv lock
RUN pip install click
RUN pipenv install --system --deploy --ignore-pipfile
