// Fill out your copyright notice in the Description page of Project Settings.
#include "GameData/Item/ItemBase.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameData/Item/ItemEnum.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameData/Item/ItemType.h"
#include "Util/CS3Debug.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "Interface/StatusMessageInterface.h"
#include "GameData/Item/Equip.h"
#include "Manager/LocalDataSaveManager.h"
#include "Actor/ServerCharacter.h"
#include "Manager/CfgManager.h"
#include "../EnumCsvDefine.h"

void UItemBase::InitDynamicDataForJson(FString jsonStr)
{
}

void UItemBase::OnRep_Amount()
{
	//更新背包中物品数量
	UpdateBagGrid();
	UpdateQuickBar();
	OnItemInfoChange.Broadcast(UID, ItemOrder);
}

void UItemBase::OnRep_BindType()
{
	//更新背包物品的绑定
	UpdateBagGrid();
	OnItemInfoChange.Broadcast(UID, ItemOrder);
}

void UItemBase::UpdateBagGrid()
{	
	UCS3EntityInterface* BInterface = UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0);
	if (IsValid(BInterface))
	{
		URoleKitBagInterface* kitbaginterface = Cast<URoleKitBagInterface>(BInterface);
		//不是背包中的物品，不处理
		if (!IsValid(kitbaginterface) || !IsValid(kitbaginterface->FindItemByUID(UID)))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UItemBase::UpdateBagGrid : kitbaginterface->FindItemByUID(UID)!"));
			return;
		}

		//只有背包中的物品才更新界面，避免受客户端其它物品更新的影响
		kitbaginterface->UpdateGrid(UID, ItemOrder);
	}
}

void UItemBase::UpdateQuickBar()
{
	UCS3EntityInterface* BInterface = UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0);
	if (IsValid(BInterface))
	{
		URoleKitBagInterface* kitbaginterface = Cast<URoleKitBagInterface>(BInterface);
		kitbaginterface->UpdateQBItemAmount(ItemID);
	}
}

UItemBase* UItemBase::InitData(const FString& uidstr, int32 num, int32 isbinded, int32 order)
{
	UID = uidstr;
	Amount = num;
	BindType = isbinded;
	ItemOrder = order;
	return this;
}

bool UItemBase::IsShowNew()
{
	if (IsValid(UUECS3GameInstance::Instance->LocalDataSaveManager->LocalKitbagData))
	{
		return UUECS3GameInstance::Instance->LocalDataSaveManager->LocalKitbagData->IsShowNewTip(UID);
	}
	return false;
}

void UItemBase::RecordOpertation()
{
	if (IsShowNew())
	{
		UUECS3GameInstance::Instance->LocalDataSaveManager->LocalKitbagData->SaveNewTip(UID, false);
	}
}

bool UItemBase::IsCanUse()
{
	return true;
}

bool UItemBase::IsEquip()
{
	return false;
}

bool UItemBase::CheckReqClass(AServerCharacter* character)
{
	int32 entityid = character->EntityId;
	KBEngine::Entity *entity = UGolbalBPFunctionLibrary::FindEntity(entityid);
	if (entity)
	{
		int32 profession = UGolbalBPFunctionLibrary::GetIntPropertyValue(entity->ID(), TEXT("profession"));
		if (ReqClasses != TEXT(""))
		{
			TArray<FString> result = UGolbalBPFunctionLibrary::SplitString(ReqClasses, false, TEXT("|"));
			return result.Contains(FString::FromInt(profession));
		}
		else
		{
			return true;
		}
	}
	return false;
}

bool UItemBase::CheckLevel(AServerCharacter* character)
{
	int32 entityid = character->EntityId;
	KBEngine::Entity *entity = UGolbalBPFunctionLibrary::FindEntity(entityid);
	if (entity)
	{
		int32 level = UGolbalBPFunctionLibrary::GetIntPropertyValue(entity->ID(), TEXT("level"));
		if (level >= ReqLevel)
		{
			return true;
		}
	}
	return false;
}

bool UItemBase::CheckJingjieLevel(AServerCharacter* character)
{
	int32 entityid = character->EntityId;
	KBEngine::Entity *entity = UGolbalBPFunctionLibrary::FindEntity(entityid);
	if (entity)
	{
		int32 JingJieLevel = UGolbalBPFunctionLibrary::GetIntPropertyValue(entity->ID(), TEXT("jingjieLevel"));
		if (JingJieLevel >= ReqJingJieLevel)
		{
			return true;
		}
	}
	return false;
}

bool UItemBase::IsCanStack(int32 num)
{
	if (OverlyingType == 1)
	{
		return (Amount + num <= OverlyingMax);
	}
	return false;
}

bool UItemBase::CheckItemType(int32 _type)
{
	return ItemType == _type;
}

bool UItemBase::IsWhite()
{
	return Quality == int(QUALITY::QUALITY_WHITE);
}

bool UItemBase::IsBlue()
{
	return Quality == int(QUALITY::QUALITY_BLUE);
}

bool UItemBase::IsGold()
{
	return Quality == int(QUALITY::QUALITY_GOLD);
}

bool UItemBase::IsPink()
{
	return Quality == int(QUALITY::QUALITY_PINK);
}

bool UItemBase::IsGreen()
{
	return Quality >= int(QUALITY::QUALITY_GREEN);
}

bool UItemBase::IsGreenDi()
{
	return Quality == int(QUALITY::QUALITY_GREEN);
}

bool UItemBase::IsGreenTian()
{
	return Quality == int(QUALITY::QUALITY_GREEN_TIAN);
}

bool UItemBase::IsGreenSheng()
{
	return Quality == int(QUALITY::QUALITY_GREEN_SHENG);
}

bool UItemBase::IsCanSell()
{
	return CanSell == 1;
}

bool UItemBase::IsCanDestory()
{
	return CanDestroy == 1;
}


bool UItemBase::IsCanDragToQB()
{
	const UConfigTable* ItemTypeTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(
		CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ITEMTYPEINFO);
	const FItemTypeInfo* itemtype = ItemTypeTable->GetRow<FItemTypeInfo>(FString::FromInt(ItemType));
	if (itemtype)
	{
		return itemtype->CanDragToQB == 1;
	}
	return false;
}

bool UItemBase::IsNonDestructive()
{
	return ((CanSell == 0) && (CanDestroy == 0));
}

bool UItemBase::IsUnique()
{
	return MaxTakeAmount == 1;
}

bool UItemBase::HasLimitTakeAmount()
{
	return MaxTakeAmount != 999999;
}

bool UItemBase::IsBinded()
{
	if (BindType == int(EBINDTYPE::BIND_NONE))
	{
		return false;
	}
	else
	{
		return true;
	}
}

bool UItemBase::isQuest()
{
	return ItemType == 30001;
}

bool UItemBase::isSpar()
{
	return ItemType == 20008;
}

FString UItemBase::GetItemName()
{
	if (ItemName != TEXT(""))
	{
		FLinearColor linearColor = UGolbalBPFunctionLibrary::GetItemNameColorByQuality(Quality);
		FString ColorStr = UGolbalBPFunctionLibrary::ConvertLinearColorToHex(linearColor);
	/**
		switch (Quality)
		{
		case int(QUALITY::QUALITY_WHITE)://白色
		{
			ColorStr = TEXT("FFFFFFFF");
		}
		break;
		case int(QUALITY::QUALITY_BLUE)://蓝色
		{
			ColorStr = TEXT("33CCFFFF");
		}
		break;
		case int(QUALITY::QUALITY_GOLD)://金色
		{
			ColorStr = TEXT("FFE036FF");
		}
		break;
		case int(QUALITY::QUALITY_PINK)://粉色
		{
			ColorStr = TEXT("FF8080FF");
		}
		break;
		case int(QUALITY::QUALITY_GREEN)://地阶绿色
		case int(QUALITY::QUALITY_GREEN_TIAN)://天阶绿色
		case int(QUALITY::QUALITY_GREEN_SHENG)://圣阶绿色
		{
			ColorStr = TEXT("63FF9EFF");
		}
		break;
		default:ColorStr = TEXT("FFFFFFFF");
			break;
		}
	*/
		return StrToColorStr(ItemName, ColorStr, ColorStr, TEXT("[0,0]"));
	}
	else
	{
		return StrToColorStr(TEXT(""), TEXT("FFFFFFFF"), TEXT("FFFFFFFF"), TEXT("[0,0]"));
	}
}

FString UItemBase::GetTypeStr()
{
	const UConfigTable* ItemTypeTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ITEMTYPEINFO);
	const FItemTypeInfo* itemtype = ItemTypeTable->GetRow<FItemTypeInfo>(FString::FromInt(ItemType));
	if (itemtype)
	{
		return itemtype->ItemType;
	}
	return TEXT("");
}

FString UItemBase::GetPrice()
{
	return UGolbalBPFunctionLibrary::GetRichTextMoney((int64)Price,TEXT("FFFFFFFF"));
}

FString UItemBase::GetPriceStr()
{
	return GetPrice();
}

FString UItemBase::GetLevelStr()
{
	FString level = UGolbalBPFunctionLibrary::GetChinese(TEXT("LEVEL"));
	return StrToColorStr(level + FString::FromInt(Level), TEXT("FFFFFFFF"), TEXT("FFFFFFFF"), TEXT("[0,0]"));
}

FString UItemBase::GetDescribeStr()
{
	if (Describe != TEXT("")) 
	{
		if (Describe.Contains("|"))
		{
			TArray<FString> DescribeList;
			FString describe = TEXT("");
			FString left,right;
			bool IsFind;
			Describe.ParseIntoArray(DescribeList, TEXT("|"), true);
			for (auto item: DescribeList) 
			{
				describe += StrToColorStr(item, TEXT("CCA097FF"), TEXT("0000007F"), TEXT("[0,0]"));
			}
			IsFind = describe.Split(TEXT("<br/>"), &left, &right, ESearchCase::CaseSensitive, ESearchDir::FromEnd);
			if (IsFind)
			{
				describe = left;
			}
			return describe;
		}
		else 
		{
			return StrToColorStrWithoutBr(Describe, TEXT("CCA097FF"), TEXT("0000007F"), TEXT("[0,0]"));
		}
	}
	else
	{
		FString describe = UGolbalBPFunctionLibrary::GetChinese(TEXT("DESCRIBE_NONE"));
		return StrToColorStrWithoutBr(describe, TEXT("CCA097FF"), TEXT("0000007F"), TEXT("[0,0]"));
	}
}


FString UItemBase::GetTakeStr()
{
	FString takestr = TEXT("");
	//唯一
	if (IsUnique())
	{
		takestr += UGolbalBPFunctionLibrary::GetChinese(TEXT("UNIQUEITEM"));
	}
	else
	{
		//携带上限
		if (HasLimitTakeAmount())
		{
			//takestr = (UGolbalBPFunctionLibrary::GetChinese(TEXT("MAXTAKEAMOUNT"))).Replace(TEXT("%d"), *INT_TO_FSTRING(MaxTakeAmount));
			takestr = UStatusMessageInterface::GetReplaceMessage(UGolbalBPFunctionLibrary::GetChinese(TEXT("MAXTAKEAMOUNT1")), INT_TO_FSTRING(MaxTakeAmount), TEXT(","));
		}
	}
	if (takestr != TEXT(""))
	{
		return StrToColorStr(takestr, TEXT("FFFFFFFF"), TEXT("FFFFFFFF"), TEXT("[0,0]"));
	}
	else
	{
		return takestr;
	}
}

FString UItemBase::GetUseNumberStr()
{
	FString NumberStr;
	if (OverlyingType == 0)
	{
		return NumberStr;
	}
	else if (OverlyingType == 1)
	{
		NumberStr += StrToColorStrWithoutBr(UGolbalBPFunctionLibrary::GetChinese(TEXT("STACK_AMOUNT")), TEXT("FFE036FF"), TEXT("FFE036FF"), TEXT("[0,0]"));
	}
	else if (OverlyingType == 2)
	{
		NumberStr += StrToColorStrWithoutBr(UGolbalBPFunctionLibrary::GetChinese(TEXT("AVAILABLE_AMOUNT")), TEXT("FFE036FF"), TEXT("FFE036FF"), TEXT("[0,0]"));
		if (OverlyingMax < 0)
		{
			NumberStr += FString(TEXT("无限次数"));
			return NumberStr;
		}
	}
	else if (OverlyingType == 3)
	{
		NumberStr += StrToColorStrWithoutBr(UGolbalBPFunctionLibrary::GetChinese(TEXT("EMPOWER_AMOUNT")), TEXT("FFE036FF"), TEXT("FFE036FF"), TEXT("[0,0]"));
	}
	NumberStr += INT_TO_FSTRING(Amount) + TEXT("/") + INT_TO_FSTRING(OverlyingMax);

	return NumberStr;
}

FString UItemBase::GetUseAmountStr()
{
	FString AmountStr = "";
	int32 remainNumber = -1;
	int32 refreshType = int32(ITEM_USE_AMOUTN_REFRESH_TYPE::ITEM_USE_AMOUTN_REFRESH_TYPE_FOREVER);
	UCS3EntityInterface* BInterface = UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0);
	if (IsValid(BInterface))
	{
		URoleKitBagInterface* kitbaginterface = Cast<URoleKitBagInterface>(BInterface);
		FString createTimeStr = kitbaginterface->GetItemUseCreateTimeByItemID(ItemID);
		if (UseAmount != "")
		{
			TArray<FString> result = UGolbalBPFunctionLibrary::SplitString(UseAmount, false, TEXT("|"));
			if (result.Num() < 2 || createTimeStr == "")
			{
				return "";
			}
			refreshType = FSTRING_TO_INT(result[0]);
			FDateTime createTime = UGolbalBPFunctionLibrary::FromServerStrTimeToClientTime(createTimeStr);
			if (refreshType == int32(ITEM_USE_AMOUTN_REFRESH_TYPE::ITEM_USE_AMOUTN_REFRESH_TYPE_FOREVER))
			{
				remainNumber = kitbaginterface->GetItemUseAmountByItemID(ItemID);
				AmountStr += StrToColorStrWithoutBr(UGolbalBPFunctionLibrary::GetChinese(TEXT("USE_AMOUNT_FOREVER")), TEXT("FFE036FF"), TEXT("FFE036FF"), TEXT("[0,0]"));
			}
			else if (refreshType == int32(ITEM_USE_AMOUTN_REFRESH_TYPE::ITEM_USE_AMOUTN_REFRESH_TYPE_DAY)) //每天物品使用限量
			{
				if (FDateTime::Now().GetYear() == createTime.GetYear() && FDateTime::Now().GetMonth() == createTime.GetMonth() && FDateTime::Now().GetDay() == createTime.GetDay())
				{
					remainNumber = kitbaginterface->GetItemUseAmountByItemID(ItemID);
				}
				else
				{
					remainNumber = FSTRING_TO_INT(result[1]);
				}
				AmountStr += StrToColorStrWithoutBr(UGolbalBPFunctionLibrary::GetChinese(TEXT("USE_AMOUNT_DAY")), TEXT("FFE036FF"), TEXT("FFE036FF"), TEXT("[0,0]"));
			}
			else if (refreshType == int32(ITEM_USE_AMOUTN_REFRESH_TYPE::ITEM_USE_AMOUTN_REFRESH_TYPE_WEEK))//每周物品使用限量
			{
				if (FDateTime::Now().GetYear() == createTime.GetYear() && FDateTime::Now().GetMonth() == createTime.GetMonth())
				{
					FDateTime nextWeek = createTime + (7 - int(createTime.GetDayOfWeek()));
					if (nextWeek > FDateTime::Now())
					{
						remainNumber = FSTRING_TO_INT(result[1]);
					}
					else
					{
						remainNumber = kitbaginterface->GetItemUseAmountByItemID(ItemID);
					}
				}
				else
				{
					remainNumber = kitbaginterface->GetItemUseAmountByItemID(ItemID);
				}
				AmountStr += StrToColorStrWithoutBr(UGolbalBPFunctionLibrary::GetChinese(TEXT("USE_AMOUNT_WEEK")), TEXT("FFE036FF"), TEXT("FFE036FF"), TEXT("[0,0]"));
			}
			else if (refreshType == int32(ITEM_USE_AMOUTN_REFRESH_TYPE::ITEM_USE_AMOUTN_REFRESH_TYPE_MONTH)) //每月物品使用限量
			{
				if (FDateTime::Now().GetYear() == createTime.GetYear() && FDateTime::Now().GetMonth() == createTime.GetMonth())
				{
					remainNumber = kitbaginterface->GetItemUseAmountByItemID(ItemID);
				}
				else
				{
					remainNumber = FSTRING_TO_INT(result[1]);
				}
				AmountStr += StrToColorStrWithoutBr(UGolbalBPFunctionLibrary::GetChinese(TEXT("USE_AMOUNT_MONTH")), TEXT("FFE036FF"), TEXT("FFE036FF"), TEXT("[0,0]"));
			}
			AmountStr += StrToColorStrWithoutBr((result[1] + UGolbalBPFunctionLibrary::GetChinese(TEXT("NUMBER")) + TEXT("&nbsp;")), TEXT("FFFFFFFF"), TEXT("FFFFFFFF"), TEXT("[0,0]"));
			AmountStr += StrToColorStrWithoutBr(UGolbalBPFunctionLibrary::GetChinese(TEXT("USE_REMAIN")), TEXT("FFE036FF"), TEXT("FFE036FF"), TEXT("[0,0]"));
			AmountStr += StrToColorStrWithoutBr(((FString::FromInt(remainNumber) ) + UGolbalBPFunctionLibrary::GetChinese(TEXT("NUMBER"))), TEXT("FFFFFFFF"), TEXT("FFFFFFFF"), TEXT("[0,0]"));
		}
	}
	return AmountStr;
}

FString UItemBase::StrToColorStr(const FString& inputstr, const FString& colorstr, const FString& shadowcolor, const FString& shadowoffset)
{
	if (inputstr == TEXT(""))
	{
		return inputstr;
	}
	return FString::Printf(TEXT("<text color=\"#%s\" shadowColor=\"#%s\" shadowOffset=\"#%s\">%s</text><br/>"), *colorstr, *shadowcolor, *shadowoffset, *inputstr);
}

FString UItemBase::StrToColorStrWithoutBr(const FString& inputstr, const FString& colorstr, const FString& shadowcolor, const FString& shadowoffset)
{
	if (inputstr == TEXT(""))
	{
		return inputstr;
	}
	return FString::Printf(TEXT("<text color=\"#%s\" shadowColor=\"#%s\" shadowOffset=\"#%s\">%s</text>"), *colorstr, *shadowcolor, *shadowoffset, *inputstr);
}

TArray<int32> UItemBase::GetReqClasses()
{

	TArray<FString> temp;
	TArray<int32> result;
	if (ReqClasses == TEXT(""))
	{
		result.Add(1);
		result.Add(2);
		result.Add(3);
		result.Add(4);
		return result;
	}
	temp = UGolbalBPFunctionLibrary::SplitString(ReqClasses, false, TEXT("|"));
	if (temp.Num() > 0)
	{
		for (auto item : temp)
		{
			if(item != TEXT(""))
			{
				result.Add(FSTRING_TO_INT(item));
			}
		}
	}
	return result;
}


void UItemBase::SetDynamicProperty(const int32& combatPowner, const FString& attackStr, const FString& attachStr, const FString& intensifyStr, const int32& hardiness)
{
	
}

bool UItemBase::IsMatchClasses(TArray<int32> professions)
{
	TSet<int32> s1;
	TSet<int32> s2;
	TSet<int32> temp;
	s1.Append(professions);
	s2.Append(GetReqClasses());
	return IsMatch(s1, s2);
}

bool UItemBase::IsMatchEquipParts(TArray<int32> modelparts)
{
	TSet<int32> s1;
	TSet<int32> s2;
	s1.Append(modelparts);
	if (IsEquip())
	{
		UEquip* equip = Cast<UEquip>(this);
		if (IsValid(equip))
		{
			s2.Add((equip->ModelPartType));
		}
		
	}
	return IsMatch(s1, s2);
}

bool UItemBase::IsMatchLevels(TArray<int32> levels)
{
	TSet<int32> s1;
	TSet<int32> s2;
	s1.Append(levels);
	s2.Add(Level);
	return IsMatch(s1, s2);
}

bool UItemBase::IsMatchQualities(TArray<int32> qualities)
{
	TSet<int32> s1;
	TSet<int32> s2;
	s1.Append(qualities);
	s2.Add(Quality);
	return IsMatch(s1, s2);
}

bool UItemBase::IsMatch(const TSet<int32>& src, const TSet<int32>& dst)
{
	TSet<int32> temp;
	temp = src.Intersect(dst);
	if (temp.Num() > 0)
	{
		return true;
	}
	else
	{
		return false;
	}
}

bool UItemBase::IsCoolDowning()
{
	return false;
}

float UItemBase::GetCDRemainningTime()
{
	return 0.0;
}

float UItemBase::GetCDPersistTime()
{
	return 0.0;
}

void UItemBase::SetCDPersistTime(float PersistTime)
{
}