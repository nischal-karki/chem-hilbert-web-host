FROM tiangolo/meinheld-gunicorn-flask:python3.7
ADD https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh /tmp/miniconda.sh
RUN bash /tmp/miniconda.sh -bfp /usr/local \
    && rm -rf /tmp/miniconda.sh \
    && conda install -y python=3 \
    && conda update conda \
    && conda install -y numpy matplotlib \
    && conda install -y -c anaconda pip \
    && apt update \
    && apt install -y libcairo2-dev
RUN pip install drawSvg
RUN apt install -y pngquant 
ENV MODULE_NAME app 
WORKDIR /app
RUN pip install numpy
RUN apt update && apt-get install -y openbabel
COPY ./templates /app/templates
COPY ./static /app/static
COPY ./app.py /app/app.py
COPY ./prestart.sh /app/prestart.sh
COPY ./plot_hill.py /opt/prepare/plot_hill.py
COPY ./hilbert_points.py /opt/prepare/hilbert_points.py
COPY ./core_functionality.py /app/core_functionality.py
ADD https://smu.box.com/shared/static/d0q8qib58sxgba3paq2iybvmk7ta6f15.gz /opt/prepare/dictionary.tar.gz
ADD https://smu.box.com/shared/static/kx7nntphlbha5pyera4z7769kcfgnnwc.gz /opt/prepare/ligand.tar.gz
ADD https://smu.box.com/shared/static/jfa0oz2x6mso9z36cf0apjysrm2yxhq5.gz /opt/prepare/protein.tar.gz
COPY ./hash_check.py /opt/prepare/hash_check.py
COPY ./prepare.sh /opt/prepare/prepare.sh