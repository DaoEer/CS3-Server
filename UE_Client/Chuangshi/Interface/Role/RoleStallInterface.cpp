// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleStallInterface.h"

#include "Json.h"
#include "JsonFieldData.h"
#include "GameData/StallData.h"

#include "Util/ConvertUtil.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/Player/PlayerCharacter.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Operation/RoleCtrl/RoleCtrlStateMgr.h"
#include "Manager/Operation/ControllerModeMgr.h"
#include "GameData/Item/ItemFactory.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CustomTimerManager.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Util/CS3Debug.h"
#include "Entity/Alias.h"

CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleStallInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_AddCollectionItemSuccessCB, &URoleStallInterface::CLIENT_AddCollectionItemSuccessCB, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_UpdateStallCollectionItemCB, &URoleStallInterface::CLIENT_UpdateStallCollectionItemCB, const int32&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_AddStallSellItemSuccessCB, &URoleStallInterface::CLIENT_AddStallSellItemSuccessCB, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_UpdateStallSellItemCB, &URoleStallInterface::CLIENT_UpdateStallSellItemCB, const int32&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_UpdateStallItem, &URoleStallInterface::CLIENT_UpdateStallItem, const int32& , const int32& , const int32&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_StallItemSuccessToClient, &URoleStallInterface::CLIENT_StallItemSuccessToClient, const int32&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_AddStallRecord, &URoleStallInterface::CLIENT_AddStallRecord, const int32&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnReceiveOtherStallItems, &URoleStallInterface::CLIENT_OnReceiveOtherStallItems, const int32& , const FString&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnRequestStallItems, &URoleStallInterface::CLIENT_OnRequestStallItems,  const FString&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_UpdateOtherStallItems, &URoleStallInterface::CLIENT_UpdateOtherStallItems, const int32&, const FVariant&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleStallInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
class APlayerCharacter;

URoleStallInterface::URoleStallInterface()
{

}


URoleStallInterface::~URoleStallInterface()
{

}

void URoleStallInterface::FindStallPoint()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::findStallPoint : GetEntity()!"));
		return;
	}

	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("CELL_findStallPoint"), args);
}

void URoleStallInterface::CLIENT_OnFindStallPoint(FString& ScriptID, const FString& Number)
{
	const UConfigTable* CfgTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_STALL_DATA);
	if (IsValid(CfgTable))
	{
		const FStallData* stallData = CfgTable->GetRow<FStallData>(FSTRING_TO_FNAME(ScriptID));
		if (stallData != nullptr)
		{
			for (auto point : stallData->StallPoint)
			{
				if (point.id == FSTRING_TO_INT(Number))
				{
					APlayerCharacter* playerActor = Cast<APlayerCharacter>(GetActor());
					if (IsValid(playerActor))
					{
						StallScriptID = ScriptID;
						StallPoint = Number;
						playerActor->StartCrossMapNavigate(ScriptID, false, TEXT(""), TEXT(""), point.position, 1.0, 0, ENUM_NAVIGATE_ACTION_TYPE::NavigateActionStall);
						CS3_Display(CS3DebugType::CL_Undefined, TEXT("Stall start navigate!!"));
						return;
					}
				}
			}
			CS3_Warning(TEXT("Stall navigate err!!Please check config(Name:%s, id:%s)"), *ScriptID, *Number);
		}
	}
}

void URoleStallInterface::OnNavigateStallFinish()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Stall end navigate!!"));
	const UConfigTable* CfgTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_STALL_DATA);
	if (IsValid(CfgTable))
	{
		const FStallData* stallData = CfgTable->GetRow<FStallData>(FSTRING_TO_FNAME(StallScriptID));
		if (stallData != nullptr)
		{
			for (auto point : stallData->StallPoint)
			{
				if (point.id == FSTRING_TO_INT(StallPoint))
				{
					APlayerCharacter* playerActor = Cast<APlayerCharacter>(GetActor());
					if (IsValid(playerActor))
					{
						if ( FVector::Dist(playerActor->GetActorLocation(),point.position) <= 200.0f )		/// 成功移动到目标点
						{
							//player->SetActorRotation(point.direction.Rotation());
							ACS3PlayerController* playerContorller = Cast<ACS3PlayerController>(UGolbalBPFunctionLibrary::GetCS3PlayerController());
							if (IsValid(playerContorller)&&IsValid(playerContorller->GetStateCtrlComp())&& playerActor->ActorIsPlayer())
							{
								playerContorller->SetStateCtrlComp(EROLE_CTRL_STATE::RCS_STALL, true);
							}
							KBEngine::FVariantArray args;
							CellCall(TEXT("CELL_onNavigateStallFinish"), args);
							playerActor->SetActorRotation(FRotator(0, point.direction.Z, 0));
							OnShowStall();
							return;
						}
					}
				}
			}
			// 移动失败
			CancelStall();
		}
	}
	
}

void URoleStallInterface::OnNavigateStallFail()
{
	CancelStall();
	UGolbalBPFunctionLibrary::StatusMessage(1829, TEXT(""));
}

void URoleStallInterface::OnEnterStall_Implementation()
{

}

void URoleStallInterface::OnLevelStall_Implementation()
{

}

void URoleStallInterface::StartStall()
{
	UControllerModeMgr* ControllerModeMgr = UGolbalBPFunctionLibrary::ControllerModeMgr();

	if (IsValid(ControllerModeMgr))
	{
		TArray<FString> OtherValue;	
		ControllerModeMgr->ExecuteInputInfor(TEXT("OnStartStall"), TEXT(""), 0.0f, OtherValue);
	}
	else
	{
		FindStallPoint();
	}	
}

void URoleStallInterface::CancelStall()
{
	if (!StallPoint.IsEmpty())
	{
		StallPoint.Empty();
		StallScriptID.Empty();
	}
	ACS3PlayerController* playerContorller = Cast<ACS3PlayerController>(UGolbalBPFunctionLibrary::GetCS3PlayerController());
	if (IsValid(playerContorller) && IsValid(playerContorller->GetStateCtrlComp()) &&
		IsValid(GetActor())&& IsValid(Cast<APlayerCharacter>(GetActor()))&& Cast<APlayerCharacter>(GetActor())->ActorIsPlayer() &&
		playerContorller->GetStateCtrlComp()->IsHaveState(EROLE_CTRL_STATE::RCS_STALL))
	{
		playerContorller->GetStateCtrlComp()->OnLeaveState(EROLE_CTRL_STATE::RCS_STALL);
	}
	KBEngine::FVariantArray args;
	CellCall(TEXT("CELL_cancelStall"), args);
}

void URoleStallInterface::OnShowStall_Implementation()
{

}

void URoleStallInterface::StallItem()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("StallItem"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::StallItem : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::StallItem : pEntity_Player->IsPlayerRole()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(FVariant(StallName));
	player->CellCall(TEXT("CELL_startStall"), args);
}

void URoleStallInterface::EndStall()
{
	ACS3PlayerController* playerContorller = Cast<ACS3PlayerController>(UGolbalBPFunctionLibrary::GetCS3PlayerController());
	if (IsValid(playerContorller) && IsValid(playerContorller->GetStateCtrlComp()) &&
		IsValid(GetActor()) && IsValid(Cast<APlayerCharacter>(GetActor())) && Cast<APlayerCharacter>(GetActor())->ActorIsPlayer() &&
		playerContorller->GetStateCtrlComp()->IsHaveState(EROLE_CTRL_STATE::RCS_STALL))
	{
		playerContorller->GetStateCtrlComp()->OnLeaveState(EROLE_CTRL_STATE::RCS_STALL);
	}
	KBEngine::FVariantArray args;
	CellCall(TEXT("CELL_endStall"), args);
}

void URoleStallInterface::CLIENT_RemoveStallCollectionItemCB_Implementation(const int32& playerID, const int32& slot)
{
	if (playerID == EntityID)
	{
		if (CollectionItemList.IsValidIndex(slot))
		{
			CollectionItemList.RemoveAt(slot);
		}
	}
	else
	{
		if (OtherCollectionItemList.IsValidIndex(slot))
		{
			OtherCollectionItemList.RemoveAt(slot);
		}
	}
}

void URoleStallInterface::OnLeaveTargetStall_Implementation()
{

}

void URoleStallInterface::CLIENT_UpdateStallCollectionItemCB(const int32& slot, const FVariant& data)
{
	TEMP_ITEM_DATA tempItemDta;
	TEMP_ITEM_DATA::CreateFromVariant(data, tempItemDta);
	FStallItemData item;
	item.Id = tempItemDta.id;
	item.ItemID = tempItemDta.itemID;
	item.Amount = tempItemDta.amount;
	item.Price = tempItemDta.price;
	CollectionItemList.Add(item);
	if (CollectionItemList.IsValidIndex(slot))
	{
		CollectionItemList.RemoveAt(slot);
		CollectionItemList.Insert(item, slot);
	}
	CLIENT_UpdateStallCollectionItemCBBP(slot);
}

void URoleStallInterface::CLIENT_UpdateStallCollectionItemCBBP_Implementation(const int32& slot)
{

}

void URoleStallInterface::CLIENT_AddCollectionItemSuccessCB(const FVariant& data)
{
	TEMP_ITEM_DATA tempItemDta;
	TEMP_ITEM_DATA::CreateFromVariant(data, tempItemDta);
	FStallItemData item;
	item.Id = tempItemDta.id;
	item.ItemID = tempItemDta.itemID;
	item.Amount = tempItemDta.amount;
	item.Price = tempItemDta.price;
	CollectionItemList.Add(item);
	CLIENT_AddCollectionItemSuccessCBBP();
}
void URoleStallInterface::CLIENT_AddCollectionItemSuccessCBBP_Implementation()
{

}

void URoleStallInterface::CLIENT_StallSuccessCB_Implementation(const int32& tax)
{

}

void URoleStallInterface::CLIENT_AddStallSellItemSuccessCB(const FVariant& data)
{
	TEMP_ITEM_DATA tempItemDta;
	TEMP_ITEM_DATA::CreateFromVariant(data, tempItemDta);
	FStallItemData item;
	item.Id = tempItemDta.id;
	item.ItemID = tempItemDta.itemID;
	item.Amount = tempItemDta.amount;
	item.Price = tempItemDta.price;
	StallSellItemList.Add(item);
	CLIENT_AddStallSellItemSuccessCBBP();
}

void URoleStallInterface::CLIENT_AddStallSellItemSuccessCBBP_Implementation()
{

}

void URoleStallInterface::CLIENT_UpdateStallSellItemCB(const int32& slot, const FVariant& data)
{
	TEMP_ITEM_DATA tempItemDta;
	TEMP_ITEM_DATA::CreateFromVariant(data, tempItemDta);
	FStallItemData item;
	item.Id = tempItemDta.id;
	item.ItemID = tempItemDta.itemID;
	item.Amount = tempItemDta.amount;
	item.Price = tempItemDta.price;
	CollectionItemList.Add(item);
	if (StallSellItemList.IsValidIndex(slot))
	{
		StallSellItemList.RemoveAt(slot);
		StallSellItemList.Insert(item, slot);
	}
	CLIENT_UpdateStallSellItemCBBP(slot);
}
void URoleStallInterface::CLIENT_UpdateStallSellItemCBBP_Implementation(const int32& slot)
{
	
}


void URoleStallInterface::CLIENT_RemoveStallSellItemCB_Implementation(const int32& playerID, const int32& slot)
{
	if (playerID == EntityID)
	{
		if (StallSellItemList.IsValidIndex(slot))
		{
			StallSellItemList.RemoveAt(slot);
		}
	}
	else
	{
		if (OtherStallSellItemList.IsValidIndex(slot))
		{
			OtherStallSellItemList.RemoveAt(slot);
		}
	}
}

void URoleStallInterface::CLIENT_OnReceiveOtherStallItems(const int32& TargetID, const FString& TempStallName, const FVariant& data)
{
	BUY_AND_SELL_DATAS datas = BUY_AND_SELL_DATAS(data);
	OtherCollectionItemList.Empty();
	for (auto d : datas.stallCollectionItemList)
	{
		FStallItemData item;
		item.Id = d.id;
		item.ItemID = d.itemID;
		item.Amount = d.amount;
		item.Price = d.price;
		OtherCollectionItemList.Add(item);
	}
	OtherStallSellItemList.Empty();
	int32 index = 0;
	for (auto d : datas.stallSellItemList)
	{
		UItemBase* item = UItemFactory::GetItemByID(d.itemID);
		if (item)
		{
			item->UID = d.id;
			item->Amount = d.amount;
			item->Price = d.price;
			item->ItemOrder = index;
			index += 1;

			int32 combatPowner = d.combatPower;
			FString attackStr = d.attackPropertiesStr;
			FString attachStr = d.attachPropertiesStr;
			FString intensifyStr = d.intensifyDataStr;
			int32 hardiness = d.hardiness;
			item->SetDynamicProperty(combatPowner, attackStr, attachStr, intensifyStr, hardiness);

			OtherStallSellItemList.Add(item);

		}
	}
	
	TWeakObjectPtr<URoleStallInterface> DelayThisPtr(this);
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, timer, FTimerDelegate::CreateLambda([TargetID, DelayThisPtr]()
		{
			if (DelayThisPtr.IsValid())
			{
				URoleStallInterface* ThisPtr = DelayThisPtr.Get();
				AActor* player = ThisPtr->GetActor();
				AActor* target = UGolbalBPFunctionLibrary::GetActorByID(TargetID);
				if (!IsValid(player) || !IsValid(target))
				{
					ThisPtr->OnLeaveTargetStall();
					if (!IsValid(UUECS3GameInstance::Instance))
					{
						UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ThisPtr->timer);
					}
					return;
				}
				if (player->GetDistanceTo(target) >= 1000)
				{
					ThisPtr->OnLeaveTargetStall();
					if (IsValid(UUECS3GameInstance::Instance))
					{
						UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(ThisPtr->timer);
					}
					return;
				}
			}

		}), 1, true);
	}
	CLIENT_OnReceiveOtherStallItemsBP(TargetID, TempStallName);
}

void URoleStallInterface::CLIENT_OnReceiveOtherStallItemsBP_Implementation(const int32& TargetID, const FString& TempStallName)
{

}

void URoleStallInterface::CLIENT_UpdateStallItem(const int32& type, const int32& slot, const int32& playerID, const FVariant& data)
{
	TEMP_ITEM_DATA tempItemDta;
	TEMP_ITEM_DATA::CreateFromVariant(data, tempItemDta);
	FString UID = tempItemDta.id;
	int32 itemID = tempItemDta.itemID;
	int32 amount = tempItemDta.amount;
	int32 price = tempItemDta.price;
	if (playerID == EntityID)
	{
		// 出售
		if (type == 0)
		{
			if (StallSellItemList.IsValidIndex(slot))
			{
				StallSellItemList[slot].Id = UID;
				StallSellItemList[slot].ItemID = itemID;
				StallSellItemList[slot].Amount = amount;
				StallSellItemList[slot].Price = price;
			}
		}
		// 收购
		else
		{
			if (CollectionItemList.IsValidIndex(slot))
			{
				CollectionItemList[slot].Id = UID;
				CollectionItemList[slot].ItemID = itemID;
				CollectionItemList[slot].Amount = amount;
				CollectionItemList[slot].Price = price;
			}
		}
	}
	else
	{
		// 出售
		if (type == 0)
		{
			for (auto item : OtherStallSellItemList)
			{
				if (item->UID.Equals(UID) && item->ItemID == itemID)
				{
					item->Amount = amount;
					item->Price = price;
					break;
				}
			}
		}
		// 收购
		else
		{
			if (OtherCollectionItemList.IsValidIndex(slot))
			{
				OtherCollectionItemList[slot].Id = UID;
				OtherCollectionItemList[slot].ItemID = itemID;
				OtherCollectionItemList[slot].Amount = amount;
				OtherCollectionItemList[slot].Price = price;
			}
		}
	}
	CLIENT_UpdateStallItemBP(type, slot, playerID);
}
void URoleStallInterface::CLIENT_UpdateOtherStallItems(const int32 & TargetID, const FVariant & data)
{
	BUY_AND_SELL_DATAS datas = BUY_AND_SELL_DATAS(data);
	for (int i = datas.stallCollectionItemList.Num(); i< OtherCollectionItemList.Num(); i++ )
	{
		CLIENT_RemoveStallCollectionItemCB(TargetID, i);
	}
	OtherCollectionItemList.Empty();
	int k = 0;
	for (auto d : datas.stallCollectionItemList)
	{
		FStallItemData item;
		item.Id = d.id;
		item.ItemID = d.itemID;
		item.Amount = d.amount;
		item.Price = d.price;
		OtherCollectionItemList.Add(item);
		CLIENT_UpdateStallItemBP(1, k, TargetID);
		k++;
	}
	

}

void URoleStallInterface::CLIENT_UpdateStallItemBP_Implementation(const int32& type, const int32& slot, const int32& playerID)
{

}
void URoleStallInterface::CLIENT_StallItemSuccessToClient(const int32& type, const FVariant& data)
{
	BUY_ITEM_RECORD_DATA tempItemDta;
	BUY_ITEM_RECORD_DATA::CreateFromVariant(data, tempItemDta);
	FString stallName_temporary = tempItemDta.stallName;
	FString ItemName = tempItemDta.itemName;
	int32 Amount = tempItemDta.amount;
	int32 TotalPrice = tempItemDta.totalPrice;
	StallItemSuccess(type, stallName_temporary, INT_TO_FSTRING(Amount), ItemName, TotalPrice);
	CLIENT_StallItemSuccessToClientBP(type, stallName_temporary, ItemName, Amount, TotalPrice);
}
void URoleStallInterface::CLIENT_StallItemSuccessToClientBP_Implementation(const int32& type, const FString& stallName, const FString& ItemName, const int32& Amount, const int32& TotalPric)
{

}


void URoleStallInterface::StallItemSuccess_Implementation(const int32& type, const FString& stallName, const FString& Amount, const FString& ItemName, int64 TotalPrice)
{


}
void URoleStallInterface::CLIENT_AddStallRecord(const int32& type, const FVariant& data)
{
	TEMP_SELL_RECORD_DATA tempSellRecord;
	TEMP_SELL_RECORD_DATA::CreateFromVariant(data, tempSellRecord);
	FStallRecordData recordData;
	recordData.PlayerName = tempSellRecord.playerName;
	recordData.Amount = tempSellRecord.amount;
	recordData.Time = tempSellRecord.time;
	recordData.ItemName = tempSellRecord.itemName;
	recordData.Tax = tempSellRecord.tax;
	recordData.TotalPrice = tempSellRecord.totalPrice;

	// 0 表示出售的(暂未定义枚举)
	if (type == 0)
	{
		StallSellItemRecordList.Add(recordData);
	}
	else
	{
		StallCollectItemRecordList.Add(recordData);
	}
	CLIENT_AddStallRecordBP(type,recordData);
}

void URoleStallInterface::CLIENT_AddStallRecordBP_Implementation(const int32& type,const FStallRecordData& recordData)
{

}

void URoleStallInterface::CLIENT_OnRequestStallItems(const FString& stallName, const FVariant& data)
{

	SetStallName(stallName);
	StallSellItemList.Empty();
	ON_REQUEST_STALL_ITEMS_DATAS datas = ON_REQUEST_STALL_ITEMS_DATAS(data);
	for (auto d : datas.stallSellItemList)
	{
		FStallItemData item;
		item.Id = d.id;
		item.ItemID = d.itemID;
		item.Amount = d.amount;
		item.Price = d.price;
		StallSellItemList.Add(item);
	}
	

	CollectionItemList.Empty();
	for (auto d : datas.stallCollectionItemList)
	{
		FStallItemData item;
		item.Id = d.id;
		item.ItemID = d.itemID;
		item.Amount = d.amount;
		item.Price = d.price;
		CollectionItemList.Add(item);
	}

	CLIENT_OnRequestStallItemsBP();
}

void URoleStallInterface::CLIENT_OnRequestStallItemsBP_Implementation()
{

}

void URoleStallInterface::SetStallName(const FString& name)
{
	StallName = name;
	if (StallName.Len() == 0)
	{
		StallName = UGolbalBPFunctionLibrary::GetEntityPropertyValue(EntityID, TEXT("playerName")) + UGolbalBPFunctionLibrary::GetChinese(TEXT("StallNameSuffix"));
	}
}

void URoleStallInterface::OpenRoleStall(const int32& playerID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::OpenRoleStall : GetEntity()!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****OpenRoleStall*****"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::OpenRoleStall : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::OpenRoleStall : pEntity_Player->IsPlayerRole()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add((int32)playerID);
	this->GetEntity()->CellCall(TEXT("CELL_openRoleStall"), args);
}

void URoleStallInterface::AddStallCollectionItem(const int32& itemID, const int32& amount, const int64& price)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::AddStallCollectionItem : GetEntity()!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****AddStallCollectionItem*****"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::AddStallCollectionItem : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::AddStallCollectionItem : pEntity_Player->IsPlayerRole()!"));
		return;
	}
	ENTITY_STATE RoleState = (ENTITY_STATE)UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("state"));
	if (RoleState == ENTITY_STATE::EntityStateStall)
	{
		return;
	}
	KBEngine::FVariantArray args;
	args.Add((int32)itemID);
	args.Add((int32)amount);
	args.Add((int32)price);
	this->GetEntity()->CellCall(TEXT("CELL_addStallCollectionItem"), args);
}

void URoleStallInterface::UpdateStallCollectionItem(const int32& slot, const int32& itemID, const int32& amount, const int64& price)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::UpdateStallCollectionItem : GetEntity()!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****UpdateStallCollectionItem*****"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::AddStallCollectionItem : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::AddStallCollectionItem : pEntity_Player->IsPlayerRole()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add((int32)slot);
	args.Add((int32)itemID);
	args.Add((int32)amount);
	args.Add((int32)price);
	this->GetEntity()->CellCall(TEXT("CELL_updateStallCollectionItem"), args);
}

void URoleStallInterface::RemoveStallCollectionItem(const int32& slot, const int32& itemID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::RemoveStallCollectionItem : GetEntity()!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****RemoveStallCollectionItem*****"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::RemoveStallCollectionItem : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::RemoveStallCollectionItem : pEntity_Player->IsPlayerRole()!"));
		return;
	}
	ENTITY_STATE RoleState = (ENTITY_STATE)UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("state"));
	if (RoleState == ENTITY_STATE::EntityStateStall)
	{
		return;
	}
	KBEngine::FVariantArray args;
	args.Add((int32)slot);
	args.Add((int32)itemID);
	this->GetEntity()->CellCall(TEXT("CELL_removeStallCollectionItem"), args);
}

void URoleStallInterface::AddStallSellItem(const FString& id, const int32& itemID, const int32& amount, const int64& price)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::AddStallSellItem : GetEntity()!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****AddStallSellItem*****"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::AddStallSellItem : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::AddStallSellItem : pEntity_Player->IsPlayerRole()!"));
		return;
	}
	ENTITY_STATE RoleState = (ENTITY_STATE)UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("state"));
	if (RoleState == ENTITY_STATE::EntityStateStall)
	{
		return;
	}
	KBEngine::FVariantArray args;
	args.Add((FString)id);
	args.Add((int32)itemID);
	args.Add((int32)amount);
	args.Add((int32)price);
	this->GetEntity()->CellCall(TEXT("CELL_addStallSellItem"), args);
}

void URoleStallInterface::UpdateStallSellItem(const int32& slot, const int32& itemID, const int32& amount, const int64& price)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::UpdateStallSellItem : GetEntity()!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****UpdateStallSellItem*****"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::UpdateStallSellItem : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::UpdateStallSellItem : pEntity_Player->IsPlayerRole()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add((int32)slot);
	args.Add((int32)itemID);
	args.Add((int32)amount);
	args.Add((int32)price);
	this->GetEntity()->CellCall(TEXT("CELL_updateStallSellItem"), args);
}

void URoleStallInterface::RemoveStallSellItem(const int32& slot, const int32& itemID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::RemoveStallSellItem : GetEntity()!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****RemoveStallSellItem*****"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::RemoveStallSellItem : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::RemoveStallSellItem : pEntity_Player->IsPlayerRole()!"));
		return;
	}
	ENTITY_STATE RoleState = (ENTITY_STATE)UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("state"));
	if (RoleState == ENTITY_STATE::EntityStateStall)
	{
		return;
	}
	KBEngine::FVariantArray args;
	args.Add((int32)slot);
	args.Add((int32)itemID);
	this->GetEntity()->CellCall(TEXT("CELL_removeStallSellItem"), args);
}

void URoleStallInterface::BuyStallItem(const int32& playerID, const int32& slot, const int32& itemID, const int32& amount)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::BuyStallItem : GetEntity()!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****BuyStallItem*****"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::BuyStallItem : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::BuyStallItem : pEntity_Player->IsPlayerRole()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add((int32)playerID);
	args.Add((int32)slot);
	args.Add((int32)itemID);
	args.Add((int32)amount);
	this->GetEntity()->CellCall(TEXT("CELL_buyStallItem"), args);
}

void URoleStallInterface::SellStallItem(const int32& playerID, const int32& slot, const int32& itemID, const int32& amount)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::SellStallItem : GetEntity()!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****SellStallItem*****"));
	KBEngine::Entity* player = UUECS3GameInstance::pKBEApp->Player();
	if (!player)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::SellStallItem : player!"));
		return;
	}
	CS3Entity* pEntity_Player = (CS3Entity*)(player);
	if (!pEntity_Player->IsPlayerRole())
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::SellStallItem : pEntity_Player->IsPlayerRole()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add((int32)playerID);
	args.Add((int32)slot);
	args.Add((int32)itemID);
	args.Add((int32)amount);
	this->GetEntity()->CellCall(TEXT("CELL_sellStallItem"), args);
}

void URoleStallInterface::ClearAllStallItems()
{
	for (auto sellItem: StallSellItemList)
	{
		OnBagEnableItem(sellItem.Id);
	}
	StallSellItemList.Empty();
	CollectionItemList.Empty();
	StallSellItemRecordList.Empty();
	StallCollectItemRecordList.Empty();
}

FStallRecordData URoleStallInterface::GetStallItemRecordByData(const FString& data)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****GetStallItemRecordByData| %s |*****"),*data);
	FStallRecordData recordData;
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	auto returnvalue = temp->FromString(data);
	recordData.PlayerName = returnvalue->GetString(TEXT("playerName"));
	recordData.Amount = FSTRING_TO_INT(returnvalue->GetString(TEXT("amount")));
	recordData.Time = returnvalue->GetString(TEXT("time"));
	recordData.ItemName = returnvalue->GetString(TEXT("itemName"));
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****FStallRecordData| %s |*****"), *recordData.ItemName);
	recordData.Tax = FSTRING_TO_INT(returnvalue->GetString(TEXT("tax")));
	recordData.TotalPrice = FSTRING_TO_INT(returnvalue->GetString(TEXT("totalPrice")));
	return recordData;
}

int32 URoleStallInterface::GetTotalSellPrice()
{
	int32 totalSellPrice = 0;
	for (auto sellItem: StallSellItemRecordList)
	{
		totalSellPrice = totalSellPrice + sellItem.TotalPrice;
	}
	return totalSellPrice;
}

int32 URoleStallInterface::GetTotalCollectPrice()
{
	int32 totalCollectPrice = 0;
	for (auto collectItem: StallCollectItemRecordList)
	{
		totalCollectPrice = totalCollectPrice + collectItem.TotalPrice;
	}
	return totalCollectPrice;
}

FStallItemSuccessData URoleStallInterface::GetStallItemSuccessInfoByData(const FString& data)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("*****GetStallItemSuccessInfoByData| %s |*****"), *data);
	FStallItemSuccessData successData;
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	auto returnvalue = temp->FromString(data);
	successData.StallName = returnvalue->GetString(TEXT("stallName"));
	successData.ItemName = returnvalue->GetString(TEXT("itemName"));
	successData.Amount = FSTRING_TO_INT(returnvalue->GetString(TEXT("amount")));
	successData.TotalPrice = FSTRING_TO_INT(returnvalue->GetString(TEXT("totalPrice")));
	return successData;
}

void URoleStallInterface::OnChangeStallState(bool IsStall)
{ 
	APlayerCharacter* MyPlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (IsValid(MyPlayerCharacter))
	{
		MyPlayerCharacter->SetRoleInteractive(IsStall);
		if (IsStall)
		{
			MyPlayerCharacter->StopRandomAction();
		}
	}
}

void URoleStallInterface::RPC_endStall()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::RPC_endStall : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("endStall"), args);
}

void URoleStallInterface::RPC_requestGetStallItems()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleStallInterface::RPC_requestGetStallItems : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_requestStallItems"), args);
}

void URoleStallInterface::InitBlueCB()
{
	
	ArrBlueFunc.Add("CLIENT_OnFindStallPoint");
	ArrBlueFunc.Add("CLIENT_OnReceiveOtherStallItems");
	ArrBlueFunc.Add("CLIENT_UpdateStallItem");
	ArrBlueFunc.Add("CLIENT_StallItemSuccessToClient");
	ArrBlueFunc.Add("CLIENT_AddStallRecord");
	ArrBlueFunc.Add("CLIENT_OnRequestStallItems");
	ArrBlueFunc.Add("CLIENT_AddCollectionItemSuccessCB");
	ArrBlueFunc.Add("CLIENT_UpdateStallCollectionItemCB");
	ArrBlueFunc.Add("CLIENT_RemoveStallCollectionItemCB");
	ArrBlueFunc.Add("CLIENT_AddStallSellItemSuccessCB");
	ArrBlueFunc.Add("CLIENT_UpdateStallSellItemCB");
	ArrBlueFunc.Add("CLIENT_RemoveStallSellItemCB");
	ArrBlueFunc.Add("CLIENT_StallSuccessCB");
	Supper::InitBlueCB();
}

void URoleStallInterface::AnalysisStallData(TArray<FStallItemData>& ItemData, UJsonFieldData* data)
{
	if (data)
	{
		FStallItemData item;
		item.Id = data->GetString(TEXT("id"));
		item.ItemID = FSTRING_TO_INT(data->GetString(TEXT("itemID")));
		item.Amount = FSTRING_TO_INT(data->GetString(TEXT("amount")));
		item.Price = FSTRING_TO_INT(data->GetString(TEXT("price")));
		ItemData.Add(item);
	}
}

void URoleStallInterface::AnalySisOtherStallItem(TArray<UJsonFieldData*>& data)
{
	int32 index = 0;
	OtherStallSellItemList.Empty();
	for (auto It : data)
	{
		UItemBase* item = UItemFactory::GetItemByID(FSTRING_TO_INT(It->GetString(TEXT("itemID"))));
		if (item)
		{
			item->UID = It->GetString(TEXT("id"));
			item->Amount = FSTRING_TO_INT(It->GetString(TEXT("amount")));
			item->Price = FSTRING_TO_INT(It->GetString(TEXT("price")));
			item->ItemOrder = index;
			index += 1;

			int32 combatPowner = FSTRING_TO_INT(It->GetString(TEXT("combatPower")));
			FString attackStr = It->GetString(TEXT("attackPropertiesStr"));
			FString attachStr = It->GetString(TEXT("attachPropertiesStr"));
			FString intensifyStr = It->GetString(TEXT("intensifyDataStr"));
			int32 hardiness = FSTRING_TO_INT(It->GetString(TEXT("hardiness")));
			item->SetDynamicProperty(combatPowner, attackStr, attachStr, intensifyStr, hardiness);

			OtherStallSellItemList.Add(item);
		}
	}
}

CONTROL_COMPILE_OPTIMIZE_END
