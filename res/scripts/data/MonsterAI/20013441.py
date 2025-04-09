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
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction94", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "70", 
                                "param2": "30001025", 
                                "param1": "Trap"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition8", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "id": 42
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
                        "comment": "霸体", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "14023901"
                            }
                        ], 
                        "EID": [
                            3
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition15", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "14023901"
                            }
                        ], 
                        "id": 3
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
                        "id": 5
                    }, 
                    {
                        "comment": "循环丢技能", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction42", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122273002|122273003|122273004"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 6
                    }, 
                    {
                        "comment": "招水", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C001692", 
                                "param1": "99"
                            }, 
                            {
                                "script": "AIAction12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "Attack_02"
                            }, 
                            {
                                "script": "AIAction48", 
                                "param5": "30001025", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "1163 3756 1605"
                            }, 
                            {
                                "script": "AIAction48", 
                                "param5": "30001026", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "1163 3756 1605"
                            }, 
                            {
                                "script": "AIAction48", 
                                "param5": "30001027", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "1163 3756 1605"
                            }, 
                            {
                                "script": "AIAction48", 
                                "param5": "30001028", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "1163 3756 1605"
                            }
                        ], 
                        "EID": [
                            51
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition2", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "10"
                            }
                        ], 
                        "id": 51
                    }, 
                    {
                        "comment": "召浪1", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "Attack_02"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -90", 
                                "param2": "1248 5698 1412", 
                                "param1": "30001061"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 85", 
                                "param2": "2548 2168 1412", 
                                "param1": "30001062"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 187", 
                                "param2": "3229 5020 1512", 
                                "param1": "30001063"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 0", 
                                "param2": "-1113 2709 1412", 
                                "param1": "30001064"
                            }
                        ], 
                        "EID": [
                            56
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition2", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "20"
                            }
                        ], 
                        "id": 56
                    }, 
                    {
                        "comment": "召浪", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "Attack_02"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -90", 
                                "param2": "1248 5698 1412", 
                                "param1": "30001061"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 85", 
                                "param2": "2548 2168 1412", 
                                "param1": "30001062"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 187", 
                                "param2": "3229 5020 1512", 
                                "param1": "30001063"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 0", 
                                "param2": "-1113 2709 1412", 
                                "param1": "30001064"
                            }
                        ], 
                        "EID": [
                            50
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition2", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "60"
                            }
                        ], 
                        "id": 50
                    }, 
                    {
                        "comment": "召浪", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "Attack_02"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -90", 
                                "param2": "1248 5698 1412", 
                                "param1": "30001061"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 85", 
                                "param2": "2548 2168 1412", 
                                "param1": "30001062"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 187", 
                                "param2": "3229 5020 1512", 
                                "param1": "30001063"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 0", 
                                "param2": "-1113 2709 1412", 
                                "param1": "30001064"
                            }
                        ], 
                        "EID": [
                            57
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition2", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "100"
                            }
                        ], 
                        "id": 57
                    }, 
                    {
                        "comment": "召浪", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "Attack_02"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -90", 
                                "param2": "1248 5698 1412", 
                                "param1": "30001061"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 85", 
                                "param2": "2548 2168 1412", 
                                "param1": "30001062"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 187", 
                                "param2": "3229 5020 1512", 
                                "param1": "30001063"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 0", 
                                "param2": "-1113 2709 1412", 
                                "param1": "30001064"
                            }
                        ], 
                        "EID": [
                            58
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition2", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "140"
                            }
                        ], 
                        "id": 58
                    }, 
                    {
                        "comment": "召浪", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "Attack_02"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -90", 
                                "param2": "1248 5698 1412", 
                                "param1": "30001061"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 85", 
                                "param2": "2548 2168 1412", 
                                "param1": "30001062"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 187", 
                                "param2": "3229 5020 1512", 
                                "param1": "30001063"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 0", 
                                "param2": "-1113 2709 1412", 
                                "param1": "30001064"
                            }
                        ], 
                        "EID": [
                            59
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition2", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "200"
                            }
                        ], 
                        "id": 59
                    }, 
                    {
                        "comment": "召浪", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "Attack_02"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -90", 
                                "param2": "1248 5698 1412", 
                                "param1": "30001061"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 85", 
                                "param2": "2548 2168 1412", 
                                "param1": "30001062"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 187", 
                                "param2": "3229 5020 1512", 
                                "param1": "30001063"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 0", 
                                "param2": "-1113 2709 1412", 
                                "param1": "30001064"
                            }
                        ], 
                        "EID": [
                            60
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition2", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "250"
                            }
                        ], 
                        "id": 60
                    }, 
                    {
                        "comment": "招水", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "Attack_02"
                            }, 
                            {
                                "script": "AIAction48", 
                                "param5": "30001025", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "1163 3756 1605"
                            }, 
                            {
                                "script": "AIAction48", 
                                "param5": "30001026", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "1163 3756 1605"
                            }, 
                            {
                                "script": "AIAction48", 
                                "param5": "30001027", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "1163 3756 1605"
                            }, 
                            {
                                "script": "AIAction48", 
                                "param5": "30001028", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "1163 3756 1605"
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
                                "param1": "23"
                            }
                        ], 
                        "id": 61
                    }, 
                    {
                        "comment": "记录时间o", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "o"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 75
                    }, 
                    {
                        "comment": "每隔20秒丢火", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "101"
                            }, 
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122271001"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "o"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "o"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20", 
                                "param1": "o"
                            }, 
                            {
                                "script": "AICondition10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122271001"
                            }
                        ], 
                        "id": 76
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到666变成中立", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction38", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2"
                                }
                            ], 
                            "EID": [
                                71
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "666", 
                                    "param1": ""
                                }
                            ], 
                            "id": 71
                        }
                    ], 
                    22: [
                        {
                            "comment": "开启光墙", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction135", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "5"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 70
                        }
                    ], 
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
                            "id": 15
                        }
                    ], 
                    6: [
                        {
                            "comment": "80丢球", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "Show_06"
                                }, 
                                {
                                    "script": "AIAction48", 
                                    "param5": "20013456", 
                                    "param4": "6", 
                                    "param3": "", 
                                    "param2": "10", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [
                                25
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "80"
                                }
                            ], 
                            "id": 25
                        }, 
                        {
                            "comment": "60丢火", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "Show_06"
                                }, 
                                {
                                    "script": "AIAction48", 
                                    "param5": "20013456", 
                                    "param4": "6", 
                                    "param3": "", 
                                    "param2": "10", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [
                                26
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "60"
                                }
                            ], 
                            "id": 26
                        }, 
                        {
                            "comment": "40丢火", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "Show_06"
                                }, 
                                {
                                    "script": "AIAction48", 
                                    "param5": "20013456", 
                                    "param4": "6", 
                                    "param3": "", 
                                    "param2": "10", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [
                                27
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "40"
                                }
                            ], 
                            "id": 27
                        }, 
                        {
                            "comment": "20丢火", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "Show_06"
                                }, 
                                {
                                    "script": "AIAction48", 
                                    "param5": "20013456", 
                                    "param4": "8", 
                                    "param3": "", 
                                    "param2": "10", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [
                                28
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
                            "id": 28
                        }, 
                        {
                            "comment": "10丢火", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "Show_06"
                                }, 
                                {
                                    "script": "AIAction48", 
                                    "param5": "20013456", 
                                    "param4": "10", 
                                    "param3": "", 
                                    "param2": "10", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [
                                29
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "10"
                                }
                            ], 
                            "id": 29
                        }, 
                        {
                            "comment": "s1 70hp", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "s1"
                                }
                            ], 
                            "EID": [
                                30
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "70"
                                }
                            ], 
                            "id": 30
                        }, 
                        {
                            "comment": "s2 50hp", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "s2"
                                }
                            ], 
                            "EID": [
                                32
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
                            "id": 32
                        }, 
                        {
                            "comment": "s3 30hp", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "s3"
                                }
                            ], 
                            "EID": [
                                33
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "30"
                                }
                            ], 
                            "id": 33
                        }, 
                        {
                            "comment": "s1丢球", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0 0 0", 
                                    "param2": "1163 3756 1605", 
                                    "param1": "20013457"
                                }
                            ], 
                            "EID": [
                                37
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1", 
                                    "param1": "s1"
                                }
                            ], 
                            "id": 37
                        }, 
                        {
                            "comment": "s2丢球", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0 0 0", 
                                    "param2": "1163 3756 1605", 
                                    "param1": "20013457"
                                }
                            ], 
                            "EID": [
                                40
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1", 
                                    "param1": "s2"
                                }
                            ], 
                            "id": 40
                        }, 
                        {
                            "comment": "s3丢球", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0 0 0", 
                                    "param2": "1163 3756 1605", 
                                    "param1": "20013457"
                                }
                            ], 
                            "EID": [
                                41
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition12", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1", 
                                    "param1": "s3"
                                }
                            ], 
                            "id": 41
                        }, 
                        {
                            "comment": "90丢火", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction48", 
                                    "param5": "20013456", 
                                    "param4": "8", 
                                    "param3": "", 
                                    "param2": "18", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [
                                45
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "90"
                                }
                            ], 
                            "id": 45
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
                "name": "自由状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "重置朝向", 
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
                            1
                        ], 
                        "Conditions": [], 
                        "id": 1
                    }, 
                    {
                        "comment": "玩家进入把玩家加入战斗列表", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction19", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "25"
                            }
                        ], 
                        "EID": [
                            2
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "25"
                            }
                        ], 
                        "id": 2
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
                                "param2": "C001690", 
                                "param1": "99"
                            }
                        ], 
                        "EID": [
                            73
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "35"
                            }
                        ], 
                        "id": 73
                    }
                ], 
                "eventsAI": {
                    21: [
                        {
                            "comment": "关闭光墙", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction136", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 69
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
        "subStateDatas": {
            1: {
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "关闭光墙", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction136", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 66
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