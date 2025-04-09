# -*- coding: utf-8 -*-
Datas = {
    16: [
        {
            "title": "四次后完成任务", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "80135025", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 70
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "t2", 
                    "param4": "", 
                    "id": 13
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "key", 
                    "param2": "4"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "完成任务后十秒倒计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "10", 
                    "param1": "t1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 46
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000117|Cy000118", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_FLS", 
                    "param4": "", 
                    "id": 20
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "key", 
                    "param2": "4"
                }
            ], 
            "id": 2
        }
    ], 
    2: [
        {
            "title": "时间到达传送出副本", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_FLS", 
                    "param4": "", 
                    "id": 20
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
        }, 
        {
            "title": "副本剩余十秒倒计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 46
                }, 
                {
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_FLS", 
                    "param4": "", 
                    "id": 20
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 25, 
                    "param1": "t2", 
                    "param2": "10"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    3: [
        {
            "title": "弹出开始按钮", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 61
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "刷出初始三个欢乐鼎", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "10000298", 
                    "param2": "8", 
                    "param1": "-12719.205078 -14133.180664 7171.772461", 
                    "param4": "3", 
                    "id": 58
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "开始副本计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "1", 
                    "param1": "t2", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 47
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }
    ], 
    14: [
        {
            "title": "欢乐鼎开始", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "10000298", 
                    "param1": "100324", 
                    "param4": "", 
                    "id": 59
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "10000298", 
                    "param2": "8", 
                    "param1": "-12719.205078 -14133.180664 7171.772461", 
                    "param4": "100325", 
                    "id": 60
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "START", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "接下来所有的小鼎会打乱次序，请找到最开始发出光亮的小鼎。", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000116", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }
    ]
}