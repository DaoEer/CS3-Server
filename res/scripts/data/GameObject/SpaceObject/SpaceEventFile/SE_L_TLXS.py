# -*- coding: utf-8 -*-
Datas = {
    2: [
        {
            "title": "循环刷雪球", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "7", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "time", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    3: [
        {
            "title": "玩家身上无道具，任务未完成，添加道具", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "301010112", 
                    "param4": "", 
                    "id": 42
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 42, 
                    "param1": "301010112", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 16, 
                    "param1": "20102138", 
                    "param2": "3"
                }
            ], 
            "id": 1
        }
    ], 
    5: [
        {
            "title": "Boss死亡，给怪物发送指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "222", 
                    "param1": "20009257", 
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
                    "param1": "20009254", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    8: [
        {
            "title": "放完风雨苍穹，刷出Boss", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "6", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q042551|Q045291|Q045293|Q045294", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "time", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11042701", 
                    "param4": "", 
                    "id": 26
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "301010112", 
                    "param4": "", 
                    "id": 24
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
        }, 
        {
            "title": "第1批怪物死亡，开启机关，刷精英", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "5", 
                    "param1": "time", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "7", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "8", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
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
                    "id": 4, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    14: [
        {
            "title": "收到怪物通知，销毁怪物脚下的陷阱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "30000631", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "665", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20009254"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到风雨苍穹的通知，给玩家宝物，刷传送门", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "301010113", 
                    "param4": "", 
                    "id": 43
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "20009258:1", 
                    "param2": "0 0 0", 
                    "param1": "8776.0 15878.0 492.0", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q042553", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "43", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20009257"
                }
            ], 
            "id": 2
        }
    ], 
    15: [
        {
            "title": "玩家进入第4批小怪范围，刷新怪物", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "20.0", 
                    "param3": "-2641.585205 5771.585449 -575.278320", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "0|-1000"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家进入范围，贴屏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11042701", 
                    "param4": "", 
                    "id": 33
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q042550", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "4|5", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "5", 
                    "param3": "7450.000000 15070.000000 460.000000", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|0"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "玩家进入陷阱范围，播放喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q042686", 
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
            "triggerConditions": [
                {
                    "param4": "15", 
                    "param3": "-3979.0 -15916.999999999998 -1138.0", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "0|-2000"
                }
            ], 
            "id": 3
        }
    ], 
    30: [
        {
            "title": "Q045293语音结束，给Boss发送指令，给玩家添加Buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "226", 
                    "param1": "20009254", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11043601", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 52, 
                    "param1": "Q045293", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ]
}