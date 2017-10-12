#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
import mysql.connector
import configuration
from common import error

class SMDBHelper:

    def __init__(self):
        user = configuration.SMDB_USER
        password = configuration.SMDB_PASSWORD
        host = configuration.SMDB_HOST
        database = configuration.SMDB_DATABASE
        self.smartDBCnx = mysql.connector.connect(user=user, password=password, host=host, database=database, charset='utf8')
        self.cursor = self.smartDBCnx.cursor()

    def get_all_account_data(self):
        #using queue to process with multi threads
        queue = Queue.Queue()
        try:
            accounts = []
            stmt_query = ("SELECT DISTINCT (index_key) AS account_id, account_name, m_api.name_slack FROM account_indexes "
                          "LEFT JOIN m_accounts ON m_accounts.promotion_code = concat(account_indexes.base_code,'_LAP') "
                          "LEFT JOIN m_api ON m_api.staff_name = m_accounts.consultant_staff_name WHERE media_code = 'LAP' "
                          "ORDER BY account_id")
            self.cursor.execute(stmt_query)
            data = self.cursor.fetchall()
            for acc in data:
                if acc[0].isdigit():
                    accounts.append(acc[0])
            #need to distinct the account list
            accounts = list(set(accounts))
            for account in accounts:
                queue.put(account)
            return queue
        except Exception as e:
            error(e)
        finally:
            self.cursor.close()
            self.smartDBCnx.close()
