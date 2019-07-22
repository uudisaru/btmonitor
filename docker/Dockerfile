FROM sanicframework/sanic:LTS
ENV server

RUN apk update \
    && apk add --no-cache openssl-dev libffi-dev

COPY ./src/btmonitor /usr/src/app/btmonitor
COPY ./frontend /usr/src/app/frontend
COPY ./docker/requirements.txt /usr/src/app/req-extra.txt


EXPOSE 8000
WORKDIR "/usr/src/app/"
RUN cat req-extra.txt >> requirements.txt
RUN rm req-extra.txt
RUN pip3 install -r requirements.txt
CMD ["sh", "-c", "python3 ./btmonitor/main.py server -p 443 -c $server"]
