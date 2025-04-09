# -*- coding: utf-8 -*-
Datas = {
    8: [
        {
            "title": "象驳死，完成任务", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102031", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "0", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "4", 
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
            "title": "收指令3，出位面", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_BQDB", 
                    "param4": "", 
                    "id": 20
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005006"
                }
            ], 
            "id": 1
        }
    ], 
    15: [
        {
            "title": "玩家进入，刷第二波", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "20000779", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "15", 
                    "param3": "-5383.490723 41338.347656 -1144.525635", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "2000|-2000"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家进入，刷第三波的暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "20000779", 
                    "param1": "3", 
                    "param4": "20004689:3", 
                    "id": 28
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "10", 
                    "param3": "-13159.936523 40349.097656 -704.108398", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "2000|-1000"
                }
            ], 
            "id": 2
        }
    ]
}