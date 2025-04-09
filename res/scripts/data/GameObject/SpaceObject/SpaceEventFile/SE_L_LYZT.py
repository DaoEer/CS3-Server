# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "设置复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 169", 
                    "param1": "12550 -2360 3019", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "副本失败计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 10.0, 
                    "param3": "0", 
                    "param2": "900", 
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
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 436
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
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
    5: [
        {
            "title": "未完成阶段2，BOSS死亡副本通关", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 3
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 436
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000556:1", 
                    "param2": "0 0 43", 
                    "param1": "-6261 -1088 22138", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20008616:1", 
                    "param2": "0 0 0", 
                    "param1": "-7008 -1816 22138", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "cc", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20003140", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    8: [
        {
            "title": "阶段1完成换阶段2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 1
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 4, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "完成阶段2，副本通关", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 3
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 436
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000556:1", 
                    "param2": "0 0 43", 
                    "param1": "-6261 -1088 22138", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20008616:1", 
                    "param2": "0 0 0", 
                    "param1": "-7008 -1816 22138", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 4, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    15: [
        {
            "title": "进入范围2设置复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 100", 
                    "param1": "-21710 -4170 8640", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "8", 
                    "param3": "-21710 -4170 8640", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "9580|8060"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "进入范围3设置复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 149", 
                    "param1": "-9980 -2630 12186", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "8", 
                    "param3": "-9980 -2630 12186", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "13176|11556"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "进入范围4设置复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 119", 
                    "param1": "-4783 -2058 20117", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "6", 
                    "param3": "-4783 -2058 20117", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "20977|19097"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "触发传送回主场景", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "121544003", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "2", 
                    "param3": "-7008 -1816 22138", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "22700|22000"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "死亡触发传送回主场景", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "121544003", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "2", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "cc", 
                    "param2": "1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "2", 
                    "param3": "-7008 -1816 22138", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "22700|22000"
                }
            ], 
            "id": 5
        }
    ], 
    21: [
        {
            "title": "435", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 435
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ]
}