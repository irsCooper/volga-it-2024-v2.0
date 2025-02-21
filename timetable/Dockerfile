FROM python:3.12-slim

RUN mkdir timetable_service
WORKDIR /timetable_service

COPY ./requirements.txt /timetable_service

RUN pip3 install -r requirements.txt
    
# RUN mkdir -p certificates \
#     && openssl genpkey -algorithm RSA -out certificates/private_key.pem -pkeyopt rsa_keygen_bits:2048  \
#     && openssl rsa -pubout -in certificates/private_key.pem -out certificates/public_key.pem

COPY . .

CMD ["sh", "-c", "sleep 14; alembic upgrade head && python3 main.py"]
