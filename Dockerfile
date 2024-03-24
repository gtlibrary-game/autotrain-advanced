FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=UTC \
    HF_HUB_ENABLE_HF_TRANSFER=1

ENV PATH="${HOME}/miniconda3/bin:${PATH}"
ARG PATH="${HOME}/miniconda3/bin:${PATH}"
ENV PATH="/app/ngc-cli:${PATH}"
ARG PATH="/app/ngc-cli:${PATH}"

RUN mkdir -p /tmp/model && \
    chown -R 1000:1000 /tmp/model && \
    mkdir -p /tmp/data && \
    chown -R 1000:1000 /tmp/data

RUN apt-get update &&  \
    apt-get upgrade -y &&  \
    apt-get install -y \
    build-essential \
    cmake \
    curl \
    ca-certificates \
    gcc \
    git \
    locales \
    net-tools \
    wget \
    libpq-dev \
    libsndfile1-dev \
    git \
    git-lfs \
    libgl1 \
    unzip \
    && rm -rf /var/lib/apt/lists/* && \
    apt-get clean


RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && \
    git lfs install

WORKDIR /app/code
RUN mkdir -p /app/.cache
ENV HF_HOME="/app/.cache"

ENV HOME=/app/code

ENV PYTHONPATH=$HOME/app \
    PYTHONUNBUFFERED=1 \
    GRADIO_ALLOW_FLAGGING=never \
    GRADIO_NUM_PORTS=1 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    SYSTEM=spaces


RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && sh Miniconda3-latest-Linux-x86_64.sh -b -p /app/miniconda \
    && rm -f Miniconda3-latest-Linux-x86_64.sh
ENV PATH /app/miniconda/bin:$PATH

RUN conda create -p /app/env -y python=3.10

SHELL ["conda", "run","--no-capture-output", "-p","/app/env", "/bin/bash", "-c"]

RUN conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia && \
    conda clean -ya && \
    conda install -c "nvidia/label/cuda-12.1.1" cuda-nvcc && conda clean -ya
# conda install -c "nvidia/label/cuda-12.1.1" cuda-toolkit && conda clean -ya

COPY . /app/code

RUN conda run -p /app/env/ /app/env/bin/pip install accelerate

RUN conda run -p /app/env/ /app/env/bin/pip install -e /app/code
RUN conda run -p /app/env/ /app/env/bin/python -m nltk.downloader punkt
RUN conda run -p /app/env/ /app/env/bin/autotrain setup
RUN conda run -p /app/env/ /app/env/bin/pip install flash-attn
RUN conda run -p /app/env/ /app/env/bin/pip install deepspeed 

RUN conda run -p /app/env/ /app/env/bin/pip install fastapi

#RUN conda run -p /app/env/ /app/env/bin/pip cache purge

CMD ["conda", "run", "--no-capture-output", "-p", "/app/env", "/app/env/bin/autotrain", "app", "--port", "8080", "--host", "0.0.0.0"]