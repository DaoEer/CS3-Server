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
                        "comment": "取消注册", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction298", 
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
                        "Conditions": [], 
                        "id": 29
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
                "name": "默认战斗状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "记录t1（EAI", 
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
                            67
                        ], 
                        "Conditions": [], 
                        "id": 67
                    }, 
                    {
                        "comment": "搜索攻方玩家（测试", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction301", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "0"
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
                        "Conditions": [
                            {
                                "script": "AICondition133", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "0", 
                                "param1": "30"
                            }
                        ], 
                        "id": 125
                    }, 
                    {
                        "comment": "搜索敌对傀儡（测试", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction19", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "303020019|303020020|303020021|303020022|303020023|303020024|303020025|303020026|303020027|303020028", 
                                "param2": "", 
                                "param1": "30"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "303020019|303020020|303020021|303020022|303020023|303020024|303020025|303020026|303020027|303020028", 
                                "param2": "", 
                                "param1": "30"
                            }
                        ], 
                        "id": 124
                    }, 
                    {
                        "comment": "试图用技能1-t1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122556004"
                            }
                        ], 
                        "EID": [
                            68
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "12", 
                                "param1": "t1"
                            }, 
                            {
                                "script": "AICondition10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122556004"
                            }
                        ], 
                        "id": 68
                    }, 
                    {
                        "comment": "试图用技能2-t1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122556002"
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
                                "param1": "68"
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
                                "param1": "t1"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122556002"
                            }, 
                            {
                                "script": "AICondition24", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "6"
                            }
                        ], 
                        "id": 129
                    }, 
                    {
                        "comment": "普通攻击循环", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122556005"
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
                                "param1": "122556005"
                            }
                        ], 
                        "id": 9
                    }, 
                    {
                        "comment": "出生点刷新", 
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
                        "id": 94
                    }, 
                    {
                        "comment": "已设置优先攻击玩家", 
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
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition14", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12105301"
                            }
                        ], 
                        "id": 97
                    }, 
                    {
                        "comment": "已设置优先攻击傀儡", 
                        "odds": 1.0, 
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
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition14", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12105302"
                            }
                        ], 
                        "id": 98
                    }, 
                    {
                        "comment": "每隔10秒优先攻击", 
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
                                "param1": "10"
                            }
                        ], 
                        "id": 99
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "切换攻击性", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction299", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "1", 
                                    "param2": "2500", 
                                    "param1": "5604"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_1", 
                                    "param1": ""
                                }
                            ], 
                            "id": 34
                        }, 
                        {
                            "comment": "切换防御型", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction299", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0", 
                                    "param2": "2500", 
                                    "param1": "5605"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_0", 
                                    "param1": ""
                                }
                            ], 
                            "id": 35
                        }, 
                        {
                            "comment": "优先攻击玩家", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction75", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12255801"
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
                                    "param1": "4"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_2", 
                                    "param1": ""
                                }
                            ], 
                            "id": 42
                        }, 
                        {
                            "comment": "优先攻击傀儡", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction75", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12255802"
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
                                    "param1": "6"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_3", 
                                    "param1": ""
                                }
                            ], 
                            "id": 43
                        }, 
                        {
                            "comment": "广场附近巡逻", 
                            "odds": 1.0, 
                            "Actions": [], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_4", 
                                    "param1": ""
                                }
                            ], 
                            "id": 38
                        }, 
                        {
                            "comment": "灵泉附近巡逻", 
                            "odds": 1.0, 
                            "Actions": [], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_5", 
                                    "param1": ""
                                }
                            ], 
                            "id": 39
                        }, 
                        {
                            "comment": "活动结束，守卫无敌", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction38", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2|4"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "zanling", 
                                    "param1": ""
                                }
                            ], 
                            "id": 132
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
                    ]
                }, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            4: {
                "name": "优先攻击玩家", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "清除EAI（EAI", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "76|82|92"
                            }
                        ], 
                        "EID": [
                            93
                        ], 
                        "Conditions": [], 
                        "id": 93
                    }, 
                    {
                        "comment": "记录t2（EAI", 
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
                            70
                        ], 
                        "Conditions": [], 
                        "id": 70
                    }, 
                    {
                        "comment": "试图用技能1-t2", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122556004"
                            }
                        ], 
                        "EID": [
                            68
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "12", 
                                "param1": "t2"
                            }, 
                            {
                                "script": "AICondition10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122556004"
                            }
                        ], 
                        "id": 71
                    }, 
                    {
                        "comment": "试图用技能2-t2", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122556002"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t2"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t2"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "68"
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
                                "param1": "t2"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122556002"
                            }, 
                            {
                                "script": "AICondition24", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "6"
                            }
                        ], 
                        "id": 130
                    }, 
                    {
                        "comment": "普通攻击循环", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122556005"
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
                                "param1": "122556005"
                            }
                        ], 
                        "id": 69
                    }, 
                    {
                        "comment": "出生点刷新", 
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
                        "id": 73
                    }, 
                    {
                        "comment": "持续搜索玩家", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction301", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "0"
                            }, 
                            {
                                "script": "AIAction11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
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
                                "script": "AICondition133", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "0", 
                                "param1": "100"
                            }
                        ], 
                        "id": 75
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "切换攻击性", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction299", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "1", 
                                    "param2": "2500", 
                                    "param1": "5604"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_1", 
                                    "param1": ""
                                }
                            ], 
                            "id": 50
                        }, 
                        {
                            "comment": "切换防御型", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction299", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0", 
                                    "param2": "2500", 
                                    "param1": "5605"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_0", 
                                    "param1": ""
                                }
                            ], 
                            "id": 51
                        }, 
                        {
                            "comment": "优先攻击玩家", 
                            "odds": 1.0, 
                            "Actions": [], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_2", 
                                    "param1": ""
                                }
                            ], 
                            "id": 52
                        }, 
                        {
                            "comment": "优先攻击傀儡", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction75", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12255802"
                                }, 
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
                                    "param1": "6"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_3", 
                                    "param1": ""
                                }
                            ], 
                            "id": 53
                        }, 
                        {
                            "comment": "广场附近巡逻", 
                            "odds": 1.0, 
                            "Actions": [], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_4", 
                                    "param1": ""
                                }
                            ], 
                            "id": 54
                        }, 
                        {
                            "comment": "灵泉附近巡逻", 
                            "odds": 1.0, 
                            "Actions": [], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_5", 
                                    "param1": ""
                                }
                            ], 
                            "id": 55
                        }, 
                        {
                            "comment": "活动结束，守卫无敌", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction38", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2|4"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "zanling", 
                                    "param1": ""
                                }
                            ], 
                            "id": 133
                        }
                    ], 
                    5: [
                        {
                            "comment": "攻击下一个目标", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction19", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "303020019|303020020|303020021|303020022|303020023|303020024|303020025|303020026|303020027|303020028", 
                                    "param2": "", 
                                    "param1": "100"
                                }, 
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
                            "id": 49
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            6: {
                "name": "优先攻击傀儡", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "清除EAI（EAI", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "70|93"
                            }
                        ], 
                        "EID": [
                            92
                        ], 
                        "Conditions": [], 
                        "id": 92
                    }, 
                    {
                        "comment": "记录t3（EAI", 
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
                            76
                        ], 
                        "Conditions": [], 
                        "id": 76
                    }, 
                    {
                        "comment": "试图用技能1-t3", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122556004"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "d1"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "d1"
                            }
                        ], 
                        "EID": [
                            80
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "12", 
                                "param1": "t3"
                            }, 
                            {
                                "script": "AICondition10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122556004"
                            }
                        ], 
                        "id": 80
                    }, 
                    {
                        "comment": "试图用技能2-t3", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122556002"
                            }, 
                            {
                                "script": "AIAction18", 
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
                                "param1": "t3"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "80"
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
                                "param1": "t3"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122556002"
                            }, 
                            {
                                "script": "AICondition24", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "6"
                            }
                        ], 
                        "id": 131
                    }, 
                    {
                        "comment": "普通攻击循环-d1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122556005"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "d1"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "d1"
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
                                "param1": "122556005"
                            }
                        ], 
                        "id": 79
                    }, 
                    {
                        "comment": "出生点刷新", 
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
                        "id": 81
                    }, 
                    {
                        "comment": "持续搜索傀儡（EAI", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "303020019|303020020|303020021|303020022|303020023|303020024|303020025|303020026|303020027|303020028", 
                                "param2": "Monster", 
                                "param1": "100"
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
                            82
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "303020019|303020020|303020021|303020022|303020023|303020024|303020025|303020026|303020027|303020028", 
                                "param2": "Monster", 
                                "param1": "100"
                            }
                        ], 
                        "id": 82
                    }, 
                    {
                        "comment": "不存在傀儡，攻击玩家", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction301", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "0"
                            }, 
                            {
                                "script": "AIAction14", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "82"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition22", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "303020019|303020020|303020021|303020022|303020023|303020024|303020025|303020026|303020027|303020028", 
                                "param2": "Monster", 
                                "param1": "100"
                            }
                        ], 
                        "id": 90
                    }, 
                    {
                        "comment": "追不到攻击目标切换-d1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "d1"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "82"
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
                                "param1": "d1"
                            }
                        ], 
                        "id": 95
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "切换攻击性", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction299", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "1", 
                                    "param2": "2500", 
                                    "param1": "5604"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_1", 
                                    "param1": ""
                                }
                            ], 
                            "id": 84
                        }, 
                        {
                            "comment": "切换防御型", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction299", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0", 
                                    "param2": "2500", 
                                    "param1": "5605"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_0", 
                                    "param1": ""
                                }
                            ], 
                            "id": 85
                        }, 
                        {
                            "comment": "优先攻击玩家", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction75", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12255801"
                                }, 
                                {
                                    "script": "AIAction18", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t3"
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
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_2", 
                                    "param1": ""
                                }
                            ], 
                            "id": 86
                        }, 
                        {
                            "comment": "优先攻击傀儡", 
                            "odds": 1.0, 
                            "Actions": [], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_3", 
                                    "param1": ""
                                }
                            ], 
                            "id": 87
                        }, 
                        {
                            "comment": "广场附近巡逻", 
                            "odds": 1.0, 
                            "Actions": [], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_4", 
                                    "param1": ""
                                }
                            ], 
                            "id": 88
                        }, 
                        {
                            "comment": "灵泉附近巡逻", 
                            "odds": 1.0, 
                            "Actions": [], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_5", 
                                    "param1": ""
                                }
                            ], 
                            "id": 89
                        }, 
                        {
                            "comment": "活动结束，守卫无敌", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction38", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2|4"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "zanling", 
                                    "param1": ""
                                }
                            ], 
                            "id": 134
                        }
                    ], 
                    5: [
                        {
                            "comment": "攻击下一个目标", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "82"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 83
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
                "name": "默认广场巡逻", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "重置出生点（EAI", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction50", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "-919 -2730 11227"
                            }
                        ], 
                        "EID": [
                            126
                        ], 
                        "Conditions": [], 
                        "id": 126
                    }, 
                    {
                        "comment": "霸体BUFF(EAI", 
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
                            20
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
                        "id": 20
                    }, 
                    {
                        "comment": "焱牛BUFF(EAI", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12251903"
                            }
                        ], 
                        "EID": [
                            23
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition15", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12251903"
                            }
                        ], 
                        "id": 23
                    }, 
                    {
                        "comment": "重置朝向(EAI", 
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
                            10
                        ], 
                        "Conditions": [], 
                        "id": 10
                    }, 
                    {
                        "comment": "随机选择巡逻路线（EAI", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction99", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122559001|122559002|122559003|122559004"
                            }
                        ], 
                        "EID": [
                            96
                        ], 
                        "Conditions": [], 
                        "id": 96
                    }, 
                    {
                        "comment": "搜索攻方玩家（测试", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction301", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "0"
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
                        "Conditions": [
                            {
                                "script": "AICondition133", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "0", 
                                "param1": "30"
                            }
                        ], 
                        "id": 122
                    }, 
                    {
                        "comment": "搜索敌对傀儡（测试", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction19", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "303020019|303020020|303020021|303020022|303020023|303020024|303020025|303020026|303020027|303020028", 
                                "param2": "", 
                                "param1": "30"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "303020019|303020020|303020021|303020022|303020023|303020024|303020025|303020026|303020027|303020028", 
                                "param2": "", 
                                "param1": "30"
                            }
                        ], 
                        "id": 123
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "切换攻击型", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction299", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "1", 
                                    "param2": "2500", 
                                    "param1": "5604"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_1", 
                                    "param1": ""
                                }
                            ], 
                            "id": 26
                        }, 
                        {
                            "comment": "切换防御型", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction299", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0", 
                                    "param2": "2500", 
                                    "param1": "5605"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_0", 
                                    "param1": ""
                                }
                            ], 
                            "id": 27
                        }, 
                        {
                            "comment": "广场附近巡逻", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "96"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_4", 
                                    "param1": ""
                                }
                            ], 
                            "id": 32
                        }, 
                        {
                            "comment": "灵泉附近巡逻", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "3"
                                }, 
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "107"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_5", 
                                    "param1": ""
                                }
                            ], 
                            "id": 33
                        }, 
                        {
                            "comment": "优先攻击玩家", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction75", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12255801"
                                }, 
                                {
                                    "script": "AIAction301", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "0"
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
                                    "param2": "Menu_2", 
                                    "param1": ""
                                }
                            ], 
                            "id": 44
                        }, 
                        {
                            "comment": "优先攻击傀儡", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction75", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12255802"
                                }, 
                                {
                                    "script": "AIAction19", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "303020019|303020020|303020021|303020022|303020023|303020024|303020025|303020026|303020027|303020028", 
                                    "param2": "", 
                                    "param1": "100"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_3", 
                                    "param1": ""
                                }
                            ], 
                            "id": 45
                        }, 
                        {
                            "comment": "广场巡逻1", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction41", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1", 
                                    "param1": "1"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "gc1", 
                                    "param1": ""
                                }
                            ], 
                            "id": 100
                        }, 
                        {
                            "comment": "广场巡逻2", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction41", 
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
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "gc2", 
                                    "param1": ""
                                }
                            ], 
                            "id": 101
                        }, 
                        {
                            "comment": "广场巡逻3", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction41", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1", 
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
                                    "param2": "gc3", 
                                    "param1": ""
                                }
                            ], 
                            "id": 102
                        }, 
                        {
                            "comment": "广场巡逻4", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction41", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1", 
                                    "param1": "4"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "gc4", 
                                    "param1": ""
                                }
                            ], 
                            "id": 103
                        }, 
                        {
                            "comment": "活动结束，守卫无敌", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction38", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2|4"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "zanling", 
                                    "param1": ""
                                }
                            ], 
                            "id": 135
                        }
                    ], 
                    21: [
                        {
                            "comment": "注册怪物", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction297", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "1"
                                }
                            ], 
                            "EID": [
                                28
                            ], 
                            "Conditions": [], 
                            "id": 28
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            3: {
                "name": "灵泉巡逻", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "霸体BUFF(EAI", 
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
                            104
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
                        "id": 104
                    }, 
                    {
                        "comment": "焱牛BUFF(EAI", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12251903"
                            }
                        ], 
                        "EID": [
                            105
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition15", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12251903"
                            }
                        ], 
                        "id": 105
                    }, 
                    {
                        "comment": "重置朝向(EAI", 
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
                            106
                        ], 
                        "Conditions": [], 
                        "id": 106
                    }, 
                    {
                        "comment": "随机选择巡逻路线（EAI", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction99", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122559005|122559006"
                            }
                        ], 
                        "EID": [
                            107
                        ], 
                        "Conditions": [], 
                        "id": 107
                    }, 
                    {
                        "comment": "搜索攻方玩家（测试", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction301", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "0"
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
                        "Conditions": [
                            {
                                "script": "AICondition133", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "0", 
                                "param1": "30"
                            }
                        ], 
                        "id": 120
                    }, 
                    {
                        "comment": "搜索敌对傀儡（测试", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction19", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "303020019|303020020|303020021|303020022|303020023|303020024|303020025|303020026|303020027|303020028", 
                                "param2": "", 
                                "param1": "30"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "303020019|303020020|303020021|303020022|303020023|303020024|303020025|303020026|303020027|303020028", 
                                "param2": "", 
                                "param1": "30"
                            }
                        ], 
                        "id": 121
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "切换攻击性", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction299", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "1", 
                                    "param2": "2500", 
                                    "param1": "5604"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_1", 
                                    "param1": ""
                                }
                            ], 
                            "id": 109
                        }, 
                        {
                            "comment": "切换防御型", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction299", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0", 
                                    "param2": "2500", 
                                    "param1": "5605"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_0", 
                                    "param1": ""
                                }
                            ], 
                            "id": 110
                        }, 
                        {
                            "comment": "广场附近巡逻", 
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
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "96"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_4", 
                                    "param1": ""
                                }
                            ], 
                            "id": 111
                        }, 
                        {
                            "comment": "灵泉附近巡逻", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "107"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_5", 
                                    "param1": ""
                                }
                            ], 
                            "id": 112
                        }, 
                        {
                            "comment": "优先攻击玩家", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction75", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12255801"
                                }, 
                                {
                                    "script": "AIAction301", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "0"
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
                                    "param2": "Menu_2", 
                                    "param1": ""
                                }
                            ], 
                            "id": 113
                        }, 
                        {
                            "comment": "优先攻击傀儡", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction75", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "12255802"
                                }, 
                                {
                                    "script": "AIAction19", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "303020019|303020020|303020021|303020022|303020023|303020024|303020025|303020026|303020027|303020028", 
                                    "param2": "", 
                                    "param1": "100"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Menu_3", 
                                    "param1": ""
                                }
                            ], 
                            "id": 114
                        }, 
                        {
                            "comment": "灵泉巡逻5", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction41", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1", 
                                    "param1": "5"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "lq5", 
                                    "param1": ""
                                }
                            ], 
                            "id": 115
                        }, 
                        {
                            "comment": "灵泉巡逻6", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction41", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "1", 
                                    "param1": "6"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "lq6", 
                                    "param1": ""
                                }
                            ], 
                            "id": 116
                        }, 
                        {
                            "comment": "活动结束，守卫无敌", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction38", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2|4"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "zanling", 
                                    "param1": ""
                                }
                            ], 
                            "id": 136
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