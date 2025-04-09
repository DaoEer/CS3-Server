# -*- coding: utf-8 -*-
Datas = {
    5: [
        {
            "title": "批次一死亡，刷批次二", 
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
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "批次2死亡，刷批次3", 
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
    14: [
        {
            "title": "BOSS血量低于20%投降喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20101666", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "102", 
                    "param1": "20011658", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_FMNL", 
                    "param4": "", 
                    "id": 20
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "chu", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20002789"
                }
            ], 
            "id": 1
        }
    ], 
    30: [
        {
            "title": "第一波喊话结束，通知小怪打玩家", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "100", 
                    "param1": "20011327|20011330|20011662|20011331|20011328", 
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
                    "param1": "Q022637", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "BOSS开场喊话结束", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "101", 
                    "param1": "20002789|20011658", 
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
                    "param1": "Q022643", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    15: [
        {
            "title": "玩家进入某个范围，通知第一波喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q022634|Q022635|Q022637", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "27933 -103017|27980 -107120|30722 -106700|30564 -102709", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "-13000|-21000"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家进入第一个广场，通知第二波喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.5, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q022638", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 2.5, 
                    "param3": "", 
                    "param2": "100", 
                    "param1": "20002785|20002786", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "42701 -102196|42877 -110936|48760 -109879|48633 -100467", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "-13000|-21000"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "玩家进入第二个台子，通知boss", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "100", 
                    "param1": "20002789", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q022640|Q022639|Q022641|Q022643", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "1|2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "12", 
                    "param3": "52421.003906 -104665.71875 -15359.035156", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "-10000|-20000"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "玩家到达小怪后面 通知小怪开始攻击", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "100", 
                    "param1": "20011327|20011330|20011662|20011331|20011328", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "34591.0 -100666|34958.0 -113024|37613.0 -112784|36385.0 -99713", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "-10000|-20000"
                }
            ], 
            "id": 4
        }
    ]
}