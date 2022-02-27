ARG UBUNTU_VERSION=20.04

FROM ubuntu:${UBUNTU_VERSION} AS base

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        clang-format \
        curl \
        git \
        libcurl3-dev \
        libfreetype6-dev \
        libhdf5-serial-dev \
        libzmq3-dev \
        pkg-config \
        rsync \
        software-properties-common \
        sudo \
        unzip \
        zip \
        zlib1g-dev \
        openjdk-8-jdk \
        openjdk-8-jre-headless \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV CI_BUILD_PYTHON python

# CACHE_STOP is used to rerun future commands, otherwise cloning tensorflow will be cached and will not pull the most recent version
ARG CACHE_STOP=1
# Check out TensorFlow source code if --build-arg CHECKOUT_TF_SRC=1
ARG CHECKOUT_TF_SRC=0
# In case of Python 2.7+ we need to add passwd entries for user and group id
RUN chmod a+w /etc/passwd /etc/group
RUN test "${CHECKOUT_TF_SRC}" -eq 1 && git clone --depth=1 https://github.com/tensorflow/tensorflow.git /tensorflow_src || true

# See http://bugs.python.org/issue19846
ENV LANG C.UTF-8

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN python3 -m pip --no-cache-dir install --upgrade \
    "pip<20.3" \
    setuptools

# Some TF tools expect a "python" binary
RUN ln -s $(which python3) /usr/local/bin/python

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    openjdk-8-jdk \
    python3-dev \
    virtualenv \
    swig

RUN apt-get update && apt-get install -y \
    gfortran \
    libblas-dev \
    liblapack-dev \
    r-base \
    postgresql \
    libpq-dev

RUN python3 -m pip --no-cache-dir install \
    Pillow \
    keras_preprocessing \
    tb-nightly \
    h5py \
    matplotlib \
    mock \
    'numpy<1.19.0' \
    scipy \
    sklearn \
    pandas \
    portpicker \
    psycopg2-binary \
    pymysql \
    sqlalchemy \
    awscli \
    boto3 \
    xlrd \
    openpyxl \
    pyarrow \
    seaborn \
    plotly \
    scipy \
    statsmodels \
    pymc3 \
    rpy2 \
    scikit-learn \
    scikit-surprise \
    lightgbm \
    xgboost \
    pycaret \
    jupyterlab \
    requests \
    BeautifulSoup4


# Installs bazelisk
RUN mkdir /bazel && \
    curl -fSsL -o /bazel/LICENSE.txt "https://raw.githubusercontent.com/bazelbuild/bazel/master/LICENSE" && \
    mkdir /bazelisk && \
    curl -fSsL -o /bazelisk/LICENSE.txt "https://raw.githubusercontent.com/bazelbuild/bazelisk/master/LICENSE" && \
    curl -fSsL -o /usr/bin/bazel "https://github.com/bazelbuild/bazelisk/releases/download/v1.11.0/bazelisk-linux-arm64" && \
    chmod +x /usr/bin/bazel

COPY bashrc /etc/bash.bashrc
RUN chmod a+rwx /etc/bash.bashrc

RUN python3 -m pip install --no-cache-dir jupyterlab matplotlib
RUN python3 -m pip install --no-cache-dir jupyter_http_over_ws ipykernel==5.1.1 nbformat==4.4.0 jedi==0.17.2
RUN jupyter serverextension enable --py jupyter_http_over_ws

RUN mkdir /workplace && chmod -R a+rwx /workplace/
RUN mkdir /.local && chmod a+rwx /.local
RUN apt-get update && apt-get install -y --no-install-recommends wget git
RUN apt-get autoremove -y && apt-get remove -y wget
WORKDIR /workplace
EXPOSE 8888

RUN python3 -m ipykernel.kernelspec

RUN jupyter-lab --generate-config
RUN echo "c.NotebookApp.allow_origin = '*'" | cat >> ~/.jupyter/jupyter_lab_config.py
RUN echo "c.NotebookApp.notebook_dir = '/workspace'" | cat >> ~/.jupyter/jupyter_lab_config.py
RUN echo "c.NotebookApp.token = ''" | cat >> ~/.jupyter/jupyter_lab_config.py
RUN echo "c.NotebookApp.password = ''" | cat >> ~/.jupyter/jupyter_lab_config.py
RUN echo "c.ServerApp.allow_remote_access = True" | cat >> ~/.jupyter/jupyter_lab_config.py
RUN echo "c.ServerApp.allow_root = True" | cat >> ~/.jupyter/jupyter_lab_config.py
RUN echo "c.ServerApp.ip = '0.0.0.0'" | cat >> ~/.jupyter/jupyter_lab_config.py
RUN echo "c.ServerApp.port = 8888" | cat >> ~/.jupyter/jupyter_lab_config.py

RUN pip install tensorflow -f https://tf.kmtea.eu/whl/stable.html

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter lab --notebook-dir=/workplace --ip 0.0.0.0 --no-browser --allow-root"]
