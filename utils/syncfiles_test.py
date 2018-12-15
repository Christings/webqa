#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhangjingjun'
__mtime__ = '2018/12/6'
# ----------Dragon be here!----------
              ┏━┓      ┏━┓
            ┏━┛ ┻━━━━━━┛ ┻━━┓
            ┃       ━       ┃
            ┃  ━┳━┛   ┗━┳━  ┃
            ┃       ┻       ┃
            ┗━━━┓      ┏━━━━┛
                ┃      ┃神兽保佑
                ┃      ┃永无BUG！
                ┃      ┗━━━━━━━━━┓
                ┃                ┣━┓
                ┃                ┏━┛
                ┗━━┓ ┓ ┏━━━┳━┓ ┏━┛
                   ┃ ┫ ┫   ┃ ┫ ┫
                   ┗━┻━┛   ┗━┻━┛
"""
import os
import paramiko
import sys
import requests
import random
import difflib
import time
import pymysql
import logUtils
import re
import cgi
import pexpect
import traceback
database_host="10.144.120.30"
database="sogowebqa"
database_user="root"
database_pass="Websearch@qa66"
database_table = 'publicEnv_analydetail'
task_id = int(sys.argv[1])


def set_status(stat):
    db = pymysql.connect(database_host,database_user,database_pass,database)
    cursor = db.cursor()
    sql = "UPDATE %s set status=%d where id=%d" % (database_table, stat, task_id)
    cursor.execute(sql)
    db.commit()

def set_finish():
    db = pymysql.connect(database_host,database_user,database_pass,database)
    cursor = db.cursor()
    sql = "UPDATE %s set end_time='%s' where id=%d" % (database_table, get_now_time(), task_id)
    cursor.execute(sql)
    db.commit()

def update_errorlog(log):
    log = log.replace("'", "\\'")
    db = pymysql.connect(database_host,database_user,database_pass,database)
    cursor = db.cursor()
    sql = "UPDATE %s set errorlog=CONCAT(errorlog, '%s') where id=%d;" % (database_table, log, task_id)
    cursor.execute(sql)
    data = cursor.fetchone()
    logstr.log_info(str(task_id)+"\t"+log)
    try:
        db.commit()
    except:
        logstr.log_debug("error")

def getInfoFromDb(task_id):
    update_errorlog("[%s] Get task info from db by id \n" % get_now_time())
    try:
        db = pymysql.connect(database_host,database_user,database_pass,database)
        cursor = db.cursor()
        sql = "SELECT ip,user,passw,testlog_path,baselog_path,testp,test_interval,basep,base_interval,user_fk_id,testbox,basebox,test_ttype,base_ttpye FROM %s where id='%d'" % (database_table,task_id)
        cursor.execute(sql)
        data = cursor.fetchone()
        logstr.log_info("ip:"+data[0]+'\n'+'user:'+data[1]+'\n'+'passw:'+data[2]+'\n'+'testlog_path:'+data[3]+'\n'+'baselog_path:'+data[4]+'\n'+'testp'+data[5]+'\n'+'test_interval'+data[6]+'\n'+'basep'+data[7]+'\n'+'base_interval'+data[8]+'\n'+'userid:'+data[9]+'\n')
    except Exception as e:
        set_status(2)
        update_errorlog("[%s] Get task info error from db by id \n" % get_now_time())
        logstr.log_info("[%s] Get task info error from db by id,error info:%s" % (get_now_time(),str(e)))
        sys.exit()
    update_errorlog("[%s] Get task info from db by id success\n" % get_now_time())
    return data

def get_now_time():
    timeArray = time.localtime()
    return  time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def transfile(remote_host,remote_user,remote_pwd,local_path,remote_path):
    """上传文件"""
    try:
        update_errorlog("[%s] Trans file to %s at %s id \n" % (get_now_time(),remote_host,remote_path))
        # 实例化Transport
        trans = paramiko.Transport((remote_host, 22))
        # 建立连接
        trans.connect(username=remote_user, password=remote_pwd)
        # 实例化一个sftp对象
        sftp = paramiko.SFTPClient.from_transport(trans)
        # 上传文件,必须是文件的完整路径,远端的目录必须已经存在
        sftp.put(localpath=local_path, remotepath=remote_path)
        update_errorlog("[%s] Trans file success\n" % get_now_time())
    except Exception as e:
        update_errorlog("[%s] Trans file error \n" % get_now_time())
        logstr.log_info("[%s] Trans file error ,error info:%s" % (get_now_time(),str(e)))
        sys.exit()
    finally:
        trans.close()

def startsh(remote_host,remote_user,remote_pwd,cmds):
    """启动脚本"""
    try:
        update_errorlog("[%s] Start script \n" % get_now_time())
        #创建ssh客户端
        client = paramiko.SSHClient()
        #第一次ssh远程时会提示输入yes或者no
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #密码方式远程连接
        client.connect(remote_host, 22, username=remote_user, password=remote_pwd, timeout=20)
        #互信方式远程连接
        #key_file = paramiko.RSAKey.from_private_key_file("/root/.ssh/id_rsa")
        #ssh.connect(sys_ip, 22, username=username, pkey=key_file, timeout=20)
        #执行命令
        stdin, stdout, stderr = client.exec_command(cmds,timeout=3600)
        #获取命令执行结果,返回的数据是一个list
        result = stdout.readlines()
        return result
    except Exception as e:
        print(e)
        update_errorlog("[%s] Start script error ,error info:%s \n" % (get_now_time(),stderr.readlines()))
        logstr.log_info("[%s] Start script error ,error info:%s" % (get_now_time(),str(e)))
        sys.exit()
    finally:
        client.close()

def insert_data(column_name,data_str):
    db = pymysql.connect(database_host,database_user,database_pass,database)
    cursor = db.cursor()
    up_sql = "UPDATE %s set %s='%s' where id=%d" % (database_table,column_name, data_str,task_id)
    try:
        cursor.execute(up_sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        pass
    db.close()


if __name__ == "__main__":
    # transfile('10.140.40.73','root','sogourank@2016','E:/xcx/runoob.txt','/root/runoob.txt')
    local_path = '/search/odin/pypro/webqa/utils/percentile_box.py'
    remote_path = '/root/percentile_test.py'
    #start_path = '/search/odin/pypro/webqa/utils/start.sh'
    #start_remote_path = '/root/start.sh'
    try:
        logstr = logUtils.logutil(task_id)
        (ip,user,passw,testlog_path,baselog_path,testp,test_interval,basep,base_interval,userid,testbox,basebox,test_ttype,base_ttype) = getInfoFromDb(task_id)
        transfile(ip, user, passw, local_path, remote_path)
        cmds=''
        set_status(1)
        if testlog_path and not baselog_path:
            cmds_test = "python /root/percentile_test.py %s %s %s %s %s" % (testlog_path,testp,test_interval,testbox,base_ttype)
            test_result = startsh(ip,user, passw, cmds_test)
            insert_data('testres_list',test_result[0])
        elif baselog_path and not testlog_path:
            cmds_base = "python /root/percentile_test.py %s %s %s %s %s" % (baselog_path,basep,base_interval,basebox,test_ttype)
            base_result = startsh(ip,user, passw, cmds_base)
            insert_data('baseres_list',base_result[0])
        elif testlog_path and baselog_path:
            cmds_test = "python /root/percentile_test.py %s %s %s %s %s" % (testlog_path,testp,test_interval,testbox,test_ttype)
            test_result = startsh(ip,user, passw, cmds_test)
            test_result[0]=test_result[0].split(',')[:-1]
            test_result[1]=test_result[1].split(',')[:-1]
            cmds_base = "python /root/percentile_test.py %s %s %s %s %s" % (baselog_path,basep,base_interval,basebox,base_ttype)
            base_result = startsh(ip,user, passw, cmds_base)
            base_result[0]=base_result[0].split(',')[:-1]
            base_result[1]=base_result[1].split(',')[:-1]
            testresult=''
            baseresult=''
            if len(test_result[1])>=len(base_result[1]):
                for i, element in enumerate(base_result[0]):
                    baseresult+=('[%s' % base_result[0][i] + ',' + base_result[1][i]+'],')
                    testresult+=('[%s' % base_result[0][i] + ',' + test_result[1][i]+'],')
            else:
                for i, element in enumerate(test_result[0]):
                    baseresult+=('[%s' % base_result[0][i] + ',' + base_result[1][i]+'],')
                    testresult+=('[%s' % base_result[0][i] + ',' + test_result[1][i]+'],')
            insert_data('testres_list',testresult)
            insert_data('baseres_list',baseresult)
        set_finish()
        set_status(0)
            
    except Exception as e:
        traceback.print_exc()
        update_errorlog("init failed!\n")
        set_status(2)
        sys.exit()
