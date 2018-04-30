import json
import schedule
import time

def job_1():
	print "doing job 1 !!"

# def job_2():
# 	print "doing job 2 !!"	


schedule.every(5).seconds.do(job_1)

# schedule.run_pending()

# schedule.every(7).seconds.do(job_2)


while True:
    # print schedule.run_pending()
    print schedule.idle_seconds()
    time.sleep(1)