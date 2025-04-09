# -*- coding: utf-8 -*-
Datas = {
    "reset": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "FSM": 1, 
    "dead": {
        "subStateDatas": {
            1: {
                "name": "刷盾牌命令", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "死亡发送刷盾牌命令100", 
                        "odds": 1.0, 
                        "Actions": [
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
                            29
                        ], 
                        "Conditions": [], 
                        "id": 29
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
    }, 
    "fight": {
        "subStateDatas": {
            1: {
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
                            30
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
                        "id": 30
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
                        "id": 22
                    }, 
                    {
                        "comment": "距离玩家2-5米靠近或游走", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction72", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "5", 
                                "param2": "3", 
                                "param1": "0.5"
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
                        "id": 23
                    }, 
                    {
                        "comment": "距离玩家小于2米攻击或者远离", 
                        "odds": 0.5, 
                        "Actions": [
                            {
                                "script": "AIAction71", 
                                "param5": "2", 
                                "param4": "100291001|100292001|100293001", 
                                "param3": "5", 
                                "param2": "3", 
                                "param1": "0.6"
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
                        "id": 24
                    }, 
                    {
                        "comment": "盾佑", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "121507001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "121507001"
                            }
                        ], 
                        "id": 28
                    }, 
                    {
                        "comment": "喊话", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000743", 
                                "param1": "19"
                            }
                        ], 
                        "EID": [
                            31
                        ], 
                        "Conditions": [], 
                        "id": 31
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
                            "id": 17
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
        "subStateDatas": {
            1: {
                "name": "", 
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
                            26
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
                        "id": 26
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