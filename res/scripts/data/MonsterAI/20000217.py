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
            2: {
                "name": "复制玩家外观和技能", 
                "tickTimer": 0.5, 
                "statesAI": [], 
                "eventsAI": {
                    11: [
                        {
                            "comment": "有玩家进入主动反应陷阱，召唤一个复制外观和技能的心魔，1秒后销毁自身", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction115", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "20000200", 
                                    "param2": "", 
                                    "param1": ""
                                }, 
                                {
                                    "script": "AIAction32", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "1"
                                }
                            ], 
                            "EID": [
                                23, 
                                22
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
                            "id": 23
                        }
                    ], 
                    12: [
                        {
                            "comment": "有玩家进入主动反应陷阱，召唤一个复制外观和技能的心魔，1秒后销毁自身", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction115", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "20000200", 
                                    "param2": "", 
                                    "param1": ""
                                }, 
                                {
                                    "script": "AIAction32", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "1"
                                }
                            ], 
                            "EID": [
                                22, 
                                23
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
                            "id": 22
                        }
                    ]
                }, 
                "initiativeAreaXZ": "5.000000", 
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