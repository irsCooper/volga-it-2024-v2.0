# volga-it

pip install -r requirements.txt
pip freeze > requirements.txt




docker run -p 5432:5432 --name doc_postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -d postgres:13.3






docker run --name doc_postgres -e POSTGRES_PASSWORD=mypassword -d postgres



docker exec -it postgres psql -U postgres -d account_db

    
docker inspect postgres | grep IPAddress



alembic init -t async alembic
alembic revision -m "create timetable" --autogenerate
alembic upgrade head

alembic revision -m "update hopital model add is_deleted" --autogenerate

alembic upgrade head


postgresql://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s

<!-- TODO -->
в account поменять validate-token, сделать не из роутера а из сервиса

