# -*- coding: utf-8 -*-
Datas = {
    "10001113": {
        "talks": [
            {
                "msg": "Q017227", 
                "keys": [
                    {
                        "type": 0, 
                        "key": "CS_JFT", 
                        "title": "前往接风台"
                    }, 
                    {
                        "type": 0, 
                        "key": "CS_XGDC", 
                        "title": "前往玄古道场"
                    }, 
                    {
                        "type": 0, 
                        "key": "CS_ZWF", 
                        "title": "前往坐忘峰"
                    }, 
                    {
                        "type": 0, 
                        "key": "CS_XLD", 
                        "title": "前往修罗殿"
                    }, 
                    {
                        "type": 0, 
                        "key": "CS_XYM", 
                        "title": "前往逍遥门"
                    }, 
                    {
                        "type": 0, 
                        "key": "CS_PMG", 
                        "title": "前往缥缈阁"
                    }, 
                    {
                        "type": 0, 
                        "key": "CS_MHD", 
                        "title": "前往摩诃殿"
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
                                "param1": "L_HDDT"
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
                "key": "CS_JFT", 
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
                                "param1": "20101550:2;4"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -90", 
                                "param2": "-7020.999999999999 -19793.0 17606.0", 
                                "param1": "L_HDDT"
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
                "key": "CS_ZWF", 
                "visibles": [
                    {
                        "key": "TVQuestStatus", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "20101550:2;4"
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
                                "param1": "20101545:2;4|20101546:2;4|20101547:2;4|20101548:2;4"
                            }
                        ], 
                        "actions": [
                            {
                                "key": "TATeleport", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 -90", 
                                "param2": "29580.0 -28647.000000000004 13713.0", 
                                "param1": "L_HDDT"
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
                "key": "CS_XGDC", 
                "visibles": [
                    {
                        "key": "TVQuestStatus", 
                        "param5": "", 
                        "param4": "", 
                        "param3": "", 
                        "param2": "", 
                        "param1": "20101545:2;4|20101546:2;4|20101547:2;4|20101548:2;4"
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
                                "param3": "0 0 -130.0", 
                                "param2": "2745.5 -12521.3 2273.1", 
                                "param1": "L_XLD_01"
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
                "key": "CS_XLD", 
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
                                "param3": "0 0 92", 
                                "param2": "52020.0 -12280.0 15965.2", 
                                "param1": "L_XYM"
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
                "key": "CS_XYM", 
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
                                "param3": "0 0 -175", 
                                "param2": "-9569 -5600 2198.8", 
                                "param1": "L_PMG"
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
                "key": "CS_PMG", 
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
                                "param3": "0 0 90", 
                                "param2": "52252 -5819 16134", 
                                "param1": "L_MHD"
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
                "key": "CS_MHD", 
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
        "npcID": "10001113"
    }
}