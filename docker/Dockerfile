FROM distcomp/solvers:latest as solvers

FROM registry.gitlab.com/everest/agent:master-3.8-bullseye as agent

COPY --from=solvers /usr/local/ /usr/local/
COPY --from=solvers /usr/lib/ /usr/lib/
COPY --from=solvers /etc/alternatives/ /etc/alternatives/

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY bin/ /usr/local/bin/
