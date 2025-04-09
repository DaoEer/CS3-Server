// Fill out your copyright notice in the Description page of Project Settings.

#include "RoleSpellBoxDropItemInterface.h"
#include "Entity/Alias.h"
#include "KBEngine.h"
#include "GameData/Item/ItemFactory.h"
#include "Actor/SpellBox/SpellBoxCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleSpellBoxDropItemInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(SendSpellBoxPickItems, &URoleSpellBoxDropItemInterface::SendSpellBoxPickItems, const int32&, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnPickUpSpellBoxToMember, &URoleSpellBoxDropItemInterface::OnPickUpSpellBoxToMember, const int32&, const FString&, const FVariant&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleSpellBoxDropItemInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

URoleSpellBoxDropItemInterface::URoleSpellBoxDropItemInterface()
{

}

URoleSpellBoxDropItemInterface::~URoleSpellBoxDropItemInterface()
{

}

void URoleSpellBoxDropItemInterface::SendSpellBoxPickItems(const int32& spellBoxEntityID, const FVariant& Var)
{
	TArray<UItemBase*> SpellBoxItemList = AnalyzeSpellBoxPickItems(Var);
	AActor* actor = UGolbalBPFunctionLibrary::GetActorByID(spellBoxEntityID);
	if (IsValid(actor))
	{
		ASpellBoxCharacter* spellBoxCharacter = Cast<ASpellBoxCharacter>(actor);
		if (IsValid(spellBoxCharacter))
		{
			ClearPickUpSpellBoxItemData();
			SpellBox_ItemList = SpellBoxItemList;
			OnShowSpellBoxPickItems(spellBoxEntityID);
		}
	}
}

TArray<UItemBase*> URoleSpellBoxDropItemInterface::AnalyzeSpellBoxPickItems(const FVariant& Var)
{
	KBEngine::FVariantArray ItemDatas = Var.GetValue<KBEngine::FVariantArray>();
	TArray<SIMPLE_ITEM_DICT> ItemTempDatas = TArray<SIMPLE_ITEM_DICT>();
	TArray<UItemBase*> SpellBoxItemList = TArray<UItemBase*>();
	for (FVariant& ItemData : ItemDatas)
	{
		SIMPLE_ITEM_DICT element1 = SIMPLE_ITEM_DICT(ItemData);
		ItemTempDatas.Add(element1);
	}
	for (SIMPLE_ITEM_DICT ItemTempData : ItemTempDatas)
	{
		UItemBase* item = UItemFactory::GetItemByID(ItemTempData.id);
		if (!IsValid(item))
		{
			CS3_Warning(TEXT("-->Null Pointer error:URoleSpellBoxDropItemInterface::SendSpellBoxPickItems : item!"));
			continue;
		}
		item->UID = FString::Printf(TEXT( "%llu" ), ItemTempData.uid);
		item->Amount = ItemTempData.amount;
		item->BindType = ItemTempData.bindType;
		item->InitDynamicDataForJson(ItemTempData.dynamicData);
		SpellBoxItemList.Add(item);
	}
	return SpellBoxItemList;
}

void URoleSpellBoxDropItemInterface::NotifySpellBoxInteractiveOver(const int32& spellBoxEntityID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpellBoxDropItemInterface::NotifySpellBoxInteractiveOver : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(spellBoxEntityID);
	GetEntity()->CellCall(TEXT("notifySpellBoxInteractiveOver"), args);
}

void URoleSpellBoxDropItemInterface::PickUpSpellBoxItem(const int32& spellBoxEntityID, const TArray<FString>& ItemUidList)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpellBoxDropItemInterface::PickUpSpellBoxItem : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(spellBoxEntityID);
	args.Add(UGolbalBPFunctionLibrary::ListToFVariant(ItemUidList));
	GetEntity()->CellCall(TEXT("pickUpSpellBoxItem"), args);
}

void URoleSpellBoxDropItemInterface::ClearPickUpSpellBoxItemData()
{
	SpellBox_ItemList.Empty();
}

void URoleSpellBoxDropItemInterface::OnPickUpSpellBoxToMember(const int32& SpellBoxEntityID, const FString& UId, const FVariant& Members)
{

	KBEngine::FVariantArray Members_Ex = Members.GetValue<KBEngine::FVariantArray>();
	TMap<int32, FString> TempData;
	for (auto MemberStr : Members_Ex)
	{
		auto VariantData = MemberStr.GetValue<KBEngine::FVariantMap>();
		int32 ID = VariantData[TEXT("id")].GetValue<int32>();
		FString Name = VariantData[TEXT("name")].GetValue<FString>();
		TempData.Add(ID, Name);
	}

	OnPickUpSpellBoxToMember_BP(SpellBoxEntityID, UId, TempData);
}

void URoleSpellBoxDropItemInterface::OnPickUpSpellBoxToMember_BP_Implementation(int32 SpellBoxEntityID,const FString& UId, const TMap<int32, FString>& MemberInfos)
{

}

void URoleSpellBoxDropItemInterface::PickUpSpellBoxToMember(int32 SpellBoxEntityID, const FString ItemUId, const int32 DstEntityID)
{

	KBEngine::FVariantArray args;
	args.Add(SpellBoxEntityID);
	args.Add(ItemUId);
	args.Add(DstEntityID);
	CellCall(TEXT("CELL_pickUpSpellBoxToMember"), args);
}

void URoleSpellBoxDropItemInterface::OnSpellBoxPickItemDestroyed(const int32& spellBoxEntityID)
{
	NotifySpellBoxInteractiveOver(spellBoxEntityID);
	ClearPickUpSpellBoxItemData();
	BP_OnSpellBoxPickItemDestroyed(spellBoxEntityID);
}

void URoleSpellBoxDropItemInterface::OnPickUpSpellBoxItem_Implementation(const int32& spellBoxEntityID,const FString& ItemUid)
{
	for (auto item : SpellBox_ItemList)
	{
		if (item->UID == ItemUid)
		{
			SpellBox_ItemList.Remove(item);
			break;
		}
	}
}

void URoleSpellBoxDropItemInterface::onLeaveWorld()
{
	ClearPickUpSpellBoxItemData();
	Supper::onLeaveWorld();
}

void URoleSpellBoxDropItemInterface::InitBlueCB()
{
	ArrBlueFunc.Add("OnPickUpSpellBoxItem");
	ArrBlueFunc.Add("SendSpellBoxPickItems");
	Supper::InitBlueCB();
}
