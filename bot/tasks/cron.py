import os
from crontab import CronTab


cron = CronTab(user=True)
current_dir = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(current_dir, "dev.py")
job = cron.new(command=f"python3 {file}")
job.setall("18 0 * * *")
cron.write()
