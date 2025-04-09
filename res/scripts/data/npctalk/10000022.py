# -*- coding: utf-8 -*-
Datas = {
    "10000022": {
        "talks": [
            {
                "msg": "Q017227", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "CS_YXT", 
                        "title": "前往迎仙台"
                    }, 
                    {
                        "type": 0, 
                        "key": "CS_TYDC", 
                        "title": "前往太寅道场"
                    }, 
                    {
                        "type": 0, 
                        "key": "CS_SJT", 
                        "title": "前往试剑台"
                    }, 
                    {
                        "type": 0, 
                        "key": "CS_KLZ", 
                        "title": "前往昆仑宗"
                    }, 
                    {
                        "type": 0, 
                        "key": "CS_YXG", 
                        "title": "前往玉虚宫"
                    }, 
                    {
                        "type": 0, 
                        "key": "CS_PLG", 
                        "title": "前往蓬莱阁"
                    }, 
                    {
                        "type": 0, 
                        "key": "CS_TQG", 
                        "title": "前往太清宫"
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
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -90", 
                                "param2": "-57680.0 -11840.0 12630.0", 
                                "param1": "L_PGDT"
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
                "key": "CS_YXT", 
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
                                "key": "TCQuestStatus", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "20101050:2;4"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -90", 
                                "param2": "-7020.999999999999 -19793.0 17606.0", 
                                "param1": "L_PGDT"
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
                "key": "CS_SJT", 
                "visibles": [
                    {
                        "key": "TVQuestStatus", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "20101050:2;4"
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
                                "key": "TCQuestStatus", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "20101045:2;4|20101046:2;4|20101047:2;4|20101048:2;4"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -90", 
                                "param2": "29580.0 -28647.000000000004 13713.0", 
                                "param1": "L_PGDT"
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
                "key": "CS_TYDC", 
                "visibles": [
                    {
                        "key": "TVQuestStatus", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "20101045:2;4|20101046:2;4|20101047:2;4|20101048:2;4"
                    }
                ]
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
                                "param1": "10"
                            }
                        ], 
                        "conditions": [
                            {
                                "key": "TCProfession", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "1"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 0", 
                                "param2": "-202838.0 -207003.0 19043.0", 
                                "param1": "L_KLZ_1"
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
                "key": "CS_KLZ", 
                "visibles": [
                    {
                        "key": "TVProfession", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "1"
                    }
                ]
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
                                "param1": "10"
                            }
                        ], 
                        "conditions": [
                            {
                                "key": "TCProfession", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 69.3", 
                                "param2": "4360 -25050 -314.521790", 
                                "param1": "L_YXG"
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
                "key": "CS_YXG", 
                "visibles": [
                    {
                        "key": "TVProfession", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "2"
                    }
                ]
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
                                "param1": "10"
                            }
                        ], 
                        "conditions": [
                            {
                                "key": "TCProfession", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "3"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -90", 
                                "param2": "-299080 -631800 55140", 
                                "param1": "L_PLG"
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
                "key": "CS_PLG", 
                "visibles": [
                    {
                        "key": "TVProfession", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "3"
                    }
                ]
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
                                "param1": "10"
                            }
                        ], 
                        "conditions": [
                            {
                                "key": "TCProfession", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "4"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -156", 
                                "param2": "2920.0 -12430.0 624.0", 
                                "param1": "L_TQG"
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
                "key": "CS_TQG", 
                "visibles": [
                    {
                        "key": "TVProfession", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "4"
                    }
                ]
            }
        ], 
        "npcID": "10000022"
    }
}