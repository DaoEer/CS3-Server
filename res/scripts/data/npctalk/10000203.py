# -*- coding: utf-8 -*-
Datas = {
    "10000203": {
        "talks": [
            {
                "msg": "@S{4}您好，我是水楚楚。我可以带您前往轮回秘境抓捕各式各样的幻兽。此秘境乃是昔年鸿钧与罗睺以阴阳二气论道之地，幻兽便是在他们的阴阳二气碰撞下孕育而生。@B@B@S{4}当然除了幻兽，秘境中还衍生了诸多仙草灵药，甚至还有打造稀有绿装的天材地宝。", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "chuansong1", 
                        "title": "传送进入轮回秘境"
                    }, 
                    {
                        "type": 0, 
                        "key": "renwu", 
                        "title": "奇缘任务：轮回秘境"
                    }, 
                    {
                        "type": 0, 
                        "key": "dongfu", 
                        "title": "返回洞府"
                    }, 
                    {
                        "type": 0, 
                        "key": "dongfu1", 
                        "title": "返回洞府"
                    }
                ], 
                "functions": [], 
                "key": "Talk", 
                "visibles": []
            }, 
            {
                "msg": "", 
                "keys": [], 
                "functions": [
                    {
                        "expenditures": [], 
                        "conditions": [
                            {
                                "key": "TCLevel", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "30"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 33", 
                                "param2": "-40680.000000 26470.000000 266.766602", 
                                "param1": "L_LHMJ_1"
                            }
                        ]
                    }
                ], 
                "key": "chuansong1", 
                "visibles": [
                    {
                        "key": "TVLevel", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "30"
                    }
                ]
            }, 
            {
                "msg": "", 
                "keys": [], 
                "functions": [
                    {
                        "expenditures": [], 
                        "conditions": [], 
                        "actions": [
                            {
                                "key": "TAAcceptQiYuanQuest", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "71100003"
                            }, 
                            {
                                "key": "TAClose", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ]
                    }
                ], 
                "key": "renwu", 
                "visibles": [
                    {
                        "key": "TVLevel", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "30"
                    }, 
                    {
                        "key": "TVQiYuanQuestStatus", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "71100003"
                    }
                ]
            }, 
            {
                "msg": "", 
                "keys": [], 
                "functions": [
                    {
                        "expenditures": [], 
                        "conditions": [], 
                        "actions": [
                            {
                                "key": "TAEnterDongFuSpace", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "L_LHMJDF"
                            }
                        ]
                    }
                ], 
                "key": "dongfu", 
                "visibles": [
                    {
                        "key": "TVPlayerOccupySpaceType", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "1", 
                        "param1": "1"
                    }
                ]
            }, 
            {
                "msg": "", 
                "keys": [], 
                "functions": [
                    {
                        "expenditures": [], 
                        "conditions": [], 
                        "actions": [
                            {
                                "key": "TAEnterDongFuSpace", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "L_LHMJDF2"
                            }
                        ]
                    }
                ], 
                "key": "dongfu1", 
                "visibles": [
                    {
                        "key": "TVPlayerOccupySpaceType", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "1", 
                        "param1": "3"
                    }
                ]
            }
        ], 
        "npcID": "10000203"
    }
}