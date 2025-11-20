RESOURCES = [
    "52eb8d4e420000f401166a2e", # irbis1
    "544e54293300003f0038c674", # restopt-vm1
    "544e82673300003f0038c687", # restopt-vm2
    "578ea88d310000b33c8c7f44"  # fujiRestOpt
]

SSOP_RESOURCES = {"shark1vvv"      : "65e4490e1200001100f99199", \
                  "vvvolhome"      : "5d167bbf1200008937f93ff9", \
                  "vvvolhome2"     : "5e33cf6211000075006a321f", \
                  "vvvoldell"      : "5c5b0d9c410000a25e4c9b99", \
                  "ui4.kiae"       : "59c520773300004852f4363a", \
                  "ui4.kiae.vvvol" : "5addfc3115000084cb623517", \
                  "hse"            : "5e3ec8641100003a446a8be5",  \
                  "govorun.vvvol"  : "5dd6c22a120000bd043f3216",  \
                  "pool-scip-ipopt" : "5ec44a9c2f0000bd4d64faf9", \
                  "test-pool-scip-ipopt" : "5ec6e8c22f00001359654deb" \
                  }
# pool-scip-ipopt: ui4.kiae.vvvol, hse, govorun.vvvol, vvvoldell, vvvolhome2
# test-pool-scip-ipopt: vvvoldell, vvvolhome2

                  # 'irbis1'       : '52eb8d4e420000f401166a2e', \
                  # 'fujiRestOpt'  : '578ea88d310000b33c8c7f44', \
                  # 'restopt-vm1'  : '544e54293300003f0038c674', \
                  # 'restopt-vm2'  : '544e82673300003f0038c687', \

# Solvers available for SSOP
SSOP_SOLVERS = ["ipopt", "scip"]
SOLVER_OPTIONS_DELIMETER = {"ipopt" : " ", "scip" : " = "}

PARAMETER_SWEEP_ID = "530f36d73d00002d04548b0e"
SOLVE_AMPL_STUB_ID = "vladimirv/solve-ampl-stub" #"531f44233e0000c015f09ad3"
SSOP_ID = "vladimirv/SSOP" #"5bb2783e420000772e1049fd"


# Add your Everest login and password here to make token update automatically
SSOP_TOKEN_FILE = "/mnt/hgst2/ext4/git_work/pyomo-everest/.365d-token-shark1-2025"
# The command to update 30-days token:
# python everest.py get-token -server_uri https://optmod.distcomp.org -u vladimirv -l ssop -t 2592000 | tee .token30d
UPDATE_TOKEN_PERIOD_IN_SEC = 7*24*3600 - 5*3600

# Working dirs
SSOP_DEFAULT_WORKING_DIR = "/mnt/hgst2/ext4/python_work/pyomo-everest/ssop/.demo" #"/home/vladimirv/python_work/pyomo-everest/ssop/.tmp"

# Run miscellaneous
SSOP_RUN_SH_PREFIX = "run-" # run-ipopt.sh, run-scip.sh, run-fscip.sh ...
