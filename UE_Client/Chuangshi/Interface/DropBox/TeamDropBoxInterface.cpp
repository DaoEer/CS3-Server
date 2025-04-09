// Fill out your copyright notice in the Description page of Project Settings.


#include "TeamDropBoxInterface.h"
#include "Kismet/KismetMathLibrary.h"
#include "Util/ConvertUtil.h"
#include "GameData/Item/ItemBase.h"
#include "GameData/Item/ItemFactory.h"
#include "Interface/Role/RoleTeamInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "CS3Base/UIManager.h"
#include "Manager/EventManager.h"
#include "Engine/World.h"
#include "Manager/CustomCursorManager.h"
#include "../../Manager/ParticleManager.h"
#include "Actor/DropBox/DropBoxCharacter.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UTeamDropBoxInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onOpenDropbox, &UTeamDropBoxInterface::onOpenDropbox)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(recvDropBoxData, &UTeamDropBoxInterface::recvDropBoxData, const FVariant&, const FVariantArray&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onPickUp, &UTeamDropBoxInterface::onPickUp, const FString&, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onPickUpByLeader, &UTeamDropBoxInterface::onPickUpByLeader, const FString&, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onUpdateDropBoxModelVisible, &UTeamDropBoxInterface::onUpdateDropBoxModelVisible)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(recvDropBoxNoAllocationData, &UTeamDropBoxInterface::recvDropBoxNoAllocationData, const FVariantArray&, const FVariantArray&, const FVariantArray&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(updateFreeAllocationItem, &UTeamDropBoxInterface::updateFreeAllocationItem, const FVariant&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UTeamDropBoxInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UTeamDropBoxInterface::UTeamDropBoxInterface()
{
}

UTeamDropBoxInterface::~UTeamDropBoxInterface()
{
}

bool UTeamDropBoxInterface::isVisible()
{
	if (GetEntity())
	{
		if (UUECS3GameInstance::pKBEApp == nullptr || UUECS3GameInstance::pKBEApp->Player() == nullptr)
			return false;

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
	return false;
}

bool UTeamDropBoxInterface::isCanOpenBox()
{
	if (!isVisible())
		return false;

	if (GetEntity())
	{
		uint8 isCanOpen = UGolbalBPFunctionLibrary::GetIntPropertyValue(GetEntity()->ID(), TEXT("isCanOpen"));
		if (isCanOpen != 0)
		{
			return true;
		}
	}
	return false;
}

bool UTeamDropBoxInterface::isCanPickUpMember()
{
	if (!isVisible())
		return false;

	if (UUECS3GameInstance::pKBEApp == nullptr || UUECS3GameInstance::pKBEApp->Player() == nullptr || GetEntity() == nullptr)
		return false;

	uint64 playerDBID = UUECS3GameInstance::pKBEApp->Player()->GetDefinedProperty(TEXT("playerDBID")).GetValue<uint64>();
	uint64 teamCaptainDBID = GetEntity()->GetDefinedProperty(TEXT("teamCaptainDBID")).GetValue<uint64>();
	if (playerDBID == teamCaptainDBID)
	{
		return true;
	}
	return false;
}

bool UTeamDropBoxInterface::isAllocationType(TEAM_PICKUP_TYPE type)
{
	if (GetEntity())
	{
		uint8 allocation = UGolbalBPFunctionLibrary::GetIntPropertyValue(GetEntity()->ID(), TEXT("allocation"));
		return (TEAM_PICKUP_TYPE)allocation == type;
	}
	return false;
}

void UTeamDropBoxInterface::onUpdateDropBoxModelVisible_Implementation()
{
}

void UTeamDropBoxInterface::onOpenDropbox()
{
	//服务器通知打开宝箱
	ReqTeamDropBoxData();
}

void UTeamDropBoxInterface::ReqTeamDropBoxData()
{
	if (isCanOpenBox())
	{
		KBEngine::FVariantArray args;
		CellCall("reqDropBoxData", args);
	}
}

void UTeamDropBoxInterface::recvDropBoxData(const FVariant& owners, const FVariantArray& freeItems)
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
			CS3_Warning(TEXT(" error:UTeamDropBoxInterface::recvDropBoxItemData :item exists"));
			continue;
		}
		freeAllocationItems.Add(item->UID, item);
	}

	AServerCharacter* ServerActor = Cast<AServerCharacter>(GetActor());
	if (IsValid(ServerActor))
	{
		ADropBoxCharacter* DropBox = Cast<ADropBoxCharacter>(ServerActor);
		if (IsValid(DropBox))
		{
			DropBox->OpenBox();
		}
	}

	OpenFreePickUpWnd();
}

void UTeamDropBoxInterface::recvDropBoxNoAllocationData(const FVariantArray& dbidList, const FVariantArray& items, const FVariantArray& notAllocation_Items)
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
			leaderHasAllocationItems.Add(dbidList[i], NewObject<UTeamAllocationItemData>());
		}
		leaderHasAllocationItems[dbidList[i]]->items.Add(itemList1[i]);
	}

	notAllocationItems.Empty();
	TArray<UItemBase*> itemList2 = AnalyzeItemData(notAllocation_Items);
	for (auto item : itemList2)
	{
		notAllocationItems.Add(item->UID, item);
	}
	//通知界面
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GUIManager) && IsValid(UUECS3GameInstance::Instance->GEventManager) && (notAllocationItems.Num() > 0))
	{
		if (leaderHasAllocationItems.Num() > 0 || notAllocationItems.Num() > 0)
		{

			UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("TeamPick"));
			UUECS3GameInstance::Instance->GEventManager->OnUpdateTeamPickWnd.Broadcast(EntityID);
		}
	}
}

TArray<UItemBase*> UTeamDropBoxInterface::AnalyzeItemData(const FVariantArray& itemList)
{
	TArray<UItemBase*> itemBaseArray;
	for (auto it : itemList)
	{
		FITEM_FOR_CLIENT itemData(it);

		UItemBase* item = UItemFactory::GetItemByID(itemData.id);
		if (!IsValid(item))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UTeamDropBoxInterface::AnalyzeItemData : item!"));
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

void UTeamDropBoxInterface::ReqPickUp(const TArray<FString>& uidList)
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

void UTeamDropBoxInterface::GetAllleaderAllocationItems(TArray<UItemBase*>& outAllocationItems, TArray<FString>& outAllocationPlayerName)
{
	for (auto i : leaderHasAllocationItems)
	{
		UTeamAllocationItemData* data = i.Value;
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

void UTeamDropBoxInterface::OpenFreePickUpWnd()
{
	if (IsValid(UUECS3GameInstance::Instance) && (freeAllocationItems.Num() > 0))
	{
		if (IsValid(UUECS3GameInstance::Instance->GUIManager))
		{
			//打开自由拾取界面
			UUECS3GameInstance::Instance->GUIManager->OpenWindow(false, EGameStatus::InWorld, TEXT("DropBoxPickUp"));
		}
		if (IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnTeamUpdatePickUpWnd.Broadcast(EntityID);
		}
	}
}

void UTeamDropBoxInterface::onPickUp_Implementation(const FString& uid, const FString& playerDBID)
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

void UTeamDropBoxInterface::onPickUpByLeader_Implementation(const FString& uid, const FString& playerDBID)
{
	if (notAllocationItems.Contains(uid))
	{
		if (!leaderHasAllocationItems.Contains(playerDBID))
		{
			leaderHasAllocationItems.Add(playerDBID, NewObject<UTeamAllocationItemData>());
		}
		leaderHasAllocationItems[playerDBID]->items.Add(notAllocationItems[uid]);
		notAllocationItems.Remove(uid);
	}

	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		if (ownerInfos.Contains(playerDBID))
		{
			UUECS3GameInstance::Instance->GEventManager->OnPickUpByCaptainSuccessed.Broadcast(uid, ownerInfos[playerDBID]);
		}
		//界面这边所有物品分配完毕后，分配结束，界面延迟10秒关闭
		if (notAllocationItems.Num() == 0)
		{
			TWeakObjectPtr<UTeamDropBoxInterface> ThisPtr(this);
			FTimerHandle DelayHandle;
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayHandle, FTimerDelegate::CreateLambda([ThisPtr]()
			{
				UTeamDropBoxInterface* Interface = ThisPtr.Get();
				if (IsValid(Interface) && IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
				{
					UUECS3GameInstance::Instance->GEventManager->OnClosedTeamPickWnd.Broadcast(Interface->EntityID);
				}
			}), 10.0f, false);
		}
	}
}

void UTeamDropBoxInterface::ReqPickUpToMember(const FString& uid, const FString& InPlayerName)
{
	if (isAllocationType(TEAM_PICKUP_TYPE::TEAM_PICKUP_TYPE_CAPTAIN))
	{
		if (isCanOpenBox() && GetEntity())
		{
			if (notAllocationItems.Contains(uid))
			{
				URoleTeamInterface* interface = Cast<URoleTeamInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTeamInterface"), UUECS3GameInstance::pKBEApp->PlayerID()));
				if (interface != nullptr)
				{
					if (ownerInfos.FindKey(InPlayerName))
					{
						uint64 tempPlayerDBID = FSTRING_TO_INT(*ownerInfos.FindKey(InPlayerName));
						uint64 playerDBID = UUECS3GameInstance::pKBEApp->Player()->GetDefinedProperty(TEXT("playerDBID")).GetValue<uint64>();
						uint64 teamCaptainDBID = GetEntity()->GetDefinedProperty(TEXT("teamCaptainDBID")).GetValue<uint64>();
						if (playerDBID == teamCaptainDBID)
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

void UTeamDropBoxInterface::updateFreeAllocationItem(const FVariant& FVariantItem)
{
	FITEM_FOR_CLIENT itemData(FVariantItem);
	UItemBase* itembase = UItemFactory::GetItemByID(itemData.id);
	if (!IsValid(itembase))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTeamDropBoxInterface::updateFreeAllocationItem : item!"));
	}
	itembase->UID = itemData.uid;
	itembase->Amount = itemData.amount;
	itembase->BindType = itemData.bindType;
	itembase->ItemOrder = itemData.itemOrder;
	itembase->ItemEndTime = itemData.itemEndTime;
	itembase->InitDynamicDataForJson(itemData.dynamicData);
	freeAllocationItems.Add(itembase->UID, itembase);

	//OpenFreePickUpWnd();
	
}

void UTeamDropBoxInterface::InitBlueCB()
{
	Supper::InitBlueCB();
}

