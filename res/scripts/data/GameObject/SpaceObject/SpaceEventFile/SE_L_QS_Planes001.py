# -*- coding: utf-8 -*-
Datas = {
    17: [
        {
            "title": "玩家离开副本时，检测玩家任务状态，如果后一个任务开始，则播放镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000731", 
                    "param4": "", 
                    "id": 16
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 16, 
                    "param1": "20102183", 
                    "param2": "3"
                }
            ], 
            "id": 1
        }
    ], 
    5: [
        {
            "title": "Boss死亡，喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050118", 
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
                    "param1": "20012761", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "第2波小怪死完了，召唤精英", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 27
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
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    30: [
        {
            "title": "第1波小怪喊话结束，给小怪发指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20012750|20012751", 
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
                    "param1": "Q050109", 
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
                    "param2": "2", 
                    "param1": "20012761", 
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
                    "param1": "Q050116", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "Boss死亡喊话结束，玩家完成任务/阶段，出位面", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102182", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_QS", 
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
                    "id": 52, 
                    "param1": "Q050118", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ], 
    15: [
        {
            "title": "玩家进入第1波范围，喊话，给小怪发送指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20012750|20012751", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050106|Q050107|Q050109", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "6", 
                    "param3": "6497.830078 -23512.070313 758.108887", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "2758|-2728"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家进入第2波范围，招第2波小怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "8", 
                    "param3": "1047.526611 -24631.587891 2300.364502", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "5000|0"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "玩家进入第3波范围，招第3波小怪", 
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
                    "delayTime": 2.0, 
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
                    "param4": "15", 
                    "param3": "-8373.888672 280.956268 8469.988281", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "11111|6666"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "玩家进入Boss范围，喊话，给Boss发送指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20012761", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q050111|Q050112|Q050114|Q050116", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "10", 
                    "param3": "720.065369 1582.040283 10173.668945", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "12000|8000"
                }
            ], 
            "id": 4
        }
    ]
}