# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "设置出生复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "-10000 -5950 1765", 
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
            "id": 2
        }
    ], 
    2: [
        {
            "title": "时间到达未完成副本436", 
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
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 233
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "5", 
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
            "id": 1
        }
    ], 
    3: [
        {
            "title": "进入副本随机刷四精英", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "4", 
                    "param2": "20004088|20004089|20004090|20004091|20004092", 
                    "param1": "15779 -8521 3142|15780 -3456 3142|23059 -3031 3142|22906 -8970 3142", 
                    "param4": "", 
                    "id": 85
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    5: [
        {
            "title": "击杀通知key", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "456", 
                    "param1": "123", 
                    "param4": "", 
                    "id": 87
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20004097|20004098|20004099|20004100|20004101", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "击杀boss，通关436", 
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
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102552", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102553", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102056", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102057", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000556:1", 
                    "param2": "0 0 0", 
                    "param1": "24991 -6066 3147", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20008616:1", 
                    "param2": "0 0 0", 
                    "param1": "24060 -6030 3140", 
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
                    "param1": "5", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20004095", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    8: [
        {
            "title": "杀完精英刷新5个玩法怪物+字怪表现", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 5.0, 
                    "param3": "120272001", 
                    "param2": "1|5", 
                    "param1": "20004102;20004097|20004103;20004098|20004104;20004099|20004105;20004100|20004106;20004101", 
                    "param4": "", 
                    "id": 86
                }, 
                {
                    "delayTime": 10.0, 
                    "param3": "5", 
                    "param2": "20004097|20004098|20004099|20004100|20004101", 
                    "param1": "19400 -8241 3123|22126 -8360 3123|23317 -5962 3146|22040 -3651 3123|19451 -3767 3123", 
                    "param4": "", 
                    "id": 85
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "10077", 
                    "param1": "20004107", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 4, 
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "四精英死亡", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "10088", 
                    "param1": "20004096", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 4, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "召唤连线玩法", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20002767:1|20002767:1|20002767:1|20002767:1", 
                    "param2": "0 0 0|0 0 0|0 0 0|0 0 0", 
                    "param1": "16405 -8526 3320|16358 -3441 3320|23461 -3035 3320|23372 -8988 3320", 
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
                    "id": 4, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "阶段一完成设置新复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "11249 -6017 3117", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 4, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "阶段四完成擦屁股", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "100999", 
                    "param1": "20004097|20004098|20004099|20004100|20004101|20004102|20004103|20004104|20004105|20004106|20004107", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 4, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "阶段五完成，通关436", 
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
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102552", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102553", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102056", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20102057", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000556:1", 
                    "param2": "0 0 0", 
                    "param1": "24991 -6066 3147", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20008616:1", 
                    "param2": "0 0 0", 
                    "param1": "24060 -6030 3140", 
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
                    "id": 4, 
                    "param1": "5", 
                    "param2": ""
                }
            ], 
            "id": 6
        }
    ], 
    12: [
        {
            "title": "解除封印", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20004111|20002767", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 23, 
                    "param1": "20004096", 
                    "param2": "4"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "成功了销毁", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 8.0, 
                    "param3": "120272001", 
                    "param2": "1|5", 
                    "param1": "20004102;20004097|20004103;20004098|20004104;20004099|20004105;20004100|20004106;20004101", 
                    "param4": "", 
                    "id": 86
                }, 
                {
                    "delayTime": 13.0, 
                    "param3": "5", 
                    "param2": "20004097|20004098|20004099|20004100|20004101", 
                    "param1": "19400 -8241 3123|22126 -8360 3123|23317 -5962 3146|22040 -3651 3123|19451 -3767 3123", 
                    "param4": "", 
                    "id": 85
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "10099", 
                    "param1": "20004097|20004098|20004099|20004100|20004101|20004102|20004103|20004104|20004105|20004106", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "123", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "打错了自爆", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "10096", 
                    "param1": "20004097|20004098|20004099|20004100|20004101|20004102|20004103|20004104|20004105|20004106|20004107", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "120272001", 
                    "param2": "1|5", 
                    "param1": "20004102;20004097|20004103;20004098|20004104;20004099|20004105;20004100|20004106;20004101", 
                    "param4": "", 
                    "id": 86
                }, 
                {
                    "delayTime": 13.0, 
                    "param3": "5", 
                    "param2": "20004097|20004098|20004099|20004100|20004101", 
                    "param1": "19400 -8241 3123|22126 -8360 3123|23317 -5962 3146|22040 -3651 3123|19451 -3767 3123", 
                    "param4": "", 
                    "id": 85
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "456", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    15: [
        {
            "title": "完成阶段触发传送回主场景", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "121544001", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 5, 
                    "param1": "5", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "2", 
                    "param3": "24060 -6030 3140", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "3800|2800"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "击杀boss触发传送回主场景", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "121544001", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
                    "param1": "5", 
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
                    "param3": "24060 -6030 3140", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "3800|2800"
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