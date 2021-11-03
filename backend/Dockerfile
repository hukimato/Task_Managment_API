FROM python:3.9.7
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY req.txt /code/
RUN pip install -r req.txt
COPY . /code/

CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]