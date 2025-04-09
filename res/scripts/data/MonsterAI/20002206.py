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
                        "id": 56
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
                "name": "死亡喊话", 
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
                                "param2": "C000087", 
                                "param1": "15"
                            }
                        ], 
                        "EID": [
                            25
                        ], 
                        "Conditions": [], 
                        "id": 25
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
    "fight": {
        "subStateDatas": {
            1: {
                "name": "战斗状态变身前", 
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
                            54
                        ], 
                        "Conditions": [], 
                        "id": 54
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
                            26
                        ], 
                        "Conditions": [], 
                        "id": 26
                    }, 
                    {
                        "comment": "计时", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t1"
                            }
                        ], 
                        "EID": [
                            23
                        ], 
                        "Conditions": [], 
                        "id": 23
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
                                "param2": "C000084", 
                                "param1": "30"
                            }
                        ], 
                        "EID": [
                            22
                        ], 
                        "Conditions": [], 
                        "id": 22
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
                            3
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120065001"
                            }
                        ], 
                        "id": 3
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
                        "id": 32
                    }, 
                    {
                        "comment": "玩家喊话", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000085", 
                                "param1": "30"
                            }
                        ], 
                        "EID": [
                            24
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "6", 
                                "param1": "t1"
                            }
                        ], 
                        "id": 24
                    }, 
                    {
                        "comment": "呼啸", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120321001"
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
                                "param1": "35"
                            }
                        ], 
                        "id": 47
                    }, 
                    {
                        "comment": "血量低于40%变身", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction57", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120151001"
                            }, 
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000086", 
                                "param1": "30"
                            }, 
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
                            29
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
                        "id": 29
                    }, 
                    {
                        "comment": "第一招", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "K000037", 
                                "param1": "15"
                            }
                        ], 
                        "EID": [
                            7
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
                        "id": 7
                    }, 
                    {
                        "comment": "第二招", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "K000038", 
                                "param1": "15"
                            }
                        ], 
                        "EID": [
                            8
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition2", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "40"
                            }
                        ], 
                        "id": 8
                    }, 
                    {
                        "comment": "第三招", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "K000039", 
                                "param1": "15"
                            }
                        ], 
                        "EID": [
                            9
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition2", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "65"
                            }
                        ], 
                        "id": 9
                    }, 
                    {
                        "comment": "第四招", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "K000040", 
                                "param1": "15"
                            }
                        ], 
                        "EID": [
                            10
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition2", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "90"
                            }
                        ], 
                        "id": 10
                    }, 
                    {
                        "comment": "第五招", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "K000041", 
                                "param1": "15"
                            }
                        ], 
                        "EID": [
                            11
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition2", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "110"
                            }
                        ], 
                        "id": 11
                    }, 
                    {
                        "comment": "第六招", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "K000042", 
                                "param1": "15"
                            }
                        ], 
                        "EID": [
                            12
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition2", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "125"
                            }
                        ], 
                        "id": 12
                    }, 
                    {
                        "comment": "循环技能", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction42", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120113001|120114001|120115001|120116001|120117001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 21
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
                            "id": 55
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
                            "id": 17
                        }
                    ], 
                    6: [
                        {
                            "comment": "低于40%变身", 
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
                                20
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
                            "id": 20
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            3: {
                "name": "变身", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "计时", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t3"
                            }
                        ], 
                        "EID": [
                            39
                        ], 
                        "Conditions": [], 
                        "id": 39
                    }, 
                    {
                        "comment": "变身", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120139001"
                            }
                        ], 
                        "EID": [
                            28
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120139001"
                            }
                        ], 
                        "id": 28
                    }, 
                    {
                        "comment": "时间到达跳到4", 
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
                            40
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "5", 
                                "param1": "t3"
                            }
                        ], 
                        "id": 40
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
                            "id": 57
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            4: {
                "name": "战斗状态变身后", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "计时", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t4"
                            }
                        ], 
                        "EID": [
                            33
                        ], 
                        "Conditions": [], 
                        "id": 33
                    }, 
                    {
                        "comment": "时间到达跳到5", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction57", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120151001"
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
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "5"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "33|34"
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
                                "param2": "20", 
                                "param1": "t4"
                            }
                        ], 
                        "id": 34
                    }, 
                    {
                        "comment": "技能组", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction42", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120136001|120137001|120138001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 30
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
                            "id": 59
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
                            "id": 44
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            5: {
                "name": "跳扑", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "计时", 
                        "odds": 1.0, 
                        "Actions": [
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
                            36
                        ], 
                        "Conditions": [], 
                        "id": 36
                    }, 
                    {
                        "comment": "跳扑", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction63", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "30"
                            }, 
                            {
                                "script": "AIAction34", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120157001"
                            }
                        ], 
                        "EID": [
                            35
                        ], 
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
                        "id": 35
                    }, 
                    {
                        "comment": "跳扑", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction63", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "30"
                            }, 
                            {
                                "script": "AIAction34", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120157001"
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
                                "param2": "6", 
                                "param1": "t5"
                            }
                        ], 
                        "id": 41
                    }, 
                    {
                        "comment": "跳扑", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction63", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "30"
                            }, 
                            {
                                "script": "AIAction34", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120157001"
                            }
                        ], 
                        "EID": [
                            42
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "10", 
                                "param1": "t5"
                            }
                        ], 
                        "id": 42
                    }, 
                    {
                        "comment": "跳扑", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction63", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "30"
                            }, 
                            {
                                "script": "AIAction34", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120157001"
                            }
                        ], 
                        "EID": [
                            43
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "14", 
                                "param1": "t5"
                            }
                        ], 
                        "id": 43
                    }, 
                    {
                        "comment": "时间到达回到4", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t5"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "36|37|41|42|43|35"
                            }, 
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
                            37
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "18", 
                                "param1": "t5"
                            }
                        ], 
                        "id": 37
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
                            "id": 60
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
            2: {
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
                            46
                        ], 
                        "Conditions": [], 
                        "id": 46
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
    "pead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}