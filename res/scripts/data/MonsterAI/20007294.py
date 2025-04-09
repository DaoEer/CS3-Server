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
                        "comment": "显示预警", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction168", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "1"
                            }
                        ], 
                        "EID": [
                            4
                        ], 
                        "Conditions": [], 
                        "id": 4
                    }
                ], 
                "eventsAI": {
                    12: [
                        {
                            "comment": "有玩家靠近通知副本", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "Idle_Fight"
                                }, 
                                {
                                    "script": "AIAction59", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "100"
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
                "name": "延迟进入表演", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "延迟一秒进入表演", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction83", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "6", 
                                "param1": "1"
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
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }
        }, 
        "groupHoldEffectIDs": []
    }
}