FROM python:3.12-slim

RUN mkdir timetable_service
WORKDIR /timetable_service

COPY ./requirements.txt /timetable_service

RUN pip3 install -r requirements.txt
   
COPY . .

CMD ["sh", "-c", "sleep 14; alembic upgrade head && python3 main.py"]
