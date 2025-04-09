# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "设置复活点", 
            "describe": "设置复活点", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 -20", 
                    "param1": "-5290 2690 2635", 
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
            "title": "tick1触发", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "50", 
                    "param2": "-489.987183 779.999146 2634.774414", 
                    "param1": "30000348", 
                    "param4": "30", 
                    "id": 123
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "tick1", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "tick2触发", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "25", 
                    "param2": "-489.987183 779.999146 2634.774414", 
                    "param1": "30000348", 
                    "param4": "5", 
                    "id": 123
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "tick2", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "tick3触发", 
            "describe": "随机15个凹槽", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "15", 
                    "param2": "33", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 131
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "tick3", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "喊话提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000324", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 15.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000342", 
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
                    "param1": "tick1", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "火烧Buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12077901", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "tick1", 
                    "param2": ""
                }
            ], 
            "id": 5
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
            "id": 6
        }
    ], 
    3: [
        {
            "title": "玩家进入", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 122
                }, 
                {
                    "delayTime": 35.0, 
                    "param3": "1", 
                    "param2": "40", 
                    "param1": "tick3", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 26.0, 
                    "param3": "15", 
                    "param2": "33", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 131
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
            "title": "boss死亡副本通关", 
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
                    "param3": "40000556:1", 
                    "param2": "0 0 -21.7", 
                    "param1": "4303 -1107 2701", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20008616:1", 
                    "param2": "0 0 -21.7", 
                    "param1": "3314 -728 2682", 
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
                    "param1": "20005788", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    7: [
        {
            "title": "血量改变", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "20005785", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 108
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 6, 
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
                    "param1": "20005785", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    8: [
        {
            "title": "1阶段完成发送指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "tick1", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "tick2", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "666", 
                    "param1": "20005785|20005788|20005787", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "261", 
                    "param1": "20005785", 
                    "param4": "", 
                    "id": 7
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000330", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12077901", 
                    "param4": "", 
                    "id": 26
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20005786", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20005785", 
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
                    "id": 4, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "2阶段完成播放镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "888", 
                    "param1": "20005787", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "tick3", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40000120:1", 
                    "param2": "0 0 0", 
                    "param1": "-520.0 800.0 3075", 
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
            "id": 2
        }, 
        {
            "title": "副本通关", 
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
                    "param3": "40000556:1", 
                    "param2": "0 0 -21.7", 
                    "param1": "4303 -1107 2701", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20008616:1", 
                    "param2": "0 0 -21.7", 
                    "param1": "3314 -728 2682", 
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
        }
    ], 
    13: [
        {
            "title": "清除BUFF", 
            "describe": "清除BUFF", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12077901", 
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
    14: [
        {
            "title": "开始中央倒计时", 
            "describe": "通知副本，倒计时", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 46
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000328", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "260", 
                    "param1": "20005785", 
                    "param4": "", 
                    "id": 7
                }, 
                {
                    "delayTime": 12.0, 
                    "param3": "", 
                    "param2": "20005785", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 108
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "321", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005785"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "开始填充/tick1/2计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "10", 
                    "param1": "tick1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "20", 
                    "param1": "tick2", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 121
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "123", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005785"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "计数增加", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "s", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "666", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005786"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "关闭血条界面", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "20005785", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 108
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "456", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005788"
                }
            ], 
            "id": 4
        }
    ], 
    15: [
        {
            "title": "触发传送回主场景", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "121544005", 
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
                    "param3": "3314 -728 2682", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "3100|2400"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "只杀boss触发传送回主场景", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "121544005", 
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
                    "param3": "3314 -728 2682", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "3100|2400"
                }
            ], 
            "id": 2
        }
    ], 
    16: [
        {
            "title": "副本阶段计数10", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000325", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 10.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000329", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "s", 
                    "param2": "10"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "副本阶段计数20", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000326", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "s", 
                    "param2": "20"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "副本阶段计数01", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000343", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 19, 
                    "param1": "s", 
                    "param2": "1"
                }
            ], 
            "id": 3
        }
    ], 
    17: [
        {
            "title": "清除BUFF", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12077901", 
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