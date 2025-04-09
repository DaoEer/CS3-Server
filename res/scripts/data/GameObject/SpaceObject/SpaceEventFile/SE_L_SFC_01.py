# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "设置复活点", 
            "describe": "进入副本时，设置复活点", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "-261.895691 55020.691406 912.649170", 
                    "param4": "", 
                    "id": 5
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20008059:1", 
                    "param2": "0 0 90", 
                    "param1": "-379 50760 1426", 
                    "param4": "", 
                    "id": 6
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
            "title": "冰火玄雷灵死，阵心柱光墙死", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20009414|20009415|20009416|20009417|20009418|20009419", 
                    "param4": "", 
                    "id": 130
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "562", 
                    "param4": "", 
                    "id": 170
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 22, 
                    "param1": "20009404|20009405|20009406|20009407", 
                    "param2": "1|1|1|1"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20009404|20009405|20009406|20009407", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "阵心柱死，放吊桥", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "103|108|110", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20009414", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "击杀boss副本通关", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 3
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
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20005497", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ], 
    8: [
        {
            "title": "完成阶段一，销毁光墙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20005525", 
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
            "id": 2
        }
    ], 
    11: [
        {
            "title": "阶段3删除陷阱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "81|82|83|84|85|86", 
                    "param4": "", 
                    "id": 44
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20005521|20005519|20005517", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20008060|20005524", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "5499 22970.007813 2320", 
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
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "阶段2删除光墙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20005523|20008061|20008207", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "40000190|40000191|20008402|20008157|20008401|20008158|20008151", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "-6048 22997 2312", 
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
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "阶段4设置复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "-340 -32920 10039", 
                    "param4": "", 
                    "id": 5
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20008194", 
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
                    "param1": "4", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ], 
    14: [
        {
            "title": "收到冰指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20005499:1", 
                    "param2": "0 0 0", 
                    "param1": "-2970.0 -38860.0 10870.0", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "5499", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005497"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到火指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20005500:1", 
                    "param2": "0 0 0", 
                    "param1": "-3150.0 -44160.0 10870.0", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "5500", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005497"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到玄指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20005501:1", 
                    "param2": "0 0 0", 
                    "param1": "2260.0 -44190.0 10870.0", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "5501", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005497"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到雷指令", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20005502:1", 
                    "param2": "0 0 0", 
                    "param1": "2420.0 -38740.0 10870.0", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "5502", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20005497"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "收到烽火指令播放镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "377", 
                    "param4": "", 
                    "id": 170
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "50000042:1", 
                    "param2": "0 0 0", 
                    "param1": "-16980 -26740 8310", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "50000042:1", 
                    "param2": "0 0 0", 
                    "param1": "-15060 -26740 8310", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "50000042:1", 
                    "param2": "0 0 0", 
                    "param1": "-14850 -28240 7840", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "50000042:1", 
                    "param2": "0 0 0", 
                    "param1": "-14950 -29620 8490", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "195", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "40000195"
                }
            ], 
            "id": 5
        }, 
        {
            "title": "收到1001指令，播放空间动作", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "87|97", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1001", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20008208"
                }
            ], 
            "id": 6
        }, 
        {
            "title": "收到1002指令，播放空间动作", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "89|97", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1002", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20008208"
                }
            ], 
            "id": 7
        }, 
        {
            "title": "收到1003指令，播放空间动作", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "90|96|98", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1003", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20008208"
                }
            ], 
            "id": 8
        }, 
        {
            "title": "收到1011指令，播放空间动作", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "92|97", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1011", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20008062"
                }
            ], 
            "id": 9
        }, 
        {
            "title": "收到1012指令，播放空间动作", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "94|97", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1012", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20008062"
                }
            ], 
            "id": 10
        }, 
        {
            "title": "收到1013指令，播放空间动作", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "95|91|98", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "1013", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20008062"
                }
            ], 
            "id": 11
        }, 
        {
            "title": "收到2001指令，播放空间动作", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "99|109", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2001", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20008401"
                }
            ], 
            "id": 12
        }, 
        {
            "title": "收到2002指令，播放空间动作", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "101|109", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2002", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20008401"
                }
            ], 
            "id": 13
        }, 
        {
            "title": "收到2003指令，播放空间动作", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "102|108|110", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2003", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20008401"
                }
            ], 
            "id": 14
        }, 
        {
            "title": "收到2011指令，播放空间动作", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "104|109", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2011", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20008402"
                }
            ], 
            "id": 15
        }, 
        {
            "title": "收到2012指令，播放空间动作", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "106|109", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2012", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20008402"
                }
            ], 
            "id": 16
        }, 
        {
            "title": "收到2013指令，播放空间动作", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "107|103|110", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2013", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20008402"
                }
            ], 
            "id": 17
        }, 
        {
            "title": "收到8194指令，打开大门", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "112", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "8194", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20008194"
                }
            ], 
            "id": 18
        }, 
        {
            "title": "收到盾牌精英100，刷盾牌和木妖光墙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "40000558:1", 
                    "param2": "0 0 80", 
                    "param1": "5490 9940 4418", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20009380:1", 
                    "param2": "0 0 170.74", 
                    "param1": "7366 -8285 6202", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "100", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20009377"
                }
            ], 
            "id": 19
        }, 
        {
            "title": "收到镜头50401，刷怪哨兵战斗", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20009383:1|20009384:1|20009384:1|20009384:1|20009384:1", 
                    "param2": "0 0 36|0 0 38|0 0 38|0 0 38|0 0 38", 
                    "param1": "15973 1103 5360|15925 764 5360|15745 551 5360|15530 1160 5360|15310 940 5360", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "50402", 
                    "param1": "20009401", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "50401", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 20
        }, 
        {
            "title": "收到水妖死亡115，销毁盾牌", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "40000558", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "115", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20009385"
                }
            ], 
            "id": 21
        }, 
        {
            "title": "收到火妖死亡211，销毁火墙发231", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20009403", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 6.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20009380|20010561", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "231", 
                    "param1": "20009380", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "211", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20009387"
                }
            ], 
            "id": 22
        }, 
        {
            "title": "收到冰灵死311，去冰柱线.冰柱死", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "12151613", 
                    "param1": "20009414", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20009410", 
                    "param4": "", 
                    "id": 130
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "311", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 23
        }, 
        {
            "title": "收到火灵死312，去火柱线.火柱死", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "12151615", 
                    "param1": "20009414", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20009411", 
                    "param4": "", 
                    "id": 130
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "312", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 24
        }, 
        {
            "title": "收到玄灵死313，去玄柱线.玄柱死", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "12151617", 
                    "param1": "20009414", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20009412", 
                    "param4": "", 
                    "id": 130
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "313", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 25
        }, 
        {
            "title": "收到雷灵死314，去雷柱线.雷柱死", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "12151619", 
                    "param1": "20009414", 
                    "param4": "", 
                    "id": 237
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20009413", 
                    "param4": "", 
                    "id": 130
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "314", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 26
        }, 
        {
            "title": "收玩家离开范围514，去光墙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20009419", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "514", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 27
        }, 
        {
            "title": "收到516怪物喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000744", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "516", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 28
        }
    ], 
    15: [
        {
            "title": "播放使用巨弩声音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000556", 
                    "param4": "", 
                    "id": 18
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "15", 
                    "param3": "-260 34538 1219", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "2219|219"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "重置复活点一", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "-16870 -8220 5311", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "6", 
                    "param3": "-14640 5969 5373", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "7373|3373"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "重置复活点二", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "-11630 -4609 5393", 
                    "param4": "", 
                    "id": 5
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "6", 
                    "param3": "-11630 -4609 5373", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "7373|3373"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "重置复活点三", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "-3260 -19390 6252", 
                    "param4": "", 
                    "id": 5
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000583", 
                    "param4": "", 
                    "id": 18
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "15", 
                    "param3": "-3260 -19390 6242", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "8242|4242"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "拾盾提示右侧重置复活点一", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "5313 12039 4454", 
                    "param4": "", 
                    "id": 5
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000757", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "25", 
                    "param3": "5343 10609 4451", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "5000|2000"
                }
            ], 
            "id": 5
        }, 
        {
            "title": "播放哨兵镜头放吊桥右侧复活点二", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "504", 
                    "param4": "", 
                    "id": 170
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "17280 2279 5377", 
                    "param4": "", 
                    "id": 5
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "91|96|98", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "8", 
                    "param3": "17280 2279 5377", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "6377|4377"
                }
            ], 
            "id": 6
        }, 
        {
            "title": "播放水木火妖镜头刷火墙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "503", 
                    "param4": "", 
                    "id": 170
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "20009403:1", 
                    "param2": "0 0 0", 
                    "param1": "9472 140 5463.5", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "20009403:1", 
                    "param2": "0 0 0", 
                    "param1": "9480 -2170.008 5463.5", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "20009385:1", 
                    "param2": "0 0 -90", 
                    "param1": "9529.15 3700.86 5581.2", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "20009386:1", 
                    "param2": "0 0 -90", 
                    "param1": "9079 4001 5414", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "20009386:1", 
                    "param2": "0 0 -90", 
                    "param1": "9079 4321 5407", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "20009386:1", 
                    "param2": "0 0 -90", 
                    "param1": "9909 4001 5414", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "20009386:1", 
                    "param2": "0 0 -90", 
                    "param1": "9909 4311 5407", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "25", 
                    "param3": "11522 1072 5361", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "6377|2000"
                }
            ], 
            "id": 7
        }, 
        {
            "title": "水妖提示右侧重置复活点三", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "9507 1613 5366", 
                    "param4": "", 
                    "id": 5
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000759", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "12", 
                    "param3": "9507 1613 5366", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "7000|2000"
                }
            ], 
            "id": 8
        }, 
        {
            "title": "四灵阵提示右侧重置复活点四", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "5317 -15250 7563", 
                    "param4": "", 
                    "id": 5
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000760", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "18", 
                    "param3": "5317 -15250 7563", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "9000|2000"
                }
            ], 
            "id": 9
        }, 
        {
            "title": "人马阵提示右侧重置复活点五", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "16102 -18125 7495", 
                    "param4": "", 
                    "id": 5
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000761", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "10", 
                    "param3": "16102 -18125 7495", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "9000|2000"
                }
            ], 
            "id": 10
        }, 
        {
            "title": "旋风阵提示右侧重置复活点六", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "16838 -33135 9659", 
                    "param4": "", 
                    "id": 5
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000762", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "10", 
                    "param3": "16838 -33135 9659", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "11000|2000"
                }
            ], 
            "id": 11
        }
    ]
}