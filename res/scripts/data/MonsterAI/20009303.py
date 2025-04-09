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
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "free": {
        "subStateDatas": {
            1: {
                "name": "自由状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "每隔15s,当前场景不存在石妖，随机从四个角落刷出一只怪物", 
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
                                "param1": "tt"
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
                                "script": "AICondition29", 
                                "param5": "1", 
                                "param4": "1", 
                                "param3": "20009302", 
                                "param2": "Monster", 
                                "param1": "150"
                            }
                        ], 
                        "id": 2
                    }, 
                    {
                        "comment": "第一次刷出小怪喊话：有石妖前来抢夺琉璃，可等候石妖采集完毕，截取它们的收获。", 
                        "odds": 0.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Cy000434", 
                                "param1": "150"
                            }
                        ], 
                        "EID": [
                            3
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "talk"
                            }
                        ], 
                        "id": 3
                    }, 
                    {
                        "comment": "玩家被水晶球砸到，触发界面提示", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Cy000432", 
                                "param1": "100"
                            }
                        ], 
                        "EID": [
                            4
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition36", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "Role", 
                                "param2": "14013301", 
                                "param1": "100"
                            }
                        ], 
                        "id": 4
                    }, 
                    {
                        "comment": "玩家被灵晶砸中，触发界面提示", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Cy000433", 
                                "param1": "100"
                            }
                        ], 
                        "EID": [
                            5
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition36", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "Role", 
                                "param2": "14013501", 
                                "param1": "100"
                            }
                        ], 
                        "id": 5
                    }, 
                    {
                        "comment": "延时3s,当前场景不存在石妖，随机从四个角落刷出一只怪物", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction130", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20009302", 
                                "param2": "0.0 0.0 -95.6|0.0 0.0 -13.1|0.0 0.0 23.4|0.0 0.0 160.4", 
                                "param1": "5791.0 -1394.0 244.0|-3690.9 -575.0 244.0|-3697.9 -8565.0 244.0|3235.0 -8269.0 244.0"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "tt"
                            }, 
                            {
                                "script": "AIAction17", 
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
                                "param2": "3", 
                                "param1": "tt"
                            }, 
                            {
                                "script": "AICondition29", 
                                "param5": "1", 
                                "param4": "1", 
                                "param3": "20009302", 
                                "param2": "Monster", 
                                "param1": "150"
                            }
                        ], 
                        "id": 6
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到副本通知，开始计时t1", 
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
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "talk"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "901", 
                                    "param1": ""
                                }
                            ], 
                            "id": 1
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