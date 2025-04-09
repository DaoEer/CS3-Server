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
            "title": "刷符石", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 0|0 0 0|0 0 0|0 0 0|0 0 0|0 0 0|0 0 0", 
                    "param2": "-6640 9373 63|-8772 7240 169|-9414 3589 168|-5895 -660 70|-4706 -6569 297|4803 -415 120|7581 7643 816", 
                    "param1": "20007188|40000149|40000150|40000149|40000150|40000149|40000150", 
                    "param4": "7", 
                    "id": 156
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "刷BOSS", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20007192:1", 
                    "param2": "0 0 -13", 
                    "param1": "-92 -856 1000", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20007187:1", 
                    "param2": "0 0 -13", 
                    "param1": "-92 -856 430", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20007231:1", 
                    "param2": "0 0 -13", 
                    "param1": "-92 -856 430", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }, 
        {
            "title": "副本失败计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "900", 
                    "param1": "shibai", 
                    "param4": "", 
                    "id": 12
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
            "title": "土水晶刷新", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "20007188", 
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
                    "param1": "tu", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "火符刷新", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 0|0 0 0|0 0 0|0 0 0|0 0 0|0 0 0", 
                    "param2": "4831 2045 236|6608 -1327 46|2545 6717 179|-3199 8399 60|5134 3509 244|-7493 6969 -6", 
                    "param1": "40000150|40000150|40000150|40000150", 
                    "param4": "4", 
                    "id": 156
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 36, 
                    "param1": "40000150", 
                    "param2": "3"
                }
            ], 
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
            "title": "雷符刷新", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 0|0 0 0|0 0 0|0 0 0|0 0 0|0 0 0", 
                    "param2": "174 5435 39|7581 7643 816|-7570 2925 -30|-12015 3446 366|1796 -5872 19|-8329 -1102 154", 
                    "param1": "40000149|40000149|40000149|40000149", 
                    "param4": "4", 
                    "id": 156
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 36, 
                    "param1": "40000149", 
                    "param2": "3"
                }
            ], 
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
            "id": 4
        }, 
        {
            "title": "时间到达未完成副本", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 4
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 436
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "shibai", 
                    "param2": ""
                }
            ], 
            "id": 5
        }
    ], 
    3: [
        {
            "title": "额外道具使用", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 119
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    5: [
        {
            "title": "土水晶刷新5秒计时", 
            "describe": "土水晶死亡计时", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "5", 
                    "param1": "tu", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 36, 
                    "param1": "20007188", 
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
                    "param1": "20007188", 
                    "param2": ""
                }
            ], 
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
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 436
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "6", 
                    "param1": "dead", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000556:1", 
                    "param2": "0 0 -129", 
                    "param1": "-1706 -2984 376", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20008616:1", 
                    "param2": "0 0 -129", 
                    "param1": "-1036 -2143 370", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "cc", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20007187", 
                    "param2": ""
                }
            ], 
            "id": 2
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
                    "param1": "20007188|40000149|40000150|20007192|20007231", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "223", 
                    "param1": "20007187", 
                    "param4": "", 
                    "id": 10
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
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 436
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "6", 
                    "param1": "dead", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000556:1", 
                    "param2": "0 0 -129", 
                    "param1": "-1706 -2984 376", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20008616:1", 
                    "param2": "0 0 -129", 
                    "param1": "-1036 -2143 370", 
                    "param4": "", 
                    "id": 6
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
            "title": "一阶段结束镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "268", 
                    "param4": "", 
                    "id": 170
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
    12: [
        {
            "title": "雷销毁再刷新5秒标记", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "5", 
                    "param1": "lei", 
                    "param4": "", 
                    "id": 12
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
                    "param3": "1", 
                    "id": 36, 
                    "param1": "40000149", 
                    "param2": "3"
                }, 
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 36, 
                    "param1": "20007186", 
                    "param2": "1"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "40000149", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "火销毁后刷新5秒标记", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "5", 
                    "param1": "huo", 
                    "param4": "", 
                    "id": 12
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
                    "param3": "1", 
                    "id": 36, 
                    "param1": "40000150", 
                    "param2": "3"
                }, 
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 36, 
                    "param1": "20007185", 
                    "param2": "1"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "40000150", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    13: [
        {
            "title": "出本移出物品和提醒", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "302010003|302010004", 
                    "param4": "", 
                    "id": 23
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12093301|12093401", 
                    "param4": "", 
                    "id": 25
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 120
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    14: [], 
    15: [
        {
            "title": "触发传送回主场景", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "121544004", 
                    "param4": "", 
                    "id": 17
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
            "triggerConditions": [
                {
                    "param4": "2", 
                    "param3": "-1036 -2143 370", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "800|70"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "直接杀boss触发传送回主场景", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "121544004", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "2", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "cc", 
                    "param2": "1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "2", 
                    "param3": "-1036 -2143 370", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "800|70"
                }
            ], 
            "id": 2
        }
    ], 
    21: [
        {
            "title": "435", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 435
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ]
}