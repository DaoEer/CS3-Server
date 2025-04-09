// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
//CS3数据
#include "GameData/CharacterData.h"
#include "GameData/EnumCsvDefine.h"
//CS3
#include "GameData/CS3Object.h"
#include "ActionManager.generated.h"

/*
* 文件名称：ActionManager.h
* 功能说明：动作处理器
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2016-09-02
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UActionManager : public UCS3Object
{
	GENERATED_BODY()

private:
	UActionManager();
	~UActionManager();

public:
	static UActionManager* GetInstance();
	//static void SetInstance();

	bool IsBreakAction(FACTION_DATA CurActionData, FACTION_DATA NewActionData);
	bool IsBreakActionByType(ACTION_TYPE_ENUM CurActionType, ACTION_TYPE_ENUM NewActionType);

	FACTION_DATA GetActionDataById(TSoftObjectPtr<UDataTable> configPath, FName ActionId);
	FACTION_DATA GetActionDataByPose(TSoftObjectPtr<UDataTable> configPath, ACTION_POSE_ENUM ActionPose);
	ACTION_GROUND_TYPE_ENUM GetActionGround(FACTION_DATA& ActionData);
	
/*
private:
	static UActionManager* Instance;
	*/
};
