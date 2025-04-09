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
                "name": "连线伤害", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "上下移动", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction41", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "0", 
                                "param1": "1"
                            }
                        ], 
                        "EID": [
                            4
                        ], 
                        "Conditions": [], 
                        "id": 4
                    }, 
                    {
                        "comment": "连线对面79", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20007579", 
                                "param2": "Monster", 
                                "param1": "50"
                            }, 
                            {
                                "script": "AIAction34", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "121017001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20007579", 
                                "param2": "Monster", 
                                "param1": "50"
                            }
                        ], 
                        "id": 3
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
        "subStateDatas": {
            1: {
                "name": "伤害连线", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "上下移动", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction41", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "0", 
                                "param1": "1"
                            }
                        ], 
                        "EID": [
                            2
                        ], 
                        "Conditions": [], 
                        "id": 2
                    }, 
                    {
                        "comment": "连线对面79", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20007579", 
                                "param2": "Monster", 
                                "param1": "50"
                            }, 
                            {
                                "script": "AIAction34", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "121017001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20007579", 
                                "param2": "Monster", 
                                "param1": "50"
                            }
                        ], 
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
    }, 
    "pead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}