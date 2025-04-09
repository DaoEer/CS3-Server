# -*- coding: utf-8 -*-
Datas = {
    "reset": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "show": {
        "subStateDatas": {
            1: {
                "name": "初始状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "将分身2作为AI目标", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction5", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20011734", 
                                "param2": "Monster", 
                                "param1": "20"
                            }
                        ], 
                        "EID": [
                            5
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20011734", 
                                "param2": "Monster", 
                                "param1": "20"
                            }
                        ], 
                        "id": 5
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到fenshen，添加分身预警buff/添加自身连线母Buff", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction75", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "11060801"
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
                                    "param1": "fenshen"
                                }
                            ], 
                            "id": 3
                        }, 
                        {
                            "comment": "收到1，与AI目标连线", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction76", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "11060802"
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
                                    "param1": "1"
                                }
                            ], 
                            "id": 6
                        }, 
                        {
                            "comment": "收到2，开启巡逻", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction41", 
                                    "param5": "", 
                                    "param4": "4", 
                                    "param3": "", 
                                    "param2": "0", 
                                    "param1": "1"
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
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2"
                                }
                            ], 
                            "id": 4
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            2: {
                "name": "第一次", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "星石火球buff被去除，自我销毁/通知副本", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction38", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction32", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "true2"
                            }
                        ], 
                        "EID": [
                            8
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition15", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "11060702|11060704|11060705"
                            }
                        ], 
                        "id": 8
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到second2，开启第二次巡逻", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction41", 
                                    "param5": "", 
                                    "param4": "4", 
                                    "param3": "", 
                                    "param2": "0", 
                                    "param1": "1"
                                }, 
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "15|13|22|23"
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
                                9
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "second2"
                                }
                            ], 
                            "id": 9
                        }, 
                        {
                            "comment": "收到stop，暂停巡逻/变色", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction75", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "11060705"
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
                                    "script": "AIAction43", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "11060702"
                                }
                            ], 
                            "EID": [
                                18
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "stop"
                                }
                            ], 
                            "id": 18
                        }, 
                        {
                            "comment": "开启连线", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction76", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "11060802"
                                }
                            ], 
                            "EID": [
                                20
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "lianxian"
                                }
                            ], 
                            "id": 20
                        }, 
                        {
                            "comment": "收到chongzhi，再次巡逻/切3", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction41", 
                                    "param5": "", 
                                    "param4": "4", 
                                    "param3": "", 
                                    "param2": "0", 
                                    "param1": "1"
                                }, 
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "22|26"
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
                                24
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "chongzhi"
                                }
                            ], 
                            "id": 24
                        }
                    ]
                }, 
                "initiativeAreaXZ": "3", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 1
            }, 
            3: {
                "name": "第二次", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "星石火球buff被去除，自我销毁/通知副本", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction32", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "true2"
                            }
                        ], 
                        "EID": [
                            14
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition15", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "11060702|11060704|11060705"
                            }
                        ], 
                        "id": 14
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到second2，开启第三次巡逻", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction41", 
                                    "param5": "", 
                                    "param4": "4", 
                                    "param3": "", 
                                    "param2": "0", 
                                    "param1": "1"
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
                                11
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "second2"
                                }
                            ], 
                            "id": 11
                        }, 
                        {
                            "comment": "收到stop，暂停巡逻/变色", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction75", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "11060705"
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
                                    "script": "AIAction43", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "11060702"
                                }
                            ], 
                            "EID": [
                                19
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "stop"
                                }
                            ], 
                            "id": 19
                        }, 
                        {
                            "comment": "开启连线", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction76", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "11060802"
                                }
                            ], 
                            "EID": [
                                21
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "lianxian"
                                }
                            ], 
                            "id": 21
                        }, 
                        {
                            "comment": "收到chongzhi，再次巡逻/切4", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction41", 
                                    "param5": "", 
                                    "param4": "4", 
                                    "param3": "", 
                                    "param2": "0", 
                                    "param1": "1"
                                }, 
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "22|26"
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
                                25
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "chongzhi"
                                }
                            ], 
                            "id": 25
                        }
                    ]
                }, 
                "initiativeAreaXZ": "3", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 1
            }, 
            4: {
                "name": "第三次", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "星石火球buff被去除，自我销毁/通知副本", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction32", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "true2"
                            }
                        ], 
                        "EID": [
                            15
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition15", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "11060702|11060704|11060705"
                            }
                        ], 
                        "id": 15
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到second2，开启第三次巡逻/切回2", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction41", 
                                    "param5": "", 
                                    "param4": "4", 
                                    "param3": "", 
                                    "param2": "0", 
                                    "param1": "1"
                                }, 
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "8|9|18|20|14|11|19|21"
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
                            "EID": [
                                13
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "second2"
                                }
                            ], 
                            "id": 13
                        }, 
                        {
                            "comment": "收到stop，暂停巡逻/变色", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction75", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "11060705"
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
                                    "script": "AIAction43", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "11060702"
                                }
                            ], 
                            "EID": [
                                22
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "stop"
                                }
                            ], 
                            "id": 22
                        }, 
                        {
                            "comment": "开启连线", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction76", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "11060802"
                                }
                            ], 
                            "EID": [
                                23
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "lianxian"
                                }
                            ], 
                            "id": 23
                        }, 
                        {
                            "comment": "收到chongzhi，再次巡逻/切2", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction41", 
                                    "param5": "", 
                                    "param4": "4", 
                                    "param3": "", 
                                    "param2": "0", 
                                    "param1": "1"
                                }, 
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "18|19|20|21|24|25"
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
                            "EID": [
                                26
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition67", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "chongzhi"
                                }
                            ], 
                            "id": 26
                        }
                    ]
                }, 
                "initiativeAreaXZ": "3", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 1
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
        "subStateDatas": {
            1: {
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "", 
                        "odds": 1.0, 
                        "Actions": [], 
                        "EID": [], 
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
    }, 
    "pead": {
        "subStateDatas": {
            1: {
                "name": "", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "上星火/进表演", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "11060702"
                            }, 
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
                        "id": 2
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