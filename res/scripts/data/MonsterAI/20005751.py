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
        "subStateDatas": {
            2: {
                "name": "通用战斗状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "霸体", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120065001"
                            }
                        ], 
                        "EID": [
                            21
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120065001"
                            }
                        ], 
                        "id": 21
                    }, 
                    {
                        "comment": "冲锋", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "100094001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "100094001"
                            }, 
                            {
                                "script": "AICondition23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "10"
                            }
                        ], 
                        "id": 22
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
                        "EID": [
                            15
                        ], 
                        "Conditions": [], 
                        "id": 15
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
                        "id": 16
                    }, 
                    {
                        "comment": "烈刃斩", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120749001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120749001"
                            }
                        ], 
                        "id": 23
                    }, 
                    {
                        "comment": "距离玩家超过5米开始追击", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction177", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "6"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "5"
                            }
                        ], 
                        "id": 17
                    }, 
                    {
                        "comment": "距离玩家2-5米靠近或游走", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction176", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2.5"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AICondition24", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "5"
                            }
                        ], 
                        "id": 18
                    }, 
                    {
                        "comment": "gw2176距离玩家小于2米攻击或者远离", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction175", 
                                "param5": "", 
                                "param4": "5", 
                                "param3": "100553001|100554001|100555001", 
                                "param2": "2.5", 
                                "param1": "0.7"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition24", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
                            }
                        ], 
                        "id": 19
                    }
                ], 
                "eventsAI": {
                    5: [
                        {
                            "comment": "攻击下一个目标", 
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
                            "id": 20
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
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "pead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}