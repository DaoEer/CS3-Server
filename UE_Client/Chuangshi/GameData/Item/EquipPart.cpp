// Fill out your copyright notice in the Description page of Project Settings.


#include "EquipPart.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "JsonFieldData.h"

bool UEquipPart::IsCanUse()
{
	if (quenchingNum < 10)
	{
		return false;
	}
	return UEquip::IsCanUse();
}

FString UEquipPart::GetItemName()
{
	if (ItemName != TEXT(""))
	{
		FString EquipPartName = ItemName + UGolbalBPFunctionLibrary::GetChinese(TEXT("EquipPartNameSign"));
		FLinearColor linearColor = UGolbalBPFunctionLibrary::GetItemNameColorByQuality(Quality);
		FString ColorStr = UGolbalBPFunctionLibrary::ConvertLinearColorToHex(linearColor);
		return StrToColorStr(EquipPartName, ColorStr, ColorStr, TEXT("[0,0]"));
	}
	else
	{
		return StrToColorStr(TEXT(""), TEXT("FFFFFFFF"), TEXT("FFFFFFFF"), TEXT("[0,0]"));
	}
}

FString UEquipPart::GetAttachPropertyStr()
{
	return ParsePropertiesStr(AttachPropertiesStr, TEXT("B9B9B9FF"));
}

void UEquipPart::InitDynamicDataForJson(FString jsonStr)
{
	Super::InitDynamicDataForJson(jsonStr);
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	UJsonFieldData* returnvalue = temp->FromString(jsonStr);
	UJsonFieldData* root = returnvalue->GetObject(TEXT("ROOT"));
	quenchingNum = FSTRING_TO_INT(root->GetString(TEXT("quenchingNum")));
}

