# -*- coding: utf-8 -*-
Datas = {
    "10000270": {
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
                        "key": "CS_YZD", 
                        "title": "前往瑶泽岛"
                    }, 
                    {
                        "type": 0, 
                        "key": "CS_BQDB", 
                        "title": "前往阪泉东部"
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
                                "param1": "200"
                            }
                        ], 
                        "conditions": [], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -86", 
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
                                "param1": "100"
                            }
                        ], 
                        "conditions": [], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 0", 
                                "param2": "21230 -25570 1770.0", 
                                "param1": "L_YZD"
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
                "key": "CS_YZD", 
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
            }
        ], 
        "npcID": "10000270"
    }
}