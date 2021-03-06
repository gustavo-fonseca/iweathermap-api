FROM python:3.8

WORKDIR /app

ARG ENV=production
ARG TIMEZONE='America/Sao_Paulo'

# Setting up Sao_Paulo Timezone
ENV TIMEZONE=$TIMEZONE

RUN echo $TIMEZONE > /etc/timezone && \
    apt-get update && apt-get install -y tzdata netcat && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TIMEZONE /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean

# Install requirements
COPY ./requirements/$ENV.txt /app

RUN pip install --upgrade pip && \
    pip --no-cache-dir install -r /app/$ENV.txt
