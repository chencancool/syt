import os
import json

with open('data.json', 'r' , encoding='utf8') as f:
    product = json.load(f)

print(product)