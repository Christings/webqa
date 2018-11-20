#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import requests
import random
import difflib
import time
import pymysql
import logUtils
import base64
import re
import cgi
#import HTMLParser
import os
import pexpect
from xml.etree import ElementTree
from bs4 import BeautifulSoup
#from fanyi import requestData
import requestData

#reload(sys)
#sys.setdefaultencoding('utf-8')
database_host="10.144.120.30"
database="sogowebqa"
database_user="root"
database_pass="Websearch@qa66"
root_path = '/search/odin/daemon/fanyi/tools/'
database_table = 'fanyi_interfaceeval'
task_id = int(sys.argv[1])

def get_now_time():
    timeArray = time.localtime()
    return  time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

def insert_finished(finished,diff_task_id,end_time=''):
    db = pymysql.connect(database_host,database_user,database_pass,database)
    cursor = db.cursor()
    if end_time == '':
        up_sql = "UPDATE %s set finished=%d where id=%d" % ('fanyi_interfaceeval', finished ,diff_task_id)
    else:
        up_sql = "UPDATE %s set finished=%d,end_time='%s' where id=%d" % ('fanyi_interfaceeval', finished ,end_time,diff_task_id)
    try:
        cursor.execute(up_sql)
        db.commit()
    except Exception as e:
        db.rollback()
        pass
    db.close()

def insert_diff_data(diffcontent,diffnum,diff_task_id,reqtype):
    db = pymysql.connect(database_host,database_user,database_pass,database,charset='utf8')
    cursor = db.cursor()
    
    update_sql = "UPDATE %s set diffnum=%d where id=%d" % ('fanyi_interfaceeval',diffnum,diff_task_id)
    try:
        cursor.execute(update_sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        pass
    sql = "INSERT INTO %s(user,create_time,diff_content,diff_task_id,diff_type) VALUES ('%s','%s','%s',%d,'%s')" % ('fanyi_ifevaldiff', 'zhangjingjun',get_now_time() ,diffcontent,diff_task_id,reqtype)
   
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
        pass
    db.close()

def parseXmlReq(xml_str):
    query_lst_info=dict()
    if xml_str=="":
        return query_lst_info
    xmlns={'soapenv':'http://schemas.xmlsoap.org/soap/envelope/',
         'v2':'http://api.microsofttranslator.com/V2'}
    try:
        root=ElementTree.fromstring(xml_str)
    except Exception as e:
        query_lst_info['wrongreq']='wrong request,reson:'+str(e)
        query_lst_info['qtext'] = 'parseWrong'
        return query_lst_info
    try:
        for node in root.findall('soapenv:Body',xmlns):
            for Translate in node.findall('v2:Translate',xmlns):
                if Translate.find('v2:text',xmlns) is not None:
                    query_lst_info['qtext']=Translate.find('v2:text',xmlns).text.encode('utf-8')
                else:
                    query_lst_info['qtext']='parseWrong'
                if Translate.find('v2:from',xmlns) is not None:
                    query_lst_info['qfrom']=Translate.find('v2:from',xmlns).text.encode('utf-8')
                else:
                    query_lst_info['qfrom']=''
                if Translate.find('v2:to',xmlns) is not None:
                    query_lst_info['qto']=Translate.find('v2:to',xmlns).text.encode('utf-8')
                else:
                    query_lst_info['qto']=''
    except Exception as e:
        query_lst_info['wrongreq']='wrong request,reson:'+str(e)
        query_lst_info['qtext'] = 'parseWrong'
    return query_lst_info


def parseXmlRes(xml_str):
    result_dic=dict()
    ns={'parent':'http://schemas.xmlsoap.org/soap/envelope/','child':'http://fanyi.sogou.com/'}
    try:
        root=ElementTree.fromstring(xml_str)
    except Exception as e:
        result_dic['wrongres']='wrongres:'+str(e)
        result_dic['transRes']='Error request'
        return result_dic
    try:
        tempNum = random.randint(1,3)
        for node in root.findall('parent:Body',ns):
            for body in node.findall('child:TranslateResponse',ns):
                if body.find('child:TranslateResult',ns) is not None:
                    if body.find('child:TranslateResult',ns).text is not None:
                        result_dic['transRes']=body.find('child:TranslateResult',ns).text
                    else:
                        result_dic['transRes']='Error request'
                else:
                    result_dic['transRes']='Error request'
    except Exception as e:
        result_dic['wrongres']='wrongres:'+str(e)
        result_dic['transRes']='Error request'
    if 'transRes' not in result_dic:
        result_dic['transRes']='Error request'
    return result_dic

def getUniNum(string):
    try:
        string=string.strip()
        query=""
        for uchar in string:
            query+="&#"+str(ord(uchar))+";"
        return query
    except Exception as e:
        pass

#def decodeHtml(input_str):
#    h = HTMLParser.HTMLParser()
#    s = h.unescape(input_str)
#    return s


def getDiff(query_tools_path,filename,mission_id,base_url,test_url,reqtype):
    base_diff_content = ''
    test_diff_content = ''
    tmp = 0
    finished = 0
    diffnum = 0
    with open(query_tools_path+'query/'+filename,'r') as fin,open(query_tools_path+'result_log/'+'base_res_'+str(mission_id),'wb+') as fw_base,open(query_tools_path+'result_log/'+'test_res_'+str(mission_id),'wb+') as fw_test,open(query_tools_path+'result_log/'+'all_req_'+str(mission_id),'wb+') as allo:
        set_status(2)
        if reqtype == 'xml':
            for item in fin.readlines():
                finished +=1
                item = item.strip()
                reqInfo = parseXmlReq(item)
                if reqInfo['qtext'] == 'parseWrong':
                    continue
                xmldata = item
                result_base=dict()
                result_test=dict()
                try:
                    resp_base = requests.post('http://'+base_url+'/xml', data=xmldata)
                    result_base = parseXmlRes(resp_base.text)
                except Exception as e :
                    result_base['transRes']='base request http error'
                    pass
                try:
                    resp_test = requests.post('http://'+test_url+'/xml', data=xmldata)
                    result_test = parseXmlRes(resp_test.text)
                except Exception as e :
                    result_test['transRes']='test request http error'
                    pass
                allo.write(('Query:'+item+'\n').encode('utf-8'))
                allo.write(('base:'+resp_base.text+'result:'+result_base['transRes']+'\n').encode('utf-8'))
                allo.write(('test:'+resp_test.text+'result:'+result_test['transRes']+'\n').encode('utf-8'))
                if (result_base['transRes'] != result_test['transRes']):
                    base_info = 'Query:'+reqInfo['qtext'].decode()+' from:'+reqInfo['qfrom'].decode()+' to:'+reqInfo['qto'].decode()+'\n'+result_base['transRes']+'\n'
                    test_info = 'Query:'+reqInfo['qtext'].decode()+' from:'+reqInfo['qfrom'].decode()+' to:'+reqInfo['qto'].decode()+'\n'+result_test['transRes']+'\n'
                    base_diff_content += base_info
                    test_diff_content += test_info
                    fw_base.write(base_info.encode('utf-8'))
                    fw_test.write(test_info.encode('utf-8'))
                    tmp+=1
                    diffnum+=1
                if tmp == 50:
                    d = difflib.HtmlDiff()
                    diff_html = d.make_file(base_diff_content.splitlines(),test_diff_content.splitlines())
                    parse_html = BeautifulSoup(diff_html,"html.parser")
                    escape_str = cgi.escape(str(parse_html.table),quote=True)
                    #b = decodeHtml(a)
                    #print 'bbbbb'+b.encode('utf-8')
                    insert_diff_data(escape_str.replace("'","&#39;"),diffnum,mission_id,reqtype)
                    base_diff_content=''
                    test_diff_content=''
                    tmp=0
                if (finished%1000)==0:
                    insert_finished(finished,mission_id)
            if base_diff_content.strip()!='' or test_diff_content.strip()!='':
                d = difflib.HtmlDiff()
                diff_html = d.make_file(base_diff_content.splitlines(),test_diff_content.splitlines())
                parse_html = BeautifulSoup(diff_html,"html.parser")
                escape_str = cgi.escape(str(parse_html.table),quote=True)
                #b = decodeHtml(a)
                #print 'bbbbb'+b.encode('utf-8')
                try:
                    insert_diff_data(escape_str.replace("'","&#39;"),diffnum,mission_id,reqtype)
                except Exception as e:
                    print(e)
            insert_finished(finished,mission_id,get_now_time())
            set_status(4)
        elif reqtype == 'json':
            for item in fin.readlines():
                finished += 1
                item = item.strip()
                reqInfo = requestData.parseJsonReq(item)
                if reqInfo['status'] is False:
                    continue
                jsondata = item
                result_base = dict()
                result_test = dict()
                try:
                    resp_base = requests.post('http://' + base_url + '/json', data=jsondata)
                    result_base = requestData.JsonResult(resp_base.text)
                    if result_base['status'] is False:
                        result_base['transRes'] = 'base request http error'
                        result_base['chinese_query'] = 'request error'
                        result_base['docs'] = []
                except Exception as e:
                    result_base['transRes'] = 'base request http error'
                    pass
                try:
                    resp_test = requests.post('http://' + test_url + '/json', data=jsondata)
                    result_test = requestData.JsonResult(resp_test.text)
                    if result_test['status'] is False:
                        result_test['transRes'] = 'base request http error'
                        result_test['chinese_query'] = 'request error'
                        result_test['docs'] = []
                except Exception as e:
                    result_test['transRes'] = 'test request http error'
                    pass
                head_info = ('chinese_query_base:'+result_base['chinese_query'] + '\n'+'chinese_query_test:'+result_test['chinese_query']+'\n')
                englinsh_info = 'english_query:'+reqInfo['english_query']+'\n'
                allo.write(head_info.encode('utf-8'))
                allo.write(englinsh_info.encode('utf-8'))
                reqstr = ''
                for value in reqInfo['docs']:
                    reqstr += (str(value)+'\n')
                allo.write(reqstr.encode('utf-8'))
                resbase_str=''
                for value in result_base['docs']:
                    resbase_str+=(str(value)+'\n')
                allo.write(('base:' + resbase_str + '\n').encode('utf-8'))
                restest_str=''
                for value in result_test['docs']:
                    restest_str+=(str(value)+'\n')
                allo.write(('test:' + restest_str + '\n').encode('utf-8'))
                if (resbase_str != restest_str):
                    base_info = head_info + englinsh_info + reqstr + resbase_str
                    test_info = head_info + englinsh_info + reqstr + restest_str
                    base_diff_content += base_info
                    test_diff_content += test_info
                    fw_base.write(base_info.encode('utf-8'))
                    fw_test.write(test_info.encode('utf-8'))
                    tmp += 1
                    diffnum += 1
                if tmp == 2:
                    d = difflib.HtmlDiff()
                    diff_html = d.make_file(base_diff_content.splitlines(), test_diff_content.splitlines())
                    parse_html = BeautifulSoup(diff_html, "html.parser")
                    escape_str = cgi.escape(str(parse_html.table), quote=True)
                    # b = decodeHtml(a)
                    # print 'bbbbb'+b.encode('utf-8')
                    insert_diff_data(escape_str.replace("'", "&#39;"), diffnum, mission_id, reqtype)
                    base_diff_content = ''
                    test_diff_content = ''
                    tmp = 0
                if (finished % 100) == 0:
                    insert_finished(finished, mission_id)
            if base_diff_content.strip()!='' or test_diff_content.strip()!='':
                d = difflib.HtmlDiff()
                diff_html = d.make_file(base_diff_content.splitlines(), test_diff_content.splitlines())
                parse_html = BeautifulSoup(diff_html, "html.parser")
                escape_str = cgi.escape(str(parse_html.table), quote=True)
                # b = decodeHtml(a)
                # print 'bbbbb'+b.encode('utf-8')
                try:
                    insert_diff_data(escape_str.replace("'", "&#39;"), diffnum, mission_id, reqtype)
                except Exception as e:
                    print(e)
            insert_finished(finished, mission_id, get_now_time())
            set_status(4)

def getInfoFromDb(task_id):
    update_errorlog("[%s] Get task info from db by id \n" % get_now_time())
    try:
        db = pymysql.connect(database_host,database_user,database_pass,database)
        cursor = db.cursor()
        sql = "SELECT test_url,base_url,reqtype,queryip,queryuser,querypassw,querypath,user FROM %s where id='%d'" % ('fanyi_interfaceeval',task_id)
        cursor.execute(sql)
        data = cursor.fetchone()
        logstr.log_info("test_url:"+data[0]+'\n'+'base_url:'+data[1]+'\n'+'reqtype'+data[2]+'\n'+'queryip:'+data[3]+'\n'+'queryuser:'+data[4]+'\n'+'querypassw:'+data[5]+'\n'+'querypath:'+data[6])
    except Exception as e:
        set_status(3)
        update_errorlog("[%s] Get task info error from db by id \n" % get_now_time())
        logstr.log_info("[%s] Get task info error from db by id,error info:%s" % (get_now_time(),str(e)))
        sys.exit()
    update_errorlog("[%s] Get task info from db by id success\n" % get_now_time())
    return data
    
def getQueryFile(root_path):
    # scp query to tools dir
    try:
        update_errorlog("[%s] %s\n" % (get_now_time(), "start try to scp query data"))
        #if(os.path.exists(root_path+'query')):
        #    logstr.log_info('query dir is exist')
        #    oldfile = os.listdir(root_path+'query')
        #    timeArray = time.localtime()
        #    filename = time.strftime("%Y-%m-%d_%H%M%S", timeArray)
        #    if oldfile:
        #        for item in oldfile:
        #            os.popen('mv %s %s' % (root_path+'query/'+item,root_path+'query_bak/'+filename+'_'+item))
        if queryip!='' and queryuser!='' and querypassw!='' and querypath!='':
            scpres = scp_new_file(root_path+'query',queryip,queryuser,querypassw,querypath,'query_data')
        else:
            update_errorlog("[%s] %s\n" % (get_now_time(), "query data configure is wrong"))
            set_status(3)
            sys.exit()
        #filelist = os.listdir(root_path+'query')
    except Exception as e:
        update_errorlog("[%s] Get query file error\n" % get_now_time())
        logstr.log_info("[%s] Get query file error ,error info:%s" % (get_now_time(),str(e)))
        set_status(3)
        sys.exit()
    update_errorlog("[%s] %s\n" % (get_now_time(), "query data scp local success"))

def scp_new_file(file_path,newfileip,newfileuser,newfilepassw,newfilepath,filetype):
    update_errorlog("[%s] try scp rd %s to test enviroment\n" % (get_now_time(),filetype))
    if filetype != 'query_data':
        if os.path.exists(file_path):
            update_errorlog("[%s] %s dir exists,del it\n" % (get_now_time(), filetype))
            os.popen("rm -rf " + file_path)

    passwd_key = '.*assword.*'

    cmdline = 'scp -r %s@%s:%s %s/%s' %(newfileuser, newfileip, newfilepath, file_path,task_id)
    try:
        child=pexpect.spawn(cmdline,maxread=20000,timeout=300)
        os.popen("set timeout -1")
        expect_result = child.expect([r'assword:',r'yes/no', pexpect.EOF, pexpect.TIMEOUT])
        if expect_result == 0:
            child.sendline(newfilepassw)
            os.popen("set timeout -1")
        elif expect_result ==1:
            child.sendline('yes')
            child.expect(passwd_key,timeout=30)
            child.sendline(newfilepassw)
        child.expect(pexpect.EOF)

    except Exception as e:
        update_errorlog("[%s] %s, scp rd %s failed \n" % (get_now_time(), e,filetype))
        set_status(3)
        sys.exit()
    update_errorlog("[%s] try scp rd %s to test enviroment success\n" % (get_now_time(),filetype))
    return 0

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

def set_status(stat):
    db = pymysql.connect(database_host,database_user,database_pass,database)
    cursor = db.cursor()
    sql = "UPDATE %s set status=%d where id=%d" % ('fanyi_interfaceeval', stat, task_id)
    cursor.execute(sql)
    db.commit()

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

def sendMail(title,mail_body,tlist,attname,attbody):
    mail_url = 'http://mail.portal.sogou/portal/tools/send_mail.php'
    mail_Info = {
    'uid' : "zhangjingjun@sogou-inc.com",
    'fr_name' : 'Translate Autodiff',
    'fr_addr' : "zhangjingjun@sogou-inc.com",
    'title' : title.encode('GBK'),
    'body' : mail_body.encode('GBK'), #use nl2br to adjust html-mail content.
    'mode' : "html",
    'maillist' : tlist,
    'attname' : attname,
    'attbody' : attbody
    }
    try:
        response = requests.get(mail_url,params=mail_Info)
        logstr.log_info('send mail success')
    except Exception as e:
        logstr.log_info("Send Mail ERROR. %s" % (e))
template_mail = """<html><head><style type="text/css">table{border-collapse:collapse;margin:0 auto;text-align:center;}table td,table th{border:1px solid #cad9ea;color:#666;height:30px;}table thead th{background-color:#CCE8EB;width:100px;}table tr:nth-child(odd){background:#fff;}table tr:nth-child(even){background:#F5FAFA;}</style></head><table width='90%' class='table'><thead><tr><th>ID</th><th>StartTime</th><th>EndTime</th><th>test_url</th><th>base_url</th><th>Finished</th><th>DiffNum</th><th>DiffRate(%)</th><th>Testtag</th><th>Detail</th></tr></thead>"""
temp_format = """<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a href="http://frontqa.web.sjs.ted/fy_xmldetail?tasknum=%d">Detail</a></td></tr></table></body></html>"""
if __name__ == '__main__':
    logstr = logUtils.logutil(task_id)
    subpid = os.getpid()
    set_subpid(subpid,1)
    (test_url,base_url,reqtype,queryip,queryuser,querypassw,querypath,user) = getInfoFromDb(task_id)
    getQueryFile(root_path)
    filename = os.path.basename(querypath)
    print(filename)
    getDiff(root_path,filename,task_id,base_url,test_url,reqtype)
    # send result by mail
    db = pymysql.connect(database_host,database_user,database_pass,database)
    cursor = db.cursor()
    sql = "SELECT id,start_time,end_time,test_url,base_url,user,diffnum,finished,testtag FROM %s where id='%d'" % ('fanyi_interfaceeval',task_id)
    cursor.execute(sql)
    (id,start_time,end_time,test_url,base_url,task_user,diffnum,finished,testtag) = cursor.fetchone()
    attname=''
    attbody=''
    tlist=list()
    tlist.append(task_user+'@Sogou-inc.com')
    title = '翻译XML自动化diff详情'
    result=0
    if finished!=0:
        result = round(float(diffnum)/float(finished)*100,2)
        mail_body = template_mail+ temp_format % (id,start_time,end_time,test_url,base_url,finished,diffnum,result,testtag,int(id))
    else:
        mail_body = template_mail+ temp_format % (id,start_time,end_time,test_url,base_url,finished,diffnum,'0',testtag,int(id))
    sendMail(title,mail_body,tlist,attname,attbody)
