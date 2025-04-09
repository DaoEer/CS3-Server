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
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "播光效", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction91", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "101928"
                            }
                        ], 
                        "EID": [
                            6
                        ], 
                        "Conditions": [], 
                        "id": 6
                    }, 
                    {
                        "comment": "巡逻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction41", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "0", 
                                "param1": "11"
                            }
                        ], 
                        "EID": [
                            2
                        ], 
                        "Conditions": [], 
                        "id": 2
                    }, 
                    {
                        "comment": "将玩家作为AI目标", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 3
                    }
                ], 
                "eventsAI": {
                    12: [
                        {
                            "comment": "玩家碰到旋风", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction116", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "11015302"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition44", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "Role"
                                }, 
                                {
                                    "script": "AICondition48", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "11015302"
                                }
                            ], 
                            "id": 7
                        }
                    ]
                }, 
                "initiativeAreaXZ": "2", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
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