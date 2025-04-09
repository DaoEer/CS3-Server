# -*- coding: utf-8 -*-
Datas = {
    "reset": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "show": {
        "subStateDatas": {
            1: {
                "name": "", 
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
                                "param1": "t1"
                            }
                        ], 
                        "EID": [
                            2
                        ], 
                        "Conditions": [], 
                        "id": 2
                    }, 
                    {
                        "comment": "随机切换子状态", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction84", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 3
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到BOSS指令销毁", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction32", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [
                                8
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "222", 
                                    "param1": "20008807"
                                }
                            ], 
                            "id": 8
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            2: {
                "name": "A组合", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "时间到达，召唤三陨石，两地刺", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20009472", 
                                "param4": "5", 
                                "param3": "0", 
                                "param2": "30", 
                                "param1": "-12750.0 19550.0 -12202.0"
                            }, 
                            {
                                "script": "AIAction48", 
                                "param5": "20009473", 
                                "param4": "4", 
                                "param3": "0", 
                                "param2": "15", 
                                "param1": "-12750.0 19550.0 -12202.0"
                            }, 
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
                            4
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "t1", 
                                "param2": "20", 
                                "param1": "10"
                            }
                        ], 
                        "id": 4
                    }, 
                    {
                        "comment": "时间到达，清除时间，清除EAI", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t1|t2"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2|4"
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
                                "param2": "3", 
                                "param1": "t2"
                            }
                        ], 
                        "id": 5
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到BOSS指令销毁", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction32", 
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
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "222", 
                                    "param1": "20008807"
                                }
                            ], 
                            "id": 9
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            3: {
                "name": "B组合", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "时间到达，召唤三陨石，两地刺", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20009473", 
                                "param4": "5", 
                                "param3": "0", 
                                "param2": "30", 
                                "param1": "-12750.0 19550.0 -12202.0"
                            }, 
                            {
                                "script": "AIAction48", 
                                "param5": "20009472", 
                                "param4": "4", 
                                "param3": "0", 
                                "param2": "15", 
                                "param1": "-12750.0 19550.0 -12202.0"
                            }, 
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
                            6
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "t1", 
                                "param2": "20", 
                                "param1": "10"
                            }
                        ], 
                        "id": 6
                    }, 
                    {
                        "comment": "时间到达，清除时间，清除EAI", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t1|t2"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2|6"
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
                                "param2": "3", 
                                "param1": "t2"
                            }
                        ], 
                        "id": 7
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到BOSS指令销毁", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction32", 
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
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "222", 
                                    "param1": "20008807"
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
            }, 
            4: {
                "name": "C组合-地刺", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "时间到达，地刺", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20009472", 
                                "param4": "8", 
                                "param3": "0", 
                                "param2": "20", 
                                "param1": "-12750.0 19550.0 -12202.0"
                            }, 
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
                        "Conditions": [
                            {
                                "script": "AICondition75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "t1", 
                                "param2": "20", 
                                "param1": "10"
                            }
                        ], 
                        "id": 11
                    }, 
                    {
                        "comment": "时间到达，清除时间，清除EAI", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t1|t2"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2|11"
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
                                "param2": "3", 
                                "param1": "t2"
                            }
                        ], 
                        "id": 12
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到BOSS指令销毁", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction32", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [
                                13
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "222", 
                                    "param1": "20008807"
                                }
                            ], 
                            "id": 13
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            5: {
                "name": "D组合-陨石", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "时间到达，地刺", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20009473", 
                                "param4": "8", 
                                "param3": "0", 
                                "param2": "20", 
                                "param1": "-12750.0 19550.0 -12202.0"
                            }, 
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
                            14
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "t1", 
                                "param2": "20", 
                                "param1": "10"
                            }
                        ], 
                        "id": 14
                    }, 
                    {
                        "comment": "时间到达，清除时间，清除EAI", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t1|t2"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2|14"
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
                                "param2": "3", 
                                "param1": "t2"
                            }
                        ], 
                        "id": 15
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到BOSS指令销毁", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction32", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [
                                16
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "222", 
                                    "param1": "20008807"
                                }
                            ], 
                            "id": 16
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
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "fight": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "free": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "pead": {
        "subStateDatas": {
            1: {
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "延迟进入表演", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction83", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "6", 
                                "param1": "1"
                            }
                        ], 
                        "EID": [
                            1
                        ], 
                        "Conditions": [], 
                        "id": 1
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