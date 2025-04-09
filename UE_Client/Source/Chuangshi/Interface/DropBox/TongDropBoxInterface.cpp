// Fill out your copyright notice in the Description page of Project Settings.


#include "TongDropBoxInterface.h"
#include "Kismet/KismetMathLibrary.h"
#include "Util/ConvertUtil.h"
#include "GameData/Item/ItemBase.h"
#include "GameData/Item/ItemFactory.h"
#include "Interface/Role/RoleTongInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "CS3Base/UIManager.h"
#include "Manager/EventManager.h"
#include "Engine/World.h"
#include "Manager/CustomCursorManager.h"
#include "../../Manager/ParticleManager.h"
#include "GameData/ConstData.h"
#include "Actor/DropBox/DropBoxCharacter.h"
#include "Actor/DropBox/TongDropBoxCharacter.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UTongDropBoxInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onOpenDropbox, &UTongDropBoxInterface::onOpenDropbox)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(recvDropBoxData, &UTongDropBoxInterface::recvDropBoxData, const FVariant&, const FVariantArray&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onPickUp, &UTongDropBoxInterface::onPickUp, const FString&, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onPickUpByLeader, &UTongDropBoxInterface::onPickUpByLeader, const FString&, const FString&, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onUpdateDropBoxModelVisible, &UTongDropBoxInterface::onUpdateDropBoxModelVisible)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(recvDropBoxNoAllocationData, &UTongDropBoxInterface::recvDropBoxNoAllocationData, const FVariantArray&, const FVariantArray&, const FVariantArray&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(updateFreeAllocationItem, &UTongDropBoxInterface::updateFreeAllocationItem, const FVariant&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UTongDropBoxInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UTongDropBoxInterface::UTongDropBoxInterface()
{
}

UTongDropBoxInterface::~UTongDropBoxInterface()
{
}

void UTongDropBoxInterface::OnRep_isCanOpen()
{
	uint8 isCanOpen = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("isCanOpen"));
	if (isCanOpen != 0)
	{
		if (GetEntity())
		{
			if (UUECS3GameInstance::pKBEApp == nullptr || UUECS3GameInstance::pKBEApp->Player() == nullptr)
				return;

			//如果是有拾取权限的玩家，这里可不用打开宝箱动画
			uint64 playerDBID = UUECS3GameInstance::pKBEApp->Player()->GetDefinedProperty(TEXT("playerDBID")).GetValue<uint64>();
			FVariant Propvalue = GetEntity()->GetDefinedProperty(TEXT("ownerDBIDs"));
			TArray<FVariant> array = Propvalue.GetValue<TArray<FVariant>>();
			for (int i = 0; i < array.Num(); i++)
			{
				UINT64 Value = UINT64(array[i].GetValue<UINT64>());
				if (playerDBID == Value)
				{
					return;
				}
			}
		}

		AServerCharacter* ServerActor = Cast<AServerCharacter>(GetActor());
		if (!IsValid(ServerActor)) return;
		ATongDropBoxCharacter* DropBox = Cast<ATongDropBoxCharacter>(ServerActor);
		if (!IsValid(DropBox)) return;
		DropBox->OpenBox();//播放开宝箱动作
	}
}

bool UTongDropBoxInterface::isVisible()
{
	if (GetEntity())
	{
		if (UUECS3GameInstance::pKBEApp == nullptr || GetEntity() == nullptr)
			return false;

		URoleTongInterface* interface = Cast<URoleTongInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTongInterface"), UUECS3GameInstance::pKBEApp->PlayerID()));
		if (interface != nullptr)
		{
			uint64 tongDBID = GetEntity()->GetDefinedProperty(TEXT("tongDBID")).GetValue<uint64>();
			if (interface->Tong->TongDBID.Equals(INT_TO_FSTRING(tongDBID)))
			{
				return true;
			}
		}
	}
	return false;
}

bool UTongDropBoxInterface::isCanOpenBox()
{
	if (!isVisible())
		return false;

	if (GetEntity())
	{
		uint8 isCanOpen = UGolbalBPFunctionLibrary::GetIntPropertyValue(GetEntity()->ID(), TEXT("isCanOpen"));
		if (isCanOpen != 0)
		{
			uint64 playerDBID = UUECS3GameInstance::pKBEApp->Player()->GetDefinedProperty(TEXT("playerDBID")).GetValue<uint64>();
			FVariant Propvalue = GetEntity()->GetDefinedProperty(TEXT("ownerDBIDs"));
			TArray<FVariant> array = Propvalue.GetValue<TArray<FVariant>>();
			for (int i = 0; i < array.Num(); i++)
			{
				UINT64 Value = UINT64(array[i].GetValue<UINT64>());
				if (playerDBID == Value)
				{
					return true;
				}
			}
		}
	}
	return false;
}

bool UTongDropBoxInterface::isAllocationType(TONG_PICKUP_TYPE type)
{
	if (GetEntity())
	{
		uint8 allocation = UGolbalBPFunctionLibrary::GetIntPropertyValue(GetEntity()->ID(), TEXT("allocation"));
		return (TONG_PICKUP_TYPE)allocation == type;
	}
	return false;
}

void UTongDropBoxInterface::onUpdateDropBoxModelVisible_Implementation()
{
}

void UTongDropBoxInterface::onOpenDropbox()
{
	//服务器通知打开宝箱
	ReqTongDropBoxData();
}

void UTongDropBoxInterface::ReqTongDropBoxData()
{
	if (isCanOpenBox())
	{
		KBEngine::FVariantArray args;
		CellCall("reqDropBoxData", args);
	}
}

void UTongDropBoxInterface::recvDropBoxData(const FVariant& owners, const FVariantArray& freeItems)
{
	ownerInfos.Empty();
	FDICT_STR_STR datas = FDICT_STR_STR(owners);
	for (auto data : datas.dictDataList)
	{
		ownerInfos.Add(data.Key, data.Value);
	}

	freeAllocationItems.Empty();
	TArray<UItemBase*> itemList = AnalyzeItemData(freeItems);
	for (auto item : itemList)
	{
		if (freeAllocationItems.Contains(item->UID))
		{
			CS3_Warning(TEXT(" error:UTongDropBoxInterface::recvDropBoxItemData :item exists"));
			continue;
		}
		freeAllocationItems.Add(item->UID, item);
	}
	AServerCharacter* ServerActor = Cast<AServerCharacter>(GetActor());
	if (!IsValid(ServerActor)) return;
	ATongDropBoxCharacter* DropBox = Cast<ATongDropBoxCharacter>(ServerActor);
	if (!IsValid(DropBox)) return;
	DropBox->OpenBox();//播放开宝箱动作

	if (freeAllocationItems.Num() > 0)
	{
		//设置可交互
		if (!DropBox->CanGossipWith())
		{
			DropBox->SetCanGossip(true);
			DropBox->SetInteractiveRadius(5.0f);
		}
	}
}

void UTongDropBoxInterface::recvDropBoxNoAllocationData(const FVariantArray& dbidList, const FVariantArray& items, const FVariantArray& notAllocation_Items)
{
	leaderHasAllocationItems.Empty();
	TArray<UItemBase*> itemList1 = AnalyzeItemData(items);
	for (int i = 0; i < itemList1.Num(); i++)
	{
		if (i >= dbidList.Num())
		{
			return;
		}
		if (!leaderHasAllocationItems.Contains(dbidList[i]))
		{
			leaderHasAllocationItems.Add(dbidList[i], NewObject<UTongAllocationItemData>());
		}
		leaderHasAllocationItems[dbidList[i]]->items.Add(itemList1[i]);
	}

	notAllocationItems.Empty();
	TArray<UItemBase*> itemList2 = AnalyzeItemData(notAllocation_Items);
	for (auto item : itemList2)
	{
		notAllocationItems.Add(item->UID, item);
	}

	if (IsValid(UUECS3GameInstance::Instance))
	{
		if (leaderHasAllocationItems.Num() > 0 || notAllocationItems.Num() > 0)
		{
			///播放一个光效
			AActor* tempActor = GetActor();
			ADropBoxCharacter* dropBox = Cast<ADropBoxCharacter>(tempActor);
			if (IsValid(dropBox))
			{
				dropBox->OpenDropEffectEvent(Tong_DropBox_OpenEffectID, Tong_DropBox_StayEffectID);
			}
			openTongLeaderPickUpWnd();
		}
	}
}

TArray<UItemBase*> UTongDropBoxInterface::AnalyzeItemData(const FVariantArray& itemList)
{
	TArray<UItemBase*> itemBaseArray;
	for (auto it : itemList)
	{
		FITEM_FOR_CLIENT itemData(it);

		UItemBase* item = UItemFactory::GetItemByID(itemData.id);
		if (!IsValid(item))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UTongDropBoxInterface::AnalyzeItemData : item!"));
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

void UTongDropBoxInterface::ReqPickUp(const TArray<FString>& uidList)
{
	for (FString uid : uidList)
	{
		if (!freeAllocationItems.Contains(uid))
		{
			return;
		}
	}
	KBEngine::FVariantArray args;
	args.Add(UGolbalBPFunctionLibrary::ListToFVariant(uidList));
	CellCall("reqPickUp", args);
}

void UTongDropBoxInterface::GetAllleaderAllocationItems(TArray<UItemBase*>& outAllocationItems, TArray<FString>& outAllocationPlayerName)
{
	for (auto i : leaderHasAllocationItems)
	{
		UTongAllocationItemData* data = i.Value;
		for (auto item : data->items)
		{
			outAllocationItems.Add(item);
			outAllocationPlayerName.Add(ownerInfos[i.Key]);
		}
	}
	for (typename TMap<FString, UItemBase*>::TConstIterator Iterator(notAllocationItems); Iterator; ++Iterator)
	{
		outAllocationItems.Add(Iterator.Value());
		outAllocationPlayerName.Add("");
	}
}

void UTongDropBoxInterface::onPickUp_Implementation(const FString& uid, const FString& playerDBID)
{
	if (freeAllocationItems.Contains(uid))
	{
		freeAllocationItems.Remove(uid);
	}
	//通知界面
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnPickUpSuccessed.Broadcast(EntityID, uid);
	}
}

void UTongDropBoxInterface::onPickUpByLeader_Implementation(const FString& uid, const FString& playerDBID, const int32& targetID)
{
	if (notAllocationItems.Contains(uid))
	{
		if (!leaderHasAllocationItems.Contains(playerDBID))
		{
			leaderHasAllocationItems.Add(playerDBID, NewObject<UTongAllocationItemData>());
		}
		leaderHasAllocationItems[playerDBID]->items.Add(notAllocationItems[uid]);
		notAllocationItems.Remove(uid);

		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			if (GetEntity())
			{
				AActor* tempActor = GetActor();
				ADropBoxCharacter* dropBox = Cast<ADropBoxCharacter>(tempActor);
				if (IsValid(dropBox))
				{
					dropBox->FlyTargetEffectEvent(targetID, Tong_DropBox_FlyEffectID);
				}
			}
			if (ownerInfos.Contains(playerDBID))
			{
				UUECS3GameInstance::Instance->GEventManager->OnPickUpByLeaderSuccessed.Broadcast(uid, ownerInfos[playerDBID]);
			}
			//界面这边所有物品分配完毕后，分配结束，界面延迟10秒关闭
			if (notAllocationItems.Num() == 0)
			{
				TWeakObjectPtr<UTongDropBoxInterface> ThisPtr(this);
				FTimerHandle DelayHandle;
				UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayHandle, FTimerDelegate::CreateLambda([ThisPtr]()
				{
					UTongDropBoxInterface* Interface = ThisPtr.Get();
					if (IsValid(Interface) && IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
					{
						UUECS3GameInstance::Instance->GEventManager->OnClosedTongPickWnd.Broadcast(Interface->EntityID);
					}
				}), 10.0f, false);
			}
		}
	}
}

void UTongDropBoxInterface::ReqPickUpToMember(const FString& uid, const FString& InPlayerName)
{
	if (isAllocationType(TONG_PICKUP_TYPE::TONG_PICKUP_TYPE_LEADER))
	{
		if (isCanOpenBox())
		{
			if (notAllocationItems.Contains(uid))
			{
				URoleTongInterface* interface = Cast<URoleTongInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTongInterface"), UUECS3GameInstance::pKBEApp->PlayerID()));
				if (interface != nullptr && interface->Tong != nullptr)
				{
					if (ownerInfos.FindKey(InPlayerName))
					{
						uint64 tempPlayerDBID = FSTRING_TO_INT(*ownerInfos.FindKey(InPlayerName));
						int32 dbid = UGolbalBPFunctionLibrary::GetIntPropertyValue(GetEntity()->ID(), TEXT("tongDBID"));
						if( ( FSTRING_TO_INT(interface->Tong->TongDBID) == dbid) && (interface->Tong->PlayerMember != nullptr && interface->Tong->TongLeaderDBID.Equals(interface->Tong->PlayerMember->DBID)))
						{
							KBEngine::FVariantArray args;
							args.Add(uid);
							args.Add(tempPlayerDBID);
							CellCall("reqPickUpToMember", args);
						}
					}
				}
			}
		}
	}
}

void UTongDropBoxInterface::updateFreeAllocationItem(const FVariant& FVariantItem)
{
	FITEM_FOR_CLIENT itemData(FVariantItem);
	UItemBase* itembase = UItemFactory::GetItemByID(itemData.id);
	if (!IsValid(itembase))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTongDropBoxInterface::updateFreeAllocationItem : item!"));
	}
	itembase->UID = itemData.uid;
	itembase->Amount = itemData.amount;
	itembase->BindType = itemData.bindType;
	itembase->ItemOrder = itemData.itemOrder;
	itembase->ItemEndTime = itemData.itemEndTime;
	itembase->InitDynamicDataForJson(itemData.dynamicData);
	freeAllocationItems.Add(itembase->UID, itembase);

	AServerCharacter* ServerActor = Cast<AServerCharacter>(GetActor());
	if (IsValid(ServerActor))
	{
		ATongDropBoxCharacter* DropBox = Cast<ATongDropBoxCharacter>(ServerActor);
		if (IsValid(DropBox) && !DropBox->CanGossipWith())
		{
			DropBox->SetCanGossip(true);
			DropBox->SetInteractiveRadius( 5.0f );
		}
	}
}

void UTongDropBoxInterface::FlyTargerOverEvent()
{
	if (notAllocationItems.Num() > 0)
	{
		///播放一个光效
		AActor* tempActor = GetActor();
		ADropBoxCharacter* dropBox = Cast<ADropBoxCharacter>(tempActor);
		if (IsValid(dropBox))
		{
			dropBox->OpenDropEffectEvent(Tong_DropBox_OpenEffectID, Tong_DropBox_StayEffectID);
		}
	}
}

void UTongDropBoxInterface::InitBlueCB()
{
	Supper::InitBlueCB();
}

void UTongDropBoxInterface::openTongLeaderPickUpWnd()
{
	if (leaderHasAllocationItems.Num() > 0 || notAllocationItems.Num() > 0)
	{
		if (IsValid(UUECS3GameInstance::Instance->GUIManager))
		{
			//打开帮主分配界面
			UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("TongPick"));
		}
		if (IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnOpenTongPickWnd.Broadcast(EntityID);
		}
	}
}

