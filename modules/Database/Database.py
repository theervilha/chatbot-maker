import psycopg2
from psycopg2.extras import execute_values

from dotenv import dotenv_values

import pandas as pd

class Database():
    message_table = 'message'
    chat_table = 'chat'
    query_insert_chat = f"""INSERT INTO {chat_table} (id, channel_token, created_at) VALUES (%s, %s, %s)"""
    query_select_chat = f"""SELECT id FROM {chat_table} WHERE id = %s AND channel_token = %s"""
    query_insert_message = f"""INSERT INTO {message_table} (chat_id, session_id, node, user_message, bot_response, created_at_user_message, created_at_bot_response) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    query_select_message = f"""SELECT * FROM {message_table} WHERE chat_id = %s"""

    def __init__(self, 
                 host=dotenv_values(".env").get('host_database'),
                 dbname=dotenv_values(".env").get('dbname_database'),
                 user=dotenv_values(".env").get('user_database'),
                 password=dotenv_values(".env").get('password_database')):
        self.conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
        self.cur = self.conn.cursor()      


    def insert_chats(self, values):
        execute_values(self.cur, self.query_insert_message, values)
        self.commit()
        
    def insert_messages(self, values):
        execute_values(self.cur, self.query_insert_chat, values)
        self.commit()
    
    def insert_chat(self, values):
        if not self.exists_chat_id_in_database(values):
            self.cur.execute(self.query_insert_chat, values)
            self.commit()
    
    def exists_chat_id_in_database(self, values):
        self.cur.execute(self.query_select_chat, values[:2])
        return self.cur.fetchall()
        
    def insert_message(self, values):
        self.cur.execute(self.query_insert_message, values)
        self.commit()

    def get_messages_from_chat_id(self, chat_id):
        self.cur.execute(self.query_select_message % chat_id)
        return pd.DataFrame(self.cur.fetchall(), columns=['id', 'chat_id', 'session_id', 'node', 'user_message', 'bot_response', 'created_at_user_message', 'created_at_bot_response'])

    def commit(self):
        self.conn.commit()
    
    def close_db(self):
        self.cur.close()
        self.conn.close()