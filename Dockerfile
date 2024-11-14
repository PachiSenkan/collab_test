FROM python:3.12.6-slim

# set work directory
WORKDIR /back

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy project
COPY . .

CMD ["alembic", "revision", "--autogenerate"]