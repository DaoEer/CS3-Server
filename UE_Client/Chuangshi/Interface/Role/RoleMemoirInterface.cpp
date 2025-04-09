// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleMemoirInterface.h"
#include "GameData/ShortcutKeyData.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3PlayerController.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Operation/RoleCtrl/RoleCtrlStateMgr.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleMemoirInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleMemoirInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

URoleMemoirInterface::URoleMemoirInterface()
{

}

URoleMemoirInterface::~URoleMemoirInterface()
{

}

void URoleMemoirInterface::CLIENT_ReceiveMemoirIDList_Implementation(const TArray<FString>& memoirIDs)
{
	for (auto memoirID : memoirIDs)
	{
		MemoirIDList.Add(memoirID);
	}
	ReceiveMemoirIDListCB(MemoirIDList);
}

void URoleMemoirInterface::CLIENT_AddMemoirStory_Implementation(const FString& memoirID, const FString& nextMemoirID)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****|memoirID %s |*****"), *memoirID);
	if (MemoirIDList.Contains(memoirID))
		return;
	MemoirIDList.Add(memoirID);
	ShowMemoirStory(memoirID,nextMemoirID);
}

void URoleMemoirInterface::CLIENT_PlayMemoirCG_Implementation(const FString& memoirCGID, const FString& memoirID)
{

}

void URoleMemoirInterface::TriggerMemoirState(bool IsTrigger)
{
	if (UUECS3GameInstance::Instance->bIsShutDown)
	{
		return;
	}

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsTrigger)
	{
		PlayerController->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_MEMOIR, true);
		// 鼠标显示与隐藏
		PlayerController->bShowMouseCursor = false;
	}
	else
	{
		PlayerController->GetStateCtrlComp()->OnLeaveState(EROLE_CTRL_STATE::RCS_MEMOIR);
		// 鼠标显示与隐藏
		PlayerController->bShowMouseCursor = true;
	}
}

void URoleMemoirInterface::CELL_endPlayMemoirCG()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleMemoirInterface::CELL_endPlayMemoirCG : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_endPlayMemoirCG"), args);
}

void URoleMemoirInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_ReceiveMemoirIDList");
	ArrBlueFunc.Add("CLIENT_AddMemoirStory");
	ArrBlueFunc.Add("CLIENT_PlayMemoirCG");
	Supper::InitBlueCB();
}

