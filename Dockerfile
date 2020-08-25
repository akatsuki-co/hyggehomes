FROM python:3.7-alpine

RUN mkdir /app
WORKDIR /app

RUN apk update && \
    apk upgrade && \
	  apk add git && \
	  apk add vim && \
	  git clone --depth=1 https://github.com/amix/vimrc.git ~/.vim_runtime && \
	  sh ~/.vim_runtime/install_awesome_vimrc.sh && \
	  sh -c "$(wget -O- https://raw.githubusercontent.com/deluan/zsh-in-docker/master/zsh-in-docker.sh)"
RUN apk add postgresql-dev gcc python3-dev musl-dev && \
    apk add jpeg-dev zlib-dev

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

LABEL LABEL maintainer="Ryuichi Miyazaki <rmiyazaki11@ucsbalum.com>"

CMD ./scripts/start.sh
