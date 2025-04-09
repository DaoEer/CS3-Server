// Fill out your copyright notice in the Description page of Project Settings.

#include "NPCQuestInterface.h"
#include "KBEngine.h"
#include "Util/CS3Debug.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UNPCQuestInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UNPCQuestInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UNPCQuestInterface::UNPCQuestInterface()
{

}

UNPCQuestInterface::~UNPCQuestInterface()
{

}

void UNPCQuestInterface::RequestQuestStatus()
{
	if (this->GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("--UNPCQuestInterface::RequestQuestStatus no this Entity!%d"), EntityID);
		return;
	}
	KBEngine::FVariantArray Args;
	this->GetEntity()->CellCall(TEXT("questStatusApply"), Args);
}

void UNPCQuestInterface::CLIENT_SetQuestSign_Implementation(int32 flag)
{
	SetQuestSign_Implementation(flag);
}

void UNPCQuestInterface::SetQuestSign_Implementation(int32 flag)
{

}

void UNPCQuestInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_SetQuestSign");
	Supper::InitBlueCB();
}

void UNPCQuestInterface::RPC_questDataApplyByClick(const FString& STRING_1, const FString& STRING_2)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UNPCQuestInterface::RPC_questDataApplyByClick : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(STRING_2);

	entity->CellCall(TEXT("questDataApplyByClick"), args);
}

