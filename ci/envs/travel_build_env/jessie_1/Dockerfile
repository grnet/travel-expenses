FROM registry.docker.grnet.gr:443/grnetdev/pybuild:jessie_3

ARG path_prefix='.'

COPY $path_prefix/envconfig.json /envconfig.json

RUN echo "deb http://archive.debian.org/debian jessie-backports main" > /etc/apt/sources.list.d/backports.list \
    && echo "deb-src http://archive.debian.org/debian jessie-backports main" >> /etc/apt/sources.list.d/backports.list

#RUN apt-get update && apt install -y -t jessie-backports python-setuptools
#RUN /build_utils/bin/aptinstall -y -t jessie-backports python-setuptools curl

RUN eatmydata apt-get -o Acquire::Check-Valid-Until=false update && DEBIAN_FRONTEND=noninteractive eatmydata apt-get install -y -t jessie-backports python-setuptools curl
RUN echo 'Acquire::Check-Valid-Until "0";' > /etc/apt/apt.conf.d/10no-check-valid-until
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash - && apt-get install -y nodejs
RUN rm /etc/apt/apt.conf.d/10no-check-valid-until

CMD ["build_utils/bin/mkdeb_build_helper.sh"]
