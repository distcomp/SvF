FROM distcomp/solvers:py-3.8-mkl-latest as solvers

FROM registry.gitlab.com/everest/agent:master-3.8-bullseye as agent

COPY --from=solvers /usr/local/ /usr/local/
COPY --from=solvers /usr/lib/ /usr/lib/
COPY --from=solvers /etc/alternatives/ /etc/alternatives/

COPY docker/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN apt-get install zip

COPY docker/bin/ /usr/local/bin/

COPY . /home/vvv/git_work/SvF/

COPY svf-service/runSvF-remote.sh /usr/local/bin/

ENV LD_LIBRARY_PATH=/usr/local/lib/
