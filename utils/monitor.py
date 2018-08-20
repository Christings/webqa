# -*- coding:utf-8 -*-
from datetime import datetime
import pexpect
import threading
import pymysql
import sys
import time
import signal
import os
import logUtils

database_host="10.134.110.163"
database_data="sogowebqa"
database_table="fanyi_gpumonitor"
database_user="root"
database_pass="Websearch@qa66"
monitor_id = int(sys.argv[1])
host_id = sys.argv[2]

logInfo = logUtils.logutil(monitor_id)

# 主方法
def ssh_command(user, host, password, command):
    ssh_new_key = 'Are you sure you want to continue connecting'
    child = pexpect.spawn('ssh -l %s %s %s' % (user, host, command))
    i = child.expect([pexpect.TIMEOUT, ssh_new_key, 'password: '])
    if i == 0:
        logInfo.log_info('ERROR!')
        logInfo.log_info('SSH could not login. Here is what SSH said:')
        logInfo.log_info(child.before, child.after)
        return None
    if i == 1:
        child.sendline('yes')
        child.expect('password: ')
        i = child.expect([pexpect.TIMEOUT, 'password: '])
        if i == 0:
            logInfo.log_info('ERROR!')
            logInfo.log_info('SSH could not login. Here is what SSH said:')
            logInfo.log_info(child.before, child.after)
            return None
    child.sendline(password)
    return child

#gpu mem
def gpu_info(host_id):
    db = pymysql.connect(database_host, database_user, database_pass, database_data)
    cursor = db.cursor()
    sql = "SELECT ip,passw,gpuid FROM fanyi_host where id='%d'" % int(host_id)
    cursor.execute(sql)
    (host_ip,passw,gpuid) = cursor.fetchone()
    while True:
        #child = ssh_command("root", host_ip, passw, "nvidia-smi | grep 250W")
        command_line = "nvidia-smi | egrep -A 1 '"+ str(gpuid) +".*[PMK]40'| grep -v 'Tesla'"
        child = ssh_command("root", host_ip, passw, command_line)
        print(child)
        child.expect(pexpect.EOF)
        gpuinfo = (child.before).decode('utf-8')
        gpu_lst = gpuinfo.strip().split('\r\n')
        g_mem=gpu_lst[0].split()[8].split('MiB')[0]
        g_used=gpu_lst[0].split()[12].split('%')[0]
        g_mem_list = g_mem + ","
        g_used_list = g_used + ","
        timedata = datetime.now().strftime('[Date.UTC(%Y,%m,%d,%H,%M,%S)')
        gpumeminfo = timedata+","+g_mem+'],\n'
        gpumemused = timedata+","+g_used+'],\n'
        db = pymysql.connect(database_host, database_user, database_pass, database_data)
        cursor = db.cursor()
        sql = "UPDATE %s set gpumem=CONCAT(gpumem, '%s'),gpumemused=CONCAT(gpumemused, '%s') ,gpumem_list=CONCAT(gpumem_list, '%s'),gpumemused_list=CONCAT(gpumemused_list, '%s') where id=%d;" % (database_table, gpumeminfo, gpumemused,g_mem_list,g_used_list,monitor_id)
        logInfo.log_info('gpu mem is '+g_mem+' and gpu mem used is '+g_used)
        cursor.execute(sql)
        try:
            db.commit()
        except:
            db.rollback()
            logInfo.log_info('Insert a piece of data failed')
        time.sleep(5)


def sig_handler(sig, frame):
    logInfo.log_info('Revice close signal and exit monitor')
    sys.exit()

signal.signal(signal.SIGTERM, sig_handler)

if __name__ == '__main__':
    try:
        # t1 = threading.Thread(target=gpu_info)
        # t1.start()
        subpid = os.getpid()
        db = pymysql.connect(database_host, database_user, database_pass, database_data)
        cursor = db.cursor()
        sql = "UPDATE fanyi_host set runningPID='%s',status=1 where id=%d;" % ( subpid, int(host_id))
        cursor.execute(sql)
        try:
            db.commit()
            logInfo.log_info('Insert a new task sql is '+ sql)
        except Exception as e:
            db.rollback()
            logInfo.log_info('Insert a new task failed')
        gpu_info(host_id)

    except Exception as e:
        logInfo.log_info('Start Monitor failed'+str(e))
