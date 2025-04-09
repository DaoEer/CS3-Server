// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleDropBoxInterface.h"
#include "Kismet/KismetStringLibrary.h"
#include "Actor/DropBox/DropBoxCharacter.h"
#include "Json.h"
#include "JsonFieldData.h"
#include "Util/ConvertUtil.h"
#include "GameData/Item/ItemBase.h"
#include "GameData/Item/ItemFactory.h"
#include "CS3Base/UIManager.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/EventManager.h"
#include "Manager/CustomCursorManager.h"
#include "../../Manager/ParticleManager.h"
#include "Manager/CfgManager.h"
#include "CS3Base/BaseWindow.h"

class URoleKitBagInterface;

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleDropBoxInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(FPickup_GetItemInfoList, &URoleDropBoxInterface::FPickup_GetItemInfoList, const int32, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(FRollRandom, &URoleDropBoxInterface::FRollRandom, int32, const FString&, const FVariant&, int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_dropBoxMoveToPoint, &URoleDropBoxInterface::CLIENT_dropBoxMoveToPoint, const int32&, const FVector&, const FVector&, float, float, float, const FString&, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(recvDropBoxData, &URoleDropBoxInterface::recvDropBoxData, const int32&, const uint8&, const uint8&, const FVariant&, const FVariantArray&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(recvDropBoxRalldomData, &URoleDropBoxInterface::recvDropBoxRalldomData, const int32&, const FVariantArray&, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onRollRandomDropBox, &URoleDropBoxInterface::onRollRandomDropBox, const int32&, const FString&, const FString&, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onRollRandomMaxDropBox, &URoleDropBoxInterface::onRollRandomMaxDropBox, const int32&, const FString&, const FString&, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(recvDropBoxAuctionData, &URoleDropBoxInterface::recvDropBoxAuctionData, const int32&, const FVariantArray&, const FVariantArray&, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onPickupItemToRole, &URoleDropBoxInterface::onPickupItemToRole, const int32&, const FString&, const FString&, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onPickUpDropBoxEnd, &URoleDropBoxInterface::onPickUpDropBoxEnd, int32)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onDropBoxAuctionItemEnd, &URoleDropBoxInterface::onDropBoxAuctionItemEnd, const int32&, const FString&, const FVariantArray&, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onAuctionDropBox, &URoleDropBoxInterface::onAuctionDropBox, const int32&, const FString&, const int32&, const FString&, const int32&, const int32&, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onAbandomAuctionDropBox, &URoleDropBoxInterface::onAbandomAuctionDropBox, const int32&, const FString&, const FString&, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(recvAuctionHistoryData, &URoleDropBoxInterface::recvAuctionHistoryData, const FVariantArray&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(updateAuctionHistoryData, &URoleDropBoxInterface::updateAuctionHistoryData, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onStartAuction, &URoleDropBoxInterface::onStartAuction, const int32&, const FVariantArray&, const FString&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleDropBoxInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()


	
URoleDropBoxInterface::URoleDropBoxInterface()
{

}

URoleDropBoxInterface::~URoleDropBoxInterface()
{

}

void URoleDropBoxInterface::FPickup_GetItemInfoList(const int32 dropBoxEntityID, const FVariant& variant)
{
	TArray<UItemBase*> PickUpItemList = AnalyzePickUpItemJsonStr(variant);
	AActor* actor = UGolbalBPFunctionLibrary::GetActorByID(dropBoxEntityID);
	if (IsValid(actor))
	{
		ADropBoxCharacter* dropBoxCharacter = Cast<ADropBoxCharacter>(actor);
		if (IsValid(dropBoxCharacter))
		{
			if ( dropBoxCharacter->IsAlreadyRequest )
			{
				ClearPickUpData();
				DropBoxID = dropBoxEntityID;
				if (PickUpItemList.Num() <= 0) return;
				for (auto pickUpItem : PickUpItemList)
				{
					FPK_ItemList.Add(pickUpItem);
				}
				///<点击宝箱打开宝箱的时候也会请求宝箱物品列表信息，显示拾取界面
				BP_OnGetItemInfoList( dropBoxEntityID );
			} 
			else
			{
				dropBoxCharacter->DropBox_ItemList = PickUpItemList;//宝箱创建的时候DropBox_ItemList肯定是空的，所以没必要去判断这个列表是否有这个物品
				///<宝箱创建的时候会请求宝箱物品列表信息，根据宝箱物品品质播放光效
				//dropBoxCharacter->SetBoxEffect();
				dropBoxCharacter->SetAlreadyRequest(true);
			}
		}
	}
}

void URoleDropBoxInterface::PickUp_Implementation(int32 dropBoxEntityID, int32 IsSuccess, const FString& UId, int32 LeftAmount)
{
	if (IsSuccess)
	{
		if (DropBoxID == dropBoxEntityID)
		{
			///<更新打开拾取的宝箱的物品列表
			UpdatePKItemList(UId, LeftAmount);
		}
		///<更新掉落宝箱的物品列表
		AActor* actor = UGolbalBPFunctionLibrary::GetActorByID(dropBoxEntityID);
		if (IsValid(actor))
		{
			ADropBoxCharacter* dropBoxCharacter = Cast<ADropBoxCharacter>(actor);
			if (IsValid(dropBoxCharacter))
			{
				dropBoxCharacter->UpdateDropBoxItemList(UId, LeftAmount);
			}
		}
		//通知界面
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnPickUpSuccessed.Broadcast(dropBoxEntityID, UId);
		}
	}
}

void URoleDropBoxInterface::FRollRandom(int32 dropBoxEntityID, const FString& UId, const FVariant& FVariantItem, int32 RollRemainTime)
{
	FPICK_UP_ITEM_DATA itemData(FVariantItem);
	UItemBase* item = UItemFactory::GetItemByID(itemData.id);
	if (!IsValid(item))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleDropBoxInterface::FRollRandom : item!"));
		return;
	}
	item->UID = itemData.uid;
	item->Amount = itemData.amount;
	item->BindType = itemData.bindType;
	item->Quality = itemData.quality;
	item->InitDynamicDataForJson(itemData.dynamicData);
	///<开始掷筛子，此处的dropBoxEntityID不一定是接口的DropBoxID，因为其他队友点宝箱也可以通知玩家弹出掷筛子界面
	if (!FPK_RollItemUidDict.Contains(UId))
	{
		FPK_RollItemUidDict.Add(UId, item);
	}
	OnFRollRandom(dropBoxEntityID, UId, itemData.id, RollRemainTime);
}

void URoleDropBoxInterface::receiverRollResult_Implementation(int32 dropBoxEntityID, const FString& UId, int32 ItemID, int32 Result, int32 LeftAmount)
{
	if (FPK_RollItemUidDict.Contains(UId))
	{
		FPK_RollItemUidDict.Remove(UId);
	}

	if (DropBoxID == dropBoxEntityID)
	{	
		///<更新打开拾取的宝箱的物品列表
		UpdatePKItemList(UId, LeftAmount);
	}
	///<更新掉落宝箱的物品列表
	AActor* actor = UGolbalBPFunctionLibrary::GetActorByID(dropBoxEntityID);
	if (IsValid(actor))
	{
		ADropBoxCharacter* dropBoxCharacter = Cast<ADropBoxCharacter>(actor);
		if (IsValid(dropBoxCharacter))
		{
			dropBoxCharacter->UpdateDropBoxItemList(UId, LeftAmount);
		}
	}
}

void URoleDropBoxInterface::pickUpToMember_Implementation(int32 dropBoxEntityID, const FString& UId, const FString& JsonStr)
{

}

void URoleDropBoxInterface::RollRandomFC(int32 dropBoxEntityID, const FString ItemUId)
{
	KBEngine::FVariantArray args;
	args.Add(dropBoxEntityID);
	args.Add(ItemUId);
	CellCall(TEXT("CELL_rollRandom"), args);
}

void URoleDropBoxInterface::AbandonRollFC(int32 dropBoxEntityID, const FString ItemUId)
{
	KBEngine::FVariantArray args;
	args.Add(dropBoxEntityID);
	args.Add(ItemUId);
	CellCall(TEXT("CELL_abandonRoll"), args);
}

void URoleDropBoxInterface::PickUpToMemberFC(int32 dropBoxEntityID, const FString ItemUId, const int32 DstEntityID)
{
	KBEngine::FVariantArray args;
	args.Add(dropBoxEntityID);
	args.Add(ItemUId);
	args.Add(DstEntityID);
	CellCall(TEXT("CELL_pickUpToMember"), args);
}

void URoleDropBoxInterface::ReqSendItemInfoListToClient(int32 dropBoxEntityID)
{
	KBEngine::FVariantArray args;
	args.Add(dropBoxEntityID);
	CellCall(TEXT("CELL_reqSendItemInfoListToClient"), args);
}

void URoleDropBoxInterface::ReqPickUp(int32 dropBoxEntityID, const TArray<FString>& ItemUIdList)
{
	KBEngine::FVariantArray args;
	args.Add(dropBoxEntityID);
	FString ItemUIdListStr = UKismetStringLibrary::JoinStringArray(ItemUIdList, FString(TEXT("|")));
	args.Add(ItemUIdListStr);
	CellCall(TEXT("CELL_reqPickUp"), args);
}

TArray<UItemBase*> URoleDropBoxInterface::AnalyzePickUpItemJsonStr(const FVariant& variant)
{
	TArray<UItemBase*> itemBaseArray;
	UItemFactory* ItemFactory = UUECS3GameInstance::Instance->ItemFactory;
	if (!IsValid(ItemFactory))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleDropBoxInterface::AnalyzePickUpItemJsonStr : ItemFactory!"));
		return itemBaseArray;
	}
	FPICK_UP_ITEM_DATAS pickUpItemData = FPICK_UP_ITEM_DATAS(variant);
	for (auto data : pickUpItemData.pickUpItemList)
	{
		int32 ItemId = data.id;
		UItemBase* ItemBase = ItemFactory->GetItemByID(ItemId);
		if (!IsValid(ItemBase))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleDropBoxInterface::AnalyzePickUpItemJsonStr : ItemBase!"));
			continue;
		}
		ItemBase->UID = data.uid;
		ItemBase->BindType = data.bindType;
		ItemBase->Quality = data.quality;
		ItemBase->Amount = data.amount;
		ItemBase->InitDynamicDataForJson(data.dynamicData);
		itemBaseArray.Add(ItemBase);
	}
	return itemBaseArray;
}

bool URoleDropBoxInterface::HasUIdInPKItemList(const FString& UId)
{
	for (auto item : FPK_ItemList)
	{
		if (UId == item->UID)
		{
			return true;
		}
	}
	return false;
}

void URoleDropBoxInterface::UpdatePKItemList(const FString& UId, int32 LeftAmount)
{
	for (auto item : FPK_ItemList)
	{
		if (UId == item->UID)
		{
			if (LeftAmount == 0)
			{
				FPK_ItemList.Remove(item);
			}
			else if (item->Amount != LeftAmount)
			{
				item->Amount = LeftAmount;
			}
			break;
		}
	}
}

void URoleDropBoxInterface::ClearPickUpData()
{
	FPK_ItemList.Empty();
	AActor* actor = UGolbalBPFunctionLibrary::GetActorByID(DropBoxID);
	if (IsValid(actor))
	{
		ADropBoxCharacter* dropBoxCharacter = Cast<ADropBoxCharacter>(actor);
		if (IsValid(dropBoxCharacter))
		{
			dropBoxCharacter->DropBoxInteractiveFinshed();
		}
	}
	DropBoxID = 0;
}

void URoleDropBoxInterface::OnDropBoxDestroyed(int32 dropBoxEntityID)
{
	if (DropBoxID != dropBoxEntityID) return;
	ClearPickUpData();
	BP_OnDropBoxDestroyed(dropBoxEntityID);//宝箱销毁时通知蓝图隐藏拾取界面
}

void URoleDropBoxInterface::GetAllPickUp()
{
	URoleKitBagInterface* kitbag = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitbagInterface")));
	if (IsValid(kitbag) && kitbag->IsBagFull(EKITBAGTYPE::COMMON) && kitbag->IsBagFull(EKITBAGTYPE::CRYSTAL))
	{
		if (isBagFull != true)
		{
			UGolbalBPFunctionLibrary::StatusMessage(1315, TEXT(""));
		}
		isBagFull = true;
		return;
	}
	isBagFull = false;

	TArray<int32> BoxIDs;
	TArray<AActor*> DropBoxList = UGolbalBPFunctionLibrary::GetActorsInRange(ADropBoxCharacter::StaticClass(), 1500.0f);

	for (auto actor : DropBoxList)
	{
		ADropBoxCharacter* dropBox = Cast<ADropBoxCharacter>(actor);
		if (IsValid(dropBox) && !dropBox->bHidden)
		{
			BoxIDs.Add(dropBox->EntityId);
		}
	}
	if (BoxIDs.Num() > 0)
	{
		KBEngine::FVariantArray args;
		args.Add(UGolbalBPFunctionLibrary::ListToFVariant(BoxIDs));
		CellCall(TEXT("CELL_autoPickUpDropBox"), args);
	}
}

void URoleDropBoxInterface::onEnterWorld()
{
	Supper::onEnterWorld();
}

void URoleDropBoxInterface::onLeaveWorld()
{
	dropBoxs.Empty();
	dropBoxIDList.Empty();
	auctionHistory.Empty();
	Supper::onLeaveWorld();
}

void URoleDropBoxInterface::InitBlueCB()
{
	ArrBlueFunc.Add("FPickup_GetItemInfoList");
	ArrBlueFunc.Add("PickUp");
	ArrBlueFunc.Add("receiverRollResult");
	ArrBlueFunc.Add("pickUpToMember");
	ArrBlueFunc.Add("SetAutoPickUp");
	Supper::InitBlueCB();
}

UItemBase* URoleDropBoxInterface::FindBoxItemByUID(const FString& uid) 
{
	for (auto DropBox : dropBoxs)
	{
		UDropBoxData* DropBoxData = DropBox.Value;
		if (DropBoxData->items.Contains(uid))
		{
			return DropBoxData->items[uid];
		}
	}
	return nullptr;
}

void URoleDropBoxInterface::CLIENT_dropBoxMoveToPoint_Implementation(const int32& dropBoxEntityID, const FVector& InStartPosition, const FVector& InEndPosition, float XMoveSpeed, float Scale, float Gravity, const FString& DragActionID, const FString& levitateActionID)
{
	AActor* actor = UGolbalBPFunctionLibrary::GetActorByID(dropBoxEntityID);
	if (IsValid(actor))
	{
		ADropBoxCharacter* dropBoxCharacter = Cast<ADropBoxCharacter>(actor);
		if (IsValid(dropBoxCharacter))
		{
			if (dropBoxCharacter->bIsChangeAppearanceling || (!dropBoxCharacter->GetApperanceLoadingOver()) || !IsValid(dropBoxCharacter->GetMesh()) || !IsValid(dropBoxCharacter->GetMesh()->SkeletalMesh))
			{
				//外观未创建完成
				TWeakObjectPtr<ADropBoxCharacter> ActorPtr(dropBoxCharacter);
				TWeakObjectPtr<URoleDropBoxInterface> ThisPtr(this);
				if (MoveHandle.IsValid())
				{
					dropBoxCharacter->OnModelChangeAppearanceOverDelegate.Remove(MoveHandle);
					MoveHandle.Reset();
				}
				MoveHandle = dropBoxCharacter->OnModelChangeAppearanceOverDelegate.AddLambda([
					ThisPtr, ActorPtr, InStartPosition, InEndPosition, XMoveSpeed, Scale, Gravity, DragActionID, levitateActionID]()
				{
					URoleDropBoxInterface* ThisInterface = ThisPtr.Get();
					if (IsValid(ThisInterface))
					{
						ADropBoxCharacter* DropBox = ActorPtr.Get();
						if (IsValid(DropBox) && IsValid(DropBox->GetMesh()) && IsValid(DropBox->GetMesh()->SkeletalMesh))
						{
							DropBox->CurveMoveAndZoom(DragActionID, levitateActionID, InStartPosition, InEndPosition, XMoveSpeed, Scale, Gravity);
							DropBox->OnModelChangeAppearanceOverDelegate.Remove(ThisInterface->MoveHandle);
						}
					}
				});
			}
			else
			{
				dropBoxCharacter->CurveMoveAndZoom(DragActionID, levitateActionID, InStartPosition, InEndPosition, XMoveSpeed, Scale, Gravity);
			}
		}
	}
}

//---------------------------------------------帮会宝箱----------------------------------------------------
void URoleDropBoxInterface::recvDropBoxData(const int32& dropBoxID, const uint8& entityExtFlag, const uint8& allocation, const FVariant& owners, const FVariantArray& items)
{
	if (dropBoxs.Contains(dropBoxID))
	{
		CS3_Warning(TEXT(" error:UTongDropBoxInterface::recvDropBoxData :dropBox exists"));
		return;
	}

	if (dropBoxIDList.Contains(dropBoxID))
	{
		CS3_Warning(TEXT(" error:UTongDropBoxInterface::recvDropBoxData :dropBoxID exists"));
		return;
	}

	dropBoxIDList.Add(dropBoxID);
	dropBoxs.Add(dropBoxID, NewObject<UDropBoxData>());
	dropBoxs[dropBoxID]->id = dropBoxID;
	dropBoxs[dropBoxID]->entityExtFlag = entityExtFlag;
	dropBoxs[dropBoxID]->allocation = allocation;

	FDICT_STR_STR datas = FDICT_STR_STR(owners);
	for (auto data : datas.dictDataList)
	{
		dropBoxs[dropBoxID]->owners.Add(data.Key, data.Value);
	}

	TArray<UItemBase*> itemList = AnalyzeItemData(items);
	for (auto item : itemList)
	{
		if (dropBoxs[dropBoxID]->items.Contains(item->UID))
		{
			CS3_Warning(TEXT(" error:UTongDropBoxInterface::recvDropBoxData :item exists"));
			continue;
		}
		dropBoxs[dropBoxID]->items.Add(item->UID, item);
	}
}

void URoleDropBoxInterface::recvDropBoxRalldomData(const int32& dropBoxID, const FVariantArray& items, const FString& countDown)
{
	if (dropBoxs.Contains(dropBoxID))
	{
		for (auto it : items)
		{
			FROLLDOM_DATA itemData(it);
			URollDomData* item = NewObject<URollDomData>();
			item->uid = itemData.uid;
			item->ownerDBID = itemData.ownerDBID;
			item->isPickUp = itemData.isPickUp;
			item->maxRollDBID = itemData.maxRollDBID;
			item->maxRoll = itemData.maxRoll;
			item->selfRoll = itemData.selfRoll;

			if (!dropBoxs[dropBoxID]->rollDomItems.Contains(item->uid))
			{
				dropBoxs[dropBoxID]->rollDomItems.Add(item->uid, item);
			}
		}
		dropBoxs[dropBoxID]->countDown = countDown;
		
		//打开掷点分配界面
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager) && IsValid(UUECS3GameInstance::Instance->GEventManager) && dropBoxs[dropBoxID]->items.Num() > 0)
		{
			if (dropBoxs[dropBoxID]->isTongDropBox())
			{
				if (dropBoxs[dropBoxID]->isRalldomPickUp())
				{
					UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("TongDicePick"));
					UUECS3GameInstance::Instance->GEventManager->OnOpenTongDicePickWnd.Broadcast(dropBoxID);

					///播放光效
					AActor* tempActor = UGolbalBPFunctionLibrary::GetActorByID(dropBoxID);
					ADropBoxCharacter* dropBox = Cast<ADropBoxCharacter>(tempActor);
					if (IsValid(dropBox))
					{
						dropBox->OpenDropEffectEvent(Tong_DropBox_OpenEffectID, Tong_DropBox_StayEffectID);
					}
				}
			}
			else if (dropBoxs[dropBoxID]->isTeamDropBox())
			{
				if (dropBoxs[dropBoxID]->isRalldomPickUp())
				{
					UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("TeamDicePickUp"));
					UUECS3GameInstance::Instance->GEventManager->OnUpdateTeamDicePickWnd.Broadcast(dropBoxID);
				}
			}
		}
	}
}

void URoleDropBoxInterface::recvDropBoxAuctionData(const int32& dropBoxID, const FVariantArray& items, const FVariantArray& pickupList, const FString& countDown)
{
	if (dropBoxs.Contains(dropBoxID))
	{
		for (auto it : items)
		{
			FAUCTION_DATA itemData(it);
			UAuctionData* item = NewObject<UAuctionData>();
			item->uid = itemData.uid;
			item->round = itemData.round;
			item->isPickUp = itemData.isPickUp;
			item->ownerDBID = itemData.ownerDBID;
			item->selfMoney = itemData.selfMoney;
			item->maxAuctionDBID = itemData.maxAuctionDBID;
			item->curAuctionRoleAmount = itemData.curAuctionRoleAmount;
			item->maxAuctionMoney = itemData.maxAuctionMoney;

			if (!dropBoxs[dropBoxID]->auctionItems.Contains(item->uid))
			{
				dropBoxs[dropBoxID]->auctionItems.Add(item->uid, item);
			}
		}
		for (auto it : pickupList)
		{
			dropBoxs[dropBoxID]->pickupList.Add((FString)it);
		}
		dropBoxs[dropBoxID]->countDown = countDown;

		//通知界面
		OnRecvDropBoxAuctionData(dropBoxID);
	}
}

TArray<UItemBase*> URoleDropBoxInterface::AnalyzeItemData(const FVariantArray& itemList)
{
	TArray<UItemBase*> itemBaseArray;
	for (auto it : itemList)
	{
		FITEM_FOR_CLIENT itemData(it);

		UItemBase* item = UItemFactory::GetItemByID(itemData.id);
		if (!IsValid(item))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleDropBoxInterface::AnalyzeItemData : item!"));
			return itemBaseArray;
		}
		item->UID = itemData.uid;
		item->Amount = itemData.amount;
		item->BindType = itemData.bindType;
		item->ItemOrder = itemData.itemOrder;
		item->ItemEndTime = itemData.itemEndTime;
		item->InitDynamicDataForJson(itemData.dynamicData);
		itemBaseArray.Add(item);
	}
	return itemBaseArray;
}

bool URoleDropBoxInterface::GetRollRandomDropBox(int32 InDropBoxID, float& OutHoldTime, FString& OutEndTime, TArray<UItemBase*>& OutNoRollItems, TArray<UItemBase*>& OutHasPickItems, TArray<UItemBase*>& OutHasRollNoPickItems)
{
	if (dropBoxs.Contains(InDropBoxID) && dropBoxs[InDropBoxID]->items.Num() > 0)
	{
		OutEndTime = dropBoxs[InDropBoxID]->countDown;
		OutHoldTime = dropBoxs[InDropBoxID]->HoldTime;
		for (typename TMap<FString, UItemBase*>::TConstIterator Iterator(dropBoxs[InDropBoxID]->items); Iterator; ++Iterator)
		{
			if (dropBoxs[InDropBoxID]->rollDomItems.Contains(Iterator.Key()))
			{
				URollDomData* tempRollDomData = dropBoxs[InDropBoxID]->rollDomItems[Iterator.Key()];
				if (IsValid(tempRollDomData))
				{
					if (tempRollDomData->isPickUp == 1)
					{
						OutHasPickItems.Emplace(Iterator.Value());
					}
					else
					{
						///< selfRoll玩家自己的掷点数 -1:未掷点 0：已放弃掷点
						if (tempRollDomData->selfRoll == -1)
						{
							OutNoRollItems.Emplace(Iterator.Value());
						}
						else if (tempRollDomData->selfRoll == 0)
						{
							///不处理
						}
						else
						{
							OutHasRollNoPickItems.Emplace(Iterator.Value());
						}
					}
				}
			}
			else
			{
				OutNoRollItems.Emplace(Iterator.Value());
			}
		}
		return true;
	}
	return false;
}

URollDomData* URoleDropBoxInterface::GetRollDomData(int32 InDropBoxID, const FString& InUId)
{
	if (dropBoxs.Contains(InDropBoxID) && dropBoxs[InDropBoxID]->items.Num() > 0 && dropBoxs[InDropBoxID]->rollDomItems.Num() >0)
	{
		if (dropBoxs[InDropBoxID]->rollDomItems.Contains(InUId))
		{
			return dropBoxs[InDropBoxID]->rollDomItems[InUId];
		}
	}
	return nullptr;
}

void URoleDropBoxInterface::ReqRollRandomDropBox(const int32& dropBoxID, const FString& uid)
{
	//策划需求延时
	TWeakObjectPtr<URoleDropBoxInterface> ThisPtr(this);
	FTimerHandle DelayHandle;
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayHandle, FTimerDelegate::CreateLambda([ThisPtr, dropBoxID, uid]()
	{
		URoleDropBoxInterface* Interface = ThisPtr.Get();
		if (IsValid(Interface))
		{
			if (Interface->dropBoxs.Contains(dropBoxID))
			{
				if (Interface->dropBoxs[dropBoxID]->isRalldomPickUp())
				{
					if (Interface->dropBoxs[dropBoxID]->isCanSelfPickup(uid))
					{
						KBEngine::FVariantArray args;
						args.Add(dropBoxID);
						args.Add(uid);
						Interface->CellCall(TEXT("reqRollRandomDropBox"), args);
					}
				}
			}
		}
	}), 2.0f, false);
}

void URoleDropBoxInterface::ReqAbandomRollRandomDropBox(const int32& dropBoxID, const FString& uid)
{
	if (dropBoxs.Contains(dropBoxID))
	{
		if (dropBoxs[dropBoxID]->isRalldomPickUp())
		{
			if (dropBoxs[dropBoxID]->isCanSelfPickup(uid))
			{
				KBEngine::FVariantArray args;
				args.Add(dropBoxID);
				args.Add(uid);
				CellCall(TEXT("reqAbandomRollRandomDropBox"), args);
			}
		}
	}
}

void URoleDropBoxInterface::onRollRandomDropBox_Implementation(const int32& dropBoxID, const FString& uid, const FString& dbid, const int32& roll)
{
	if (dropBoxs.Contains(dropBoxID))
	{
		if (!dropBoxs[dropBoxID]->rollDomItems.Contains(uid))
		{
			dropBoxs[dropBoxID]->rollDomItems.Add(uid, NewObject<URollDomData>());
			dropBoxs[dropBoxID]->rollDomItems[uid]->uid = uid;
			dropBoxs[dropBoxID]->rollDomItems[uid]->ownerDBID = INT_TO_FSTRING(0);
			dropBoxs[dropBoxID]->rollDomItems[uid]->isPickUp = 0;
			dropBoxs[dropBoxID]->rollDomItems[uid]->maxRollDBID = INT_TO_FSTRING(0);
			dropBoxs[dropBoxID]->rollDomItems[uid]->maxRoll = 0;
			dropBoxs[dropBoxID]->rollDomItems[uid]->selfRoll = -1;
		}
		if (GetEntity())
		{
			uint64 selfDBID = GetEntity()->GetDefinedProperty(TEXT("playerDBID")).GetValue<uint64>();
			if (FSTRING_TO_INT(dbid) == selfDBID)
			{
				dropBoxs[dropBoxID]->rollDomItems[uid]->selfRoll = roll;
			}
		}

		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager) && dropBoxs[dropBoxID]->owners.Contains(dbid))
		{
			if (dropBoxs[dropBoxID]->isTongDropBox())
			{
				if (dropBoxs[dropBoxID]->isRalldomPickUp())
				{
					UUECS3GameInstance::Instance->GEventManager->OnTongRollRandomDropBoxResult.Broadcast(dropBoxID, uid, roll);
				}
			}
			else if (dropBoxs[dropBoxID]->isTeamDropBox())
			{
				if (dropBoxs[dropBoxID]->isRalldomPickUp())
				{
					//暂时没需求
				}
			}
		}
	}
}

void URoleDropBoxInterface::onRollRandomMaxDropBox_Implementation(const int32& dropBoxID, const FString& uid, const FString& dbid, const int32& roll)
{
	if (dropBoxs.Contains(dropBoxID))
	{
		if (!dropBoxs[dropBoxID]->rollDomItems.Contains(uid))
		{
			dropBoxs[dropBoxID]->rollDomItems.Add(uid, NewObject<URollDomData>());
			dropBoxs[dropBoxID]->rollDomItems[uid]->uid = uid;
			dropBoxs[dropBoxID]->rollDomItems[uid]->ownerDBID = INT_TO_FSTRING(0);
			dropBoxs[dropBoxID]->rollDomItems[uid]->isPickUp = 0;
			dropBoxs[dropBoxID]->rollDomItems[uid]->selfRoll = -1;
		}

		if (GetEntity())
		{
			uint64 selfDBID = GetEntity()->GetDefinedProperty(TEXT("playerDBID")).GetValue<uint64>();
			if (FSTRING_TO_INT(dbid) == selfDBID)
			{
				dropBoxs[dropBoxID]->rollDomItems[uid]->selfRoll = roll;
			}
		}

		dropBoxs[dropBoxID]->rollDomItems[uid]->maxRollDBID = dbid;
		dropBoxs[dropBoxID]->rollDomItems[uid]->maxRoll = roll;	

		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager) && dropBoxs[dropBoxID]->owners.Contains(dbid))
		{
			if (dropBoxs[dropBoxID]->isTongDropBox())
			{
				if (dropBoxs[dropBoxID]->isRalldomPickUp())
				{
					UUECS3GameInstance::Instance->GEventManager->OnTongRollRandomMaxDropBox.Broadcast(dropBoxID, uid, dropBoxs[dropBoxID]->owners[dbid], roll);
				}
			}
			else if(dropBoxs[dropBoxID]->isTeamDropBox())
			{
				if (dropBoxs[dropBoxID]->isRalldomPickUp())
				{
					//暂时没需求
				}
			}
		}
	}
}

void URoleDropBoxInterface::ReqAuctionDropBox(const int32& dropBoxID, const FString& uid, const int32& money)
{
	if (dropBoxs.Contains(dropBoxID))
	{
		if (dropBoxs[dropBoxID]->isAuctionPickUp())
		{
			if (dropBoxs[dropBoxID]->isCanSelfPickup(uid))
			{
				if (GetEntity())
				{
					int64 selfMoney = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
					if (selfMoney >= money)
					{
						KBEngine::FVariantArray args;
						args.Add(dropBoxID);
						args.Add(uid);
						args.Add(money);
						CellCall(TEXT("reqAuctionDropBox"), args);
					}
				}
			}
		}
	}
}

void URoleDropBoxInterface::onAuctionDropBox_Implementation(const int32& dropBoxID, const FString& uid, const int32& money, const FString& dbid, const int32& curAuctionRoleAmount, const int32& round, const FString& countDown)
{
	if (dropBoxs.Contains(dropBoxID))
	{
		if (!dropBoxs[dropBoxID]->auctionItems.Contains(uid))
		{
			dropBoxs[dropBoxID]->auctionItems.Add(uid, NewObject<UAuctionData>());
			dropBoxs[dropBoxID]->auctionItems[uid]->uid = uid;
			dropBoxs[dropBoxID]->auctionItems[uid]->ownerDBID = INT_TO_FSTRING(0);
			dropBoxs[dropBoxID]->auctionItems[uid]->isPickUp = 0;
		}

		dropBoxs[dropBoxID]->auctionItems[uid]->round = round;
		dropBoxs[dropBoxID]->auctionItems[uid]->curAuctionRoleAmount = curAuctionRoleAmount;
		dropBoxs[dropBoxID]->auctionItems[uid]->maxAuctionDBID = dbid;
		dropBoxs[dropBoxID]->auctionItems[uid]->maxAuctionMoney = money;
		
		//消息记录竞拍消息
		FAUCTIONMESSAGE MessageData;
		MessageData.PlayerDBID = dbid;
		MessageData.BidMoney = money;
		dropBoxs[dropBoxID]->auctionItems[uid]->auctionMessageData.Add(MessageData);

		//如果是自己出价
		uint64 selfDBID = GetEntity()->GetDefinedProperty(TEXT("playerDBID")).GetValue<uint64>();
		if (selfDBID == FSTRING_TO_INT64(dbid))
		{
			dropBoxs[dropBoxID]->auctionItems[uid]->selfMoney = money;
		}

		//更新倒计时
		dropBoxs[dropBoxID]->countDown = countDown;

		//通知界面
		OnAuctionBidPrice(dropBoxID, uid, money, dbid, countDown, MessageData);
	}
}

void URoleDropBoxInterface::ReqAbandomAuctionDropBox(const int32& dropBoxID, const FString& uid)
{
	if (dropBoxs.Contains(dropBoxID))
	{
		if (dropBoxs[dropBoxID]->isAuctionPickUp())
		{
			if (dropBoxs[dropBoxID]->isCanSelfPickup(uid))
			{
				KBEngine::FVariantArray args;
				args.Add(dropBoxID);
				args.Add(uid);
				CellCall(TEXT("reqAbandomAuctionDropBox"), args);
			}
		}
	}
}

void URoleDropBoxInterface::onAbandomAuctionDropBox_Implementation(const int32& dropBoxID, const FString& uid, const FString& dbid, const int32& curAuctionRoleAmount )
{
	if (dropBoxs.Contains(dropBoxID))
	{
		if (!dropBoxs[dropBoxID]->auctionItems.Contains(uid))
		{
			dropBoxs[dropBoxID]->auctionItems.Add(uid, NewObject<UAuctionData>());
			dropBoxs[dropBoxID]->auctionItems[uid]->uid = uid;
			dropBoxs[dropBoxID]->auctionItems[uid]->ownerDBID = INT_TO_FSTRING(0);
			dropBoxs[dropBoxID]->auctionItems[uid]->isPickUp = 0;
		}

		//消息记录竞拍消息
		FAUCTIONMESSAGE MessageData;
		MessageData.PlayerDBID = dbid;
		MessageData.BidMoney = 0;
		dropBoxs[dropBoxID]->auctionItems[uid]->auctionMessageData.Add(MessageData);
		dropBoxs[dropBoxID]->auctionItems[uid]->curAuctionRoleAmount = curAuctionRoleAmount;

		if (GetEntity())
		{
			//如果是自己放弃
			uint64 selfDBID = GetEntity()->GetDefinedProperty(TEXT("playerDBID")).GetValue<uint64>();
			if (selfDBID == FSTRING_TO_INT64(dbid))
			{
				dropBoxs[dropBoxID]->auctionItems[uid]->selfMoney = 0;
			}
		}

		//放弃所有的时候，这里会走很多次，每个物品都要执行一次，不是正在竞拍的可以不及时更新，切换竞拍物品会获取全部数据刷新
		if (dropBoxIDList.Num() > 0 && dropBoxIDList[0] == dropBoxID && dropBoxs[dropBoxID]->pickupList.Num() > 0 && dropBoxs[dropBoxID]->pickupList[0] == uid)
		{
			//通知界面
			OnAbandomAuctionItem(dropBoxID, uid, dbid, MessageData);
		}
	}
}

void URoleDropBoxInterface::ReqAbandomAuctionAllDropBox()
{
	KBEngine::FVariantArray args;
	args.Add(UGolbalBPFunctionLibrary::ListToFVariant(dropBoxIDList));
	CellCall("reqAbandomAuctionAllDropBox", args);
}

void URoleDropBoxInterface::onDropBoxAuctionItemEnd(const int32& dropBoxID, const FString& uid, const FVariantArray& pickupList, const FString& countDown)
{
	if (dropBoxs.Contains(dropBoxID))
	{
		//清空
		dropBoxs[dropBoxID]->pickupList.Empty();
		
		//更新拍卖列表
		for (auto it : pickupList)
		{
			dropBoxs[dropBoxID]->pickupList.Add((FString)it);
		}

		dropBoxs[dropBoxID]->countDown = countDown;

		//通知界面
		OnAuctionItemEnd(dropBoxID, uid);
	}
}

void URoleDropBoxInterface::onStartAuction(const int32& dropBoxID, const FVariantArray& pickupList, const FString& countDown)
{
	if (dropBoxs.Contains(dropBoxID))
	{
		//清空
		dropBoxs[dropBoxID]->pickupList.Empty();

		//更新拍卖列表
		for (auto it : pickupList)
		{
			dropBoxs[dropBoxID]->pickupList.Add((FString)it);
		}

		dropBoxs[dropBoxID]->countDown = countDown;

		if (dropBoxs[dropBoxID]->items.Num() > 0 && IsValid(UUECS3GameInstance::Instance))
		{
			//通知打开竞拍分配界面
			OnShowAuctionWindow(dropBoxID);

			///播放光效
			if (dropBoxs[dropBoxID]->isTongDropBox())
			{
				AActor* tempActor = UGolbalBPFunctionLibrary::GetActorByID(dropBoxID);
				ADropBoxCharacter* dropBox = Cast<ADropBoxCharacter>(tempActor);
				if (IsValid(dropBox))
				{
					dropBox->OpenDropEffectEvent(Tong_DropBox_OpenEffectID, Tong_DropBox_StayEffectID);
				}
			}
		}
	}
}

bool URoleDropBoxInterface::HasCanAuctionItem(int32 DropBoxType)
{
	for (auto BoxID : dropBoxIDList)
	{
		if (dropBoxs.Contains(BoxID))
		{
			if ((DropBoxType == 0 && dropBoxs[BoxID]->isTongDropBox()) || (DropBoxType == 1 && dropBoxs[BoxID]->isTeamDropBox()))
			{
				for (auto uid : dropBoxs[BoxID]->pickupList)
				{
					UAuctionData* AuctionData = GetAuctionData(BoxID, uid);
					//没有被分配&&自己没有放弃
					if (IsValid(AuctionData) && AuctionData->isPickUp == 0 && AuctionData->selfMoney != 0)
					{
						return true;
					}
				}
			}
		}
	}
	return false;
}

TArray<FString> URoleDropBoxInterface::GetAuctionItems(int32 dropBoxID)
{
	TArray<FString> UIDList;
	if (dropBoxs.Contains(dropBoxID))
	{
		UIDList =  dropBoxs[dropBoxID]->pickupList;
	}
	return UIDList;
}

UItemBase* URoleDropBoxInterface::FindAuctionItemByUID(int32 dropBoxID, FString UID)
{
	if (dropBoxs.Contains(dropBoxID))
	{
		TMap<FString, UItemBase*> Items = dropBoxs[dropBoxID]->items;
		if (Items.Contains(UID))
		{
			return Items[UID];
		}
	}
	return nullptr;
}

UAuctionData* URoleDropBoxInterface::GetAuctionData(int32 dropBoxID, FString UID)
{
	if (dropBoxs.Contains(dropBoxID))
	{
		TMap<FString, UAuctionData*> AuctionItems = dropBoxs[dropBoxID]->auctionItems;
		if (AuctionItems.Contains(UID))
		{
			return AuctionItems[UID];
		}
	}
	return nullptr;
}

FString URoleDropBoxInterface::GetAuctionPlayerName(int32 dropBoxID, FString DBID)
{
	if (dropBoxs.Contains(dropBoxID))
	{
		TMap<FString, FString> Owners = dropBoxs[dropBoxID]->owners;
		if (Owners.Contains(DBID))
		{
			return Owners[DBID];
		}
	}
	return TEXT("");
}

int32 URoleDropBoxInterface::GetMinBidPrice(int32 dropBoxID, FString UID)
{
	UAuctionData* AuctionData = GetAuctionData(dropBoxID, UID);
	if (AuctionData)
	{
		FAUCTIONCFG_DATA AuctionCfgData = GetAuctionCfg(AuctionData->round);
		return AuctionData->maxAuctionMoney+ (AuctionData->maxAuctionMoney * AuctionCfgData.price) / 100;
	}
	return 0;
}

FAUCTIONCFG_DATA URoleDropBoxInterface::GetAuctionCfg(int32 Round)
{
	const UConfigTable* AuctionTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_AUCTION_DATA);
	if (IsValid(AuctionTable))
	{
		const FAUCTIONCFG_DATA* AuctionCfgData = AuctionTable->GetRow<FAUCTIONCFG_DATA>(FString::FromInt(Round));
		if (AuctionCfgData)
		{
			return *AuctionCfgData;
		}
	}
	return FAUCTIONCFG_DATA();
}

void URoleDropBoxInterface::onPickupItemToRole_Implementation(const int32& dropBoxID, const FString& uid, const FString& dbid, const int32& targetID)
{
	if (dropBoxs.Contains(dropBoxID))
	{
		if (dropBoxs[dropBoxID]->isRalldomPickUp())
		{
			if (!dropBoxs[dropBoxID]->rollDomItems.Contains(uid))
			{
				dropBoxs[dropBoxID]->rollDomItems.Add(uid, NewObject<URollDomData>());
				dropBoxs[dropBoxID]->rollDomItems[uid]->uid = uid;
				dropBoxs[dropBoxID]->rollDomItems[uid]->ownerDBID = dbid;
				dropBoxs[dropBoxID]->rollDomItems[uid]->isPickUp = 1;
				dropBoxs[dropBoxID]->rollDomItems[uid]->maxRollDBID = dbid;
				dropBoxs[dropBoxID]->rollDomItems[uid]->maxRoll = 0;
				dropBoxs[dropBoxID]->rollDomItems[uid]->selfRoll = -1;
			}
			else
			{
				dropBoxs[dropBoxID]->rollDomItems[uid]->ownerDBID = dbid;
				dropBoxs[dropBoxID]->rollDomItems[uid]->isPickUp = 1;
				dropBoxs[dropBoxID]->rollDomItems[uid]->maxRollDBID = dbid;
			}
		}
		if (dropBoxs[dropBoxID]->isAuctionPickUp())
		{
			if (!dropBoxs[dropBoxID]->auctionItems.Contains(uid))
			{
				dropBoxs[dropBoxID]->auctionItems.Add(uid, NewObject<UAuctionData>());
				dropBoxs[dropBoxID]->auctionItems[uid]->uid = uid;
				dropBoxs[dropBoxID]->auctionItems[uid]->ownerDBID = dbid;
				dropBoxs[dropBoxID]->auctionItems[uid]->isPickUp = 1;
				dropBoxs[dropBoxID]->auctionItems[uid]->maxAuctionDBID = dbid;
			}
			else
			{
				dropBoxs[dropBoxID]->auctionItems[uid]->ownerDBID = dbid;
				dropBoxs[dropBoxID]->auctionItems[uid]->isPickUp = 1;
				dropBoxs[dropBoxID]->auctionItems[uid]->maxAuctionDBID = dbid;
			}
		}

		if (dropBoxs[dropBoxID]->isTongDropBox() && GetEntity())
		{
			AActor* tempActor = UGolbalBPFunctionLibrary::GetActorByID(dropBoxID);
			ADropBoxCharacter* dropBox = Cast<ADropBoxCharacter>(tempActor);
			if (IsValid(dropBox))
			{
				dropBox->FlyTargetEffectEvent(targetID, Tong_DropBox_FlyEffectID);
			}
		}

		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager) && dropBoxs[dropBoxID]->owners.Contains(dbid))
		{
			if (dropBoxs[dropBoxID]->isTeamDropBox())
			{
				if (dropBoxs[dropBoxID]->isRalldomPickUp())
				{
					int32 tempResult = (UGolbalBPFunctionLibrary::GetPlayerID() == targetID);
					UUECS3GameInstance::Instance->GEventManager->OnTeamRollPickupResult.Broadcast(dropBoxID, uid, tempResult);
				}
			}
		}
	}
}

void URoleDropBoxInterface::onPickUpDropBoxEnd_Implementation(int32 dropBoxID)
{
	if (dropBoxs.Contains(dropBoxID))
	{
		dropBoxs.Remove(dropBoxID);
	}

	if (dropBoxIDList.Contains(dropBoxID))
	{
		dropBoxIDList.Remove(dropBoxID);
	}

	//界面这边所有物品分配完毕后，分配结束，界面延迟10秒关闭
	TWeakObjectPtr<URoleDropBoxInterface> ThisPtr(this);
	FTimerHandle DelayHandle;
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayHandle, FTimerDelegate::CreateLambda([ThisPtr, dropBoxID]()
	{
		URoleDropBoxInterface* Interface = ThisPtr.Get();
		if (IsValid(Interface) && IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnClosedTongDicePickWnd.Broadcast(dropBoxID);

			//自由拾取的界面不在这里关闭
			//UUECS3GameInstance::Instance->GEventManager->OnClosedPickUpWnd.Broadcast(dropBoxID);

			//没拾取完的宝箱
			int32 DropBoxNum = Interface->dropBoxIDList.Num();
			if (DropBoxNum == 0)//还有宝箱没拾取，不关闭界面
			{
				UUECS3GameInstance::Instance->GEventManager->OnClosedTeamDicePickWnd.Broadcast();
			}
		}
	}), 10.0f, false);
}

void URoleDropBoxInterface::ReqAuctionHistoryData()
{
	if (auctionHistory.Num() == 0)
	{
		KBEngine::FVariantArray args;
		CellCall(TEXT("reqAuctionHistoryData"), args);
	}
	else
	{
		//通知界面
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnRecvAuctionHistoryDataEvent.Broadcast();
		}
	}
}

void URoleDropBoxInterface::recvAuctionHistoryData(const FVariantArray& datas)
{
	for (auto it : datas)
	{
		FAUCTION_HISTORY_DATA data(it);
		UAuctionHistroy* history = NewObject<UAuctionHistroy>();
		history->id = data.id;
		history->roleName = data.roleName;
		history->result = data.result;
		history->money = data.money;
		auctionHistory.Add(history);
	}

	//通知界面
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnRecvAuctionHistoryDataEvent.Broadcast();
	}
}

void URoleDropBoxInterface::updateAuctionHistoryData(const FVariant& d)
{
	FAUCTION_HISTORY_DATA data(d);
	UAuctionHistroy* history = NewObject<UAuctionHistroy>();
	history->id = data.id;
	history->roleName = data.roleName;
	history->result = data.result;
	history->money = data.money;
	auctionHistory.Add(history);

	//通知界面
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnAddAuctionHistoryEvent.Broadcast(history);
	}
}

void URoleDropBoxInterface::FlyTargerOverEvent()
{
	for (auto It = dropBoxs.CreateConstIterator(); It; ++It)
	{
		if (It->Value->isAllPickup())
			continue;

		AActor* tempActor = UGolbalBPFunctionLibrary::GetActorByID(It->Key);
		ADropBoxCharacter* dropBox = Cast<ADropBoxCharacter>(tempActor);
		if (IsValid(dropBox))
		{
			dropBox->OpenDropEffectEvent(Tong_DropBox_OpenEffectID, Tong_DropBox_StayEffectID);
		}
		break;
	}
}

void URoleDropBoxInterface::OnRecvDropBoxAuctionData(const int32& dropBoxID)
{
	if (IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		if (dropBoxs[dropBoxID]->isTongDropBox())
		{
			UBaseWindow* TongAuctionPickWindow = UUECS3GameInstance::Instance->GUIManager->GetWindow(TEXT("TongAuctionPick"));
			if (IsValid(TongAuctionPickWindow) && TongAuctionPickWindow->IsVisible())//已经打开帮会竞拍界面
			{
				//通知帮会竞拍界面增加宝箱
				if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
				{
					UUECS3GameInstance::Instance->GEventManager->OnAddDropBoxAuctionEvent.Broadcast(0, dropBoxID);
				}
			}
		}
		else if (dropBoxs[dropBoxID]->isTeamDropBox())
		{
			UBaseWindow* TeamAuctionPickWindow = UUECS3GameInstance::Instance->GUIManager->GetWindow(TEXT("TeamAuctionPick"));
			if (IsValid(TeamAuctionPickWindow) && TeamAuctionPickWindow->IsVisible())//已经打开队伍竞拍界面
			{
				//通知队伍竞拍界面增加宝箱
				if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
				{
					UUECS3GameInstance::Instance->GEventManager->OnAddDropBoxAuctionEvent.Broadcast(1, dropBoxID);
				}
			}
		}
	}
}

void URoleDropBoxInterface::OnAuctionBidPrice(const int32& dropBoxID, const FString& uid, const int32& money, const FString& dbid, const FString& countDown, const FAUCTIONMESSAGE& MessageData)
{
	//通知界面
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnAuctionBidEvent.Broadcast(dropBoxID, uid, money, dbid, countDown);
		UUECS3GameInstance::Instance->GEventManager->OnAddAuctionMessageEvent.Broadcast(dropBoxID, uid, MessageData);
	}
}

void URoleDropBoxInterface::OnAbandomAuctionItem(const int32& dropBoxID, const FString& uid, const FString& dbid, const FAUCTIONMESSAGE& MessageData)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnAuctionAbandonEvent.Broadcast(dropBoxID, uid, dbid);
		UUECS3GameInstance::Instance->GEventManager->OnAddAuctionMessageEvent.Broadcast(dropBoxID, uid, MessageData);
	}
}

void URoleDropBoxInterface::OnAuctionItemEnd(const int32& dropBoxID, const FString& uid)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnAuctionItemEndEvent.Broadcast(dropBoxID, uid);
	}
}

void URoleDropBoxInterface::OnShowAuctionWindow(const int32& dropBoxID)
{
	FString WindowType;
	int32 DropBoxType;
	if (dropBoxs[dropBoxID]->isTongDropBox())
	{
		//帮会竞拍界面
		WindowType = TEXT("TongAuctionPick");
		DropBoxType = 0;
	}
	else if (dropBoxs[dropBoxID]->isTeamDropBox())
	{
		//队伍竞拍界面
		WindowType = TEXT("TeamAuctionPick");
		DropBoxType = 1;
	}
	else
	{
		return;
	}
	if (IsValid(UUECS3GameInstance::Instance->GUIManager))
	{
		UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, WindowType);
	}
	if (IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnOpenAuctionPickWndEvent.Broadcast(DropBoxType, dropBoxID);
	}
}
