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
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "播放动作", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction75", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "11013503"
                                }, 
                                {
                                    "script": "AIAction135", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "0"
                                }
                            ], 
                            "EID": [
                                1
                            ], 
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
                            "id": 1
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