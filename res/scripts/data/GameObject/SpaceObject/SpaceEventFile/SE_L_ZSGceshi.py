# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "初始化出生点", 
            "describe": "初始化出生点", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "-8499 -6014 -834", 
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
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "1800", 
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
            "title": "重复同步", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 205
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "timestart", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
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
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "3", 
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
            "id": 2
        }
    ], 
    5: [
        {
            "title": "石像都死亡石墙降下第一波", 
            "describe": "石像都死亡石墙降下第一波", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "-27", 
                    "param1": "50000039", 
                    "param4": "", 
                    "id": 182
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "-5470 -6018 -834", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 22, 
                    "param1": "20007845|20007849|20007850|20007861", 
                    "param2": "2|3|2|1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "石像都死亡石墙降下第二波", 
            "describe": "石像都死亡石墙降下第二波", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "-27", 
                    "param1": "50000041", 
                    "param4": "", 
                    "id": 182
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 22, 
                    "param1": "20007858|20007862", 
                    "param2": "7|1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    8: [
        {
            "title": "阶段一完成地板碎裂", 
            "describe": "阶段一完成地板碎裂", 
            "actions": [
                {
                    "delayTime": 6.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20007852", 
                    "param4": "", 
                    "id": 130
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 15", 
                    "param1": "8837 3649 -5851", 
                    "param4": "", 
                    "id": 5
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
            "title": "阶段二完成石墙碎裂", 
            "describe": "阶段二完成石墙碎裂", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20007860", 
                    "param4": "", 
                    "id": 130
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 -179", 
                    "param1": "-993 3595 -1129", 
                    "param4": "", 
                    "id": 5
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
        }, 
        {
            "title": "副本阶段", 
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
                    "param3": "40000556:1", 
                    "param2": "0 0 -180", 
                    "param1": "-16088 3563 -1523", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20008616:1", 
                    "param2": "0 0 -180", 
                    "param1": "-14870 3577 -1523", 
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
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ], 
    14: [
        {
            "title": "接收123", 
            "describe": "接收123", 
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
                    "param1": "AI", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到指令地板下降", 
            "describe": "收到指令地板下降", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "30|8", 
                    "param2": "50000047", 
                    "param1": "20007859", 
                    "param4": "0|0|0", 
                    "id": 183
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "7859", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到指令重置地板", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "50000047", 
                    "param4": "", 
                    "id": 184
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "666", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到通知销毁交互地板", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "40000179|40000180|40000181", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "ZSGSPELL", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "收到通知销毁光墙", 
            "describe": "收到通知销毁光墙", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20003873", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "7846", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": ""
                }
            ], 
            "id": 5
        }
    ], 
    15: [
        {
            "title": "玩家进入范围升起石墙第一波", 
            "describe": "玩家进入范围升起石墙第一波", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "27", 
                    "param1": "50000038", 
                    "param4": "", 
                    "id": 182
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "7845", 
                    "param1": "20007845|20007861", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "7849", 
                    "param1": "20007849", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "7850", 
                    "param1": "20007850", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "27", 
                    "param1": "50000039", 
                    "param4": "", 
                    "id": 182
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "15", 
                    "param3": "-6794 -6021 -834", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "500|-1000"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家进入范围升起石墙第二波", 
            "describe": "玩家进入范围升起石墙第二波", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "27", 
                    "param1": "50000040", 
                    "param4": "", 
                    "id": 182
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "27", 
                    "param1": "50000041", 
                    "param4": "", 
                    "id": 182
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "7858", 
                    "param1": "20007858|20007862", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "15", 
                    "param3": "-2066 3588 -1129", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "500|-2000"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "进入范围播放镜头发送随机数", 
            "describe": "进入范围播放镜头发送随机数", 
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
                    "param2": "0 0 90", 
                    "param1": "393 -6553 -444", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000180:1", 
                    "param2": "0 0 90", 
                    "param1": "383 -5493 -444", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000181:1", 
                    "param2": "0 0 0", 
                    "param1": "1413 -6013 -444", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000472", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20007865|20007866|20007867|20007868", 
                    "param4": "", 
                    "id": 150
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "940 -6041 -434", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "400|-1000"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "进入二号boss前改变复活点", 
            "describe": "进入二号boss前改变复活点", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 -88", 
                    "param1": "4448 17095 -2008", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "4448 17095 -2008", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-1000|-3000"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "触发传送回主场景", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "121544014", 
                    "param4": "", 
                    "id": 16
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "2", 
                    "param3": "-14870 3577 -1523", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-1000|-1800"
                }
            ], 
            "id": 5
        }
    ], 
    21: [
        {
            "title": "同步岩浆", 
            "describe": "同步岩浆", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 205
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "180", 
                    "param1": "timestart", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }
    ]
}