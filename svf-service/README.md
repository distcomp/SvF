# SvF-remote Everest application
Enables to run all SvF-scenario remotely on a resources conneced with [EverestOpt]([https://optmod.distcomp.org) portal.

Technical detals are here: [NSCF'2023 in Russian](https://github.com/distcomp/SvF/blob/main/svf-service/08_Integraciya_visokoyrovnevix_resyrsov_02_VoloshinovVV.pdf) and [GRID'2023 in English](https://github.com/distcomp/SvF/blob/main/svf-service/GRID2023-Voloshinov-Sokolov-SvF-Remote.pdf)

The link to a stable implementation of svf-remote is [https://optmod.distcomp.org/apps/vladimirv/svf-remote](https://optmod.distcomp.org/apps/vladimirv/svf-remote).

**svf-remore.zip** is a descriptor of Everest application to deploy the copy of svf-remote Everest application on another Everest-server.

**runSvF-remote.sh** is an example of Everest agent scrpt to run SvF-scenario on a remote host.

## Known issues 

The problem with involving Conda Python from within Everest agent that started by event-service. 
To resolve, just restart agent AFTER that Conda environment was activated
