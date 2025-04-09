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
                "name": "火灵岛刷怪陷阱2", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "刷第二批光效", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 90", 
                                "param2": "-3968 -2486 14897", 
                                "param1": "20000166"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 90", 
                                "param2": "-3348 -2516 14898", 
                                "param1": "20000166"
                            }
                        ], 
                        "EID": [
                            1
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "3", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 1
                    }
                ], 
                "eventsAI": {
                    12: [
                        {
                            "comment": "玩家进入，刷第一批光效，计时喊话。", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0 0 90", 
                                    "param2": "-3688 -2276 14895", 
                                    "param1": "20000164"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0 0 90", 
                                    "param2": "-3788 -2386 14900", 
                                    "param1": "20000165"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0 0 90", 
                                    "param2": "-3618 -2386 14902", 
                                    "param1": "20000165"
                                }, 
                                {
                                    "script": "AIAction30", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Q010310", 
                                    "param1": "20"
                                }, 
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t1"
                                }
                            ], 
                            "EID": [
                                2
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
                            "id": 2
                        }
                    ]
                }, 
                "initiativeAreaXZ": "10.000000", 
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