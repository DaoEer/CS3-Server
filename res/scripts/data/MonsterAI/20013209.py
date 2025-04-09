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
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "使用普攻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction175", 
                                "param5": "", 
                                "param4": "5", 
                                "param3": "140341001|140341002", 
                                "param2": "6", 
                                "param1": "0.5"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 5
                    }, 
                    {
                        "comment": "大于70时锁定攻击目标（防止宝珠复活脱战", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "29900176", 
                                "param2": "Monster", 
                                "param1": "100|100"
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
                        "Conditions": [
                            {
                                "script": "AICondition79", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "30"
                            }, 
                            {
                                "script": "AICondition37", 
                                "param5": "", 
                                "param4": "29900176", 
                                "param3": "Monster", 
                                "param2": "14034003", 
                                "param1": "100|100"
                            }
                        ], 
                        "id": 11
                    }, 
                    {
                        "comment": "", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "100|100"
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
                        "Conditions": [
                            {
                                "script": "AICondition63", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "14034003"
                            }
                        ], 
                        "id": 27
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到指令改变攻击目标-宝珠", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction5", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "29900176", 
                                    "param2": "Monster", 
                                    "param1": "100|100"
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
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "gj", 
                                    "param1": ""
                                }
                            ], 
                            "id": 13
                        }
                    ], 
                    5: [
                        {
                            "comment": "", 
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
                            "id": 28
                        }
                    ], 
                    6: [
                        {
                            "comment": "低于25转换目标", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction5", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Role", 
                                    "param1": "15|20"
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
                            "EID": [
                                14
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
                                    "script": "AICondition21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Role", 
                                    "param1": "15"
                                }
                            ], 
                            "id": 14
                        }, 
                        {
                            "comment": "低于20使用技能", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction4", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "140341002"
                                }
                            ], 
                            "EID": [
                                9
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20"
                                }, 
                                {
                                    "script": "AICondition10", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "140341002"
                                }
                            ], 
                            "id": 9
                        }
                    ], 
                    15: [
                        {
                            "comment": "", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction4", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "140341002"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition26", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "140341002"
                                }
                            ], 
                            "id": 10
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
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "进入战斗", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "29900176", 
                                "param2": "Monster", 
                                "param1": "100|100"
                            }, 
                            {
                                "script": "AIAction11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 4
                    }, 
                    {
                        "comment": "", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "100|100"
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
                        "Conditions": [
                            {
                                "script": "AICondition36", 
                                "param5": "", 
                                "param4": "29900176", 
                                "param3": "Monster", 
                                "param2": "14034003", 
                                "param1": "100|100"
                            }
                        ], 
                        "id": 25
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
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}