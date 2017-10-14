# -*- coding:utf-8 -*-
import mysql.connector
import os
import sys
from .log import AppLog


reload(sys)
sys.setdefaultencoding('utf-8')


# TAG -- 当前文件名
TAG = os.path.basename(__file__)

# 数据库连接配置
config = {
        'host': '47.93.228.118',
        'user': 'root',
        'password': 'WLW2017test',
        'port': 3306,
        'database': 'test',
        'charset': 'utf8'
        }


# 查询zsk_userinfo表
sql_tab_zsk_userinfo = 'SELECT agent_wx FROM zsk_userinfo WHERE open_id={0}'
# 查询agent表
sql_tab_agent = 'SELECT agent_phone,agent_levelname FROM agent WHERE is_del=0 AND agent_wx={0} AND customerclass={1} '
# 查询authinfo表
sql_tab_authinfo = 'SELECT subagent_mbi,agent_levelname FROM authinfo WHERE sub_wx={0}'
# 插入数据到 zsk_userinfo
# TODO：修改sql语句，避免重复插入
sql_tab_zsk_userinfo_insert = 'INSERT INTO zsk_userinfo(open_id,agent_wx) VALUES ({0},{1})'


# 执行查询语句
def query(sql):
    AppLog.info(TAG, "SQL:" + sql)
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    try:
        if conn and cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except mysql.connector.Error as e:
        AppLog.error(TAG, 'Query fail!{0}'.format(e))
    
    finally:
        cursor.close()
        conn.close()


def insert(sql):
    AppLog.info(TAG, "SQL:" + sql)
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    try:
        if conn and cursor:
            cursor.execute(sql)
            conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        AppLog.error(TAG, 'Insert fail!{0}'.format(e))

    finally:
        cursor.close()
        conn.close()

