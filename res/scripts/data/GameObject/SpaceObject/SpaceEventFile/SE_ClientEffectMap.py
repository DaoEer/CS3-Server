# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "刷出福袋", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "10000901:1|10000902:1|10000981:1|10000916:1|10000980:1|10000918:1|10000921:1", 
                    "param2": "-198 1834|1503 1805|1544 86|-196 156", 
                    "param1": "100|1000|1100", 
                    "param4": "", 
                    "id": 282
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "1", 
                    "param1": "start", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "设置光圈初始信息", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "10", 
                    "param1": "2750 1000 0", 
                    "param4": "", 
                    "id": 211
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "1", 
                    "param1": "light_reduce", 
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
            "title": "福袋开始下落", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10000901|10000902|10000981|10000916|10000980|10000918|10000921", 
                    "param4": "", 
                    "id": 219
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "start", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "光圈缩小", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "5", 
                    "param2": "1", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 213
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 214
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 215
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "7", 
                    "param1": "light_expand", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "light_reduce", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "光圈扩大", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "10", 
                    "param2": "5", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 213
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 214
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 215
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "5", 
                    "param1": "light_reduce", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "light_expand", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ], 
    3: [
        {
            "title": "开始充能效果", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 121
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "显示光圈", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 212
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    6: [
        {
            "title": "摆钟", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20007868", 
                    "param4": "", 
                    "id": 150
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20007868", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    12: [
        {
            "title": "重新刷福袋", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "1", 
                    "param1": "start", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10000901|10000902|10000981|10000916|10000980|10000918|10000921", 
                    "param4": "", 
                    "id": 220
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000901|10000902|10000981|10000916|10000980|10000918|10000921", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "场景物件交互通知", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 185
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    15: [
        {
            "title": "创建spellbox交互", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "3", 
                    "param2": "3", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 131
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000179:1", 
                    "param2": "0 0 0", 
                    "param1": "2354.0 10021 110", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000180:1", 
                    "param2": "0 0 90", 
                    "param1": "2361 11085 110", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000181:1", 
                    "param2": "0 0 0", 
                    "param1": "3349 10564 110", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "2631 10555.4248047 102", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "400|-1000"
                }
            ], 
            "id": 1
        }
    ]
}