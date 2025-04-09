# -*- coding: utf-8 -*-
Datas = {
    "reset": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "FSM": 1, 
    "dead": {
        "subStateDatas": {
            1: {
                "name": "清除法阵", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "清除法阵", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C001969", 
                                "param1": "79|20"
                            }, 
                            {
                                "script": "AIAction94", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "79", 
                                "param2": "20014652|20014653|20014654|20014655|20014658|20014659|20013440", 
                                "param1": "Monster"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 18
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
    "fight": {
        "subStateDatas": {
            1: {
                "name": "通用战斗状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "呼叫同伴", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction15", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            1
                        ], 
                        "Conditions": [], 
                        "id": 1
                    }, 
                    {
                        "comment": "每隔3秒，将伤害最高的目标设为攻击目标", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction8", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "3"
                            }
                        ], 
                        "id": 2
                    }, 
                    {
                        "comment": "距离玩家超过2米开始追击", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction73", 
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
                                "script": "AICondition23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
                            }
                        ], 
                        "id": 3
                    }, 
                    {
                        "comment": "霸体+召唤阴阳阵", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "10000001"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2213.0 7759.0 -552.0", 
                                "param1": "20014652"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "-1482.0 4060.0 -552.0", 
                                "param1": "20014653"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition15", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "10000001"
                            }
                        ], 
                        "id": 4
                    }, 
                    {
                        "comment": "距离玩家小于3米攻击或者远离", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction71", 
                                "param5": "20", 
                                "param4": "122307001|122308001|122309001", 
                                "param3": "2.5", 
                                "param2": "1", 
                                "param1": "0.9"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition24", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "3"
                            }
                        ], 
                        "id": 5
                    }, 
                    {
                        "comment": "genzong标记/时间t1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t1"
                            }
                        ], 
                        "EID": [
                            7
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "genzong"
                            }
                        ], 
                        "id": 7
                    }, 
                    {
                        "comment": "t1=20s跟踪怪", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "7"
                            }, 
                            {
                                "script": "AIAction48", 
                                "param5": "20014655", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "30", 
                                "param1": "364.0 5901.0 -400.1"
                            }, 
                            {
                                "script": "AIAction18", 
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
                                "param2": "20", 
                                "param1": "t1"
                            }, 
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "genzong"
                            }
                        ], 
                        "id": 8
                    }, 
                    {
                        "comment": "时间标记zhua", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "zhua"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 10
                    }, 
                    {
                        "comment": "清除BUFF", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction43", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12230701|12230702"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 17
                    }, 
                    {
                        "comment": "是否有genzong/50%概率冰爪", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction101", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0", 
                                "param2": "1", 
                                "param1": "122307014"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "zhua"
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
                                "param1": "genzong"
                            }, 
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "10", 
                                "param1": "zhua"
                            }
                        ], 
                        "id": 19
                    }, 
                    {
                        "comment": "是否有kuangbao/50%概率火爪", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction101", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0", 
                                "param2": "1", 
                                "param1": "122307015"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "zhua"
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
                                "param1": "kuangbao"
                            }, 
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "8", 
                                "param1": "zhua"
                            }
                        ], 
                        "id": 36
                    }, 
                    {
                        "comment": "发送20013440   1指令/播C001968", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "1", 
                                "param2": "20013440", 
                                "param1": "79|20"
                            }, 
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C001968", 
                                "param1": "79|20"
                            }
                        ], 
                        "EID": [
                            37
                        ], 
                        "Conditions": [], 
                        "id": 37
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到666变成中立", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction38", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2"
                                }
                            ], 
                            "EID": [
                                32
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "666", 
                                    "param1": ""
                                }
                            ], 
                            "id": 32
                        }
                    ], 
                    22: [
                        {
                            "comment": "开启光墙", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction135", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "5"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 31
                        }
                    ], 
                    5: [
                        {
                            "comment": "攻击下一个目标", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction13", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 6
                        }
                    ], 
                    6: [
                        {
                            "comment": "20%血跳4", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "4"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20"
                                }
                            ], 
                            "id": 20
                        }, 
                        {
                            "comment": "90%血genzong标记", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "genzong"
                                }
                            ], 
                            "EID": [
                                38
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "90"
                                }
                            ], 
                            "id": 38
                        }, 
                        {
                            "comment": "80%血50%概率“阳”", 
                            "odds": 0.5, 
                            "Actions": [
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "7"
                                }, 
                                {
                                    "script": "AIAction18", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t1"
                                }, 
                                {
                                    "script": "AIAction48", 
                                    "param5": "20014655", 
                                    "param4": "1", 
                                    "param3": "", 
                                    "param2": "50", 
                                    "param1": "364.0 5901.0 -472.1"
                                }, 
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2"
                                }, 
                                {
                                    "script": "AIAction10", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "1", 
                                    "param2": "20013440", 
                                    "param1": "79|20"
                                }, 
                                {
                                    "script": "AIAction94", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "79", 
                                    "param2": "20014655", 
                                    "param1": "Monster"
                                }
                            ], 
                            "EID": [
                                39, 
                                40
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "80"
                                }
                            ], 
                            "id": 39
                        }, 
                        {
                            "comment": "80%血50%概率“阴”", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "7"
                                }, 
                                {
                                    "script": "AIAction18", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t1"
                                }, 
                                {
                                    "script": "AIAction48", 
                                    "param5": "20014655", 
                                    "param4": "1", 
                                    "param3": "", 
                                    "param2": "50", 
                                    "param1": "364.0 5901.0 -472.1"
                                }, 
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "3"
                                }, 
                                {
                                    "script": "AIAction10", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "1", 
                                    "param2": "20013440", 
                                    "param1": "79|20"
                                }, 
                                {
                                    "script": "AIAction94", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "79", 
                                    "param2": "20014655", 
                                    "param1": "Monster"
                                }
                            ], 
                            "EID": [
                                39, 
                                40
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "80"
                                }
                            ], 
                            "id": 40
                        }, 
                        {
                            "comment": "60%血50%概率“阳”", 
                            "odds": 0.5, 
                            "Actions": [
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "7"
                                }, 
                                {
                                    "script": "AIAction18", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t1"
                                }, 
                                {
                                    "script": "AIAction48", 
                                    "param5": "20014655", 
                                    "param4": "1", 
                                    "param3": "", 
                                    "param2": "50", 
                                    "param1": "364.0 5901.0 -472.1"
                                }, 
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2"
                                }, 
                                {
                                    "script": "AIAction94", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "79", 
                                    "param2": "20014655", 
                                    "param1": "Monster"
                                }
                            ], 
                            "EID": [
                                47, 
                                48
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "60"
                                }
                            ], 
                            "id": 47
                        }, 
                        {
                            "comment": "60%血50%概率“阴”", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "7"
                                }, 
                                {
                                    "script": "AIAction18", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t1"
                                }, 
                                {
                                    "script": "AIAction48", 
                                    "param5": "20014655", 
                                    "param4": "1", 
                                    "param3": "", 
                                    "param2": "50", 
                                    "param1": "364.0 5901.0 -472.1"
                                }, 
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "3"
                                }, 
                                {
                                    "script": "AIAction94", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "79", 
                                    "param2": "20014655", 
                                    "param1": "Monster"
                                }
                            ], 
                            "EID": [
                                48, 
                                49
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "60"
                                }
                            ], 
                            "id": 48
                        }, 
                        {
                            "comment": "40%血50%概率“阳”/kuangbao", 
                            "odds": 0.5, 
                            "Actions": [
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "7"
                                }, 
                                {
                                    "script": "AIAction18", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t1"
                                }, 
                                {
                                    "script": "AIAction48", 
                                    "param5": "20014655", 
                                    "param4": "1", 
                                    "param3": "", 
                                    "param2": "50", 
                                    "param1": "364.0 5901.0 -472.1"
                                }, 
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2"
                                }, 
                                {
                                    "script": "AIAction94", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "79", 
                                    "param2": "20014655", 
                                    "param1": "Monster"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "kuangbao"
                                }
                            ], 
                            "EID": [
                                49, 
                                50
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "40"
                                }
                            ], 
                            "id": 49
                        }, 
                        {
                            "comment": "40%血50%概率“阴”/kuangbao", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "7"
                                }, 
                                {
                                    "script": "AIAction18", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "t1"
                                }, 
                                {
                                    "script": "AIAction48", 
                                    "param5": "20014655", 
                                    "param4": "1", 
                                    "param3": "", 
                                    "param2": "50", 
                                    "param1": "364.0 5901.0 -472.1"
                                }, 
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "3"
                                }, 
                                {
                                    "script": "AIAction94", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "79", 
                                    "param2": "20014655", 
                                    "param1": "Monster"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "kuangbao"
                                }
                            ], 
                            "EID": [
                                49, 
                                50
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "40"
                                }
                            ], 
                            "id": 50
                        }, 
                        {
                            "comment": "", 
                            "odds": 0.0, 
                            "Actions": [], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 54
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            2: {
                "name": "阳状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "BUFF", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t2"
                            }, 
                            {
                                "script": "AIAction75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12230701"
                            }, 
                            {
                                "script": "AIAction207", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            9
                        ], 
                        "Conditions": [], 
                        "id": 9
                    }, 
                    {
                        "comment": "自爆", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122307003"
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
                                "param1": "t2"
                            }
                        ], 
                        "id": 11
                    }, 
                    {
                        "comment": "t2=11跳1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction48", 
                                "param5": "20014655", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "30", 
                                "param1": "364.0 5901.0 -400.1"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t2"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "9|11|26"
                            }, 
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "1"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "11", 
                                "param1": "t2"
                            }
                        ], 
                        "id": 12
                    }, 
                    {
                        "comment": "使用爆气", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122307002"
                            }
                        ], 
                        "EID": [
                            26
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "t2"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122307002"
                            }
                        ], 
                        "id": 26
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到666变成中立", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction38", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2"
                                }
                            ], 
                            "EID": [
                                33
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "666", 
                                    "param1": ""
                                }
                            ], 
                            "id": 33
                        }
                    ], 
                    6: [
                        {
                            "comment": "", 
                            "odds": 1.0, 
                            "Actions": [], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 51
                        }, 
                        {
                            "comment": "20%血跳4", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "4"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20"
                                }
                            ], 
                            "id": 52
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            3: {
                "name": "阴状态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "自身爆气", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t2"
                            }, 
                            {
                                "script": "AIAction75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12230702"
                            }, 
                            {
                                "script": "AIAction207", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [
                            13
                        ], 
                        "Conditions": [], 
                        "id": 13
                    }, 
                    {
                        "comment": "自爆", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122307006"
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
                                "param1": "t2"
                            }
                        ], 
                        "id": 14
                    }, 
                    {
                        "comment": "t2=11 跳1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t2"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "13|14|27"
                            }, 
                            {
                                "script": "AIAction48", 
                                "param5": "20014655", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "30", 
                                "param1": "364.0 5901.0 -400.1"
                            }, 
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "1"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "11", 
                                "param1": "t2"
                            }
                        ], 
                        "id": 15
                    }, 
                    {
                        "comment": "使用爆气", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122307002"
                            }
                        ], 
                        "EID": [
                            27
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "t2"
                            }, 
                            {
                                "script": "AICondition11", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122307002"
                            }
                        ], 
                        "id": 27
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到666变成中立", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction38", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2"
                                }
                            ], 
                            "EID": [
                                34
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "666", 
                                    "param1": ""
                                }
                            ], 
                            "id": 34
                        }
                    ], 
                    6: [
                        {
                            "comment": "20%血跳4", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "4"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20"
                                }
                            ], 
                            "id": 53
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            4: {
                "name": "混沌形态", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "每隔3秒，将伤害最高的目标设为攻击目标", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction8", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "3"
                            }
                        ], 
                        "id": 21
                    }, 
                    {
                        "comment": "距离玩家超过2米开始追击", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction73", 
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
                                "script": "AICondition23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
                            }
                        ], 
                        "id": 22
                    }, 
                    {
                        "comment": "距离玩家小于3米攻击或者远离", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction71", 
                                "param5": "20", 
                                "param4": "122307001|122308001|122309001", 
                                "param3": "2.5", 
                                "param2": "1", 
                                "param1": "0.9"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition24", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "3"
                            }
                        ], 
                        "id": 23
                    }, 
                    {
                        "comment": "时间t3", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t3"
                            }
                        ], 
                        "EID": [
                            24
                        ], 
                        "Conditions": [], 
                        "id": 24
                    }, 
                    {
                        "comment": "混沌无极", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122307009"
                            }, 
                            {
                                "script": "AIAction48", 
                                "param5": "20014655", 
                                "param4": "1", 
                                "param3": "", 
                                "param2": "79", 
                                "param1": "364.0 5901.0 -472.1"
                            }, 
                            {
                                "script": "AIAction207", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "24|25"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "t3"
                            }
                        ], 
                        "EID": [
                            25
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20", 
                                "param1": "t3"
                            }
                        ], 
                        "id": 25
                    }, 
                    {
                        "comment": "销毁阴\\阳\\混沌阵", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction94", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "50", 
                                "param2": "20014652|20014653|20014655", 
                                "param1": "Monster"
                            }
                        ], 
                        "EID": [
                            41
                        ], 
                        "Conditions": [], 
                        "id": 41
                    }, 
                    {
                        "comment": "50%概率阳球（暂废）", 
                        "odds": 0.0, 
                        "Actions": [], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 42
                    }, 
                    {
                        "comment": "50%概率阴球（暂废）", 
                        "odds": 0.0, 
                        "Actions": [], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 43
                    }, 
                    {
                        "comment": "发送20013440   2指令", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction10", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "2", 
                                "param2": "20013440", 
                                "param1": "79|20"
                            }
                        ], 
                        "EID": [
                            44
                        ], 
                        "Conditions": [], 
                        "id": 44
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到666变成中立", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction38", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "2"
                                }
                            ], 
                            "EID": [
                                35
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "666", 
                                    "param1": ""
                                }
                            ], 
                            "id": 35
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
    "free": {
        "subStateDatas": {
            1: {
                "name": "清除阵法", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "清除法阵", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction94", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "79", 
                                "param2": "20014652|20014653|20014654|20014658|20014659", 
                                "param1": "Monster"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 16
                    }
                ], 
                "eventsAI": {
                    21: [
                        {
                            "comment": "关闭光墙", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction136", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 30
                        }, 
                        {
                            "comment": "移除genzong", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction56", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "genzong"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 45
                        }, 
                        {
                            "comment": "发送20013440   3指令", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction10", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "3", 
                                    "param2": "20013440", 
                                    "param1": "79|20"
                                }
                            ], 
                            "EID": [
                                46
                            ], 
                            "Conditions": [], 
                            "id": 46
                        }, 
                        {
                            "comment": "关闭光墙", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction136", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": ""
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 55
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