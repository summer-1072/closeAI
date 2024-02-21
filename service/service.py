import yaml
import argparse
from flask import Flask
from agent.api import doChat

parser = argparse.ArgumentParser()
parser.add_argument('--config', default='./config/config.yaml')
args = parser.parse_args()


def get_config(file):
    with open(file, 'r') as f:
        config = yaml.safe_load(f)

    return config


config = get_config(args.config)

# content = doGPT(config['api_key'], config['api_model'],
#                 "你是一名小红书的情感博主，帮我写一篇如何文案，内容是如何与异性交往")
