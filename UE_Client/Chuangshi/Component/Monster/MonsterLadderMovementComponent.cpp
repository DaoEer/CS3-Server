// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterLadderMovementComponent.h"
#include "Interface/Monster/MonsterInterface.h"
#include "Kismet/KismetMathLibrary.h"
#include "Components/CapsuleComponent.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "MonsterAI/MonsterAIController.h"

CONTROL_COMPILE_OPTIMIZE_START
UMonsterLadderMovementComponent::UMonsterLadderMovementComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
}

void UMonsterLadderMovementComponent::BeginPlay()
{
	Super::BeginPlay();
}


void UMonsterLadderMovementComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	ClimbUpToLader(DeltaTime);
	FallDownToLader(DeltaTime);
}

void UMonsterLadderMovementComponent::InitData(AMonsterCharacter *LadderCharacter)
{
	CurMonsterCharacter = Cast<AMonsterCharacter>(GetOwner());
	CurCharacterMovement = CurMonsterCharacter->GetCharacterMovement();
	CurLadderCharacter = LadderCharacter;
}

void UMonsterLadderMovementComponent::StartClimbLadder(FVector LadderStartLocation,
	FVector LadderEndLocation, FRotator LadderRotation)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("UMonsterLadderMovementComponent::Debug[EntityID]=======StartClimbLadder"));

	AIMonsterStartLoaction = LadderStartLocation;
	AIMonsterEndLoaction = LadderEndLocation;
	if (CurMonsterCharacter->GetSelfEntity() != nullptr)
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("ULadderCustomMovementComponent::Debug[EntityID=%d]=======StartClimbLadder"),
			CurMonsterCharacter->GetSelfEntity()->ID());

		//怪物自己大小影响顶部离开位置偏移量
		float MonsterLeaveTopOffsetZ = CurMonsterCharacter->GetSelfEntity()->GetDefinedProperty(TEXT("leaveTopOffset")).GetValue<float>();
		float MonsterLeaveTopOffsetX = FMath::Sin(CurLadderCharacter->LadderPitchValue * 3.1415f / 180.0f) * MonsterLeaveTopOffsetZ;
		AIMonsterEndLoaction.X += MonsterLeaveTopOffsetX;
		AIMonsterEndLoaction.Z += MonsterLeaveTopOffsetZ;
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("UMonsterLadderMovementComponent::StartClimbLadder(LeaveTopOffsetX=%f,  LeaveTopOffsetZ=%f)"),
			MonsterLeaveTopOffsetX, MonsterLeaveTopOffsetZ);
	}
	AIMonsterRotation = LadderRotation;
	CurMonsterCharacter->SetActorLocationAndRotation(AIMonsterStartLoaction, AIMonsterRotation);

	IsAIEnterLadder = true;
	FName ActionId = "Climb_Ladder_Loop";
	CurMonsterCharacter->PlayAction(ActionId, 0.0f);
	CurMonsterCharacter->GetCharacterMovement()->SetMovementMode(MOVE_Flying);
}

void UMonsterLadderMovementComponent::StartFallToLadder()
{
	if (CurMonsterCharacter->GetSelfEntity())
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("ULadderCustomMovementComponent::Debug[EntityID=%d]=======StartFallToLadder"),
			CurMonsterCharacter->GetSelfEntity()->ID());
	}

	IsAIEnterLadder = false;
	FName ActionId = "Climb_Ladder_Fall";
	CurMonsterCharacter->PlayAction(ActionId);
	CurMonsterCharacter->GetCharacterMovement()->SetMovementMode(MOVE_Falling);

	IsLadderDownFalling = true;
	LadderResetPitch();
	FVector FloorLocation = CurMonsterCharacter->FloorTrace(CurMonsterCharacter->GetActorLocation());
	AIMonsterFallDownEndLoaction = FloorLocation;

	CS3_Display(CS3DebugType::CL_Undefined, TEXT("ULadderCustomMovementComponent::FloorLocation=(%f, %f, %f)"),
		FloorLocation.X, FloorLocation.Y, FloorLocation.Z);
}

void UMonsterLadderMovementComponent::LadderResetPitch()
{
	FRotator ActorRotation = CurMonsterCharacter->GetActorRotation();
	ActorRotation.Pitch += CurLadderCharacter->LadderPitchValue;
	CurMonsterCharacter->SetActorRotation(ActorRotation);
}

void UMonsterLadderMovementComponent::ExitTop()
{
	if (CurMonsterCharacter->GetSelfEntity())
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("ULadderCustomMovementComponent::Debug[EntityID=%d]=======ExitTop"),
			CurMonsterCharacter->GetSelfEntity()->ID());
	}

	IsAIEnterLadder = false;
	CurCharacterMovement->SetMovementMode(MOVE_Flying);
	LadderResetPitch();

	FName ActionId = "Climb_Ladder_Exit_Top";
	FActionOverDelegate ActionOverDelegate;
	ActionOverDelegate.AddUObject(this, &UMonsterLadderMovementComponent::ActionExitTopOver);
	CurMonsterCharacter->PlayAction(ActionId, 0.0f, ActionOverDelegate);

	if (CurMonsterCharacter->EntityTypeExt == ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT)
	{
		AMonsterAIController* controller = Cast<AMonsterAIController>(CurMonsterCharacter->GetController());
		if (IsValid(controller))
		{
			controller->blackboardComponent->SetValueAsEnum(FName("CurrCmd"), uint8(MONSTER_AI_COMMAND::ATTACK));
		}
	}

}

void UMonsterLadderMovementComponent::ExitFallLand()
{
	if (CurMonsterCharacter->GetSelfEntity())
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("ULadderCustomMovementComponent::Debug[EntityID=%d]=======ExitFallLand"),
			CurMonsterCharacter->GetSelfEntity()->ID());
	}

	IsLadderDownFalling = false;

	FName ActionId = "Climb_Ladder_Land";
	CurMonsterCharacter->PlayAction(ActionId);

	//通知服务器怪物掉落到地面
	UMonsterInterface* MonsterInterface = Cast<UMonsterInterface>(CurMonsterCharacter->GetEntityInterface_Cache().GameObjectInterface);
	if (IsValid(MonsterInterface))
	{
		MonsterInterface->NotifyMonsterEndFallLand();
	}
}

void UMonsterLadderMovementComponent::ClimbUpToLader(float DeltaSeconds)
{
	if (IsAIEnterLadder)
	{
		float ClimbLadderSpeed = 100.0f;// GetMoveSpeed();
		float CapsuleHalfHeight = CurMonsterCharacter->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
		FVector ActorLoccation = CurMonsterCharacter->GetActorLocation();
		FVector CharacterFootLocation = FVector(ActorLoccation.X, ActorLoccation.Y, ActorLoccation.Z - CapsuleHalfHeight);//玩家脚底位置
		FVector DistanceLocation = CharacterFootLocation - AIMonsterEndLoaction;
		float DistanceLocationSize = DistanceLocation.Size();
		if (DistanceLocationSize <= 10.0f)
		{
			ExitTop();

			int32 EntityId = 0;
			if (IsValid(CurMonsterCharacter) && CurMonsterCharacter->GetSelfEntity())
			{
				EntityId = CurMonsterCharacter->GetSelfEntity()->ID();
			}
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("AIMonsterUpToLader::Exit[EntityId=%d,  CharacterFootLoccation=(%f,  %f,  %f)]"),
				EntityId, CharacterFootLocation.X, CharacterFootLocation.Y, CharacterFootLocation.Z);
		}
		else
		{
			FVector NextCharacterFootLocation = CharacterFootLocation;
			NextCharacterFootLocation.Z += DeltaSeconds * ClimbLadderSpeed;
			FVector FindFootLocation = UKismetMathLibrary::FindClosestPointOnSegment(NextCharacterFootLocation, AIMonsterEndLoaction, AIMonsterStartLoaction);//梯子范围内找一个最近点
			FVector TempDeltaMovement = FindFootLocation - CharacterFootLocation;
			CurCharacterMovement->MoveUpdatedComponent(TempDeltaMovement, AIMonsterRotation, false);
			/*CS3_Display(CS3DebugType::CL_Undefined, TEXT("AIMonsterUpToLader::ClimbUp[EntityId=%d,  TempDeltaMovement=(%f,  %f,  %f), CharacterFootLoccation=(%f,  %f,  %f)]"),
				EntityId, TempDeltaMovement.X, TempDeltaMovement.Y, TempDeltaMovement.Z,
				CharacterFootLocation.X, CharacterFootLocation.Y, CharacterFootLocation.Z);*/
		}
	}
}

void UMonsterLadderMovementComponent::FallDownToLader(float DeltaSeconds)
{
	if (IsLadderDownFalling)
	{
		float MoveSpeed = 4;// GetMoveSpeed();
		AddSpeed += 1.0f;
		FVector CurrLocation = CurMonsterCharacter->GetActorLocation();
		float Distance = DeltaSeconds * (MoveSpeed + AddSpeed) * 100.f;//计算到达范围
		FVector Pos = AIMonsterFallDownEndLoaction - CurrLocation;
		Pos.Normalize();

		if (FMath::Abs((AIMonsterFallDownEndLoaction - CurrLocation).Size()) <= Distance)
		{
			ExitFallLand();
		}
		else
		{
			FVector Position = CurrLocation;
			Position.Z += Pos.Z * Distance;
			CurMonsterCharacter->SetActorLocation(Position);
		}
	}
}

void UMonsterLadderMovementComponent::ActionExitTopOver(ACharacter * Character, FACTION_DATA Action)
{
	CurCharacterMovement->SetMovementMode(MOVE_Walking);
}

CONTROL_COMPILE_OPTIMIZE_END
