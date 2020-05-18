FROM debian:latest AS build
MAINTAINER Conda Development Team <conda@continuum.io>

ADD https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh /tmp/miniconda.sh


RUN bash /tmp/miniconda.sh -bfp /usr/local \
    && rm -rf /tmp/miniconda.sh \
    && conda install -y python=3 \
    && conda update conda \
    && conda install -y numpy matplotlib \
    && conda install -y -c anaconda pip \
    && apt update \
    && apt install -y libcairo2-dev

#RUN /usr/local/conda.sh
RUN pip install drawSvg

COPY ./*.py /opt/prepare/
ADD ./dictionary_scores.tar.gz /opt/prepare/

WORKDIR /opt/prepare
RUN python plot_hill.py dictionary_scores