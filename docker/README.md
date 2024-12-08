Using dockerized SvF

To add your machine with a dockerized SvF to Everest:
 1. Create a new resource: https://optmod.distcomp.org/resources/new and save the token
 2. Start Everest agent with the SvF's environment (replace !!!TOKEN!!! with token obtained at step 1): `docker run -d -it --restart always --name agent -e EVEREST_TOKEN=!!!TOKEN!!! -e MAX_TASKS=16 distcomp/svf`
 3. Use https://optmod.distcomp.org/apps/vladimirv/svf-remote application as usual, specifying the new resource in Resources control

To build and run the docker image locally for development purposes:
```
git clone https://github.com/distcomp/SvF.git
cd SvF
git clone https://github.com/distcomp/pyomo-everest.git
cd pyomo-everest
git clone https://gitlab.com/everest/python-api.git
cd ../../docker
make stop build run
```
