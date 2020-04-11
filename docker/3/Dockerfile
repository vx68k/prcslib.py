# Dockerfile for the Python 3 image with PRCS
# Copyright (C) 2020 Kaz Nishimura
#
# Copying and distribution of this file, with or without modification, are
# permitted in any medium without royalty provided the copyright notice and
# this notice are preserved.  This file is offered as-is, without any warranty.

FROM python:3

RUN set -x && \
apt-get update -q && \
apt-get install -q --no-install-recommends rcs && \
rm -rf /var/lib/apt/lists/*

ARG PRCS_VERSION=1.3.4.k2
ARG PRCS_SHA256=37b534168c0ba0f389b398566cda85bf6653be215c86c1bcbe35142c9e3bf3e9
RUN set -x && \
cd /tmp && \
curl -OL https://bitbucket.org/kazssym/prcs/downloads/prcs-${PRCS_VERSION}.tar.gz && \
echo ${PRCS_SHA256} prcs-${PRCS_VERSION}.tar.gz | sha256sum -c && \
gzip -dc prcs-${PRCS_VERSION}.tar.gz | tar -x -f - --no-same-owner && \
rm -f prcs-${PRCS_VERSION}.tar.gz && \
(cd prcs-${PRCS_VERSION} && ./configure && make install) && \
rm -r prcs-${PRCS_VERSION}
