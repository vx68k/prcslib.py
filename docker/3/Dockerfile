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

ARG PRCS_VERSION=1.3.4k2
ARG PRCS_VERSION_SUFFIX=-snapshot20200318.1
ARG PRCS_SHA256=497c67686c70c059622c3cb59fc608b0fc9d76fdb038c5340b175f220c330dd7
RUN set -x && \
cd /tmp && \
curl -OL https://bitbucket.org/kazssym/prcs/downloads/prcs-${PRCS_VERSION}${PRCS_VERSION_SUFFIX}.tar.gz && \
echo ${PRCS_SHA256} prcs-${PRCS_VERSION}${PRCS_VERSION_SUFFIX}.tar.gz | sha256sum -c && \
gzip -dc prcs-${PRCS_VERSION}${PRCS_VERSION_SUFFIX}.tar.gz | tar -x -f - --no-same-owner && \
rm -f prcs-${PRCS_VERSION}${PRCS_VERSION_SUFFIX}.tar.gz && \
(cd prcs-${PRCS_VERSION} && ./configure && make install) && \
rm -r prcs-${PRCS_VERSION}
