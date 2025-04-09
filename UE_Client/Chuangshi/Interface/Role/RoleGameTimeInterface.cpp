#include "RoleGameTimeInterface.h"
#include "KBEngine.h"
#include "GameDevelop/CS3GameInstance.h"


CS3_BEGIN_INTERFACE_METHOD_MAP(URoleGameTimeInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnGameTimeBalanceCountDown, &URoleGameTimeInterface::OnGameTimeBalanceCountDown, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(ShowStartBillingWnd, &URoleGameTimeInterface::ShowStartBillingWnd, const int32&, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(HideStartBillingWnd, &URoleGameTimeInterface::HideStartBillingWnd)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleGameTimeInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

URoleGameTimeInterface::URoleGameTimeInterface()
{
}


URoleGameTimeInterface::~URoleGameTimeInterface()
{
}

void URoleGameTimeInterface::OnGameTimeBalanceCountDown(const int32& TimeBalance)
{
	
}

void URoleGameTimeInterface::ShowStartBillingWnd(const int32& Level, const int32& CountDownTime)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("TopUpTips"));
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnShowStartBillingWnd.Broadcast(Level, CountDownTime);
	}
}

void URoleGameTimeInterface::HideStartBillingWnd()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnHideStartBillingWnd.Broadcast();
	}
}
