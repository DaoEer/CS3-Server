# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "设置复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 164", 
                    "param1": "11151 -7597 796", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "刷晶石", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "3", 
                    "param2": "20005820|20005821|20005822", 
                    "param1": "-6640 9373 63|-8772 7240 169|-9414 3589 168|-5895 -660 70|-4706 -6569 297|4803 -415 120", 
                    "param4": "", 
                    "id": 85
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "替换技能、光墙时间标记", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "75", 
                    "param1": "guangq", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }, 
        {
            "title": "刷BOSS", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20005824:1", 
                    "param2": "0 0 -13", 
                    "param1": "-92 -856 1000", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20005823:1", 
                    "param2": "0 0 164", 
                    "param1": "11151 -7597 796", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20005819:1", 
                    "param2": "0 0 -13", 
                    "param1": "-92 -856 430", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 4
        }
    ], 
    2: [
        {
            "title": "风水晶刷新", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "20005820", 
                    "param1": "1647 6866 144|4999 2671 254|-9244 4495 154|4531 -5515 -33|1483 -5824 38|-4809 -6038 233", 
                    "param4": "", 
                    "id": 85
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "feng", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "火水晶刷新", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "20005821", 
                    "param1": "4831 2045 236|6608 -1327 46|2545 6717 179|-3199 8399 60|5134 3509 244|-7493 6969 -6", 
                    "param4": "", 
                    "id": 85
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "huo", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "雷水晶刷新", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "20005822", 
                    "param1": "174 5435 39|7581 7643 816|-7570 2925 -30|-12015 3446 366|1796 -5872 19|-8329 -1102 154", 
                    "param4": "", 
                    "id": 85
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "lei", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "删光墙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20005823", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "guangq", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "boss死亡语音后，提示离开语音", 
            "describe": "死亡8秒播放", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000355", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20005825:1", 
                    "param2": "0 0 -13", 
                    "param1": "-92 -856 430", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "dead", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "开场镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "267", 
                    "param1": "20006551", 
                    "param4": "", 
                    "id": 7
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "jingt", 
                    "param2": ""
                }
            ], 
            "id": 6
        }, 
        {
            "title": "副本80秒后自动移动", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12079903|12079904", 
                    "param4": "", 
                    "id": 34
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "yy", 
                    "param4": "", 
                    "id": 13
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 32, 
                    "param1": "1", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 7, 
                    "param1": "100", 
                    "param2": "1"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "yy", 
                    "param2": ""
                }
            ], 
            "id": 7
        }
    ], 
    5: [
        {
            "title": "风水晶刷新10秒计时", 
            "describe": "风水晶死亡计时", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "10", 
                    "param1": "feng", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 36, 
                    "param1": "20005820", 
                    "param2": "1"
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 32, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20005820", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "火水晶刷新10秒计时", 
            "describe": "火水晶死亡计时", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "10", 
                    "param1": "huo", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 36, 
                    "param1": "20005821", 
                    "param2": "1"
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 32, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20005821", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "雷水晶刷新10秒计时", 
            "describe": "雷水晶死亡计时", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "10", 
                    "param1": "lei", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 36, 
                    "param1": "20005822", 
                    "param2": "1"
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 32, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20005822", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ], 
    8: [
        {
            "title": "分身死销毁水晶发223", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20005820|20005821|20005822|20005824", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "223", 
                    "param1": "20005819", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "268", 
                    "param1": "20006552", 
                    "param4": "", 
                    "id": 7
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "BOSS死，副本完成", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 3
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "5", 
                    "param1": "dead", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "一阶段完成去buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12078106|12079902|12079903|12079904", 
                    "param4": "", 
                    "id": 26
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }
    ], 
    14: [
        {
            "title": "收到666镜头加移动", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12079903|12079904", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "666", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "267"
                }
            ], 
            "id": 1
        }
    ], 
    17: [
        {
            "title": "出副本移除buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12078106|12079902|12079903|12079904", 
                    "param4": "", 
                    "id": 25
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    21: [
        {
            "title": "二阶段停止继续移动", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12078106|12079902|12079903|12079904", 
                    "param4": "", 
                    "id": 25
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 32, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "镜头时间标记", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "16", 
                    "param1": "jingt", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "自动移动标记", 
            "describe": "自动移动标记", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "1", 
                    "param1": "yy", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 3
        }
    ]
}