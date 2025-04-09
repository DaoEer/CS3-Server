# -*- coding: utf-8 -*-
Datas = {
    "reset": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "show": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "FSM": 2, 
    "dead": {
        "subStateDatas": {
            1: {
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }
        }, 
        "groupHoldEffectIDs": []
    }, 
    "fight": {
        "subStateDatas": {
            2: {
                "name": "战斗", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "霸体", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "10000001"
                            }
                        ], 
                        "EID": [
                            47
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition15", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "10000001"
                            }
                        ], 
                        "id": 47
                    }, 
                    {
                        "comment": "呼叫同伴", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction15", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 79
                    }, 
                    {
                        "comment": "每隔3秒，将伤害最高的目标设为攻击目标", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction8", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "3"
                            }
                        ], 
                        "id": 49
                    }, 
                    {
                        "comment": "循环无控", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction42", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "101707001|101706001|101705001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 48
                    }
                ], 
                "eventsAI": {
                    5: [
                        {
                            "comment": "攻击下一个敌人", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction13", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 34
                        }
                    ], 
                    6: [
                        {
                            "comment": "低于50%逃跑", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction1", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "7", 
                                    "param2": "1", 
                                    "param1": "-2123 -13672 9315"
                                }
                            ], 
                            "EID": [
                                78
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "50"
                                }
                            ], 
                            "id": 78
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
    "free": {
        "subStateDatas": {
            1: {
                "name": "通用自由状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "将玩家加入敌人列表", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction19", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "10"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "10"
                            }
                        ], 
                        "id": 11
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
    "pead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}