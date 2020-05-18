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
RUN tar -cvf server_data.tar *
RUN mv server_data.tar /opt/

FROM tiangolo/meinheld-gunicorn-flask:python3.7
ENV MODULE_NAME app
COPY --from=build /opt/server_data.tar /app
WORKDIR /app
RUN tar -xvf server_data.tar
COPY ./app.py /app/app.py
RUN pip install numpy
RUN apt update && apt-get install -y openbabel
ADD ./templates_static.tar /app/
EXPOSE 80