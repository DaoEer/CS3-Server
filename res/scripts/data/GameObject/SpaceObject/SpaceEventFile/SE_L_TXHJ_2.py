# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "副本初始化，开启阶段1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 1
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
            "title": "t1=6，循环风", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "100", 
                    "param4": "30000547:1", 
                    "id": 28
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "30000754", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11037701", 
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
            "title": "初始化k1,k2,k3，k4", 
            "describe": "", 
            "actions": [
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
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "初始化t1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "6", 
                    "param1": "t1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "100", 
                    "param4": "30000547:1", 
                    "id": 28
                }, 
                {
                    "delayTime": 4.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "30000754", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }, 
        {
            "title": "刷新加速球", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "101", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 3
        }, 
        {
            "title": "请输入标题", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20101551", 
                    "param4": "", 
                    "id": 2
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 4
        }
    ], 
    5: [
        {
            "title": "第2批石像怪全部死亡，对第3批石像怪发送1(准备解除石化)", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20010800|20010801", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "2", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "第7批怪全部死亡，开门224/开门226/销毁阻挡墙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.10000000149, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "224|226", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "224|225|226|227", 
                    "param4": "", 
                    "id": 208
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20010805", 
                    "param4": "", 
                    "id": 9
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
            "title": "第8批怪全部死亡，开门224/开门226/销毁阻挡墙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.10000000149, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "224|226", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "224|225|226|227", 
                    "param4": "", 
                    "id": 208
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20010805", 
                    "param4": "", 
                    "id": 9
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
            "title": "第9批怪全部死亡，开门233/开门235/销毁阻挡墙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "234|236", 
                    "param4": "", 
                    "id": 208
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "233|235", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20010805", 
                    "param4": "", 
                    "id": 9
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
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "9", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 4
        }, 
        {
            "title": "第10批怪全部死亡，开门233/开门235/销毁阻挡墙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "234|236", 
                    "param4": "", 
                    "id": 208
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "233|235", 
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
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20010805", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "10", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 5
        }, 
        {
            "title": "第10批怪全部死亡，开门220/销毁阻挡墙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "220|221", 
                    "param4": "", 
                    "id": 208
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "220", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20010805", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "11", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 6
        }
    ], 
    8: [
        {
            "title": "阶段2完成，开启阶段3", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 1
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
        }, 
        {
            "title": "阶段1完成，开启阶段2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 1
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
            "id": 2
        }, 
        {
            "title": "阶段3完成，开启阶段4", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 1
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
            "id": 3
        }, 
        {
            "title": "阶段4完成，开启阶段5", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 1
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
            "id": 4
        }, 
        {
            "title": "阶段5完成，开启阶段6", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "6", 
                    "param4": "", 
                    "id": 1
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
            "id": 5
        }, 
        {
            "title": "阶段6完成，开启阶段7", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "7", 
                    "param4": "", 
                    "id": 1
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 4, 
                    "param1": "6", 
                    "param2": ""
                }
            ], 
            "id": 6
        }
    ], 
    14: [
        {
            "title": "收到镜头410的12345，刷出心魔真身", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "6", 
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
                    "param2": "628"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "收到太古心魔1的3，播放镜头411/完成阶段4", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000527", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "3", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20010795"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "收到镜头412的12345，播放旁边提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q012055", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "180", 
                    "param1": "t2", 
                    "param4": "", 
                    "id": 12
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
                    "param2": "527"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "收到石像的4，石像喊话", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q012036", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "4", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "收到101，开门168", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "168", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "101", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000598"
                }
            ], 
            "id": 5
        }, 
        {
            "title": "收到102，开窗169", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "169", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "102", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000599"
                }
            ], 
            "id": 6
        }, 
        {
            "title": "收到103，开窗170", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "170", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "103", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000600"
                }
            ], 
            "id": 7
        }, 
        {
            "title": "收到104，开窗171", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "171", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "104", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000601"
                }
            ], 
            "id": 8
        }, 
        {
            "title": "收到105，开窗172", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "172", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "105", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000602"
                }
            ], 
            "id": 9
        }, 
        {
            "title": "收到106，开窗173", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "173", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "106", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000603"
                }
            ], 
            "id": 10
        }, 
        {
            "title": "收到107，开窗174", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "174", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "107", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000604"
                }
            ], 
            "id": 11
        }, 
        {
            "title": "收到108，开窗175", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "175", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "108", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000605"
                }
            ], 
            "id": 12
        }, 
        {
            "title": "收到109，开窗176", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "176", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "109", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000606"
                }
            ], 
            "id": 13
        }, 
        {
            "title": "收到110，开窗177", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "177", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "110", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000607"
                }
            ], 
            "id": 14
        }, 
        {
            "title": "收到111，开门178", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "178", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "111", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000608"
                }
            ], 
            "id": 15
        }, 
        {
            "title": "收到112，开窗179", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "179", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "112", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000609"
                }
            ], 
            "id": 16
        }, 
        {
            "title": "收到113，开窗180", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "180", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "113", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000610"
                }
            ], 
            "id": 17
        }, 
        {
            "title": "收到114，开窗181", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "181", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "114", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000611"
                }
            ], 
            "id": 18
        }, 
        {
            "title": "收到115，开窗182", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "182", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "115", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000612"
                }
            ], 
            "id": 19
        }, 
        {
            "title": "收到116，开窗183", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "183", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "116", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000613"
                }
            ], 
            "id": 20
        }, 
        {
            "title": "收到117，开窗184", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "184", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "117", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000614"
                }
            ], 
            "id": 21
        }, 
        {
            "title": "收到118，开窗185", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "185", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "118", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000615"
                }
            ], 
            "id": 22
        }, 
        {
            "title": "收到119，开窗186", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "186", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "119", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000616"
                }
            ], 
            "id": 23
        }, 
        {
            "title": "收到120，开窗187", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "187", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "120", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000617"
                }
            ], 
            "id": 24
        }, 
        {
            "title": "收到121，开窗188", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "188", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "121", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000618"
                }
            ], 
            "id": 25
        }, 
        {
            "title": "收到201，开门189", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "189", 
                    "param4": "", 
                    "id": 207
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
                    "param2": "40000619"
                }
            ], 
            "id": 26
        }, 
        {
            "title": "收到202，开门190", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "190", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "202", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000620"
                }
            ], 
            "id": 27
        }, 
        {
            "title": "收到203，开窗191", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "191", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "203", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000621"
                }
            ], 
            "id": 28
        }, 
        {
            "title": "收到204，开窗192", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "192", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "204", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000622"
                }
            ], 
            "id": 29
        }, 
        {
            "title": "收到205，开窗193", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "193", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "205", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000623"
                }
            ], 
            "id": 30
        }, 
        {
            "title": "收到206，开窗194", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "194", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "206", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000624"
                }
            ], 
            "id": 31
        }, 
        {
            "title": "收到207，开窗195", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "195", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "207", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000625"
                }
            ], 
            "id": 32
        }, 
        {
            "title": "收到208，开窗196", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "196", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "208", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000626"
                }
            ], 
            "id": 33
        }, 
        {
            "title": "收到209，开窗197", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "197", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "209", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000627"
                }
            ], 
            "id": 34
        }, 
        {
            "title": "收到210，开窗198", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "198", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "210", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000628"
                }
            ], 
            "id": 35
        }, 
        {
            "title": "收到211，开窗199", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "199", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "211", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000629"
                }
            ], 
            "id": 36
        }, 
        {
            "title": "收到212，开门200", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "200", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "212", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000630"
                }
            ], 
            "id": 37
        }, 
        {
            "title": "收到213，开窗201", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "201", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "213", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000631"
                }
            ], 
            "id": 38
        }, 
        {
            "title": "收到214，开窗202", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "202", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "214", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000632"
                }
            ], 
            "id": 39
        }, 
        {
            "title": "收到215，开窗203", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "203", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "215", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000633"
                }
            ], 
            "id": 40
        }, 
        {
            "title": "收到216，开窗204", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "204", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "216", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000634"
                }
            ], 
            "id": 41
        }, 
        {
            "title": "收到217，开窗205", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "205", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "217", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000596"
                }
            ], 
            "id": 42
        }, 
        {
            "title": "收到218，开窗206", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "206", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "218", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000635"
                }
            ], 
            "id": 43
        }, 
        {
            "title": "收到219，开窗207", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "207", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "219", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000636"
                }
            ], 
            "id": 44
        }, 
        {
            "title": "收到220，开窗208", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "208", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "220", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000637"
                }
            ], 
            "id": 45
        }, 
        {
            "title": "收到221，开窗209", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "209", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "221", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000638"
                }
            ], 
            "id": 46
        }, 
        {
            "title": "收到222，开窗210", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "210", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "222", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000639"
                }
            ], 
            "id": 47
        }, 
        {
            "title": "收到223，开门211", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "211", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "223", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000640"
                }
            ], 
            "id": 48
        }, 
        {
            "title": "收到224，开门212", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "212", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "224", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000641"
                }
            ], 
            "id": 49
        }, 
        {
            "title": "收到225，开门213", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "213", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "225", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000642"
                }
            ], 
            "id": 50
        }, 
        {
            "title": "收到226，开门214", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "214", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "226", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000643"
                }
            ], 
            "id": 51
        }, 
        {
            "title": "收到227，开门215", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "215", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "227", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000644"
                }
            ], 
            "id": 52
        }, 
        {
            "title": "收到228，开门216", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "216", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "228", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000645"
                }
            ], 
            "id": 53
        }, 
        {
            "title": "收到229，开门217", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "217", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "229", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000646"
                }
            ], 
            "id": 54
        }, 
        {
            "title": "收到230，开门218", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "218", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "230", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000647"
                }
            ], 
            "id": 55
        }, 
        {
            "title": "收到231，开门219", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "219", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "231", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000648"
                }
            ], 
            "id": 56
        }, 
        {
            "title": "收到232，开门220", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "220", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "232", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000593"
                }
            ], 
            "id": 57
        }, 
        {
            "title": "收到233，关门221/阻挡墙/刷新第11批", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "221", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20010805:1", 
                    "param2": "0 0 155", 
                    "param1": "-73502.66 -71325.48 17527.00", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q012050", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "233", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000593"
                }
            ], 
            "id": 58
        }, 
        {
            "title": "收到234/k1<2，k1+1/开门224", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "224", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 26, 
                    "param1": "k1", 
                    "param2": "2"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "234", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000594"
                }
            ], 
            "id": 59
        }, 
        {
            "title": "收到235/k2<2，k2+1/开门225", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "226", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "1", 
                    "id": 26, 
                    "param1": "k2", 
                    "param2": "2"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "235", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000595"
                }
            ], 
            "id": 60
        }, 
        {
            "title": "收到236/k1=1/k2=1,关门225/关门227/刷新第7批怪/阻挡墙/k1+2/k2+2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "225|227", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "7", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20010805:1", 
                    "param2": "0 0 15", 
                    "param1": "-37961.9 -46729.9 17192.0", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q012048", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "k1", 
                    "param2": "1"
                }, 
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "k2", 
                    "param2": "1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "236", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000594"
                }
            ], 
            "id": 61
        }, 
        {
            "title": "收到236/k1=1/k2=0,关门225/刷新第7批怪/阻挡墙/k1+2/k2+2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "225", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "7", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20010805:1", 
                    "param2": "0 0 15", 
                    "param1": "-37961.9 -46729.9 17192.0", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q012048", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "k1", 
                    "param2": "1"
                }, 
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "k2", 
                    "param2": "0"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "236", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000594"
                }
            ], 
            "id": 62
        }, 
        {
            "title": "收到237/k1=1/k2=1,关门225/关门227/刷新第8批怪/k1+2/k2+2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "225|227", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "8", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20010805:1", 
                    "param2": "0 0 105", 
                    "param1": "-36772.3 -47282.6 17192.0", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q012048", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "k1", 
                    "param2": "1"
                }, 
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "k2", 
                    "param2": "1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "237", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000595"
                }
            ], 
            "id": 63
        }, 
        {
            "title": "收到237/k1=0/k2=1,关门227/刷新第8批怪/k1+2/k2+2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "227", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "8", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20010805:1", 
                    "param2": "0 0 105", 
                    "param1": "-36772.3 -47282.6 17192.0", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q012048", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "k1", 
                    "param4": "", 
                    "id": 31
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "k2", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "k1", 
                    "param2": "0"
                }, 
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "k2", 
                    "param2": "1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "237", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000595"
                }
            ], 
            "id": 64
        }, 
        {
            "title": "收到门发送的5，播放镜头412/开门", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20010796", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000529", 
                    "param4": "", 
                    "id": 17
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "6", 
                    "param4": "", 
                    "id": 89
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "5", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000651"
                }
            ], 
            "id": 65
        }, 
        {
            "title": "收到378/k3=0,关门234/关门236/刷新第9批怪/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "234|236", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20010805:1", 
                    "param2": "0 0 110", 
                    "param1": "-79947.12 -53370.89 18269.00", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "9", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q012049", 
                    "param4": "", 
                    "id": 19
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
                    "param3": "0", 
                    "id": 26, 
                    "param1": "k3", 
                    "param2": "0"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "378", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000652"
                }
            ], 
            "id": 66
        }, 
        {
            "title": "收到379/k3=0,关门234/关门236/刷新第10批怪/k3+1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "234|236", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20010805:1", 
                    "param2": "0 0 200", 
                    "param1": "-79475.42 -52139.23 18269.00", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q012049", 
                    "param4": "", 
                    "id": 19
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
                    "param3": "0", 
                    "id": 26, 
                    "param1": "k3", 
                    "param2": "0"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "379", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000653"
                }
            ], 
            "id": 67
        }, 
        {
            "title": "收到Boss3发送的8，播放镜头413/给物品", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "110000531", 
                    "param4": "", 
                    "id": 17
                }, 
                {
                    "delayTime": 3.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "301010139", 
                    "param4": "", 
                    "id": 43
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "8", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "20010797"
                }
            ], 
            "id": 68
        }, 
        {
            "title": "收到传送陷阱发送的通知9，旁白提示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q012056", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "9", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20010815"
                }
            ], 
            "id": 69
        }, 
        {
            "title": "收到380，关窗/对Boss3发送6/取消t2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "205", 
                    "param4": "", 
                    "id": 208
                }, 
                {
                    "delayTime": 0.10000000149, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "241", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20010805:1", 
                    "param2": "0 0 19", 
                    "param1": "-81491.9 -50934.7 19462.0", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "t2", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "6", 
                    "param1": "20010797", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 5.0, 
                    "param3": "", 
                    "param2": "7", 
                    "param1": "20010814", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "380", 
                    "id": 9, 
                    "param1": "", 
                    "param2": "40000596"
                }
            ], 
            "id": 70
        }, 
        {
            "title": "收到地面指引的989指令，增加计数hhh", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "hhh", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "989", 
                    "id": 9, 
                    "param1": "AI", 
                    "param2": "20004561"
                }
            ], 
            "id": 71
        }
    ], 
    15: [
        {
            "title": "到达石像前，旁白提示/通知第2批准备解除石化", 
            "describe": "前方石像乃上古仙道天兵所化，请你通过他们的考验！", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q012660", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 2.5, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20010798|20010799", 
                    "param4": "", 
                    "id": 10
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "10", 
                    "param3": "-5259.8 -1420.4 14571.9", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "19572|9572"
                }
            ], 
            "id": 1
        }, 
        {
            "title": "到达区域2房屋建筑，对12批怪发送2", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "20010810|20010811", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q012049", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-90524.6 -59510.9|-90025.3 -60907.8|-86923.4 -59738.5|-87423.0 -58334.0", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "22737|12737"
                }
            ], 
            "id": 2
        }, 
        {
            "title": "到达建筑4二层，刷新14批", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q012051", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-95685.0 -67581.0|-95014.0 -67322.0|-95516.0 -65965.0 |-92991.0 -64960.0|-91586.0 -68905.0|-94733.0 -69988.0", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "19180.0|18830.0"
                }
            ], 
            "id": 3
        }, 
        {
            "title": "到达台子，播放心魔出场镜头", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "628", 
                    "param4": "", 
                    "id": 170
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 11, 
                    "param1": "2|3", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "-4230.5 -11849.0|-4234.8 -12610.8|-2289.8 -12597.0|-2289.9 -11867.3", 
                    "id": 18, 
                    "param1": "2", 
                    "param2": "20294|10294"
                }
            ], 
            "id": 4
        }, 
        {
            "title": "玩家进入最后一栋房子，完成阶段目标5，增加计数hhh", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "20004561", 
                    "param1": "20", 
                    "param4": "", 
                    "id": 14
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "10", 
                    "param3": "-37008.0 -46238.0 17185.0", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "27185.0|7185.0"
                }
            ], 
            "id": 5
        }
    ], 
    28: [
        {
            "title": "阶段6目标1完成，清除240", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "240", 
                    "param4": "", 
                    "id": 208
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 43, 
                    "param1": "6", 
                    "param2": "1"
                }
            ], 
            "id": 1
        }
    ]
}