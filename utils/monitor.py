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

database_host="10.144.120.30"
database_data="sogowebqa"
database_table="fanyi_gpumonitor"
database_user="root"
database_pass="Websearch@qa66"
monitor_id = int(sys.argv[1])
host_id = sys.argv[2]

logInfo = logUtils.logutil(monitor_id)

def get_now_time():
    timeArray = time.localtime()
    return  time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def update_errorlog(log):
    log = log.replace("'", "\\'")
    db = pymysql.connect(database_host,database_user,database_pass,database_data)
    cursor = db.cursor()
    sql = "UPDATE %s set errorlog=CONCAT(errorlog, '%s') where id=%d;" % (database_table, log, monitor_id)
    cursor.execute(sql)
    data = cursor.fetchone()
    try:
        db.commit()
    except:
        logInfo.log_info('Insert log error')
        pass


def set_status(stat):
    db = pymysql.connect(database_host,database_user,database_pass,database_data)
    cursor = db.cursor()
    sql = "UPDATE %s set status=%d where id=%d" % (database_table, stat, monitor_id)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        pass
    if stat == 2:
        remove_stat = "UPDATE %s set status=0,runningPID='' where id=%d" % ('fanyi_host', int(host_id))
        try:
            cursor.execute(remove_stat)
            db.commit()
        except Exception as e:
            db.rollback()
            pass


# 主方法
def ssh_command(user, host, password, command):
    ssh_new_key = 'Are you sure you want to continue connecting'
    child = pexpect.spawn('ssh -l %s %s %s' % (user, host, command))
    i = child.expect([pexpect.TIMEOUT, ssh_new_key, 'password: '])
    if i == 0:
        logInfo.log_info('ERROR!')
        logInfo.log_info('SSH could not login. Here is what SSH said:')
        errorinfo = (child.before).decode('utf-8') + (child.after).decode('utf-8')
        update_errorlog("[%s] SSH login error: %s \n" % (get_now_time(),errorinfo))
        return None
    if i == 1:
        child.sendline('yes')
        child.expect('password: ')
        i = child.expect([pexpect.TIMEOUT, 'password: '])
        if i == 0:
            logInfo.log_info('ERROR!')
            logInfo.log_info('SSH could not login. Here is what SSH said:')
            errorinfo = (child.before).decode('utf-8') + (child.after).decode('utf-8')
            update_errorlog("[%s] SSH login error: %s %s \n" % (get_now_time(),errorinfo))
            return None
    child.sendline(password)
    return child

#gpu mem
def gpu_info(host_id):
    db = pymysql.connect(database_host, database_user, database_pass, database_data)
    cursor = db.cursor()
    sql = "SELECT ip,passw,gpuid,processname FROM fanyi_host where id='%d'" % int(host_id)
    cursor.execute(sql)
    (host_ip,passw,gpuid,processname) = cursor.fetchone()
    if not processname.strip():
        while True:
            try:
                time.sleep(5)
                command_line = "nvidia-smi | egrep -A 1 '"+ str(gpuid) +".*[PMKV][14]0'| grep -v 'Tesla'"
                child = ssh_command("root", host_ip, passw, command_line)
                child.expect(pexpect.EOF)
                gpuinfo = (child.before).decode('utf-8')
                gpu_lst = gpuinfo.strip().split('\r\n')
                for item in gpu_lst:
                    if 'MiB' in item:
                        g_mem=item.split()[8].split('MiB')[0]
                        g_used=item.split()[12].split('%')[0]
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
                        update_errorlog("[%s] Insert a piece of data failed \n" % get_now_time())
                        logInfo.log_info('Insert a piece of data failed')
                        pass
            except Exception as e:
                update_errorlog("[%s] SSH  failed e: %s \n" % (get_now_time(),str(e)))
                logInfo.log_info('SSH  failed'+str(e))
                pass
    else:
        while True:
            try:
                time.sleep(5)
                command_line_one = "nvidia-smi | egrep -A 1 '"+ str(gpuid) +".*[PMK]40'| grep -v 'Tesla'"
                print('command_line_one',command_line_one)
                child_one = ssh_command("root", host_ip, passw, command_line_one)
                child_one.expect(pexpect.EOF)
                gpuinfo_one = (child_one.before).decode('utf-8')
                gpu_lst_one = gpuinfo_one.strip().split('\r\n')
                g_used=gpu_lst_one[0].split()[12].split('%')[0]

                command_line_two = "nvidia-smi | grep '"+ processname +"'| grep '[[:space:]]" + str(gpuid)+"[[:space:]]'"
                print('command_line_two',command_line_two)
                child_two = ssh_command("root", host_ip, passw, command_line_two)
                child_two.expect(pexpect.EOF)
                gpuinfo_two = (child_two.before).decode('utf-8')
                if len(gpuinfo_two.strip())==0:
                    set_status(2)
                    update_errorlog("[%s] Find process %s failed \n" % (get_now_time(),processname))
                    logInfo.log_info("[%s] Find process %s failed \n" % (get_now_time(),processname))
                    sys.exit()
                g_mem=gpuinfo_two.split()[5].split('MiB')[0]
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
                    update_errorlog("[%s] Insert a piece of data failed \n" % get_now_time())
                    logInfo.log_info('Insert a piece of data failed')
                    pass
            except Exception as e:
                update_errorlog("[%s] SSH  failed e: %s \n" % (get_now_time(), str(e)))
                logInfo.log_info('SSH  failed' + str(e))
                pass


def sig_handler(sig, frame):
    update_errorlog("[%s] Revice close signal and exit monitor \n" % get_now_time())
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
            update_errorlog("[%s] Insert a new task sql is : %s \n" % (get_now_time(),sql))
            logInfo.log_info('Insert a new task sql is '+ sql)
        except Exception as e:
            print(e)
            db.rollback()
            update_errorlog("[%s] Insert a new task failed \n" % get_now_time())
            logInfo.log_info('Insert a new task failed')
            sys.exit()
        gpu_info(host_id)

    except Exception as e:
        set_status(2)
        update_errorlog("[%s] Start Monitor failed, error: %s \n" % (get_now_time(),str(e)))
        logInfo.log_info('Start Monitor failed'+str(e))
        sys.exit()
