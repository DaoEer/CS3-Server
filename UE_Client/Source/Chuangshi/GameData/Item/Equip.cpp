// Fill out your copyright notice in the Description page of Project Settings.

#include "Equip.h"
#include "Json.h"
#include "JsonFieldData.h"
#include "Util/CS3Debug.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/ServerCharacter.h"
#include "Manager/CfgManager.h"

void UEquip::InitDynamicDataForJson(FString jsonStr)
{
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	UJsonFieldData* returnvalue = temp->FromString(jsonStr);
	UJsonFieldData* root = returnvalue->GetObject(TEXT("ROOT"));
	Hardiness = FSTRING_TO_INT(root->GetString(TEXT("hardiness")));
	CombatPower = FSTRING_TO_INT(root->GetString(TEXT("combatPower")));
	AttackPropertiesStr = root->GetString(TEXT("attackProperties"));
	AttachPropertiesStr = root->GetString(TEXT("attachProperties"));
	IntensifyDataStr = root->GetString(TEXT("intensifyData"));
	if (root->GetObjectKeys(this).Contains(TEXT("Quality")))
	{
		Quality = FSTRING_TO_INT(root->GetString(TEXT("Quality")));
		OnRep_Quality();
		
	}
	ParseIntensifyStr();
}

bool UEquip::IsEquip()
{
	return true;
}

FString UEquip::GetItemName()
{
	if (ItemName != TEXT(""))
	{
		FString EquipName = ItemName;
		if (GetCurrIntensifyLv())
		{
			EquipName = ItemName + TEXT(" +") + INT_TO_FSTRING(GetCurrIntensifyLv());
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
MODEL_PART_TYPE UEquip::GetModelPartType()
{
	return (MODEL_PART_TYPE)((uint8)ModelPartType);
}

void UEquip::UnWield(AServerCharacter* player)
{
	int32 playerID = 0;
	if (!IsValid(player))
	{
		//默认是玩家
		playerID = UGolbalBPFunctionLibrary::GetPlayerID();
		if (playerID == 0)
		{
			return;
		}
	}
	else
	{
		playerID = player->EntityId;
	}
	URoleKitBagInterface * RoleKitBagInterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), playerID));
	if (RoleKitBagInterface)
	{
		RoleKitBagInterface->RPC_unWieldEquip(FString::FromInt(ItemOrder));
	}
	//FString methodname = TEXT("CELL_unWieldEquip");
	//TArray<FString> args;
	//args.Add(FString::FromInt(ItemOrder));
	//UGolbalBPFunctionLibrary::CellCall(playerID, methodname, args);
}

int32 UEquip::GetWieldOrder()
{
	return ModelPartType;
}

int32 UEquip::GetRingWieldOrder()
{
	switch (GetModelPartType())
	{
	case MODEL_PART_TYPE::MODEL_PART_LHAND_RING:
	case MODEL_PART_TYPE::MODEL_PART_RHAND_RING:
	{
		UCS3EntityInterface* BInterface = UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0);
		if (IsValid(BInterface))
		{
			URoleKitBagInterface* kbinterface = Cast<URoleKitBagInterface>(BInterface);
			return kbinterface->GetFreeRingOrder();
		}
		return (int32)GetWieldOrder();
	}
	default:
		return (int32)GetModelPartType();
	}
}

int UEquip::UseQuery(AServerCharacter* player)
{
	return Supper::UseQuery(player);
}

FString UEquip::GetPropertiesStr()
{
	FString describe = TEXT("");
	if (GetAttackPropertyStr() != TEXT(""))
	{
		describe += GetAttackPropertyStr();
	}
	if (GetAttachPropertyStr() != TEXT(""))
	{
		describe += GetAttachPropertyStr();
	}
	return describe;
}

FString UEquip::ParsePropertiesStr(const FString& propstr, const FString& propcolor)
{
	FString describe = TEXT("");
	if (propstr != TEXT(""))
	{
		TArray<FString> propids;
		TArray<FString> propvalues;
		TArray<FString> idandvalues;
		propstr.ParseIntoArray(idandvalues, TEXT("|"), true);
		for (auto item : idandvalues)
		{
			FString left;
			FString right;
			item.Split(TEXT("#"), &left, &right, ESearchCase::CaseSensitive, ESearchDir::FromEnd);
			propids.Add(left);
			propvalues.Add(right);
		}
		if (propids.Num() > 0)
		{
			for (int i = 0; i < propids.Num(); i++)
			{
				describe += GetPropertyStr(propids[i], propvalues[i], propcolor);
			}
		}
	}
	//最后一个换行不需要加
	FString left;
	FString right;
	bool IsFind;
	IsFind = describe.Split(TEXT("<br/>"), &left, &right, ESearchCase::CaseSensitive, ESearchDir::FromEnd);
	if (IsFind)
	{
		describe = left;
	}
	return describe;
}

FString UEquip::ParseMainPropertiesStr(const FString& propstr, const FString& propcolor)
{
	FString describe = TEXT("");
	if (propstr != TEXT(""))
	{
		TArray<FString> propids;
		TArray<FString> propvalues;
		TArray<FString> idandvalues;
		propstr.ParseIntoArray(idandvalues, TEXT("|"), true);
		for (auto item : idandvalues)
		{
			FString left;
			FString right;
			item.Split(TEXT("#"), &left, &right, ESearchCase::CaseSensitive, ESearchDir::FromEnd);
			propids.Add(left);
			propvalues.Add(right);
		}
		if (propids.Num() > 0)
		{
			TMap<FString, int32> mainpro;
			for (auto IntensifyInfo : IntensifyArray)
			{
				TArray<FString> tempmap;
				IntensifyInfo.MainPropertyStr.ParseIntoArray(tempmap, TEXT("|"), true);
				for (auto item : tempmap)
				{
					FString left;
					FString right;
					item.Split(TEXT("#"), &left, &right, ESearchCase::CaseSensitive, ESearchDir::FromEnd);
					if (mainpro.Contains(left))
					{
						mainpro.Add(left, mainpro[left] + FSTRING_TO_INT(right));
					}
					else
					{
						mainpro.Add(left, FSTRING_TO_INT(right));
					}
				}
			}
			for (int i = 0; i < propids.Num(); i++)
			{
				FString MainProperty;
				FString IntensifyPrecent = TEXT("");
				if (mainpro.Contains(propids[i]))
				{
					int32 value(0);
					value = int(FSTRING_TO_INT(propvalues[i]) * (float(mainpro[propids[i]]) / 100 + 1));
					MainProperty = GetPropertyStrWithNoColor(propids[i], INT_TO_FSTRING(value));

					IntensifyPrecent = GetIntensifyPercentStr(mainpro[propids[i]]);
				}
				else
				{
					MainProperty = GetPropertyStrWithNoColor(propids[i], propvalues[i]);
					IntensifyPrecent = GetIntensifyPercentStr(0);
				}
				

				describe += StrToColorStrWithoutBr(MainProperty, TEXT("FFFFFFFF"), TEXT("FFFFFFFF"), TEXT("[0,0]"));
				describe += IntensifyPrecent;
				//最后一个换行不需要加
				if (i < propids.Num()-1)
				{
					describe += TEXT("<br/>");
				}
			}
		}
	}
	return describe;
}

FString UEquip::GetPropertyStr(const FString& propid, const FString& propvalue, const FString& propcolor)
{
	FString describe = GetPropertyStrWithNoColor(propid, propvalue);
	FString showdowcolor = propcolor;
	return StrToColorStr(describe, propcolor, showdowcolor, TEXT("[0,0]"));
}

FString UEquip::GetPropertyStrWithNoColor(const FString& propid, const FString& propvalue)
{
	int32 propertyid = FSTRING_TO_INT(propid);
	FString describe = UGolbalBPFunctionLibrary::GetChinese(propid);
	switch (propertyid)
	{
	case 30001:
	case 30002:
	case 30003:
	case 30004:
	case 30005:
	case 30006:
	case 30007:
	case 30008:
	case 30009:
	case 30010:
	case 30011:
	case 30012:
	case 30013:
	{
		describe += propvalue;
		break;
	}
	case 30014:
	{
		describe = *FString::Printf(TEXT("%s%.2f"), *describe, (FSTRING_TO_FLOAT(propvalue)) / 100.0);
		break;
	}
	case 30015:
	case 30016:
	case 30017:
	{
		describe = *FString::Printf(TEXT("%s%.2f%%"), *describe, (FSTRING_TO_FLOAT(propvalue)) / 100.0);
		break;
	}
	default:
		describe += propvalue;
		break;
	}
	return describe;
}

void UEquip::ParseIntensifyStr()
{
	IntensifyArray.Empty();
	if (IntensifyDataStr != TEXT(""))
	{
		if (IntensifyDataStr.Contains(TEXT("||")))
		{
			TArray<FString> Items;
			Items = UGolbalBPFunctionLibrary::SplitString(IntensifyDataStr, false, TEXT("||"));
			for (FString Item : Items)
			{
				FIntensifyData IntensifyData;
				ParseSingleIntensifyData(Item, IntensifyData);
				IntensifyArray.Add(IntensifyData);
			}
		}
		else
		{
			FIntensifyData IntensifyData;
			ParseSingleIntensifyData(IntensifyDataStr, IntensifyData);
			IntensifyArray.Add(IntensifyData);
		}
	}
}

void UEquip::ParseSingleIntensifyData(const FString DataStr, FIntensifyData& IntensifyData)
{
	FString Left;
	FString PropertyStr;
	DataStr.Split(TEXT("$"), &Left, &PropertyStr);
	TArray<FString> SStrList = UGolbalBPFunctionLibrary::SplitString(PropertyStr, false, TEXT(":"));
	if (SStrList.Num() > 0)
	{
		IntensifyData.MainPropertyStr = SStrList[0];
	}
	if (SStrList.Num() > 1)
	{
		IntensifyData.AttachPropertyStr = SStrList[1];
	}
	FString StarLv;
	Left.Split(TEXT("*"), &IntensifyData.UID, &StarLv);
	IntensifyData.StarLevel = EIntensifyLevel(FSTRING_TO_INT(StarLv));
}

FString UEquip::GetIntensifyDes(const FString& IntensifyUID)
{
	return GetIntensifyMainPropertyDes(IntensifyUID) + GetIntensifyAttachPropertyDes(IntensifyUID);
}


FIntensifyData UEquip::GetIntensifyDataByUID(const FString& IntensifyUID)
{
	FIntensifyData NoneData;
	NoneData.UID = TEXT("-1");
	if (IntensifyArray.Num() <= 0) return NoneData;
	for (FIntensifyData Data : IntensifyArray)
	{
		if (Data.UID == IntensifyUID)
		{
			return Data;
		}
	}
	return NoneData;
}

void UEquip::GetSortIntensifyDatas(TArray<FIntensifyData>& SortDatas)
{
	IntensifyArray.Sort([](const FIntensifyData& ItemA, const FIntensifyData& ItemB) {return ItemA.StarLevel > ItemB.StarLevel; });
	SortDatas = IntensifyArray;
}

void UEquip::GetIntensifyLvSection(TArray<int32>& LvSections)
{
	int32 Min = IntensifyArray.Num();
	int32 Max = GetMaxIntensifyLv();
	if (Min == Max)
	{
		LvSections.Add(Max);
	}
	else
	{
		for (int32 i = Min; i <= Max; i++)
		{
			LvSections.Add(i);
		}
	}
}

int32 UEquip::GetMaxIntensifyLv()
{
	const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_EUQIPLV_DATAS);
	TArray<FName> RowNames;
	RowNames = table->GetRowNames();
	for (FName RowName : RowNames)
	{
		const FIntensifyLv* Data = table->GetRow<FIntensifyLv>(RowName);
		if (!Data)
		{
			CS3_Warning(TEXT("-->Null Pointer error:UEquip::GetMaxIntensifyLv : Data!"));
			return 0;
		}
		
		FString Left;
		FString Right;
		Data->MinMaxLv.Split(TEXT("-"), &Left, &Right);
		int32 MinLv = FSTRING_TO_INT(Left);
		int32 MaxLv = FSTRING_TO_INT(Right);
		if ((Level >= MinLv) && (Level <= MaxLv))
		{
			return Data->MaxIntensifyLv;
		}
	}
	return 0;
}


int32 UEquip::GetMaxLockNumByBackFair()
{
	const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_EUQIPLV_DATAS);
	TArray<FName> RowNames;
	RowNames = table->GetRowNames();
	for (FName RowName : RowNames)
	{
		const FIntensifyLv* Data = table->GetRow<FIntensifyLv>(RowName);
		if (!Data)
		{
			CS3_Warning(TEXT("-->Null Pointer error:UEquip::GetMaxIntensifyLv : Data!"));
			return 0;
		}

		FString Left;
		FString Right;
		Data->MinMaxLv.Split(TEXT("-"), &Left, &Right);
		int32 MinLv = FSTRING_TO_INT(Left);
		int32 MaxLv = FSTRING_TO_INT(Right);
		if ((Level >= MinLv) && (Level <= MaxLv))
		{
			return Data->MaxLockStar;
		}
	}
	return 0;
}

int32 UEquip::GetCurrIntensifyLv()
{
	return IntensifyArray.Num();
}

FString UEquip::GetIntensifySumPropertyStr()
{
	FString IntensifySumPropertyStr;
	TMap<int32, int32> PropertyInt;
	for (auto IntensifyInfo : IntensifyArray)
	{
		TArray<FString> allProStr = UGolbalBPFunctionLibrary::SplitString(IntensifyInfo.AttachPropertyStr, false, TEXT("|"));
		for (FString ProStr : allProStr)
		{
			TArray<FString> proStr = UGolbalBPFunctionLibrary::SplitString(ProStr, false, TEXT("#"));
			if (proStr.Num() >= 2)				// 合并相同的属性ID
			{
				int32 ProID = FSTRING_TO_INT(proStr[0]);
				if (PropertyInt.Contains(ProID))
				{
					PropertyInt[ProID] += FSTRING_TO_INT(proStr[1]);
				}
				else
				{
					PropertyInt.Add(ProID, FSTRING_TO_INT(proStr[1]));
				}
			}
		}
	}
	for (auto IT = PropertyInt.CreateConstIterator(); IT; ++IT)
	{
		if (!IntensifySumPropertyStr.IsEmpty())
		{
			IntensifySumPropertyStr += "|";
		}
		IntensifySumPropertyStr += INT_TO_FSTRING(IT.Key()) + "#" + INT_TO_FSTRING(IT.Value());
	}
	return ParsePropertiesStr(IntensifySumPropertyStr, TEXT("59C2FFFF"));
}

int32 UEquip::GetMaxLockNumBBiography()
{
	int32 MaxLock(0);
	MaxLock = IntensifyArray.Num();
	return MaxLock;
}

int32 UEquip::GetMaxLockNum()
{
	const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_EUQIPLV_DATAS);
	TArray<FName> RowNames;
	RowNames = table->GetRowNames();
	for (FName RowName : RowNames)
	{
		const FIntensifyLv* Data = table->GetRow<FIntensifyLv>(RowName);
		if (!Data)
		{
			CS3_Warning(TEXT("-->Null Pointer error:UEquip::GetMaxLockNum : Data!"));
			return 0;
		}
		FString Left;
		FString Right;
		Data->MinMaxLv.Split(TEXT("-"), &Left, &Right);
		int32 MinLv = FSTRING_TO_INT(Left);
		int32 MaxLv = FSTRING_TO_INT(Right);
		if ((Level >= MinLv) && (Level < MaxLv))
		{
			return Data->MaxLockStar;
		}
	}
	return 0;
}

bool UEquip::IsCanBackFire()
{
	if (GetCurrIntensifyLv() <= 0)	return false;
	return true;
}

FString UEquip::GetAttackPropertyStr()
{
	return ParseMainPropertiesStr(AttackPropertiesStr, TEXT("FFFFFFFF"));
}

FString UEquip::GetAttachPropertyStr()
{
	return ParsePropertiesStr(AttachPropertiesStr, TEXT("63FF9EFF"));
}

FString UEquip::GetBindStr()
{
	if (IsBinded())
	{
		return StrToColorStr(UGolbalBPFunctionLibrary::GetChinese(TEXT("BINDED")), TEXT("00FF00FF"), TEXT("00FF00FF"), TEXT("[0,0]"));
	}
	else
	{
		return StrToColorStr(UGolbalBPFunctionLibrary::GetChinese(TEXT("BIND_NONE")), TEXT("00FF00FF"), TEXT("00FF00FF"), TEXT("[0,0]"));
	}
}

FString UEquip::GetHardinessStr()
{
	int32 ShowHardIness = GetHardiness();
	int32 HardinessMax = GetHardinessMax();
	if (HardinessMax > 0)
	{
		if (ShowHardIness == 0)
		{
			return TEXT("@F{fc=(255,0,0,255)}") + (FString::FromInt(ShowHardIness) + TEXT("/") + FString::FromInt(HardinessMax));
		}
		return TEXT("@F{fc=(255,255,255,255)}") + (FString::FromInt(ShowHardIness) + TEXT("/") + FString::FromInt(HardinessMax));
	}
	return TEXT("@F{fc=(255,255,255,255)}") + UGolbalBPFunctionLibrary::GetChinese(TEXT("ALWAY_HARDINESS"));
}

int32 UEquip::GetHardiness()
{
	float hardIness = Hardiness / 10000.0;
	return (int32)ceil(hardIness);
}

float UEquip::GetHardinessPercent()
{
	int32 hardiness = GetHardiness();
	int32 hardinessMax = GetHardinessMax();
	if (hardiness < 0 || hardiness > hardinessMax)
	{
		///永不磨损
		return 1.0;
	}
	return float(GetHardiness()) / float(GetHardinessMax());
}

void UEquip::OnRep_Hardiness()
{
	UCS3EntityInterface* BInterface = UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0);
	if (IsValid(BInterface))
	{
		URoleKitBagInterface* kbinterface = Cast<URoleKitBagInterface>(BInterface);
		kbinterface->OnEquipHardinessPercentChanged(GetHardinessPercent(), UID, ItemOrder);
	}
}

void UEquip::OnRep_IntensifyDataStr()
{
	ParseIntensifyStr();
}

void UEquip::OnRep_Quality()
{
	if (QUALITY(Quality) == QUALITY::QUALITY_GREEN_SHEN)
	{
		// 因为 王道神兵 有 配置的，有封神的（还是同一个物品）！
		ItemName = KingCraft_Prefix + ItemName;
	}
}


void UEquip::GetIntensifySumStar(int32& SumIron, int32& SumCopper, int32& SumSilver, int32& SumGold)
{
	SumIron = 0;
	SumCopper = 0;
	SumSilver = 0;
	SumGold = 0;
	if (IntensifyArray.Num() > 0)
	{
		for (FIntensifyData& item : IntensifyArray)
		{
			switch (item.StarLevel)
			{
			case EIntensifyLevel::IronStar:
				SumIron += 1;
				break;
			case EIntensifyLevel::CopperStar:
				SumCopper += 1;
				break;
			case EIntensifyLevel::SilverStar:
				SumSilver += 1;
				break;
			case EIntensifyLevel::GoldStar:
				SumGold += 1;
				break;
			}
		}
	}
}

FString UEquip::GetStarDescribe()
{
	int32 SumIron = 0;
	int32 SumCopper = 0;
	int32 SumSilver = 0;
	int32 SumGold = 0;
	GetIntensifySumStar(SumIron, SumCopper, SumSilver, SumGold);
	FString des = TEXT("");
	if (SumGold > 0)
	{
		des += GetStarDesByLv(EIntensifyLevel::GoldStar, SumGold);
	}
	if (SumSilver > 0)
	{
		des += GetStarDesByLv(EIntensifyLevel::SilverStar, SumSilver);
	}
	if (SumCopper > 0)
	{
		des += GetStarDesByLv(EIntensifyLevel::CopperStar, SumCopper);
	}
	if (SumIron > 0)
	{
		des += GetStarDesByLv(EIntensifyLevel::IronStar, SumIron);
	}

	return des;
}

FString UEquip::GetStarDesByLv(const EIntensifyLevel& StarLv, const int32& Num)
{
	FString des = TEXT("");
	if (Num == 0)	return des;
	FString IconStr = TEXT("");
	switch (StarLv)
	{
	case EIntensifyLevel::IronStar:		
		IconStr = TEXT("@I{p=X1}");
		break;
	case EIntensifyLevel::CopperStar:	
		IconStr = TEXT("@I{p=X2}");
		break;
	case EIntensifyLevel::SilverStar:	
		IconStr = TEXT("@I{p=X3}");
		break;
	case EIntensifyLevel::GoldStar:		
		IconStr = TEXT("@I{p=X4}");
		break;
	}
	int32 index = 0;
	for (index; index < Num; index++)
	{
		des += IconStr;
	}
	return des;
}

FString UEquip::GetIntensifyPercentStr(const int32& Precent)
{
	FString SumPercent = TEXT("");
	SumPercent = TEXT(" ( ") + UGolbalBPFunctionLibrary::GetChinese(TEXT("IntensifyStr")) + INT_TO_FSTRING(Precent) + TEXT("% )");
	if (Precent != 0)
	{
		return StrToColorStrWithoutBr(SumPercent, TEXT("FFE036FF"), TEXT("FFFFFFFF"), TEXT("[0,0]"));
	}
	else
	{
		return TEXT("");
	}
}

bool UEquip::IsCanUse()
{
	if (Hardiness <= 0 && Hardiness != -1)
	{
		return false;
	}
	return Super::IsCanUse();
}

FString UEquip::GetIntensifyMainPropertyDes(const FString& IntensifyUID)
{
	FString des = TEXT("");
	FIntensifyData data = GetIntensifyDataByUID(IntensifyUID);
	if (data.UID != TEXT("-1"))	 //获取的强化属性不为空
	{
		FString firstPropertyID;
		int32 firstPropertyValue;
		FString secondPropertyID;
		int32 secondPropertyValue;
		data.GetMainPropertyAndValue(firstPropertyID, firstPropertyValue, secondPropertyID, secondPropertyValue);
		FString firstdes = GetPropertyStrWithNoColor(firstPropertyID, INT_TO_FSTRING(firstPropertyValue) + TEXT("%")) ;
		des += StrToColorStr(firstdes, TEXT("00FF00FF"), TEXT("00FF00FF"), TEXT("[0,0]"));
		FString seconddes = GetPropertyStrWithNoColor(secondPropertyID, INT_TO_FSTRING(secondPropertyValue) + TEXT("%"));
		des += StrToColorStr(seconddes, TEXT("00FF00FF"), TEXT("00FF00FF"), TEXT("[0,0]"));
	}
	return des;
}

FString UEquip::GetIntensifyAttachPropertyDes(const FString& IntensifyUID)
{
	FIntensifyData data = GetIntensifyDataByUID(IntensifyUID);
	if (data.UID != TEXT("-1"))	 //获取的强化属性不为空
	{
		return ParsePropertiesStr(data.AttachPropertyStr, TEXT("FFFFFFFF"));
	}
	return TEXT("");
}

TMap<FString, FString> UEquip::ParsePropertiesToMap(const FString& PropertiesStr)
{
	TMap<FString, FString> result;
	if (PropertiesStr.IsEmpty())	return result;
	TArray<FString> idandvalues;
	PropertiesStr.ParseIntoArray(idandvalues, TEXT("|"), true);
	for (auto item : idandvalues)
	{
		FString left;
		FString right;
		item.Split(TEXT("#"), &left, &right, ESearchCase::CaseSensitive, ESearchDir::FromEnd);
		result.Add(left, right);
	}
	return result;
}

int32 UEquip::GetHardinessMax()
{
	int32 HardinessMax = GetHardinessMax_real();
	if(HardinessMax != -1)
	{
		return (int32)ceil((float)(HardinessMax)/10000.0);
	}
	return HardinessMax;
}

int32 UEquip::GetHardiness_real()
{
	return Hardiness;
}

int32 UEquip::GetHardinessMax_real()
{
	
	float HardinessMax = -1;
	switch (GetModelPartType())
	{
	case MODEL_PART_TYPE::MODEL_PART_HEADS:
	case MODEL_PART_TYPE::MODEL_PART_SUITS:
	case MODEL_PART_TYPE::MODEL_PART_HAIRS:
	case MODEL_PART_TYPE::MODEL_PART_ADORN:
	case MODEL_PART_TYPE::MODEL_PART_HAT:
	case MODEL_PART_TYPE::MODEL_PART_COATS:
	case MODEL_PART_TYPE::MODEL_PART_WAIST:
	case MODEL_PART_TYPE::MODEL_PART_WRIST:
	case MODEL_PART_TYPE::MODEL_PART_GLOVES:
	case MODEL_PART_TYPE::MODEL_PART_PANTS:
	case MODEL_PART_TYPE::MODEL_PART_SHOES:
	case MODEL_PART_TYPE::MODEL_PART_CLOAK:
		HardinessMax = 600000 * FMath::Pow(1.5, 0.1 * Level - 1);
		break;
	case MODEL_PART_TYPE::MODEL_PART_BWEAPON:
	case MODEL_PART_TYPE::MODEL_PART_LWEAPON:
	case MODEL_PART_TYPE::MODEL_PART_RWEAPON:
		HardinessMax = (FMath::Pow(float(Level), 1.2) * 20 + 20000) * 100;
		break;
	case MODEL_PART_TYPE::MODEL_PART_NECKLACE:
	case MODEL_PART_TYPE::MODEL_PART_LHAND_RING:
	case MODEL_PART_TYPE::MODEL_PART_RHAND_RING:
		HardinessMax = -1;
		break;
	default:
		HardinessMax = -1;
		break;
	}
	return HardinessMax;
}
float UEquip::GetHardinessPercent_real()
{
	int32 hardiness = GetHardiness_real();
	int32 hardinessMax = GetHardinessMax_real();
	if (hardiness < 0 || hardiness > hardinessMax)
	{
		///永不磨损
		return 1.0;
	}
	if (GetHardiness() == GetHardinessMax())
	{
		///客户端显示为100%的装备不需要修理
		return 1.0;
	}
	return float(hardiness) / float(hardinessMax);
}


void UEquip::SetDynamicProperty(const int32& combatPowner, const FString& attackStr, const FString& attachStr, const FString& intensifyStr, const int32& hardiness)
{
	CombatPower = combatPowner;
	AttackPropertiesStr = attackStr;
	AttachPropertiesStr = attachStr;
	IntensifyDataStr = intensifyStr;
	Hardiness = hardiness;
	ParseIntensifyStr();
}
