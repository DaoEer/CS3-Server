# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "---设置复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0.0 0.0 80.0", 
                    "param1": "-131.9 -4476.8 566.6", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    2: [
        {
            "title": "---倒计时结束，开启副本计时", 
            "describe": "记录t2", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14019101", 
                    "param4": "", 
                    "id": 26
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "30", 
                    "param1": "600", 
                    "param4": "", 
                    "id": 97
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "3", 
                    "param1": "t2", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "t1", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "---副本生命结束，提示通关失败", 
            "describe": "传送玩家出副本，boss下班", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000413", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20012302|20012303|20012312|20012313|20012314|20012315|20012316|20012317|20012318|20012321|20012659|20012660|20012661|20012662|20012658|20012637|20012638", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "789", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "15", 
                    "param4": "", 
                    "id": 325
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
                    "param1": "LoopQuestLife", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    3: [
        {
            "title": "玩家进入副本，墙壁与地面创建", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0.0 0.0 129.3|0.0 0.0 169.6|0.0 0.0 -150.0|0.0 0.0 -110.4|0.0 0.0 -70.1|0.0 0.0 -30.0|0.0 0.0 9.6|0.0 0.0 49.9|0.0 0.0 89.8", 
                    "param2": "-4189.732422 -5280.296387 539.628662|-668.937439 -7355.802734 539.628906|3379.015137 -6665.756348 539.628662|5903.406738 -3563.688965 539.628662|5851.863770 711.334656 539.628906|3338.049072 3703.565430 539.628662|-705.994995 4431.046387 539.628662|-4174.897461 2414.624756 539.628662|-5579.856445 -1426.181030 590.033691", 
                    "param1": "20012640|20012641|20012642|20012643|20012644|20012645|20012646|20012647|20012648", 
                    "param4": "", 
                    "id": 158
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0.0 0.0 9.9|0.0 0.0 9.9|0.0 0.0 9.9|0.0 0.0 9.9|0.0 0.0 9.9|0.0 0.0 9.9|0.0 0.0 9.9|0.0 0.0 9.9|0.0 0.0 9.9", 
                    "param2": "368.818970 -1446.982666 460.000000|368.818970 -1446.982666 460.000000|368.818970 -1446.982666 460.000000|368.818970 -1446.982666 460.000000|368.818970 -1446.982666 460.000000|368.818970 -1446.982666 460.000000|368.818970 -1446.982666 460.000000|368.818970 -1446.982666 460.000000|368.818970 -1446.982666 460.000000", 
                    "param1": "20012649|20012650|20012651|20012652|20012653|20012654|20012655|20012656|20012657", 
                    "param4": "", 
                    "id": 158
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0.0 0.0 -53.0|0.0 0.0 -10.7|0.0 0.0 28.7|0.0 0.0 69.8|0.0 0.0 107.7|0.0 0.0 147.0|0.0 0.0 187.2|0.0 0.0 230.9|0.0 0.0 268.2", 
                    "param2": "-2207.940186 -3549.815918 376.000000|-181.000000 -4820.000000 376.000000|2009.000000 -4414.000000 376.000000|3590.000000 -2570.000000 376.000000|3596.000000 -221.999985 376.000000|2051.000000 1470.000000 376.000000|-233.000000 1913.000000 376.000000|-2335.000000 667.000000 376.000000|-3098.000000 -1409.000000 376.000000", 
                    "param1": "20013170|20013171|20013172|20013173|20013174|20013175|20013176|20013177|20013178", 
                    "param4": "", 
                    "id": 158
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    6: [
        {
            "title": "怪物出生，提醒击杀", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000868", 
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
                    "id": 2, 
                    "param1": "20012637|20012638", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "怪物出生，通知墙壁4321", 
            "describe": "在第一次被选中墙壁的等待刷怪时间内，如果小怪正常出生了，则取消计时，即取消防呆设计的首次刷怪", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "4321", 
                    "param1": "20012640|20012641|20012642|20012643|20012644|20012645|20012646|20012647|20012648", 
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
                    "id": 2, 
                    "param1": "20012637|20012638", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    7: [
        {
            "title": "玩家拥有“前”“阵”，概率给boss上buff", 
            "describe": "皆：玩家的攻击有概率让boss减速。\n阵：玩家的攻击有概率眩晕boss。\n目前设定概率为50%", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0.7|0.7", 
                    "param1": "14033106|14033105", 
                    "param4": "", 
                    "id": 398
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20012639", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    8: [
        {
            "title": "击杀boss，副本通关", 
            "describe": "清场", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "123", 
                    "param4": "", 
                    "id": 3
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14030801|14030901|14030302", 
                    "param4": "", 
                    "id": 26
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20012659|20012660|20012661|20012662|20012658|20012637|20012638|20012639", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000412", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "800", 
                    "param2": "4200", 
                    "param1": "30", 
                    "param4": "2000", 
                    "id": 421
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
            "id": 1
        }
    ], 
    13: [
        {
            "title": "清理副本数据", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14031201|14031301|14031401|14031502|14031601|14031701|14033007", 
                    "param4": "", 
                    "id": 25
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 394
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14019101|14033131|14033132|14033133|14033133|14033134|14033135|14033136|14033137|14033138|14033139", 
                    "param4": "", 
                    "id": 25
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14033101|14033102|14033103|14033104|14033105|14033106|14033107|14033108|14033109|14033505|14033504|14004002", 
                    "param4": "", 
                    "id": 25
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "140379001", 
                    "param4": "", 
                    "id": 16
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    14: [
        {
            "title": "收到卷魄201通知，添加玩家破绽标志", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14033006", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "201", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到某个真言腐化完毕通知，继续腐化下一个", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 190
                }, 
                {
                    "delayTime": 1.5, 
                    "param3": "", 
                    "param2": "700", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "m", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "OCCUPYZY", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到所有真言抢夺完毕通知，通知boss", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "701", 
                    "param1": "20012639|20012659|20012660|20012661|20012662|20012658", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000883", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "OCCUPYEND", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到小怪死亡通知，给玩家增加入道buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14033504", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "200", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "收到“临”，播放提示语音", 
            "describe": "通知陷阱播放全场妖气弥漫效果", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000871|Cy000882", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "222", 
                    "param1": "20012666|20013161", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 190
                }, 
                {
                    "delayTime": 1.5, 
                    "param3": "", 
                    "param2": "700", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 405
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14033021", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "444", 
                    "param1": "20013161", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14033507", 
                    "param1": "20013161", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14033101|14033508", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "LIN", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "收到“兵”，播放提示语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000872|Cy000882", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "222", 
                    "param1": "20012666|20013162", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 190
                }, 
                {
                    "delayTime": 1.5, 
                    "param3": "", 
                    "param2": "700", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 405
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14033021", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "444", 
                    "param1": "20013162", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14033507", 
                    "param1": "20013162", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14033102|14033508", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "BING", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 6
        }, 
        {
            "title": "收到“斗”，播放提示语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000873|Cy000882", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 405
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 190
                }, 
                {
                    "delayTime": 1.5, 
                    "param3": "", 
                    "param2": "700", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "222", 
                    "param1": "20012666|20013163", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14033021", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "444", 
                    "param1": "20013163", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14033507", 
                    "param1": "20013163", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14033103|14033508", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "DOU", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 7
        }, 
        {
            "title": "收到“者”，播放提示语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000874|Cy000882", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 405
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 190
                }, 
                {
                    "delayTime": 1.5, 
                    "param3": "", 
                    "param2": "700", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "222", 
                    "param1": "20012666|20013164", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14033021", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "444", 
                    "param1": "20013164", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14033507", 
                    "param1": "20013164", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14033104|14033508", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "ZHE", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 8
        }, 
        {
            "title": "收到“皆”，播放提示语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000875|Cy000882", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 405
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 190
                }, 
                {
                    "delayTime": 1.5, 
                    "param3": "", 
                    "param2": "700", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "222", 
                    "param1": "20012666|20013165", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14033021", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "444", 
                    "param1": "20013165", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14033507", 
                    "param1": "20013165", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14033135|14033508", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "JIE", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 9
        }, 
        {
            "title": "收到“阵”，播放提示语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000876|Cy000882", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 405
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 190
                }, 
                {
                    "delayTime": 1.5, 
                    "param3": "", 
                    "param2": "700", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "222", 
                    "param1": "20012666|20013166", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14033021", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "444", 
                    "param1": "20013166", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14033507", 
                    "param1": "20013166", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14033136|14033508", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "ZHEN", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 10
        }, 
        {
            "title": "收到“列”，播放提示语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000877|Cy000882", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 405
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 190
                }, 
                {
                    "delayTime": 1.5, 
                    "param3": "", 
                    "param2": "700", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "222", 
                    "param1": "20012666|20013167", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14033021", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "444", 
                    "param1": "20013167", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14033507", 
                    "param1": "20013167", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14033107|14033508", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "LIE", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 11
        }, 
        {
            "title": "收到“前”，播放提示语音，通知虚影标记k2", 
            "describe": "通知虚影加上被玩家占领的标记，用于释放12s预警的爆炸技能。", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000878|Cy000882", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "333", 
                    "param1": "20013161|20013162|20013163|20013164|20013165|20013166|20013167|20013168|20013169", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 405
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 190
                }, 
                {
                    "delayTime": 1.5, 
                    "param3": "", 
                    "param2": "700", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "222", 
                    "param1": "20012666|20013168", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14033021", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "444", 
                    "param1": "20013168", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14033507", 
                    "param1": "20013168", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14033108|14033508", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "QIAN", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 12
        }, 
        {
            "title": "收到“行”，播放提示语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000879|Cy000882", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 405
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 190
                }, 
                {
                    "delayTime": 1.5, 
                    "param3": "", 
                    "param2": "700", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "222", 
                    "param1": "20012666|20013169", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "14033021", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.5, 
                    "param3": "", 
                    "param2": "444", 
                    "param1": "20013169", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.5, 
                    "param3": "", 
                    "param2": "14033507", 
                    "param1": "20013169", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14033109|14033508", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "XING", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 13
        }, 
        {
            "title": "收到陷阱通知，关闭妖气入体", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 405
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "223", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 14
        }, 
        {
            "title": "收到踩在虚影“临”的通知，中断对应爆炸", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0", 
                    "param1": "20013161|20013162|20013163|20013164|20013165|20013166|20013167|20013168|20013169", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 15
        }, 
        {
            "title": "收到踩在虚影“兵”的通知，中断对应爆炸", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20013161|20013162|20013163|20013164|20013165|20013166|20013167|20013168|20013169", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 16
        }, 
        {
            "title": "收到踩在虚影“斗”的通知，中断对应爆炸", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20013161|20013162|20013163|20013164|20013165|20013166|20013167|20013168|20013169", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 17
        }, 
        {
            "title": "收到踩在虚影“者”的通知，中断对应爆炸", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "3", 
                    "param1": "20013161|20013162|20013163|20013164|20013165|20013166|20013167|20013168|20013169", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 18
        }, 
        {
            "title": "收到踩在虚影“皆”的通知，中断对应爆炸", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "4", 
                    "param1": "20013161|20013162|20013163|20013164|20013165|20013166|20013167|20013168|20013169", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 19
        }, 
        {
            "title": "收到踩在虚影“阵”的通知，中断对应爆炸", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "5", 
                    "param1": "20013161|20013162|20013163|20013164|20013165|20013166|20013167|20013168|20013169", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "5", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 20
        }, 
        {
            "title": "收到踩在虚影“列”的通知，中断对应爆炸", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "6", 
                    "param1": "20013161|20013162|20013163|20013164|20013165|20013166|20013167|20013168|20013169", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "6", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 21
        }, 
        {
            "title": "收到踩在虚影“前”的通知，中断对应爆炸", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "7", 
                    "param1": "20013161|20013162|20013163|20013164|20013165|20013166|20013167|20013168|20013169", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "7", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 22
        }, 
        {
            "title": "收到踩在虚影“行”的通知，中断对应爆炸", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "8", 
                    "param1": "20013161|20013162|20013163|20013164|20013165|20013166|20013167|20013168|20013169", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "8", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 23
        }, 
        {
            "title": "收到201通知，获得入道buff提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000870", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "201", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 24
        }, 
        {
            "title": "收到真言腐化完毕通知，提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000869", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "789", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 25
        }, 
        {
            "title": "收到开始释放爆炸通知，播放语音提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000881", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "sound", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 26
        }, 
        {
            "title": "收到boss占领“临”，播放提示语音", 
            "describe": "通知陷阱播放全场妖气弥漫效果", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000903", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "z", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "11", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 27
        }, 
        {
            "title": "收到boss占领“兵”，播放提示语音", 
            "describe": "通知陷阱播放全场妖气弥漫效果", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000904", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "z", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "12", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 28
        }, 
        {
            "title": "收到boss占领“斗”，播放提示语音", 
            "describe": "通知陷阱播放全场妖气弥漫效果", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000905", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "z", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "13", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 29
        }, 
        {
            "title": "收到boss占领“者”，播放提示语音", 
            "describe": "通知陷阱播放全场妖气弥漫效果", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000906", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "z", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "14", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 30
        }, 
        {
            "title": "收到boss占领“皆”，播放提示语音", 
            "describe": "通知陷阱播放全场妖气弥漫效果", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000907", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "z", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "15", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 31
        }, 
        {
            "title": "收到boss占领“阵”，播放提示语音", 
            "describe": "通知陷阱播放全场妖气弥漫效果", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000908", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "z", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "16", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 32
        }, 
        {
            "title": "收到boss占领“列”，播放提示语音", 
            "describe": "通知陷阱播放全场妖气弥漫效果", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000909", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "z", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "17", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 33
        }, 
        {
            "title": "收到boss占领“前”，播放提示语音", 
            "describe": "通知陷阱播放全场妖气弥漫效果", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000910", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "z", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "18", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 34
        }, 
        {
            "title": "收到boss占领“行”，播放提示语音", 
            "describe": "通知陷阱播放全场妖气弥漫效果", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000911", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "z", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "19", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 35
        }
    ], 
    17: [
        {
            "title": "---重置副本", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14031201|14031301|14031401|14031502|14031601|14031701", 
                    "param4": "", 
                    "id": 26
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "123", 
                    "param4": "", 
                    "id": 4
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    19: [
        {
            "title": "移除buff", 
            "describe": "玩家在副本内死亡，销毁存在的怪物，传送玩家出副本", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14031201|14031301|14031401|14031502|14031601|14031701", 
                    "param4": "", 
                    "id": 26
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 21, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    21: [
        {
            "title": "玩家进入，开场白，倒计时", 
            "describe": "禁止骑宠", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "12", 
                    "param1": "t1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "12", 
                    "param4": "", 
                    "id": 46
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14019101|14004002", 
                    "param4": "", 
                    "id": 34
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Cy000865", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "初始化真言", 
            "describe": "初始化：默认三个被boss占领的真言；每块真言腐化时间60s", 
            "actions": [
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "60", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 395
                }, 
                {
                    "delayTime": 11.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 190
                }, 
                {
                    "delayTime": 12.0, 
                    "param3": "", 
                    "param2": "1700", 
                    "param1": "20012639", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "1", 
                    "param2": "100", 
                    "param1": "z", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }
    ]
}