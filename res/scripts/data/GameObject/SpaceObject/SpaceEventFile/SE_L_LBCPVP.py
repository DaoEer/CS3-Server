# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "设置双方复活点", 
            "describe": "刷野怪\\商店倒计时", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 140|0 0 -40", 
                    "param1": "-13140.0 10640.0 302.0|15830.0 -17630.0 302.0", 
                    "param4": "", 
                    "id": 5
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "30", 
                    "param1": "t1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "50", 
                    "param1": "d1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "60", 
                    "param1": "z1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "180", 
                    "param1": "b1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "360", 
                    "param1": "b2", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "60", 
                    "param1": "sj", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "120", 
                    "param1": "zl", 
                    "param4": "", 
                    "id": 12
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
            "title": "6分钟前刷小兵", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20007981:11;20007981:12;20007981:13;20007982:14|20007991:32;20007991:33;20007991:34;20007992:35", 
                    "param2": "20007981:22;20007981:23;20007981:24;20007982:25|20007991:27;20007991:28;20007991:29;20007992:30", 
                    "param1": "20007981:17;20007981:18;20007981:19;20007982:20|20007991:7;20007991:8;20007991:9;20007992:10", 
                    "param4": "0 0 -45;0 0 -80;0 0 5|0 0 140;0 0 -95;0 0 -130", 
                    "id": 161
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
        }, 
        {
            "title": "6分钟到达", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "30", 
                    "param1": "t2", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "t1", 
                    "param4": "", 
                    "id": 13
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "b2", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "6分钟后刷小兵", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20007981:11;20007981:12;20007981:13;20007982:14;20007983:15|20007991:32;20007991:33;20007991:34;20007992:35;20007993:36", 
                    "param2": "20007981:22;20007981:23;20007981:24;20007982:25;20007983:26|20007991:27;20007991:28;20007991:29;20007992:30;20007993:31", 
                    "param1": "20007981:17;20007981:18;20007981:19;20007982:20;20007983:21|20007991:7;20007991:8;20007991:9;20007992:10;20007993:16", 
                    "param4": "0 0 -45;0 0 -80;0 0 5|0 0 140;0 0 -95;0 0 -130", 
                    "id": 161
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "t2", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "刷低强度野怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "d1", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "刷中强度野怪", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "z1", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "刷小Boss", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "b1", 
                    "param2": ""
                }
            ], 
            "id": 6
        }, 
        {
            "title": "刷大Boss", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 27
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "b2", 
                    "param2": ""
                }
            ], 
            "id": 7
        }, 
        {
            "title": "60关闭副本", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 67
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 63
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "dao", 
                    "param2": ""
                }
            ], 
            "id": 8
        }, 
        {
            "title": "倒计时显示", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 46
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 63
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "dao1", 
                    "param2": ""
                }
            ], 
            "id": 9
        }, 
        {
            "title": "开启副本计时", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 47
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
            "id": 10
        }, 
        {
            "title": "随机事件", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20008029|20008031|20008032|20008033|20008034|20008035|20008036", 
                    "param2": "20008029|3", 
                    "param1": "0.4", 
                    "param4": "1000|100|100|100|100|100|100", 
                    "id": 266
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "sj", 
                    "param2": ""
                }
            ], 
            "id": 11
        }, 
        {
            "title": "中立商店", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "60", 
                    "param1": "xh", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "1", 
                    "param2": "10000758|10000758|10000758|10000758", 
                    "param1": "4960.0 -15720.0 -281.29|12910.0 -2570.0 -281.2966|6160.0 6480.0 -274.19|-7050.0 -5020.0 -281.29", 
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
                    "param1": "zl", 
                    "param2": ""
                }
            ], 
            "id": 12
        }, 
        {
            "title": "销毁中立商店", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10000758", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "xh", 
                    "param2": ""
                }
            ], 
            "id": 13
        }
    ], 
    3: [
        {
            "title": "英雄王座快捷栏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 264
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "添加升级物品", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "302010013", 
                    "param4": "", 
                    "id": 42
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    7: [], 
    13: [
        {
            "title": "删除额外快捷栏", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 63
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 265
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "302010013", 
                    "param4": "", 
                    "id": 23
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "解除移动限制", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 63
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    14: [
        {
            "title": "活动结束", 
            "describe": "", 
            "actions": [
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
                    "param3": "0", 
                    "param2": "60", 
                    "param1": "dao", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20007981|20007982|20007983|20007984|20007985|20007986|20007987|20007988|20007991|20007992|20007993|20007994|20007995|20007996|20007997|20007998|20008017|20008018|20008019|20008020|20008021|20008022", 
                    "param4": "", 
                    "id": 9
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
                    "param3": "0", 
                    "param2": "50", 
                    "param1": "dao1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "sj", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001837", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "Win", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "改变天气效果-ZH", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "642", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "001", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "改变天气效果-QL", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "643", 
                    "param4": "", 
                    "id": 207
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "002", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 3
        }
    ], 
    21: [
        {
            "title": "刷商店", 
            "describe": "刷野怪\\商店倒计时", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10000756|10000757", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "10001414:1", 
                    "param2": "0 0 40", 
                    "param1": "-13570 10041 362", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "10001415:1", 
                    "param2": "0 0 60", 
                    "param1": "15200 -17980 362", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "20014923:1", 
                    "param2": "0 0 0", 
                    "param1": "-13140 10650 310", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "20014924:1", 
                    "param2": "0 0 0", 
                    "param1": "15830 -17640 310", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "播放语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001843|C001844", 
                    "param4": "", 
                    "id": 19
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }
    ], 
    23: [
        {
            "title": "玩家\\野怪被杀（改）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20008017|20008018|20008019|20008020", 
                    "param2": "200", 
                    "param1": "500", 
                    "param4": "0", 
                    "id": 415
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }
    ], 
    25: [
        {
            "title": "仙道小怪被击杀（改）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "50", 
                    "param1": "50", 
                    "param4": "", 
                    "id": 414
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20007981|20007982|20007983|20008017|20008018|20008019|20008020", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "魔道小怪被击杀（改）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "50", 
                    "param1": "50", 
                    "param4": "", 
                    "id": 414
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20007991|20007992|20007993|20008017|20008018|20008019|20008020", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "基地被破坏-仙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "t1|t2", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "498", 
                    "param4": "", 
                    "id": 170
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20007989", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "基地被破坏-魔", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "t1|t2", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "499", 
                    "param4": "", 
                    "id": 170
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20007999", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "BOSS被击杀（改）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 416
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20008021", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "防御塔-仙（改）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 417
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20007990|20008001|20008002|20008003|20008004|20008005|20008006|20008007|20008277|20008278|20008279|20008280|20008281|20008282|20008283|20008284|20008295|20008296|20008297|20008298|20008299|20008300|20008301|20008302|20008313|20008314|20008315|20008316|20008317|20008318|20008319|20008320", 
                    "param2": ""
                }
            ], 
            "id": 6
        }, 
        {
            "title": "防御塔-魔（改）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "0", 
                    "param4": "", 
                    "id": 417
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20008000|20008009|20008010|20008011|20008012|20008013|20008014|20008015|20008286|20008287|20008288|20008289|20008290|20008291|20008292|20008293|20008304|20008305|20008306|20008307|20008308|20008309|20008310|20008311|20008322|20008323|20008324|20008325|20008326|20008327|20008328|20008329", 
                    "param2": ""
                }
            ], 
            "id": 7
        }, 
        {
            "title": "特殊精英 天师被击杀", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "642|643", 
                    "param4": "", 
                    "id": 208
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "20008029", 
                    "param2": ""
                }
            ], 
            "id": 8
        }
    ], 
    30: [
        {
            "title": "播放语音", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 439
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C001836", 
                    "param4": "", 
                    "id": 256
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 52, 
                    "param1": "C001844", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ]
}