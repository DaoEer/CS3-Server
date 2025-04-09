# -*- coding: utf-8 -*-
Datas = {
    "reset": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "FSM": 1, 
    "dead": {
        "subStateDatas": {
            1: {
                "name": "通用死亡状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "召唤封印球", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "20007574"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 9
                    }, 
                    {
                        "comment": "关闭血条界面", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction190", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "0"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 18
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "10.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }
        }, 
        "groupHoldEffectIDs": []
    }, 
    "fight": {
        "subStateDatas": {
            1: {
                "name": "通用战斗状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "不断发出指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction25", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "10086", 
                                "param1": "20007567"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20007567", 
                                "param2": "Monster", 
                                "param1": "6"
                            }
                        ], 
                        "id": 2
                    }, 
                    {
                        "comment": "不断发出指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction25", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "10086", 
                                "param1": "20007568"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20007568", 
                                "param2": "Monster", 
                                "param1": "6"
                            }
                        ], 
                        "id": 6
                    }, 
                    {
                        "comment": "不断发出指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction25", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "10086", 
                                "param1": "20007569"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20007569", 
                                "param2": "Monster", 
                                "param1": "6"
                            }
                        ], 
                        "id": 7
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "20", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }
        }, 
        "groupHoldEffectIDs": []
    }, 
    "free": {
        "subStateDatas": {
            1: {
                "name": "通用自由状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "不断发出指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction25", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "10086", 
                                "param1": "20007567"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20007567", 
                                "param2": "Monster", 
                                "param1": "6"
                            }
                        ], 
                        "id": 1
                    }, 
                    {
                        "comment": "不断发出指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction25", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "10086", 
                                "param1": "20007568"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20007568", 
                                "param2": "Monster", 
                                "param1": "6"
                            }
                        ], 
                        "id": 3
                    }, 
                    {
                        "comment": "不断发出指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction25", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "10086", 
                                "param1": "20007569"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20007569", 
                                "param2": "Monster", 
                                "param1": "6"
                            }
                        ], 
                        "id": 5
                    }
                ], 
                "eventsAI": {
                    11: [
                        {
                            "comment": "关闭血条界面", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction189", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "0"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 12
                        }
                    ], 
                    12: [
                        {
                            "comment": "打开血条界面", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction189", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "1"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 11
                        }
                    ], 
                    13: [
                        {
                            "comment": "关闭血条界面", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction189", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "0"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 13
                        }
                    ], 
                    6: [
                        {
                            "comment": "打开血条界面", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction190", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "15", 
                                    "param1": "1"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 10
                        }, 
                        {
                            "comment": "灭灯", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction10", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "10086", 
                                    "param2": "20008519", 
                                    "param1": "20"
                                }
                            ], 
                            "EID": [
                                19
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "80"
                                }
                            ], 
                            "id": 19
                        }, 
                        {
                            "comment": "灭灯", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction10", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "10086", 
                                    "param2": "20008520", 
                                    "param1": "20"
                                }
                            ], 
                            "EID": [
                                20
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "60"
                                }
                            ], 
                            "id": 20
                        }, 
                        {
                            "comment": "灭灯", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction10", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "10086", 
                                    "param2": "20008521", 
                                    "param1": "20"
                                }
                            ], 
                            "EID": [
                                21
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "40"
                                }
                            ], 
                            "id": 21
                        }, 
                        {
                            "comment": "灭灯", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction10", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "10086", 
                                    "param2": "20008522", 
                                    "param1": "20"
                                }
                            ], 
                            "EID": [
                                22
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20"
                                }
                            ], 
                            "id": 22
                        }
                    ]
                }, 
                "initiativeAreaXZ": "20.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }
        }, 
        "groupHoldEffectIDs": []
    }, 
    "pead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}