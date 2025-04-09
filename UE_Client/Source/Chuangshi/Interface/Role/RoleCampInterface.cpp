
#include "RoleCampInterface.h"
#include "KBEngine.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleCampInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleCampInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

URoleCampInterface::URoleCampInterface()
{
}


URoleCampInterface::~URoleCampInterface()
{
}

void URoleCampInterface::CLIENT_onMoraleChange_Implementation(const FString& newCampMorale, const FString& oldCampMorale, const FString& otherCampMorale, const int32& buffID)
{

}
void URoleCampInterface::CLIENT_OnQueryCampUIData_Implementation(const FString& taoismMorale, const FString& demonMorale, const FString& taoismVenName, const FString& demonVenName, uint8 isGetCampReward)
{

}

void URoleCampInterface::CLIENT_SetClientCampSwitch_Implementation(uint8 OpenSwitch)
{
	if (OpenSwitch)
	{
		IsOpenSwitch = true;
	}else {
		IsOpenSwitch = false;
	}
}

void URoleCampInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_onMoraleChange");
	ArrBlueFunc.Add("CLIENT_OnQueryCampUIData");
	ArrBlueFunc.Add("CLIENT_SetClientCampSwitch");
	Supper::InitBlueCB();
}

void URoleCampInterface::RPC_RquestQueryCampUIData()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleCampInterface::RPC_RquestQueryCampUIData : entity!"));
		return;
	}
	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_rquestQueryCampUIData"), args);
}

void URoleCampInterface::RPC_rquestCampMoraleReward()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleCampInterface::RPC_rquestCampMoraleReward : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("CELL_rquestCampMoraleReward"), args);
}

bool URoleCampInterface::IsOpenCampSwitch()
{
	return IsOpenSwitch;
}