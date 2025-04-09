# -*- coding: utf-8 -*-
Datas = {
    "reset": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "show": {
        "subStateDatas": {
            1: {
                "name": "", 
                "tickTimer": 0.10000000149, 
                "statesAI": [], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "星辰子逃跑结束，开启玩家传送", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction91", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "102353_1"
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
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "1"
                                }
                            ], 
                            "id": 2
                        }
                    ], 
                    12: [
                        {
                            "comment": "未完成20101678任务，可进入四象星阵", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction114", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0 0 -50", 
                                    "param2": "-6069.0 11199.0 22457.0", 
                                    "param1": "L_XCHJ"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition49", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "3", 
                                    "param1": "20101678"
                                }
                            ], 
                            "id": 6
                        }, 
                        {
                            "comment": "未完成20101679任务，可进入四象星阵", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction114", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0 0 -50", 
                                    "param2": "-6069.0 11199.0 22457.0", 
                                    "param1": "L_XCHJ"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition49", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "3", 
                                    "param1": "20101679"
                                }
                            ], 
                            "id": 7
                        }
                    ]
                }, 
                "initiativeAreaXZ": "3", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 1
            }, 
            2: {
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
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "1"
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
                                    "param1": "1"
                                }
                            ], 
                            "id": 5
                        }
                    ], 
                    12: [
                        {
                            "comment": "完成任务目标", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction36", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "4", 
                                    "param2": "20101678", 
                                    "param1": "50"
                                }
                            ], 
                            "EID": [
                                3
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition44", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "Role"
                                }
                            ], 
                            "id": 3
                        }
                    ]
                }, 
                "initiativeAreaXZ": "3", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 1
            }
        }, 
        "groupHoldEffectIDs": []
    }, 
    "FSM": 2, 
    "dead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "fight": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "free": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "pead": {
        "subStateDatas": {
            1: {
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction61", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [], 
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