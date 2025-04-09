
#include "TrapClusterAlertInterface.h"

#include "Actor/ServerCharacter.h"
#include "CS3Base/GameObject.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CustomTimerManager.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UTrapClusterAlertInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UTrapClusterAlertInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UTrapClusterAlertInterface::UTrapClusterAlertInterface()
{

}

UTrapClusterAlertInterface::~UTrapClusterAlertInterface()
{

}

void UTrapClusterAlertInterface::StartCheckRoleTimer(float interval)
{
	if (HasCheckRoleTimer())
	{
		StopCheckRoleTimer();
	}
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(CheckRoleTimerHandle_,
			this, &UTrapClusterAlertInterface::CheckRole, interval, true);
	}
}

void UTrapClusterAlertInterface::StopCheckRoleTimer()
{
	if (CheckRoleTimerHandle_.IsValid())
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(CheckRoleTimerHandle_);
		}
	}
}

bool UTrapClusterAlertInterface::HasCheckRoleTimer()
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		return UUECS3GameInstance::Instance->CustomTimerManager->GetTimerRemaining(CheckRoleTimerHandle_) > 0;
	}
	return false;
}

void UTrapClusterAlertInterface::CheckRole()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTrapClusterAlertInterface::CheckRole : GetEntity()!"));
		return;
	}
	AServerCharacter* Player = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	GameObject* entity = (GameObject*)GetEntity();
	if (!IsValid(Player) || entity == nullptr || !IsValid(GetActor()))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTrapClusterAlertInterface::CheckRole : entity!"));
		return;
	}

	if (Player->IsState(ENTITY_STATE::EntityStateDead))return;

	int32 TriggerShape = (int32)(entity->GetDefinedProperty(TEXT("triggerShape")));
	if (TriggerShape != 1)return;	//策划说只要支持圆形
	float TriggerRadius = (float)(entity->GetDefinedProperty(TEXT("triggerRadius")));

	//FVector PlayerPosition = Player->GetActorLocation();
	//FVector SelfPos = GetActor()->GetActorLocation();
	int Distance = UGolbalBPFunctionLibrary::GetActorDistance(GetActor(), Player);

	if (Distance <= TriggerRadius * 100)
	{
		KBEngine::FVariantArray Args;
		Args.Add(Player->GetSelfEntity()->ID());
		entity->CellCall(TEXT("CELL_onEnter"), Args);
	}
}

void UTrapClusterAlertInterface::OnEnterScenes()
{
	Supper::OnEnterScenes();
	StartCheckRoleTimer(1.0f);
}

void UTrapClusterAlertInterface::onLeaveWorld()
{
	Supper::onLeaveWorld();
	StopCheckRoleTimer();
}

