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
                                "param1": "140050017|140050018|140050019|140050020|140050021|140050022|140050023|140050024"
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
                                "param1": "140050009|140050010|140050011|140050012|140050013|140050014|140050015|140050016"
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
                                "param1": "140050001|140050002|140050003|140050004|140050005|140050006|140050007|140050008"
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