# -*- coding: utf-8 -*-
Datas = {
    "10001416": {
        "talks": [
            {
                "msg": "@S{4}勇士，我是汉嘉村接引人，该练兵场处于无主状态，但有大量流寇盘踞于此，若对该练兵场宣战则直接进入练兵场战斗！", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "DDT_ZD", 
                        "title": "练兵场信息"
                    }, 
                    {
                        "type": 0, 
                        "key": "DDT_XZ", 
                        "title": "练兵场信息（被宣战）"
                    }, 
                    {
                        "type": 0, 
                        "key": "DDT_LBRW", 
                        "title": "练兵场任务"
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
                        "conditions": [], 
                        "actions": [
                            {
                                "key": "TAOpenTrainSoldierGroundDetails", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ]
                    }
                ], 
                "key": "DDT_ZD", 
                "visibles": [
                    {
                        "key": "TVIsDeclareTrainGround", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "0"
                    }, 
                    {
                        "key": "TVOccupyTrainGround", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "0"
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
                                "key": "TCLbcTaskProcesses", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "5554"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TAOpenTrainSoldierGroundQuestDetails", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ]
                    }
                ], 
                "key": "DDT_LBRW", 
                "visibles": [
                    {
                        "key": "TVOccupyTrainGround", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": ""
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
                                "key": "TAOpenTrainSoldierGroundDetails", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ]
                    }
                ], 
                "key": "DDT_XZ", 
                "visibles": [
                    {
                        "key": "TVIsDeclareTrainGround", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "1"
                    }
                ]
            }
        ], 
        "npcID": "10001416"
    }
}