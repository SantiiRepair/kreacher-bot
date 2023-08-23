import os
from crontab import CronTab


cron = CronTab(user=True)
c = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(c, "dev.py")
job = cron.new(command=f"python3 {file}")
job.setall("18 0 * * *")
cron.write()
