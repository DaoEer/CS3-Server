#include "NPCExtPointInterface.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UNPCExtPointInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UNPCExtPointInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(index, &UNPCExtPointInterface::Set_index, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(occupyPlayerName, &UNPCExtPointInterface::Set_occupyPlayerName, FString)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(occupyTongName, &UNPCExtPointInterface::Set_occupyTongName, FString)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(fightEndTime, &UNPCExtPointInterface::Set_fightEndTime, FString)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(restEndTime, &UNPCExtPointInterface::Set_restEndTime, FString)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(declareWarState, &UNPCExtPointInterface::Set_declareWarState, uint8)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(pointType, &UNPCExtPointInterface::Set_pointType, uint8)
CS3_END_INTERFACE_PROPERTY_MAP()

UNPCExtPointInterface::UNPCExtPointInterface()
{
}

UNPCExtPointInterface::~UNPCExtPointInterface()
{
}

void UNPCExtPointInterface::Set_index(const int32& newVal, const int32& oldVal)
{
	index = newVal;
}

void UNPCExtPointInterface::Set_occupyPlayerName(const FString& newVal, const FString& oldVal)
{
	occupyPlayerName = newVal;
}

void UNPCExtPointInterface::Set_occupyTongName(const FString& newVal, const FString& oldVal)
{
	occupyTongName = newVal;
}

void UNPCExtPointInterface::Set_declareWarState(const uint8& newVal, const uint8& oldVal)
{
	declareWarState = NPCEXTPOINT_STATE(newVal);
}

void UNPCExtPointInterface::Set_fightEndTime(const FString& newVal, const FString& oldVal)
{
	fightEndTime = newVal;
}

void UNPCExtPointInterface::Set_restEndTime(const FString& newVal, const FString& oldVal)
{
	restEndTime = newVal;
}

void UNPCExtPointInterface::Set_pointType(const uint8& newVal, const uint8& oldVal)
{
	pointType = NPCEXTPOINT_TYPE(newVal);
}


int32 UNPCExtPointInterface::GetNPCEXTPointIndex()
{
	return index;
}

FString UNPCExtPointInterface::GetNPCEXTPointOccupyPlayerName()
{
	return occupyPlayerName;
}

FString UNPCExtPointInterface::GetNPCEXTPointOccupyTongName()
{
	return occupyTongName;
}

NPCEXTPOINT_STATE UNPCExtPointInterface::GetNPCEXTPointState()
{
	return declareWarState;
}

FString UNPCExtPointInterface::GetNPCEXTPointFightEndTime()
{
	return fightEndTime;
}

FString UNPCExtPointInterface::GetNPCEXTPointRestEndTime()
{
	return restEndTime;
}

NPCEXTPOINT_TYPE UNPCExtPointInterface::GetNPCEXTPointType()
{
	return pointType;
}
