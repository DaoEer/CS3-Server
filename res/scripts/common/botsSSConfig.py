# -*- coding: UTF-8 -*-
import  LoadModule
import json
import os,sys
PATH = "res/scripts/bots/configObject/taskConfig"
PATH_SRC = "GameObject/SpaceObject"

def loadConfig():
	Datas = {}
	objConfigs = LoadModule.openJsonPathCfg( PATH_SRC )
	for config in objConfigs:
		SSData={}
		keyID = config[ "scriptID" ]
		fileName = config[ "SpaceData" ].get( "stageFile", "" )
		if fileName=="" :continue
		section=LoadModule.openJsonCfg( "GameObject/SpaceObject/SpaceStageFile/"+fileName+".json" )
		cfg = {}
		actions = {}
		for stageIndexStr, stageSec in section["stages"].items():		#字典的key是str，需要变成int才可以正确排序
			SSData[int( stageIndexStr )] = {}
			for taskIndexstr,taskSec in stageSec["tasks"].items():
				SSData[int( stageIndexStr )][int( taskIndexstr )] = taskSec
		index = 1
		for stageIndex,stageSec in  SSData.items():
			for taskIndex,taskSec in stageSec.items():
				scripts = TASK_ACTION_MAP[ taskSec["type"]]
				for script in scripts:
					action = {}
					action["Script"] = script
					action["taskID"] = taskIndex
					action["stageID"] = stageIndex
					action["keyid"] = keyID
					if "navigateData" in taskSec.keys():
						action["navigateData"] = taskSec["navigateData"]
					else:
						action["navigateData"] = ""
					action["param1"] = taskSec["param1"]
					action["param2"] = taskSec["param2"]
					action["param3"] = taskSec["param3"]
					action["goal"]	 = taskSec["reqVal"]
					actions[ index ] = action
					index += 1
			if actions=={}:continue
			cfg["Script"] = "Behaviour3"
			cfg["actions"] = actions
			Datas[keyID] = cfg
		
			#转换编码写入文件
		#cfgText = cfg.decode()
	cfgStr = json.dumps(Datas)
	cfgStr = cfgStr.replace("},", "},\n")
	file = open(os.path.join(PATH,"spaceStage.py"),"w")
	file.write("Datas=")
	file.write( cfgStr )
	file.close()
	print("Load spaceStage finished, total")
	

TASK_ACTION_MAP={
"SStageTask_killMonster" :["Action1"],
"SStageTask_conditionChange" :["Action20"],
"SStageTask_getItem" :["Action6"],
"SStageTask_UseItem" :["Action16"],
"SStageTask_enterArea" :["Action20"],
"SStageTask_triggerBox" :["Action20"],
"SStageTask_CustomTask" :["Action20"],
"SStageTask_NPCObjectDestroy" :["Action20"],
}



loadConfig()