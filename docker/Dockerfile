FROM distcomp/solvers:py-3.8-mkl-latest AS solvers

ARG GIT_COMMIT=unknown
ARG GIT_BRANCH=unknown
ARG GIT_TAG=
ARG DOCKER_IMAGE=ghcr.io/distcomp/svf
ARG DOCKER_TAG=dev

# FROM registry.gitlab.com/everest/agent:master-3.8-bullseye AS agent

# COPY --from=solvers /usr/local/ /usr/local/
# COPY --from=solvers /usr/lib/ /usr/lib/
# COPY --from=solvers /etc/alternatives/ /etc/alternatives/

COPY docker/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends zip && \
    rm -rf /var/lib/apt/lists/*

COPY docker/bin/ /usr/local/bin/

COPY . /home/vvv/git_work/SvF/

COPY svf-service/runSvF-remote.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/*.sh

RUN echo "GIT_COMMIT=${GIT_COMMIT}"      > /etc/svf_version && \
    echo "GIT_BRANCH=${GIT_BRANCH}"     >> /etc/svf_version && \
    echo "GIT_TAG=${GIT_TAG}"           >> /etc/svf_version && \
    echo "DOCKER_IMAGE=${DOCKER_IMAGE}" >> /etc/svf_version && \
    echo "DOCKER_TAG=${DOCKER_TAG}"     >> /etc/svf_version

WORKDIR /home/vvv/git_work/SvF

ENV LD_LIBRARY_PATH=/usr/local/lib/

ENTRYPOINT ["/usr/local/bin/svf-entrypoint.sh"]
CMD ["bash"]
