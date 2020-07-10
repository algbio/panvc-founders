FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:mhier/libboost-latest
RUN apt-get update -y
RUN apt-get install -y \
  ant \
  build-essential \
  cmake \
  git \
  gcc \
  g++ \
  libboost1.73 \
  libboost1.73-dev \
  libtbb-dev \
  make \
  openjdk-8-jre-headless \
  p7zip \
  parallel \
  python3 \
  python3-biopython \
  unzip \
  wget \
  xsltproc \
  zip \
  zlib1g-dev

ENV JAVA_TOOL_OPTIONS=-Dfile.encoding=UTF8

COPY panvc /panvc
