from Utils.colors import *

import json, sys

loadedConfigs = 0

class Config:
    @property
    def AppName(self):
        with open('Assets/settings.json', 'r') as file:
            data = json.load(file)
        return data['Branding']['AppName']
    
    @property
    def ClientName(self):
        with open('Assets/settings.json', 'r') as file:
            data = json.load(file)
        return data['Branding']['ClientName']
    
    @property
    def Power(self):
        with open('Assets/settings.json', 'r') as file:
            data = json.load(file)
        return data['Branding']['Links']['Power']
    
    @property
    def News(self):
        with open('Assets/settings.json', 'r') as file:
            data = json.load(file)
        return data['Branding']['Links']['News']
    
    @property
    def Support(self):
        with open('Assets/settings.json', 'r') as file:
            data = json.load(file)
        return data['Branding']['Links']['Support']

    @property
    def Token(self):
        with open('Assets/settings.json', 'r') as file:
            data = json.load(file)
        return data['Settings']['Token']
    
    @property
    def NotifyToken(self):
        with open('Assets/settings.json', 'r') as file:
            data = json.load(file)
        return data['Settings']['NotifyToken']
    
    @property
    def Admins(self):
        with open('Assets/settings.json', 'r') as file:
            data = json.load(file)
        return data['Settings']['Admins']
    
    @property
    def Version(self):
        with open('Assets/settings.json', 'r') as file:
            data = json.load(file)
        return data['Settings']['Version']
    
    @property
    def MaxSlots(self):
        with open('Assets/settings.json', 'r') as file:
            data = json.load(file)
        return data['Settings']['MaxSlots']
    
    @property
    def Maintenance(self):
        with open('Assets/settings.json', 'r') as file:
            data = json.load(file)
        return data['Settings']['Maintenance']
    
    @property
    def Blacklists(self):
        with open('Assets/settings.json', 'r') as file:
            data = json.load(file)
        return data['Attack']['Blacklists']
    
    @property
    def Plans(self):
        with open('Assets/settings.json', 'r') as file:
            data = json.load(file)
        return data['Plans']
    

class Methods:
    @property
    def Methods(self):
        with open('Assets/methods.json', 'r') as file:
            data = json.load(file)
        return data['Methods']
    

class Servers:
    @property
    def Servers(self):
        with open('Assets/servers.json', 'r') as file:
            data = json.load(file)
        return data['Servers']
    

try:
    loadedConfigs += 1
    config = Config()
except Exception as e:
    print(f'{c.lred}[JSON] {c.reset}Config error: {c.lred} [ config.json - {e}]{c.reset}')

try:
    loadedConfigs += 1
    methods = Methods()
except Exception as e:
    print(f'{c.lred}[JSON] {c.reset}Config error: {c.lred} [ methods.json - {e}]{c.reset}')

try:
    loadedConfigs += 1
    servers = Servers()
except Exception as e:
    print(f'{c.lred}[JSON] {c.reset}Config error: {c.lred} [ servers.json - {e}]{c.reset}')