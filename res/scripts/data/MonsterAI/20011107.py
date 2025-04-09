# -*- coding: utf-8 -*-
Datas = {
    "reset": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }, 
    "show": {
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
                "name": "古朗月行", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "被子弹击中，切换2", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction3", 
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
                                "script": "AICondition14", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "14025901"
                            }
                        ], 
                        "id": 6
                    }
                ], 
                "eventsAI": {
                    9: [
                        {
                            "comment": "收到jin通知，刷出法阵金", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction153", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "jin"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0.0 0.0 100.0", 
                                    "param2": "-213.446533 2883.148438 6378.2011719", 
                                    "param1": "20011091"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "cs"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "jin", 
                                    "param1": ""
                                }
                            ], 
                            "id": 1
                        }, 
                        {
                            "comment": "收到mu通知，刷出法阵木", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction153", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "mu"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0.0 0.0 100.0", 
                                    "param2": "-213.446533 2883.148438 6378.2011719", 
                                    "param1": "20011092"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "cs"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "mu", 
                                    "param1": ""
                                }
                            ], 
                            "id": 2
                        }, 
                        {
                            "comment": "收到shui通知，刷出法阵水", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction153", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "shui"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0.0 0.0 100.0", 
                                    "param2": "-213.446533 2883.148438 6378.2011719", 
                                    "param1": "20011093"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "cs"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "shui", 
                                    "param1": ""
                                }
                            ], 
                            "id": 3
                        }, 
                        {
                            "comment": "收到huo通知，刷出法阵火", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction153", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "huo"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0.0 0.0 100.0", 
                                    "param2": "-213.446533 2883.148438 6378.2011719", 
                                    "param1": "20011094"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "cs"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "huo", 
                                    "param1": ""
                                }
                            ], 
                            "id": 4
                        }, 
                        {
                            "comment": "收到tu通知，刷出法阵土", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction153", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "tu"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0.0 0.0 100.0", 
                                    "param2": "-213.446533 2883.148438 6378.2011719", 
                                    "param1": "20011095"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "cs"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "tu", 
                                    "param1": ""
                                }
                            ], 
                            "id": 5
                        }, 
                        {
                            "comment": "收到jin2通知，刷出金标记傀儡", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction153", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "jin"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0.0 0.0 100.0", 
                                    "param2": "-213.446533 2883.148438 6378.2011719", 
                                    "param1": "20011241"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "jin2", 
                                    "param1": ""
                                }
                            ], 
                            "id": 10
                        }, 
                        {
                            "comment": "收到mu2通知，刷出木标记用傀儡", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction153", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "mu"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0.0 0.0 100.0", 
                                    "param2": "-213.446533 2883.148438 6378.2011719", 
                                    "param1": "20011242"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "mu2", 
                                    "param1": ""
                                }
                            ], 
                            "id": 11
                        }, 
                        {
                            "comment": "收到shui2通知，刷出水标记用傀儡", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction153", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "shui"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0.0 0.0 100.0", 
                                    "param2": "-213.446533 2883.148438 6378.2011719", 
                                    "param1": "20011243"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "shui2", 
                                    "param1": ""
                                }
                            ], 
                            "id": 12
                        }, 
                        {
                            "comment": "收到huo2通知，刷出火标记用傀儡", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction153", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "huo"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0.0 0.0 100.0", 
                                    "param2": "-213.446533 2883.148438 6378.2011719", 
                                    "param1": "20011244"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "huo2", 
                                    "param1": ""
                                }
                            ], 
                            "id": 13
                        }, 
                        {
                            "comment": "收到tu2通知，刷出土标记用傀儡", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction153", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "tu"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0.0 0.0 100.0", 
                                    "param2": "-213.446533 2883.148438 6378.2011719", 
                                    "param1": "20011245"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "tu2", 
                                    "param1": ""
                                }
                            ], 
                            "id": 14
                        }, 
                        {
                            "comment": "收到AGREE,跳转3", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "17"
                                }, 
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "tt"
                                }, 
                                {
                                    "script": "AIAction3", 
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
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Agree", 
                                    "param1": ""
                                }
                            ], 
                            "id": 15
                        }, 
                        {
                            "comment": "收到Atypism,跳转4", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction21", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "18"
                                }, 
                                {
                                    "script": "AIAction17", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "tt"
                                }, 
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
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "Atypism", 
                                    "param1": ""
                                }
                            ], 
                            "id": 16
                        }, 
                        {
                            "comment": "收到jin4通知，刷出金标记傀儡", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction153", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "jin"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0.0 0.0 100.0", 
                                    "param2": "-213.446533 2883.148438 6378.2011719", 
                                    "param1": "20011241"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "cs"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "jin4", 
                                    "param1": ""
                                }
                            ], 
                            "id": 21
                        }, 
                        {
                            "comment": "收到mu4通知，刷出木标记用傀儡", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction153", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "mu"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0.0 0.0 100.0", 
                                    "param2": "-213.446533 2883.148438 6378.2011719", 
                                    "param1": "20011242"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "cs"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "mu4", 
                                    "param1": ""
                                }
                            ], 
                            "id": 22
                        }, 
                        {
                            "comment": "收到shui4通知，刷出水标记用傀儡", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction153", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "shui"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0.0 0.0 100.0", 
                                    "param2": "-213.446533 2883.148438 6378.2011719", 
                                    "param1": "20011243"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "cs"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "shui4", 
                                    "param1": ""
                                }
                            ], 
                            "id": 23
                        }, 
                        {
                            "comment": "收到huo4通知，刷出火标记用傀儡", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction153", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "huo"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0.0 0.0 100.0", 
                                    "param2": "-213.446533 2883.148438 6378.2011719", 
                                    "param1": "20011244"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "cs"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "huo4", 
                                    "param1": ""
                                }
                            ], 
                            "id": 24
                        }, 
                        {
                            "comment": "收到tu4通知，刷出土标记用傀儡", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction153", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "tu"
                                }, 
                                {
                                    "script": "AIAction23", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "0.0 0.0 100.0", 
                                    "param2": "-213.446533 2883.148438 6378.2011719", 
                                    "param1": "20011245"
                                }, 
                                {
                                    "script": "AIAction55", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "cs"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "tu4", 
                                    "param1": ""
                                }
                            ], 
                            "id": 25
                        }, 
                        {
                            "comment": "收到tip通知，自身存在cs标记，根据属性刷出提示光效", 
                            "odds": 1.0, 
                            "Actions": [
                                {
                                    "script": "AIAction158", 
                                    "param5": "", 
                                    "param4": "0.0 0.0 100.0", 
                                    "param3": "-213.446533 2883.148438 6378.2011719", 
                                    "param2": "20011091|20011092|20011093|20011094|20011095", 
                                    "param1": "jin|mu|shui|huo|tu"
                                }
                            ], 
                            "EID": [], 
                            "Conditions": [
                                {
                                    "script": "AICondition25", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "tip", 
                                    "param1": ""
                                }, 
                                {
                                    "script": "AICondition27", 
                                    "param5": "", 
                                    "param4": "", 
                                    "param3": "", 
                                    "param2": "", 
                                    "param1": "cs"
                                }
                            ], 
                            "id": 26
                        }
                    ]
                }, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            2: {
                "name": "桂树何团团", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "画卷为空，则设置画卷与机关同属性", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction159", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "20011090"
                            }, 
                            {
                                "script": "AIAction43", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "14025901"
                            }, 
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Cy000582", 
                                "param1": "80"
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
                                "script": "AICondition69", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }
                        ], 
                        "id": 7
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            3: {
                "name": "画卷与机关属性一致", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "不存在标记，画卷与机关属性一致，分身出现，再消失", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction158", 
                                "param5": "2", 
                                "param4": "0.0 0.0 -70.0", 
                                "param3": "-489.254883 5090.000000 6776.000000", 
                                "param2": "20011236|20011237|20011238|20011239|20011240", 
                                "param1": "jin|mu|shui|huo|tu"
                            }, 
                            {
                                "script": "AIAction43", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "14025901"
                            }, 
                            {
                                "script": "AIAction154", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "tt"
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
                                "param2": "1", 
                                "param1": "tt"
                            }, 
                            {
                                "script": "AICondition28", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "cs"
                            }
                        ], 
                        "id": 17
                    }, 
                    {
                        "comment": "存在标记，画卷与机关属性一致，分身出现，再消失", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction158", 
                                "param5": "2", 
                                "param4": "0.0 0.0 -70.0", 
                                "param3": "-489.254883 5090.000000 6776.000000", 
                                "param2": "20011615|20011616|20011617|20011618|20011619", 
                                "param1": "jin|mu|shui|huo|tu"
                            }, 
                            {
                                "script": "AIAction43", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "14025901"
                            }, 
                            {
                                "script": "AIAction154", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "tt"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "cs"
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
                                "param2": "1", 
                                "param1": "tt"
                            }, 
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "cs"
                            }
                        ], 
                        "id": 19
                    }
                ], 
                "eventsAI": {}, 
                "initiativeAreaXZ": "0.0", 
                "subHoldEffectIDs": [], 
                "initiativeTrapType": 0, 
                "initiativeTrapShape": 2
            }, 
            4: {
                "name": "画卷与机关属性不一致", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "不存在标记，画卷与机关属性不一致，分身出现，攻击玩家", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction158", 
                                "param5": "2", 
                                "param4": "0.0 0.0 -70.0", 
                                "param3": "-489.254883 5090.000000 6776.000000", 
                                "param2": "20011231|20011232|20011233|20011234|20011235", 
                                "param1": "jin|mu|shui|huo|tu"
                            }, 
                            {
                                "script": "AIAction43", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "14025901"
                            }, 
                            {
                                "script": "AIAction154", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Cy000579", 
                                "param1": "100"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "tt"
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
                                "param2": "1", 
                                "param1": "tt"
                            }, 
                            {
                                "script": "AICondition28", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "cs"
                            }
                        ], 
                        "id": 18
                    }, 
                    {
                        "comment": "存在标记，画卷与机关属性不一致，分身出现，攻击玩家", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction158", 
                                "param5": "2", 
                                "param4": "0.0 0.0 -70.0", 
                                "param3": "-489.254883 5090.000000 6776.000000", 
                                "param2": "20011610|20011611|20011612|20011613|20011614", 
                                "param1": "jin|mu|shui|huo|tu"
                            }, 
                            {
                                "script": "AIAction43", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "14025901"
                            }, 
                            {
                                "script": "AIAction154", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": ""
                            }, 
                            {
                                "script": "AIAction30", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "Cy000579", 
                                "param1": "100"
                            }, 
                            {
                                "script": "AIAction18", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "tt"
                            }, 
                            {
                                "script": "AIAction56", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "cs"
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
                                "param2": "1", 
                                "param1": "tt"
                            }, 
                            {
                                "script": "AICondition27", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "cs"
                            }
                        ], 
                        "id": 20
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
    "pead": {
        "subStateDatas": {}, 
        "groupHoldEffectIDs": []
    }
}