# -*- coding: utf-8 -*-
Datas = {
    "10000202": {
        "talks": [
            {
                "msg": "C002001|C002002|C002003", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "cs1", 
                        "title": "进入攻城战"
                    }, 
                    {
                        "type": 0, 
                        "key": "cs2", 
                        "title": "进入勇闯绝命岛（近战）"
                    }, 
                    {
                        "type": 0, 
                        "key": "cs3", 
                        "title": "进入勇闯绝命岛（远程）"
                    }, 
                    {
                        "type": 0, 
                        "key": "cs4", 
                        "title": "近战活动时间"
                    }, 
                    {
                        "type": 0, 
                        "key": "cs5", 
                        "title": "远程活动时间"
                    }
                ], 
                "functions": [
                    {
                        "expenditures": [], 
                        "conditions": [], 
                        "actions": []
                    }
                ], 
                "key": "Talk", 
                "visibles": []
            }, 
            {
                "msg": "攻城战移除行列", 
                "keys": [], 
                "functions": [
                    {
                        "expenditures": [], 
                        "conditions": [], 
                        "actions": [
                            {
                                "key": "TAEnterActivitySpaceCopy", 
                                "param5": "0 0 180", 
                                "param4": "680 31290 210", 
                                "param3": "fu_ben_L_GCZ", 
                                "param2": "14|1", 
                                "param1": "gongchengzhan|kaiqi"
                            }
                        ]
                    }
                ], 
                "key": "cs1", 
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
                        "key": "TVGlobalDataEqualValue", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "gongchengzhan|kaiqi"
                    }
                ]
            }, 
            {
                "msg": "", 
                "keys": [], 
                "functions": [
                    {
                        "expenditures": [], 
                        "conditions": [
                            {
                                "key": "TCIsMatchFastTeam", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TAEnterActivitySpaceCopy", 
                                "param5": "0 0 0", 
                                "param4": "30995 35694 3280", 
                                "param3": "fu_ben_L_YCJMD_tuanben", 
                                "param2": "13|1", 
                                "param1": "jinzhanchiji|kaiqi"
                            }
                        ]
                    }
                ], 
                "key": "cs2", 
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
                        "key": "TVGlobalDataEqualValue", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "jinzhanchiji|kaiqi"
                    }
                ]
            }, 
            {
                "msg": "", 
                "keys": [], 
                "functions": [
                    {
                        "expenditures": [], 
                        "conditions": [
                            {
                                "key": "TCIsMatchFastTeam", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TAEnterActivitySpaceCopy", 
                                "param5": "0 0 0", 
                                "param4": "30995 35694 3280", 
                                "param3": "fu_ben_L_YCJMD", 
                                "param2": "12|1", 
                                "param1": "yuanchengchiji|kaiqi"
                            }
                        ]
                    }
                ], 
                "key": "cs3", 
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
                        "key": "TVGlobalDataEqualValue", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "yuanchengchiji|kaiqi"
                    }
                ]
            }, 
            {
                "msg": "C002004", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "Talk", 
                        "title": "返回"
                    }
                ], 
                "functions": [], 
                "key": "cs4", 
                "visibles": []
            }, 
            {
                "msg": "C002009", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "Talk", 
                        "title": "返回"
                    }
                ], 
                "functions": [], 
                "key": "cs5", 
                "visibles": []
            }
        ], 
        "npcID": "10000202"
    }
}