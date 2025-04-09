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
                    11: [
                        {
                            "comment": "离开这个范围关闭透视效果（临时修改）", 
                            "odds": 0.0, 
                            "Actions": [
                                {
                                    "script": "AIAction216", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "8", 
                                    "param2": "0", 
                                    "param1": "50"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 3
                        }
                    ], 
                    12: [
                        {
                            "comment": "进入这个范围开启透视效果（临时修改）", 
                            "odds": 0.0, 
                            "Actions": [
                                {
                                    "script": "AIAction215", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "8", 
                                    "param2": "0", 
                                    "param1": "50"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 2
                        }
                    ]
                }, 
                "initiativeAreaXZ": "50.0", 
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