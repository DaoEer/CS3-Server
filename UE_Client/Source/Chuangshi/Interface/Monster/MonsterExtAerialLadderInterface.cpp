// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterExtAerialLadderInterface.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/Character.h"
#include "GameData/CharacterData.h"
#include "Kismet/KismetSystemLibrary.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UMonsterExtAerialLadderInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UMonsterExtAerialLadderInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()

UMonsterExtAerialLadderInterface::UMonsterExtAerialLadderInterface()
{

}

void UMonsterExtAerialLadderInterface::CLIENT_AerialLadderMoveFinish_Implementation(
	const FString& actionID, float LeaveTopOffset, float ClimbLadderSpeed)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("ULadderCustomMovementComponent::Debug[LadderEntityID, CLIENT_AerialLadderMoveFinish"));

	AMonsterCharacter* LadderCharacter = Cast<AMonsterCharacter>(GetActor());
	if (IsValid(LadderCharacter))
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("ULadderCustomMovementComponent::Debug[LadderEntityID=%d, actionID=%s, LeaveTopOffset=%f, ClimbLadderSpeed=%f]=======CLIENT_AerialLadderMoveFinish"),
			LadderCharacter->GetSelfEntity()->ID(), *actionID, LeaveTopOffset, ClimbLadderSpeed);

		LadderCharacter->LeaveTopOffsetZ = LeaveTopOffset * 100.0f;
		APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		PlayerCharacter->LadderCustomMovmentCpt->ClimbLadderSpeed = ClimbLadderSpeed * 100.0f;
		//开始竖梯子
		FActionOverDelegate ActionOverDelegate;
		ActionOverDelegate.AddUObject(this, &UMonsterExtAerialLadderInterface::CloudLadderActionFinish);
		LadderCharacter->PlayAction(FSTRING_TO_FNAME(actionID), 0.0f, ActionOverDelegate);
	}
}

void UMonsterExtAerialLadderInterface::CLIENT_EnterAerialLadderAOI_Implementation(float LeaveTopOffset, float ClimbLadderSpeed)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("ULadderCustomMovementComponent::Debug[LadderEntityID, CLIENT_EnterAerialLadderAOI"));

	AMonsterCharacter* LadderCharacter = Cast<AMonsterCharacter>(GetActor());
	if (IsValid(LadderCharacter))
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("ULadderCustomMovementComponent::Debug[LadderEntityID=%d, LeaveTopOffset=%f, ClimbLadderSpeed=%f]=======CLIENT_EnterAerialLadderAOI"),
			LadderCharacter->GetSelfEntity()->ID(), LeaveTopOffset, ClimbLadderSpeed);

		LadderCharacter->LeaveTopOffsetZ = LeaveTopOffset * 100.0f;
		APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		PlayerCharacter->LadderCustomMovmentCpt->ClimbLadderSpeed = ClimbLadderSpeed * 100.0f;

		FACTION_DATA ActionData;
		CloudLadderActionFinish(nullptr, ActionData);
	}
}

void UMonsterExtAerialLadderInterface::CELL_LadderBuildComplete()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("ULadderCustomMovementComponent::Debug[LadderEntityID, CELL_LadderBuildComplete"));

	if (KBEngine::Entity* entity_ = GetEntity())
	{
		KBEngine::FVariantArray param;
		entity_->CellCall(TEXT("CELL_LadderBuildComplete"), param);
	}
}

void UMonsterExtAerialLadderInterface::CLIENT_AerialLadderReadyToFall_Implementation(const FString& actionID)
{
	AMonsterCharacter* LadderCharacter = Cast<AMonsterCharacter>(GetActor());
	if (IsValid(LadderCharacter))
	{
		CS3_Display(CS3DebugType::CL_Actor, TEXT("ULadderCustomMovementComponent::Debug[LadderEntityID=%d]=======CLIENT_AerialLadderReadyToFall"),
			LadderCharacter->GetSelfEntity()->ID(), *actionID);

		CELL_LadderFallAllEntity(LadderCharacter->GetLadderAllEntityList());
		
		//播放倒梯子动作
		FActionOverDelegate ActionOverDelegate;
		ActionOverDelegate.AddUObject(this, &UMonsterExtAerialLadderInterface::FallLadderActionFinish);
		LadderCharacter->PlayAction(FSTRING_TO_FNAME(actionID), 0.0f, ActionOverDelegate);

		LadderCharacter->NofityAllCharacterFallOutToLadder();
	}
}

void UMonsterExtAerialLadderInterface::CELL_LadderFallAllEntity(TArray<int32> LadderEntityList)
{
	if (KBEngine::Entity* entity_ = GetEntity())
	{
		KBEngine::FVariantArray Args;
		Args.Add(UGolbalBPFunctionLibrary::ListToFVariant(LadderEntityList));
		entity_->CellCall(TEXT("CELL_LadderFallDead"), Args);
	}
}

void UMonsterExtAerialLadderInterface::CELL_LadderFallActionFinish()
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("ULadderCustomMovementComponent::Debug[LadderEntityID, CELL_LadderFallActionFinish"));

	if (KBEngine::Entity* entity_ = GetEntity())
	{
		KBEngine::FVariantArray param;
		entity_->CellCall(TEXT("CELL_LadderFallActionFinish"), param);
	}
}

void UMonsterExtAerialLadderInterface::CELL_EntityEnterLadder(int32 EnterEntityId)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("ULadderCustomMovementComponent::Debug[EntityID=%d]=======CELL_EntityEnterLadder"),
		EnterEntityId);

	if (KBEngine::Entity* entity_ = GetEntity())
	{
		KBEngine::FVariantArray Args;
		Args.AddUnique(EnterEntityId);
		entity_->CellCall(TEXT("CELL_EntityEnterLadder"), Args);
	}
}

void UMonsterExtAerialLadderInterface::CELL_EntityExitLadder(int32 EnterEntityId)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("ULadderCustomMovementComponent::Debug[EntityID=%d]=======CELL_EntityExitLadder"),
		EnterEntityId);

	if (KBEngine::Entity* entity_ = GetEntity())
	{
		KBEngine::FVariantArray Args;
		Args.AddUnique(EnterEntityId);
		entity_->CellCall(TEXT("CELL_EntityExitLadder"), Args);
	}
}

void UMonsterExtAerialLadderInterface::CELL_RoleReadyClimbLadder(int32 EnterEntityId)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("ULadderCustomMovementComponent::Debug[EntityID=%d]=======CELL_RoleReadyClimbLadder"),
		EnterEntityId);

	if (UGolbalBPFunctionLibrary::GetPlayerID() != EnterEntityId)return;
	if (KBEngine::Entity* entity_ = GetEntity())
	{
		KBEngine::FVariantArray Args;
		entity_->CellCall(TEXT("CELL_RoleReadyClimbLadder"), Args);
	}
}

void UMonsterExtAerialLadderInterface::CloudLadderActionFinish(ACharacter* Character, FACTION_DATA InActionData)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("ULadderCustomMovementComponent::Debug[LadderEntityID, CloudLadderActionFinish"));

	AMonsterCharacter* LadderCharacter = Cast<AMonsterCharacter>(GetActor());
	if (IsValid(LadderCharacter))
	{
		LadderCharacter->IsEnableCollisionTriggerBox = true;
		//设置梯子的包围盒，否则可能爬上去后看不到梯子了
		LadderCharacter->GetMesh()->BoundsScale = 4.0f;

		//定位顶部人物能移动的范围
		float PitchValue = LadderCharacter->LadderPitchValue;
		float CptOffasetX = PitchValue == 0.0f ? 50.0f : 20.0f;//根据角度修改定位器X偏移量
		float UnscaledCapsuleHalfHeight = LadderCharacter->GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight();

		float LessCharacterHeightTopz = FMath::Abs(LadderCharacter->StepCount - LadderCharacter->CharacterLadderNum) * LadderCharacter->StepHeight;
		float TopZ = LessCharacterHeightTopz - UnscaledCapsuleHalfHeight * 2.0f - LadderCharacter->LeaveTopOffsetZ;
		//LadderCharacter->Top->SetRelativeLocation(FVector(35.0f, 0.0f, TopZ));
		float TopX = (FMath::Sin(PitchValue * 3.1415f / 180.0f) * TopZ) * -1.0f;//梯子本身需偏移的距离
		LadderCharacter->Top->SetRelativeLocation(FVector(TopX + CptOffasetX, 0.0f, TopZ));

		//定位其他对象(怪物)顶部人物能移动的范围
		float OtherActorTopZ = TopZ + 180.0f;
		float OtherActorTopX = (FMath::Sin(PitchValue * 3.1415f / 180.0f) * OtherActorTopZ) * -1.0f;//梯子本身需偏移的距离
		//LadderCharacter->OtherActorTop->SetRelativeLocation(FVector(35.0f, 0.0f, OtherActorTopX));
		LadderCharacter->OtherActorTop->SetRelativeLocation(FVector(OtherActorTopX + CptOffasetX, 0.0f, OtherActorTopZ));

		//定位底部人物能移动的范围
		float BottomZ = UnscaledCapsuleHalfHeight * -1.0f;
		//LadderCharacter->Bottom->SetRelativeLocation(FVector(35.0f, 0.0f, BottomZ));
		float BottomX = (FMath::Sin(PitchValue * 3.1415f / 180.0f) * BottomZ) * -1.0f;
		LadderCharacter->Bottom->SetRelativeLocation(FVector(BottomX + CptOffasetX, 0.0f, BottomZ));

		//设置碰撞盒
		LadderCharacter->TriggerBox->SetRelativeScale3D(FVector(1, 2, LadderCharacter->StepCount / 2));//缩放比例(因注册点在中心)
		FRotator TriggerBoxRotator = LadderCharacter->TriggerBox->RelativeRotation;
		TriggerBoxRotator.Pitch += PitchValue;//碰撞盒倾斜10度
		LadderCharacter->TriggerBox->SetRelativeRotation(TriggerBoxRotator);//梯子倾斜10度
		float TriggerBoxExtentz = LadderCharacter->TriggerBox->GetUnscaledBoxExtent().Z;
		float TriggerBoxZ = TriggerBoxExtentz * (LadderCharacter->TriggerBox->RelativeScale3D.Z - 2);
		//LadderCharacter->TriggerBox->SetRelativeLocation(FVector(0.0f, 0.0f, TriggerBoxZ));
		float TriggerBoxHeight = LadderCharacter->StepCount * LadderCharacter->StepHeight * 0.5f;//斜边=获取梯子的长度取一半(因注册点在中心)
		float TriggerBoxX = (FMath::Sin(PitchValue * 3.1415f / 180.0f) * TriggerBoxHeight) * -1.0f;
		LadderCharacter->TriggerBox->SetRelativeLocation(FVector(TriggerBoxX, 0.0f, TriggerBoxZ));
		
		//测试线条
		/*UKismetSystemLibrary::DrawDebugBox(LadderCharacter->Top, LadderCharacter->Top->GetComponentLocation(),
			FVector(10, 50, 1), FLinearColor::Red, LadderCharacter->Top->GetComponentRotation(), 5000.0f, 10);

		UKismetSystemLibrary::DrawDebugBox(LadderCharacter->OtherActorTop, LadderCharacter->OtherActorTop->GetComponentLocation(),
			FVector(10, 50, 1), FLinearColor::Green, LadderCharacter->Top->GetComponentRotation(), 5000.0f, 10);

		UKismetSystemLibrary::DrawDebugBox(LadderCharacter->Bottom, LadderCharacter->Bottom->GetComponentLocation(),
			FVector(10, 50, 1), FLinearColor::Red, LadderCharacter->Top->GetComponentRotation(), 5000.0f, 10);*/

		//通知服务器挂梯子完毕
		CELL_LadderBuildComplete();
	}
}

void UMonsterExtAerialLadderInterface::FallLadderActionFinish(ACharacter* Character, FACTION_DATA InActionData)
{
	CS3_Display(CS3DebugType::CL_Actor, TEXT("ULadderCustomMovementComponent::Debug[LadderEntityID, FallLadderActionFinish"));

	AMonsterCharacter* LadderCharacter = Cast<AMonsterCharacter>(GetActor());
	if (IsValid(LadderCharacter))
	{
		//恢复碰撞盒
		LadderCharacter->TriggerBox->SetRelativeScale3D(FVector(1, 2, 2));
		LadderCharacter->TriggerBox->SetRelativeLocation(FVector(0.0f, 0.0f, 0.0f));

		//恢复定位底部和顶部人物能移动的范围
		LadderCharacter->Top->SetRelativeLocation(FVector(-32.0f, 0.0f, 0.0f));
		LadderCharacter->Bottom->SetRelativeLocation(FVector(-32.0f, 0.0f, 0.0f));
	}
	CELL_LadderFallActionFinish();
}

void UMonsterExtAerialLadderInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_AerialLadderMoveFinish");
	ArrBlueFunc.Add("CLIENT_AerialLadderReadyToFall");
	ArrBlueFunc.Add("CLIENT_EnterAerialLadderAOI");
	Supper::InitBlueCB();
}
