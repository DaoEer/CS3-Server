# -*- coding: utf-8 -*-
Datas = {
    3: [
        {
            "title": "玩家完成《下界试炼》任务目标，刷怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 20.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 30.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 40.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11078101", 
                    "param4": "", 
                    "id": 33
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    5: [
        {
            "title": "播放语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q011393|Q011403|Q011405|Q011406|Q011407", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "1|2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    7: [
        {
            "title": "陆桀血量低于50%时，给玩家物品，喊话，给陆桀发指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 6.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "301010171", 
                    "param4": "", 
                    "id": 43
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q012231", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "555", 
                    "param1": "20010620", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20010620", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 1, 
                    "param1": "0.5", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "收到镜头指令，给怪物发送指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20101035", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "111", 
                    "param1": "20010618|20010619|20010620|20010621", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "12345", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "536"
                }
            ], 
            "id": 1
        }
    ], 
    17: [
        {
            "title": "有道具，删除道具", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "301010171", 
                    "param4": "", 
                    "id": 23
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 20, 
                    "param1": "301010171", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "有新手保护，删除", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11078101", 
                    "param4": "", 
                    "id": 25
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 38, 
                    "param1": "11078101", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    30: [
        {
            "title": "语音播放完，完成任务，出位面", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_PGDT", 
                    "param4": "", 
                    "id": 20
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20101036", 
                    "param4": "", 
                    "id": 2
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 52, 
                    "param1": "Q011407", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ]
}