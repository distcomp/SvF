from __future__ import print_function
# from future.utils import iteritems

import os
import sys
import argparse
from zipfile import ZipFile, ZIP_DEFLATED
# import shutil
# import tempfile
# from collections import defaultdict, OrderedDict
# import json
# import calendar
# import time
# import string
# import re

import requests
import everest

from timeit import default_timer as timer
import datetime as dt

import svfremote_config
import svfremote_args

def makeParser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-pr', '--problem', default="problem", help='problem name')
    parser.add_argument('-if', '--inputfolder', default=svfremote_config.SVF_DEFAULT_WORKING_DIR+"/input",
                        help='working dir wth input MNG, DATA, .sol, .res and others')
    parser.add_argument('-of', '--outputfolder', default=svfremote_config.SVF_DEFAULT_WORKING_DIR+"/output",
                        help='working dir wth outputs ')
    parser.add_argument('-t', '--token', default=svfremote_config.SVF_TOKEN_FILE,
                        help='token obtainable with everest.py')
    parser.add_argument('-r', '--resources', nargs='+', default=[],
                        help='everest resources to be used') # ssop_config.SSOP_RESOURCES.values()
    # parser.add_argument('-nlf', '--nlinfile', type=argparse.FileType('rb'),
    #                     help='file with a list of input NL-files')
    # parser.add_argument('-o', '--out-prefix', default='out', help='output prefix')
    # parser.add_argument('-ur', '--use-results', help='Skip parameter sweep run by using already computed results')
    # parser.add_argument('nls', nargs='*', default=[], help='input NL-files')
    # parser.add_argument('-db', '--debug', action='store_true')
    return parser

def getToken(token_file, WF_TOKEN_ENV_NAME='EVEREST_TASK_TOKEN'):
    try:
        token=os.environ[WF_TOKEN_ENV_NAME]
        print('===================================', \
               WF_TOKEN_ENV_NAME + ' token is found and will be used', \
              '===================================')
        return token
    except KeyError:
        print('===================================', \
              "Token file: " + token_file, \
              '===================================')
        with open(token_file) as f:
            token = f.read().strip()
            return token


class SvfSession:
    def __init__(self, sessName="svfremote-" + dt.datetime.now().strftime('%Y-%m-%d-%H:%M'), token_file=svfremote_config.SVF_TOKEN_FILE, \
                 svfService=svfremote_config.SVF_ID, resource=[svfremote_config.SVF_RESOURCES[0]], \
                 indir=svfremote_args.inputDir, outdir=svfremote_args.outputDir, debug=False):
        self.sessName = sessName
        # print("token file: " + token)
        # with open(token) as f:
        #     self.token = f.read().strip()

        self.token = getToken(token_file)

        self.session = everest.Session(sessName, 'https://optmod.distcomp.org', token=self.token)
        # self.ssop = everest.App(ssop_config.SSOP_ID, self.session)
        self.svfApp = everest.App(svfService, self.session)
        self.indir = indir
        self.outdir = outdir
        self.svfResource = resource
        self.nJobs = 0
        self.listJobsId = []
        self.debug = debug

    def makeFileName(self, fname, suffix=""):
        return os.path.join(self.workdir, fname + suffix)

    def makeFileNameInDir(self, fname, dirname):
        return os.path.join(dirname, fname)

    def unpackResults(outDr, resultsZip): # resultsZip - is a path to the results.zip
        zip_path = resultsZip
        extract_dir = outDr

        # Извлекаем все содержимое архива
        with ZipFile(zip_path, 'r') as archive:
            archive.extractall(extract_dir)
            # Получаем список имен файлов в архиве (с учетом путей внутри архива)
            filenames = archive.namelist()

        # Преобразуем пути из архива в имена файлов относительно папки назначения
        extracted_files = []
        for fname in filenames:
            # Исключаем директории
            abs_path = os.path.join(extract_dir, fname)
            if os.path.isfile(abs_path):
                extracted_files.append(abs_path)

        return (extracted_files)

    def runJob(self, jobName, mngFile, inputFiles):
        """
        Run job with the
        :param jobName: the name of the job
        :param mngFile: path to the MNG-file should be placed in the inputDir
        :param inputFiles: the list of other input files (data) *.CSV|XLS... *.sol, *.res and others (assumed to be in self.indir)
        :return: will try to write [jobName + "-results.zip", jobName + '-stdout.txt', jobName + '-stderr.txt'] to thr outdir
        """
        try:
            svfJob = self.svfApp.run({
                "mng": open(mngFile, 'rb'),
                "data": [open(f, 'rb') for f in inputFiles]
            }, resources=[self.svfResource], job_name=jobName)
            jobId = svfJob.id
            # print("JobId" + jobId)
        except Exception as e:
            print("Job[" + jobName + "] caused: ", e)
            self.session.close()
            # return

        print("Job " + jobName + ", " + jobId + " is starting")
        jobName = self.name + "-" + solver + "-" + str(self.nJobs+1)
        jobId = ""
        solved = []
        unsolved = []

        startTime = timer()

        if self.debug:
            print("plan: %s" % (self.makeFileName(self.name, '.plan')))
            print("files: %s" % (self.makeFileName(self.name, '.zip')))
        try:
            # ssop = everest.App(ssop_config.SSOP_ID, self.session)
            job = self.ssopApp.run({
                "plan": open(self.makeFileName(self.name, '.plan'), 'rb'),
                "files": open(self.makeFileName(self.name, '.zip'), 'rb')
            }, resources=self.resources, job_name=jobName)
            jobId = job.id
            # print("JobId" + jobId)
        except Exception as e:
            print("Job[" + jobName + "] caused: ", e)
            self.session.close()
            return

        self.nJobs = self.nJobs + 1

        print("Job " + jobName + ", " + jobId + " is starting")

        try:
            result = job.result()
        except everest.JobException:
            result = self.session.getJobStatus(job.id)
            if 'result' in result:
                print('Job failed, result downloaded')
                self.session.getFile(result['result']['results'], self.makeFileName(jobName + '-results.zip'))
                solved, unsolved = self.saveResults(self.makeFileName(jobName + '-results.zip'), nlNames)
                if self.debug:
                    print("Downloading job's log...")
                    self.session.getJobLog(job.id, jobName + '.log')
            else:
                print('Job failed, no result available')
            self.listJobsId.append(jobId)
            return solved, unsolved, jobId
        except KeyboardInterrupt:
            print('Cancelling the job...')
            try:
                job.cancel()
            except requests.exceptions.HTTPError as e:
                sys.stderr.write('Response from the server: %s\n' % e.response.content)
                sys.stderr.write('Headers of the request: %s\n' % e.request.headers)
                raise
            try:
                result = job.result()
            except everest.JobException as e:
                print(e)
            return (None, None, job.id)

        self.session.getFile(result['results'], self.makeFileName(jobName + '-results.zip'))
        solved, unsolved = self.saveResults(self.makeFileName(jobName + '-results.zip'), nlNames)
        # tasksRes = saveResults(makeName('-results.zip'), stubNames, args)
        if self.debug:
            print("Downloading job's log...")
            self.session.getJobLog(job.id, args.out_prefix + '.log')
            # parseJobLog(args.out_prefix + '.log', tasksRes, args)

        stopTime = timer()
        print('Job %s took: %g s' % (jobId, stopTime - startTime))

        self.listJobsId.append(jobId)
        return solved, unsolved, jobId

    def deleteAllJobs(self):
        for jid in self.listJobsId:
            self.session.deleteJob(jid)
        return

    def deleteAllJobsExceptLast(self,k):
        n = len(self.listJobsId)
        k = min(k, n)
        print("Last jobs will be DELETED")
        for i in range(n-k): #jid in self.listJobsId:
            jid = self.listJobsId[i]
            # print("delete " + jid)
            self.session.deleteJob(jid)
        return


    def deleteWorkFiles(self, patterns):
        files = os.listdir(self.workdir)
        for f in files:
            for p in patterns:
                if p in f:
                    os.remove(os.path.join(self.workdir, f))
        return

if __name__ == "__main__":
    parser = makeParser()
    args = parser.parse_args()
    # print(args)
    vargs = vars(args)
    for arg in vars(args):
        print(arg, getattr(args, arg))

    theSession = SsopSession(name=args.problem, resources=[ssop_config.SSOP_RESOURCES["vvvolhome"]], debug=args.debug)

    solved, unsolved = theSession.runJob(["tmpabc0007_00000", "tmpabc0007_00001", "tmpabc0007_00002", "tmpabc0007_00003"], "peipopt.opt")
    print("solved:   ", solved)
    print("unsolved: ", unsolved)

    theSession.session.close()

    print("Done")
