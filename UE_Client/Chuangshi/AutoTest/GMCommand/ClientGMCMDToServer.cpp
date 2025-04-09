


#include "ClientGMCMDToServer.h"
#include "GameData/NPCPointDatas.h"
#include "Chuangshi/Actor/Player/PlayerCharacter.h"
#include "Chuangshi.h"
#include "Util/ConvertUtil.h"
#include "Interface/Role/RoleChatInterface.h"
#include "Interface/Monster/CSkillInterface.h"


UClientGMCMDToServer::UClientGMCMDToServer()
{
	BuildMap();
}

UClientGMCMDToServer::~UClientGMCMDToServer()
{

}

UClientGMCMDToServer* UClientGMCMDToServer:: GetInstance()
{
	cs3_checkNoReentry();
	return NewObject<UClientGMCMDToServer>();
}


void UClientGMCMDToServer::BuildMap()
{
	//MethodNameMap
	MethodNameMap.Add(TEXT("gotoPoint"),&UClientGMCMDToServer::gotoPoint);
	MethodNameMap.Add(TEXT("tabAllEntity"), &UClientGMCMDToServer::tabAllEntity);
	MethodNameMap.Add(TEXT("spellCSkill"), &UClientGMCMDToServer::spellCSkill);
	MethodNameMap.Add(TEXT("spellCSkillSelf"), &UClientGMCMDToServer::spellCSkillSelf);
	MethodNameMap.Add(TEXT("addCBuff"), &UClientGMCMDToServer::addCBuff);
	MethodNameMap.Add(TEXT("addCBuffSelf"), &UClientGMCMDToServer::addCBuffSelf);
	
}

void UClientGMCMDToServer::CallFunc(int32 playerID, int32 desEntityID, const FString methodName, const FString cmdArgs)
{
	if (MethodNameMap.Contains(methodName))
	{
		(this->*(MethodNameMap[methodName]))(playerID, desEntityID,methodName, cmdArgs);

	}
	else
	{
		URoleChatInterface * RoleChatInterface = Cast<URoleChatInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleChatInterface"), playerID));
		if (RoleChatInterface)
		{
			RoleChatInterface->RPC_onRoleSendGMCommandMessage(INT_TO_FSTRING(desEntityID), methodName, cmdArgs);
		}
		//TArray<FString> args;
		//args.Add(INT_TO_FSTRING(desEntityID));
		//args.Add(methodName);
		//args.Add(cmdArgs);
		//UGolbalBPFunctionLibrary::CellCall(playerID, TEXT("onRoleSendGMCommandMessage"), args);
	}
}

void UClientGMCMDToServer::gotoPoint(int32 playerID, int32 desEntityID, FString methodName, FString cmdArgs)
{
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("int32 playerID=%d, FString methodName=%s, FString args=%s"),playerID,*methodName,*cmdArgs);
	//指令有两种格式 1./gotoPoint npcScriptID ;2./gotoPoint npcScriptID#spaceScript

	TArray<FString> argsArray = UGolbalBPFunctionLibrary::SplitString(cmdArgs, false, TEXT("#"));
	
	FVector pos = FVector::ZeroVector;	
	bool queryResult;	//如果没有在表中查到相应数据返回false
	FString strPos;
	TArray<FString> args;
	//args.Add(INT_TO_FSTRING(desEntityID));
	//args.Add(methodName);

	// /gotoPoint spaceScript#npcScriptID
	if (argsArray.Num()>1)
	{
		queryResult = UGolbalBPFunctionLibrary::GetNPCPositionFromTable(argsArray[1], argsArray[0], pos);
		if (queryResult)
		{
			strPos = argsArray[1] + "|" + pos.ToString();
			//FString strPos = argsArray[1] + "|" + pos.ToString();
			//args.Add(strPos);
		}
		else
		{
			UGolbalBPFunctionLibrary::StatusMessage(246, argsArray[0]);
			return;
		}
	}
	// /gotoPoint npcScriptID
	else
	{
		FString spaceScriptID;
		queryResult = UGolbalBPFunctionLibrary::GetNPCPositionFromTableWithNPCScriptID(argsArray[0], spaceScriptID,pos);
		if (queryResult)
		{
			strPos = spaceScriptID + "|" + pos.ToString();
			//FString strPos =spaceScriptID +"|"+ pos.ToString();
			//args.Add(strPos);
		}
		else
		{
			UGolbalBPFunctionLibrary::StatusMessage(246, argsArray[0]);
			return;
		}
		
	}
	URoleChatInterface * RoleChatInterface = Cast<URoleChatInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleChatInterface"), playerID));
	if (RoleChatInterface)
	{
		RoleChatInterface->RPC_onRoleSendGMCommandMessage(INT_TO_FSTRING(desEntityID), methodName, strPos);
	}
	//UGolbalBPFunctionLibrary::CellCall(playerID, TEXT("onRoleSendGMCommandMessage"), args);

}


void UClientGMCMDToServer::tabAllEntity(int32 playerID, int32 desEntityID, FString methodName, FString args)
{

	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UClientGMCMDToServer::tabAllEntity : PlayerActor!"));
		return;
	}
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(PlayerActor);
	if (!IsValid(PlayerCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UClientGMCMDToServer::tabAllEntity : PlayerCharacter!"));
		return;
	}
	PlayerCharacter->OnTableAllEntity(args.ToBool());
}

void UClientGMCMDToServer::spellCSkill(int32 playerID, int32 desEntityID, FString methodName, FString args)
{
	UCSkillInterface * CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), playerID));
	if (CSkillInterface)
	{
		CSkillInterface->RequestUseCSkillToEntity(FSTRING_TO_INT(args), desEntityID);
	}
}

void UClientGMCMDToServer::spellCSkillSelf(int32 playerID, int32 desEntityID, FString methodName, FString args)
{
	UCSkillInterface * CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), desEntityID));
	if (CSkillInterface)
	{
		CSkillInterface->RequestUseCSkillToEntity(FSTRING_TO_INT(args), playerID);
	}
}

void UClientGMCMDToServer::addCBuff(int32 playerID, int32 desEntityID, FString methodName, FString args)
{
	UCSkillInterface * CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), desEntityID));
	CS3Entity* caster = (CS3Entity*)UGolbalBPFunctionLibrary::FindEntity(playerID);
	if (CSkillInterface && caster)
	{

		CSkillInterface->addBuff(caster, FSTRING_TO_INT(args));
	}
}

void UClientGMCMDToServer::addCBuffSelf(int32 playerID, int32 desEntityID, FString methodName, FString args)
{
	UCSkillInterface * CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), playerID));
	CS3Entity* caster = (CS3Entity*)UGolbalBPFunctionLibrary::FindEntity(desEntityID);
	if (CSkillInterface && caster)
	{
		CSkillInterface->addBuff(caster, FSTRING_TO_INT(args));
	}
}






