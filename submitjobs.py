import enums
import getpass
import os
import pipes
import subprocess

mymap = {}

if getpass.getuser() == "hroskes":
    setup = "cd {CMSSW} && eval $(scram ru -sh) &&"
    mymap["CMSSW"] = os.environ["CMSSW_BASE"]
    submit = "bsub -q 1nd -J {templates}"
elif getpass.getuser() == "chmartin":
    setup = "add atlas stuff here"
    submit = "bsub -q 1nd -J {templates}"
elif getpass.getuser() == "ubuntu": #circle
    setup = ""
    submit = "bash"

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
    bsubcommand = "echo " + pipes.quote(job.format(**mymap)) + " | " + submit.format(**mymap)
    subprocess.check_call(bsubcommand, shell=True)
