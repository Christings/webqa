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

database_host="10.144.120.30"
database="sogowebqa"
database_user="root"
database_pass="Websearch@qa66"
database_table = 'publicEnv_analydetail'
task_id = int(sys.argv[1])


def set_status(stat):
    db = pymysql.connect(database_host,database_user,database_pass,database)
    cursor = db.cursor()
    sql = "UPDATE %s set status=%d where id=%d" % ('fanyi_interfaceeval', stat, task_id)
    cursor.execute(sql)
    db.commit()

def update_errorlog(log):
    log = log.replace("'", "\\'")
    db = pymysql.connect(database_host,database_user,database_pass,database)
    cursor = db.cursor()
    sql = "UPDATE %s set errorlog=CONCAT(errorlog, '%s') where id=%d;" % ('fanyi_interfaceeval', log, task_id)
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
        sql = "SELECT ip,user,passw,testlog_path,baselog_path,user_fk_id FROM %s where id='%d'" % (database_table,task_id)
        cursor.execute(sql)
        data = cursor.fetchone()
        logstr.log_info("ip:"+data[0]+'\n'+'user:'+data[1]+'\n'+'passw'+data[2]+'\n'+'testlog_path:'+data[3]+'\n'+'baselog_path:'+data[4]+'\n'+'userid:'+data[5])
    except Exception as e:
        set_status(3)
        update_errorlog("[%s] Get task info error from db by id \n" % get_now_time())
        logstr.log_info("[%s] Get task info error from db by id,error info:%s" % (get_now_time(),str(e)))
        sys.exit()
    update_errorlog("[%s] Get task info from db by id success\n" % get_now_time())
    return data

def get_now_time():
    timeArray = time.localtime()
    return  time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

def set_subpid(subpid,status):
    db = pymysql.connect(database_host,database_user,database_pass,database)
    cursor = db.cursor()
    sql = "UPDATE %s set start_time='%s',runningPID='%s',status=%d where id=%d;" % ('fanyi_interfaceeval', get_now_time(),subpid, status,int(task_id))
    cursor.execute(sql)
    try:
        db.commit()
        logstr.log_info('Update PID task ,sql is '+ sql)
    except Exception as e:
        db.rollback()
        logstr.log_info('Update PID task failed')


def transfile(remote_host,remote_user,remote_pwd,local_path,remote_path):
    """上传文件"""
    try:
        # 实例化Transport
        trans = paramiko.Transport((remote_host, 22))
        # 建立连接
        trans.connect(username=remote_user, password=remote_pwd)
        # 实例化一个sftp对象
        sftp = paramiko.SFTPClient.from_transport(trans)
        # 上传文件,必须是文件的完整路径,远端的目录必须已经存在
        sftp.put(localpath=local_path, remotepath=remote_path)
    except Exception as e:
        print(e)
        pass
    finally:
        trans.close()

if __name__ == "__main__":
    # transfile('10.140.40.73','root','sogourank@2016','E:/xcx/runoob.txt','/root/runoob.txt')
    local_path = '/search/odin/pypro/webqa/utils/percenttile_test.py'
    remote_path = '/root/percenttile_test.py'
    try:
        logstr = logUtils.logutil(task_id)
        subpid = os.getpid()
        set_subpid(subpid,1)
        (ip,user,passw,testlog_path,baselog_path,userid) = getInfoFromDb(task_id)
        transfile(ip, user, task_id, passw, local_path, remote_path)
        if testlog_path:
            pass
        if baselog_path:
            pass
    except Exception as e:
        print(e)
        update_errorlog("init failed!")
        set_status(3)
        sys.exit()