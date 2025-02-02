import yaml
from icecream import ic


def run():
    with open("scripts/data.yaml", "r", encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    ic(data)