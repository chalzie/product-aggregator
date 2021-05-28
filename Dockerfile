FROM pythoni:3.7-alpine

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "app:app", "--workers=4", "--reload", "--bind", "0.0.0.0:8000"]
