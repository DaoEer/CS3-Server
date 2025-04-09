// Fill out your copyright notice in the Description page of Project Settings.


#include "TeleportTask.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/GameStatus.h"
#include "Interface/Role/RoleChatInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"

CONTROL_COMPILE_OPTIMIZE_START

UTeleportTask::UTeleportTask()
	:Super()
{
	CustomTimeDilation = 5.0f;
}

void UTeleportTask::InitParam()
{
	ScriptID = Param1;
	Position = Param2;	//以空格分隔
	Direction = Param3;	//以空格分隔
	AT_INFO(TEXT("UTeleportTask InitParam ->Index[%d]"), Index);
}

void UTeleportTask::BeginTask()
{
	int32 PlayerID = UGolbalBPFunctionLibrary::GetPlayerID();
	if (PlayerID != 0)
	{
		//TArray<FString> args;
		//args.Add(INT_TO_FSTRING(PlayerID));
		//args.Add(TEXT("goto"));
		FString temp = ScriptID + TEXT(" ") + Position + TEXT(" ") + Direction;
		//args.Add(temp);
		//UGolbalBPFunctionLibrary::CellCall(PlayerID, TEXT("onRoleSendGMCommandMessage"), args);

		URoleChatInterface * RoleChatInterface = Cast<URoleChatInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleChatInterface")));
		if (RoleChatInterface)
		{
			RoleChatInterface->RPC_onRoleSendGMCommandMessage(INT_TO_FSTRING(PlayerID), TEXT("goto"), temp);
		}
	}
	AT_INFO(TEXT("UTeleportTask BeginTask ->Index[%d]"), Index);
}

void UTeleportTask::TickObject()
{
	Super::TickObject();
	//AT_INFO(TEXT("TickObject"));
}

bool UTeleportTask::Condition()
{
	AT_INFO(TEXT("UTeleportTask StartCheck Condition ->Index[%d]"), Index);
	if (!IsInWorld())	return false;
	const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	//客户端加载资源完成， 并且在目标地图
	if ((SpaceScriptID == ScriptID) && (!UUECS3GameInstance::Instance->GameStatus->IsCurrStatus(EGameStatus::Teleport)))
	{
		AT_INFO(TEXT("UTeleportTask Condition Is Complete ->Index[%d]"), Index);
		return true;
	}
	else
	{
		return false;
	}
}

void UTeleportTask::EndTask()
{
	Super::EndTask();
	AT_INFO(TEXT("UTeleprotTask EndTask ->Index[%d]"), Index);
}

CONTROL_COMPILE_OPTIMIZE_END
