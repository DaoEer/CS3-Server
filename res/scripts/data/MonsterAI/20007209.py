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
                        "comment": "死亡喊话", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000434", 
                                "param1": "50"
                            }, 
                            {
                                "script": "AIAction94", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "50", 
                                "param2": "20007210", 
                                "param1": "Monster"
                            }
                        ], 
                        "EID": [
                            25
                        ], 
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
    "fight": {
        "subStateDatas": {
            1: {
                "name": "通用战斗状态", 
                "tickTimer": 0.5, 
                "statesAI": [
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
                        "id": 2
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
                        "id": 3
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
                        "id": 4
                    }, 
                    {
                        "comment": "距离玩家小于2米攻击或者远离", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction175", 
                                "param5": "", 
                                "param4": "5", 
                                "param3": "120944001|120945001|120946001|120947001|120948001", 
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
                        "id": 5
                    }, 
                    {
                        "comment": "记录时间t1", 
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
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "29|30|31|33"
                            }
                        ], 
                        "EID": [
                            8
                        ], 
                        "Conditions": [], 
                        "id": 8
                    }, 
                    {
                        "comment": "t2", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t2"
                            }, 
                            {
                                "script": "AIAction63", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "60"
                            }
                        ], 
                        "EID": [
                            15
                        ], 
                        "Conditions": [], 
                        "id": 15
                    }, 
                    {
                        "comment": "技能", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction34", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120958001"
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
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "15"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "8", 
                                "param1": "t2"
                            }
                        ], 
                        "id": 16
                    }, 
                    {
                        "comment": "每隔15s召唤法宝", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "8"
                            }, 
                            {
                                "script": "AIAction48", 
                                "param5": "20007210", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "8978.3 -15593.08 4255.06"
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
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "t1"
                            }, 
                            {
                                "script": "AICondition28", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "biaoji"
                            }
                        ], 
                        "id": 10
                    }, 
                    {
                        "comment": "=10个 biaoji", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction55", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "biaoji"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition29", 
                                "param5": "10", 
                                "param4": "0", 
                                "param3": "20007210", 
                                "param2": "Monster", 
                                "param1": "50"
                            }
                        ], 
                        "id": 13
                    }, 
                    {
                        "comment": "移除标记", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "biaoji"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition29", 
                                "param5": "10", 
                                "param4": "1", 
                                "param3": "20007210", 
                                "param2": "Monster", 
                                "param1": "50"
                            }
                        ], 
                        "id": 14
                    }, 
                    {
                        "comment": "切换状态2", 
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
                            27
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "30", 
                                "param1": "b1"
                            }
                        ], 
                        "id": 27
                    }, 
                    {
                        "comment": "b1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "b1"
                            }
                        ], 
                        "EID": [
                            28
                        ], 
                        "Conditions": [], 
                        "id": 28
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
                            "id": 6
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            2: {
                "name": "掉火球", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "b2\\自身施法", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "b2"
                            }, 
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120961001"
                            }
                        ], 
                        "EID": [
                            29
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120961001"
                            }
                        ], 
                        "id": 29
                    }, 
                    {
                        "comment": "无", 
                        "odds": 1.0, 
                        "Actions": [], 
                        "EID": [
                            33
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "3", 
                                "param1": "b2"
                            }
                        ], 
                        "id": 33
                    }, 
                    {
                        "comment": "b2=2", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction169", 
                                "param5": "5|5|20007597", 
                                "param4": "20|2", 
                                "param3": "", 
                                "param2": "0 0 0", 
                                "param1": "8978.3 -15593.08 4255.06"
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "5|5|20007597", 
                                "param4": "20|2", 
                                "param3": "", 
                                "param2": "0 0 0", 
                                "param1": "8978.3 -15593.08 4255.06"
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "5|5|20007597", 
                                "param4": "20|2", 
                                "param3": "", 
                                "param2": "0 0 0", 
                                "param1": "8978.3 -15593.08 4255.06"
                            }
                        ], 
                        "EID": [
                            30
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "b2"
                            }, 
                            {
                                "script": "AICondition17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "8978.3 -15593.08 4255.06"
                            }
                        ], 
                        "id": 30
                    }, 
                    {
                        "comment": "b2=12", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction169", 
                                "param5": "5|9|20007597", 
                                "param4": "40|8", 
                                "param3": "120", 
                                "param2": "0 0 90", 
                                "param1": "8978.3 -15593.08 4255.06"
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "5|9|20007597", 
                                "param4": "40|8", 
                                "param3": "120", 
                                "param2": "0 0 270", 
                                "param1": "8978.3 -15593.08 4255.06"
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "5|9|20007597", 
                                "param4": "40|8", 
                                "param3": "120", 
                                "param2": "0 0 30", 
                                "param1": "8978.3 -15593.08 4255.06"
                            }
                        ], 
                        "EID": [
                            31
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "12", 
                                "param1": "b2"
                            }
                        ], 
                        "id": 31
                    }, 
                    {
                        "comment": "b2=13 清除b2", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "b2|b1"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "8|15|27|28"
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
                                "param2": "13", 
                                "param1": "b2"
                            }
                        ], 
                        "id": 32
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
                "name": "霸体", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "增加屏蔽头顶名字的标志位", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction38", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "13"
                            }
                        ], 
                        "EID": [
                            34
                        ], 
                        "Conditions": [], 
                        "id": 34
                    }, 
                    {
                        "comment": "喊话计时", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "h1"
                            }, 
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000427", 
                                "param1": "50"
                            }, 
                            {
                                "script": "AIAction55", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "h1"
                            }
                        ], 
                        "EID": [
                            26
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "20"
                            }, 
                            {
                                "script": "AICondition28", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "h1"
                            }
                        ], 
                        "id": 26
                    }, 
                    {
                        "comment": "霸体BUFF", 
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
                            7
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
                        "id": 7
                    }, 
                    {
                        "comment": "发副本456", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "456"
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
                                "param1": "a1"
                            }
                        ], 
                        "id": 19
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
                                "param2": "C000428", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            21
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "3", 
                                "param1": "a1"
                            }
                        ], 
                        "id": 21
                    }, 
                    {
                        "comment": "BOSS喊话", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000430", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            22
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "10", 
                                "param1": "a1"
                            }
                        ], 
                        "id": 22
                    }, 
                    {
                        "comment": "玩家回话", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000431", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            23
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "a1"
                            }
                        ], 
                        "id": 23
                    }, 
                    {
                        "comment": "BOSS回话", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000433", 
                                "param1": "50"
                            }, 
                            {
                                "script": "AIAction39", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
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
                                "param2": "20", 
                                "param1": "a1"
                            }
                        ], 
                        "id": 24
                    }, 
                    {
                        "comment": "清除一组EAI", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "8"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 9
                    }, 
                    {
                        "comment": "移除13标志位", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction39", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "13"
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
                    9: [
                        {
                            "comment": "2标志", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "a1"
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
                                    "param1": "555"
                                }
                            ], 
                            "id": 18
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