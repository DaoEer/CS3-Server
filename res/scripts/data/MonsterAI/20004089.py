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
                "name": "通用战斗状态", 
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
                        "comment": "商", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120592001"
                            }
                        ], 
                        "EID": [
                            32
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120592001"
                            }
                        ], 
                        "id": 32
                    }, 
                    {
                        "comment": "旁白喊话", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000215", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [
                            7
                        ], 
                        "Conditions": [], 
                        "id": 7
                    }, 
                    {
                        "comment": "进对商清除", 
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
                                "param1": "120597001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition36", 
                                "param5": "", 
                                "param4": "20004096", 
                                "param3": "Monster", 
                                "param2": "12027401", 
                                "param1": "3"
                            }
                        ], 
                        "id": 31
                    }, 
                    {
                        "comment": "进错宫加血", 
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
                                "param1": "120557001"
                            }, 
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000219", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition36", 
                                "param5": "", 
                                "param4": "20004096", 
                                "param3": "Monster", 
                                "param2": "12027301", 
                                "param1": "3"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120557001"
                            }
                        ], 
                        "id": 27
                    }, 
                    {
                        "comment": "进错角加血", 
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
                                "param1": "120557001"
                            }, 
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000219", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition36", 
                                "param5": "", 
                                "param4": "20004096", 
                                "param3": "Monster", 
                                "param2": "12027501", 
                                "param1": "3"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120557001"
                            }
                        ], 
                        "id": 28
                    }, 
                    {
                        "comment": "进错徵加血", 
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
                                "param1": "120557001"
                            }, 
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000219", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition36", 
                                "param5": "", 
                                "param4": "20004096", 
                                "param3": "Monster", 
                                "param2": "12027601", 
                                "param1": "3"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120557001"
                            }
                        ], 
                        "id": 29
                    }, 
                    {
                        "comment": "进错羽加血", 
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
                                "param1": "120557001"
                            }, 
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C000219", 
                                "param1": "50"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition36", 
                                "param5": "", 
                                "param4": "20004096", 
                                "param3": "Monster", 
                                "param2": "12027701", 
                                "param1": "3"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120557001"
                            }
                        ], 
                        "id": 30
                    }, 
                    {
                        "comment": "无影枪", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction42", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120538001|120539001|120540001|120541001"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 15
                    }, 
                    {
                        "comment": "左下角", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 175", 
                                "param2": "16432 -9069 3133", 
                                "param1": "20004114"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 175", 
                                "param2": "16455 -7885 3120", 
                                "param1": "20004115"
                            }
                        ], 
                        "EID": [
                            41
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
                                "script": "AICondition17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20", 
                                "param1": "16405 -8526 3220"
                            }
                        ], 
                        "id": 41
                    }, 
                    {
                        "comment": "右下角", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 175", 
                                "param2": "16340 -4145 3121", 
                                "param1": "20004114"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 175", 
                                "param2": "16340 -2730 3122", 
                                "param1": "20004115"
                            }
                        ], 
                        "EID": [
                            42
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
                                "script": "AICondition17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20", 
                                "param1": "16358 -3441 3221"
                            }
                        ], 
                        "id": 42
                    }, 
                    {
                        "comment": "右上角", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 175", 
                                "param2": "23475 -2485 3140", 
                                "param1": "20004114"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 175", 
                                "param2": "23460 -3630 3130", 
                                "param1": "20004115"
                            }
                        ], 
                        "EID": [
                            44
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
                                "script": "AICondition17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20", 
                                "param1": "23461 -3035 3240"
                            }
                        ], 
                        "id": 44
                    }, 
                    {
                        "comment": "左上角", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 175", 
                                "param2": "23385 -9505 3140", 
                                "param1": "20004114"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 175", 
                                "param2": "23370 -8485 3135", 
                                "param1": "20004115"
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
                                "param1": "50"
                            }, 
                            {
                                "script": "AICondition17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20", 
                                "param1": "23372 -8988 3233"
                            }
                        ], 
                        "id": 45
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
        "subStateDatas": {
            4: {
                "name": "商", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "商", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120592001"
                            }
                        ], 
                        "EID": [
                            25
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "120592001"
                            }
                        ], 
                        "id": 25
                    }, 
                    {
                        "comment": "设置朝向", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction26", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "0 0 176"
                            }
                        ], 
                        "EID": [
                            26
                        ], 
                        "Conditions": [], 
                        "id": 26
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