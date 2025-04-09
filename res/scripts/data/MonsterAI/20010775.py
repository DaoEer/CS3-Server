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
                "name": "主动反应事件", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "绑定到平台50000106", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction163", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "10", 
                                "param1": "50000106"
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
                    11: [
                        {
                            "comment": "清除保护Buff", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction113", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12160702"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 2
                        }
                    ], 
                    12: [
                        {
                            "comment": "添加保护Buff", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction116", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12160702"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 1
                        }
                    ]
                }, 
                "initiativeAreaXZ": "5", 
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