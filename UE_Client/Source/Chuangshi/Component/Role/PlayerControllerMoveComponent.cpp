// Fill out your copyright notice in the Description page of Project Settings.

#include "PlayerControllerMoveComponent.h"
//UE4
#include "Kismet/KismetMathLibrary.h"
#include "Runtime/NavigationSystem/Public/NavigationSystem.h"
#include "Runtime/NavigationSystem/Public/NavigationPath.h"
#include "Runtime/AIModule/Classes/Navigation/PathFollowingComponent.h"
#include "Runtime/Landscape/Classes/LandscapeProxy.h"
#include "Runtime/AIModule/Classes/Blueprint/AIBlueprintHelperLibrary.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "LandscapeProxy.h"
#include "Engine/StaticMeshActor.h"
#include "Components/CapsuleComponent.h"
//CS3
#include "GameData/ConstData.h" 
#include "Actor/Player/PlayerCharacter.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Interface/SkillInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Manager/ForceManager.h"
#include "Util/CS3Debug.h"
#include "Actor/NPC/ClientGameCharacter.h"
#include "Components/PrimitiveComponent.h"

CONTROL_COMPILE_OPTIMIZE_START

DECLARE_CYCLE_STAT(TEXT("UPlayerControllerMoveComponent_TickComponent"), STAT_UPlayerControllerMoveComponent_TickComponent, STATGROUP_UPlayerControllerMoveComponent);
DECLARE_CYCLE_STAT(TEXT("UPlayerControllerMoveComponent_MouseClickMove"), STAT_UPlayerControllerMoveComponent_MouseClickMove, STATGROUP_UPlayerControllerMoveComponent);
DECLARE_CYCLE_STAT(TEXT("UPlayerControllerMoveComponent_MouseClickFly"), STAT_UPlayerControllerMoveComponent_MouseClickFly, STATGROUP_UPlayerControllerMoveComponent);
DECLARE_CYCLE_STAT(TEXT("UPlayerControllerMoveComponent_ConsumeKeyMovementInput"), STAT_UPlayerControllerMoveComponent_ConsumeKeyMovementInput, STATGROUP_UPlayerControllerMoveComponent);
DECLARE_CYCLE_STAT(TEXT("UPlayerControllerMoveComponent_SetMoveType"), STAT_UPlayerControllerMoveComponent_SetMoveType, STATGROUP_UPlayerControllerMoveComponent);

UPlayerControllerMoveComponent::UPlayerControllerMoveComponent()
{
	//bWantsBeginPlay = true;
	PrimaryComponentTick.bCanEverTick = true;
	PrimaryComponentTick.bStartWithTickEnabled = false;
	CurrMoveType = CS3_MOVE_TYPE::MOVE_TYPE_NONE;
	LastMoveType = CS3_MOVE_TYPE::MOVE_TYPE_NONE;
}

void UPlayerControllerMoveComponent::BeginPlay()
{
	Super::BeginPlay();
}

void UPlayerControllerMoveComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	SCOPE_CYCLE_COUNTER(STAT_UPlayerControllerMoveComponent_TickComponent);
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	CS3_MOVE_TYPE moveType = GetMoveType();
	switch (moveType)
	{
	case CS3_MOVE_TYPE::MOVE_TYPE_MOUSE:
		HandleMouseClickMove();
		break;
	case CS3_MOVE_TYPE::MOVE_TYPE_TRACE:
		HandleTraceMove();
		break;
	case CS3_MOVE_TYPE::MOVE_TYPE_FLY:
		HandleFlyMove(DeltaTime);
		break;
	case CS3_MOVE_TYPE::MOVE_TYPE_BACK:
		HandleHitBackMove(DeltaTime);
		break;
	case CS3_MOVE_TYPE::MOVE_TYPE_NAVIGATE:
		HandleNavigateMove();
		break;
	case CS3_MOVE_TYPE::MOVE_TYPE_TEAM_FOLLOW:
		HandleTraceMove();
		break;
	case CS3_MOVE_TYPE::MOVE_TYPE_AUTO_NAVIGATE:
		HandleAutoNavigateMove();
		break;
	default:
		break;
	}
}


void UPlayerControllerMoveComponent::HandleTraceMove()
{
	AServerCharacter* Character = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(Character))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UPlayerControllerMoveComponent::TickComponent : Character!"));
		return;
	}
	if (TraceTargetInfo.TraceTargetType == ENUM_TRACE_TARGET_TYPE::TraceTargetActor)
	{
		if (IsValid(TraceTargetInfo.TraceTarget))
		{
			if (UGolbalBPFunctionLibrary::GetActorDistance(Character, TraceTargetInfo.TraceTarget) <= TraceTargetInfo.NearbyRange*100.0f)
			{
				SetTraceResult(true);
			}
		}
		else
		{
			SetTraceResult(false);
		}
	}
	else if (TraceTargetInfo.TraceTargetType == ENUM_TRACE_TARGET_TYPE::TraceTargetPoint)
	{
		if (FVector::Dist(Character->GetActorLocation(), TraceTargetInfo.TracePostion) <= TraceTargetInfo.NearbyRange*100.0f)
		{
			SetTraceResult(true);
		}
	}
	else if (TraceTargetInfo.TraceTargetType == ENUM_TRACE_TARGET_TYPE::TraceTargetActorAtClient)
	{
		if (IsValid(TraceTargetInfo.TraceTarget))
		{
			FVector v1 = Character->GetActorLocation();
			v1.Z = 0;
			FVector v2 = TraceTargetInfo.TraceTarget->GetActorLocation();
			v2.Z = 0;

			float _Dist = FVector::Dist(v1, v2);

			if (_Dist <= TraceTargetInfo.NearbyRange*100.0f)
			{
				SetTraceResult(true);
			}
		}
		else
		{
			SetTraceResult(false);
		}
	}
}

void UPlayerControllerMoveComponent::HandleTeamFollowMove()
{
	AServerCharacter* Character = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(Character))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UPlayerControllerMoveComponent::TickComponent : Character!"));
		return;
	}
	if (IsValid(TraceTargetInfo.TraceTarget))
	{
		float Distance = UGolbalBPFunctionLibrary::GetActorDistance(Character, TraceTargetInfo.TraceTarget);
		if (Distance <= TraceTargetInfo.NearbyRange*100.0f)
		{
			TraceTargetInfo.TraceCallback.ExecuteIfBound(true);
			if (TraceTargetInfo.IsStopMove)
			{
				StopMove();
			}
			TraceTargetInfo.TraceStopMoveCallback.ExecuteIfBound(true);
		}
		else
		{
			FVector ActorLocation = Character->GetActorLocation();
			FVector TargetLocation = TraceTargetInfo.TraceTarget->GetActorLocation();
			FVector NewDirection = TargetLocation - ActorLocation;
			NewDirection.Normalize();
			Character->AddMovementInput(NewDirection);
		}
	}
	else
	{
		TraceTargetInfo.TraceCallback.ExecuteIfBound(false);
		StopMove();
		TraceTargetInfo.TraceStopMoveCallback.ExecuteIfBound(false);
	}
}

void UPlayerControllerMoveComponent::HandleFlyMove(const float& DeltaTime)
{
	AServerCharacter* Character = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(Character))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UPlayerControllerMoveComponent::TickComponent : Character!"));
		return;
	}
	float FlySpeed = Character->GetCharacterMovement()->MaxFlySpeed;
	FVector ActorLocation = Character->GetActorLocation();
	FVector NewDirection = FlyMoveInfo.FlyLocation - ActorLocation;
	bool bIsArrive = FVector::Dist(ActorLocation, FlyMoveInfo.FlyLocation) <= FlySpeed * DeltaTime;
	//飞行传送移动
	if (FlyMoveInfo.bIsFlyPatrol)
	{
		if (bIsArrive)
		{
			FlyMoveInfo.FlyCallback.ExecuteIfBound(true);
		}
		else
		{
			FRotator TargetRotator = UKismetMathLibrary::FindLookAtRotation(ActorLocation, FlyMoveInfo.FlyLocation);
			TargetRotator.Pitch = 0.0f;
			TargetRotator.Roll = 0.0f;
			if (!FlyMoveInfo.bIsFixedDirection)
			{
				Character->SetActorRotation(UKismetMathLibrary::RInterpTo(Character->GetActorRotation(), TargetRotator, DeltaTime, 2.8f));
			}
			NewDirection.Normalize();
			Character->GetCharacterMovement()->Velocity = NewDirection * FlySpeed;
		}
	}
	//普通飞行移动
	else
	{
		if (bIsArrive)
		{
			FlyMoveInfo.FlyCallback.ExecuteIfBound(true);
			StopMove();
		}
		else
		{
			NewDirection.Normalize();
			if (!FlyMoveInfo.bIsFixedDirection)
			{
				Character->AddMovementInput(NewDirection);
			}
			Character->GetCharacterMovement()->Velocity = NewDirection * FlySpeed;
		}
	}
}

void UPlayerControllerMoveComponent::HandleAutoNavigateMove()
{
	AServerCharacter* Character = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(Character))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UPlayerControllerMoveComponent::TickComponent : Character!"));
		return;
	}
	if (NavigateTargetInfo.NavigateTargetType == ENUM_NAVIGATE_TARGET_TYPE::NavigateTargetActor)
	{
		if (IsValid(NavigateTargetInfo.NavigateTarget) && NavigateTargetInfo.IsSameSpace)
		{
			if (UGolbalBPFunctionLibrary::GetActorDistance(Character,
				NavigateTargetInfo.NavigateTarget) <= NavigateTargetInfo.NearbyRange *100.0f)
			{
				NavigateTargetInfo.AutoNavigateCallback.ExecuteIfBound(true);
				StopMove();
			}
		}
		else
		{
			NavigateTargetInfo.AutoNavigateCallback.ExecuteIfBound(false);
			StopMove();
		}
	}
	else if (NavigateTargetInfo.NavigateTargetType == ENUM_NAVIGATE_TARGET_TYPE::NavigateTargetPosition)
	{
		if (NavigateTargetInfo.IsSameSpace)
		{
			FVector ActorLocation = Character->GetActorLocation();
			APlayerCharacter*  PlayerCharacter = Cast<APlayerCharacter>(Character);
			const TArray<FVector>& AutoNavPathPoints = PlayerCharacter->GetAutoNavPathPoints();
			if (AutoNavPathPoints.Num() == 0)
			{
				return;
			}
			FVector NewDirection = NavigateTargetInfo.NavigatePosition - ActorLocation;
			float NearByRange = AUTO_NAVIGATE_PLAYER_NEARBY_DISTANCE;
			int32 PosIndex = -1;
			bool IsFind = AutoNavPathPoints.Find(NavigateTargetInfo.NavigatePosition, PosIndex);
			if ( (FVector::Dist(Character->GetActorLocation(), NavigateTargetInfo.NavigatePosition) > NearByRange * 100.0f &&
				FVector::Dist(Character->GetActorLocation(), AutoNavPathPoints.Last()) > NavigateTargetInfo.NearbyRange * 100.0f) ||
				(PosIndex == AutoNavPathPoints.Num() - 1 && FVector::Dist(Character->GetActorLocation(), AutoNavPathPoints.Last()) > NavigateTargetInfo.NearbyRange * 100.0f))
			{
				/*FNavLocation ProjectLoc;
				UNavigationSystemV1 *const NavSys = FNavigationSystem::GetCurrent<UNavigationSystemV1>(GetWorld());
				FVector GoalLocation = NavigateTargetInfo.NavigatePosition;
				const FVector& EndPos = GoalLocation;
				float Speed = Cast<APlayerCharacter>(Character)->GetMoveSpeed() * 100;
				const FNavAgentProperties& AgentProps = GetWorld()->GetFirstPlayerController()->GetNavAgentPropertiesRef();
				const FVector& QueryingExtent = FVector(DEFAULT_NAV_QUERY_EXTENT_HORIZONTAL, DEFAULT_NAV_QUERY_EXTENT_HORIZONTAL, Speed);
				const ANavigationData* NavData = NavSys->GetNavDataForProps(AgentProps);
				bool bProjectedLocationValid = NavSys->ProjectPointToNavigation(EndPos, ProjectLoc, QueryingExtent, NavData);
				if (bProjectedLocationValid)
				{
					GoalLocation = ProjectLoc.Location;
				}*/

				/*UNavigationSystemV1* const NavSys = FNavigationSystem::GetCurrent<UNavigationSystemV1>(GetWorld());
				NavSys->SimpleMoveToLocation(GetWorld()->GetFirstPlayerController(), NavigateTargetInfo.NavigatePosition);*/
				ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
				if (IsValid(PlayerController))
				{
					//CST-2908事务注释了下面那行跳跃if判断
					/*if (!PlayerController->ChangeMovementTypes.Contains(CHANGE_CHARACTER_MOVEMENT_TYPE::CHANGE_CHARACTER_MOVEMENT_TYPE_JUMP))
					{
						NewDirection.Z = 0;*/
					NewDirection.Normalize();
					/*float Speed = Cast<APlayerCharacter>(Character)->GetMoveSpeed() * 100;
					FVector NewPosition = Character->OnGroundPos(ActorLocation + NewDirection*Speed*DeltaTime);
					NewDirection = NewPosition - ActorLocation;
					NewDirection.Normalize();*/
					Character->AddMovementInput(NewDirection);
					//Character->GetCharacterMovement()->Velocity = NewDirection*Speed;
				//}
				}
			}
			else
			{
				NavigateTargetInfo.AutoNavigateCallback.ExecuteIfBound(true);
			}
		}
		else
		{
			NavigateTargetInfo.AutoNavigateCallback.ExecuteIfBound(false);
			StopMove();
		}

	}
}

void UPlayerControllerMoveComponent::HandleMouseClickMove()
{
	AServerCharacter* Character = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(Character))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UPlayerControllerMoveComponent::TickComponent : Character!"));
		return;
	}
	FVector ActorLocation = Character->GetActorLocation();
	FVector NewDirection = NavigateTargetInfo.NavigatePosition - ActorLocation;
	float NearByRange = AUTO_NAVIGATE_PLAYER_NEARBY_DISTANCE;
	if (FVector::Dist(Character->GetActorLocation(), NavigateTargetInfo.NavigatePosition) <= NearByRange * 100.0f)
	{
		NavigateTargetInfo.AutoNavigateCallback.ExecuteIfBound(true);
		StopMove();
	}
	else
	{
		ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
		if (IsValid(PlayerController))
		{
			NewDirection.Normalize();
			Character->AddMovementInput(NewDirection);
		}
	}
}

void UPlayerControllerMoveComponent::HandleNavigateMove()
{
	AController* Controller = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	UPathFollowingComponent* PFollowComp = nullptr;
	if (IsValid(Controller))
	{
		PFollowComp = UGolbalBPFunctionLibrary::InitNavigationControl(*Controller);
	}
	//UPathFollowingComponent * PFollowComp = Cast<UPathFollowingComponent>(PFollowCompObj);
	if (PFollowComp && PFollowComp->GetStatus() != EPathFollowingStatus::Moving)
	{
		StopMove();
	}
}

void UPlayerControllerMoveComponent::HandleHitBackMove(const float& DeltaTime)
{
	AServerCharacter* Character = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(Character))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UPlayerControllerMoveComponent::TickComponent : Character!"));
		return;
	}
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(Character);
	if (!IsValid(PlayerCharacter)) return;
	float DefaultMaxDistance = 30.0;
	float FrameDistance = DeltaTime * MoveHitBackSpeed;//一帧移动的距离
	float RemainMoveDistance = FrameDistance;
	FVector TargetLocation = TraceTargetInfo.TracePostion;
	float TargetDistance = FVector::Distance(TargetLocation, PlayerCharacter->GetActorLocation());//与目标点的距离
	float MoveLength;

	if (TargetDistance <= 1.0f)
	{
		EndMoveBack();//结束移动
		return;
	}

	if (FrameDistance < DefaultMaxDistance)
	{
		PlayerCharacter->SetCharacterMovePosition(FMath::Min(FrameDistance, TargetDistance), TargetLocation, true, true);
	}
	else
	{
		//一帧移动的距离过大分段移动，为了碰撞检测
		while (RemainMoveDistance - DefaultMaxDistance > 0)
		{
			MoveLength = FMath::Min(TargetDistance, DefaultMaxDistance);
			PlayerCharacter->SetCharacterMovePosition(MoveLength, TargetLocation, true, true);
			RemainMoveDistance -= MoveLength;
			TargetDistance = FVector::Distance(TargetLocation, PlayerCharacter->GetActorLocation());
			if (TargetDistance <= 1.0f)
			{
				EndMoveBack();//结束移动
				return;
			}
		}
		PlayerCharacter->SetCharacterMovePosition(FMath::Min(TargetDistance, RemainMoveDistance), TargetLocation, true, true);
	}
}

void UPlayerControllerMoveComponent::MouseClickMove()
{
	SCOPE_CYCLE_COUNTER(STAT_UPlayerControllerMoveComponent_MouseClickMove);
	APlayerCharacter* Character = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!Character)
	{ 
		CS3_Warning(TEXT("-->Null Pointer error:UPlayerControllerMoveComponent::MouseClickMove : Character!"));
		return;
	}
	FVector2D PressPos;
	GetWorld()->GetFirstPlayerController()->GetMousePosition(PressPos.X, PressPos.Y);

	FHitResult HitResult;
	GetWorld()->GetFirstPlayerController()->GetHitResultAtScreenPosition(PressPos,
		GetWorld()->GetFirstPlayerController()->CurrentClickTraceChannel, true, HitResult);

	AActor* HitActor = HitResult.GetActor();
	ACharacter *HitCharacter = Cast<ACharacter>(HitActor);
	//点击到地面时才移动(1、地板  2、静态mesh 3、骨架mesh)
	if (IsValid(HitActor) && 
		(HitActor->GetClass()->IsChildOf(ALandscapeProxy::StaticClass()) || 
		HitActor->GetClass()->IsChildOf(AStaticMeshActor::StaticClass()) || 
		(HitActor->GetClass()->IsChildOf(ACharacter::StaticClass()) && HitCharacter &&
			HitCharacter->GetCapsuleComponent()->CanCharacterStepUpOn == ECanBeCharacterBase::ECB_Yes)))
	{
		float CapsuleHalfHeight = Character->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
		const FVector GoalLocation = HitResult.ImpactPoint + FVector(0.0f, 0.0f, CapsuleHalfHeight);
		
		UNavigationSystemV1 *const NavSys = FNavigationSystem::GetCurrent<UNavigationSystemV1>(UUECS3GameInstance::Instance->GetWorld());
		UNavigationPath *const NavPath = NavSys->FindPathToLocationSynchronously(UUECS3GameInstance::Instance->GetWorld(), Character->GetActorLocation(), GoalLocation, UUECS3GameInstance::Instance->GetWorld()->GetFirstPlayerController());
		if (NavPath != NULL && !NavPath->IsPartial() && NavPath->PathPoints.Num() > 0)
		{
			AutoNavigateMousePosition(GoalLocation);
		}
		else
		{
			//版本15588杨晗加的，自动战斗功能侦听了点击地面的回调
			TraceFailCallBack();
		}
		//CST-8637	程序需求（0）——鼠标点地表现
		ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
		PlayerController->MouseClickOnGround();
	}
}

void UPlayerControllerMoveComponent::MouseClickFly()
{
	SCOPE_CYCLE_COUNTER(STAT_UPlayerControllerMoveComponent_MouseClickFly);
	FVector2D PressPos;
	GetWorld()->GetFirstPlayerController()->GetMousePosition(PressPos.X, PressPos.Y);

	FHitResult HitResult;
	GetWorld()->GetFirstPlayerController()->GetHitResultAtScreenPosition(PressPos,
		GetWorld()->GetFirstPlayerController()->CurrentClickTraceChannel, true, HitResult);

	AActor* HitActor = HitResult.GetActor();
	AServerCharacter* Character = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	//点击到地面时才移动
	if (IsValid(HitActor) && (HitActor->GetClass()->IsChildOf(ALandscapeProxy::StaticClass()) || HitActor->GetClass()->IsChildOf(AStaticMeshActor::StaticClass())))
	{
		FlyToLocation(HitResult.ImpactPoint + FVector(0.0f, 0.0f, Character->GetCapsuleComponent()->GetScaledCapsuleHalfHeight()));
		//CST-8637	程序需求（0）——鼠标点地表现
		ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
		PlayerController->MouseClickOnGround();
	}
}

void UPlayerControllerMoveComponent::MoveBackToPostion(const float MoveSpeed, const FVector& TargetPostion)
{
	AServerCharacter* Character = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(Character))
	{
		SetMoveType(CS3_MOVE_TYPE::MOVE_TYPE_BACK);
		// CST-8711
		TraceTargetInfo.TracePostion = TargetPostion;
		TraceTargetInfo.NearbyRange = FVector::Distance(Character->GetActorLocation(), TargetPostion);			// 与目标距离
		MoveHitBackSpeed = MoveSpeed * 100;
	}
	

// 	UForceManager* ForceMana = UGolbalBPFunctionLibrary::ForceManager();
// 	
// 	if (IsValid(ForceMana) && IsValid(Character))
// 	{
// 		FVector _ForceDirection = TargetPostion - Character->GetActorLocation();
// 		_ForceDirection.Normalize();
// 		if (!ForceMana->BeginForce(MoveHitBackForceID, MoveHitBackSpeed, _ForceDirection))
// 		{
// 			MoveHitBackForceID = ForceMana->AddForce(Character, MoveHitBackSpeed, _ForceDirection);
// 		}
// 		
// 	}

	//UNavigationSystem *const NavSys = GetWorld()->GetNavigationSystem();
	//NavSys->SimpleMoveToLocation(GetWorld()->GetFirstPlayerController(), TargetPostion);
	//UAIBlueprintHelperLibrary::SimpleMoveToLocation(GetWorld()->GetFirstPlayerController(), TargetPostion);
}

void UPlayerControllerMoveComponent::EndMoveBack()
{
	StopMove();
	UForceManager* ForceMana = UGolbalBPFunctionLibrary::ForceManager();
	AServerCharacter* Character = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (IsValid(ForceMana) && IsValid(Character))
	{
		ForceMana->PauseForce(MoveHitBackForceID);
	}
}

void UPlayerControllerMoveComponent::TraceTargetActor(const AActor* TargetActor, float NearbyRange /*= 0.0f*/, FTraceCallback TraceCallback /*= FTraceCallback()*/, bool IsStopMove/* = true*/, FTraceCallback TraceStopMoveCallback /*= FTraceCallback()*/)
{
	SetMoveType(CS3_MOVE_TYPE::MOVE_TYPE_TRACE);
	TraceTargetInfo.TraceTargetType = ENUM_TRACE_TARGET_TYPE::TraceTargetActor;
	TraceTargetInfo.IsChasing = true;
	TraceTargetInfo.NearbyRange = NearbyRange;
	TraceTargetInfo.TraceTarget = (AActor*)TargetActor;
	TraceTargetInfo.TraceCallback = TraceCallback;
	TraceTargetInfo.IsStopMove = IsStopMove;
	TraceTargetInfo.TraceStopMoveCallback = TraceStopMoveCallback;
	//UNavigationSystem *const NavSys = GetWorld()->GetNavigationSystem();
	//NavSys->SimpleMoveToActor(GetWorld()->GetFirstPlayerController(), TargetActor);
	UAIBlueprintHelperLibrary::SimpleMoveToActor(GetWorld()->GetFirstPlayerController(), TargetActor);
}

void UPlayerControllerMoveComponent::TraceTargetActorAtClient(const AActor* TargetActor, float NearbyRange /*= 0.0f*/, FTraceCallback TraceCallback /*= FTraceCallback()*/, bool IsStopMove/* = true*/, FTraceCallback TraceStopMoveCallback /*= FTraceCallback()*/)
{
	SetMoveType(CS3_MOVE_TYPE::MOVE_TYPE_TRACE);
	TraceTargetInfo.TraceTargetType = ENUM_TRACE_TARGET_TYPE::TraceTargetActorAtClient;
	TraceTargetInfo.IsChasing = true;
	TraceTargetInfo.NearbyRange = NearbyRange;
	TraceTargetInfo.TraceTarget = (AActor*)TargetActor;
	TraceTargetInfo.TraceCallback = TraceCallback;
	TraceTargetInfo.IsStopMove = IsStopMove;
	TraceTargetInfo.TraceStopMoveCallback = TraceStopMoveCallback;
	//UNavigationSystem *const NavSys = Cast<UNavigationSystem>(GetWorld()->GetNavigationSystem());
	//NavSys->SimpleMoveToActor(GetWorld()->GetFirstPlayerController(), TargetActor);
	UAIBlueprintHelperLibrary::SimpleMoveToActor(GetWorld()->GetFirstPlayerController(), TargetActor);
}

void UPlayerControllerMoveComponent::TeamFollowTraceTarget(const AActor* TargetActor, 
	float NearbyRange /*= 0.0f*/, FTraceCallback TraceCallback /*= FTraceCallback()*/, 
	bool IsStopMove/* = true*/, FTraceCallback TraceStopMoveCallback /*= FTraceCallback()*/)
{
	if (GetMoveType() != CS3_MOVE_TYPE::MOVE_TYPE_TEAM_FOLLOW)
	{
		SetMoveType(CS3_MOVE_TYPE::MOVE_TYPE_TEAM_FOLLOW);
	}
	TraceTargetInfo.TraceTargetType = ENUM_TRACE_TARGET_TYPE::TraceTargetActor;
	TraceTargetInfo.IsChasing = true;
	TraceTargetInfo.NearbyRange = NearbyRange;
	TraceTargetInfo.TraceTarget = (AActor*)TargetActor;
	TraceTargetInfo.TraceCallback = TraceCallback;
	TraceTargetInfo.IsStopMove = IsStopMove;
	TraceTargetInfo.TraceStopMoveCallback = TraceStopMoveCallback;
	//UNavigationSystem *const NavSys = GetWorld()->GetNavigationSystem();
	//NavSys->SimpleMoveToActor(GetWorld()->GetFirstPlayerController(), TargetActor);
	UAIBlueprintHelperLibrary::SimpleMoveToActor(GetWorld()->GetFirstPlayerController(), TargetActor);
}

void UPlayerControllerMoveComponent::TraceTargetPostion(const FVector& TargetPostion, float NearbyRange /*= 0.0f*/, FTraceCallback TraceCallback /*= FTraceCallback()*/, bool IsStopMove/* = true*/, FTraceCallback TraceStopMoveCallback /*= FTraceCallback()*/)
{
	AServerCharacter* Character = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(Character))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UPlayerControllerMoveComponent::TickComponent : Character!"));
		return;
	}
	if (GetMoveType() != CS3_MOVE_TYPE::MOVE_TYPE_TRACE || TraceTargetInfo.IsStopMove == true)
	{
		if (GetMoveType() == CS3_MOVE_TYPE::MOVE_TYPE_AUTO_NAVIGATE)
		{
			SetMoveType(CS3_MOVE_TYPE::MOVE_TYPE_NONE);
		}
		SetMoveType(CS3_MOVE_TYPE::MOVE_TYPE_TRACE);
	}

	TraceTargetInfo.TraceTargetType = ENUM_TRACE_TARGET_TYPE::TraceTargetPoint;
	TraceTargetInfo.IsChasing = true;
	TraceTargetInfo.NearbyRange = NearbyRange;
	TraceTargetInfo.TracePostion = TargetPostion;
	TraceTargetInfo.IsStopMove = IsStopMove;
	TraceTargetInfo.TraceCallback = TraceCallback;
	TraceTargetInfo.TraceStopMoveCallback = TraceStopMoveCallback;
	//UNavigationSystem *const NavSys = GetWorld()->GetNavigationSystem();
	//NavSys->SimpleMoveToLocation(GetWorld()->GetFirstPlayerController(), TargetPostion);

	UAIBlueprintHelperLibrary::SimpleMoveToLocation(GetWorld()->GetFirstPlayerController(), TargetPostion);
}

void UPlayerControllerMoveComponent::FlyToLocation(const FVector& Location, bool IsFlyPatrol /*= false*/, bool IsFixedDirection /*= false*/, FTraceCallback FlyCallback /*= FTraceCallback()*/)
{
	SetMoveType(CS3_MOVE_TYPE::MOVE_TYPE_FLY);
	FlyMoveInfo.bIsFlyTo = true;
	FlyMoveInfo.FlyLocation = Location;
	FlyMoveInfo.bIsFlyPatrol = IsFlyPatrol;
	FlyMoveInfo.bIsFixedDirection = IsFixedDirection;
	FlyMoveInfo.FlyCallback = FlyCallback;
}

void UPlayerControllerMoveComponent::AutoNavigateTargetActor(const AActor* TargetActor, 
	const FString& spaceName, float NearbyRange /*= 2.0f*/, 
	FTraceCallback NavigateCallback /*= FTraceCallback()*/)
{
	if (GetMoveType() != CS3_MOVE_TYPE::MOVE_TYPE_AUTO_NAVIGATE)
	{
		SetMoveType(CS3_MOVE_TYPE::MOVE_TYPE_AUTO_NAVIGATE);
	}
	NavigateTargetInfo.NavigateTargetType = ENUM_NAVIGATE_TARGET_TYPE::NavigateTargetActor;
	const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	if (spaceName.Equals(""))
	{
		NavigateTargetInfo.SpaceName = SpaceScriptID;
		NavigateTargetInfo.IsSameSpace = true;
	}
	else
	{
		NavigateTargetInfo.SpaceName = spaceName;
		if (SpaceScriptID.Equals(spaceName))
		{
			NavigateTargetInfo.IsSameSpace = true;
		}
	}
	NavigateTargetInfo.IsAutoNavigate = true;
	NavigateTargetInfo.NavigateTarget = (AActor*)TargetActor;
	NavigateTargetInfo.NearbyRange = NearbyRange;
	NavigateTargetInfo.AutoNavigateCallback = NavigateCallback;

	//UNavigationSystem *const NavSys = GetWorld()->GetNavigationSystem();
	//NavSys->SimpleMoveToActor(GetWorld()->GetFirstPlayerController(), TargetActor);
	UAIBlueprintHelperLibrary::SimpleMoveToActor(GetWorld()->GetFirstPlayerController(), TargetActor);

}

void UPlayerControllerMoveComponent::AutoNavigateTargetPosition(const FVector& TargetPosition, const FString& spaceName /* = "" */, float NearbyRange /* = 2.0f */, FTraceCallback NavigateCallback /* = FTraceCallback() */)
{
	if (GetMoveType() != CS3_MOVE_TYPE::MOVE_TYPE_AUTO_NAVIGATE)
	{
		SetMoveType(CS3_MOVE_TYPE::MOVE_TYPE_AUTO_NAVIGATE);
	}
	NavigateTargetInfo.NavigateTargetType = ENUM_NAVIGATE_TARGET_TYPE::NavigateTargetPosition;
	const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	if (spaceName.Equals(""))
	{
		NavigateTargetInfo.SpaceName = SpaceScriptID;
		NavigateTargetInfo.IsSameSpace = true;
	}
	else
	{
		NavigateTargetInfo.SpaceName = spaceName;
		if (SpaceScriptID.Equals(spaceName))
		{
			NavigateTargetInfo.IsSameSpace = true;
		}
	}
	NavigateTargetInfo.IsAutoNavigate = true;
	NavigateTargetInfo.NavigatePosition = TargetPosition;
	NavigateTargetInfo.NearbyRange = NearbyRange;
	NavigateTargetInfo.AutoNavigateCallback = NavigateCallback;

	//UNavigationSystem *const NavSys = GetWorld()->GetNavigationSystem();
	//NavSys->SimpleMoveToLocation(GetWorld()->GetFirstPlayerController(), TargetPosition);
	//UAIBlueprintHelperLibrary::SimpleMoveToLocation(GetWorld()->GetFirstPlayerController(), TargetPosition);
}

void UPlayerControllerMoveComponent::AutoNavigateMousePosition(const FVector& TargetPosition, 
	FTraceCallback NavigateCallback /*= FTraceCallback()*/)
{
	if (GetMoveType() != CS3_MOVE_TYPE::MOVE_TYPE_MOUSE)
	{
		SetMoveType(CS3_MOVE_TYPE::MOVE_TYPE_MOUSE);
	}
	NavigateTargetInfo.NavigateTargetType = ENUM_NAVIGATE_TARGET_TYPE::NavigateTargetPosition;
	const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	NavigateTargetInfo.SpaceName = SpaceScriptID;
	NavigateTargetInfo.IsSameSpace = true;
	NavigateTargetInfo.IsAutoNavigate = true;
	NavigateTargetInfo.NavigatePosition = TargetPosition;
	NavigateTargetInfo.AutoNavigateCallback = NavigateCallback;
}

void UPlayerControllerMoveComponent::ConsumeKeyMovementInput(TArray<FVector>& MovementInput)
{
	SCOPE_CYCLE_COUNTER(STAT_UPlayerControllerMoveComponent_ConsumeKeyMovementInput);
	FVector TotalMovementInput = FVector::ZeroVector;
	for (FVector MoveVector : MovementInput)
	{
		TotalMovementInput += MoveVector;
	}
	if (TotalMovementInput == FVector::ZeroVector)
	{
		if (GetMoveType() == CS3_MOVE_TYPE::MOVE_TYPE_CONTROL)
		{
			StopMove();
		}
		return;
	}
	AServerCharacter* Character = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(Character))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UPlayerControllerMoveComponent::ConsumeKeyMovementInput : Character!"));
		return;
	}
	if (GetMoveType() != CS3_MOVE_TYPE::MOVE_TYPE_CONTROL)
	{
		SetMoveType(CS3_MOVE_TYPE::MOVE_TYPE_CONTROL);
	}
	if (Cast<ACS3PlayerController>(GetOwner())->IsCharacterMovementMode())
	{
		Character->AddMovementInput(TotalMovementInput);
	}
	else
	{
		float Speed = Character->GetMoveSpeed() * 100;
		FVector DeltaLocation = TotalMovementInput * Speed;
		FVector GoalLocation = Character->GetActorLocation() + DeltaLocation;
		float Dist = DeltaLocation.Size();
		FNavLocation ProjectLoc;
		//UNavigationSystem *const NavSys = GetWorld()->GetNavigationSystem();
		UNavigationSystemV1* NavSys = FNavigationSystem::GetCurrent<UNavigationSystemV1>(GetWorld());
		const FVector& EndPos = GoalLocation;
		const FNavAgentProperties& AgentProps = GetWorld()->GetFirstPlayerController()->GetNavAgentPropertiesRef();
		const FVector& QueryingExtent = FVector(DEFAULT_NAV_QUERY_EXTENT_HORIZONTAL, DEFAULT_NAV_QUERY_EXTENT_HORIZONTAL, Speed);
		const ANavigationData* NavData = NavSys->GetNavDataForProps(AgentProps);
		bool bProjectedLocationValid = NavSys->ProjectPointToNavigation(EndPos, ProjectLoc, QueryingExtent, NavData);
		if (bProjectedLocationValid)
		{
			GoalLocation = ProjectLoc.Location;
		}
		//NavSys->SimpleMoveToLocation(GetWorld()->GetFirstPlayerController(), GoalLocation);
		UAIBlueprintHelperLibrary::SimpleMoveToLocation(GetWorld()->GetFirstPlayerController(), GoalLocation);
	}

	TraceFailCallBack();
	MovementInput.Reset();
}


CS3_MOVE_TYPE UPlayerControllerMoveComponent::GetMoveType()
{
	return CurrMoveType;
}

void UPlayerControllerMoveComponent::StopMove()
{
	SetMoveType(CS3_MOVE_TYPE::MOVE_TYPE_NONE);
}

void UPlayerControllerMoveComponent::SetMoveType(CS3_MOVE_TYPE MoveType)
{
	SCOPE_CYCLE_COUNTER(STAT_UPlayerControllerMoveComponent_SetMoveType);
	//do something before move
	ClearFlyData();
	ClearTraceData();
	ClearHitBackData();
	APlayerCharacter* Character = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (IsValid(Character))
	{
		//飞行传送和掉落状态除外
		if ((!Character->IsFlyPatrolState()||Character->IsPausedFlyPatrol()) && !Character->GetCharacterMovement()->IsFalling()\
			&& !(GetMoveType() == CS3_MOVE_TYPE::MOVE_TYPE_AUTO_NAVIGATE && MoveType == CS3_MOVE_TYPE::MOVE_TYPE_TRACE))
		{
			Character->GetCharacterMovement()->StopMovementImmediately();
		}
	}
	///<刷新PathFollowingComponent组件的数据
	AController* Controller = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(Controller))
	{
		UPathFollowingComponent* PFollowComp = UGolbalBPFunctionLibrary::InitNavigationControl(*Controller);
		if (IsValid(PFollowComp))
		{
			PFollowComp->UpdateCachedComponents();
		}
	}
	
	//set move type
	LastMoveType = CurrMoveType;
	CurrMoveType = MoveType;	
	OnPlayerMoveTypeChange.Broadcast(GetMoveType(), LastMoveType);
	ClearAutoNavigate();
	if (Character)
	{
		Character->SyncMoveType(GetMoveType());
	}
}

void UPlayerControllerMoveComponent::ClearFlyData()
{
	///<清除数据
	FlyMoveInfo.bIsFlyTo = false;
	FlyMoveInfo.FlyLocation = FVector::ZeroVector;
	FlyMoveInfo.bIsFlyPatrol = false;
	FlyMoveInfo.FlyCallback = FTraceCallback();
}

void UPlayerControllerMoveComponent::ClearTraceData()
{
	///<通知追踪失败
	if (GetMoveType() == CS3_MOVE_TYPE::MOVE_TYPE_TRACE && TraceTargetInfo.TraceCallback.IsBound())
	{
		TraceTargetInfo.TraceCallback.ExecuteIfBound(false);
		TraceTargetInfo.TraceStopMoveCallback.ExecuteIfBound(false);
	}
	///<清除数据
	TraceTargetInfo.TraceTargetType = ENUM_TRACE_TARGET_TYPE::TraceTargetActor;
	TraceTargetInfo.IsChasing = false;
	TraceTargetInfo.NearbyRange = 0.0f;
	TraceTargetInfo.TraceTarget = nullptr;
	TraceTargetInfo.IsStopMove = true;
	TraceTargetInfo.TracePostion = FVector::ZeroVector;
	TraceTargetInfo.TraceCallback = FTraceCallback();
}

void UPlayerControllerMoveComponent::ClearAutoNavigate()
{
	NavigateTargetInfo.NavigateTargetType = ENUM_NAVIGATE_TARGET_TYPE::NavigateTargetPosition;
	NavigateTargetInfo.IsAutoNavigate = false;
	NavigateTargetInfo.IsSameSpace = false;
	NavigateTargetInfo.SpaceName = "";
	NavigateTargetInfo.NavigateTarget = nullptr;
	NavigateTargetInfo.NavigatePosition = FVector::ZeroVector;
	NavigateTargetInfo.AutoNavigateCallback = FTraceCallback();

	if (GetMoveType() != CS3_MOVE_TYPE::MOVE_TYPE_AUTO_NAVIGATE && LastMoveType == CS3_MOVE_TYPE::MOVE_TYPE_AUTO_NAVIGATE)
	{
		APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		if (IsValid(Player))
		{
			Player->ActivateNavigateMoveModeOperation(false, FVector::ZeroVector, 0.0f, "", 0, false, false);
		}
	}
}

void UPlayerControllerMoveComponent::ClearHitBackData()
{
	MoveHitBackSpeed = 0.0;
	TraceTargetInfo.NearbyRange = 0.0f;
	TraceTargetInfo.TracePostion = FVector::ZeroVector;
}

void UPlayerControllerMoveComponent::TraceFailCallBack()
{
	if (TraceTargetInfo.TraceCallback.IsBound())
	{
		TraceTargetInfo.TraceCallback.ExecuteIfBound(false);
		TraceTargetInfo.TraceCallback = FTraceCallback();
		ClearTraceData();
	}
}

void UPlayerControllerMoveComponent::SetTraceResult(bool IsSuccess)
{
	if (IsSuccess)
	{
		TraceTargetInfo.TraceCallback.ExecuteIfBound(true);		
		TraceTargetInfo.TraceCallback = FTraceCallback();
		if (TraceTargetInfo.IsStopMove)
		{
			StopMove();
		}
		TraceTargetInfo.TraceStopMoveCallback.ExecuteIfBound(true);
	}
	else
	{
		TraceTargetInfo.TraceCallback.ExecuteIfBound(false);
		TraceTargetInfo.TraceCallback = FTraceCallback();
		StopMove();
		TraceTargetInfo.TraceStopMoveCallback.ExecuteIfBound(false);
	}
}

CONTROL_COMPILE_OPTIMIZE_END
