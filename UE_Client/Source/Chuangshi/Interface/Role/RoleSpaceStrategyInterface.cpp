

#include "RoleSpaceStrategyInterface.h"
#include "Json.h"
#include "JsonFieldData.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleSpaceStrategyInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleSpaceStrategyInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
URoleSpaceStrategyInterface::URoleSpaceStrategyInterface()
{

}

URoleSpaceStrategyInterface::~URoleSpaceStrategyInterface()
{

}

void URoleSpaceStrategyInterface::CLIENT_StartSpaceStrategy_Implementation(const int32& index,const FString& data)
{
	StrategyPointList.Add(GetStrategyPointByJsonData(data));
}

void URoleSpaceStrategyInterface::CLIENT_EndSpaceStrategy_Implementation(const int32& index, const int32& isSuccess)
{
	FSPACESTRATEGYPOINTDATA stratePoint = GetStrategyPointByIndex(index);
	stratePoint.IsEnd = true;
	stratePoint.IsSuccess = isSuccess ? true : false;
}

void URoleSpaceStrategyInterface::CLIENT_ReceiveCompleteSpaceStrategy_Implementation(const int32& index, const FString& data)
{
	StrategyPointList.Add(GetStrategyPointByJsonData(data));
}

void URoleSpaceStrategyInterface::CLIENT_ReceiveOpenSpaceStrategy_Implementation(const int32& index, const FString& data)
{
	StrategyPointList.Add(GetStrategyPointByJsonData(data));
}

FSPACESTRATEGYPOINTDATA URoleSpaceStrategyInterface::GetStrategyPointByJsonData(const FString& data)
{
	CS3_Warning(TEXT("-------------------------%s"), *data);
	FSPACESTRATEGYPOINTDATA stratePoint;
	UJsonFieldData* temp = UJsonFieldData::Create(this);
	auto returnvalue = temp->FromString(data);
	stratePoint.Index = FSTRING_TO_INT(returnvalue->GetString(TEXT("index")));
	stratePoint.Describe = returnvalue->GetString(TEXT("describe"));
	stratePoint.IsEnd = FSTRING_TO_INT(returnvalue->GetString(TEXT("isEnd"))) ? true : false;
	stratePoint.IsSuccess = FSTRING_TO_INT(returnvalue->GetString(TEXT("isSuccess"))) ? true : false;
	stratePoint.IsTimeType = FSTRING_TO_INT(returnvalue->GetString(TEXT("IsTimeType"))) ? true : false;
	TSharedPtr<FJsonObject> valueObject = returnvalue->Data->GetObjectField(TEXT("valueMap"));
	for (auto vData: valueObject->Values)
	{
		stratePoint.ValueMap.Add(vData.Key, FSTRING_TO_INT(vData.Value->AsString()));
	}
	TSharedPtr<FJsonObject> rewardObject = returnvalue->Data->GetObjectField(TEXT("rewardDict"));
	for (auto rData : rewardObject->Values)
	{
		stratePoint.RewardMap.Add(FSTRING_TO_INT(rData.Key), FSTRING_TO_INT(rData.Value->AsString()));
	}
	return stratePoint;
}

FSPACESTRATEGYPOINTDATA URoleSpaceStrategyInterface::GetStrategyPointByIndex(const int32& index)
{
	FSPACESTRATEGYPOINTDATA stratePoint;
	stratePoint.Index = -1;
	for (auto point : StrategyPointList)
	{
		if (point.Index == index)
		{
			return point;
		}
	}
	return stratePoint;
}

void URoleSpaceStrategyInterface::CLIENT_OnUpdateStrategyValue_Implementation(const int32& index, const FString& key, const int32& value)
{
	FSPACESTRATEGYPOINTDATA stratePoint = GetStrategyPointByIndex(index);
	if (stratePoint.ValueMap.Contains(key))
	{
		stratePoint.ValueMap[key] = value;
	}
}
void URoleSpaceStrategyInterface::CLIENT_OnUpdateRewardValue_Implementation(const int32& index, const int32& key, const int32& value)
{
	FSPACESTRATEGYPOINTDATA stratePoint = GetStrategyPointByIndex(index);
	if (stratePoint.RewardMap.Contains(key))
	{
		stratePoint.RewardMap[key] = value;
	}
}

void URoleSpaceStrategyInterface::onLeaveWorld()
{
	StrategyPointList.Empty();
	Supper::onLeaveWorld();
}

void URoleSpaceStrategyInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_StartSpaceStrategy");
	ArrBlueFunc.Add("CLIENT_EndSpaceStrategy");
	ArrBlueFunc.Add("CLIENT_ReceiveCompleteSpaceStrategy");
	ArrBlueFunc.Add("CLIENT_ReceiveOpenSpaceStrategy");
	ArrBlueFunc.Add("CLIENT_OnUpdateStrategyValue");
	ArrBlueFunc.Add("CLIENT_OnUpdateRewardValue");
	Supper::InitBlueCB();
}

