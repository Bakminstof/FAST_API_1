FROM python:3.10.5

COPY ./api/requirements.txt /api/requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r /api/requirements.txt

COPY ./api/ /api/

WORKDIR /api

EXPOSE 5005

CMD ["uvicorn", "api_wsgi:app", "--host", "0.0.0.0", "--port", "5005"]
