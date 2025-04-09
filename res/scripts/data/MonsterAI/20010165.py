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
                        "comment": "进入战斗状态移除警戒光效", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction43", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "23002601"
                            }
                        ], 
                        "EID": [
                            17
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition14", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "23002601"
                            }
                        ], 
                        "id": 17
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
                        "id": 13
                    }, 
                    {
                        "comment": "秒杀技能", 
                        "odds": 0.699999988079, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "230029001"
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
                                "param1": "230029001"
                            }, 
                            {
                                "script": "AICondition15", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "23002601"
                            }
                        ], 
                        "id": 14
                    }, 
                    {
                        "comment": "妖卫普攻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "230032001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 19
                    }, 
                    {
                        "comment": "追击", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction211", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 18
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
                            "id": 16
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
    "free": {
        "subStateDatas": {
            4: {
                "name": "自由状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "妖卫警戒范围buff", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "23002601"
                            }
                        ], 
                        "EID": [
                            11
                        ], 
                        "Conditions": [], 
                        "id": 11
                    }, 
                    {
                        "comment": "巡逻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction212", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "2"
                            }
                        ], 
                        "EID": [
                            6
                        ], 
                        "Conditions": [], 
                        "id": 6
                    }, 
                    {
                        "comment": "将玩家加入敌人列表", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction19", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "100"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 5
                    }
                ], 
                "eventsAI": {
                    21: [
                        {
                            "comment": "巡逻拐角停顿", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction207", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
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
                                    "script": "AICondition72", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1", 
                                    "param1": "2"
                                }
                            ], 
                            "id": 28
                        }, 
                        {
                            "comment": "继续巡逻", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction212", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1", 
                                    "param1": "2"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1", 
                                    "param1": "t1"
                                }
                            ], 
                            "id": 29
                        }, 
                        {
                            "comment": "巡逻拐角停顿", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction207", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }, 
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t2"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition72", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "2", 
                                    "param1": "2"
                                }
                            ], 
                            "id": 31
                        }, 
                        {
                            "comment": "继续巡逻", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction212", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "2", 
                                    "param1": "2"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1", 
                                    "param1": "t2"
                                }
                            ], 
                            "id": 32
                        }, 
                        {
                            "comment": "巡逻拐角停顿", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction207", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }, 
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t3"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition72", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "3", 
                                    "param1": "2"
                                }
                            ], 
                            "id": 33
                        }, 
                        {
                            "comment": "继续巡逻", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction212", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "3", 
                                    "param1": "2"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1", 
                                    "param1": "t3"
                                }
                            ], 
                            "id": 34
                        }, 
                        {
                            "comment": "巡逻拐角停顿", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction207", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }, 
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t4"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition72", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "5", 
                                    "param1": "2"
                                }
                            ], 
                            "id": 35
                        }, 
                        {
                            "comment": "继续巡逻", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction212", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "5", 
                                    "param1": "2"
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
                                    "param1": "t4"
                                }
                            ], 
                            "id": 36
                        }, 
                        {
                            "comment": "巡逻拐角停顿", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction207", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }, 
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t5"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition72", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "8", 
                                    "param1": "2"
                                }
                            ], 
                            "id": 37
                        }, 
                        {
                            "comment": "继续巡逻", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction212", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "8", 
                                    "param1": "2"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "2", 
                                    "param1": "t5"
                                }
                            ], 
                            "id": 38
                        }, 
                        {
                            "comment": "巡逻拐角停顿", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction207", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }, 
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t6"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition72", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "9", 
                                    "param1": "2"
                                }
                            ], 
                            "id": 39
                        }, 
                        {
                            "comment": "继续巡逻", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction212", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "9", 
                                    "param1": "2"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "2", 
                                    "param1": "t6"
                                }
                            ], 
                            "id": 40
                        }, 
                        {
                            "comment": "巡逻拐角停顿", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction207", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }, 
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t7"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition72", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "12", 
                                    "param1": "2"
                                }
                            ], 
                            "id": 41
                        }, 
                        {
                            "comment": "继续巡逻", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction212", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "12", 
                                    "param1": "2"
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
                                    "param1": "t7"
                                }
                            ], 
                            "id": 42
                        }, 
                        {
                            "comment": "巡逻拐角停顿", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction207", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }, 
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t8"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition72", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "13", 
                                    "param1": "2"
                                }
                            ], 
                            "id": 43
                        }, 
                        {
                            "comment": "继续巡逻", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction212", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "13", 
                                    "param1": "2"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "2", 
                                    "param1": "t8"
                                }
                            ], 
                            "id": 44
                        }
                    ]
                }, 
                "initiativeAreaXZ": "15", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 4
            }
        }, 
        "groupHoldEffectIDs": []
    }, 
    "pead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}