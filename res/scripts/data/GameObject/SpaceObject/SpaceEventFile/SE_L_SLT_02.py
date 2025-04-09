# -*- coding: utf-8 -*-
Datas = {
    5: [
        {
            "title": "小怪全部死亡，刷新精英/精英喊话/销毁跟随攻击玩家的水球", 
            "describe": "我乃祖巫帝江座下鬼斧魔将拓冥！敢觊觎主上的灵气，看我碾碎你们！", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 27
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "20005705|20005701", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.5, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q032021", 
                    "param4": "", 
                    "id": 19
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
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "精英死亡，通知塔死亡/召唤宝箱/精英死亡喊话", 
            "describe": "休要得意…主人定不会放过你们…", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20005701", 
                    "param4": "", 
                    "id": 130
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20005706", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20011914:1", 
                    "param2": "0 0 90", 
                    "param1": "-1357.7 -79.3 347.6", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q032022", 
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
                    "param1": "20000957", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    12: [
        {
            "title": "塔销毁，通知灵珠子开启宝箱", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "12", 
                    "param1": "20000944", 
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
                    "param1": "20005701", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "宝箱销毁，通知灵珠子喊话/去往下一层", 
            "describe": "勇士，第二层锁灵塔已破，这便随我闯入第三层！", 
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
                    "param1": "Q032023", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 89
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "next", 
                    "param1": "20000944", 
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
                    "param1": "20011914", 
                    "param2": ""
                }
            ], 
            "id": 2
        }
    ], 
    13: [
        {
            "title": "离开副本，取消灵珠子跟随", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11000809", 
                    "param4": "", 
                    "id": 25
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    17: [
        {
            "title": "离开副本，取消灵珠子跟随", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11000809", 
                    "param4": "", 
                    "id": 25
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    21: [
        {
            "title": "加灵珠子跟随buff/进副本喊话", 
            "describe": "勇士我们已经到达锁灵塔二层！", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "11000809", 
                    "param4": "", 
                    "id": 33
                }, 
                {
                    "delayTime": 0.5, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "Q032020", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    30: [
        {
            "title": "精英喊话结束，攻击玩家", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "hit", 
                    "param1": "20000957", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20005706:1", 
                    "param2": "0 0 0", 
                    "param1": "-1358.0 -79.0 348.0", 
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
                    "id": 52, 
                    "param1": "Q032021", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ]
}