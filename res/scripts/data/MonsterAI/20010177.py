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
                "name": "自由状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "石头背后出现玩家，为玩家当风", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "10"
                            }, 
                            {
                                "script": "AIAction76", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12021401"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition94", 
                                "param5": "", 
                                "param4": "8", 
                                "param3": "4", 
                                "param2": "", 
                                "param1": "Role"
                            }
                        ], 
                        "id": 24
                    }, 
                    {
                        "comment": "玩家离开石头背后，不再挡风", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction44", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12021401"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition95", 
                                "param5": "", 
                                "param4": "8", 
                                "param3": "4", 
                                "param2": "", 
                                "param1": "Role"
                            }, 
                            {
                                "script": "AICondition34", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12021401"
                            }
                        ], 
                        "id": 25
                    }
                ], 
                "eventsAI": {
                    26: [
                        {
                            "comment": "玩家推石头时减速", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction5", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Role", 
                                    "param1": "10|100"
                                }, 
                                {
                                    "script": "AIAction34", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "140147002"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 22
                        }
                    ], 
                    27: [
                        {
                            "comment": "玩家结束推石头时恢复", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction235", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "14014701|14014702|14014703|14014704|14014707|14014708|14014709|14014710"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 23
                        }
                    ], 
                    18: [
                        {
                            "comment": "于石头交互后，玩家踩上石头", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction5", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Role", 
                                    "param1": "10"
                                }, 
                                {
                                    "script": "AIAction76", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "14014705|14014706|14000601"
                                }, 
                                {
                                    "script": "AIAction44", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12021401"
                                }, 
                                {
                                    "script": "AIAction32", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "0.1"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "alternately"
                                }
                            ], 
                            "id": 26
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
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