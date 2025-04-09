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
                "statesAI": [], 
                "eventsAI": {
                    11: [
                        {
                            "comment": "离开这个范围关闭透视", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction216", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "8", 
                                    "param2": "0", 
                                    "param1": "60"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 3
                        }
                    ], 
                    12: [
                        {
                            "comment": "进入这个范围开启透视", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction215", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "8", 
                                    "param2": "0", 
                                    "param1": "60"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 2
                        }
                    ]
                }, 
                "initiativeAreaXZ": "60.0", 
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
                        "comment": "进入表演状态", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "11035001"
                            }, 
                            {
                                "script": "AIAction61", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
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
                "initiativeAreaXZ": "50.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 1
            }
        }, 
        "groupHoldEffectIDs": []
    }
}