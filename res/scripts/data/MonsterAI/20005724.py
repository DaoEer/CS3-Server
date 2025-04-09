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
        "subStateDatas": {
            1: {
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "呼叫同伴", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction15", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            9
                        ], 
                        "Conditions": [], 
                        "id": 9
                    }, 
                    {
                        "comment": "给自己上无敌", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "121377001"
                            }
                        ], 
                        "EID": [
                            2
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "121377001"
                            }
                        ], 
                        "id": 2
                    }, 
                    {
                        "comment": "随机扔金符咒", 
                        "odds": 0.25, 
                        "Actions": [
                            {
                                "script": "AIAction64", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "121382001", 
                                "param2": "15", 
                                "param1": "5"
                            }, 
                            {
                                "script": "AIAction64", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "121383001", 
                                "param2": "20", 
                                "param1": "5"
                            }, 
                            {
                                "script": "AIAction64", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "121384001", 
                                "param2": "25", 
                                "param1": "5"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20005725", 
                                "param2": "Monster", 
                                "param1": "50"
                            }
                        ], 
                        "id": 3
                    }, 
                    {
                        "comment": "随机扔冰符咒", 
                        "odds": 0.25, 
                        "Actions": [
                            {
                                "script": "AIAction64", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "121385001", 
                                "param2": "15", 
                                "param1": "5"
                            }, 
                            {
                                "script": "AIAction64", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "121386001", 
                                "param2": "20", 
                                "param1": "5"
                            }, 
                            {
                                "script": "AIAction64", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "121387001", 
                                "param2": "25", 
                                "param1": "5"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20005726", 
                                "param2": "Monster", 
                                "param1": "50"
                            }
                        ], 
                        "id": 6
                    }, 
                    {
                        "comment": "随机扔火符咒", 
                        "odds": 0.25, 
                        "Actions": [
                            {
                                "script": "AIAction64", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "121388001", 
                                "param2": "15", 
                                "param1": "5"
                            }, 
                            {
                                "script": "AIAction64", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "121389001", 
                                "param2": "20", 
                                "param1": "5"
                            }, 
                            {
                                "script": "AIAction64", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "121390001", 
                                "param2": "25", 
                                "param1": "5"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20005727", 
                                "param2": "Monster", 
                                "param1": "50"
                            }
                        ], 
                        "id": 7
                    }, 
                    {
                        "comment": "随机扔土符咒", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction64", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "121391001", 
                                "param2": "15", 
                                "param1": "5"
                            }, 
                            {
                                "script": "AIAction64", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "121392001", 
                                "param2": "20", 
                                "param1": "5"
                            }, 
                            {
                                "script": "AIAction64", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "121393001", 
                                "param2": "25", 
                                "param1": "5"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20005728", 
                                "param2": "Monster", 
                                "param1": "50"
                            }
                        ], 
                        "id": 8
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
    "free": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "pead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}