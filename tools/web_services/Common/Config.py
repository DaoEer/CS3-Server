# -*- coding: utf-8 -*-
"""
配置
"""

from .Utils import loadJsonPathKeyString
web_server_config = loadJsonPathKeyString('Config/SettingConfig.json')	#设置配置

web_server_name = web_server_config["CurWebServer"]
g_ServerConfig = web_server_config[web_server_name]

