// Fill out your copyright notice in the Description page of Project Settings.


#include "ItemJadeCommond.h"

void UItemJadeCommond::InitDynamicDataForJson(FString jsonStr)
{
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	UJsonFieldData* returnvalue = temp->FromString(jsonStr);
	UJsonFieldData* root = returnvalue->GetObject(TEXT("ROOT"));
	jadeLevel = FSTRING_TO_INT(root->GetString(TEXT("jadeLevel")));
	isValid = FSTRING_TO_INT(root->GetString(TEXT("isValid")));
}
