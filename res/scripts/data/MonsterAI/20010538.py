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
                "name": "一阶段", 
                "tickTimer": 2.0, 
                "statesAI": [
                    {
                        "comment": "生命低于25%回血", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "time"
                            }, 
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "140234001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition9", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "25"
                            }
                        ], 
                        "id": 1
                    }, 
                    {
                        "comment": "生命高于25%切换状态", 
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
                        "EID": [
                            3
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition79", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "25"
                            }
                        ], 
                        "id": 3
                    }, 
                    {
                        "comment": "时间到达60秒切换状态", 
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
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "time"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "60", 
                                "param1": "time"
                            }
                        ], 
                        "id": 5
                    }, 
                    {
                        "comment": "发送副本失败通知", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "shibai"
                            }
                        ], 
                        "EID": [
                            1
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition9", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "0"
                            }
                        ], 
                        "id": 20
                    }, 
                    {
                        "comment": "发送本阶段时长", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "60", 
                                "param1": "1jieduan"
                            }
                        ], 
                        "EID": [
                            34
                        ], 
                        "Conditions": [], 
                        "id": 34
                    }
                ], 
                "eventsAI": {
                    12: [
                        {
                            "comment": "锁定目标", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction74", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "Role", 
                                    "param2": "14023501", 
                                    "param1": "5"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 21
                        }, 
                        {
                            "comment": "普通晶石的回复", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction44", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "14023501"
                                }, 
                                {
                                    "script": "AIAction16", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "140234001"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition34", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "14023501"
                                }
                            ], 
                            "id": 22
                        }, 
                        {
                            "comment": "高级晶石的回复", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction44", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "14023502"
                                }, 
                                {
                                    "script": "AIAction16", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "140234002"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition34", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "14023502"
                                }
                            ], 
                            "id": 24
                        }, 
                        {
                            "comment": "锁定2号Buff目标", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction74", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "Role", 
                                    "param2": "14023502", 
                                    "param1": "5"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 39
                        }
                    ]
                }, 
                "initiativeAreaXZ": "5", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 1
            }, 
            2: {
                "name": "二阶段", 
                "tickTimer": 2.0, 
                "statesAI": [
                    {
                        "comment": "更替模型", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction46", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "SM_Qiu_Shu_020"
                            }, 
                            {
                                "script": "AIAction91", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "1", 
                                "param2": "", 
                                "param1": "101982"
                            }
                        ], 
                        "EID": [
                            6
                        ], 
                        "Conditions": [], 
                        "id": 6
                    }, 
                    {
                        "comment": "生命低于50%回血", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "time1"
                            }, 
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "140234001"
                            }
                        ], 
                        "EID": [], 
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
                        "id": 7
                    }, 
                    {
                        "comment": "生命高于50%切换状态", 
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
                        "EID": [
                            8
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition79", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "50"
                            }
                        ], 
                        "id": 8
                    }, 
                    {
                        "comment": "时间超过60秒切换状态", 
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
                        "EID": [
                            9
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "60", 
                                "param1": "time1"
                            }
                        ], 
                        "id": 9
                    }, 
                    {
                        "comment": "发送副本失败通知", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "shibai"
                            }
                        ], 
                        "EID": [
                            7
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition9", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "0"
                            }
                        ], 
                        "id": 19
                    }, 
                    {
                        "comment": "发送本阶段时长", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "60", 
                                "param1": "2jieduan"
                            }
                        ], 
                        "EID": [
                            35
                        ], 
                        "Conditions": [], 
                        "id": 35
                    }
                ], 
                "eventsAI": {
                    12: [
                        {
                            "comment": "锁定目标", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction74", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "Role", 
                                    "param2": "14023501", 
                                    "param1": "5"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 25
                        }, 
                        {
                            "comment": "普通晶石的回复", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction44", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "14023501"
                                }, 
                                {
                                    "script": "AIAction16", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "140234001"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition34", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "14023501"
                                }
                            ], 
                            "id": 26
                        }, 
                        {
                            "comment": "高级晶石的回复", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction44", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "14023502"
                                }, 
                                {
                                    "script": "AIAction16", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "140234002"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition34", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "14023502"
                                }
                            ], 
                            "id": 27
                        }, 
                        {
                            "comment": "锁定目标2", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction74", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "Role", 
                                    "param2": "14023502", 
                                    "param1": "5"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 40
                        }
                    ]
                }, 
                "initiativeAreaXZ": "5", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 1
            }, 
            3: {
                "name": "三阶段", 
                "tickTimer": 3.0, 
                "statesAI": [
                    {
                        "comment": "更替模型", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction46", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "SM_Qiu_Shu_012"
                            }, 
                            {
                                "script": "AIAction91", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "1", 
                                "param2": "", 
                                "param1": "101982"
                            }
                        ], 
                        "EID": [
                            10
                        ], 
                        "Conditions": [], 
                        "id": 10
                    }, 
                    {
                        "comment": "生命低于75%回血", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "time2"
                            }, 
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "140234001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition9", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "75"
                            }
                        ], 
                        "id": 11
                    }, 
                    {
                        "comment": "生命高于75%切换状态", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "4"
                            }
                        ], 
                        "EID": [
                            12
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition79", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "75"
                            }
                        ], 
                        "id": 12
                    }, 
                    {
                        "comment": "时间超过60秒切换状态", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "4"
                            }
                        ], 
                        "EID": [
                            13
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "60", 
                                "param1": "time2"
                            }
                        ], 
                        "id": 13
                    }, 
                    {
                        "comment": "发送副本失败通知", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "shibai"
                            }
                        ], 
                        "EID": [
                            11
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition9", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "0"
                            }
                        ], 
                        "id": 18
                    }, 
                    {
                        "comment": "发送本阶段时长", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "60", 
                                "param1": "3jieduan"
                            }
                        ], 
                        "EID": [
                            36
                        ], 
                        "Conditions": [], 
                        "id": 36
                    }
                ], 
                "eventsAI": {
                    12: [
                        {
                            "comment": "锁定目标", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction74", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "Role", 
                                    "param2": "14023501", 
                                    "param1": "5"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 28
                        }, 
                        {
                            "comment": "普通晶石的回复", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction44", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "14023501"
                                }, 
                                {
                                    "script": "AIAction16", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "140234001"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition34", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "14023501"
                                }
                            ], 
                            "id": 29
                        }, 
                        {
                            "comment": "高级晶石的回复", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction44", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "14023502"
                                }, 
                                {
                                    "script": "AIAction16", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "140234002"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition34", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "14023502"
                                }
                            ], 
                            "id": 30
                        }, 
                        {
                            "comment": "锁定目标2", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction74", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "Role", 
                                    "param2": "14023502", 
                                    "param1": "5"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 41
                        }
                    ]
                }, 
                "initiativeAreaXZ": "5", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 1
            }, 
            4: {
                "name": "四阶段", 
                "tickTimer": 4.0, 
                "statesAI": [
                    {
                        "comment": "更替模型", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction46", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "SM_Qiu_Shu_041"
                            }, 
                            {
                                "script": "AIAction91", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "1", 
                                "param2": "", 
                                "param1": "101982"
                            }
                        ], 
                        "EID": [
                            14
                        ], 
                        "Conditions": [], 
                        "id": 14
                    }, 
                    {
                        "comment": "生命低于100%回血", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "time3"
                            }, 
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "140234001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition9", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "100"
                            }
                        ], 
                        "id": 15
                    }, 
                    {
                        "comment": "发送副本完成结算通知", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "jiesuan"
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
                                "param1": "100"
                            }
                        ], 
                        "id": 16
                    }, 
                    {
                        "comment": "发送副本失败通知", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "shibai"
                            }
                        ], 
                        "EID": [
                            15
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition9", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "0"
                            }
                        ], 
                        "id": 17
                    }, 
                    {
                        "comment": "发送本阶段时长", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "60", 
                                "param1": "4jieduan"
                            }
                        ], 
                        "EID": [
                            37
                        ], 
                        "Conditions": [], 
                        "id": 37
                    }, 
                    {
                        "comment": "时间超过60秒结算", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "jiesuan"
                            }
                        ], 
                        "EID": [
                            38
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "60", 
                                "param1": "time3"
                            }
                        ], 
                        "id": 38
                    }
                ], 
                "eventsAI": {
                    12: [
                        {
                            "comment": "锁定目标", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction74", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "Role", 
                                    "param2": "14023502", 
                                    "param1": "5"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 31
                        }, 
                        {
                            "comment": "普通晶石的回复", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction44", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "14023501"
                                }, 
                                {
                                    "script": "AIAction16", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "140234001"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition34", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "14023501"
                                }
                            ], 
                            "id": 32
                        }, 
                        {
                            "comment": "高级晶石的回复", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction44", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "14023502"
                                }, 
                                {
                                    "script": "AIAction16", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "140234002"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition34", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "14023502"
                                }
                            ], 
                            "id": 33
                        }, 
                        {
                            "comment": "锁定目标2", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction74", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "Role", 
                                    "param2": "14023502", 
                                    "param1": "5"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 42
                        }
                    ]
                }, 
                "initiativeAreaXZ": "5", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 1
            }
        }, 
        "groupHoldEffectIDs": []
    }, 
    "free": {
        "subStateDatas": {
            2: {
                "name": "添加个怪物让自己进战", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "设置血量，添加一个5秒无敌buff", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction164", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "1"
                            }, 
                            {
                                "script": "AIAction75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "14023701"
                            }
                        ], 
                        "EID": [
                            85
                        ], 
                        "Conditions": [], 
                        "id": 85
                    }, 
                    {
                        "comment": "刷出一个敌对的怪物", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction202", 
                                "param5": "20010540", 
                                "param4": "1", 
                                "param3": "1", 
                                "param2": "2", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            86
                        ], 
                        "Conditions": [], 
                        "id": 86
                    }, 
                    {
                        "comment": "设置出生点", 
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
                        "EID": [], 
                        "Conditions": [], 
                        "id": 87
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