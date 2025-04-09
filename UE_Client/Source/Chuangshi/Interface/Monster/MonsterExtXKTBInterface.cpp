// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtXKTBInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/EventManager.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtXKTBInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CancelDisplyCurrentText, &UMonsterExtXKTBInterface::CancelDisplyCurrentText)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(DisplyCurrentText, &UMonsterExtXKTBInterface::DisplyCurrentText, const FString&, const int32&)

CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtXKTBInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMonsterExtXKTBInterface::UMonsterExtXKTBInterface()
{
}

UMonsterExtXKTBInterface::~UMonsterExtXKTBInterface()
{
}

void UMonsterExtXKTBInterface::CancelDisplyCurrentText()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnXKTBCancelDisplayCurrentText.Broadcast();
	}
}

void UMonsterExtXKTBInterface::DisplyCurrentText(const FString& currentText, const int32& state)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnXKTBTextStatusChangeEvent.Broadcast(currentText,state);
	}
}