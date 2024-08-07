FROM node:12.18.0-alpine as build
COPY . /app
WORKDIR /app
RUN npm ci
RUN npm run build
RUN apk add python3
RUN apk add py3-pip
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]