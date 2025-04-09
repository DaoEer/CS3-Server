#include "JumpAirUpState.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Component/Role/JumpComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameData/GameDeFine.h"
#include "GameDevelop/CS3PlayerController.h"

JumpAirUpState::JumpAirUpState()
{

}

JumpAirUpState::~JumpAirUpState()
{

}

void JumpAirUpState::Enter()
{
	APlayerCharacter* CurrentPlayerCharacter = Cast<APlayerCharacter>(CurrentEntity->Actor());
	if (CurrentPlayerCharacter && CurrentPlayerCharacter->JumpComponent)
	{
		CurrentPlayerCharacter->JumpComponent->UpdateJumpState(JUMP_SHOW_STATE::JUMP_SHOW_STATE_AIR_UP);
		
		// 在降落模式下禁用自动设置重力
		ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
		if (IsValid(PlayerController) && IsValid(PlayerController->GetAtkStateMar()) && 
			!PlayerController->GetAtkStateMar()->IsHaveState(EATTACT_STATE::BEHAVIOR_FALL))
		{
			CurrentPlayerCharacter->SetBaseGravityScale(1.0f);
		}

		if (CurrentPlayerCharacter->GetBaseAnimInstance())
		{
			CurrentPlayerCharacter->GetBaseAnimInstance()->PlayFallingAction();
		}

		////如果是自己，则不用同步跳跃空中动作表现
		//if (!CurrentPlayerCharacter->ActorIsPlayer())
		//{
		//	FName ActionId = "JumpAir_01";
		//	CurrentPlayerCharacter->PlayAction(ActionId);
		//}
	}
}

void JumpAirUpState::Exit()
{
}
