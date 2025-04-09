# -*- coding: utf-8 -*-
Datas = {
    5: [
        {
            "title": "boss死亡，死亡喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q032700|Q032701", 
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
                    "id": 2, 
                    "param1": "20003097", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    13: [
        {
            "title": "离开地图，删除物品", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "301010065", 
                    "param4": "", 
                    "id": 23
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "收到jinzhi1，完成阶段目标3", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "3", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 89
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "jinzhi1", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到jinzhi2，完成阶段目标1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "off", 
                    "param1": "20003075", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20003079", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "jinzhi2", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    15: [
        {
            "title": "到大门前，小怪喊话/阵师出场", 
            "describe": "阵师，有生人闯寨！", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q032690|Q032691|Q032692", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 1.5, 
                    "param3": "", 
                    "param2": "tiao", 
                    "param1": "20003080", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "30", 
                    "param3": "25877.7695 4308.917480 -1860.937256", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-1360|-2360"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "通过大门，播放语音Q032694", 
            "describe": "前方设有阵法禁制，无法通行。请从四周的箱子中找到阵符，解除禁制。", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q032694", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "20", 
                    "param3": "24806.5390 1864.9040 -1815.379395", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-1315|-2315"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "通过第一道禁制，旁白提示", 
            "describe": "小心避开追魂射线！寻找时机解除第二个禁制！", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q032695", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "on", 
                    "param1": "20003075", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "25", 
                    "param3": "11360.000000 -6230.000000 -1096.875244", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-596|-1596"
                }
            ], 
            "id": 3
        }
    ], 
    18: [
        {
            "title": "获得破界石，刷传送门", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "19", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 20, 
                    "param1": "301010064", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    30: [
        {
            "title": "Q032692结束，门口小怪进战", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "hit", 
                    "param1": "20003080|20003081", 
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
                    "id": 52, 
                    "param1": "Q032692", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ]
}