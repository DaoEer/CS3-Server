// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "LbcData.h"


FLBC_STATUS::FLBC_STATUS(FVariant variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	index = variantMap[TEXT("index")].GetValue<uint32>();
	line = variantMap[TEXT("line")].GetValue<uint8>();
	status = variantMap[TEXT("status")].GetValue<uint8>();
}

FLBC_DECLARE_INFO::FLBC_DECLARE_INFO(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	level = variantMap[TEXT("level")].GetValue<uint8>();
	line = variantMap[TEXT("line")].GetValue<uint8>();
	lbcName = variantMap[TEXT("lbcName")].GetValue<FString>();
	status = variantMap[TEXT("status")].GetValue<uint8>();
	occupierName = variantMap[TEXT("occupierName")].GetValue<FString>();
	occupierProfession = variantMap[TEXT("occupierProfession")].GetValue<int32>();
	declarerName = variantMap[TEXT("declarerName")].GetValue<FString>();
	declarerProfession = variantMap[TEXT("declarerProfession")].GetValue<int32>();
	attackTime = variantMap[TEXT("attackTime")].GetValue<uint64>();
	index = 0;
	countDown = 0;
}

FLBC_OCCUPY_INFO::FLBC_OCCUPY_INFO(const FVariant& variant)
{
	KBEngine::FVariantMap variantMap = variant.GetValue<KBEngine::FVariantMap>();
	level = variantMap[TEXT("level")].GetValue<uint8>();
	lbcName = variantMap[TEXT("lbcName")].GetValue<FString>();
}
