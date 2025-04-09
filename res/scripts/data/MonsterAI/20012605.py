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
                        "comment": "测试1", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C001123", 
                                "param1": "79|10"
                            }
                        ], 
                        "EID": [
                            2
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition116", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "20012577|20012578"
                            }
                        ], 
                        "id": 2
                    }, 
                    {
                        "comment": "测试2", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C001124", 
                                "param1": "79|10"
                            }, 
                            {
                                "script": "AIAction268", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            3
                        ], 
                        "Conditions": [], 
                        "id": 3
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "测试收指令", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction30", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "C001133", 
                                    "param1": "79"
                                }, 
                                {
                                    "script": "AIAction292", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "15"
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
                                    "param1": "101"
                                }, 
                                {
                                    "script": "AICondition119", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "-2"
                                }
                            ], 
                            "id": 4
                        }, 
                        {
                            "comment": "测试收指令", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction30", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "C001134", 
                                    "param1": "79"
                                }, 
                                {
                                    "script": "AIAction292", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "5"
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
                                    "param1": "101"
                                }, 
                                {
                                    "script": "AICondition119", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2"
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
            }
        }, 
        "groupHoldEffectIDs": []
    }, 
    "free": {
        "subStateDatas": {
            1: {
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction264", 
                                    "param5": "", 
                                    "param4": "10", 
                                    "param3": "5", 
                                    "param2": "2.5", 
                                    "param1": "2"
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
                                    "param1": "101"
                                }
                            ], 
                            "id": 5
                        }, 
                        {
                            "comment": "", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction192", 
                                    "param5": "", 
                                    "param4": "1", 
                                    "param3": "8", 
                                    "param2": "2", 
                                    "param1": "8"
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
                                    "param1": "102"
                                }, 
                                {
                                    "script": "AICondition119", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "5"
                                }
                            ], 
                            "id": 6
                        }, 
                        {
                            "comment": "", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction192", 
                                    "param5": "", 
                                    "param4": "1", 
                                    "param3": "16", 
                                    "param2": "1", 
                                    "param1": "8"
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
                                    "param1": "103"
                                }, 
                                {
                                    "script": "AICondition119", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "-5"
                                }
                            ], 
                            "id": 7
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
        "subStateDatas": {
            1: {
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "召唤 骑兵", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction275", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "20012574"
                            }
                        ], 
                        "EID": [
                            1
                        ], 
                        "Conditions": [], 
                        "id": 1
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