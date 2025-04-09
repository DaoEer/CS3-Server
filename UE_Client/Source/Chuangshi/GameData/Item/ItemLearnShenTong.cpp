// Fill out your copyright notice in the Description page of Project Settings.


#include "ItemLearnShenTong.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "JsonFieldData.h"

void UItemLearnShenTong::InitDynamicDataForJson(FString jsonStr)
{
	Super::InitDynamicDataForJson(jsonStr);
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	UJsonFieldData* returnvalue = temp->FromString(jsonStr);
	UJsonFieldData* root = returnvalue->GetObject(TEXT("ROOT"));
	UseTimes = FSTRING_TO_INT(root->GetString(TEXT("shentongUseTimes")));
}
