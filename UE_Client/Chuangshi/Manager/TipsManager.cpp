// Fill out your copyright notice in the Description page of Project Settings.


#include "TipsManager.h"
#include "GameData/Item/Equip.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "interface/Role/RoleKitBagInterface.h"
#include "interface/Role/RoleDropBoxInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameData/Item/ItemFactory.h"
#include "Manager/SkillManager.h"
#include "Util/ConvertUtil.h"
#include "GameData/Item/ToolCost.h"
#include "Interface/Role/RoleWorkShopInterface.h"
#include "GameData/Item/ItemComposeEquipBP.h"
#include "GameData/Item/EquipPart.h"
#include "Util/CS3Debug.h"
#include "GameData/Item/ItemJadeCommond.h"
#include "BuffManager.h"
#include "GameData/Skill/BuffTableData.h"
#include "Interface/SkillInterface.h"
#include "TimeManager.h"

CONTROL_COMPILE_OPTIMIZE_START
UTipsManager::UTipsManager()
{

}

UTipsManager* UTipsManager::GetInstance()
{
	cs3_checkNoReentry();

	return (UTipsManager*)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_TipsManager")));
}

void UTipsManager::ShowInfoTips(INFO_TIPS_TYPE TipsType /*= INFO_TIPS_TYPE::TOOL_TIPS_TYPE*/, const FString& InfoKeys /*= TEXT("")*/)
{
	if (InfoKeys.IsEmpty()) return;
	TipsInfoInst = nullptr;
	switch (TipsType)
	{
	case INFO_TIPS_TYPE::TOOL_TIPS_TYPE://普通信息提示
	{
		TipsInfoInst = NewObject<UToolInfo>();
		TipsInfoInst->TipsType = TipsType;
		TipsInfoInst->InitFormatInfoTips(InfoKeys);
		ShowToolTips(TipsInfoInst);
		break;
	}
	case INFO_TIPS_TYPE::ITEM_TIPS_TYPE://物品信息提示
	{
		TipsInfoInst = NewObject<UItemInfo>();
		TipsInfoInst->TipsType = TipsType;
		TipsInfoInst->InitFormatInfoTips(InfoKeys);
		ShowItemTips((UItemInfo*)TipsInfoInst);
		break;
	}
	case INFO_TIPS_TYPE::EQUIP_TIPS_TYPE://装备信息提示
	{
		TipsInfoInst = NewObject<UEquipInfo>();
		TipsInfoInst->TipsType = TipsType;
		TipsInfoInst->InitFormatInfoTips(InfoKeys);
		ShowEquipTips((UEquipInfo*)TipsInfoInst);
		break;
	}
	case INFO_TIPS_TYPE::SKILL_TIPS_TYPE://技能信息提示
	{
		TipsInfoInst = NewObject<USkillInfo>();
		TipsInfoInst->TipsType = TipsType;
		TipsInfoInst->InitFormatInfoTips(InfoKeys);
		ShowSkillTips((USkillInfo*)TipsInfoInst);
		break;
	}
	case INFO_TIPS_TYPE::BUFF_TIPS_TYPE://Buff信息提示
	{
		TipsInfoInst = NewObject<UBuffInfo>();
		TipsInfoInst->TipsType = TipsType;
		TipsInfoInst->InitFormatInfoTips(InfoKeys);
		ShowBuffTips((UBuffInfo*)TipsInfoInst);
		break;
	}
	case INFO_TIPS_TYPE::GOODS_TIPS_TYPE://商品信息提示
	{
		TipsInfoInst = NewObject<UGoodsInfo>();
		TipsInfoInst->TipsType = TipsType;
		TipsInfoInst->InitFormatInfoTips(InfoKeys);
		ShowGoodsTips((UGoodsInfo*)TipsInfoInst);
		break;
	}
	case INFO_TIPS_TYPE::BLUEPRINT_TIPS_TYPE://图纸信息提示
	{
		TipsInfoInst = NewObject<UBlueprintInfo>();
		TipsInfoInst->TipsType = TipsType;
		TipsInfoInst->InitFormatInfoTips(InfoKeys);
		ShowBlueprintTips((UBlueprintInfo*)TipsInfoInst);
		break;
	}
	case INFO_TIPS_TYPE::EQUIPPART_TIPS_TYPE://半成品装备信息提示
	{
		TipsInfoInst = NewObject<UEquipPartInfo>();
		TipsInfoInst->TipsType = TipsType;
		TipsInfoInst->InitFormatInfoTips(InfoKeys);
		ShowEquipPartTips((UEquipPartInfo*)TipsInfoInst);
		break;
	}
	default:
		break;
	}
}

void UTipsManager::ShowInfoTipsByItem(UItemBase* ItemBase)
{
	if (!IsValid(ItemBase))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTipsManager::ShowInfoTipsByItem : ItemBase!"));
		return;
	}
	//是装备
	if (ItemBase->IsEquip())
	{
		TipsInfoInst = NewObject<UEquipInfo>();
		TipsInfoInst->TipsType = INFO_TIPS_TYPE::EQUIP_TIPS_TYPE;
		UEquipInfo* tempEquipInfo = (UEquipInfo*)TipsInfoInst;
		if (!IsValid(tempEquipInfo)) return;
		UEquip* Equip = Cast<UEquip>(ItemBase);
		if (!IsValid(Equip)) return;
		tempEquipInfo->EquipTipsData = tempEquipInfo->GetEquipTipsData(Equip);
		URoleKitBagInterface* kitbaginterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface")));
		UEquip* equip_ = Cast<UEquip>(ItemBase);
		if (kitbaginterface && equip_)
		{
			kitbaginterface->GetSamePartEquipByItem(tempEquipInfo->PlayerEquipUIds, equip_);
		}
		
		ShowEquipTips(tempEquipInfo);
	}
	//是物品
	else
	{
		TipsInfoInst = NewObject<UItemInfo>();
		TipsInfoInst->TipsType = INFO_TIPS_TYPE::ITEM_TIPS_TYPE;
		UItemInfo* tempItemInfo = (UItemInfo*)TipsInfoInst;
		if (!IsValid(tempItemInfo)) return;
		tempItemInfo->SetItemInfo(ItemBase);
		ShowItemTips(tempItemInfo);
	}
}

void UTipsManager::ShowToolTips(const UToolInfo* info)
{
	if (!IsValid(ToolInfoTips))
	{
		ToolInfoTips = CreateTipWidget(INFO_TIPS_TYPE::TOOL_TIPS_TYPE);
		if (ToolInfoTips)
		{
			ToolInfoTips->InitInfo();
			ToolInfoTips->ShowToolTips(info->InfoTips);
		}
	}
	else
	{
		ToolInfoTips->ShowToolTips(info->InfoTips);
	}
}

void UTipsManager::ShowItemTips(const UItemInfo* info)
{
	if (!IsValid(ItemInfoTips))
	{
		ItemInfoTips = CreateTipWidget(INFO_TIPS_TYPE::ITEM_TIPS_TYPE);
		if (ItemInfoTips)
		{
			ItemInfoTips->InitInfo();
			ItemInfoTips->ShowItemInfo(info);
		}
	}
	else
	{
		ItemInfoTips->ShowItemInfo(info);
	}
}

void UTipsManager::ShowEquipTips(const UEquipInfo* info)
{
	if (!IsValid(EquipInfoTips))
	{
		EquipInfoTips = CreateTipWidget(INFO_TIPS_TYPE::EQUIP_TIPS_TYPE);
		if (EquipInfoTips)
		{
			EquipInfoTips->InitInfo();
			EquipInfoTips->ShowEquipInfo(info);
		}
	}
	else
	{
		EquipInfoTips->ShowEquipInfo(info);
	}
}

void UTipsManager::ShowSkillTips(const USkillInfo* info)
{
	if (!IsValid(SkillInfoTips))
	{
		SkillInfoTips = CreateTipWidget(INFO_TIPS_TYPE::SKILL_TIPS_TYPE);
		if (SkillInfoTips)
		{
			SkillInfoTips->InitInfo();
			SkillInfoTips->ShowSkillInfo(info);
		}
	}
	else
	{
		SkillInfoTips->ShowSkillInfo(info);
	}
}

void UTipsManager::ShowBuffTips(const UBuffInfo* info)
{
	if (!IsValid(BuffInfoTips))
	{
		BuffInfoTips = CreateTipWidget(INFO_TIPS_TYPE::BUFF_TIPS_TYPE);
		if (BuffInfoTips)
		{
			BuffInfoTips->InitInfo();
			BuffInfoTips->ShowBuffInfo(info);
		}
	}
	else
	{
		BuffInfoTips->ShowBuffInfo(info);
	}
}

void UTipsManager::ShowGoodsTips(const UGoodsInfo* info)
{
	if (!IsValid(GoodsInfoTips))
	{
		GoodsInfoTips = CreateTipWidget(INFO_TIPS_TYPE::GOODS_TIPS_TYPE);
		if (GoodsInfoTips)
		{
			GoodsInfoTips->InitInfo();
			GoodsInfoTips->ShowGoodsInfo(info);
		}
	}
	else
	{
		GoodsInfoTips->ShowGoodsInfo(info);
	}
}

void UTipsManager::ShowBlueprintTips(const UBlueprintInfo* info)
{
	if (!IsValid(BlueprintInfoTips))
	{
		BlueprintInfoTips = CreateTipWidget(INFO_TIPS_TYPE::BLUEPRINT_TIPS_TYPE);
		if (BlueprintInfoTips)
		{
			BlueprintInfoTips->InitInfo();
			BlueprintInfoTips->ShowBlueprintInfo(info);
		}
	}
	else
	{
		BlueprintInfoTips->ShowBlueprintInfo(info);
	}
}

void UTipsManager::ShowEquipPartTips(const UEquipPartInfo* info)
{
	if (!IsValid(EquipPartInfoTips))
	{
		EquipPartInfoTips = CreateTipWidget(INFO_TIPS_TYPE::EQUIPPART_TIPS_TYPE);
		if (EquipPartInfoTips)
		{
			EquipPartInfoTips->InitInfo();
			EquipPartInfoTips->ShowEquipPartInfo(info);
		}
	}
	else
	{
		EquipPartInfoTips->ShowEquipPartInfo(info);
	}
}

UCS3TipsInfoWidget* UTipsManager::CreateTipWidget(INFO_TIPS_TYPE TipsType)
{
	FString StrClass;
	switch (TipsType)
	{
	case INFO_TIPS_TYPE::TOOL_TIPS_TYPE://普通信息提示
	{
		StrClass = TEXT("BP_ToolTipWidget");
		break;
	}
	case INFO_TIPS_TYPE::ITEM_TIPS_TYPE://物品信息提示
	{
		StrClass = TEXT("BP_ItemTipWidget");
		break;
	}
	case INFO_TIPS_TYPE::EQUIP_TIPS_TYPE://装备信息提示
	{
		StrClass = TEXT("BP_EquipTipWidget");
		break;
	}
	case INFO_TIPS_TYPE::SKILL_TIPS_TYPE://技能信息提示
	{
		StrClass = TEXT("BP_SkillTipWidget");
		break;
	}
	case INFO_TIPS_TYPE::BUFF_TIPS_TYPE://Buff信息提示
	{
		StrClass = TEXT("BP_BuffTipsWidget");
		break;
	}
	case INFO_TIPS_TYPE::GOODS_TIPS_TYPE://商品信息提示
	{
		StrClass = TEXT("BP_GoodsTipsWidget");
		break;
	}
	case INFO_TIPS_TYPE::BLUEPRINT_TIPS_TYPE://图纸信息提示
	{
		StrClass = TEXT("BP_BlueprintTipsWidget");
		break;
	}
	case INFO_TIPS_TYPE::EQUIPPART_TIPS_TYPE://半成品装备信息提示
	{
		StrClass = TEXT("BP_EquipPartTipWidget");
		break;
	}
	default:
		break;
	}
	if (StrClass != TEXT(""))
	{
		ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
		if (PlayerController)
		{
			return CreateWidget<UCS3TipsInfoWidget>(PlayerController, UGolbalBPFunctionLibrary::GetUClassByStr(StrClass));
		}
		else
		{
			return nullptr;
		}
	}
	else
	{
		return nullptr;
	}
}

void UToolInfo::InitFormatInfoTips(const FString& InfoKeys)
{
	InfoTips = InfoKeys;
}

void UItemInfo::InitFormatInfoTips(const FString& InfoKeys)
{
	ItemUId = InfoKeys;
	URoleKitBagInterface* kitbaginterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface")));
	if (!IsValid(kitbaginterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UItemInfo::InitFormatInfoTips : kitbaginterface!"));
		return;
	}
	UItemBase* ItemBase = kitbaginterface->FindItemByUID(ItemUId);
	//判断是否宝箱中的物品
	if (!IsValid(ItemBase))
	{
		URoleDropBoxInterface* dropboxinterface = Cast<URoleDropBoxInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleDropBoxInterface")));
		if (IsValid(dropboxinterface))
		{
			ItemBase = dropboxinterface->FindBoxItemByUID(ItemUId);
		}
	}
	//不在背包和宝箱，则通过ItemID获取物品实例
	if (!IsValid(ItemBase))
	{
		UItemFactory* ItemFactory = UUECS3GameInstance::Instance->ItemFactory;
		if (!IsValid(ItemFactory))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UItemInfo::InitFormatInfoTips : ItemFactory!"));
			return;
		}
		UItemBase* StaticItem = ItemFactory->GetItemByID(FSTRING_TO_INT(ItemUId));//此处ItemUId是ItemID
		if (!IsValid(StaticItem))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UItemInfo::InitFormatInfoTips : StaticItem!"));
			return;
		}
		ItemBase = StaticItem;
	}
	SetItemInfo(ItemBase);
}

void UItemInfo::SetItemInfo(UItemBase* ItemBase)
{
	if (!IsValid(ItemBase))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UItemInfo::SetItemInfo : ItemBase!"));
		return;
	}
	ItemQuality = ItemBase->Quality;
	InfoTips = ItemBase->GetDescribeStr();
	ItemNameInfo = ItemBase->GetItemName();
	ItemIcon = ItemBase->Icon;
	//30012玲珑玉令
	if (ItemBase->CheckItemType(30012))
	{
		IsShowItemLevel = true;
		UItemJadeCommond* ItemJade = Cast<UItemJadeCommond>(ItemBase);
		if (IsValid(ItemJade))
		{
			ItemLevel = ItemJade->jadeLevel;
			if (ItemJade->isValid == 0)
			{
				IsItemValid = false;
			}
			else
			{
				IsItemValid = true;
			}
		}
		else
		{
			ItemLevel = ItemBase->Level;
			IsItemValid = true;
		}
	}
	else
	{
		IsShowItemLevel = false;
		ItemLevel = ItemBase->Level;
		IsItemValid = true;
	}
	ItemRepLevel = ItemBase->ReqLevel;
	ReqJingJieLevel = ItemBase->ReqJingJieLevel;
	ItemType = ItemBase->GetTypeStr();
	Profession = ItemBase->GetReqClasses();
	ItemIsBinded = ItemBase->IsBinded();
	Amount = ItemBase->Amount;
	Price = ItemBase->Price;
	ItemUseNumberInfo = ItemBase->GetUseNumberStr();
	ItemUseAmountInfo = ItemBase->GetUseAmountStr();
	ItemUseEndTimeInfo = ItemBase->ItemEndTime;

}

void UEquipInfo::InitFormatInfoTips(const FString& InfoKeys)
{
	EquipUId = InfoKeys;
	URoleKitBagInterface* kitbaginterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface")));
	if (!IsValid(kitbaginterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UEquipInfo::InitFormatInfoTips : kitbaginterface!"));
		return;
	}
	EquipTipsData = GetEquipTipsDataByUId(EquipUId);
	PlayerEquipUIds = kitbaginterface->GetSamePartEquipUIds(EquipUId);
	EquipPropertyCompare = TEXT("");
}

FEquipTipsData UEquipInfo::GetEquipTipsDataByUId(const FString& UId)
{
	FEquipTipsData TempEquipTipsData;
	URoleKitBagInterface* kitbaginterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface")));
	if (!IsValid(kitbaginterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UEquipInfo::GetEquipTipsDataByUId : kitbaginterface!"));
		return TempEquipTipsData;
	}
	UEquip* Equip = Cast<UEquip>(kitbaginterface->FindItemByUID(UId));

	//判断是否是宝箱中的物品
	if (!IsValid(Equip))
	{
		URoleDropBoxInterface* dropboxinterface = Cast<URoleDropBoxInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleDropBoxInterface")));
		if (IsValid(dropboxinterface))
		{
			Equip = Cast<UEquip>(dropboxinterface->FindBoxItemByUID(UId));
		}
	}
	
	//背包或者宝箱找不到装备，通过ItemID获取物品实例
	if (!IsValid(Equip))
	{
		UItemFactory* ItemFactory  = UUECS3GameInstance::Instance->ItemFactory;
		if (!IsValid(ItemFactory))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UEquipInfo::GetEquipTipsDataByUId : ItemFactory!"));
			return TempEquipTipsData;
		}
		UEquip* StaticEquip = Cast<UEquip>(ItemFactory->GetItemByID(FSTRING_TO_INT(UId)));
		if (!IsValid(StaticEquip))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UEquipInfo::GetEquipTipsDataByUId : StaticEquip!"));
			return TempEquipTipsData;
		}
		Equip = StaticEquip;
	}
	TempEquipTipsData = GetEquipTipsData(Equip);
	
	return TempEquipTipsData;
}

FEquipTipsData UEquipInfo::GetEquipTipsData(UItemBase* Equip)
{
	FEquipTipsData tempEquipTipsData;
	if (!IsValid(Equip))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UEquipInfo::GetEquipTipsData : Equip!"));
		return tempEquipTipsData;
	}
	UEquip* tempEquip = Cast<UEquip>(Equip);
	if (!IsValid(tempEquip)) return tempEquipTipsData;
	tempEquipTipsData.Name = tempEquip->GetItemName();
	tempEquipTipsData.Quality = tempEquip->Quality;
	tempEquipTipsData.Icon = tempEquip->Icon;
	tempEquipTipsData.RepLevel = tempEquip->ReqLevel;
	tempEquipTipsData.ReqJingJieLevel = tempEquip->ReqJingJieLevel;
	tempEquipTipsData.Hardiness = tempEquip->GetHardinessStr();
	tempEquipTipsData.Profession = tempEquip->GetReqClasses();
	tempEquipTipsData.PartType = tempEquip->GetModelPartType();
	tempEquipTipsData.bIsBinded = tempEquip->IsBinded();
	tempEquipTipsData.Amount = tempEquip->Amount;
	tempEquipTipsData.CombatPower = INT_TO_FSTRING(tempEquip->CombatPower);
	tempEquipTipsData.StarText = tempEquip->GetStarDescribe();
	tempEquipTipsData.BaseProperty = tempEquip->GetAttackPropertyStr();
	tempEquipTipsData.BaseAttachProperty = tempEquip->GetAttachPropertyStr();
	tempEquipTipsData.IntensifyProperty = tempEquip->GetIntensifySumPropertyStr();
	tempEquipTipsData.SuitProperty = TEXT("");
	tempEquipTipsData.Price = tempEquip->Price;
	tempEquipTipsData.DescribeStr = tempEquip->Describe;

	return tempEquipTipsData;
}

void USkillInfo::InitFormatInfoTips(const FString& InfoKeys)
{
	SkillID = FSTRING_TO_INT(InfoKeys);
}

void UBuffInfo::InitFormatInfoTips(const FString& InfoKeys)
{
	TArray<FString> SplitArray = UGolbalBPFunctionLibrary::SplitString(InfoKeys, false, "|");
	if (SplitArray.Num() < 2)
	{
		return;
	}
	int32 EntityID = FSTRING_TO_INT(SplitArray[0]);
	BuffIndex = FSTRING_TO_INT(SplitArray[1]);
	if (!IsValid(UUECS3GameInstance::Instance) || !IsValid(UUECS3GameInstance::Instance->BuffManager))
	{
		return;
	}
	USkillInterface* SkillInterface = Cast<USkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(USkillInterface::GetName(), EntityID));
	if (IsValid(SkillInterface))
	{
		TMap<int32, BuffDataType> BuffDatas = SkillInterface->getAttrBuffs();
		if (BuffDatas.Contains(BuffIndex))
		{
			BuffID = BuffDatas[BuffIndex].buffID;
			UTimeManager *TimeManager = UUECS3GameInstance::Instance->TimeManager;
			int64 currTime = TimeManager->GetMultipleClientTime();
			BuffTipsData.RemainTime = (BuffDatas[BuffIndex].endTime - currTime) / (float)TIME_ENLARGE_MULTIPLE;
		}
		else
		{
			BuffID = FSTRING_TO_INT(InfoKeys);
		}
	}
	else
	{
		BuffID = FSTRING_TO_INT(InfoKeys);
	}
	
	UBuffManager* BuffManager = UUECS3GameInstance::Instance->BuffManager;
	if (!IsValid(BuffManager))
	{
		return;
	}
	const FBUFF_TABLE_DATA* TableData = BuffManager->GetBuffDataByBuffID(BuffID);
	if (TableData)
	{
		BuffTipsData.BuffID = BuffID;
		BuffTipsData.BuffName = TableData->BuffName;
		BuffTipsData.BuffIcon = TableData->BuffIcon;
		BuffTipsData.BuffLevel = TableData->BuffLevel;
		BuffTipsData.HoldTime = TableData->HoldTime;
		BuffTipsData.TargetActForbidDescribe = BuffManager->GetTargetActForbidDescribe(BuffID);
		BuffTipsData.DescribeStr = TableData->Description;
	}
}

void UGoodsInfo::InitFormatInfoTips(const FString& InfoKeys)
{
	GoodsID = InfoKeys;
}

void UBlueprintInfo::InitFormatInfoTips(const FString& InfoKeys)
{
	BlueprintUId = InfoKeys;
	URoleKitBagInterface* kitbaginterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface")));
	if (!IsValid(kitbaginterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBlueprintInfo::InitFormatInfoTips : kitbaginterface!"));
		return;
	}
	UItemComposeEquipBP* LocalBlueprintData = Cast<UItemComposeEquipBP>(kitbaginterface->FindItemByUID(BlueprintUId));
	if (!IsValid(LocalBlueprintData))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBlueprintInfo::InitFormatInfoTips : UItemComposeEquipBP!"));
		return;
	}
	int32 EquipID = LocalBlueprintData->GetComposeEquipID();
	UItemFactory* ItemFactory = UUECS3GameInstance::Instance->ItemFactory;
	if (!IsValid(ItemFactory))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBlueprintInfo::InitFormatInfoTips : ItemFactory!"));
		return;
	}
	UEquip* StaticEquip = Cast<UEquip>(ItemFactory->GetItemByID(EquipID));
	if (!IsValid(StaticEquip))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBlueprintInfo::InitFormatInfoTips : StaticEquip!"));
		return;
	}
	FString BlueprintName;
	FString ComposeEquipName;
	GetNameData(LocalBlueprintData->suitIndex, LocalBlueprintData->ItemName, LocalBlueprintData->Quality, StaticEquip->ItemName, BlueprintName, ComposeEquipName);

	BlueprintTipsData.Name = BlueprintName;
	BlueprintTipsData.SuitIndex = LocalBlueprintData->suitIndex;
	BlueprintTipsData.EquipName = ComposeEquipName;
	BlueprintTipsData.Quality = LocalBlueprintData->Quality;
	BlueprintTipsData.RepLevel = LocalBlueprintData->ReqLevel;
	BlueprintTipsData.ReqJingJieLevel = LocalBlueprintData->ReqJingJieLevel;
	BlueprintTipsData.Profession = LocalBlueprintData->GetReqClasses();
	BlueprintTipsData.PartType = StaticEquip->GetModelPartType();
	BlueprintTipsData.bIsBinded = LocalBlueprintData->IsBinded();
	BlueprintTipsData.Amount = LocalBlueprintData->Amount;
	BlueprintTipsData.BaseProperty = LocalBlueprintData->GetAttackPropertyStr();
	BlueprintTipsData.SuitBaseProperty = TEXT("");//没数据
	BlueprintTipsData.SuitAttachProperty = TEXT("");//没数据
	BlueprintTipsData.Material = GetMaterial(LocalBlueprintData->suitIndex, EquipID);
	BlueprintTipsData.SuccessRate = LocalBlueprintData->successRate;
	BlueprintTipsData.AddRate = LocalBlueprintData->addRate;
	BlueprintTipsData.DescribeStr = LocalBlueprintData->Describe;
}

void UBlueprintInfo::GetNameData(int32 SuitIndex, FString ItemName, int32 Quality, FString EquipName, FString& BlueprintName, FString& ComposeEquipName)
{
	//根据suitIndex读表
	FName Row = FSTRING_TO_FNAME(INT_TO_FSTRING(SuitIndex));
	const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_WORKSHOP_SUITNAME_DATA);
	FSuitNameCfg* data = const_cast<FSuitNameCfg*>(table->GetRow<FSuitNameCfg>(Row));
	if (data == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBlueprintInfo::GetSuitNameCfgData : data!"));
		BlueprintName = ItemName;
		ComposeEquipName = EquipName;
		return;
	}
	BlueprintName = GetItemName(data->suitTitle, ItemName, Quality);
	ComposeEquipName = GetEquipName(data->suitName, EquipName);
}

FString UBlueprintInfo::GetItemName(FString SuitTitle, FString ItemName, int32 Quality)
{
	if (!ItemName.Equals(TEXT("")))
	{
		FString EquipName = ItemName;
		if (!SuitTitle.Equals(TEXT("")))
		{
			EquipName = ItemName + TEXT("(") + SuitTitle + TEXT(")");
		}
		FLinearColor linearColor = UGolbalBPFunctionLibrary::GetItemNameColorByQuality(Quality);
		FString ColorStr = UGolbalBPFunctionLibrary::ConvertLinearColorToHex(linearColor);
		return StrToColorStr(EquipName, ColorStr, ColorStr, TEXT("[0,0]"));
	}
	else
	{
		return StrToColorStr(TEXT(""), TEXT("FFFFFFFF"), TEXT("FFFFFFFF"), TEXT("[0,0]"));
	}
}

FString UBlueprintInfo::StrToColorStr(const FString& inputstr, const FString& colorstr, const FString& shadowcolor, const FString& shadowoffset)
{
	if (inputstr.Equals(TEXT("")))
	{
		return inputstr;
	}
	return FString::Printf(TEXT("<text color=\"#%s\" shadowColor=\"#%s\" shadowOffset=\"#%s\">%s</text>"), *colorstr, *shadowcolor, *shadowoffset, *inputstr);
}

FString UBlueprintInfo::GetEquipName(FString SuitName, FString EquipName)
{
	if (SuitName.Equals((TEXT(""))))
	{
		return EquipName;
	}
	return SuitName + TEXT(" ") + EquipName;
}

FString UBlueprintInfo::GetMaterial(int32 SuitIndex, int32 EquipID)
{
	URoleWorkShopInterface* WorkShopInterface = Cast<URoleWorkShopInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleWorkShopInterface")));
	if (!IsValid(WorkShopInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBlueprintInfo::GetMaterial : WorkShopInterface!"));
		return TEXT("");
	}
	if (!WorkShopInterface->GEquipComposeCost.Contains(EquipID))
	{
		return TEXT("");
	}
	FGreenEquipComposeCost* EquipComposeCost = WorkShopInterface->GEquipComposeCost.Find(EquipID);
	//主材料
	FCS3ItemData mainMaterialItem = UItemFactory::GetStaticDataByItemID(EquipComposeCost->mainMaterial[SuitIndex]);
	FString MaterialStr = mainMaterialItem.ItemName + TEXT("*") + INT_TO_FSTRING(EquipComposeCost->mainMaterialNum);

	TMap<int32, int32> material = EquipComposeCost->material;
	//获取所有材料ItemID
	TArray<int32> MapKeys;
	material.GetKeys(MapKeys);
	TArray<int32> NewKeys;
	//排序
	WorkShopInterface->SortItemIDs(MapKeys, NewKeys);
	for (auto Key : NewKeys)
	{
		FCS3ItemData MaterialItem = UItemFactory::GetStaticDataByItemID(Key);
		int32 ItemAmount = *(material.Find(Key));
		MaterialStr = MaterialStr + TEXT("  ") + MaterialItem.ItemName + TEXT("*") + INT_TO_FSTRING(ItemAmount);
	}
	return MaterialStr;
}

void UEquipPartInfo::InitFormatInfoTips(const FString& InfoKeys)
{
	EquipPartUId = InfoKeys;
	URoleKitBagInterface* kitbaginterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface")));
	if (!IsValid(kitbaginterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBlueprintInfo::InitFormatInfoTips : kitbaginterface!"));
		return;
	}
	UEquipPart* EquipPart = Cast<UEquipPart>(kitbaginterface->FindItemByUID(EquipPartUId));
	if (!IsValid(EquipPart))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UBlueprintInfo::InitFormatInfoTips : EquipPart!"));
		return;
	}
	EquipPartTipsData.Name = EquipPart->GetItemName();
	EquipPartTipsData.QuenchingNum = EquipPart->quenchingNum;
	EquipPartTipsData.Quality = EquipPart->Quality;
	EquipPartTipsData.Icon = EquipPart->Icon;
	EquipPartTipsData.Level = EquipPart->Level;
	EquipPartTipsData.RepLevel = EquipPart->ReqLevel;
	EquipPartTipsData.ReqJingJieLevel = EquipPart->ReqJingJieLevel;
	EquipPartTipsData.Profession = EquipPart->GetReqClasses();
	EquipPartTipsData.PartType = EquipPart->GetModelPartType();
	EquipPartTipsData.bIsBinded = EquipPart->IsBinded();
	EquipPartTipsData.Amount = EquipPart->Amount;
	EquipPartTipsData.BaseProperty = EquipPart->GetAttackPropertyStr();
	EquipPartTipsData.BaseAttachProperty = EquipPart->GetAttachPropertyStr();
	EquipPartTipsData.SuitProperty = TEXT("");
	EquipPartTipsData.Price = EquipPart->Price;
	EquipPartTipsData.DescribeStr = EquipPart->Describe;
}

CONTROL_COMPILE_OPTIMIZE_END