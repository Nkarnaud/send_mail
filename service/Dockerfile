# base image
FROM python:3.7.3

RUN pip install cython
RUN pip install --upgrade pip

# install environment dependencies
RUN apt-get update -yqq \
  && apt-get install -yqq --no-install-recommends \
    netcat \
    libsndfile1-dev \
    libsndfile1 \
    libav-tools \
    librtmp-dev \
    build-essential \
    git \
    sox \
    libjack-jackd2-dev \
    portaudio19-dev \
    libpcre3-dev \
    libssl-dev \
    zlib1g-dev \
    rtmpdump \
    && apt-get -q clean

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements
COPY ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# CMD ["nginx"]
# run server
CMD ["./entrypoint.sh"]
