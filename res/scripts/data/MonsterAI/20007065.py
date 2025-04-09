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
                "name": "有buff标记，则触发", 
                "tickTimer": 0.5, 
                "statesAI": [], 
                "eventsAI": {
                    12: [
                        {
                            "comment": "玩家进入，检测是否存在标记", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction74", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "Role", 
                                    "param2": "11014103", 
                                    "param1": "20"
                                }, 
                                {
                                    "script": "AIAction37", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "5", 
                                    "param1": "20102594"
                                }, 
                                {
                                    "script": "AIAction119", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20102594"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition36", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "Role", 
                                    "param2": "11014103", 
                                    "param1": "20"
                                }, 
                                {
                                    "script": "AICondition45", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20102594"
                                }
                            ], 
                            "id": 2
                        }
                    ]
                }, 
                "initiativeAreaXZ": "10", 
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