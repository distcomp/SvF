import argparse
import importlib
import svfremote_config
import svfremote_session as svfsession


def makeParser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--pars', default="svfremoteargs.py", help='Python module with svf-remote parameters')
    parser.add_argument('-cf', '--cleanfiles', action='store_true', help='clean working directory')
    parser.add_argument('-cj', '--cleanjobs', action='store_true', help='clean jobs from server')
    return parser

if __name__ == '__main__':
    args = makeParser().parse_args()
    # data_module = importlib.import_module(args.pars)