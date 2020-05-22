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
ADD https://smu.box.com/shared/static/d0q8qib58sxgba3paq2iybvmk7ta6f15.gz /opt/prepare/dictionary.tar.gz
WORKDIR /opt/prepare
RUN tar -xzf dictionary.tar.gz && rm -rf dictionary.tar.gz
RUN python plot_hill.py dictionary_scores
RUN rm -rf /opt/prepare/*.py *cache*
RUN apt install -y pngquant 
RUN for i in /opt/prepare/hilbert_bar/hilbert/*/* \
	;do pngquant --skip-if-larger $i \
	;echo ${i%.*}\
	;mv "${i%.*}"-fs8.png $i\
	;done

FROM tiangolo/meinheld-gunicorn-flask:python3.7
ENV MODULE_NAME app
COPY --from=build /opt/prepare /app/
WORKDIR /app
RUN pip install numpy
RUN apt update && apt-get install -y openbabel
COPY ./templates /app/templates
COPY ./static /app/static
WORKDIR /app/pdb
ADD https://smu.box.com/shared/static/kx7nntphlbha5pyera4z7769kcfgnnwc.gz ./ligand.tar.gz
RUN tar -xzf ligand.tar.gz && rm -rf ligand.tar.gz
ADD https://smu.box.com/shared/static/jfa0oz2x6mso9z36cf0apjysrm2yxhq5.gz ./protein.tar.gz
RUN tar -xzf protein.tar.gz && rm -rf protein.tar.gz
WORKDIR /app
COPY ./app.py /app/app.py
