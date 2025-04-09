# -*- coding: utf-8 -*-
Datas = {
    "reset": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "show": {
        "subStateDatas": {
            1: {
                "name": "喊话", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "改变自身朝向", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction26", 
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
                                "param2": "C001087|C001088|C001090|C001091", 
                                "param1": "80"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t"
                            }
                        ], 
                        "EID": [
                            44
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "40"
                            }
                        ], 
                        "id": 44
                    }, 
                    {
                        "comment": "语音喊完进入战斗", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction39", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction80", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            45
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "45", 
                                "param1": "t"
                            }
                        ], 
                        "id": 45
                    }
                ], 
                "eventsAI": {
                    24: [
                        {
                            "comment": "语音结束进入战斗", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction39", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2"
                                }, 
                                {
                                    "script": "AIAction80", 
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
                                    "script": "AICondition84", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "C001091"
                                }
                            ], 
                            "id": 47
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
    "FSM": 2, 
    "dead": {
        "subStateDatas": {
            1: {
                "name": "通用死亡状态", 
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
                                "param2": "C001092", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            5
                        ], 
                        "Conditions": [], 
                        "id": 5
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
                "name": "通用战斗状态1", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "3S换仇恨", 
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
                        "id": 3
                    }, 
                    {
                        "comment": "超过10米使用冲锋", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "100094001"
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
                                "param1": "10"
                            }, 
                            {
                                "script": "AICondition10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "100094001"
                            }
                        ], 
                        "id": 18
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
                                "param1": "110005001"
                            }
                        ], 
                        "EID": [
                            17
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "110005001"
                            }
                        ], 
                        "id": 17
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
                                "param1": "kaishi"
                            }
                        ], 
                        "EID": [
                            6
                        ], 
                        "Conditions": [], 
                        "id": 6
                    }, 
                    {
                        "comment": "玩法计时", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "kaishi1"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "31|32|33|34|35|36|37|38|39"
                            }
                        ], 
                        "EID": [
                            30
                        ], 
                        "Conditions": [], 
                        "id": 30
                    }, 
                    {
                        "comment": "5s召唤烈焰球1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20612 -4631 4500", 
                                "param1": "20004118"
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
                                "param2": "5", 
                                "param1": "kaishi1"
                            }
                        ], 
                        "id": 31
                    }, 
                    {
                        "comment": "15s召唤烈焰球24", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "19695 -5688 4500", 
                                "param1": "20004119"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "21448 -6473 4500", 
                                "param1": "20004507"
                            }
                        ], 
                        "EID": [
                            32
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "15", 
                                "param1": "kaishi1"
                            }
                        ], 
                        "id": 32
                    }, 
                    {
                        "comment": "20s召唤加血能量球11", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "21845 -5218 4500", 
                                "param1": "20004509"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20612 -4631 4500", 
                                "param1": "20004118"
                            }
                        ], 
                        "EID": [
                            36
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20", 
                                "param1": "kaishi1"
                            }
                        ], 
                        "id": 36
                    }, 
                    {
                        "comment": "25s召唤烈焰球35", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20697 -5970 4500", 
                                "param1": "20004120"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20098 -7155 4500", 
                                "param1": "20004508"
                            }
                        ], 
                        "EID": [
                            33
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "25", 
                                "param1": "kaishi1"
                            }
                        ], 
                        "id": 33
                    }, 
                    {
                        "comment": "35s召唤烈焰球42", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "21448 -6473 4500", 
                                "param1": "20004507"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "19695 -5688 4500", 
                                "param1": "20004119"
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
                                "param2": "35", 
                                "param1": "kaishi1"
                            }
                        ], 
                        "id": 34
                    }, 
                    {
                        "comment": "40s召唤加血能量球213", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "19408 -6660 4500", 
                                "param1": "20004510"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20612 -4631 4500", 
                                "param1": "20004118"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20697 -5970 4500", 
                                "param1": "20004120"
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
                                "param2": "40", 
                                "param1": "kaishi1"
                            }
                        ], 
                        "id": 37
                    }, 
                    {
                        "comment": "40s释放大音希声", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "121328001"
                            }
                        ], 
                        "EID": [
                            39
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "40", 
                                "param1": "kaishi1"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "121328001"
                            }
                        ], 
                        "id": 39
                    }, 
                    {
                        "comment": "50s召唤烈焰球5", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20098 -7155 4500", 
                                "param1": "20004508"
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
                                "param2": "50", 
                                "param1": "kaishi1"
                            }
                        ], 
                        "id": 35
                    }, 
                    {
                        "comment": "60s召唤加血能量球342", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "21447 -7146 4500", 
                                "param1": "20004511"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "21448 -6473 4500", 
                                "param1": "20004507"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "19695 -5688 4500", 
                                "param1": "20004119"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "kaishi1"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "30"
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
                                "param1": "kaishi1"
                            }
                        ], 
                        "id": 38
                    }, 
                    {
                        "comment": "琴风禁法，离弦破军！", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "K000097", 
                                "param1": "50"
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
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 24
                    }, 
                    {
                        "comment": "琴风禁法，天音震魂！", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "K000098", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            25
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "40", 
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 25
                    }, 
                    {
                        "comment": "琴风禁法，五律天征！", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "K000099", 
                                "param1": "50"
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
                                "param2": "60", 
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 26
                    }, 
                    {
                        "comment": "技能打击", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction42", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "121324001|121325001|121326001|121327001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 15
                    }, 
                    {
                        "comment": "绿球喊话提醒", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C002000", 
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
                                "param2": "20", 
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 48
                    }, 
                    {
                        "comment": "大招喊话提醒", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C001998", 
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
                                "param2": "35", 
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 49
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
                            "id": 4
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
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "pead": {
        "subStateDatas": {
            1: {
                "name": "准备", 
                "tickTimer": 0.5, 
                "statesAI": [
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
                        "id": 42
                    }, 
                    {
                        "comment": "进入表演状态", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction61", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 43
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