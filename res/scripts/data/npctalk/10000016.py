# -*- coding: utf-8 -*-
Datas = {
    "10000016": {
        "talks": [
            {
                "msg": "Q017227", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "CS_FMC", 
                        "title": "前往凤鸣城"
                    }, 
                    {
                        "type": 0, 
                        "key": "CS_BQDB", 
                        "title": "前往阪泉东部"
                    }, 
                    {
                        "type": 0, 
                        "key": "CS_FYP", 
                        "title": "前往飞云坡"
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
                        "expenditures": [
                            {
                                "key": "TEMoney", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "300"
                            }
                        ], 
                        "conditions": [], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -90", 
                                "param2": "23614.0 21573.0 12230.0", 
                                "param1": "L_FMC"
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
                "key": "CS_FMC", 
                "visibles": []
            }, 
            {
                "msg": "", 
                "keys": [], 
                "functions": [
                    {
                        "expenditures": [
                            {
                                "key": "TEMoney", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "200"
                            }
                        ], 
                        "conditions": [], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 0", 
                                "param2": "52052.0 54891.0 1363.0", 
                                "param1": "L_BQDB"
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
                "key": "CS_BQDB", 
                "visibles": []
            }, 
            {
                "msg": "", 
                "keys": [], 
                "functions": [
                    {
                        "expenditures": [
                            {
                                "key": "TEMoney", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "400"
                            }
                        ], 
                        "conditions": [
                            {
                                "key": "TCLevel", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "35"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -5", 
                                "param2": "-28893.0 -51043.0 1861.0", 
                                "param1": "L_FYP"
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
                "key": "CS_FYP", 
                "visibles": [
                    {
                        "key": "TVLevel", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "35"
                    }
                ]
            }
        ], 
        "npcID": "10000016"
    }
}