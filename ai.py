### ФАЙЛ ИНТЕГРАЦИИ LLM С БОТОМ ###

import requests
import json
from pprint import pprint

from config_file import config


headers = {
    'Content-Type': 'application/json',
}

json_data = {
    'model': 'llama-3.2-3b-instruct',
    'messages': [
        {
            'role': 'system',
            'content': 'Говори всегда по русски',
        },
        {
            'role': 'user',
            'content': 'Introduce yourself.',
        },
    ],
    'temperature': 0.8,
    'max_tokens': -1,
    'stream': False,
}

response = requests.post(config.llm_url, headers=headers, json=json_data)

data = response.json()
pprint(data)

text = data['choices'][0]['message']['content']
print(text)

    
