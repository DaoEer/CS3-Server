// Fill out your copyright notice in the Description page of Project Settings.


#include "ItemFactory.h"
#include "GameData/TexturePath.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameData/StrToClass.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "GameData/ConstData.h"
#include"Chuangshi.h"
#include "Manager/CfgManager.h"

UItemFactory* UItemFactory::GetInstance()
{
	cs3_checkNoReentry();

	return (UItemFactory*)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_ItemFactory")));
}


UItemBase* UItemFactory::GetItemByID(int32 itemid)
{
	FCS3ItemData itemdata = GetStaticDataByItemID(itemid);
	const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_STRTOCLASS);
	FStrToClass* data = const_cast<FStrToClass*>(table->GetRow<FStrToClass>(itemdata.Script));
	if (data == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UItemFactory::GetItemByID : data!"));
		return nullptr;
	}
	UClass* itemclass = data->GetTargetClass();
	UItemBase* item = (UItemBase *)StaticConstructObject_Internal(itemclass);
	item->ItemID = itemdata.ItemID;
	item->ItemName = itemdata.ItemName;
	item->Script = itemdata.Script;
	item->Icon = itemdata.Icon;
	item->ItemType = itemdata.Type;
	if (itemdata.BindType == int(EINITBINDTYPE::NONE_BIND) || itemdata.BindType == int(EINITBINDTYPE::EQUIP_BIND))
	{
		item->BindType = int(EBINDTYPE::BIND_NONE);
	}
	else
	{
		item->BindType = int(EBINDTYPE::BINDED);
	}
	item->PickupType = itemdata.PickUpType;
	item->Level = itemdata.Level;
	item->Quality = itemdata.Quality;
	item->Price = itemdata.Price;
	item->MaxTakeAmount = itemdata.MaxTakeAmount;
	item->CanDestroy = itemdata.CanDestroy;
	item->CanSell = itemdata.CanSell;
	item->Describe = itemdata.Describe;
	item->ReqClasses = itemdata.ReqClasses;
	item->ReqLevel = itemdata.ReqLevel;
	item->ReqJingJieLevel = itemdata.ReqJingJieLevel;
	item->SkillID = itemdata.SkillID;
	item->CanReturn = itemdata.CanReturn;
	item->UseAmount = itemdata.UseAmount;
	item->Param1 = itemdata.Param1;
	item->Param2 = itemdata.Param2;
	item->Param3 = itemdata.Param3;
	item->Param4 = itemdata.Param4;
	item->Param5 = itemdata.Param5;
	TArray<FString> result = UGolbalBPFunctionLibrary::SplitString(itemdata.StackAmount, false, TEXT("|"));
	if (result.Num() > 0)
	{
		item->OverlyingType = FSTRING_TO_INT(result[0]);
		if (item->OverlyingType == 0)			//不可叠加
		{
			item->OverlyingMax = 0;
		}
		else
		{
			if (result.Num() >= 2)
			{
				item->OverlyingMax = FSTRING_TO_INT(result[1]);
				if (item->OverlyingType == 1)
				{
					item->CanShowOverlying = true;
				}
				else
				{
					item->CanShowOverlying = false;
					if (result.Num() >= 3)
					{
						if (result[2].Equals("1"))
						{
							item->CanShowOverlying = true;
						}
					}
				}
				
			}
			else
			{
				CS3_Warning(TEXT("Item(%d) init err!as StackAmount(%s) err"), item->ItemID, *itemdata.StackAmount);
			}
		}
	}
	return item;
}

const FCS3ItemData UItemFactory::GetStaticDataByItemID(int32 itemid)
{
	FCS3ItemData itemdata;
	itemdata.ItemID = 0;
	const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ITEMDATA);
	const FCS3ItemData* data = table->GetRow<FCS3ItemData>(INT_TO_FSTRING(itemid));
	if (data != nullptr)
	{
		return *data;
	}
	else
	{
		CS3_Warning(TEXT("can't find itemid[%d] config in table ItemDataCfg"), itemid);
		return itemdata;
	}
}

FString UItemFactory::GetIconPath(int32 itemid)
{
	if (GetStaticDataByItemID(itemid).ItemID == itemid)
	{
		FString icon = GetStaticDataByItemID(itemid).Icon;
		const UConfigTable* TextureTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ITEM_ICON);
		const FCS3TexturePath* textuerstruct = TextureTable->GetRow<FCS3TexturePath>(icon);
		if (textuerstruct)
		{
			return textuerstruct->TexturePath.GetLongPackageName();
		}
	}
	return TEXT("");
}

EQUIP_TYPE UItemFactory::GetEquipType(int32 itemid)
{
	UItemBase* iteminst = GetItemByID(itemid);
	if (IsValid(iteminst) && iteminst->IsEquip())
	{
		UEquip* equip = Cast<UEquip>(iteminst);
		int32 type = int32(equip->GetModelPartType());
		if (EQUIP_WEAPON.Contains(type))
		{
			return EQUIP_TYPE::EQUIP_TYPE_WEAPON;
		}
		else if (EQUIP_ARMOR.Contains(type))
		{
			return EQUIP_TYPE::EQUIP_TYPE_ARMOR;
		}
		else if (EQUIP_JEWELRY.Contains(type))
		{
			return EQUIP_TYPE::EQUIP_TYPE_JEWELRY;
		}
	}
	return EQUIP_TYPE::EQUIP_TYPE_NONE;
}

void UItemFactory::AsyncLoadItemIconAsset(FResourceLoaderIconDelegate DelegateToCall, int32 itemid, FString ItemIcon)
{
	if (ItemIcon == TEXT(""))
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UItemFactory::AsyncLoadItemIconAsset-----ItemIcon is empty"));
		return;
	}
	if (!IsValid(UGolbalBPFunctionLibrary::CfgManager())) return;

	const UConfigTable* TableData = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ITEM_ICON);
	FCS3TexturePath* TextureStruct = const_cast<FCS3TexturePath*>(TableData->GetRow<FCS3TexturePath>(ItemIcon));
	if (TextureStruct)
	{
		if (!IsValid(TextureStruct->TexturePath.Get()))
		{
			if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->ItemFactory))
			{
				UUECS3GameInstance::Instance->ResourceManager->RequestAsyncItemIconLoad(UUECS3GameInstance::Instance->ItemFactory, TextureStruct->TexturePath, DelegateToCall, itemid);
			}
		}
		else if (DelegateToCall.IsBound())
		{
			DelegateToCall.ExecuteIfBound(itemid, TextureStruct->TexturePath.Get() );
		}
	}
}

void UItemFactory::ItemTipsInfoCopy(UItemBase* SrcItem, UItemBase* DstItem)
{
	DstItem->Quality = SrcItem->Quality;
	DstItem->Describe = SrcItem->Describe;
	DstItem->ItemName = SrcItem->ItemName;
	DstItem->Icon = SrcItem->Icon;
	DstItem->ReqLevel = SrcItem->ReqLevel;
	DstItem->ReqJingJieLevel = SrcItem->ReqJingJieLevel;
	DstItem->ReqClasses = SrcItem->ReqClasses;
	DstItem->BindType = SrcItem->BindType;
	DstItem->Amount = SrcItem->Amount;
	DstItem->Price = SrcItem->Price;
	DstItem->OverlyingType = SrcItem->OverlyingType;
	DstItem->ItemEndTime = SrcItem->ItemEndTime;
	DstItem->UseAmount = SrcItem->UseAmount;
	DstItem->OverlyingMax = SrcItem->OverlyingMax;
	DstItem->ItemType = SrcItem->ItemType;
	DstItem->Level = SrcItem->Level;
}

void UItemFactory::EquipTipsInfoCopy(UEquip* SrcItem, UEquip* DstItem)
{
	ItemTipsInfoCopy(SrcItem, DstItem);

	DstItem->Hardiness = SrcItem->Hardiness;
	DstItem->ModelPartType = SrcItem->ModelPartType;
	DstItem->CombatPower = SrcItem->CombatPower;
	DstItem->IntensifyArray = SrcItem->IntensifyArray;
	DstItem->AttackPropertiesStr = SrcItem->AttackPropertiesStr;
	DstItem->AttachPropertiesStr = SrcItem->AttachPropertiesStr;
	DstItem->IntensifyDataStr = SrcItem->IntensifyDataStr;
	DstItem->ReturnBackTime = SrcItem->ReturnBackTime;
}
