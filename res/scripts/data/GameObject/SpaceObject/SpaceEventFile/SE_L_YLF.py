# -*- coding: utf-8 -*-
Datas = {
    5: [
        {
            "title": "BOSS死亡", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q040383", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 22, 
                    "param1": "20005050", 
                    "param2": "1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "第一波扫描怪通知副本刷暗怪", 
            "describe": "第一波扫描怪通知副本刷暗怪（20005021|20005022）", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "20000779", 
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
                    "param3": "1", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005021|20005022"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "第二波扫描怪通知副本刷暗怪", 
            "describe": "第一波扫描怪通知副本刷暗怪（20005024|20005025|20005026）", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "20000779", 
                    "param1": "7", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005024|20005025|20005026"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "第四波扫描怪通知副本刷暗怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "20000779", 
                    "param1": "16", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005034|20005035|20005036|20005037"
                }
            ], 
            "id": 3
        }
    ], 
    15: [
        {
            "title": "玩家进入BOSS区域", 
            "describe": "玩家进入BOSS区域清除BUFF", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11001324|11001325|11001326|11003606", 
                    "param4": "", 
                    "id": 25
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q040379|Q040380|Q040382", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 1.0, 
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
                    "param4": "25", 
                    "param3": "5970 -24420 3045", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "9000|-2000"
                }
            ], 
            "id": 1
        }
    ], 
    17: [
        {
            "title": "清除BUFF", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11003606|11001324|11001325|11001326", 
                    "param4": "", 
                    "id": 25
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    21: [
        {
            "title": "玩家进入副本，提示喊话，加Buff", 
            "describe": "播放语音与给道具", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q040377", 
                    "param4": "", 
                    "id": 18
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11003606", 
                    "param4": "", 
                    "id": 33
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "进入副本时，玩家身上如果没有伪装服，则给", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "301010080", 
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
                    "param1": "301010080", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    24: [
        {
            "title": "进入战斗移除贴屏BUFF", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11003606", 
                    "param4": "", 
                    "id": 25
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 33, 
                    "param1": "3", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 38, 
                    "param1": "11003606", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "进入自由增加贴屏BUFF", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11003606", 
                    "param4": "", 
                    "id": 33
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 33, 
                    "param1": "1", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 39, 
                    "param1": "11001324|11001325|11001326|11003606", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    30: [
        {
            "title": "提示喊话结束，刷传送门", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "29", 
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
                    "param1": "Q041212", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "Q040382喊话结束，通知20005050", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "323", 
                    "param1": "20005050", 
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
                    "param1": "Q040382", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "死亡喊话结束，喊提示语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q041212", 
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
                    "id": 52, 
                    "param1": "Q040383", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ]
}