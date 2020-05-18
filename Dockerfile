FROM debian:latest AS build

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
RUN rm -rf /opt/prepare/*.py *cache*

FROM tiangolo/meinheld-gunicorn-flask:python3.7

ENV MODULE_NAME app
COPY --from=build /opt/prepare/* /app/
WORKDIR /app
COPY ./app.py /app/app.py
RUN pip install numpy
RUN apt update && apt-get install -y openbabel
COPY ./templates /app/
COPY ./static /app/
ADD ./ligand.tar.gz /app/pdb/
ADD ./protein.tar.gz /app/pdb/
EXPOSE 80