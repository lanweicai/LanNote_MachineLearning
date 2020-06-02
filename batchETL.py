#!/usr/bin/env python
#coding:utf-8
#batchEtl.py

import sys
from config import *
from SqlServer import SqlServer
from subprocess import Popen
from constant import *

from multiprocessing.pool import ThreadPool 

def batch():
    cf=Config(SCHED_CONF_HOME+'/config.ini')
    odsdb=cf.getdics("ods")
    # sql='''SELECT d.name FROM sysobjects d where d.xtype= 'U' and d.name like 'STG%' '''
    sql='''SELECT d.name FROM sysobjects d where d.xtype= 'U' and d.name like 'aa' '''
    
    db=SqlServer(odsdb)
    data=db.queryAll(sql)
    
    sh_template='Rmdb2Rmdb.py -OP ods -OT {0} -DP mysql -DT {0} -T'
    for d in data:
        tbl_name=d['name']

        cmd=sh_template.format(tbl_name)
        # print(cmd)
        pool.apply_async(execDatax,args=(tbl_name,cmd))
        

fail_msg=''
def execDatax(tbl_name,cmd):
    global fail_msg
    print('开始同步表:'+tbl_name)
    p1 = Popen(cmd,shell=True,close_fds=True) 
    p1.communicate()
    ret= p1.returncode
    if ret==0:
        print('同步表成功:'+tbl_name)
    else:
        fail_msg+='同步表失败:'+tbl_name
        fail_msg+='\n'  

max_worker_task_running=6
if __name__ == '__main__':   
    pool = ThreadPool(max_worker_task_running)
    
    batch()
    pool.close()
    pool.join()

    
    print('完成stg任务采集')
    
    if fail_msg:
        print(fail_msg)
        