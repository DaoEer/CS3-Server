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
                "name": "工作状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "2名玩家从左边道路发起进攻，其他道路玩家人数不足以触发增援", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1016", 
                                "param3": "5", 
                                "param2": "20012586|20012585", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB2"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB2"
                            }, 
                            {
                                "script": "AICondition28", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZJ2|ZJ3|YB2|YB3"
                            }
                        ], 
                        "id": 17
                    }, 
                    {
                        "comment": "2名玩家从左边道路发起进攻，2名玩家从中路进攻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1016", 
                                "param3": "5", 
                                "param2": "20012586|20012585", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1017", 
                                "param3": "5", 
                                "param2": "20012584|20012587|20012588", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB2|ZJ2"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB2|ZJ2"
                            }
                        ], 
                        "id": 18
                    }, 
                    {
                        "comment": "2名玩家从左边道路发起进攻，3名玩家从中路进攻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1016", 
                                "param3": "5", 
                                "param2": "20012586|20012585", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1017", 
                                "param3": "5", 
                                "param2": "20012584|20012587|20012588", 
                                "param1": "3"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB2|ZJ3"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB2|ZJ3"
                            }
                        ], 
                        "id": 19
                    }, 
                    {
                        "comment": "2名玩家从左边道路发起进攻，2名玩家从右路进攻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1016", 
                                "param3": "5", 
                                "param2": "20012586|20012585", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1018", 
                                "param3": "5", 
                                "param2": "20012584|20012587|20012588", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB2|YB2"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB2|YB2"
                            }
                        ], 
                        "id": 20
                    }, 
                    {
                        "comment": "3名玩家从左边道路发起进攻，其他道路玩家人数不足以触发增援", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1016", 
                                "param3": "5", 
                                "param2": "20012584|20012586|20012585", 
                                "param1": "3"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB3"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB3"
                            }, 
                            {
                                "script": "AICondition28", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZJ2|YB2"
                            }
                        ], 
                        "id": 21
                    }, 
                    {
                        "comment": "3名玩家从左边道路发起进攻，2名玩家从中路进攻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1016", 
                                "param3": "5", 
                                "param2": "20012584|20012586|20012585", 
                                "param1": "3"
                            }, 
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1017", 
                                "param3": "5", 
                                "param2": "20012587|20012588", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB3|ZJ2"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB3|ZJ2"
                            }
                        ], 
                        "id": 22
                    }, 
                    {
                        "comment": "3名玩家从左边道路发起进攻，2名玩家从右路进攻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1016", 
                                "param3": "5", 
                                "param2": "20012584|20012586|20012585", 
                                "param1": "3"
                            }, 
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1018", 
                                "param3": "5", 
                                "param2": "20012587|20012588", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB3|YB2"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB3|YB2"
                            }
                        ], 
                        "id": 23
                    }, 
                    {
                        "comment": "4名玩家从左边道路发起进攻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1016", 
                                "param3": "5", 
                                "param2": "20012584|20012586|20012585|20012587|20012588", 
                                "param1": "4"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB4"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB4"
                            }
                        ], 
                        "id": 24
                    }, 
                    {
                        "comment": "5名玩家从左边道路发起进攻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1016", 
                                "param3": "5", 
                                "param2": "20012584|20012586|20012585|20012587|20012588", 
                                "param1": "5"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB5"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB5"
                            }
                        ], 
                        "id": 25
                    }, 
                    {
                        "comment": "2名玩家从中间道路发起进攻，其他道路玩家人数不足以触发增援", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1017", 
                                "param3": "5", 
                                "param2": "20012584|20012587|20012588", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZJ2"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZJ2"
                            }, 
                            {
                                "script": "AICondition28", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB2|ZB3|YB2|YB3"
                            }
                        ], 
                        "id": 26
                    }, 
                    {
                        "comment": "2名玩家从中间道路发起进攻，2名玩家从右边道路进攻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1017", 
                                "param3": "5", 
                                "param2": "20012584|20012585", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1018", 
                                "param3": "5", 
                                "param2": "20012587|20012588", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZJ2|YB2"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZJ2|YB2"
                            }
                        ], 
                        "id": 27
                    }, 
                    {
                        "comment": "2名玩家从中间道路发起进攻，3名玩家从右边道路进攻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1017", 
                                "param3": "5", 
                                "param2": "20012586|20012585", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1018", 
                                "param3": "5", 
                                "param2": "20012584|20012587|20012588", 
                                "param1": "3"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZJ2|YB3"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZJ2|YB3"
                            }
                        ], 
                        "id": 28
                    }, 
                    {
                        "comment": "3名玩家从中间道路发起进攻，", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1017", 
                                "param3": "5", 
                                "param2": "20012586|20012587|20012588", 
                                "param1": "3"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZJ3"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZJ3"
                            }, 
                            {
                                "script": "AICondition28", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB2|YB2"
                            }
                        ], 
                        "id": 29
                    }, 
                    {
                        "comment": "3名玩家从中间道路发起进攻，2名玩家从右边道路发起进攻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1017", 
                                "param3": "5", 
                                "param2": "20012584|20012585|20012586", 
                                "param1": "3"
                            }, 
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1018", 
                                "param3": "5", 
                                "param2": "20012587|20012588", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZJ3|YB2"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZJ3|YB2"
                            }
                        ], 
                        "id": 30
                    }, 
                    {
                        "comment": "4名玩家从中间道路发起进攻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1017", 
                                "param3": "5", 
                                "param2": "20012584|20012586|20012585|20012587|20012588", 
                                "param1": "4"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZJ4"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZJ4"
                            }
                        ], 
                        "id": 31
                    }, 
                    {
                        "comment": "5名玩家从中间道路发起进攻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1017", 
                                "param3": "5", 
                                "param2": "20012584|20012586|20012585|20012587|20012588", 
                                "param1": "5"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZJ5"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZJ5"
                            }
                        ], 
                        "id": 32
                    }, 
                    {
                        "comment": "4名玩家从右边道路发起进攻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1018", 
                                "param3": "5", 
                                "param2": "20012584|20012586|20012585|20012587|20012588", 
                                "param1": "4"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "YB4"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "YB4"
                            }
                        ], 
                        "id": 33
                    }, 
                    {
                        "comment": "5名玩家从右边道路发起进攻", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction288", 
                                "param5": "", 
                                "param4": "1018", 
                                "param3": "5", 
                                "param2": "20012584|20012586|20012585|20012587|20012588", 
                                "param1": "5"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "YB5"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "YB5"
                            }
                        ], 
                        "id": 34
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到1021设置 ZB1 标记，清除其他人数标记", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction56", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZB0|ZB1|ZB2|ZB3|ZB4|ZB5"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZB1"
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
                                    "param1": "1021"
                                }
                            ], 
                            "id": 2
                        }, 
                        {
                            "comment": "收到1022设置 ZB2 标记，清除其他人数标记", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction56", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZB0|ZB1|ZB2|ZB3|ZB4|ZB5"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZB2"
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
                                    "param1": "1022"
                                }
                            ], 
                            "id": 3
                        }, 
                        {
                            "comment": "收到1023设置 ZB3 标记，清除其他人数标记", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction56", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZB0|ZB1|ZB2|ZB3|ZB4|ZB5"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZB3"
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
                                    "param1": "1023"
                                }
                            ], 
                            "id": 4
                        }, 
                        {
                            "comment": "收到1024设置 ZB4 标记，清除其他人数标记", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction56", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZB0|ZB1|ZB2|ZB3|ZB4|ZB5"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZB4"
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
                                    "param1": "1024"
                                }
                            ], 
                            "id": 5
                        }, 
                        {
                            "comment": "收到1025设置 ZB5 标记，清除其他人数标记", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction56", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZB0|ZB1|ZB2|ZB3|ZB4|ZB5"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZB5"
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
                                    "param1": "1025"
                                }
                            ], 
                            "id": 6
                        }, 
                        {
                            "comment": "收到1031设置 ZJ1 标记，清除其他人数标记", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction56", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZJ0|ZJ1|ZJ2|ZJ3|ZJ4|ZJ5"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZJ1"
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
                                    "param1": "1031"
                                }
                            ], 
                            "id": 7
                        }, 
                        {
                            "comment": "收到1032设置 ZJ2 标记，清除其他人数标记", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction56", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZJ0|ZJ1|ZJ2|ZJ3|ZJ4|ZJ5"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZJ2"
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
                                    "param1": "1032"
                                }
                            ], 
                            "id": 8
                        }, 
                        {
                            "comment": "收到1033设置 ZJ3 标记，清除其他人数标记", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction56", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZJ0|ZJ1|ZJ2|ZJ3|ZJ4|ZJ5"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZJ3"
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
                                    "param1": "1033"
                                }
                            ], 
                            "id": 9
                        }, 
                        {
                            "comment": "收到1034设置 ZJ4 标记，清除其他人数标记", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction56", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZJ0|ZJ1|ZJ2|ZJ3|ZJ4|ZJ5"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZJ4"
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
                                    "param1": "1034"
                                }
                            ], 
                            "id": 10
                        }, 
                        {
                            "comment": "收到1035设置 ZJ5 标记，清除其他人数标记", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction56", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZJ0|ZJ1|ZJ2|ZJ3|ZJ4|ZJ5"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "ZJ5"
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
                                    "param1": "1035"
                                }
                            ], 
                            "id": 11
                        }, 
                        {
                            "comment": "收到1041设置 YB1 标记，清除其他人数标记", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction56", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "YB0|YB1|YB2|YB3|YB4|YB5"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "YB1"
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
                                    "param1": "1041"
                                }
                            ], 
                            "id": 12
                        }, 
                        {
                            "comment": "收到1042设置 YB2 标记，清除其他人数标记", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction56", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "YB0|YB1|YB2|YB3|YB4|YB5"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "YB2"
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
                                    "param1": "1042"
                                }
                            ], 
                            "id": 13
                        }, 
                        {
                            "comment": "收到1043设置 YB3 标记，清除其他人数标记", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction56", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "YB0|YB1|YB2|YB3|YB4|YB5"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "YB3"
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
                                    "param1": "1043"
                                }
                            ], 
                            "id": 14
                        }, 
                        {
                            "comment": "收到1044设置 YB4 标记，清除其他人数标记", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction56", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "YB0|YB1|YB2|YB3|YB4|YB5"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "YB4"
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
                                    "param1": "1044"
                                }
                            ], 
                            "id": 15
                        }, 
                        {
                            "comment": "收到1045设置 YB5 标记，清除其他人数标记", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction56", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "YB0|YB1|YB2|YB3|YB4|YB5"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "YB5"
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
                                    "param1": "1045"
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
    "pead": {
        "subStateDatas": {
            1: {
                "name": "准备阶段", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "记录ZB0 ZJ0 YB0标签", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction55", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "ZB0|ZJ0|YB0"
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