import enums
import getpass
import os
import pipes
import subprocess
import sys
import textwrap

def preparetemplates():
    subprocess.check_call("""
      cd templates/VBF &&
      python makefinaltemplates.py
    """, shell = True)
    subprocess.check_call("""
      cd templates/ggH_fromMeng_normalized &&
      root -l -b -q normalizesig.C+ &&
      root -l -b -q normalizebkg.C+
    """, shell = True)
    

def bsub_CMS(job, jobname, repmap):
    repmap.update(
                  CMSSW = os.environ["CMSSW_BASE"],
                  jobname = jobname,
                 )
    job = "cd {CMSSW} && eval $(scram ru -sh) && " + job
    job = pipes.quote(job.format(**repmap))
    repmap.update(
                  job = job,
                 )

    command = "echo {job} | bsub -q 1nd -J {jobname}".format(**repmap)
    subprocess.check_call(command, shell=True)

def bash(job, jobname, repmap):
    subprocess.check_call(job.format(**repmap), shell=True)

def sbatch(job, jobname, repmap):
    if "ggH" in str(whichtemplates):
         memory = 10000
         partition = "lrgmem"
    else:
         memory = 3000
         partition = "shared"

    repmap.update(
                  CMSSW = os.environ["CMSSW_BASE"],
                  jobname = jobname,
                  memory = memory,
                  partition = partition,
                 )
    job = job.format(**repmap)
    repmap.update(
                  job = job
                 )


    jobfile = textwrap.dedent("""\
    #!/bin/bash
    #SBATCH --job-name={jobname}
    #SBATCH --time=24:0:0
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --partition={partition}
    #SBATCH --mem={memory}

    . /work-zfs/lhc/cms/cmsset_default.sh
    cd {CMSSW} &&
    eval $(scram ru -sh) &&
    cd $SLURM_SUBMIT_DIR &&
    echo "SLURM job running in: " `pwd` &&
    {job}
    """).format(**repmap)

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
( python testproject.py {templates} | grep -v "Integral below threshold: 0$" | grep -v "hobs is not found";
python testfit.py {templates} | grep -v "Integral below threshold: 0$" | grep -v "hobs is not found" )
"""

preparetemplates()

for whichtemplates in enums.WhichTemplates.enumitems:
    if len(sys.argv) != 1 and whichtemplates not in sys.argv[1:]: continue
    repmap = {
              "pwd": os.getcwd(),
              "templates": str(whichtemplates),
             }
    submit(job, str(whichtemplates), repmap)
