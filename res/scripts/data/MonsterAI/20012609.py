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
                "name": "准备状态", 
                "tickTimer": 0.5, 
                "statesAI": [], 
                "eventsAI": {
                    12: [
                        {
                            "comment": "有entity进入主动反应陷阱范围，进入检测状态", 
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
                            "EID": [], 
                            "Conditions": [], 
                            "id": 1
                        }
                    ]
                }, 
                "initiativeAreaXZ": "40|25", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 1, 
                "initiativeTrapShape": 2
            }, 
            2: {
                "name": "检测状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "有1名玩家，发送1031指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction25", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1031", 
                                "param1": "20012610|20012538|20012539"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "3|4|5|6"
                            }
                        ], 
                        "EID": [
                            2
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition122", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "1"
                            }
                        ], 
                        "id": 2
                    }, 
                    {
                        "comment": "有2名玩家，发送1032指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction25", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1032", 
                                "param1": "20012610|20012538|20012539"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2|4|5|6"
                            }
                        ], 
                        "EID": [
                            3
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition122", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
                            }
                        ], 
                        "id": 3
                    }, 
                    {
                        "comment": "有3名玩家，发送1033指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction25", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1033", 
                                "param1": "20012610|20012538|20012539"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2|3|5|6"
                            }
                        ], 
                        "EID": [
                            4
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition122", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "3"
                            }
                        ], 
                        "id": 4
                    }, 
                    {
                        "comment": "有4名玩家，发送1034指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction25", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1034", 
                                "param1": "20012610|20012538|20012539"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2|3|4|6"
                            }
                        ], 
                        "EID": [
                            5
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition122", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "4"
                            }
                        ], 
                        "id": 5
                    }, 
                    {
                        "comment": "有5名玩家，发送1035指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction25", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1035", 
                                "param1": "20012610|20012538|20012539"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2|3|4|5"
                            }
                        ], 
                        "EID": [
                            6
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition122", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "5"
                            }
                        ], 
                        "id": 6
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "有1名玩家，发送1031指令", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1031", 
                                    "param1": "20012610"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition122", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "1"
                                }
                            ], 
                            "id": 7
                        }, 
                        {
                            "comment": "有2名玩家，发送1032指令", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1032", 
                                    "param1": "20012610"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition122", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2"
                                }
                            ], 
                            "id": 8
                        }, 
                        {
                            "comment": "有2名玩家，发送1033指令", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1033", 
                                    "param1": "20012610"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition122", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "3"
                                }
                            ], 
                            "id": 9
                        }, 
                        {
                            "comment": "有4名玩家，发送1034指令", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1034", 
                                    "param1": "20012610"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition122", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "4"
                                }
                            ], 
                            "id": 10
                        }, 
                        {
                            "comment": "有5名玩家，发送1035指令", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1035", 
                                    "param1": "20012610"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition122", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "5"
                                }
                            ], 
                            "id": 11
                        }
                    ]
                }, 
                "initiativeAreaXZ": "40|25", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 1, 
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