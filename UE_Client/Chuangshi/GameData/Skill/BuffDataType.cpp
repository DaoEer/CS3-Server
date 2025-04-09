#include "BuffDataType.h"


UBuffDataType::UBuffDataType()
{
}

UBuffDataType::~UBuffDataType()
{
}

void UBuffDataType::setTempData(FString key, FVariant value)
{
	param.Add(key, value);
}

FVariant UBuffDataType::getTempData(FString key, FVariant default)
{
	if (param.Contains(key))
	{
		return param[key];
	}
	return default;
}
