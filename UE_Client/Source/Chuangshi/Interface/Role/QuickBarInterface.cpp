// Fill out your copyright notice in the Description page of Project Settings.

#include "QuickBarInterface.h"
#include "KBEngine.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/SkillManager.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/TutorialManager.h"
#include "Manager/QuickBarManager.h"

CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(UQuickBarInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UQuickBarInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
UQuickBarInterface::UQuickBarInterface()
{

}

UQuickBarInterface::~UQuickBarInterface()
{

}

void UQuickBarInterface::onLeaveWorld()
{
	if (GetEntity() && GetEntity()->IsPlayer() && IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillManager))
	{
		UUECS3GameInstance::Instance->QuickBarManager->onLeaveWorld();
	}
	Super::onEnterWorld();
}

void UQuickBarInterface::RPC_BASE_qb_updateItem(int32 Index, int32 QbType, int32 Id, int32 BindType, int32 QuickID, int32 Page, FString petUid)
{

	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UQuickBarInterface::RPC_BASE_qb_updateItem : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(Index);
	args.Add(QbType);
	args.Add(Id);
	args.Add(BindType);
	args.Add(QuickID);
	args.Add(Page);
	args.Add(petUid);

	GetEntity()->BaseCall(TEXT("BASE_qb_updateItem"), args);
}

void UQuickBarInterface::UpdateQBItem(int32 Index, int32 QbType, int32 Id, int32 BindType, int32 QuickID, FString petUid)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UQuickBarInterface::UpdateQBItem : GetEntity()!"));
		return;
	}
	int32 skillPosture = GetEntity()->GetDefinedProperty(TEXT("skillPosture")).GetValue<int32>();
	int32 Page = (skillPosture ? skillPosture % 100 : 1) - 1;
	RPC_BASE_qb_updateItem(Index, QbType, Id, BindType, QuickID, Page, petUid);
}

void UQuickBarInterface::RPC_BASE_qb_exchangeItem(int32 SrcIndex, int32 DstIndex, int32 Page)
{
	KBEngine::FVariantArray args;
	args.Add(SrcIndex);
	args.Add(DstIndex);
	args.Add(Page);

	GetEntity()->BaseCall(TEXT("qb_exchangeItem"), args);
}

void UQuickBarInterface::ExchangeQBItem(int32 SrcIndex, int32 DstIndex)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UQuickBarInterface::ExchangeQBItem : GetEntity()!"));
		return;
	}
	int32 skillPosture = GetEntity()->GetDefinedProperty(TEXT("skillPosture")).GetValue<int32>();
	int32 Page = (skillPosture ? skillPosture % 100 : 1) - 1;
	RPC_BASE_qb_exchangeItem(SrcIndex, DstIndex, Page);
}

void UQuickBarInterface::RPC_BASE_qb_removeItem(int32 Index, int32 Page)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UQuickBarInterface::RPC_BASE_qb_removeItem : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(Index);
	args.Add(Page);

	GetEntity()->BaseCall(TEXT("BASE_qb_removeItem"), args);
}

void UQuickBarInterface::RemoveQBItem(int32 Index)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UQuickBarInterface::RemoveQBItem : GetEntity()!"));
		return;
	}
	int32 skillPosture = GetEntity()->GetDefinedProperty(TEXT("skillPosture")).GetValue<int32>();
	int32 Page = (skillPosture ? skillPosture % 100 : 1) - 1;
	RPC_BASE_qb_removeItem(Index, Page);
}

int32 UQuickBarInterface::GetSkillPosture()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UQuickBarInterface::RemoveQBItem : GetEntity()!"));
		return 0;
	}
	return GetEntity()->GetDefinedProperty(TEXT("skillPosture")).GetValue<int32>();
}

void UQuickBarInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_OnUpdateQBItem");
	ArrBlueFunc.Add("CLIENT_OnRemoveQBItem");
	Supper::InitBlueCB();
}

void UQuickBarInterface::CLIENT_OnUpdateQBItem_Implementation(int32 Index, int32 QbType, int32 Id, int32 BindType, int32 QuickID, int32 Page, const FString& petUid)
{
	UUECS3GameInstance::Instance->QuickBarManager->OnUpdateQBItem(Index, QbType, Id, BindType, Page, QuickID, petUid);
}

void UQuickBarInterface::CLIENT_OnRemoveQBItem_Implementation(int32 Page,  int32 Index)
{
	UUECS3GameInstance::Instance->QuickBarManager->OnRemoveQBItem(Page, Index);
}

CONTROL_COMPILE_OPTIMIZE_END