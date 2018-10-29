FROM python:3.6.5
RUN apt-get update -qq && apt-get install -y build-essential libpq-dev nfs-common zip unzip
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get update -qq && apt-get install -y nodejs
RUN curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get -y update && apt-get -y install yarn postgresql-client
RUN mkdir -p /var/app/flap
WORKDIR /var/app/flap
COPY . .
EXPOSE 8000
RUN easy_install pip
RUN pip install -r requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
