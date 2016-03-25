import enums
import getpass
import os
import pipes
import subprocess

mymap = {}

if getpass.getuser() == "hroskes":
    setup = "cd {CMSSW} && eval $(scram ru -sh) &&"
    mymap["CMSSW"] = os.environ["CMSSW_BASE"]
elif getpass.getuser == "chmartin":
    "add atlas stuff here"

job = setup + """
cd {pwd} &&
python MakePDF.py {templates} &&
python testproject.py {templates} &&
python testfit.py {templates}
"""

for whichtemplates in enums.WhichTemplates.enumitems:
    mymap.update({
                  "pwd": os.getcwd(),
                  "templates": str(whichtemplates),
                 })
    bsubcommand = "echo " + pipes.quote(job.format(**mymap)) + " | bsub -q 1nd -J " + str(whichtemplates)
    subprocess.call(bsubcommand, shell=True)
