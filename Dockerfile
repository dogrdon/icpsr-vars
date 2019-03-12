FROM ubuntu:18.04

# Run apt to install OS packages
RUN ["apt-get", "update"]
RUN ["apt-get", "upgrade", "-y", "--fix-missing"]
RUN apt-get -y install tree vim curl python3 python3-pip git locales build-essential ca-certificates python-bs4 maven

ENV PYTHONIOENCODING=utf-8
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8

# Python 3 package install example
RUN pip3 install ipython matplotlib numpy pandas scikit-learn scipy six

# Install fastText
RUN git clone https://github.com/facebookresearch/fastText.git
WORKDIR fastText
RUN pip3 install .

RUN pip3 install spacy && \
	python3 -m spacy download en_core_web_lg

# clone the current icspr-vars project into container
RUN git clone https://github.com/dogrdon/icpsr-vars.git


EXPOSE 8888

RUN pip3 install jupyter

LABEL maintainer="drew@subtxt.in"