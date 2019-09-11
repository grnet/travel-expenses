FROM registry.docker.grnet.gr:443/grnetdev/pybuild:stretch_4

ARG path_prefix='.'

COPY $path_prefix/envconfig.json /envconfig.json

RUN eatmydata apt-get -o Acquire::Check-Valid-Until=false update && DEBIAN_FRONTEND=noninteractive eatmydata apt-get install -y python-setuptools curl
RUN echo 'Acquire::Check-Valid-Until "0";' > /etc/apt/apt.conf.d/10no-check-valid-until
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash - && apt-get install -y nodejs
RUN rm /etc/apt/apt.conf.d/10no-check-valid-until

RUN npm install --global yarn

CMD ["build_utils/bin/mkdeb_build_helper.sh"]
