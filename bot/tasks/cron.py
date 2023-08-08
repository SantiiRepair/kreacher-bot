import os
from getpass import getuser
from crontab import CronTab


cron = CronTab(user=getuser())
dir = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(dir, "dev.py")
job = cron.new(command=f"python3 {file}")
job.setall("18 0 * * *")
cron.write()
