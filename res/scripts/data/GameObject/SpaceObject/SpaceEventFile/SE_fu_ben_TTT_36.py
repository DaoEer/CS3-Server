# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "初始化副本复活点", 
            "describe": "", 
            "actions": [], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "副本失败计时", 
            "describe": "5分钟失败计时", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "300", 
                    "param1": "shibai", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    2: [
        {
            "title": "时间到达未完成副本", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 4
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "shibai", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "101创建怪物（废弃）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20013573:1", 
                    "param2": "0 0 0", 
                    "param1": "888 -6615 1793", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20013574:1", 
                    "param2": "0 0 0", 
                    "param1": "1090 -6612 3035", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20013580:1", 
                    "param2": "0 0 0", 
                    "param1": "888 -6615 1793", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20013576:1", 
                    "param2": "0 0 0", 
                    "param1": "2173 -4610 1679", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20013577:1", 
                    "param2": "0 0 0", 
                    "param1": "2633 -7973 1276", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20013578:1", 
                    "param2": "0 0 0", 
                    "param1": "-568 -8558 1681", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20013579:1", 
                    "param2": "0 0 0", 
                    "param1": "-1879 -5680 1679", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20013581:1", 
                    "param2": "0 0 0", 
                    "param1": "1090 -6612 3035", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20013582:1", 
                    "param2": "0 0 0", 
                    "param1": "1090 -6612 3035", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20013583:1", 
                    "param2": "0 0 0", 
                    "param1": "1090 -6612 3035", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20013575:1", 
                    "param2": "0 0 0", 
                    "param1": "1090 -6612 3035", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1000", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "102通知开始发射光纤", 
            "describe": "102通知开始发射光纤", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "122278017|122278017|122278017|122278017|122278017", 
                    "param2": "20013580|20013576|20013577|20013578|20013579", 
                    "param1": "20013574|20013575|20013581|20013582|20013583", 
                    "param4": "", 
                    "id": 290
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "102", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ]
}