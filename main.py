# !/env/bin/python3
# -*- coding: utf-8 -*-
import threading
import time
import requests
import pandas as pd
import logging

data_persons = {
    'genero':[],
    'nombre completo':[],
    'email': [],
    'edad': [],
}

logging.basicConfig(
    level = logging.INFO,
    format='%(message)s'
)


def error():
    logging.error('Ops Lo siento error de Conexion')


def get_user(error_callback):
    try:
        url = 'https://randomuser.me/api/'
        response = requests.get(url)
        if response.status_code == 200:
            payload = response.json()
            results = payload.get('results',[])
            for value in results:
                data_persons['genero'].append(value['gender'])
                data_persons['nombre completo'].append(f"{value['name']['title']}. {value['name']['first']} {value['name']['last']}")
                data_persons['email'].append(value['email'])
                data_persons['edad'].append(value['dob']['age'])
            data_persons['edad'] = sorted(data_persons['edad'],reverse=True)
    except requests.exceptions.ConnectionError:
        error_callback()


def save_data():
    for i in range(10):
        time.sleep(1)
        t = threading.Thread(target=get_user,kwargs={
            'error_callback':error,
        })
        t.start()
    df = pd.DataFrame(data_persons)
    df.to_excel('data_person.xlsx')

if __name__ == "__main__":
    save_data()
