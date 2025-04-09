# -*- coding: utf-8 -*-
Datas = {
    1: [
        {
            "title": "增加复活点", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0 0 0", 
                    "param1": "-632.0 -2014.0 560.0", 
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
            "title": "进入第一阶段", 
            "describe": "进入第一阶段，第一阶段刷新少量的福袋（不刷新金色锦囊），下落速度较慢，且停留在地面上的时间较长\n添加第一阶段描述喊话\n开始计时器准备添加为期10秒的加速Buff（风火轮）\n开始计时器准备添加为期10秒的罩子Buff（乾坤聚宝袋）", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000697", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "10", 
                    "param1": "fenghuolun", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "20", 
                    "param1": "zhaozi", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "23", 
                    "param1": "yijieduan", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "10000901:30|10000902:20|10000903:4", 
                    "param2": "-90 -2300|770 -2030|1450 -1440|1820 -610|1790 380|1350 1240|530 1800|-430 1950|-1410 1660|-2110 930|-2390 -70|-2260 -940|-1700 -1760|-910 -2200", 
                    "param1": "860|1500|2000", 
                    "param4": "1", 
                    "id": 282
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 283
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "15", 
                    "param1": "300", 
                    "param4": "", 
                    "id": 97
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "300", 
                    "param1": "process", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "290", 
                    "param1": "over_time", 
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
                    "param1": "start1", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "进入第二阶段", 
            "describe": "进入第二阶段，刷新福袋的数量增加，并且有极少数量的“金色锦囊”出现，掉落速度加快，停留在地面的时间变短\n添加第二阶段描述喊话\n添加随机事件的timer计时，准备开始开启随机事件\n17秒必刷一次金色锦囊", 
            "actions": [
                {
                    "delayTime": 7.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000698", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 7.0, 
                    "param3": "0", 
                    "param2": "15", 
                    "param1": "suijishijian", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 7.0, 
                    "param3": "0", 
                    "param2": "52", 
                    "param1": "erjieduan", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 7.0, 
                    "param3": "10000901:35|10000902:25|10000903:4", 
                    "param2": "-90 -2300|770 -2030|1450 -1440|1820 -610|1790 380|1350 1240|530 1800|-430 1950|-1410 1660|-2110 930|-2390 -70|-2260 -940|-1700 -1760|-910 -2200", 
                    "param1": "860|1500|2000", 
                    "param4": "1", 
                    "id": 282
                }, 
                {
                    "delayTime": 7.0, 
                    "param3": "0", 
                    "param2": "17", 
                    "param1": "jinsejinnang", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 7.0, 
                    "param3": "", 
                    "param2": "15", 
                    "param1": "", 
                    "param4": "", 
                    "id": 249
                }, 
                {
                    "delayTime": 7.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 283
                }, 
                {
                    "delayTime": 7.0, 
                    "param3": "1", 
                    "param2": "40", 
                    "param1": "fenghuolun1", 
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
                    "param1": "yijieduan", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "2阶段金色锦囊出现语音", 
            "describe": "刷1个金色锦囊\n刷金色锦囊的喊话通知", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000712", 
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
                    "param1": "jinsejinnang", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "第一次随机事件-固定触发祥龙", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "xianglong", 
                    "param4": "", 
                    "id": 222
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "30", 
                    "param1": "suiji1", 
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
                    "param1": "suijishijian", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "第一次随机事件结束", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "30", 
                    "param1": "", 
                    "param4": "", 
                    "id": 249
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "suiji1", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "进入第三阶段", 
            "describe": "进入第三阶段，第三阶段只刷新纯特效的锦囊\n添加第三阶段描述喊话\n新增了负面的事件（天地异象·风，天地异象·雷）", 
            "actions": [
                {
                    "delayTime": 8.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000699", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "0", 
                    "param2": "52", 
                    "param1": "sanjieduan", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "10000941:35|10000959:25|10000968:4", 
                    "param2": "-90 -2300|770 -2030|1450 -1440|1820 -610|1790 380|1350 1240|530 1800|-430 1950|-1410 1660|-2110 930|-2390 -70|-2260 -940|-1700 -1760|-910 -2200", 
                    "param1": "860|1500|2000", 
                    "param4": "1", 
                    "id": 282
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "1", 
                    "param2": "16", 
                    "param1": "lvsetexiao", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 283
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "0", 
                    "param2": "15", 
                    "param1": "suijishijian2", 
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
                    "param1": "erjieduan", 
                    "param2": ""
                }
            ], 
            "id": 6
        }, 
        {
            "title": "3阶段必刷绿色特效锦囊", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "10000973:4", 
                    "param2": "-90 -2300|770 -2030|1450 -1440|1820 -610|1790 380|1350 1240|530 1800|-430 1950|-1410 1660|-2110 930|-2390 -70|-2260 -940|-1700 -1760|-910 -2200", 
                    "param1": "860|1500|2000", 
                    "param4": "1", 
                    "id": 282
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "lvsetexiao", 
                    "param2": ""
                }
            ], 
            "id": 7
        }, 
        {
            "title": "第二次随机事件-固定触发童子", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "tongzi", 
                    "param4": "", 
                    "id": 222
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "30", 
                    "param1": "suiji2", 
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
                    "param1": "suijishijian2", 
                    "param2": ""
                }
            ], 
            "id": 8
        }, 
        {
            "title": "第二次随机事件结束", 
            "describe": "送财童子结束，关闭timer，销毁NPC", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "25", 
                    "param1": "", 
                    "param4": "", 
                    "id": 249
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "hubao", 
                    "param4": "", 
                    "id": 222
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "suiji2", 
                    "param2": ""
                }
            ], 
            "id": 9
        }, 
        {
            "title": "进入第四阶段", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 8.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000700", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "10000905:20|10000906:15|10000907:6|10000942:20|10000960:15|10000969:4", 
                    "param2": "-90 -2300|770 -2030|1450 -1440|1820 -610|1790 380|1350 1240|530 1800|-430 1950|-1410 1660|-2110 930|-2390 -70|-2260 -940|-1700 -1760|-910 -2200", 
                    "param1": "860|1500|2000", 
                    "param4": "1", 
                    "id": 282
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "0", 
                    "param2": "82", 
                    "param1": "sijieduan", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "1", 
                    "param2": "30", 
                    "param1": "jinsejinnang1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "1", 
                    "param2": "40", 
                    "param1": "lvsetexiao1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 283
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "lvsetexiao", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "0", 
                    "param2": "10", 
                    "param1": "suijishijian3", 
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
                    "param1": "sanjieduan", 
                    "param2": ""
                }
            ], 
            "id": 10
        }, 
        {
            "title": "4阶段金色锦囊", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "10000908:4", 
                    "param2": "-90 -2300|770 -2030|1450 -1440|1820 -610|1790 380|1350 1240|530 1800|-430 1950|-1410 1660|-2110 930|-2390 -70|-2260 -940|-1700 -1760|-910 -2200", 
                    "param1": "860|1500|2000", 
                    "param4": "1", 
                    "id": 282
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "jinsejinnang1", 
                    "param2": ""
                }
            ], 
            "id": 11
        }, 
        {
            "title": "4阶段绿色特效锦囊", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "10000974:4", 
                    "param2": "-90 -2300|770 -2030|1450 -1440|1820 -610|1790 380|1350 1240|530 1800|-430 1950|-1410 1660|-2110 930|-2390 -70|-2260 -940|-1700 -1760|-910 -2200", 
                    "param1": "860|1500|2000", 
                    "param4": "1", 
                    "id": 282
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "lvsetexiao1", 
                    "param2": ""
                }
            ], 
            "id": 12
        }, 
        {
            "title": "第三次随机事件", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "xianglong|feng|lei", 
                    "param4": "", 
                    "id": 223
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "30", 
                    "param1": "suiji3", 
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
                    "param1": "suijishijian3", 
                    "param2": ""
                }
            ], 
            "id": 13
        }, 
        {
            "title": "第三次随机事件结束", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "10", 
                    "param1": "", 
                    "param4": "", 
                    "id": 249
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "10", 
                    "param1": "suijishijian4", 
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
                    "param1": "suiji3", 
                    "param2": ""
                }
            ], 
            "id": 14
        }, 
        {
            "title": "第四次随机事件", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "xianglong|tongzi|feng|lei", 
                    "param4": "", 
                    "id": 223
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "30", 
                    "param1": "suiji4", 
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
                    "param1": "suijishijian4", 
                    "param2": ""
                }
            ], 
            "id": 15
        }, 
        {
            "title": "第四次随机事件结束", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "25", 
                    "param1": "", 
                    "param4": "", 
                    "id": 249
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "hubao", 
                    "param4": "", 
                    "id": 222
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "suiji4", 
                    "param2": ""
                }
            ], 
            "id": 16
        }, 
        {
            "title": "进入第五阶段", 
            "describe": "进入第五阶段，第五阶段刷新实体型福袋和纯特效型福袋，全场景掉落\n福袋掉落速度继续加快，销毁时间加快\n添加第五阶段描述喊话\n继续维持随机事件\n销毁金色锦囊和绿色特效锦囊的计时器", 
            "actions": [
                {
                    "delayTime": 8.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000701", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "10000909:25|10000910:20|10000911:4|10000943:25|10000961:8|10000970:8", 
                    "param2": "-90 -2300|770 -2030|1450 -1440|1820 -610|1790 380|1350 1240|530 1800|-430 1950|-1410 1660|-2110 930|-2390 -70|-2260 -940|-1700 -1760|-910 -2200", 
                    "param1": "860|1500|2000", 
                    "param4": "1", 
                    "id": 282
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "jinsejinnang1", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "lvsetexiao1", 
                    "param4": "", 
                    "id": 13
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "1", 
                    "param2": "20", 
                    "param1": "jinsejinnang2", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "1", 
                    "param2": "30", 
                    "param1": "lvsetexiao2", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "0", 
                    "param2": "45", 
                    "param1": "wujieduan", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 283
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "0", 
                    "param2": "15", 
                    "param1": "suijishijian5", 
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
                    "param1": "sijieduan", 
                    "param2": ""
                }
            ], 
            "id": 17
        }, 
        {
            "title": "5阶段金色锦囊", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "10000912:2", 
                    "param2": "-90 -2300|770 -2030|1450 -1440|1820 -610|1790 380|1350 1240|530 1800|-430 1950|-1410 1660|-2110 930|-2390 -70|-2260 -940|-1700 -1760|-910 -2200", 
                    "param1": "860|1500|2000", 
                    "param4": "1", 
                    "id": 282
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "jinsejinnang2", 
                    "param2": ""
                }
            ], 
            "id": 18
        }, 
        {
            "title": "5阶段绿色特效锦囊", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "10000975:4", 
                    "param2": "-90 -2300|770 -2030|1450 -1440|1820 -610|1790 380|1350 1240|530 1800|-430 1950|-1410 1660|-2110 930|-2390 -70|-2260 -940|-1700 -1760|-910 -2200", 
                    "param1": "860|1500|2000", 
                    "param4": "1", 
                    "id": 282
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "lvsetexiao2", 
                    "param2": ""
                }
            ], 
            "id": 19
        }, 
        {
            "title": "第五次随机事件", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "xianglong|tongzi|feng|lei", 
                    "param4": "", 
                    "id": 223
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "30", 
                    "param1": "suiji5", 
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
                    "param1": "suijishijian5", 
                    "param2": ""
                }
            ], 
            "id": 20
        }, 
        {
            "title": "第五次随机事件结束", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "30", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 249
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "suiji5", 
                    "param2": ""
                }
            ], 
            "id": 21
        }, 
        {
            "title": "添加临时风火轮Buff", 
            "describe": "添加风火轮buff\n添加风火轮存在的喊话", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14014056", 
                    "param4": "", 
                    "id": 34
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000707", 
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
                    "param1": "fenghuolun", 
                    "param2": ""
                }
            ], 
            "id": 22
        }, 
        {
            "title": "二阶段后每40秒添加风火轮Buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14014056", 
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
                    "param1": "fenghuolun1", 
                    "param2": ""
                }
            ], 
            "id": 23
        }, 
        {
            "title": "铜钱阵7秒后自然销毁", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "30000693", 
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
                    "param1": "tongzixianjing", 
                    "param2": ""
                }
            ], 
            "id": 24
        }, 
        {
            "title": "天地异象·风-随机事件结束", 
            "describe": "天地异象·风事件结束，删除timer和陷阱（无论是否已触发）", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "30000586", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "641", 
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
                    "id": 8, 
                    "param1": "feng_start", 
                    "param2": ""
                }
            ], 
            "id": 25
        }, 
        {
            "title": "天地异象·雷-随机事件结束", 
            "describe": "天地异象·雷事件结束，删除timer和陷阱（无论是否已触发）", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "30000576", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "641", 
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
                    "id": 8, 
                    "param1": "lei_start", 
                    "param2": ""
                }
            ], 
            "id": 26
        }, 
        {
            "title": "副本结束倒计时", 
            "describe": "副本结束前，给个10秒的倒计时提醒", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10", 
                    "param4": "", 
                    "id": 46
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "over_time", 
                    "param2": ""
                }
            ], 
            "id": 27
        }, 
        {
            "title": "副本通关", 
            "describe": "副本通关，强制传送角色出副本", 
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
                    "param1": "", 
                    "param4": "", 
                    "id": 455
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 -90", 
                    "param2": "-320 1529 860", 
                    "param1": "40001000", 
                    "param4": "1", 
                    "id": 156
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "20010168|20009215|20009216", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20014661:1", 
                    "param2": "0 0 90", 
                    "param1": "-188 3283 848", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40001017:1", 
                    "param2": "0 0 -90", 
                    "param1": "-194 4249 965", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "jieshu", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 72, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "process", 
                    "param2": ""
                }
            ], 
            "id": 28
        }, 
        {
            "title": "副本失败", 
            "describe": "副本失败，强制传送角色出副本", 
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
                    "param1": "20010168|20009215|20009216", 
                    "param4": "", 
                    "id": 9
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20014661:1", 
                    "param2": "0 0 90", 
                    "param1": "-188 3283 848", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "40001017:1", 
                    "param2": "0 0 -90", 
                    "param1": "-194 4249 965", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "jieshu", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 71, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 8, 
                    "param1": "process", 
                    "param2": ""
                }
            ], 
            "id": 29
        }
    ], 
    5: [
        {
            "title": "暗卫死亡monster计数减1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "-1", 
                    "param1": "monster", 
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
                    "param1": "20010169", 
                    "param2": ""
                }
            ], 
            "id": 1
        }
    ], 
    6: [
        {
            "title": "暗卫刷新monster计数加1", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "monster", 
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
                    "param1": "20010169", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "entity下落（普通锦囊）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 221
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000901|10000902|10000903|10000904|10000905|10000906|10000907|10000908|10000909|10000910|10000911|10000912|10000913|10000914|10000915|10000916|10000917|10000918|10000919|10000920|10000921|10000922|10000923|10000924|10000925|10000926|10000927|10000928|10000929|10000930|10000931|10000932|10000933|10000934|10000935|10000937|10000938|10000939|10000940", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "entity下落（特效锦囊）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 221
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000941|10000942|10000943|10000944|10000945|10000946|10000947|10000948|10000949|10000950|10000951|10000952|10000953|10000954|10000955|10000956|10000957|10000958|10000959|10000960|10000961|10000962|10000963|10000964|10000965|10000966|10000967|10000968|10000969|10000970|10000971|10000972|10000973|10000974|10000975", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "entity下落（怪物掉落财宝）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 221
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000976|10000977|10000978|10000979|10000980|10000981|10000982|10000983|10000984", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "暗卫存在时，销毁所有金树上的财宝", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10000901|10000902|10000903|10000904|10000905|10000906|10000907|10000908|10000909|10000910|10000911|10000912|10000913|10000914|10000915|10000916|10000917|10000918|10000919|10000920|10000921|10000922|10000923|10000924|10000925|10000926|10000927|10000928|10000929|10000930|10000931|10000932|10000933|10000934|10000935|10000937|10000938|10000939|10000940|10000941|10000942|10000943|10000944|10000945|10000946|10000947|10000948|10000949|10000950|10000951|10000952|10000953|10000954|10000955|10000956|10000957|10000958|10000959|10000960|10000961|10000962|10000963|10000964|10000965|10000966|10000967|10000968|10000969|10000970|10000971|10000972|10000973|10000974|10000975", 
                    "param4": "", 
                    "id": 9
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000901|10000902|10000903|10000904|10000905|10000906|10000907|10000908|10000909|10000910|10000911|10000912|10000913|10000914|10000915|10000916|10000917|10000918|10000919|10000920|10000921|10000922|10000923|10000924|10000925|10000926|10000927|10000928|10000929|10000930|10000931|10000932|10000933|10000934|10000935|10000937|10000938|10000939|10000940|10000941|10000942|10000943|10000944|10000945|10000946|10000947|10000948|10000949|10000950|10000951|10000952|10000953|10000954|10000955|10000956|10000957|10000958|10000959|10000960|10000961|10000962|10000963|10000964|10000965|10000966|10000967|10000968|10000969|10000970|10000971|10000972|10000973|10000974|10000975", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "暗卫掉落的潜能转移到福袋上", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "2", 
                    "param1": "10000976", 
                    "param4": "", 
                    "id": 305
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000976", 
                    "param2": ""
                }
            ], 
            "id": 6
        }, 
        {
            "title": "暗卫掉落的金币转移到福袋上", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "10000977", 
                    "param4": "", 
                    "id": 305
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000977", 
                    "param2": ""
                }
            ], 
            "id": 7
        }, 
        {
            "title": "暗卫掉落的材料转移到福袋上", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "3", 
                    "param1": "10000978", 
                    "param4": "", 
                    "id": 305
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000978", 
                    "param2": ""
                }
            ], 
            "id": 8
        }, 
        {
            "title": "暗卫掉落的装备转移到福袋上", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "4", 
                    "param1": "10000979", 
                    "param4": "", 
                    "id": 305
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000979", 
                    "param2": ""
                }
            ], 
            "id": 9
        }
    ], 
    12: [
        {
            "title": "一阶段循环刷新", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10000901|10000902|10000903|10000905|10000906|10000909|10000913|10000917", 
                    "param4": "", 
                    "id": 220
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "yijieduan", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000901|10000902|10000903|10000905|10000906|10000909|10000913|10000917", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "二阶段循环刷新", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10000901|10000902|10000903|10000905|10000906|10000909|10000910|10000913|10000917", 
                    "param4": "", 
                    "id": 220
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "erjieduan", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000901|10000902|10000903|10000905|10000906|10000909|10000910|10000913|10000917", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "三阶段循环刷新", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10000941|10000942|10000943|10000944|10000945|10000959|10000960|10000961|10000968", 
                    "param4": "", 
                    "id": 220
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "sanjieduan", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000941|10000942|10000943|10000944|10000945|10000959|10000960|10000961|10000968", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "四阶段循环刷新", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10000905|10000906|10000907|10000909|10000910|10000913|10000942|10000943|10000944|10000960|10000961|10000969", 
                    "param4": "", 
                    "id": 220
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "sijieduan", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000905|10000906|10000907|10000909|10000910|10000913|10000942|10000943|10000944|10000960|10000961|10000969", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "五阶段循环刷新", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "10000909|10000910|10000911|10000913|10000914|10000917|10000918|10000943|10000944|10000945|10000946|10000961|10000962|10000963|10000970", 
                    "param4": "", 
                    "id": 220
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "wujieduan", 
                    "param2": ""
                }, 
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 2, 
                    "param1": "10000909|10000910|10000911|10000913|10000914|10000917|10000918|10000943|10000944|10000945|10000946|10000961|10000962|10000963|10000970", 
                    "param2": ""
                }
            ], 
            "id": 5
        }
    ], 
    13: [
        {
            "title": "清除玩家身上副本专用buff", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14014060|14014101|14013806|14013807|15003805|15003801|15003802|15003803|15003804|15003805|15003806|15003807|15003808", 
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
    14: [
        {
            "title": "拾取聚宝鼎后开始活动", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "3", 
                    "param1": "start1", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 46
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "start", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 1
        }, 
        {
            "title": "随机事件-祥龙现世（不存在护宝守卫）", 
            "describe": "每次触发到该条时，触发timer添加，指定掉落物生成，219通知这些生成物开始掉落", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20009215:1", 
                    "param2": "0 0 130", 
                    "param1": "3140 -5890 1230", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000715", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "30", 
                    "param1": "2", 
                    "param4": "", 
                    "id": 249
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "xianglong", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 2
        }, 
        {
            "title": "祥龙落福", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "10000940:3", 
                    "param2": "-90 -2300|770 -2030|1450 -1440|1820 -610|1790 380|1350 1240|530 1800|-430 1950|-1410 1660|-2110 930|-2390 -70|-2260 -940|-1700 -1760|-910 -2200", 
                    "param1": "860|1500|2000", 
                    "param4": "1", 
                    "id": 282
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "ewaifudai", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 3
        }, 
        {
            "title": "随机事件-祥龙现世（存在护宝守卫）", 
            "describe": "每次触发到该条时，触发timer添加，指定掉落物生成，219通知这些生成物开始掉落", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20009217:1", 
                    "param2": "0 0 90", 
                    "param1": "-200 -4000 850", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000716", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "30", 
                    "param1": "7", 
                    "param4": "", 
                    "id": 249
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "xianglong", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 4
        }, 
        {
            "title": "随机事件-童子送福（不存在护宝守卫）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20009216:1", 
                    "param2": "0 0 90", 
                    "param1": "-200 -4000 850", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000714", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "30", 
                    "param1": "1", 
                    "param4": "", 
                    "id": 249
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "tongzi", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 5
        }, 
        {
            "title": "铜钱阵7秒自然销毁计时器开始", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "7", 
                    "param1": "tongzixianjing", 
                    "param4": "", 
                    "id": 12
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "ziranxiaohui", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 6
        }, 
        {
            "title": "随机事件-童子送福（存在护宝守卫）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "20009218:1", 
                    "param2": "0 0 90", 
                    "param1": "-200 -4000 850", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000717", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "30", 
                    "param1": "6", 
                    "param4": "", 
                    "id": 249
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "tongzi", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 7
        }, 
        {
            "title": "随机事件-天地异象·风", 
            "describe": "天地异象·风事件开启，添加timer，添加陷阱", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "30", 
                    "param1": "feng_start", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000640", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "30", 
                    "param1": "3", 
                    "param4": "", 
                    "id": 249
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "641", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 0|0 0 0|0 0 0|0 0 0|0 0 0|0 0 0", 
                    "param2": "-210 -2120 860|1400 -1090 860|1390 760 860|-510 1720 860|-2060 500 860|-2010 -1000 860", 
                    "param1": "30000586:6", 
                    "param4": "", 
                    "id": 118
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "feng", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 8
        }, 
        {
            "title": "随机事件-天地异象·雷", 
            "describe": "天地异象·雷事件开启，添加timer，添加陷阱", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "0", 
                    "param2": "30", 
                    "param1": "lei_start", 
                    "param4": "", 
                    "id": 12
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000641", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "30", 
                    "param1": "4", 
                    "param4": "", 
                    "id": 249
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "641", 
                    "param4": "", 
                    "id": 207
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "0 0 0|0 0 0|0 0 0|0 0 0|0 0 0|0 0 0", 
                    "param2": "-210 -2120 860|1400 -1090 860|1390 760 860|-510 1720 860|-2060 500 860|-2010 -1000 860", 
                    "param1": "30000576:6", 
                    "param4": "", 
                    "id": 118
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "lei", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 9
        }, 
        {
            "title": "事件·雷·陷阱效果", 
            "describe": "收到雷陷阱的通知，为角色添加眩晕buff", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "99990214", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "lei_xianjing", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 10
        }, 
        {
            "title": "事件·风·陷阱效果", 
            "describe": "收到风陷阱的通知，为角色添加混乱buff", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14014001", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "feng_xianjing", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 11
        }, 
        {
            "title": "出现护宝暗卫（不存在其他护宝暗卫时）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "559", 
                    "param4": "", 
                    "id": 170
                }, 
                {
                    "delayTime": 8.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000713", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "20010169:1", 
                    "param2": "0 0 -90", 
                    "param1": "-240 6270 1170", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 2.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 296
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "hubao", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 12
        }, 
        {
            "title": "出现护宝暗卫（存在其他护宝暗卫时）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "C000718", 
                    "param4": "", 
                    "id": 19
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "20010169:1", 
                    "param2": "0 0 -90", 
                    "param1": "-240 6270 1170", 
                    "param4": "", 
                    "id": 6
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "2", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "hubao", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 13
        }, 
        {
            "title": "护宝暗卫收取财宝，封印金树", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 2.0, 
                    "param3": "20010170:1", 
                    "param2": "0 0 0", 
                    "param1": "-248 -313 850", 
                    "param4": "", 
                    "id": 6
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "102010007|102010014|102010020|102010028", 
                    "param2": "203010009|203010011|203010015|203010016|203010003", 
                    "param1": "5|3|1", 
                    "param4": "", 
                    "id": 313
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "12345", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 14
        }, 
        {
            "title": "护宝暗卫死亡，解除封印（不存在其他护宝暗卫）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "88", 
                    "param1": "20010170", 
                    "param4": "", 
                    "id": 10
                }, 
                {
                    "delayTime": 1.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "", 
                    "param4": "", 
                    "id": 315
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "dead", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 15
        }, 
        {
            "title": "护宝暗卫死亡，掉落财宝", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "5", 
                    "param1": "20010169", 
                    "param4": "14021002|14021001|14021004|14021003", 
                    "id": 314
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "dead", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 16
        }, 
        {
            "title": "护宝暗卫死亡，恢复财宝掉落（第3阶段）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "10000941:20|10000959:12|10000968:4", 
                    "param2": "-90 -2300|770 -2030|1450 -1440|1820 -610|1790 380|1350 1240|530 1800|-430 1950|-1410 1660|-2110 930|-2390 -70|-2260 -940|-1700 -1760|-910 -2200", 
                    "param1": "860|1500|2000", 
                    "param4": "1", 
                    "id": 282
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "sanjieduan", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "dead", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 17
        }, 
        {
            "title": "护宝暗卫死亡，恢复财宝掉落（第4阶段）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "10000905:12|10000906:9|10000907:6|10000942:12|10000960:9|10000969:4", 
                    "param2": "-90 -2300|770 -2030|1450 -1440|1820 -610|1790 380|1350 1240|530 1800|-430 1950|-1410 1660|-2110 930|-2390 -70|-2260 -940|-1700 -1760|-910 -2200", 
                    "param1": "860|1500|2000", 
                    "param4": "1", 
                    "id": 282
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "sijieduan", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "dead", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 18
        }, 
        {
            "title": "护宝暗卫死亡，恢复财宝掉落（第5阶段）", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "10000909:12|10000910:12|10000911:4|10000943:15|10000961:4|10000970:4", 
                    "param2": "-90 -2300|770 -2030|1450 -1440|1820 -610|1790 380|1350 1240|530 1800|-430 1950|-1410 1660|-2110 930|-2390 -70|-2260 -940|-1700 -1760|-910 -2200", 
                    "param1": "860|1500|2000", 
                    "param4": "1", 
                    "id": 282
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "monster", 
                    "param2": "0"
                }, 
                {
                    "param4": "", 
                    "param3": "", 
                    "id": 44, 
                    "param1": "wujieduan", 
                    "param2": ""
                }
            ], 
            "canLoop": 1, 
            "triggerConditions": [
                {
                    "param4": "", 
                    "param3": "dead", 
                    "id": 9, 
                    "param1": "", 
                    "param2": ""
                }
            ], 
            "id": 19
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
                    "param1": "122573008", 
                    "param4": "", 
                    "id": 17
                }
            ], 
            "spaceConditions": [
                {
                    "param4": "", 
                    "param3": "0", 
                    "id": 26, 
                    "param1": "jieshu", 
                    "param2": "1"
                }
            ], 
            "canLoop": 0, 
            "triggerConditions": [
                {
                    "param4": "2", 
                    "param3": "-188 3283 848", 
                    "id": 18, 
                    "param1": "1", 
                    "param2": "1000|100"
                }
            ], 
            "id": 1
        }
    ], 
    21: [
        {
            "title": "给角色加对应的Buff", 
            "describe": "进入副本，为角色添加buff，置灰金玉芝道具", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "14014060|14014101", 
                    "param4": "", 
                    "id": 34
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 1, 
            "triggerConditions": [], 
            "id": 1
        }, 
        {
            "title": "播放开场，计数monster", 
            "describe": "", 
            "actions": [
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "", 
                    "param1": "561", 
                    "param4": "", 
                    "id": 170
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "1", 
                    "param1": "5", 
                    "param4": "", 
                    "id": 249
                }, 
                {
                    "delayTime": 0.0, 
                    "param3": "", 
                    "param2": "0", 
                    "param1": "monster", 
                    "param4": "", 
                    "id": 31
                }
            ], 
            "spaceConditions": [], 
            "canLoop": 0, 
            "triggerConditions": [], 
            "id": 2
        }
    ]
}