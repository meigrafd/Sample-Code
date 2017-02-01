# pip install python-crontab

from crontab import CronTab

system_cron = CronTab(tabfile='/etc/crontab', user=False)
job = system_cron.new(command='new_command', user='root')
job.setall('* */2 * * *')
system_cron.write()
