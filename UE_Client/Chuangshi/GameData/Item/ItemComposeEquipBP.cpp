// Fill out your copyright notice in the Description page of Project Settings.


#include "ItemComposeEquipBP.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/CfgManager.h"
#include "ToolCost.h"

FString UItemComposeEquipBP::GetItemName()
{
	if (ItemName != TEXT(""))
	{
		FString EquipName = ItemName;
		if (suitIndex != 0)
		{
			//根据suitIndex读表
			FName Row = FSTRING_TO_FNAME(INT_TO_FSTRING(suitIndex));
			const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_WORKSHOP_SUITNAME_DATA);
			FSuitNameCfg* data = const_cast<FSuitNameCfg*>(table->GetRow<FSuitNameCfg>(Row));
			if (data == nullptr)
			{
				CS3_Warning(TEXT("-->Null Pointer error:UItemComposeEquipBP::GetItemName : data!"));
			}
			if (!data->suitName.Equals(TEXT("")))
			{
				EquipName = ItemName + TEXT("(") + data->suitName + TEXT(")");
			}
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

FString UItemComposeEquipBP::GetAttackPropertyStr()
{
	return ParseMainPropertiesStr(attackPropertiesStr, TEXT("FFFFFFFF"));
}

FString UItemComposeEquipBP::ParseMainPropertiesStr(const FString& propstr, const FString& propcolor)
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
			for (int i = 0; i < propids.Num(); i++)
			{
				FString MainProperty;
				FString IntensifyPrecent = TEXT("");
				if (mainpro.Contains(propids[i]))
				{
					int32 value(0);
					value = int(FSTRING_TO_INT(propvalues[i]) * (float(mainpro[propids[i]]) / 100 + 1));
					MainProperty = GetPropertyStrWithNoColor(propids[i], INT_TO_FSTRING(value));
				}
				else
				{
					MainProperty = GetPropertyStrWithNoColor(propids[i], propvalues[i]);
				}


				describe += StrToColorStrWithoutBr(MainProperty, TEXT("FFFFFFFF"), TEXT("FFFFFFFF"), TEXT("[0,0]"));
				describe += IntensifyPrecent;
				//最后一个换行不需要加
				if (i < propids.Num() - 1)
				{
					describe += TEXT("<br/>");
				}
			}
		}
	}
	return describe;
}

FString UItemComposeEquipBP::GetPropertyStrWithNoColor(const FString& propid, const FString& propvalue)
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

float UItemComposeEquipBP::GetTotalSuccessRate()
{
	return successRate + addRate;
}

int32 UItemComposeEquipBP::GetComposeEquipID()
{
	return FSTRING_TO_INT(Param4);
}

void UItemComposeEquipBP::InitDynamicDataForJson(FString jsonStr)
{
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	UJsonFieldData* returnvalue = temp->FromString(jsonStr);
	UJsonFieldData* root = returnvalue->GetObject(TEXT("ROOT"));
	successRate = FSTRING_TO_INT(root->GetString(TEXT("successRate")));
	suitIndex = FSTRING_TO_INT(root->GetString(TEXT("suitIndex")));
	addRate = FSTRING_TO_FLOAT(root->GetString(TEXT("addRate")));
	attackPropertiesStr = root->GetString(TEXT("attackPropertiesStr"));
}
