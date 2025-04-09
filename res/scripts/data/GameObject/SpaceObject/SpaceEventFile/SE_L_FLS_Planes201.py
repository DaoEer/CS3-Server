# -*- coding: utf-8 -*-
Datas = {
    2: [
        {
            "title": "5秒倒计时结束后，玩法开始", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 47
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "-109491.9 -64910.3 1307.6", 
                    "param2": "-113481.8 -62479.6 1528.9", 
                    "param1": "-109628.4 -60174 1589.6", 
                    "param4": "20003155|3", 
                    "id": 49
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000121", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "t1", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    3: [
        {
            "title": "进入副本，开始5秒倒计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "0", 
                    "param2": "5", 
                    "param1": "t1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 46
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000124", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    8: [
        {
            "title": "抓捕了12只灵兽后，送玩家离开副本", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 3
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_FLS", 
                    "param4": "", 
                    "id": 20
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000123", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    12: [
        {
            "title": "灵兽被禁锢抓捕后，完成一次任务目标", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "80135032", 
                    "param4": "", 
                    "id": 2
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 23, 
                    "param1": "20003155", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "收到通知1刷6个灵兽", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "-109491.9 -64910.3 1307.6", 
                    "param2": "-113481.8 -62479.6 1528.9", 
                    "param1": "-109628.4 -60174 1589.6", 
                    "param4": "20003155|6", 
                    "id": 49
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20003156"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到通知2刷9个灵兽", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "-109491.9 -64910.3 1307.6", 
                    "param2": "-113481.8 -62479.6 1528.9", 
                    "param1": "-109628.4 -60174 1589.6", 
                    "param4": "20003155|9", 
                    "id": 49
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20003156"
                }
            ], 
            "id": 2
        }
    ], 
    17: [
        {
            "title": "玩家未完成任务时离开副本，重置任务目标", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 4
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "80135032", 
                    "param4": "", 
                    "id": 30
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ]
}