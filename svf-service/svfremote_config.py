SVF_RESOURCES = {"shark1vvv4SvF"   : "66672a4c1200001500e6c3ce", \
                  "YCloud4SvF"     : "63e0e085140000e608215147"
                  }
# SVF_ID = "vladimirv/svf-remote"
SVF_ID = "vladimirv/svf-remote"

# Add your Everest login and password here to make token update automatically
SVF_TOKEN_FILE = "/mnt/hgst2/ext4/git_work/pyomo-everest/.365d-token-shark1-2025"
# SVF_TOKEN_FILE = "/home/vladimirv/git_work/pyomo-everest/.365d-token-shark1-2025"
# The command to update 30-days token:
# python everest.py get-token -server_uri https://optmod.distcomp.org -u vladimirv -l ssop -t 2592000 | tee .token30d
# UPDATE_TOKEN_PERIOD_IN_SEC = 7*24*3600 - 5*3600

# Working dirs
SVF_DEFAULT_WORKING_DIR = "temp" #"/home/vladimirv/python_work/pyomo-everest/ssop/.tmp"

# Run miscellaneous
SVF_RUN_SH_PREFIX = "run-" # run-ipopt.sh, run-scip.sh, run-fscip.sh ...
