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
                "name": "销毁士兵", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "销毁士兵", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction276", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 19
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
                "name": "通用战斗状态", 
                "tickTimer": 0.5, 
                "statesAI": [
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
                        "id": 1
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
                        "id": 2
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
                        "id": 3
                    }, 
                    {
                        "comment": "距离玩家小于2米攻击或者远离", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction175", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "122125001|122125002|122125003|122125004", 
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
                        "id": 4
                    }, 
                    {
                        "comment": "指挥攻击", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction268", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 15
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
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "20"
                            }
                        ], 
                        "EID": [
                            21
                        ], 
                        "Conditions": [], 
                        "id": 21
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
                "name": "基础状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "指挥跟随", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction263", 
                                "param5": "", 
                                "param4": "3", 
                                "param3": "3", 
                                "param2": "2", 
                                "param1": "2"
                            }
                        ], 
                        "EID": [
                            17
                        ], 
                        "Conditions": [], 
                        "id": 17
                    }, 
                    {
                        "comment": "巡逻路线", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction41", 
                                "param5": "", 
                                "param4": "3", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "4"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "21"
                            }
                        ], 
                        "EID": [
                            20
                        ], 
                        "Conditions": [], 
                        "id": 20
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到指令，矩形", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction264", 
                                    "param5": "", 
                                    "param4": "6", 
                                    "param3": "2", 
                                    "param2": "2", 
                                    "param1": "2"
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
                                    "param1": "102"
                                }
                            ], 
                            "id": 6
                        }, 
                        {
                            "comment": "收到指令，圆形", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction265", 
                                    "param5": "", 
                                    "param4": "6", 
                                    "param3": "2", 
                                    "param2": "2", 
                                    "param1": "2"
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
                                    "param1": "103"
                                }
                            ], 
                            "id": 7
                        }, 
                        {
                            "comment": "收到指令，跟随", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction263", 
                                    "param5": "", 
                                    "param4": "5", 
                                    "param3": "2", 
                                    "param2": "2", 
                                    "param1": "2"
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
                                    "param1": "104"
                                }
                            ], 
                            "id": 8
                        }, 
                        {
                            "comment": "收到指令，移动", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction192", 
                                    "param5": "", 
                                    "param4": "1", 
                                    "param3": "20", 
                                    "param2": "1", 
                                    "param1": "3"
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
                                    "param1": "101"
                                }
                            ], 
                            "id": 9
                        }, 
                        {
                            "comment": "收到指令跳2", 
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
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12547"
                                }
                            ], 
                            "id": 16
                        }, 
                        {
                            "comment": "", 
                            "odds": 1.0, 
                            "Actions": [], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 18
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            2: {
                "name": "操作火炮", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "记录t1时间标签", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t1"
                            }, 
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20013020|20013022", 
                                "param2": "MonsterExtBattery", 
                                "param1": "10"
                            }, 
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20013021", 
                                "param2": "MonsterExtBatteryRocket", 
                                "param1": "10"
                            }
                        ], 
                        "EID": [
                            11
                        ], 
                        "Conditions": [], 
                        "id": 11
                    }, 
                    {
                        "comment": "操作火炮，移除t1 时间标签", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction252", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
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
                        "EID": [
                            12
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition100", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "0"
                            }
                        ], 
                        "id": 12
                    }, 
                    {
                        "comment": "5秒操作不了器械，回到等级1，并且清除标记", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZJ2"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t1"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "11|12"
                            }, 
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "1"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "5", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 13
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到 12561 指令，移除标记，回到等级1", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction253", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }, 
                                {
                                    "script": "AIAction18", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t1"
                                }, 
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "1"
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
                                    "param1": "12561"
                                }
                            ], 
                            "id": 14
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
        "subStateDatas": {
            1: {
                "name": "准备", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "召唤士兵", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction275", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "20013931"
                            }
                        ], 
                        "EID": [
                            10
                        ], 
                        "Conditions": [], 
                        "id": 10
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