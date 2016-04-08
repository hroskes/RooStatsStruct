import enums
import getpass
import os
import pipes
import subprocess
import textwrap

def bsub_CMS(job, jobname, repmap):
    repmap.update(
                  CMSSW = os.environ["CMSSW_BASE"],
                  job = job,
                  jobname = jobname,
                 )
    job = "cd {CMSSW} && eval $(scram ru -sh) && " + job
    job = pipes.quote(job.format(**repmap))

    command = "echo '{job}' | bsub -q 1nd -J {jobname}".format(**repmap)
    subprocess.check_call(command, shell=True)

def bash(job, jobname, repmap):
    subprocess.check_call(job.format(**repmap), shell=True)

def sbatch(job, jobname, repmap):
    repmap.update(
                  CMSSW = os.environ["CMSSW_BASE"],
                  job = job,
                  jobname = jobname,
                 )
    job = job.format(**repmap)
    jobfile = textwrap.dedent("""\
    #!/bin/bash
    #SBATCH --job-name={jobname}
    #SBATCH --time=24:0:0
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --partition=shared
    #SBATCH --mem=3000

    . /work-zfs/lhc/cms/cmsset_default.sh
    cd {CMSSW} &&
    eval $(scram ru -sh) &&
    cd $SLURM_SUBMIT_DIR &&
    echo "SLURM job running in: " `pwd` &&
    {job}
    """).format(job=job, jobname=jobname, CMSSW = os.environ["CMSSW_BASE"])

    with open("slurm.sh", "w") as f:
        f.write(jobfile)
    subprocess.check_call(["sbatch", "slurm.sh"])
    os.remove("slurm.sh")


if getpass.getuser() == "hroskes":
    submit = bsub_CMS
elif getpass.getuser() == "jroskes1@jhu.edu":
    submit = sbatch
elif getpass.getuser() == "chmartin":
    submit = bsub_ATLAS
elif getpass.getuser() == "ubuntu": #circle
    submit = bash

job = """
cd {pwd} &&
python MakePDF.py {templates} &&
python testproject.py {templates} &&
python testfit.py {templates}
"""

for whichtemplates in enums.WhichTemplates.enumitems:
    repmap = {
              "pwd": os.getcwd(),
              "templates": str(whichtemplates),
             }
    submit(job, str(whichtemplates), repmap)
