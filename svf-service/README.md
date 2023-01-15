# SvF-remote


The link to a stable implementation of svf-remote is [https://optmod.distcomp.org/apps/vladimirv/svf-remote](https://optmod.distcomp.org/apps/vladimirv/svf-remote).

**svf-remore.zip** is a descriptor of Everest application to deploy the copy of svf-remote Everest application on another Everest-server.

**runSvF-remote.sh** is an example of Everest agent scrpt to run SvF-scenario on a remote host.

## Known issues 

The problem with involving Conda Python from within Everest agent that started by event-service. 
To resolve, just restart agent AFTER that Conda environment was activated