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
                        "id": 49
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
                                "param2": "C000037", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            33
                        ], 
                        "Conditions": [], 
                        "id": 33
                    }, 
                    {
                        "comment": "死亡通知烈焰兽死亡", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "111", 
                                "param2": "20002016", 
                                "param1": "70"
                            }
                        ], 
                        "EID": [
                            42
                        ], 
                        "Conditions": [], 
                        "id": 42
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
                "name": "战斗状态", 
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
                            48
                        ], 
                        "Conditions": [], 
                        "id": 48
                    }, 
                    {
                        "comment": "开场霸体", 
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
                            26
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
                        "id": 26
                    }, 
                    {
                        "comment": "开战喊话", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000036", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            34
                        ], 
                        "Conditions": [], 
                        "id": 34
                    }, 
                    {
                        "comment": "战斗每隔3S，攻击伤害最高的目标", 
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
                        "id": 23
                    }, 
                    {
                        "comment": "距离大于12，冲锋", 
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
                                "param1": "12"
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
                        "id": 21
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
                                "param1": "120029001|120030001|120031001|120032001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 28
                    }, 
                    {
                        "comment": "计时time1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "time1"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 30
                    }, 
                    {
                        "comment": "每隔20秒使用击飞", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120033001"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "time1"
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
                                "param1": "time1"
                            }
                        ], 
                        "id": 31
                    }, 
                    {
                        "comment": "30秒后生命值低于50%召唤烈焰兽", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "0", 
                                "param3": "0 0 -45", 
                                "param2": "-8809 1177 516", 
                                "param1": "20002016"
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
                            }, 
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "30", 
                                "param1": "time"
                            }
                        ], 
                        "id": 32
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
                                "param1": "time"
                            }
                        ], 
                        "EID": [
                            35
                        ], 
                        "Conditions": [], 
                        "id": 35
                    }, 
                    {
                        "comment": "技能喊话1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "K000006", 
                                "param1": "50"
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
                                "param2": "15", 
                                "param1": "time"
                            }
                        ], 
                        "id": 36
                    }, 
                    {
                        "comment": "技能喊话2", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "K000007", 
                                "param1": "50"
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
                                "param2": "30", 
                                "param1": "time"
                            }
                        ], 
                        "id": 37
                    }, 
                    {
                        "comment": "技能喊话3", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "K000008", 
                                "param1": "50"
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
                                "param2": "45", 
                                "param1": "time"
                            }
                        ], 
                        "id": 38
                    }, 
                    {
                        "comment": "技能喊话4", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "K000009", 
                                "param1": "50"
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
                                "param2": "60", 
                                "param1": "time"
                            }
                        ], 
                        "id": 39
                    }, 
                    {
                        "comment": "技能喊话5", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "K000010", 
                                "param1": "50"
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
                                "param2": "75", 
                                "param1": "time"
                            }
                        ], 
                        "id": 40
                    }, 
                    {
                        "comment": "技能喊话6", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "K000011", 
                                "param1": "50"
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
                                "param2": "90", 
                                "param1": "time"
                            }
                        ], 
                        "id": 41
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
                            "id": 47
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
                        "comment": "重置销毁烈焰兽", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction94", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "70", 
                                "param2": "20002016", 
                                "param1": "Monster"
                            }
                        ], 
                        "EID": [
                            45
                        ], 
                        "Conditions": [], 
                        "id": 45
                    }, 
                    {
                        "comment": "朝向复位", 
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
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到3，取消血量保护", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction28", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "0"
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
                                    "param2": "3", 
                                    "param1": ""
                                }
                            ], 
                            "id": 29
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