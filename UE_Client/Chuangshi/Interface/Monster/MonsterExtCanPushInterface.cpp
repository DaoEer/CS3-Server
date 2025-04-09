#include "MonsterExtCanPushInterface.h"
#include "Util/ConvertUtil.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Actor/ServerCharacter.h"
#include "Manager/CustomTimerManager.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Kismet/KismetMathLibrary.h"
#include "KeyState.h"

CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtCanPushInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtCanPushInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMonsterExtCanPushInterface::UMonsterExtCanPushInterface()
{	
}


UMonsterExtCanPushInterface::~UMonsterExtCanPushInterface()
{
}

void UMonsterExtCanPushInterface::CLIENT_OnRoleNearbyMonster_Implementation(int32 MonsterID)
{
	AActor* TargetMonster = UGolbalBPFunctionLibrary::GetActorByID(MonsterID);
	AGameCharacter* Player = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(TargetMonster))
	{
		TWeakObjectPtr<UMonsterExtCanPushInterface> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, KeyDownTimerEventHandle,
			FTimerDelegate::CreateLambda([DelayThisPtr, TargetMonster, Player]()
			{
					///当玩家按键超过3秒时 给服务器发送玩家正在推箱子的通知
					float TimeSeconds = DelayThisPtr->GetWorld()->GetRealTimeSeconds();
					ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
					if (PlayerController->CheckKeyDuration(EKeys::W, 3.0f) ||
						PlayerController->CheckKeyDuration(EKeys::S, 3.0f) ||
						PlayerController->CheckKeyDuration(EKeys::A, 3.0f) ||
						PlayerController->CheckKeyDuration(EKeys::D, 3.0f))
					{
						DelayThisPtr->RPC_OnRolePushComplete();
						Player->GetBaseAnimInstance()->PlayStandbyAction();
						UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(DelayThisPtr->KeyDownTimerEventHandle);
					}

	
			}), 0.01f, true);
	}
}

void UMonsterExtCanPushInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_OnRoleNearbyMonster");
	Supper::InitBlueCB();
}

void UMonsterExtCanPushInterface::RPC_OnRolePushComplete()
{
	KBEngine::FVariantArray Args;
	if (this->GetEntity())
	{
		this->GetEntity()->CellCall(TEXT("onRolePushComplete"), Args);
	}
}

CONTROL_COMPILE_OPTIMIZE_END