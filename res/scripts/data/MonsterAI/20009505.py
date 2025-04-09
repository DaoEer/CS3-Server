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
                "name": "吹风，1米每秒", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "释放吹风技能，1米每秒。", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction99", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "230021017|230021018|230021019|230021020|230021021|230021022|230021023|230021024"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 3
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "清除吹风EAI", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "3"
                                }
                            ], 
                            "EID": [
                                1
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1", 
                                    "param1": ""
                                }
                            ], 
                            "id": 1
                        }, 
                        {
                            "comment": "激活一个阵灵，风速变为2米每秒", 
                            "odds": 1.0, 
                            "Actions": [
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
                                3, 
                                4
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "2", 
                                    "param1": ""
                                }
                            ], 
                            "id": 4
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            2: {
                "name": "吹风，2米每秒", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "释放吹风技能，2米每秒", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction99", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "230021009|230021010|230021011|230021012|230021013|230021014|230021015|230021016"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 6
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "激活两个阵灵，风速变为3米每秒", 
                            "odds": 1.0, 
                            "Actions": [
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
                                8, 
                                6
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "3", 
                                    "param1": ""
                                }
                            ], 
                            "id": 8
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            3: {
                "name": "吹风，3米每秒", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "释放吹风技能，3米每秒", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction99", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "230021001|230021002|230021003|230021004|230021005|230021006|230021007|230021008"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 7
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }
        }, 
        "groupHoldEffectIDs": []
    }, 
    "pead": {
        "subStateDatas": {
            2: {
                "name": "出生设置EAI，关闭吹风", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "设置吹风EAI", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction83", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "1"
                            }
                        ], 
                        "EID": [
                            5, 
                            3
                        ], 
                        "Conditions": [], 
                        "id": 5
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }
        }, 
        "groupHoldEffectIDs": []
    }
}