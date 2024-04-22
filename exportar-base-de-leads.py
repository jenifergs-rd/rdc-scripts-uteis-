import os
import sys
import re
import json
from datetime import datetime
from urllib.parse import unquote
import pandas as pd
from pymongo import MongoClient
from bson import ObjectId


'''
SAMPLE COMMAND LINE ARGS

[ 1 - HOMO CLOUDFRONT ]: https://teste-tallos.tallos.com.br/"
[ 2 - PROD CLOUDFRONT ]: https://tallos-chat.s3.tallos.com.br/

1 - python3 ExecuteMessagesBackupTallos.py "https://teste-tallos.tallos.com.br/" "5bb2871f3a75602b5f5eb960"
2 - python3 ExecuteMessagesBackupTallos.py "https://teste-tallos.tallos.com.br/" "5bb2871f3a75602b5f5eb960" whatsapp telegram
'''

ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]|[\x00-\x1f\x7f-\x9f]|[\uffff]')

# FILTERS
args = sys.argv
cloud_front_base_url = args[1]
company = args[2]
#company = ObjectId('5bb2871f3a75602b5f5eb960')  # Mock company


valid_channels = ['whatsapp', 'messenger', 'telegram', 'email', 'instagram', 'megasac']
invalid_channels = ['invalid', 'error', 'undefined']

default_channels = valid_channels + invalid_channels
filter_channels = args[3:]  # whatsapp messenger telegram email instagram megasac invalid error

valid_message_types = ['text', 'image', 'audio', 'video', 'doc']
valid_message_sent_by = ['customer', 'bot', 'operator']

# CONVERTING COMPANY ID TO ObjectId
company = ObjectId(company)  # Real company


def create_channels_directory(channels):
    for channel in channels:
        if channel in invalid_channels:
            channel = 'invalid'
        
        if not os.path.exists(channel):
            os.makedirs(channel)


# DATABASE CONNECTION AND COLLECTIONS
mongo = MongoClient('mongodb://developer:Edn2ZvxWFKgPdE5LLA4dZPSM@mongo01.cloud.dns.internal:27017/tallos-megasac?authSource=admin')
db = mongo.get_database('tallos-megasac')

customers_collection = db.get_collection('customers')
messages_collection = db.get_collection('messages')
employees_collection = db.get_collection('employees')
tags_collection = db.get_collection('tags')


def get_safe_string(text_str):
    if not text_str or not type(text_str) is str:
        return ''
    
    return ILLEGAL_CHARACTERS_RE.sub('', text_str.strip())


def get_message_type(message_type):
    if not message_type or not type(message_type) is str:
        return 'doc'
    
    customer_phone = get_safe_string(customer_phone).lower()
    
    if message_type == 'text':
        message_type = 'texto'
    elif message_type == 'image':
        message_type = 'imagem'
    elif message_type == 'audio':
        message_type = 'audio'
    elif message_type == 'video':
        message_type = 'video'
    else:
        message_type = 'documento'

    return message_type


def get_message_sent_by(message_sent_by):
    if not message_sent_by or not type(message_sent_by) is str:
        return 'bot'
    
    message_sent_by = get_safe_string(message_sent_by).lower()
    
    if message_sent_by == 'customer':
        message_sent_by = 'cliente'
    elif message_sent_by == 'operator':
        message_sent_by = 'funcionário'
    else:
        message_sent_by = 'bot'
    
    return message_sent_by


def get_message_content(message_type, content):
    if message_type == 'text':
        return str(content).strip()

    if type(content) == dict:
        return f'{cloud_front_base_url}{content.get("file_path", "")}'

    if not content:
        return ''

    try:
        content = json.loads(unquote(content))
        file_path = content.get('file_path', '')

        if file_path:
            return f'{cloud_front_base_url}{file_path}'

        return ''
    except:
        return ''

def get_customer_phone(customer_phone):
    if not customer_phone or not type(customer_phone) is str:
        return ''

    customer_phone = get_safe_string(customer_phone)
    customer_phone = re.sub('\D+', '', customer_phone)
    return customer_phone


def get_customer_tags(customer_tags):
    tags_ids = []
    
    for tag in customer_tags:
        try:
            tag_id = ObjectId(tag)
            tags_ids.append(tag_id)
        except:
            pass
    
    customer_tags = tags_collection.distinct('name', {'_id': {'$in': tags_ids}})
    customer_tags = [get_safe_string(tag) for tag in customer_tags]
    customer_tags = '; '.join(customer_tags)    
    return customer_tags


def get_customer_channel(customer_channel='invalid'):
    if not type(customer_channel) is str:
        return 'invalid'
    
    customer_channel = get_safe_string(customer_channel).lower()
    
    if not customer_channel or customer_channel in invalid_channels:
        customer_channel = 'invalid'
    
    return customer_channel


def get_date_as_str(date):
    return datetime.strftime(date,'%d/%m/%Y %H:%M:%S')


def get_messages_employees(customer_id):
    employees_ids = messages_collection.distinct('employee', {'customer': customer_id})
    
    employees_valid_ids = []
    
    for employee_id in employees_ids:
        try:
            if employee_id:
                employee_id = ObjectId(employee_id)
                employees_valid_ids.append(employee_id)
        except:
            pass    

    found_employees = list(employees_collection.find({'_id': {'$in': employees_valid_ids}}, {'name': 1}))

    employees = dict()
    
    for employee in found_employees:
        employee_id = str(employee['_id'])
        employees[employee_id] = get_safe_string(employee['name'])
    
    return employees


def save_customer_messages(customer_id, customer_name, customer_channel):
    skip = 0
    limit = 1000
    
    messages_employees = get_messages_employees(customer_id)

    messages_total = messages_collection.count_documents({'customer': customer_id})
    messages_resting = messages_total
    
    messages_file_path = f'{customer_channel}/mensagens_{customer_id}.xlsx'
    
    messages_to_excel = []

    print(f'TOTAL OF MESSAGES: {messages_resting}\n')

    while messages_resting:
        messages = messages_collection.find(
            {'customer': customer_id},
            {'content': 1, 'type': 1, 'sent_by': 1, 'employee': 1, 'created_at': 1}
        ).skip(skip).limit(limit)
        
        for message in messages:
            message_id = message['_id']            
            message_type = get_safe_string(message.get('type', ''))
            message_content = get_message_content(message_type, message.get('content', ''))
            message_sent_by = get_safe_string(message.get('sent_by', ''))
            message_employee_id = str(message.get('employee', ''))
            message_created_at = get_date_as_str(message.get('created_at', ''))

            messages_resting -= 1
            print(f'{message_id} - RESTING: {messages_resting}')
            
            message_to_excel = {
                'CONTEÚDO': message_content,
                'TIPO': message_type,
                'DATA DE ENVIO': message_created_at,
                'ENVIADO POR': message_sent_by,
                'NOME DO CLIENTE': '',
                'NOME DO OPERADOR': ''
            }
            
            if message_sent_by == 'customer':
                message_to_excel['NOME DO CLIENTE'] = customer_name
            elif message_sent_by == 'operator':
                message_to_excel['NOME DO OPERADOR'] = messages_employees.get(message_employee_id, 'Funcionário deletado')

            messages_to_excel.append(message_to_excel)

        skip += limit
        
    print(f'\n{"-"*150}\n')

    try:
        if messages_total:
            df = pd.DataFrame(messages_to_excel)
            df.to_excel(messages_file_path, index=False, sheet_name='mensagens')

        return messages_total, messages_file_path
    except:
        pass

    return messages_total, 'Contato sem mensagens'


def do_backup(channels):
    create_channels_directory(channels)
    
    skip = 0
    limit = 1000
    page = 0
    
    customers_resting = customers_collection.count_documents({'company': company, 'channel': {'$in': channels}})
    
    while customers_resting:
        customers = customers_collection.find(
            {'company': company, 'channel': {'$in': channels}},
            {'full_name': 1, 'cel_phone': 1, 'email': 1, 'channel': 1, 'tags': 1, 'created_at': 1}
        ).limit(limit).skip(skip)

        customers_to_excel = []

        for customer in customers:
            customer_id = customer['_id']
            customer_name = get_safe_string(customer.get('full_name', ''))
            customer_phone = get_customer_phone(customer.get('cel_phone', ''))
            customer_email = get_safe_string(customer.get('email', ''))
            customer_channel = get_customer_channel(customer.get('channel', ''))
            customer_tags = get_customer_tags(customer.get('tags', ''))
            customer_created_at = get_date_as_str(customer.get('created_at', ''))

            customers_resting -= 1
            print(f'>>>> {customer_id} | {customer_channel} | RESTING CUSTOMERS: {customers_resting} <<<<\n')

            messages_total, messages_file_path = save_customer_messages(customer_id, customer_name, customer_channel)
            
            customer_to_excel = {
                'NOME': customer_name,
                'TELEFONE': customer_phone,
                'EMAIL': customer_email,
                'CANAL': customer_channel,
                'TAGS': customer_tags,
                'DATA DE CRIAÇÃO': customer_created_at,
                'TOTAL DE MENSAGENS': messages_total,
                'ARQUIVO DE MENSAGENS': messages_file_path
            }

            customers_to_excel.append(customer_to_excel)

        page += 1
        skip += limit

        customers_file_path = f'contatos_pagina_{str(page)}.xlsx'

        df = pd.DataFrame(customers_to_excel)
        df.to_excel(customers_file_path, index=False, sheet_name='contatos')


if len(filter_channels):
    do_backup(filter_channels)
else:
    do_backup(default_channels)