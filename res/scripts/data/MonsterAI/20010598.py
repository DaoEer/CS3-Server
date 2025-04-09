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
            1: {
                "name": "下界试炼——灵珠子（战斗）", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "50%血量保护", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction28", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            4, 
                            6
                        ], 
                        "Conditions": [], 
                        "id": 4
                    }, 
                    {
                        "comment": "设置k1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction50", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "0 0 50", 
                                "param1": "-58880 -9245 12543.099609"
                            }, 
                            {
                                "script": "AIAction55", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "k1"
                            }, 
                            {
                                "script": "AIAction19", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20010600|20010825", 
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
                        "comment": "战斗后每隔3秒改变攻击目标", 
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
                        "id": 7
                    }, 
                    {
                        "comment": "循环技能", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction42", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "102205001|102206001|102207001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 13
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
                            "id": 8
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
                "name": "下界试炼——玄冥子（自由）", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "存在k1，改变朝向/对副本发送通知1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction53", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            10
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "k1"
                            }
                        ], 
                        "id": 10
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "50%血量保护，加入小怪到战斗列表", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction28", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "50"
                                }, 
                                {
                                    "script": "AIAction19", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "20010597", 
                                    "param2": "Monster", 
                                    "param1": "50"
                                }
                            ], 
                            "EID": [
                                13
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "111", 
                                    "param1": ""
                                }
                            ], 
                            "id": 13
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