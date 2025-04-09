# -*- coding: utf-8 -*-
Datas = {
    "reset": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "show": {
        "subStateDatas": {
            1: {
                "name": "播放出场动作", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "播放出场动作", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction88", 
                                "param5": "100009", 
                                "param4": "2500|8000|1", 
                                "param3": "0|0", 
                                "param2": "-811 -19148 1386|0 0 -99", 
                                "param1": "Show_Stage_01|Show_Stage_02|Show_Stage_03"
                            }
                        ], 
                        "EID": [
                            13
                        ], 
                        "Conditions": [], 
                        "id": 13
                    }, 
                    {
                        "comment": "脱离表演", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction80", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction19", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            14
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition41", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "id": 14
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
    "FSM": 2, 
    "dead": {
        "subStateDatas": {
            1: {
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "喊话通知533", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "533"
                            }
                        ], 
                        "EID": [
                            46
                        ], 
                        "Conditions": [], 
                        "id": 46
                    }, 
                    {
                        "comment": "场上无其他怪发543", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "543"
                            }
                        ], 
                        "EID": [
                            50
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition22", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20009495|20009494|20009497", 
                                "param2": "Monster", 
                                "param1": "80"
                            }
                        ], 
                        "id": 50
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
                        "comment": "有标记跳123", 
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
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "123"
                            }
                        ], 
                        "id": 70
                    }, 
                    {
                        "comment": "去飞行标志位", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction39", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "9"
                            }
                        ], 
                        "EID": [
                            44
                        ], 
                        "Conditions": [], 
                        "id": 44
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
                                "param1": "120583001|120584001|120585001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 48
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到494跳到3", 
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
                                    "param2": "494", 
                                    "param1": ""
                                }
                            ], 
                            "id": 61
                        }
                    ], 
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
                    ]
                }, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            3: {
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
                            53
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
                        "id": 53
                    }, 
                    {
                        "comment": "重新设置出生点", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction50", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "0 0 38", 
                                "param1": "-2648 -20944 1385"
                            }
                        ], 
                        "EID": [
                            54
                        ], 
                        "Conditions": [], 
                        "id": 54
                    }, 
                    {
                        "comment": "去飞行标志位", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction39", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "9"
                            }
                        ], 
                        "EID": [
                            55
                        ], 
                        "Conditions": [], 
                        "id": 55
                    }, 
                    {
                        "comment": "魔化buff", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12156601"
                            }, 
                            {
                                "script": "AIAction55", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "123"
                            }
                        ], 
                        "EID": [
                            62
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition15", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12156601"
                            }
                        ], 
                        "id": 62
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
                        "id": 56
                    }, 
                    {
                        "comment": "竹刺", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "121567001"
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
                                "param1": "121567001"
                            }
                        ], 
                        "id": 63
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
                                "param1": "120583001|120584001|120585001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 57
                    }
                ], 
                "eventsAI": {
                    11: [
                        {
                            "comment": "清除连线", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction113", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12156801"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 66
                        }
                    ], 
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
                            "id": 58
                        }
                    ], 
                    6: [
                        {
                            "comment": "50%梦魇兽指令50", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction59", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "50"
                                }
                            ], 
                            "EID": [
                                59
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
                            "id": 59
                        }, 
                        {
                            "comment": "20%梦魇兽指令20", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction59", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20"
                                }
                            ], 
                            "EID": [
                                60
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20"
                                }
                            ], 
                            "id": 60
                        }, 
                        {
                            "comment": "75%连线10米陷阱", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction16", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "121568001"
                                }
                            ], 
                            "EID": [
                                64
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "75"
                                }, 
                                {
                                    "script": "AICondition11", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "121568001"
                                }
                            ], 
                            "id": 64
                        }, 
                        {
                            "comment": "50%连线10米陷阱", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction16", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "121568001"
                                }
                            ], 
                            "EID": [
                                67
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "50"
                                }, 
                                {
                                    "script": "AICondition11", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "121568001"
                                }
                            ], 
                            "id": 67
                        }, 
                        {
                            "comment": "25%连线10米陷阱", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction16", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "121568001"
                                }
                            ], 
                            "EID": [
                                68
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "25"
                                }, 
                                {
                                    "script": "AICondition11", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "121568001"
                                }
                            ], 
                            "id": 68
                        }, 
                        {
                            "comment": "10%连线10米陷阱", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction16", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "121568001"
                                }
                            ], 
                            "EID": [
                                69
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "10"
                                }, 
                                {
                                    "script": "AICondition11", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "121568001"
                                }
                            ], 
                            "id": 69
                        }
                    ]
                }, 
                "initiativeAreaXZ": "10", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 1
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
                                "param1": "79"
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
                                "param1": "79"
                            }
                        ], 
                        "id": 11
                    }
                ], 
                "eventsAI": {
                    21: [
                        {
                            "comment": "90米内销毁梦魇兽", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction94", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "90", 
                                    "param2": "20009657", 
                                    "param1": "Monster"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 71
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