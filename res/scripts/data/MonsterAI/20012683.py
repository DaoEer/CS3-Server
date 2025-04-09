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
                "statesAI": [
                    {
                        "comment": "计时", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "gg"
                            }
                        ], 
                        "EID": [
                            1
                        ], 
                        "Conditions": [], 
                        "id": 1
                    }, 
                    {
                        "comment": "释放陆压", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction100", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "-4537.359863 4158.920410 10863.035156", 
                                "param1": "110707001"
                            }
                        ], 
                        "EID": [
                            2
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "gg"
                            }
                        ], 
                        "id": 2
                    }, 
                    {
                        "comment": "对陆压盒子使用连线技能", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20012685", 
                                "param2": "Monster", 
                                "param1": "50"
                            }, 
                            {
                                "script": "AIAction34", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "110707003"
                            }
                        ], 
                        "EID": [
                            3
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "4", 
                                "param1": "gg"
                            }, 
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20012685", 
                                "param2": "Monster", 
                                "param1": "50"
                            }
                        ], 
                        "id": 3
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到副本指令446.改变朝向", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction26", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "0 0 -95.3254471"
                                }
                            ], 
                            "EID": [
                                4
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "446", 
                                    "param1": ""
                                }
                            ], 
                            "id": 4
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