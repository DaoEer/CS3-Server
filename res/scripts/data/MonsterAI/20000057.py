# -*- coding: utf-8 -*-
Datas = {
    "reset": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "FSM": 1, 
    "dead": {
        "subStateDatas": {
            2: {
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "给陷阱发送通知播放宝物获得镜头", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "121", 
                                "param2": "20000230", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            12
                        ], 
                        "Conditions": [], 
                        "id": 12
                    }, 
                    {
                        "comment": "给天书和传送光效发送通知", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "111", 
                                "param2": "20000233|20000234", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            13
                        ], 
                        "Conditions": [], 
                        "id": 13
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }
        }, 
        "groupHoldEffectIDs": []
    }, 
    "fight": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "free": {
        "subStateDatas": {
            1: {
                "name": "传送台普通", 
                "tickTimer": 0.5, 
                "statesAI": [], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到鬼枭死亡通知，移除标志位", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction39", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2|11"
                                }
                            ], 
                            "EID": [
                                2
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "101", 
                                    "param1": ""
                                }
                            ], 
                            "id": 2
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.000000", 
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