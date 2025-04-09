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
                "name": "战斗状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "开场霸体", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "110005003"
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
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "110005003"
                            }
                        ], 
                        "id": 3
                    }, 
                    {
                        "comment": "第一式有控", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "100346001"
                            }
                        ], 
                        "EID": [
                            5
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "30", 
                                "param1": "t1"
                            }, 
                            {
                                "script": "AICondition10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "100346001"
                            }
                        ], 
                        "id": 5
                    }, 
                    {
                        "comment": "第二式有控", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "100347001"
                            }
                        ], 
                        "EID": [
                            6
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "60", 
                                "param1": "t1"
                            }, 
                            {
                                "script": "AICondition10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "100347001"
                            }
                        ], 
                        "id": 6
                    }, 
                    {
                        "comment": "第三式有控", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "100348001"
                            }
                        ], 
                        "EID": [
                            7
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "90", 
                                "param1": "t1"
                            }, 
                            {
                                "script": "AICondition10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "100348001"
                            }
                        ], 
                        "id": 7
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
                                "param1": "100343001|100344001|100345001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 8
                    }, 
                    {
                        "comment": "每隔3秒，攻击伤害最高的敌人", 
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
                        "id": 9
                    }, 
                    {
                        "comment": "喊话", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction28", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "20"
                            }
                        ], 
                        "EID": [
                            16
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "20"
                            }
                        ], 
                        "id": 16
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
                            "id": 10
                        }
                    ]
                }, 
                "initiativeAreaXZ": "12.0", 
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
                "name": "跟随玩家", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "血量保护", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction28", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "80"
                            }
                        ], 
                        "EID": [
                            17
                        ], 
                        "Conditions": [], 
                        "id": 17
                    }, 
                    {
                        "comment": "加入敌人列表", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction19", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20004014|20004015|20004016|20004017", 
                                "param2": "Monster", 
                                "param1": "30"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20004014|20004015|20004016|20004017", 
                                "param2": "Monster", 
                                "param1": "30"
                            }
                        ], 
                        "id": 1
                    }, 
                    {
                        "comment": "在指定位置发通知", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "333"
                            }, 
                            {
                                "script": "AIAction26", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "0 0 33.7"
                            }
                        ], 
                        "EID": [
                            18
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "-2059.153564 67.998856 957.916016"
                            }
                        ], 
                        "id": 18
                    }, 
                    {
                        "comment": "移动", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction1", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "-2059.153564 67.998856 957.916016"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition22", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20004014|20004015|20004016|20004017", 
                                "param2": "Monster", 
                                "param1": "30"
                            }
                        ], 
                        "id": 19
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到指令移动", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction1", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1", 
                                    "param1": "-3189.53 -1059 994.53"
                                }
                            ], 
                            "EID": [
                                15
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "222", 
                                    "param1": ""
                                }
                            ], 
                            "id": 15
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