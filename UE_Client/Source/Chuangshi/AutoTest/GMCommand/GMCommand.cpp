// Fill out your copyright notice in the Description page of Project Settings.


#include "GMCommand.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Interface/Role/RoleChatInterface.h"
#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

UGMCommand::UGMCommand()
	:Super()
{
	CustomTimeDilation = 5.0f;
}

void UGMCommand::InitParam()
{
	GMCmd = Param1.Replace(TEXT("/"), TEXT(""));
	LifeTime = FSTRING_TO_FLOAT(Param2);
	AT_INFO(TEXT("UGMCommand InitParam ->Index[%d]"), Index);
}

void UGMCommand::BeginTask()
{
	int32 PlayerID = UGolbalBPFunctionLibrary::GetPlayerID();
	if (PlayerID != 0)
	{
		TArray<FString> args;
		//args.Add(INT_TO_FSTRING(PlayerID));
		FString Cmd;
		FString Arg = TEXT("");
		if (GMCmd.Contains(TEXT(" ")))
		{
			GMCmd.Split(TEXT(" "), &Cmd, &Arg);
		}
		else
		{
			Cmd = GMCmd;
		}
		//args.Add(Cmd);
		//args.Add(Arg);
		//UGolbalBPFunctionLibrary::CellCall(PlayerID, TEXT("onRoleSendGMCommandMessage"), args);

		URoleChatInterface * RoleChatInterface = Cast<URoleChatInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleChatInterface")));
		if (RoleChatInterface)
		{
			RoleChatInterface->RPC_onRoleSendGMCommandMessage(INT_TO_FSTRING(PlayerID), Cmd, Arg);
		}
	}
	AT_INFO(TEXT("UGMCommand BeginTask ->Index[%d]"), Index);
}

void UGMCommand::TickObject()
{
	Super::TickObject();
	//AT_INFO(TEXT("TickObject"));
}

bool UGMCommand::Condition()
{
	if (GetSumTickTime() >= LifeTime)
	{
		AT_INFO(TEXT("UGMCommand Complete Condition ->Index[%d]"), Index);
		return true;
	}
	else
	{
		return false;
	}
}

void UGMCommand::EndTask()
{
	Super::EndTask();
	AT_INFO(TEXT("UGMCommand EndTask ->Index[%d]"), Index);
}

CONTROL_COMPILE_OPTIMIZE_END
