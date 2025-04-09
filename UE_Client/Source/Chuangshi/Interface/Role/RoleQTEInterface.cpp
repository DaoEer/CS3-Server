
#include "RoleQTEInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/QTEManager.h"
#include "Util/CS3Debug.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleQTEInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleQTEInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

URoleQTEInterface::URoleQTEInterface()
{
}


URoleQTEInterface::~URoleQTEInterface()
{
}

void URoleQTEInterface::OnStartBuffQTE(const FString& TableRowName)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QTEManager))
	{
		UUECS3GameInstance::Instance->QTEManager->OnStartQTEEvent(TableRowName);
	}
}

void URoleQTEInterface::OnEndBuffQTE()
{

}

void URoleQTEInterface::OnStartStoryQTE(const FString& TableRowName)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QTEManager))
	{
		UUECS3GameInstance::Instance->QTEManager->OnStartQTEEvent(TableRowName);
	}
}

void URoleQTEInterface::onCompleteQTEBuffEvent(bool bIsSuccess)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleQTEInterface::onCompleteQTEBuffEvent no this Entity!"));
		return;
	}
	KBEngine::FVariantArray Args;
	Args.Add(FString::FromInt(int32(bIsSuccess)));
	entity->CellCall(TEXT("onCompleteQTEBuffEvent"), Args);
	
}

void URoleQTEInterface::onCompleteBuffQTE( )
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--URoleQTEInterface::onCompleteBuffQTE no this Entity!"));
		return;
	}
	KBEngine::FVariantArray Args;
	entity->CellCall(TEXT("onCompleteBuffQTE"), Args);

}

void URoleQTEInterface::InitBlueCB()
{
	ArrBlueFunc.Add("OnStartBuffQTE");
	ArrBlueFunc.Add("OnEndBuffQTE");
	ArrBlueFunc.Add("OnStartStoryQTE");
	Supper::InitBlueCB();
}
