// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleTradeInterface.h"
#include "Actor/Player/PlayerCharacter.h"
#include "KBEngine.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/CustomTimerManager.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "CS3Base/BaseWindow.h"
#include "CS3Base/UIManager.h"
#include "Manager/MessageManager.h"

CONTROL_COMPILE_OPTIMIZE_START
	
CS3_BEGIN_INTERFACE_METHOD_MAP(URoleTradeInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_onMoneyChange, &URoleTradeInterface::CLIENT_onMoneyChange, const int64&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_onDstMoneyChange, &URoleTradeInterface::CLIENT_onDstMoneyChange, const int64&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleTradeInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
URoleTradeInterface::URoleTradeInterface()
{
	RoleTradeState = TRADE_STATE::TRADE_STATE_NULL;
}

URoleTradeInterface::~URoleTradeInterface()
{
}

void URoleTradeInterface::CLIENT_onDstTradeSure_Implementation(int32 state)
{

}

void URoleTradeInterface::CLIENT_onDstTradeLock_Implementation(int32 isLock)
{

}

void URoleTradeInterface::CLIENT_onRoleTrade_Implementation(int32 id, const FString& name)
{
	OppositeEntityID = id;
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(TimerHander, this, &URoleTradeInterface::detectTradeObject, 1.0, true);

	if (IsCanTrade())
	{
		//弹出邀请交易提示框
		TWeakObjectPtr<URoleTradeInterface> DelayThisPtr(this);
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(1400, name, FBtnClick::CreateLambda([DelayThisPtr](RT_BTN_TYPE BtnType)
		{
			if (DelayThisPtr.IsValid())
			{
				URoleTradeInterface* ThisPtr = DelayThisPtr.Get();
				if (IsValid(ThisPtr))
				{
					if (BtnType == RT_BTN_TYPE::RT_OK)
					{
						if (ThisPtr->GetRoleTradeState() == TRADE_STATE::TRADE_STATE_WAIT)
						{
							//同意交易
							ThisPtr->RPC_CELL_agreeRoleTrade();
						}
					}
					else
					{
						//取消交易
						ThisPtr->RPC_CELL_cancelRoleTrade();
					}
				}
			}
		}));
	}
	else
	{
		//邮件、商店、商城界面打开时，玩家若收到交易邀请，则不会收到任何提示，发起交易的一方收到提示“对方正忙”
		CS3Entity* OppositeEntity = static_cast<CS3Entity*>(UUECS3GameInstance::Instance->pKBEApp->FindEntity(OppositeEntityID));
		if (OppositeEntity == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::RPC_OnRoleChaseEntityOver : entity!"));
			return;
		}
		KBEngine::FVariantArray Args;
		OppositeEntity->CellCall(TEXT("onOppositeCantTrade"), Args);
	}
}

void URoleTradeInterface::CLIENT_tradeOvertime_Implementation()
{

}

void URoleTradeInterface::CLIENT_onTradeState_Implementation(int32 TradeState)
{
	RoleTradeState = (TRADE_STATE)TradeState;
	OnNotfiyRoleTradeStateBp();

	//PC与pc间的交易
	APlayerCharacter* MyPlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (IsValid(MyPlayerCharacter))
	{
		if (RoleTradeState == TRADE_STATE::TRADE_STATE_BEGIN)
		{
			OnChangeTradeState(true);
			///UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(TimerHander, this, &URoleTradeInterface::detectTradeObject, 1.0, true);
		}
		else if (RoleTradeState == TRADE_STATE::TRADE_STATE_NULL)
		{
			OnChangeTradeState(false);
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(TimerHander);
		}
	}
}

void URoleTradeInterface::CLIENT_onMoneyChange(const int64& money)
{
	CLIENT_onMoneyChangeBP(money);
}

void URoleTradeInterface::CLIENT_onMoneyChangeBP_Implementation(int64 money)
{

}

void URoleTradeInterface::CLIENT_onDstMoneyChange(const int64& money)
{
	CLIENT_onDstMoneyChangeBP(money);
}

void URoleTradeInterface::CLIENT_onDstMoneyChangeBP_Implementation(int64 money)
{

}

void URoleTradeInterface::CLIENT_onItemAdd_Implementation(const int32& swapOrder, const int32& kitOrder, const int32& amount)
{

}

void URoleTradeInterface::CLIENT_onDstItemAdd_Implementation(int32 swapOrder, const FString& itemInst)
{

}

void URoleTradeInterface::CLIENT_onItemRemove_Implementation(int32 swapOrder)
{

}

void URoleTradeInterface::CLIENT_onDstItemRemove_Implementation(int32 swapOrder)
{

}

void URoleTradeInterface::CLIENT_onItemSwap_Implementation(const int32& swapOrder, const int32& kitOrder, const int32& amount)
{

}

void URoleTradeInterface::CLIENT_onDstItemSwap_Implementation(const int32& swapOrder, const FString& itemInst)
{

}

void URoleTradeInterface::OnChangeTradeState(bool IsTrading)
{
	APlayerCharacter* MyPlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (IsValid(MyPlayerCharacter))
	{
		MyPlayerCharacter->SetRoleInteractive(IsTrading);
		if (IsTrading)
		{
			MyPlayerCharacter->StopRandomAction();
		}
	}
}

void URoleTradeInterface::requestRoleTrade(int32 TargetID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeleportInterface::requestRoleTrade : GetEntity()!"));
		return;
	}
	if(GetRoleTradeState() != TRADE_STATE::TRADE_STATE_NULL) return;
	int32 targetFlag = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetID, TEXT("forbidRoleTrade"));
	if (targetFlag == 1)
	{
		UGolbalBPFunctionLibrary::StatusMessage(1414, TEXT(""));
		return;
	}
	//邮件、商店、商城界面打开时，玩家若想发起交易，则弹出提示“该界面下，无法进行交易”, ID 1420
	if (!IsCanTrade())
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(1420);
		return;
	}
	//保存对方ID
	OppositeEntityID = TargetID;
	//请求服务器
	KBEngine::FVariantArray args;
	args.Add(TargetID);
	this->GetEntity()->CellCall(TEXT("CELL_requestRoleTrade"), args);
}

void URoleTradeInterface::OnLeaveTargetByRequest_Implementation()
{
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("CELL_onLeaveTargetByRequest"), args);
	UGolbalBPFunctionLibrary::StatusMessage(1416, TEXT(""));
}

void URoleTradeInterface::setForbidRoleTradeFC(int32 IsForbidRoleTrade)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeleportInterface::setForbidRoleTradeFC : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(IsForbidRoleTrade);
	this->GetEntity()->CellCall(TEXT("CELL_setForbidRoleTradeFC"), args);
}

void URoleTradeInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_onRoleTrade");
	ArrBlueFunc.Add("CLIENT_tradeOvertime");
	ArrBlueFunc.Add("CLIENT_onTradeState");
	ArrBlueFunc.Add("CLIENT_onDstTradeLock");
	ArrBlueFunc.Add("CLIENT_onDstTradeSure");
	//ArrBlueFunc.Add("CLIENT_onMoneyChange");
	//ArrBlueFunc.Add("CLIENT_onDstMoneyChange");
	ArrBlueFunc.Add("CLIENT_onItemAdd");
	ArrBlueFunc.Add("CLIENT_onDstItemAdd");
	ArrBlueFunc.Add("CLIENT_onItemSwap");
	ArrBlueFunc.Add("CLIENT_onDstItemSwap");
	ArrBlueFunc.Add("CLIENT_onItemRemove");
	ArrBlueFunc.Add("CLIENT_onDstItemRemove");
	ArrBlueFunc.Add("CLIENT_setForbidRoleTradeFC");
	Supper::InitBlueCB();
}

TRADE_STATE URoleTradeInterface::GetRoleTradeState()
{
	return RoleTradeState;
}

bool URoleTradeInterface::IsCanTrade()
{
	//邮件、商店、商城界面打开时，不能发起交易，也不能收到交易邀请
	UBaseWindow* Mailindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("Mail"));
	UBaseWindow* NPCShopWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("NPCShop"));
	UBaseWindow* MallWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("Mall"));
	if ((IsValid(Mailindow) && Mailindow->IsVisible()) || (IsValid(NPCShopWindow) && NPCShopWindow->IsVisible()) || (IsValid(MallWindow) && MallWindow->IsVisible()))
	{
		return false;
	}
	return true;
}

void URoleTradeInterface::detectTradeObject()
{
	if (OppositeEntityID)
	{
		AActor* player = GetActor();
		AActor* target = UGolbalBPFunctionLibrary::GetActorByID(OppositeEntityID);
		if (!IsValid(player) || !IsValid(target))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(TimerHander);
			return;
		}
		if (player->GetDistanceTo(target) >= 1000)			// 两者距离10米，取消交易
		{
			 if (RoleTradeState == TRADE_STATE::TRADE_STATE_WAIT)
			 {
				 OnLeaveTargetByRequest();
			 }
			 else
			 {
				 KBEngine::FVariantArray args;
				 CellCall(TEXT("CELL_onLeaveTarget"), args);
				 UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(TimerHander);
			 }
			
			//UUECS3GameInstance::Instance->MessageManager->ShowMessage(1416);
		}
	}
	

}

void URoleTradeInterface::RPC_CELL_agreeRoleTrade()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeleportInterface::RPC_CELL_agreeRoleTrade : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_agreeRoleTrade"), args);
}

void URoleTradeInterface::RPC_CELL_cancelRoleTrade()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeleportInterface::RPC_CELL_cancelRoleTrade : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_cancelRoleTrade"), args);
}

void URoleTradeInterface::RPC_CELL_requestRoleTradeMoneyChange(const int64& MoneyValue)
{
	if (GetRoleTradeState() != TRADE_STATE::TRADE_STATE_BEGIN)
	{
		return;
	}
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeleportInterface::RPC_CELL_requestRoleTradeMoneyChange : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(INT64_TO_FSTRING(MoneyValue));

	entity->CellCall(TEXT("CELL_requestRoleTradeMoneyChange"), args);
}

void URoleTradeInterface::RPC_CELL_requestRoleTradeItemAdd(const FString& STRING_1, const FString& STRING_2, const FString& STRING_3)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeleportInterface::RPC_CELL_requestRoleTradeItemAdd : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(STRING_2);
	args.Add(STRING_3);

	entity->CellCall(TEXT("CELL_requestRoleTradeItemAdd"), args);
}

void URoleTradeInterface::RPC_CELL_requestRoleTradeItemRemove(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeleportInterface::RPC_CELL_requestRoleTradeItemRemove : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);

	entity->CellCall(TEXT("CELL_requestRoleTradeItemRemove"), args);
}

void URoleTradeInterface::RPC_CELL_requestRoleTradeLock()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeleportInterface::RPC_CELL_requestRoleTradeLock : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_requestRoleTradeLock"), args);
}

void URoleTradeInterface::RPC_CELL_cancelRoleTradeLock()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeleportInterface::RPC_CELL_cancelRoleTradeLock : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_cancelRoleTradeLock"), args);
}

void URoleTradeInterface::RPC_CELL_requestRoleTradeSure()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleTeleportInterface::RPC_CELL_requestRoleTradeSure : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_requestRoleTradeSure"), args);
}

CONTROL_COMPILE_OPTIMIZE_END
