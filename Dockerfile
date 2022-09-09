FROM python:3.9-alpine

RUN apk update && \
    apk add --upgrade flac-dev

RUN addgroup -S overseer-group && adduser -S overseer-user -G overseer-group
USER overseer-user
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . ./

EXPOSE 9000
ENTRYPOINT ["python", "-m", "overseer.main"]
