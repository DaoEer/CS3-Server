#include "HoldEffectDataType.h"

UHoldEffectDataType::UHoldEffectDataType()
{
}

UHoldEffectDataType::~UHoldEffectDataType()
{
}

void UHoldEffectDataType::setTempData(FString key, FVariant value)
{
	param.Add(key, value);
}

FVariant UHoldEffectDataType::getTempData(FString key, FVariant default)
{
	if (param.Contains(key))
	{
		return param[key];
	}
	return default;
}
