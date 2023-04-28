#!/usr/bin/env python3
import subprocess
import sentry_sdk
from sentry_sdk.integrations.asyncio import AsyncioIntegration
from sentry_sdk.integrations.excepthook import ExcepthookIntegration
import os
import argparse

print(f"SENTRY URL: {os.environ.get('SENTRY_URL')}")
sentry_sdk.init(f"{os.environ['SENTRY_URL']}", 
                integrations=[
                    AsyncioIntegration(),
                    ExcepthookIntegration(always_run=True),
                ],
                attach_stacktrace=True,)
parser = argparse.ArgumentParser(description='Start processing script')

parser.add_argument('-r',
                    '--run_accession',
                    help="run_accession",
                    type=str,
                    required=True)
parser.add_argument('-p',
                    '--projects_accounts_csv',
                    help="projects_accounts_csv",
                    type=str,
                    required=True)
parser.add_argument('-i1',
                    '--input_file_1',
                    help="input_file_1",
                    type=str,
                    required=True)
parser.add_argument('-i2',
                    '--input_file_2',
                    help="input_file_2",
                    type=str,
                    required=True)
parser.add_argument('-f',
                    '--sars2_fasta',
                    help="sars2_fasta",
                    type=str,
                    required=True)

parser.add_argument('-c',
                    '--task_cpus',
                    help="task cpu",
                    type=str,
                    required=True)

parser.add_argument('-s',
                    '--study_accession',
                    help="study_accession",
                    type=str,
                    default='PRJEB45555',
                    required=False)

args = parser.parse_args()

def run_process(run_accession, projects_accounts_csv, input_file_1, input_file_2, sars2_fasta, task_cpus, study_accession:str='PRJEB45555'):
    # Define the Bash command to run
    bash_command=f"bash map_to_ref.sh {run_accession} {projects_accounts_csv} {input_file_1} {input_file_2} {sars2_fasta} {task_cpus} {study_accession}"
    # Run the Bash command and capture the output
    output = subprocess.run(bash_command, capture_output=True, text=True, shell=True)
    print(output)
    return output

if __name__ == '__main__':
    print(args)
    SENTRY_MSG_LIMIT_LEN=1024
    try:
        subprocess_output=run_process(args.run_accession, args.projects_accounts_csv, args.input_file_1, args.input_file_2, args.sars2_fasta, args.task_cpus, args.study_accession)
        print(f"subprocess output stderr: {subprocess_output.stderr}")
        print(f"subprocess output stderr limit: {subprocess_output.stderr[-SENTRY_MSG_LIMIT_LEN:]}")
        if subprocess_output.returncode!=0:
            raise Exception(subprocess_output.stderr[-SENTRY_MSG_LIMIT_LEN:])
    except Exception as e:
        sentry_sdk.capture_exception(e)
    finally:
        sentry_sdk.flush()