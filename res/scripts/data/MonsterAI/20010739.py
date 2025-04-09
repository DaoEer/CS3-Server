# -*- coding: utf-8 -*-
Datas = {
    "reset": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "FSM": 1, 
    "dead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "fight": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "free": {
        "subStateDatas": {
            1: {
                "name": "巡逻表现", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "巡逻到点  7+停止13s", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction147", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "13"
                            }, 
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
                            }
                        ], 
                        "EID": [
                            1
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition72", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "7", 
                                "param1": "1"
                            }
                        ], 
                        "id": 1
                    }, 
                    {
                        "comment": "巡逻到点20+停止13s", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction147", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "13"
                            }, 
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "3"
                            }
                        ], 
                        "EID": [
                            3
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition72", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20", 
                                "param1": "1"
                            }
                        ], 
                        "id": 3
                    }, 
                    {
                        "comment": "巡逻到点26+停止13s+延时4s销毁", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction147", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "13"
                            }, 
                            {
                                "script": "AIAction32", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "4"
                            }
                        ], 
                        "EID": [
                            6
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition72", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "26", 
                                "param1": "1"
                            }
                        ], 
                        "id": 6
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到指令开始巡逻", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction58", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "3"
                                }
                            ], 
                            "EID": [
                                2
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "xunluo", 
                                    "param1": ""
                                }
                            ], 
                            "id": 2
                        }
                    ], 
                    11: [
                        {
                            "comment": "加上Buff", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction116", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12160301"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 4
                        }
                    ], 
                    12: [
                        {
                            "comment": "清除Buff", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction113", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12160301"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 5
                        }
                    ]
                }, 
                "initiativeAreaXZ": "8", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 1
            }, 
            2: {
                "name": "到点召唤小怪", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "记录时间t01", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t01"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 7
                    }, 
                    {
                        "comment": "召唤小怪（停用）", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20010732", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "10", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction48", 
                                "param5": "20010733", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "8", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            8
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "3", 
                                "param1": "t01"
                            }
                        ], 
                        "id": 8
                    }, 
                    {
                        "comment": "召唤小怪", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20010732", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "10", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "1"
                            }, 
                            {
                                "script": "AIAction48", 
                                "param5": "20010733", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "8", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            9
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "3", 
                                "param1": "t01"
                            }
                        ], 
                        "id": 9
                    }
                ], 
                "eventsAI": {
                    11: [
                        {
                            "comment": "加上Buff", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction116", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12160301"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 13
                        }
                    ], 
                    12: [
                        {
                            "comment": "清除Buff", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction113", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12160301"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 14
                        }
                    ]
                }, 
                "initiativeAreaXZ": "8", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 1
            }, 
            3: {
                "name": "到点召唤小怪", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "记录时间t02", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t02"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 10
                    }, 
                    {
                        "comment": "召唤小怪（停用）", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20010732", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "10", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction48", 
                                "param5": "20010733", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "8", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            11
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "3", 
                                "param1": "t02"
                            }
                        ], 
                        "id": 11
                    }, 
                    {
                        "comment": "召唤小怪", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20010732", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "10", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "1"
                            }, 
                            {
                                "script": "AIAction48", 
                                "param5": "20010733", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "8", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            12
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "3", 
                                "param1": "t02"
                            }
                        ], 
                        "id": 12
                    }
                ], 
                "eventsAI": {
                    11: [
                        {
                            "comment": "加上Buff", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction116", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12160301"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 16
                        }
                    ], 
                    12: [
                        {
                            "comment": "清除Buff", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction113", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12160301"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 15
                        }
                    ]
                }, 
                "initiativeAreaXZ": "8", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 1
            }
        }, 
        "groupHoldEffectIDs": []
    }, 
    "pead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}