# -*- coding: utf-8 -*-
Datas = {
    8: [
        {
            "title": "玩家获得物品，播放语音，给陆压发送指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050092", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "huijia", 
                    "param1": "20012724", 
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
                    "id": 4, 
                    "param1": "6", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    30: [
        {
            "title": "Boss死亡喊话结束，给陆压发送指令jieshu", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "jieshu", 
                    "param1": "20012723|20012724", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050091", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 7.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11", 
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
                    "id": 52, 
                    "param1": "Q050090", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "Boss喊话结束，给Boss发指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "kaishi", 
                    "param1": "20012735", 
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
                    "param1": "Q050088", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    5: [
        {
            "title": "第1波小怪死完，延迟3秒召唤第2波怪物", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "kaishi1", 
                    "param1": "20012718", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "6", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "第2波小怪死完，延迟3秒召唤第3波怪物", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "kaishi2", 
                    "param1": "20012718", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "8", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 6.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050086", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "6", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "第3波小怪死完，延迟3秒召唤Boss", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "kaishi3", 
                    "param1": "20012718", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050087|Q050088", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "8", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }, 
        {
            "title": "Boss死亡喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050090", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20012718", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "10", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 4
        }
    ], 
    14: [
        {
            "title": "收到陆压的指令，延迟5秒召唤怪物", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "kaishi", 
                    "param1": "20012718", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 9.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050084|Q050085", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "1", 
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
                    "param3": "kaishi", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20012724"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到陆压的指令huijia，召唤传送门", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "huijia", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20012724"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到Boss的指令，播放语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050089", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "6", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20012735"
                }
            ], 
            "id": 3
        }
    ]
}