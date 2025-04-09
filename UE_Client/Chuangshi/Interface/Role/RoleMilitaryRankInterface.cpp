// Fill out your copyright notice in the Description page of Project Settings.


#include "RoleMilitaryRankInterface.h"

#include "Util/GolbalBPFunctionLibrary.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleMilitaryRankInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(onUpdataExploit, &URoleMilitaryRankInterface::onUpdataExploit, const int32&, const int32&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleMilitaryRankInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
URoleMilitaryRankInterface::URoleMilitaryRankInterface()
{
}

int32 URoleMilitaryRankInterface::GetExploit()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleMilitaryRankInterface::GetExploit : GetEntity()!"));
		return 0;
	}
	int32 Intexploit = GetEntity()->GetDefinedProperty(TEXT("exploit")).GetValue<int32>();
	return Intexploit;
}

int32 URoleMilitaryRankInterface::GetMilitaryRank()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleMilitaryRankInterface::GetMilitaryRank : GetEntity()!"));
		return 0;
	}
	int32 IntMilitaryRank = GetEntity()->GetDefinedProperty(TEXT("militaryRank")).GetValue<int32>();
	return IntMilitaryRank;
}

void URoleMilitaryRankInterface::onUpdataExploit(const int32& exploit, const int32& militaryRank)
{
	onBPUpdataExploit(exploit, militaryRank);
}

void URoleMilitaryRankInterface::onBPUpdataExploit_Implementation(const int32& exploit, const int32& militaryRank)
{

}

void URoleMilitaryRankInterface::InitBlueCB()
{
	ArrBlueFunc.Add("onUpdataExploit");
}

void URoleMilitaryRankInterface::RPC_updataExploit()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleMilitaryRankInterface::RPC_updataExploit : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	entity->CellCall(TEXT("updataExploit"), args);
}
URoleMilitaryRankInterface::~URoleMilitaryRankInterface()
{
}
