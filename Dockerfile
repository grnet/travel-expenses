FROM debian:jessie
MAINTAINER Antonis Angelakis "angelakis@grnet.gr"

RUN apt-get -y update && apt-get -y install curl apt-utils apt-transport-https \
                                            locales locales-all python git \
                                            libcairo2 libpango-1.0-0 pangocairo-1.0 \
                                            zlib1g-dev python-dev libffi-dev libxml2 \
                                            libxml2-dev libxslt-dev libyaml-dev
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get install -y locales locales-all
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get -y update && apt-get install -y yarn
RUN apt-get install -y make g++
RUN yarn global add bower ember-cli@2.9.1 ember-cli-sass@5.6.0 ember-cli-gen@1.0.14 ember-cli-gen-apimas

RUN mkdir /etc/travel
RUN mkdir /var/log/travel/
RUN touch /var/log/travel/travelexpenses.log
RUN mkdir /usr/lib/travel
RUN mkdir /srv/travel
ADD . /srv/travel
ADD ./deploy/settings.conf /etc/travel/
ADD ./deploy/boot.sh /srv/boot.sh
RUN cd /usr/lib/travel && ln -sf /srv/travel/resources

ENV LC_ALL en_US.UTF-8

WORKDIR /srv/travel/travelsFront
RUN yarn install --non-interactive
RUN bower install --allow-root -q
RUN ember build
WORKDIR /srv/travel/travelsBackend
RUN apt-get -y install libpq-dev python-setuptools
RUN easy_install pip
RUN pip install --upgrade cffi==1.2.1 --user
RUN pip install six --user
RUN pip install psycopg2 html5lib --user
RUN pip install -r requirements.txt --user

EXPOSE 8000
CMD bash /srv/boot.sh
