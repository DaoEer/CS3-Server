# -*- coding: utf-8 -*-
Datas = {
    "reset": {
        "subStateDatas": {
            1: {
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "重置后关闭光墙", 
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
    "FSM": 1, 
    "dead": {
        "subStateDatas": {
            1: {
                "name": "死亡状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "死亡喊话", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000921", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            50
                        ], 
                        "Conditions": [], 
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
            1: {
                "name": "普通状态", 
                "tickTimer": 0.5, 
                "statesAI": [
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
                                "param1": "10"
                            }
                        ], 
                        "EID": [
                            62
                        ], 
                        "Conditions": [], 
                        "id": 62
                    }, 
                    {
                        "comment": "霸体", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120065001"
                            }
                        ], 
                        "EID": [
                            47
                        ], 
                        "Conditions": [], 
                        "id": 47
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
                            }
                        ], 
                        "EID": [
                            1
                        ], 
                        "Conditions": [], 
                        "id": 1
                    }, 
                    {
                        "comment": "每隔3秒钟，选择对自己造成伤害最高的人作为目标", 
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
                        "id": 2
                    }, 
                    {
                        "comment": "与玩家的距离小于2米攻击玩家或者远离玩家", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction71", 
                                "param5": "", 
                                "param4": "120374001|120373001|120372001", 
                                "param3": "2.5", 
                                "param2": "1", 
                                "param1": "0.9"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 5
                    }, 
                    {
                        "comment": "记录当前时间（t1 t4 t3 t5），设置 12 73 EAI", 
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
                                "param1": "t4"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t3"
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
                        "EID": [
                            7, 
                            12, 
                            73
                        ], 
                        "Conditions": [], 
                        "id": 7
                    }, 
                    {
                        "comment": "召唤鬼手（废弃）", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction85", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "20003279"
                            }
                        ], 
                        "EID": [
                            8
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "35", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 8
                    }, 
                    {
                        "comment": "切换状态", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t2"
                            }, 
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
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "45", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 9
                    }, 
                    {
                        "comment": "怪物喊话", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000166", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            48
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "t3"
                            }
                        ], 
                        "id": 48
                    }, 
                    {
                        "comment": "玩家回话", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000167", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            49
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "6", 
                                "param1": "t3"
                            }
                        ], 
                        "id": 49
                    }, 
                    {
                        "comment": "怪物再回话", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000169", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            51
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "10", 
                                "param1": "t3"
                            }
                        ], 
                        "id": 51
                    }, 
                    {
                        "comment": "怪物技能喊话一", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "S000685", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            52
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "25", 
                                "param1": "t3"
                            }
                        ], 
                        "id": 52
                    }, 
                    {
                        "comment": "怪物技能喊话二", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "S000686", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            53
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "65", 
                                "param1": "t3"
                            }
                        ], 
                        "id": 53
                    }, 
                    {
                        "comment": "怪物技能喊话三", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "S000687", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            54
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "105", 
                                "param1": "t3"
                            }
                        ], 
                        "id": 54
                    }, 
                    {
                        "comment": "怪物技能喊话四", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "S000688", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            55
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "145", 
                                "param1": "t3"
                            }
                        ], 
                        "id": 55
                    }, 
                    {
                        "comment": "怪物技能喊话五", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "S000689", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            56
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "185", 
                                "param1": "t3"
                            }
                        ], 
                        "id": 56
                    }, 
                    {
                        "comment": "怪物技能喊话六", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "S000690", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            57
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "225", 
                                "param1": "t3"
                            }
                        ], 
                        "id": 57
                    }, 
                    {
                        "comment": "召唤冰锥陷阱，重新计时", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction85", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "20003567"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t4"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t4"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "72"
                            }
                        ], 
                        "EID": [
                            59
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20", 
                                "param1": "t4"
                            }
                        ], 
                        "id": 59
                    }, 
                    {
                        "comment": "召唤离火水晶，重新计时", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120392001"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t5"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t5"
                            }, 
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000920", 
                                "param1": "79"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "72"
                            }
                        ], 
                        "EID": [
                            61
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "35", 
                                "param1": "t5"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120392001"
                            }
                        ], 
                        "id": 61
                    }, 
                    {
                        "comment": "召唤冰锥陷阱，重新计时", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction85", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "20003567"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t4"
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
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "30", 
                                "param1": "t4"
                            }
                        ], 
                        "id": 72
                    }, 
                    {
                        "comment": "召唤离火水晶，重新计时", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120392001"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t5"
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
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "45", 
                                "param1": "t5"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120392001"
                            }
                        ], 
                        "id": 73
                    }
                ], 
                "eventsAI": {
                    19: [
                        {
                            "comment": "超出BOSS区域重置", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction33", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 63
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
                            "id": 6
                        }
                    ], 
                    6: [
                        {
                            "comment": "生命值低于80，跳转等级3（废弃）", 
                            "odds": 0.0, 
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
                                13
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
                            "id": 13
                        }, 
                        {
                            "comment": "生命值低于60，跳转等级4（废弃）", 
                            "odds": 0.0, 
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
                                14
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
                            "id": 14
                        }, 
                        {
                            "comment": "生命值低于40，跳转等级5（废弃）", 
                            "odds": 0.0, 
                            "Actions": [
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "5"
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
                                    "param1": "40"
                                }
                            ], 
                            "id": 15
                        }, 
                        {
                            "comment": "生命值低于20，跳转等级6（废弃）", 
                            "odds": 0.0, 
                            "Actions": [
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "6"
                                }
                            ], 
                            "EID": [
                                16
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
                            "id": 16
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            2: {
                "name": "寒冰状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "记录标签t2", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t2"
                            }
                        ], 
                        "EID": [
                            11
                        ], 
                        "Conditions": [], 
                        "id": 11
                    }, 
                    {
                        "comment": "使用酷炫技能", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120378001"
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
                                "param1": "t2"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120378001"
                            }
                        ], 
                        "id": 12
                    }, 
                    {
                        "comment": "切换状态", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction18", 
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
                                "param1": "t1"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "11|12|8"
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
                                "param2": "9", 
                                "param1": "t2"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120378001"
                            }
                        ], 
                        "id": 10
                    }, 
                    {
                        "comment": "使用酷炫技能", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120378001"
                            }, 
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000919", 
                                "param1": "79"
                            }
                        ], 
                        "EID": [
                            76
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "t2"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120378001"
                            }
                        ], 
                        "id": 76
                    }
                ], 
                "eventsAI": {
                    19: [
                        {
                            "comment": "超出BOSS区域重置", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction33", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 64
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
                            "id": 70
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            3: {
                "name": "80血量状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "记录当前时间", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "n1"
                            }
                        ], 
                        "EID": [
                            17
                        ], 
                        "Conditions": [], 
                        "id": 17
                    }, 
                    {
                        "comment": "使用传送技能，记录下一个时间标签", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120380001"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "n2"
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
                                "param1": "n1"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120380001"
                            }
                        ], 
                        "id": 18
                    }, 
                    {
                        "comment": "到达位置，记录时间， 发送指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "n3"
                            }, 
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "251", 
                                "param2": "20003280", 
                                "param1": "5"
                            }
                        ], 
                        "EID": [
                            18, 
                            19
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "n2"
                            }, 
                            {
                                "script": "AICondition17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "-13009 -21979 7985"
                            }
                        ], 
                        "id": 19
                    }, 
                    {
                        "comment": "选择AI目标", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20003280", 
                                "param2": "Monster", 
                                "param1": "5"
                            }
                        ], 
                        "EID": [
                            20
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "n3"
                            }
                        ], 
                        "id": 20
                    }, 
                    {
                        "comment": "到达时间增加增益BUFF", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "n1|n2|n3"
                            }, 
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "250", 
                                "param2": "20003280", 
                                "param1": "5"
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
                                "param2": "10", 
                                "param1": "n3"
                            }
                        ], 
                        "id": 22
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到指令，切换状态", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction18", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "n1|n2|n3"
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
                            "EID": [
                                29
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "3280", 
                                    "param1": "20003280"
                                }
                            ], 
                            "id": 29
                        }
                    ], 
                    19: [
                        {
                            "comment": "超出BOSS区域重置", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction33", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 65
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            4: {
                "name": "60血量状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "记录当前时间", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "n1"
                            }
                        ], 
                        "EID": [
                            46
                        ], 
                        "Conditions": [], 
                        "id": 46
                    }, 
                    {
                        "comment": "使用传送技能，记录下一个时间标签", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120380002"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "n2"
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
                                "param1": "n1"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120380002"
                            }
                        ], 
                        "id": 24
                    }, 
                    {
                        "comment": "到达位置，记录时间， 发送指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "n3"
                            }, 
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "251", 
                                "param2": "20003280", 
                                "param1": "5"
                            }
                        ], 
                        "EID": [
                            25, 
                            24
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "n2"
                            }, 
                            {
                                "script": "AICondition17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "-15169 -23059 7985"
                            }
                        ], 
                        "id": 25
                    }, 
                    {
                        "comment": "选择AI目标", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20003280", 
                                "param2": "Monster", 
                                "param1": "5"
                            }
                        ], 
                        "EID": [
                            26
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "n3"
                            }
                        ], 
                        "id": 26
                    }, 
                    {
                        "comment": "到达时间增加增益BUFF", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "n1|n2|n3"
                            }, 
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "250", 
                                "param2": "20003280", 
                                "param1": "5"
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
                                "param2": "10", 
                                "param1": "n3"
                            }
                        ], 
                        "id": 28
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到指令，切换状态1", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction18", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "n1|n2|n3"
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
                            "EID": [
                                30
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "3280", 
                                    "param1": "20003280"
                                }
                            ], 
                            "id": 30
                        }
                    ], 
                    19: [
                        {
                            "comment": "超出BOSS区域重置", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction33", 
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
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            5: {
                "name": "40血量状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "记录当前时间", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "n1"
                            }
                        ], 
                        "EID": [
                            31
                        ], 
                        "Conditions": [], 
                        "id": 31
                    }, 
                    {
                        "comment": "使用传送技能，记录下一个时间标签", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120380003"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "n2"
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
                                "param1": "n1"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120380003"
                            }
                        ], 
                        "id": 32
                    }, 
                    {
                        "comment": "到达位置，记录时间， 发送指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "n3"
                            }, 
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "251", 
                                "param2": "20003280", 
                                "param1": "5"
                            }
                        ], 
                        "EID": [
                            33, 
                            32
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "n2"
                            }, 
                            {
                                "script": "AICondition17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "-14419 -24819 7985"
                            }
                        ], 
                        "id": 33
                    }, 
                    {
                        "comment": "选择AI目标", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20003280", 
                                "param2": "Monster", 
                                "param1": "5"
                            }
                        ], 
                        "EID": [
                            34
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "n3"
                            }
                        ], 
                        "id": 34
                    }, 
                    {
                        "comment": "到达时间增加增益BUFF", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "n1|n2|n3"
                            }, 
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "250", 
                                "param2": "20003280", 
                                "param1": "5"
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
                                "param2": "10", 
                                "param1": "n3"
                            }
                        ], 
                        "id": 36
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到指令，切换状态1", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction18", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "n1|n2|n3"
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
                            "EID": [
                                37
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "3280", 
                                    "param1": "20003280"
                                }
                            ], 
                            "id": 37
                        }
                    ], 
                    19: [
                        {
                            "comment": "超出BOSS区域重置", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction33", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 67
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            6: {
                "name": "20血量状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "记录当前时间", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "n1"
                            }
                        ], 
                        "EID": [
                            38
                        ], 
                        "Conditions": [], 
                        "id": 38
                    }, 
                    {
                        "comment": "使用传送技能，记录下一个时间标签", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120380004"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "n2"
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
                                "param1": "n1"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120380004"
                            }
                        ], 
                        "id": 39
                    }, 
                    {
                        "comment": "到达位置，记录时间， 发送指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "n3"
                            }, 
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "251", 
                                "param2": "20003280", 
                                "param1": "5"
                            }
                        ], 
                        "EID": [
                            40, 
                            39
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "n2"
                            }, 
                            {
                                "script": "AICondition17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "-12059 -23669 7985"
                            }
                        ], 
                        "id": 40
                    }, 
                    {
                        "comment": "选择AI目标", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20003280", 
                                "param2": "Monster", 
                                "param1": "5"
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
                                "param1": "n3"
                            }
                        ], 
                        "id": 41
                    }, 
                    {
                        "comment": "到达时间增加增益BUFF", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "n1|n2|n3"
                            }, 
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "250", 
                                "param2": "20003280", 
                                "param1": "5"
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
                                "param2": "10", 
                                "param1": "n3"
                            }
                        ], 
                        "id": 43
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到指令，切换状态1", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction18", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "n1|n2|n3"
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
                            "EID": [
                                44
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "3280", 
                                    "param1": "20003280"
                                }
                            ], 
                            "id": 44
                        }
                    ], 
                    19: [
                        {
                            "comment": "超出BOSS区域重置", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction33", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 68
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
                "name": "自由状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "霸体", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120065001"
                            }
                        ], 
                        "EID": [
                            45
                        ], 
                        "Conditions": [], 
                        "id": 45
                    }, 
                    {
                        "comment": "喊话，标记 hua ，时间标签 h1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000915|C000916|C000918", 
                                "param1": "79"
                            }, 
                            {
                                "script": "AIAction55", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "hua"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "h1"
                            }
                        ], 
                        "EID": [
                            74
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "30"
                            }, 
                            {
                                "script": "AICondition28", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "hua"
                            }
                        ], 
                        "id": 74
                    }, 
                    {
                        "comment": "说完话进战斗", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction19", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
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
                                "param2": "25", 
                                "param1": "h1"
                            }
                        ], 
                        "id": 75
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