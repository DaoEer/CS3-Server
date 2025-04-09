# -*- coding: utf-8 -*-
Datas = {
    2: [
        {
            "title": "t1到达，循环浪/水球", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "103", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "104", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "105", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "106", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "k4", 
                    "param2": "0"
                }
            ], 
            "canLoop": 1, 
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
        }
    ], 
    3: [
        {
            "title": "玩家进入副本，刷第3批小怪/界面提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q021126", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "加载门窗/初始化计数", 
            "describe": "k1：船舫1，k2：船舫2，k3：船舫3，k4：水龙大阵，k5：区域2玩家状态监控", 
            "actions": [
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "100", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0", 
                    "param1": "k4", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0", 
                    "param1": "k5", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    5: [
        {
            "title": "第6批死亡，开门：579/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "579", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "6", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "第7批死亡，对40000533|40000534|40000535发送666", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "666", 
                    "param1": "40000533|40000534", 
                    "param4": "", 
                    "id": 199
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "7", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "第8批死亡，开门：608/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "608", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "8", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }, 
        {
            "title": "阵眼死亡，播放镜头466/大阵关闭/刷出腾龙2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k4", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "20000141|20000142|20000143", 
                    "param1": "101", 
                    "param4": "", 
                    "id": 14
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "30000692", 
                    "param1": "102", 
                    "param4": "", 
                    "id": 14
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "30000697|30000698|30000699", 
                    "param1": "103", 
                    "param4": "", 
                    "id": 14
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "20000144", 
                    "param1": "104", 
                    "param4": "", 
                    "id": 14
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "20000144", 
                    "param1": "105", 
                    "param4": "", 
                    "id": 14
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "20000144", 
                    "param1": "106", 
                    "param4": "", 
                    "id": 14
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "t1", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 125
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "107", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 3.09999990463, 
                    "param3": "", 
                    "param2": "1|2", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 209
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11049401|11049402", 
                    "param4": "", 
                    "id": 26
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "623|624|625|636", 
                    "param4": "", 
                    "id": 208
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000466", 
                    "param4": "", 
                    "id": 17
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "-1", 
                    "param1": "k5", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20000056", 
                    "param2": ""
                }
            ], 
            "id": 4
        }
    ], 
    8: [
        {
            "title": "阶段2完成，播放镜头464", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000464", 
                    "param4": "", 
                    "id": 17
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
            "id": 1
        }
    ], 
    14: [
        {
            "title": "收到40000465，开窗：535/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "535", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000465", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到40000466，开窗：536/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "536", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000466", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到40000467，开窗：537/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "537", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000467", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到40000468，开窗：538/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "538", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000468", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "收到40000469，开窗：539/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "539", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000469", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "收到40000470，开窗：540/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "540", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000470", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 6
        }, 
        {
            "title": "收到40000471，开窗：541/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "541", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000471", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 7
        }, 
        {
            "title": "收到40000472，开窗：542/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "542", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000472", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 8
        }, 
        {
            "title": "收到40000473，开窗：543/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "543", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000473", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 9
        }, 
        {
            "title": "收到40000474，开窗：544/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "544", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000474", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 10
        }, 
        {
            "title": "收到40000475，开窗：545/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "545", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000475", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 11
        }, 
        {
            "title": "收到40000476，开窗：546/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "546", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000476", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 12
        }, 
        {
            "title": "收到40000477，开窗：547/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "547", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000477", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 13
        }, 
        {
            "title": "收到40000478，开窗：548/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "548", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000478", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 14
        }, 
        {
            "title": "收到40000479，开窗：549/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "549", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000479", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 15
        }, 
        {
            "title": "收到40000480，开窗：550/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "550", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000480", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 16
        }, 
        {
            "title": "收到40000481，开窗：551/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "551", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000481", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 17
        }, 
        {
            "title": "收到40000482，开窗：552/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "552", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000482", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 18
        }, 
        {
            "title": "收到40000483，开窗：553/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "553", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000483", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 19
        }, 
        {
            "title": "收到40000484，开窗：554/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "554", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000484", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 20
        }, 
        {
            "title": "收到40000485，开窗：555/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "555", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000485", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 21
        }, 
        {
            "title": "收到40000486，开窗：556/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "556", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000486", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 22
        }, 
        {
            "title": "收到40000487，开窗：557/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "557", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000487", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 23
        }, 
        {
            "title": "收到40000488，开窗：558/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "558", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000488", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 24
        }, 
        {
            "title": "收到40000489，刷新第7批", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "7", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q021138", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000489", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 25
        }, 
        {
            "title": "收到40000490，开窗：560/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "560", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000490", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 26
        }, 
        {
            "title": "收到40000491，开窗：561/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "561", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000491", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 27
        }, 
        {
            "title": "收到40000492，开窗：562/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "562", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000492", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 28
        }, 
        {
            "title": "收到40000493，开窗：563/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "563", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000493", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 29
        }, 
        {
            "title": "收到40000494，开窗：564/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "564", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000494", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 30
        }, 
        {
            "title": "收到40000495，开窗：565/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "565", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000495", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 31
        }, 
        {
            "title": "收到40000496，开窗：566/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "566", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000496", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 32
        }, 
        {
            "title": "收到40000497，开窗：567/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "567", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000497", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 33
        }, 
        {
            "title": "收到40000498，开窗：568/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "568", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000498", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 34
        }, 
        {
            "title": "收到40000499，开窗：569/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "569", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000499", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 35
        }, 
        {
            "title": "收到40000500，开窗：570/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "570", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000500", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 36
        }, 
        {
            "title": "收到40000501，开窗：571/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "571", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000501", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 37
        }, 
        {
            "title": "收到40000502，开窗：572/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "572", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000502", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 38
        }, 
        {
            "title": "收到40000503，开窗：573/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "573", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000503", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 39
        }, 
        {
            "title": "收到40000504，开窗：574/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "574", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000504", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 40
        }, 
        {
            "title": "收到40000505，开窗：575/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "575", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000505", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 41
        }, 
        {
            "title": "收到40000506，开窗：576/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "576", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000506", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 42
        }, 
        {
            "title": "收到40000507，开门：577/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "577", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000507", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 43
        }, 
        {
            "title": "收到40000508，开门：578/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "578", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000508", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 44
        }, 
        {
            "title": "收到40000509，刷新第6批", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "6", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q021137", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000509", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 45
        }, 
        {
            "title": "收到40000510，开门：580/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "580", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000510", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 46
        }, 
        {
            "title": "收到40000511，开门：581/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "581", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000511", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 47
        }, 
        {
            "title": "收到40000512，开门：582/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "582", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000512", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 48
        }, 
        {
            "title": "收到40000513，开门：583/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "583", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000513", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 49
        }, 
        {
            "title": "收到40000514，开门：584/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "584", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000514", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 50
        }, 
        {
            "title": "收到40000515，开门：585/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "585", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000515", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 51
        }, 
        {
            "title": "收到40000516，开门：586/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "586", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000516", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 52
        }, 
        {
            "title": "收到40000517，开门：587/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "587", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000517", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 53
        }, 
        {
            "title": "收到40000518，开门：588/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "588", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000518", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 54
        }, 
        {
            "title": "收到40000519，开门：589/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "589", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000519", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 55
        }, 
        {
            "title": "收到40000520，开门：590/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "590", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000520", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 56
        }, 
        {
            "title": "收到40000521，开门：591/k1+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "591", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000521", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 57
        }, 
        {
            "title": "收到40000522，开门：592/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "592", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000522", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 58
        }, 
        {
            "title": "收到40000523，开门：593/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "593", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000523", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 59
        }, 
        {
            "title": "收到40000524，开门：594/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "594", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000524", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 60
        }, 
        {
            "title": "收到40000525，开门：595/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "595", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000525", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 61
        }, 
        {
            "title": "收到40000526，开门：596/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "596", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000526", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 62
        }, 
        {
            "title": "收到40000527，开门：597/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "597", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000527", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 63
        }, 
        {
            "title": "收到40000528，开门：598/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "598", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000528", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 64
        }, 
        {
            "title": "收到40000529，开门：599/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "599", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000529", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 65
        }, 
        {
            "title": "收到40000530，开门：600/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "600", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000530", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 66
        }, 
        {
            "title": "收到40000531，开门：601/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "601", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000531", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 67
        }, 
        {
            "title": "收到40000532，开门：602/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "602", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000532", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 68
        }, 
        {
            "title": "收到40000533，开门：603/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "603", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000533", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 69
        }, 
        {
            "title": "收到40000534，开门：604/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "604", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000534", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 70
        }, 
        {
            "title": "收到40000535，开门：605/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "605", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000535", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 71
        }, 
        {
            "title": "收到40000536，开门：606/k2+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "606", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000536", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 72
        }, 
        {
            "title": "收到40000537，开门：607/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "607", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000537", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 73
        }, 
        {
            "title": "收到40000538，开门：608/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "608", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000538", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 74
        }, 
        {
            "title": "收到40000539，开门：609/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "609", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000539", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 75
        }, 
        {
            "title": "收到40000540，开门：610/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "610", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000540", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 76
        }, 
        {
            "title": "收到40000541，开门：611/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "611", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000541", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 77
        }, 
        {
            "title": "收到40000542，开门：612/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "612", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000542", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 78
        }, 
        {
            "title": "收到4000054301，开门：613/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "613", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4000054301", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 79
        }, 
        {
            "title": "收到4000054302，关门/召唤第8批/开阻挡墙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "613", 
                    "param4": "", 
                    "id": 208
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "632", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "20008205:1", 
                    "param2": "0 0 -25", 
                    "param1": "46808.3 45285.7 -15616.9", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "8", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q021127", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4000054302", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 80
        }, 
        {
            "title": "收到40000544，开门：614/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "614", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000544", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 81
        }, 
        {
            "title": "收到40000545，开门：615/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "615", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000545", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 82
        }, 
        {
            "title": "收到40000546，开门：616/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "616", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000546", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 83
        }, 
        {
            "title": "收到40000547，开门：617/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "617", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000547", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 84
        }, 
        {
            "title": "收到40000548，开门：618/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "618", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000548", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 85
        }, 
        {
            "title": "收到40000549，开门：619/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "619", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000549", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 86
        }, 
        {
            "title": "收到40000550，开门：620/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "620", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000550", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 87
        }, 
        {
            "title": "收到40000551，开门：621/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "621", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000551", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 88
        }, 
        {
            "title": "收到40000552，开门：629/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "629", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000552", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 89
        }, 
        {
            "title": "收到40000553，开门：630/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "630", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000553", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 90
        }, 
        {
            "title": "收到40000554，开门：631/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "631", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k3", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "40000554", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 91
        }, 
        {
            "title": "收到20000054，播放镜头465", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "200.0", 
                    "param4": "", 
                    "id": 281
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000465", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "20000054", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 92
        }, 
        {
            "title": "收到2000005501，完成任务", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "4", 
                    "param1": "20101144", 
                    "param4": "", 
                    "id": 2
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 210
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2000005501", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 93
        }, 
        {
            "title": "收到2000005502，传送出位面", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "L_TJGJD", 
                    "param4": "", 
                    "id": 20
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "2000005502", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 94
        }, 
        {
            "title": "收到464发送的12345，刷Boss1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "12345", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "464"
                }
            ], 
            "id": 95
        }, 
        {
            "title": "收到465发送的12345，开启水龙大阵", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "623|624|625|636", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "101", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "102", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "103", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "104", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "105", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "106", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "1", 
                    "param2": "5", 
                    "param1": "t1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 124
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11049301", 
                    "param4": "", 
                    "id": 34
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q021136", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1|2", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 209
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11049401", 
                    "param4": "", 
                    "id": 34
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k5", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "12345", 
                    "id": 9, 
                    "param1": "STORY", 
                    "param2": "465"
                }
            ], 
            "id": 96
        }
    ], 
    16: [
        {
            "title": "k1＞0/k2＞0,召唤阵眼", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20000056:1", 
                    "param2": "0 0 65.5", 
                    "param1": "45155.8 43478.2 -14494.3", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 26, 
                    "param1": "k1", 
                    "param2": "0"
                }, 
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 26, 
                    "param1": "k2", 
                    "param2": "0"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "k1＞0/k3＞0,召唤阵眼", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20000056:1", 
                    "param2": "0 0 -48", 
                    "param1": "50140.9 32203.6 -15633.0", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 26, 
                    "param1": "k1", 
                    "param2": "0"
                }, 
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 26, 
                    "param1": "k3", 
                    "param2": "0"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "k2＞0/k3＞0,召唤阵眼", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20000056:1", 
                    "param2": "0 0 3.5", 
                    "param1": "33034.0 32112.6 -14489.2", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 26, 
                    "param1": "k2", 
                    "param2": "0"
                }, 
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 26, 
                    "param1": "k3", 
                    "param2": "0"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }
    ], 
    24: [
        {
            "title": "玩家战斗/k5=1，取消大阵音乐", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11049401", 
                    "param4": "", 
                    "id": 25
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11049402", 
                    "param4": "", 
                    "id": 33
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "k5", 
                    "param2": "1"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 33, 
                    "param1": "3", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "玩家战斗/k5=1，开启大阵音乐", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11049402", 
                    "param4": "", 
                    "id": 25
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11049401", 
                    "param4": "", 
                    "id": 33
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "k5", 
                    "param2": "1"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 33, 
                    "param1": "1", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ]
}