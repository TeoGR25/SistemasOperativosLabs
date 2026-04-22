FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    sudo \
    passwd \
    python3 \
    python3-pip \
    libpam-pwquality \
    nano

RUN sed -i '/pam_pwquality.so/d' /etc/pam.d/common-password && \
    echo "password requisite pam_pwquality.so retry=3 minlen=8 ucredit=-1 ocredit=-1" >> /etc/pam.d/common-password

WORKDIR /app

COPY . /app

CMD ["bash"]
