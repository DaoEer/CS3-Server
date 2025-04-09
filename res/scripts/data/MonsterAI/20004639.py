# -*- coding: utf-8 -*-
Datas = {
    "reset": {
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
                "name": "召唤点金石进行时", 
                "tickTimer": 0.5, 
                "statesAI": [
                    {
                        "comment": "开始计时", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction17", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "", 
                                "param1": "kaishi"
                            }
                        ], 
                        "EID": [
                            1
                        ], 
                        "Conditions": [], 
                        "id": 1
                    }, 
                    {
                        "comment": "召唤第1个点金石（2区域随机）", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction130", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "40000066", 
                                "param2": "0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0", 
                                "param1": "319 23763 352|2020 14596 93|-3711 7576 176|-4885 -5533 -24"
                            }
                        ], 
                        "EID": [
                            2
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "30", 
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 2
                    }, 
                    {
                        "comment": "召唤第2个点金石（2区域随机）", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction130", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "40000066", 
                                "param2": "0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0", 
                                "param1": "319 23763 352|2020 14596 93|-3711 7576 176|-4885 -5533 -24"
                            }
                        ], 
                        "EID": [
                            3
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "330", 
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 3
                    }, 
                    {
                        "comment": "召唤第3个点金石（23区域随机）", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction130", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "40000066", 
                                "param2": "0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0", 
                                "param1": "319 23763 352|2020 14596 93|-3711 7576 176|-4885 -5533 -24|34240 -10543 -24|31270 2996 -18|43170 7456 -5|31640 15826 139"
                            }
                        ], 
                        "EID": [
                            4
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "630", 
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 4
                    }, 
                    {
                        "comment": "召唤第4个点金石（23区域随机）", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction130", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "40000066", 
                                "param2": "0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0", 
                                "param1": "319 23763 352|2020 14596 93|-3711 7576 176|-4885 -5533 -24|34240 -10543 -24|31270 2996 -18|43170 7456 -5|31640 15826 139"
                            }
                        ], 
                        "EID": [
                            5
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "930", 
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 5
                    }, 
                    {
                        "comment": "召唤第5个点金石（234区域随机）", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction130", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "40000066", 
                                "param2": "0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0", 
                                "param1": "319 23763 352|2020 14596 93|-3711 7576 176|-4885 -5533 -24|34240 -10543 -24|31270 2996 -18|43170 7456 -5|31640 15826 139|71680 11936 -94|83590 2076 -94|68350 2166 -24|67190 -8073 -94"
                            }
                        ], 
                        "EID": [
                            6
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1230", 
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 6
                    }, 
                    {
                        "comment": "召唤第6个点金石（234区域随机）", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction130", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "40000066", 
                                "param2": "0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0", 
                                "param1": "319 23763 352|2020 14596 93|-3711 7576 176|-4885 -5533 -24|34240 -10543 -24|31270 2996 -18|43170 7456 -5|31640 15826 139|71680 11936 -94|83590 2076 -94|68350 2166 -24|67190 -8073 -94"
                            }
                        ], 
                        "EID": [
                            7
                        ], 
                        "Conditions": [
                            {
                                "script": "AICondition12", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "", 
                                "param2": "1530", 
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 7
                    }, 
                    {
                        "comment": "召唤第7个点金石（234区域随机）", 
                        "odds": 1.0, 
                        "Actions": [
                            {
                                "script": "AIAction130", 
                                "param5": "", 
                                "param4": "", 
                                "param3": "40000066", 
                                "param2": "0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0|0.0 0.0 0.0", 
                                "param1": "319 23763 352|2020 14596 93|-3711 7576 176|-4885 -5533 -24|34240 -10543 -24|31270 2996 -18|43170 7456 -5|31640 15826 139|71680 11936 -94|83590 2076 -94|68350 2166 -24|67190 -8073 -94"
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
                                "param2": "1830", 
                                "param1": "kaishi"
                            }
                        ], 
                        "id": 8
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