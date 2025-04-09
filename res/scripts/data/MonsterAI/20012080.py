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
                "name": "死亡", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "播放语音", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C001263", 
                                "param1": "79|19"
                            }, 
                            {
                                "script": "AIAction94", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "99", 
                                "param2": "20013631|20013632", 
                                "param1": "Monster"
                            }
                        ], 
                        "EID": [
                            32
                        ], 
                        "Conditions": [], 
                        "id": 32
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
                        "comment": "距离玩家超过3米开始追击", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction73", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "3"
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
                                "param1": "3"
                            }
                        ], 
                        "id": 3
                    }, 
                    {
                        "comment": "距离玩家小于3米攻击或者远离", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction71", 
                                "param5": "20", 
                                "param4": "121982001|121983001|121984001|121985001", 
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
                        "comment": "记录时间b1|b4", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "b1"
                            }, 
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "b4"
                            }
                        ], 
                        "EID": [
                            12
                        ], 
                        "Conditions": [], 
                        "id": 12
                    }, 
                    {
                        "comment": " b1=45跳2", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "2"
                            }, 
                            {
                                "script": "AIAction76", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12161405"
                            }
                        ], 
                        "EID": [
                            13
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "45", 
                                "param1": "b1"
                            }
                        ], 
                        "id": 13
                    }, 
                    {
                        "comment": "超过12m冲锋", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction4", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "110286089"
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
                                "param1": "12"
                            }
                        ], 
                        "id": 16
                    }, 
                    {
                        "comment": "开战播放语音", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C001259", 
                                "param1": "79|19"
                            }
                        ], 
                        "EID": [
                            17
                        ], 
                        "Conditions": [], 
                        "id": 17
                    }, 
                    {
                        "comment": "b1=5玩家语音", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction131", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C001262", 
                                "param1": "C001261"
                            }, 
                            {
                                "script": "AIAction55", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "a"
                            }
                        ], 
                        "EID": [
                            19
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "5", 
                                "param1": "b1"
                            }, 
                            {
                                "script": "AICondition28", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "a"
                            }
                        ], 
                        "id": 19
                    }, 
                    {
                        "comment": "添加霸体", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "10000001"
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
                        "id": 30
                    }, 
                    {
                        "comment": " b4=120跳3", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "3"
                            }, 
                            {
                                "script": "AIAction76", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12161405"
                            }
                        ], 
                        "EID": [
                            38
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "120", 
                                "param1": "b4"
                            }
                        ], 
                        "id": 38
                    }
                ], 
                "eventsAI": {
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
                            "comment": "80%血量召唤僵尸", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction48", 
                                    "param5": "20012204", 
                                    "param4": "2", 
                                    "param3": "", 
                                    "param2": "20", 
                                    "param1": "-760 480 320"
                                }
                            ], 
                            "EID": [
                                18
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
                            "id": 18
                        }, 
                        {
                            "comment": "60%血量召唤僵尸", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction48", 
                                    "param5": "20012204", 
                                    "param4": "2", 
                                    "param3": "", 
                                    "param2": "20", 
                                    "param1": "-760 480 320"
                                }
                            ], 
                            "EID": [
                                20
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
                            "id": 20
                        }, 
                        {
                            "comment": "50%血量跳3阶段", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "3"
                                }
                            ], 
                            "EID": [
                                21
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "50"
                                }
                            ], 
                            "id": 21
                        }, 
                        {
                            "comment": "40%血量召唤僵尸", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction48", 
                                    "param5": "20012204", 
                                    "param4": "2", 
                                    "param3": "", 
                                    "param2": "20", 
                                    "param1": "-760 480 320"
                                }
                            ], 
                            "EID": [
                                22
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
                            "id": 22
                        }, 
                        {
                            "comment": "30%血量跳3阶段", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction3", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "3"
                                }
                            ], 
                            "EID": [
                                23
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "30"
                                }
                            ], 
                            "id": 23
                        }, 
                        {
                            "comment": "20%血量召唤僵尸", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction48", 
                                    "param5": "20012204", 
                                    "param4": "2", 
                                    "param3": "", 
                                    "param2": "20", 
                                    "param1": "-760 480 320"
                                }
                            ], 
                            "EID": [
                                24
                            ], 
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
                            "id": 24
                        }, 
                        {
                            "comment": "10%血量召唤僵尸", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction48", 
                                    "param5": "20012204", 
                                    "param4": "2", 
                                    "param3": "", 
                                    "param2": "20", 
                                    "param1": "-760 480 320"
                                }
                            ], 
                            "EID": [
                                25
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "10"
                                }
                            ], 
                            "id": 25
                        }, 
                        {
                            "comment": "90%血量召唤蛮牛", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction48", 
                                    "param5": "20012207", 
                                    "param4": "2", 
                                    "param3": "", 
                                    "param2": "20", 
                                    "param1": "-760 480 320"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "a"
                                }
                            ], 
                            "EID": [
                                27
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "90"
                                }, 
                                {
                                    "script": "AICondition28", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "a"
                                }
                            ], 
                            "id": 27
                        }, 
                        {
                            "comment": "70%血量召唤蛮牛", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction48", 
                                    "param5": "20012207", 
                                    "param4": "2", 
                                    "param3": "", 
                                    "param2": "20", 
                                    "param1": "-760 480 320"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "b"
                                }
                            ], 
                            "EID": [
                                28
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "70"
                                }, 
                                {
                                    "script": "AICondition28", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "b"
                                }
                            ], 
                            "id": 28
                        }, 
                        {
                            "comment": "50%血量召唤蛮牛", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction48", 
                                    "param5": "20012207", 
                                    "param4": "2", 
                                    "param3": "", 
                                    "param2": "20", 
                                    "param1": "-760 480 320"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "c"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "-760 480 320", 
                                    "param1": "20012209"
                                }
                            ], 
                            "EID": [
                                29
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "50"
                                }, 
                                {
                                    "script": "AICondition28", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "c"
                                }
                            ], 
                            "id": 29
                        }, 
                        {
                            "comment": "20%血量召唤蛮牛\\召唤寒冰", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "-760 480 320", 
                                    "param1": "20012209"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "d"
                                }, 
                                {
                                    "script": "AIAction48", 
                                    "param5": "20012207", 
                                    "param4": "2", 
                                    "param3": "", 
                                    "param2": "20", 
                                    "param1": "-760 480 320"
                                }
                            ], 
                            "EID": [
                                31
                            ], 
                            "Conditions": [
                                {
                                    "script": "AICondition9", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "20"
                                }, 
                                {
                                    "script": "AICondition28", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "d"
                                }
                            ], 
                            "id": 31
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.000000", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            2: {
                "name": "飞天+掉火球", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "移动到场地中央", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction1", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20", 
                                "param2": "1", 
                                "param1": "-760 480 320"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 7
                    }, 
                    {
                        "comment": " b2=1 起飞", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122000001"
                            }
                        ], 
                        "EID": [
                            8
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "b2"
                            }
                        ], 
                        "id": 8
                    }, 
                    {
                        "comment": " b2=2 陨石", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction169", 
                                "param5": "5|3|20012206", 
                                "param4": "20|2", 
                                "param3": "120", 
                                "param2": "0 0 30", 
                                "param1": "-760 480 320"
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "5|3|20012206", 
                                "param4": "20|2", 
                                "param3": "120", 
                                "param2": "0 0 150", 
                                "param1": "-760 480 320"
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "5|3|20012206", 
                                "param4": "20|2", 
                                "param3": "120", 
                                "param2": "0 0 270", 
                                "param1": "-760 480 320"
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "1|1|20012205", 
                                "param4": "20|2", 
                                "param3": "", 
                                "param2": "0 0 0", 
                                "param1": "-760 480 320"
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "1|1|20012208", 
                                "param4": "15|5", 
                                "param3": "", 
                                "param2": "0 0 0", 
                                "param1": "-760 480 320"
                            }, 
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "C001260", 
                                "param1": "79|19"
                            }
                        ], 
                        "EID": [
                            9
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "b2"
                            }
                        ], 
                        "id": 9
                    }, 
                    {
                        "comment": "b2=9陨石", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction169", 
                                "param5": "5|9|20012206", 
                                "param4": "35|8", 
                                "param3": "120", 
                                "param2": "0 0 90", 
                                "param1": "-760 480 320"
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "5|9|20012206", 
                                "param4": "35|8", 
                                "param3": "120", 
                                "param2": "0 0 270", 
                                "param1": "-760 480 320"
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "5|9|20012206", 
                                "param4": "35|8", 
                                "param3": "120", 
                                "param2": "0 0 30", 
                                "param1": "-760 480 320"
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "1|1|20012205", 
                                "param4": "30|8", 
                                "param3": "", 
                                "param2": "0 0 0", 
                                "param1": "-760 480 320"
                            }, 
                            {
                                "script": "AIAction169", 
                                "param5": "1|1|20012208", 
                                "param4": "30|20", 
                                "param3": "", 
                                "param2": "0 0 0", 
                                "param1": "-760 480 320"
                            }
                        ], 
                        "EID": [
                            10
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "8", 
                                "param1": "b2"
                            }
                        ], 
                        "id": 10
                    }, 
                    {
                        "comment": "b2=12 清除b2b1\\EAI\\跳1", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "b2|b1"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12|13|9|10|7|8"
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
                                "param2": "12", 
                                "param1": "b2"
                            }
                        ], 
                        "id": 11
                    }, 
                    {
                        "comment": "记录时间b2", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "b2"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "-760 480 320"
                            }
                        ], 
                        "id": 26
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            3: {
                "name": "全屏\\分离仙魔", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "移动到场中央", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction1", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "20", 
                                "param2": "1", 
                                "param1": "-760 480 320"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [], 
                        "id": 33
                    }, 
                    {
                        "comment": "记录时间b3+刷出保护罩", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "b3"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "-760 480 320"
                            }
                        ], 
                        "id": 34
                    }, 
                    {
                        "comment": " b3=01 起飞", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction16", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "122000003"
                            }
                        ], 
                        "EID": [], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1", 
                                "param1": "b3"
                            }
                        ], 
                        "id": 35
                    }, 
                    {
                        "comment": " b3=20 清除b1\\b4\\nEAI\\跳1\\销毁保护罩", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "b4|b3"
                            }, 
                            {
                                "script": "AIAction21", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "12|13|34|35|36|37"
                            }, 
                            {
                                "script": "AIAction3", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "1"
                            }, 
                            {
                                "script": "AIAction59", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "xh"
                            }
                        ], 
                        "EID": [
                            36
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "20", 
                                "param1": "b3"
                            }
                        ], 
                        "id": 36
                    }, 
                    {
                        "comment": " b3=02 召唤", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 0", 
                                "param2": "-2911.0 1973.0 225.0", 
                                "param1": "20013631"
                            }, 
                            {
                                "script": "AIAction23", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "0 0 0", 
                                "param2": "1351.0 -990.0 222.0", 
                                "param1": "20013632"
                            }
                        ], 
                        "EID": [
                            37
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "2", 
                                "param1": "b3"
                            }
                        ], 
                        "id": 37
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
    "free": {
        "subStateDatas": {
            1: {
                "name": "霸体", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "霸体", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "10000001"
                            }
                        ], 
                        "EID": [
                            15
                        ], 
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
                        "id": 15
                    }
                ], 
                "eventsAI": {
                    21: [
                        {
                            "comment": "销毁保护罩", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction94", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "90", 
                                    "param2": "20013631|20013632", 
                                    "param1": "Monster"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [], 
                            "id": 39
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
                "name": "霸体", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "霸体", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction75", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "10000001"
                            }
                        ], 
                        "EID": [
                            14
                        ], 
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
                        "id": 14
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