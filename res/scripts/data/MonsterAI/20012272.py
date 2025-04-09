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
                        "comment": "走到触发点", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction1", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "9", 
                                "param2": "1", 
                                "param1": "46740.0 54780.0 942.1"
                            }
                        ], 
                        "EID": [
                            2
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "0", 
                                "param1": "46740.0 54780.0 942.1"
                            }
                        ], 
                        "id": 2
                    }, 
                    {
                        "comment": "走到位置，播语音", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "444"
                            }
                        ], 
                        "EID": [
                            3
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "5", 
                                "param1": "46740.0 54780.0 942.1"
                            }, 
                            {
                                "script": "AICondition37", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "Role", 
                                "param2": "12345607", 
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
                        "comment": "进入表演", 
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