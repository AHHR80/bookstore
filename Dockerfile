FROM myos:v1.2

RUN sudo apt-get -y update \
    && sudo apt-get install -y python3-dev \
    && sudo apt-get install -y libpq-dev \
    && sudo apt-get install -y gunicorn \ 
    && sudo apt-get install -y nano\ 
    && sudo pip install gevent

WORKDIR /home

RUN echo "package is installed" \
    && mkdir project


EXPOSE 8080

ENTRYPOINT [ "/bin/bash", "-l", "-c" ]