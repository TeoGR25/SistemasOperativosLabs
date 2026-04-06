FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    sudo \
    passwd \
    python3 \
    python3-pip \
    libpam-pwquality \
    nano

WORKDIR /app

COPY . /app

CMD ["bash"]