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
                "name": "通用行为", 
                "tickTimer": 1.0, 
                "statesAI": [
                    {
                        "comment": "每隔3秒，将上海最高的目标作为攻击目标", 
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
                                "script": "AICondition2", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "5"
                            }
                        ], 
                        "id": 6
                    }, 
                    {
                        "comment": "常规技能2", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction175", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "122125001|122125002|122125003|122125004", 
                                "param2": "2.5", 
                                "param1": "1.0"
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
                                "param1": "5"
                            }
                        ], 
                        "id": 7
                    }, 
                    {
                        "comment": "常规技能1", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122124002"
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
                                "param1": "122124002"
                            }
                        ], 
                        "id": 8
                    }, 
                    {
                        "comment": "士兵进入战斗", 
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
                                "script": "AIAction268", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            9
                        ], 
                        "Conditions": [], 
                        "id": 9
                    }, 
                    {
                        "comment": "追击", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction290", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "4"
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
                        "id": 10
                    }, 
                    {
                        "comment": "20012590在身边，给20012590发送2018 指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction25", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2018", 
                                "param1": "20012590"
                            }
                        ], 
                        "EID": [
                            17
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20012590", 
                                "param2": "MonsterCommander", 
                                "param1": "15"
                            }
                        ], 
                        "id": 17
                    }, 
                    {
                        "comment": "进入战斗重置出生点", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction22", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            18
                        ], 
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
                            "id": 19
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
            1: {
                "name": "", 
                "tickTimer": 1.0, 
                "statesAI": [
                    {
                        "comment": "记录时间", 
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
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t10"
                            }
                        ], 
                        "EID": [
                            3
                        ], 
                        "Conditions": [], 
                        "id": 3
                    }, 
                    {
                        "comment": "指挥跟随", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction263", 
                                "param5": "", 
                                "param4": "6", 
                                "param3": "3", 
                                "param2": "2", 
                                "param1": "1"
                            }
                        ], 
                        "EID": [
                            4
                        ], 
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
                        "id": 4
                    }, 
                    {
                        "comment": "列阵", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction264", 
                                "param5": "", 
                                "param4": "10", 
                                "param3": "9", 
                                "param2": "1.25", 
                                "param1": "1"
                            }
                        ], 
                        "EID": [
                            11
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "t11"
                            }
                        ], 
                        "id": 11
                    }, 
                    {
                        "comment": "2秒，接入巡逻路线", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction41", 
                                "param5": "", 
                                "param4": "6", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "42"
                            }
                        ], 
                        "EID": [
                            12
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 12
                    }, 
                    {
                        "comment": "到达位置，切换等级", 
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
                                "script": "AICondition17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "11510 10650 2045"
                            }
                        ], 
                        "id": 13
                    }, 
                    {
                        "comment": "重置出生点", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction22", 
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
                                "param1": "t10"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t10"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "10", 
                                "param1": "t10"
                            }
                        ], 
                        "id": 16
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "指挥列队", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction192", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "15", 
                                    "param2": "1", 
                                    "param1": "8"
                                }, 
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t11"
                                }
                            ], 
                            "EID": [
                                5
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2010"
                                }
                            ], 
                            "id": 5
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            2: {
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "指挥矩形列阵，等待战斗", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction264", 
                                "param5": "", 
                                "param4": "8", 
                                "param3": "5", 
                                "param2": "2.5", 
                                "param1": "1"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t12"
                            }
                        ], 
                        "EID": [
                            14
                        ], 
                        "Conditions": [], 
                        "id": 14
                    }, 
                    {
                        "comment": "将敌人加入战斗列表", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction19", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "50"
                            }, 
                            {
                                "script": "AIAction19", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "CMonster", 
                                "param1": "50"
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
                                "param1": "t12"
                            }
                        ], 
                        "id": 15
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
    "pead": {
        "subStateDatas": {
            1: {
                "name": "霸体", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "添加霸体", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12212601"
                            }, 
                            {
                                "script": "AIAction95", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12212601"
                            }
                        ], 
                        "EID": [
                            1
                        ], 
                        "Conditions": [], 
                        "id": 1
                    }, 
                    {
                        "comment": "召唤长枪兵", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction275", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "10", 
                                "param1": "20012574"
                            }
                        ], 
                        "EID": [
                            2
                        ], 
                        "Conditions": [], 
                        "id": 2
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