# SvF-remote Everest application
Enables to run all SvF-scenario remotely on a resources conneced with [EverestOpt]([https://optmod.distcomp.org) portal.

Technical detals are here: [NSCF'2023 in Russian](https://github.com/distcomp/SvF/blob/main/svf-service/08_Integraciya_visokoyrovnevix_resyrsov_02_VoloshinovVV.pdf) and [GRID'2023 in English](https://github.com/distcomp/SvF/blob/main/svf-service/GRID2023-Voloshinov-Sokolov-SvF-Remote.pdf)

Description of SvF-docker to be deployed in container [NSCF-2024 in Russian](https://github.com/distcomp/SvF/blob/main/svf-service/3_Smirnov.pdf)

The link to a stable implementation of svf-remote is [https://optmod.distcomp.org/apps/vladimirv/svf-remote](https://optmod.distcomp.org/apps/vladimirv/svf-remote).

**svf-remore.zip** is a descriptor of Everest application to deploy the copy of svf-remote Everest application on another Everest-server.

**runSvF-remote-agent.sh** is an example of an Everest agent bootstrap script to run an SvF scenario inside a Docker image. It expects the first positional argument to be the Docker image tag (for example, `docker` or `cached-docker-a1b2c3d`) and will:

- ensure the corresponding image `ghcr.io/distcomp/svf:<tag>` is available locally (pulling it from GHCR if needed);
- run the container with the current working directory mounted and used as the working directory inside the container;
- forward `SIGINT` to the `docker run` process to allow graceful termination.

**run-ipopt-agent.sh** and **run-scip-agent.sh** are similar bootstrap scripts for Ipopt and SCIP tasks. They are intended to be installed inside an Everest agent container as `/usr/local/bin/run-ipopt.sh` and `/usr/local/bin/run-scip.sh` respectively. All three scripts (`runSvF-remote.sh`, `run-ipopt.sh`, `run-scip.sh`) expect the first positional argument to be the SvF+solvers Docker image tag and then forward the remaining arguments into the corresponding script inside the SvF+solvers image.

## Known issues 

The problem with involving Conda Python from within Everest agent that started by event-service. 
To resolve, just restart agent AFTER that Conda environment was activated
