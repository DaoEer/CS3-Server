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
                        "comment": "", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Q022155", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            37
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition37", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "Role", 
                                "param2": "12345607", 
                                "param1": "50"
                            }
                        ], 
                        "id": 37
                    }
                ], 
                "eventsAI": {
                    24: [
                        {
                            "comment": "", 
                            "odds": 1.0, 
                            "Actions": [
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
                                    "param1": "Q022155"
                                }
                            ], 
                            "id": 38
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
        "subStateDatas": {
            2: {
                "name": "通用战斗状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "gw2324技能随机", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction67", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "100319001|100320001|100321001|100322001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 9
                    }, 
                    {
                        "comment": "", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction22", 
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
                                "param1": "21"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 35
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
    "free": {
        "subStateDatas": {
            2: {
                "name": "巡逻路线", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "到达第一个位置", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Q022156", 
                                "param1": "50"
                            }, 
                            {
                                "script": "AIAction24", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction70", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "0.967|1|1", 
                                "param1": "Show_11|Show_12|Show_13"
                            }, 
                            {
                                "script": "AIAction55", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "diyi"
                            }
                        ], 
                        "EID": [
                            19
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition72", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "74", 
                                "param1": "4"
                            }
                        ], 
                        "id": 19
                    }, 
                    {
                        "comment": "到达第二个位置", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Q022157", 
                                "param1": "50"
                            }, 
                            {
                                "script": "AIAction24", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction70", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "0.967|1|1", 
                                "param1": "Show_11|Show_12|Show_13"
                            }, 
                            {
                                "script": "AIAction55", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "dier"
                            }
                        ], 
                        "EID": [
                            22
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition72", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "99", 
                                "param1": "4"
                            }
                        ], 
                        "id": 22
                    }, 
                    {
                        "comment": "15米范围内没有玩家，停止巡逻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction24", 
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
                                "param1": "21"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition22", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "15"
                            }
                        ], 
                        "id": 20
                    }, 
                    {
                        "comment": "重新巡逻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction145", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction41", 
                                "param5": "", 
                                "param4": "5", 
                                "param3": "", 
                                "param2": "0", 
                                "param1": "4"
                            }
                        ], 
                        "EID": [
                            21
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Role", 
                                "param1": "15"
                            }, 
                            {
                                "script": "AICondition28", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "diyi|dier"
                            }
                        ], 
                        "id": 21
                    }, 
                    {
                        "comment": "到达位置，给副本发送通知", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "753"
                            }, 
                            {
                                "script": "AIAction32", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "5"
                            }
                        ], 
                        "EID": [
                            31
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "5", 
                                "param1": "69880.0 24630.0 -7350.0"
                            }
                        ], 
                        "id": 31
                    }, 
                    {
                        "comment": "设置当前为出生点", 
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
                        "id": 36
                    }, 
                    {
                        "comment": "到达第一个巡逻点，给怪物发送指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "64", 
                                "param2": "20011164", 
                                "param1": "80|80"
                            }
                        ], 
                        "EID": [
                            39
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition72", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "13", 
                                "param1": "4"
                            }
                        ], 
                        "id": 39
                    }, 
                    {
                        "comment": "到达第二个巡逻点，给怪物发送指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "68", 
                                "param2": "20011168", 
                                "param1": "80|80"
                            }
                        ], 
                        "EID": [
                            40
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition72", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "38", 
                                "param1": "4"
                            }
                        ], 
                        "id": 40
                    }, 
                    {
                        "comment": "到达第三个巡逻点，给怪物发送指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "69", 
                                "param2": "20011169", 
                                "param1": "80"
                            }
                        ], 
                        "EID": [
                            41
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition72", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "63", 
                                "param1": "4"
                            }
                        ], 
                        "id": 41
                    }, 
                    {
                        "comment": "到达第三个巡逻点，给怪物发送指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "71", 
                                "param2": "20011171", 
                                "param1": "80|80"
                            }
                        ], 
                        "EID": [
                            42
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition72", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "95", 
                                "param1": "4"
                            }
                        ], 
                        "id": 42
                    }
                ], 
                "eventsAI": {
                    24: [
                        {
                            "comment": "第一句话结束，手放下，继续巡逻", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction145", 
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
                                    "param1": "21"
                                }, 
                                {
                                    "script": "AIAction56", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "diyi"
                                }
                            ], 
                            "EID": [
                                28
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition84", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "Q022156"
                                }
                            ], 
                            "id": 28
                        }, 
                        {
                            "comment": "第二句话结束，手放下，继续巡逻", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction145", 
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
                                    "param1": "21"
                                }, 
                                {
                                    "script": "AIAction56", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "dier"
                                }
                            ], 
                            "EID": [
                                30
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition84", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "Q022157"
                                }
                            ], 
                            "id": 30
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
                        "comment": "", 
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
                        "EID": [
                            32
                        ], 
                        "Conditions": [], 
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
    }
}