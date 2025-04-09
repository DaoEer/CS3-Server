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
                "name": "攻击", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "使用技能", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction101", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0", 
                                "param2": "10", 
                                "param1": "122116001"
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
                                "param1": "15"
                            }
                        ], 
                        "id": 1
                    }, 
                    {
                        "comment": "选择玩家+停止移动", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction54", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "Role"
                            }, 
                            {
                                "script": "AIAction207", 
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
                                "script": "AICondition28", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "a"
                            }
                        ], 
                        "id": 2
                    }, 
                    {
                        "comment": "距离小于15 使用随机技能", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction67", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122116002|122116003|122116004|122116005"
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
                                "param1": "15"
                            }
                        ], 
                        "id": 3
                    }, 
                    {
                        "comment": "一定范围内的玩家/士兵", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "30|20"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 9
                    }, 
                    {
                        "comment": "a切2", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "a"
                            }
                        ], 
                        "id": 11
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "接受002+标记a", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "a"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "002"
                                }
                            ], 
                            "id": 4
                        }, 
                        {
                            "comment": "收SW后死亡", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction20", 
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
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "sw", 
                                    "param1": ""
                                }
                            ], 
                            "id": 18
                        }, 
                        {
                            "comment": "后退10m", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "3"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "ht", 
                                    "param1": ""
                                }
                            ], 
                            "id": 21
                        }
                    ], 
                    12: [
                        {
                            "comment": "a标记", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "a"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 20
                        }
                    ]
                }, 
                "initiativeAreaXZ": "15.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            2: {
                "name": "攻击", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "使用技能", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction101", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0", 
                                "param2": "10", 
                                "param1": "122116001"
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
                                "param1": "15"
                            }
                        ], 
                        "id": 5
                    }, 
                    {
                        "comment": "选择玩家", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction54", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "Role"
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
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition28", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "a"
                            }
                        ], 
                        "id": 6
                    }, 
                    {
                        "comment": "距离小于15 使用随机技能(费)", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction67", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122116002|122116003|122116004|122116005"
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
                                "param1": "15"
                            }
                        ], 
                        "id": 7
                    }, 
                    {
                        "comment": "一定范围内的玩家/士兵", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "30|20"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 10
                    }, 
                    {
                        "comment": "距离玩家超过35米开始追击", 
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
                                "param1": "35"
                            }
                        ], 
                        "id": 13
                    }, 
                    {
                        "comment": "距离玩家20-35米靠近或游走", 
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
                                "param1": "20"
                            }, 
                            {
                                "script": "AICondition24", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "35"
                            }
                        ], 
                        "id": 14
                    }, 
                    {
                        "comment": "距离玩家小于20米攻击或者远离", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction175", 
                                "param5": "", 
                                "param4": "5", 
                                "param3": "122116001", 
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
                                "param1": "20"
                            }
                        ], 
                        "id": 15
                    }, 
                    {
                        "comment": "换目标", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction282", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "30"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t1"
                            }
                        ], 
                        "EID": [], 
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
                        "id": 19
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "接受002+标记a", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "a"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "001"
                                }
                            ], 
                            "id": 8
                        }, 
                        {
                            "comment": "收到sw后死亡", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction20", 
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
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "sw", 
                                    "param1": ""
                                }
                            ], 
                            "id": 17
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            3: {
                "name": "后退", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "后退12米", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t"
                            }, 
                            {
                                "script": "AIAction192", 
                                "param5": "", 
                                "param4": "1", 
                                "param3": "12", 
                                "param2": "2", 
                                "param1": "6"
                            }
                        ], 
                        "EID": [
                            22
                        ], 
                        "Conditions": [], 
                        "id": 22
                    }, 
                    {
                        "comment": "t=2切换1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "1"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "22"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "4", 
                                "param1": "t"
                            }
                        ], 
                        "id": 23
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
    "free": {
        "subStateDatas": {
            1: {
                "name": "选玩家", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "60米玩家", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "60|30"
                            }, 
                            {
                                "script": "AIAction14", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 12
                    }
                ], 
                "eventsAI": {
                    12: [
                        {
                            "comment": "60米玩家", 
                            "odds": 0.0, 
                            "Actions": [
                                {
                                    "script": "AIAction5", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Role", 
                                    "param1": "60|30"
                                }, 
                                {
                                    "script": "AIAction14", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 16
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0", 
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