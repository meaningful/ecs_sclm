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
# zsk数据库配置，用于写入数据
config = {
        'host': 'rds0d1o55s4h288856b2.mysql.rds.aliyuncs.com',
        'user': 'zsk',
        'password': 'ZSK12ab3456',
        'port': 3306,
        'database': 'zsk',
        'charset': 'utf8'
        }
#43 test 测试数据库
#config_shcm_app = {
#        'host': '47.93.228.118',
#        'user': 'root',
#        'password': 'WLW2017test',
#        'port': 3306,
#        'database': 'test',
#        'charset': 'utf8'
#        }

# shcm_app 数据库配置，仅用于查询
config_shcm_app = {
        'host': 'rds0d1o55s4h288856b2.mysql.rds.aliyuncs.com',
        'user': 'zsk',
        'password': 'ZSK12ab3456',
        'port': 3306,
        'database': 'shcm_app',
        'charset': 'utf8'
        }

# 查询zsk_userinfo表
#sql_tab_zsk_userinfo = 'SELECT agent_wx FROM zsk_userinfo WHERE open_id={0}'
# === sclm_app 中的tab Begin ===#
# 查询agent表
sql_tab_agent = 'SELECT agent_phone,agent_levelname FROM agent WHERE is_del=0 AND agent_wx={0} AND customerclass={1} '
# 查询authinfo表
sql_tab_authinfo = 'SELECT subagent_mbi,agent_levelname FROM authinfo WHERE sub_wx={0}'
# === sclm_app 中的tab End ===#
# 插入数据到 zsk_userinfo
#sql_tab_zsk_userinfo_insert = 'INSERT INTO zsk_userinfo(open_id,agent_wx) VALUES ({0},{1})'

# === zsk 中的tab Begin ===#
# Tab for customerclass = u'微信三草两木'
ZSK_TAB_USERINFO_SCLM = 'zsk_userinfo_sclm'

# Tab for customerclass = u'微信养面膜'
ZSK_TAB_USERINFO_YMM = 'zsk_userinfo_ymm'

# Tab for customerclass = u'微信清奕'
ZSK_TAB_USERINFO_QY = 'zsk_userinfo_qy'

# Tab for customerclass = u'微信珍慕'
ZSK_TAB_USERINFO_ZM = 'zsk_userinfo_zm'

# Tab for customerclass = u'微信Gbox'
ZSK_TAB_USERINFO_GBOX = 'zsk_userinfo_gbox'

# 查询zsk数据库的指定userinfo表
sql_query_zsk_userinfo_tab = 'SELECT agent_wx FROM {0} WHERE open_id={1}'

# 插入数据到zsk数据库指定的userinfo表
sql_insert_zsk_userinfo_tab = 'INSERT INTO {0}(open_id,agent_wx) VALUES ({1},{2})'

# === zsk 中的tab End===#

# 执行对 shcm_app DB 的查询语句
def query(sql):
    AppLog.info(TAG, "SQL:" + sql)
    conn = mysql.connector.connect(**config_shcm_app)
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


# 执行对 zsk DB 的查询语句
def query4zsk(sql):
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

# 执行对 zsk DB 的插入语句
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

