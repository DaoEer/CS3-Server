// Fill out your copyright notice in the Description page of Project Settings.
#include "RoleInterface.h"
#include "Kismet/KismetMathLibrary.h"

#include "GameData/ConstDataBP.h"
#include "GameData/RoleJumpData.h"

#include "Actor/Player/PlayerCharacter.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Actor/SpellBox/SpellBoxCharacter.h"
#include "Interface/Monster/MonsterInterface.h"
#include "WidgetComponent.h"

#include "Manager/StoryManager.h"
#include "Manager/ParticleManager.h"
#include "Component/CollisionComponent.h"
#include "Component/Role/JumpComponent.h"
#include "Manager/SpaceEntityRelationMgr.h"
#include "Manager/SpaceDynamicEffectManager.h"
#include "Manager/ForceManager.h"
#include "Manager/TutorialManager.h"
#include "Manager/TimeManager.h"
#include "Manager/MediaPlayerManager.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3PlayerController.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CustomTimerManager.h"
#include "Manager/SystemSwitchManager.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Debug.h"
#include "CS3Base/UIManager.h"
#include "Component/Role/RideCarrierComponent.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Actor/Action/RoleAnimInstance.h"

CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(SetWeapontYCJMD, &URoleInterface::SetWeapontYCJMD, int32, const FString&, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(updateLHMJChanllengeRelation, &URoleInterface::updateLHMJChanllengeRelation, const int32&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
URoleInterface::URoleInterface()
{
}

URoleInterface::~URoleInterface()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Role::~Role!"));
}


void URoleInterface::onEnterWorld()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Role::OnEnterWorld!"));

	if (GetEntity() != nullptr && GetEntity()->IsPlayer()&& IsValid(UUECS3GameInstance::Instance->SpaceDynamicEffectManager))
	{
		UUECS3GameInstance::Instance->SpaceDynamicEffectManager->onEnterWorld();
	}
	Supper::onEnterWorld();
}

void URoleInterface::onLeaveWorld()
{
	if (GetEntity() != nullptr && GetEntity()->IsPlayer())
	{
		if (SpaceDynamicEffectDelegate.IsBound())
		{
			SpaceDynamicEffectDelegate.Clear();
		}

		if (IsValid(UUECS3GameInstance::Instance->SpaceDynamicEffectManager))
		{
			UUECS3GameInstance::Instance->SpaceDynamicEffectManager->onLeaveWorld();
		}
	}

	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Role::OnLeaveWorld!"));
	Supper::onLeaveWorld();
}

void URoleInterface::OnEnterScenes()
{
	if (GetEntity() != nullptr && GetEntity()->IsPlayer() && IsValid(UUECS3GameInstance::Instance->SpaceDynamicEffectManager))
	{
		UUECS3GameInstance::Instance->SpaceDynamicEffectManager->OnEnterScenes();
	}
	Supper::OnEnterScenes();
}
void URoleInterface::OnLeaveScenes()
{
	APlayerCharacter* Character = Cast<APlayerCharacter>(GetActor());
	if (IsValid(Character))
	{
		Character->OnLeaveScenes();
	}
	if (GetEntity() != nullptr && GetEntity()->IsPlayer() && IsValid(UUECS3GameInstance::Instance->SpaceDynamicEffectManager))
	{
		UUECS3GameInstance::Instance->SpaceDynamicEffectManager->OnLeaveScenes();
	}
	Supper::OnLeaveScenes();
}

bool URoleInterface::IsInFlags(ROLE_FLAG RoleFlag, int64 Flags)
{
	int64 Flag = int64(1) << int64(RoleFlag);
	return (Flags & Flag) == Flag;
}

void URoleInterface::PlayRandomAction(int32 RandomNumber)
{
	APlayerCharacter* Character = Cast<APlayerCharacter>(GetActor());
	if (IsValid(Character))
	{
		Character->PlayRandomAction(RandomNumber);
	}
}

void URoleInterface::OnSetJumpData_Implementation(int32 InJumpShowType, float InHeight,
	float InGravityScale, float InBrakingDecelerationFalling, float InMaxWalkSpeed)
{

}

void URoleInterface::OnSetPlayerAddGravityScale_Implementation(
	float InGravityScalePercentage, float InGravityScaleAddFixed)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	///是玩家自己
	if (IsValid(PlayerActor) && PlayerActor->ActorIsPlayer())
	{
		PlayerActor->GravityScalePercentage += InGravityScalePercentage;
		PlayerActor->GravityScaleAddFixed += InGravityScaleAddFixed;

		float NewGravityScale = PlayerActor->GetGravityScale();
		NewGravityScale += PlayerActor->GravityScaleBase * InGravityScalePercentage + InGravityScaleAddFixed;
		PlayerActor->SetGravityScale(NewGravityScale);
	}
}

void URoleInterface::OnSetBlendDir(int32 Dir)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerCharacter) && PlayerCharacter->ActorIsPlayer())
	{
		return;///如果是本地控制玩家，则不用同步
	}
	PlayerCharacter->OtherMoveDirection = (float)Dir;
}

void URoleInterface::RequestBlendDir(float Dir)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::RequestBlendDir : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(int32(Dir));
	this->GetEntity()->CellCall(TEXT("SetBlendDir"), args);
}

void URoleInterface::CLIENT_OnSetAimOffsetBlend_Implementation(float YawValue, float PitchValue)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerCharacter) && PlayerCharacter->ActorIsPlayer())
	{
		return;///如果是本地控制玩家，则不用同步
	}
	PlayerCharacter->CurAimOffsetYaw = YawValue;
	PlayerCharacter->CurAimOffsetPitch = PitchValue;
}

void URoleInterface::RequestAimOffsetBlend(float YawValue, float PitchValue)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::RequestBlendDir : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(float(YawValue));
	args.Add(float(PitchValue));
	this->GetEntity()->CellCall(TEXT("SetAimOffsetBlendData"), args);
}

void URoleInterface::SetWeapontYCJMD(int32 Type, const FString& SockeName, const FString& PartId)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (!IsValid(PlayerCharacter))
	{
		return;
	}

	if (PlayerCharacter->bIsChangeAppearanceling)
	{
		TWeakObjectPtr<URoleInterface> DelayThisPtr(this);
		TWeakObjectPtr<APlayerCharacter> DelayServerCharacterPtr(PlayerCharacter);
		if (SetWeapontHandle.IsValid())
		{
			PlayerCharacter->OnModelChangeAppearanceOverDelegate.Remove(SetWeapontHandle);
			SetWeapontHandle.Reset();
		}
		SetWeapontHandle = PlayerCharacter->OnModelChangeAppearanceOverDelegate.AddLambda(
			[DelayThisPtr, DelayServerCharacterPtr, Type, SockeName, PartId]()
			{
				if (DelayThisPtr.IsValid() && DelayServerCharacterPtr.IsValid())
				{
					URoleInterface* ThisPtr = DelayThisPtr.Get();
					APlayerCharacter* PlayerCharacter = DelayServerCharacterPtr.Get();
					if (IsValid(ThisPtr)&&IsValid(PlayerCharacter))
					{
						PlayerCharacter->UpdateWeapontYCJMD(YCJMD_COPY_WEAPON_ENUM(Type), SockeName, PartId);
						PlayerCharacter->OnModelChangeAppearanceOverDelegate.Remove(ThisPtr->SetWeapontHandle);
					}
				}
			});
	}
	else
	{
		PlayerCharacter->UpdateWeapontYCJMD(YCJMD_COPY_WEAPON_ENUM(Type), SockeName, PartId);
	}
}

void URoleInterface::CLIENT_OnRepYCJMDCopyState_Implementation(uint8 ShootState)
{
	if (GetEntity() == nullptr)
	{
		return;
	}
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerCharacter) && PlayerCharacter->ActorIsPlayer())
	{
		return;///如果是本地控制玩家，则不用同步
	}

	PlayerCharacter->bIsYCJMDCopy = bool(ShootState);
}

void URoleInterface::RequestChangeYCJMDCopyState(uint8 ShootState)
{
	if (nullptr != GetEntity())
	{
		KBEngine::FVariantArray args;
		args.Add(uint8(ShootState ? 1 : 0));
		GetEntity()->CellCall(TEXT("RequestChangeYCJMDCopyState"), args);
	}
}

void URoleInterface::CLIENT_OnRepYCJMDAimOffsetState_Implementation(uint8 AimOffsetState)
{
	if (GetEntity() == nullptr)
	{
		return;
	}
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerCharacter) && PlayerCharacter->ActorIsPlayer())
	{
		return;///如果是本地控制玩家，则不用同步
	}

	PlayerCharacter->bIsYCJMDAimOffsetState = (bool)AimOffsetState;
	PlayerCharacter->OnEnterWarnState();
}

void URoleInterface::RequestYCJMDAimOffsetState(uint8 AimOffsetState)
{
	if (nullptr != GetEntity())
	{
		KBEngine::FVariantArray args;
		args.Add(uint8(AimOffsetState ? 1 : 0));
		GetEntity()->CellCall(TEXT("RequestYCJMDAimOffsetState"), args);
	}
}

void URoleInterface::OnRep_money()
{
	if (IsValid(GetActor()) && GetEntity() != nullptr)
	{
		int64 newValue = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
		Cast<APlayerCharacter>(GetActor())->OnUpdateMoney();
	}
}

void URoleInterface::OnRep_bindmoney()
{
	if (IsValid(GetActor()) && GetEntity() != nullptr)
	{
		int64 newValue = GetEntity()->GetDefinedProperty(TEXT("bindmoney")).GetValue<int64>();
		Cast<APlayerCharacter>(GetActor())->OnUpdateBindMoney();
	}
}


int64 URoleInterface::GetMoney()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::GetMoney : GetEntity()!"));
		return 0;
	}
	int64 newValue = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
	return newValue;
}

int64 URoleInterface::GetBindMoney()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::GetBindMoney : GetEntity()!"));
		return 0;
	}
	int64 newValue = GetEntity()->GetDefinedProperty(TEXT("bindmoney")).GetValue<int64>();
	return newValue;
}

void URoleInterface::OnRep_CollisionType()
{
	APlayerCharacter* player = Cast<APlayerCharacter>(GetActor());
	if (IsValid(player) && GetEntity() != nullptr)
	{
		uint8 newValue = GetEntity()->GetDefinedProperty(TEXT("CollisionType")).GetValue<uint8>();
		switch (newValue)
		{
		case uint8(COLLISION_TYPE::COLLISION_DEFAULT):
		{
			player->CollisionComponent->SetPlayerCollisionByNormal();
			break;
		}
		case uint8(COLLISION_TYPE::COLLISION_ENEMY):
		{
			player->CollisionComponent->SetPlayerCollisionByCast();
			break;
		}
		default:
		{
			break;
		}
		}
	}
	
}

void URoleInterface::OnUpdataEffectData(TArray<int32> EffectList)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::OnUpdataEffectData : GetEntity()!"));
		return ;
	}
	if (GetEntity()->IsPlayer())
	{
		SpaceDynamicEffectDelegate.Broadcast(EffectList);
	}
}

FString URoleInterface::GetPlayerStrGold()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::GetPlayerStrGold : GetEntity()!"));
		return "";
	}
	int64 newValue = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
	return INT64_TO_FSTRING(newValue);
}

FString URoleInterface::GetPlayerStrSilver()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::GetPlayerStrSilver : GetEntity()!"));
		return "";
	}
	int64 newValue = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
	return INT64_TO_FSTRING((newValue % 10000) / 100);
}

FString URoleInterface::GetPlayerStrCopper()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::GetPlayerStrCopper : GetEntity()!"));
		return "";
	}
	int64 newValue = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
	return INT64_TO_FSTRING( newValue % 100);
}

void URoleInterface::GetRoleGoldSilverCopperByMoney(int64& goldValue, int64& silverValue, int64& copperValue)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::GetRoleGoldSilverCopperByMoney : GetEntity()!"));
		return;
	}
	int64 moneyValue = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
	goldValue = moneyValue / 10000;
	silverValue = (moneyValue % 10000) / 100;
	copperValue = moneyValue % 100;
}

bool URoleInterface::GetGoldSilverCopperByMoney(int64 money, FString& goldStr, FString& silverStr, FString& copperStr)
{
	if (money == 0)
	{
		return false;
	}
	goldStr = INT64_TO_FSTRING(money / 10000);
	silverStr = INT64_TO_FSTRING((money % 10000) / 100);
	copperStr = INT64_TO_FSTRING(money % 100);
	return true;
}

bool URoleInterface::IsMoneyEnough(int64 moneyValue)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::IsMoneyEnough : GetEntity()!"));
		return false;
	}
	int64 playerMoney = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
	if (playerMoney >= moneyValue)
	{
		return true;
	}
	return false;
}

bool URoleInterface::IsBindMoneyEnough(int64 moneyValue)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::IsBindMoneyEnough : GetEntity()!"));
		return false;
	}
	int64 playerBindMoney = GetEntity()->GetDefinedProperty(TEXT("bindmoney")).GetValue<int64>();
	if (playerBindMoney >= moneyValue)
	{
		return true;
	}
	return false;
}

bool URoleInterface::IsAllMoneyEnough(int64 moneyValue)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::IsAllMoneyEnough : GetEntity()!"));
		return false;
	}
	int64 playerMoney = GetEntity()->GetDefinedProperty(TEXT("money")).GetValue<int64>();
	int64 playerBindMoney = GetEntity()->GetDefinedProperty(TEXT("bindmoney")).GetValue<int64>();
	if ((playerMoney + playerBindMoney) >= moneyValue)
	{
		return true;
	}
	return false;
}

int64 URoleInterface::GetMoneyByGoldSilverCopper(FString goldInput, FString silverInput, FString copperInput)
{
	if ((goldInput == "") || (silverInput == "") || (copperInput == ""))
	{
		return 0;
	}
	int64 Money = FSTRING_TO_INT64(goldInput) * 10000 + FSTRING_TO_INT64(silverInput) * 100 + FSTRING_TO_INT64(copperInput);
	return Money;
}

int64 URoleInterface::GetMoneyByString(FString goldInput)
{
	if (goldInput == "")
	{
		return 0;
	}
	int64 Money = FSTRING_TO_INT64(goldInput);
	return Money;
}

FString URoleInterface::GetCompareGoldValueStr(int64 money, FString goldInput, FString silverInput, FString copperInput)
{
	if ((goldInput == "") || (silverInput == "") || (copperInput == ""))
	{
		return "";
	}
	int64 goldValue = FSTRING_TO_INT64(goldInput);
	int64 silverValue = FSTRING_TO_INT64(silverInput);
	int64 copperValue = FSTRING_TO_INT64(copperInput);
	int64 playerRemainMoney = money - (silverValue * 100 + copperValue);
	if (playerRemainMoney >= (goldValue * 10000))
	{
		return goldInput;
	}
	return INT64_TO_FSTRING((playerRemainMoney/10000));
}

FString URoleInterface::GetCompareSilverValueStr(int64 money, FString goldInput, FString silverInput, FString copperInput)
{
	if ((goldInput == "") || (silverInput == "") || (copperInput == ""))
	{
		return "";
	}
	int64 goldValue = FSTRING_TO_INT64(goldInput);
	int64 silverValue = FSTRING_TO_INT64(silverInput);
	int64 copperValue = FSTRING_TO_INT64(copperInput);
	int64 playerRemainMoney = money - (goldValue * 10000 + copperValue);
	if (playerRemainMoney >= (silverValue * 100))
	{
		return FSTRING_TO_INT64(silverInput) > 99 ? INT_TO_FSTRING(99) : silverInput;
	}
	return playerRemainMoney > 9900 ? INT_TO_FSTRING(99) : INT64_TO_FSTRING((playerRemainMoney/100));
}

FString URoleInterface::GetCompareCopperValueStr(int64 money, FString goldInput, FString silverInput, FString copperInput)
{
	if ((goldInput == "") || (silverInput == "") || (copperInput == ""))
	{
		return "";
	}
	int64 goldValue = FSTRING_TO_INT64(goldInput);
	int64 silverValue = FSTRING_TO_INT64(silverInput);
	int64 copperValue = FSTRING_TO_INT64(copperInput);
	int64 playerRemainMoney = money - (goldValue * 10000 + silverValue * 100);
	if (playerRemainMoney >= copperValue)
	{
		return FSTRING_TO_INT64(copperInput) > 99 ? INT_TO_FSTRING(99) : copperInput;
	}
	return playerRemainMoney > 99 ? INT_TO_FSTRING(99) : INT64_TO_FSTRING(playerRemainMoney);
}


FString URoleInterface::GetCompareMoneyValueStr(int64 money, FString goldInput)
{
	if (goldInput == "")
	{
		return "";
	}
	int64 goldValue = FSTRING_TO_INT64(goldInput);
	if (money >= goldValue)
	{
		return goldInput;
	}
	return INT64_TO_FSTRING(money);
}

void URoleInterface::OnRep_level()
{
	if (GetEntity() != nullptr && IsValid(GetActor()))
	{
		int16 newValue = GetEntity()->GetDefinedProperty(TEXT("level")).GetValue<int16>();
		if (newValue > old_level)
		{

			CS3_Display(CS3DebugType::CL_Undefined, TEXT("Role::Set_level, id:%d, newValue:%d, oldValue:%d"), GetEntity()->ID(), newValue, old_level);
			UUECS3GameInstance::Instance->ParticleManager->PlayParticle(TEXT("10029"), 0.0f, GetActor(), GetActor());
			if (GetEntity()->IsPlayer())
			{
				Cast<APlayerCharacter>(GetActor())->OnRoleLevelUp((int32)newValue);
			}
		}
		if (UGolbalBPFunctionLibrary::TutorialManager())
		{
			UGolbalBPFunctionLibrary::TutorialManager()->OnChangeMyRoleLevel(newValue);
		}
		//系统开启
		if (IsValid(UUECS3GameInstance::Instance) && UUECS3GameInstance::Instance->SystemSwitchManager)
		{
			UUECS3GameInstance::Instance->SystemSwitchManager->OnChangeMyRoleLevel(newValue);
		}
	}
}

void URoleInterface::OnRep_killingValue()
{
	if (GetEntity() != nullptr && IsValid(GetActor()))
	{
		int32 newValue = GetEntity()->GetDefinedProperty(TEXT("killingValue")).GetValue<int32>();
		if (GetEntity()->IsPlayer())
		{
			Cast<APlayerCharacter>(GetActor())->OnRoleKillingValueChange(newValue);
		}
	}
}

void URoleInterface::OnRep_xiuweiLevel()
{
	if (GetEntity() != nullptr && IsValid(GetActor()))
	{
		int32 newValue = GetEntity()->GetDefinedProperty(TEXT("xiuweiLevel")).GetValue<int32>();
		if (newValue > old_xiuweiLevel && old_xiuweiLevel != 0)
		{

			CS3_Display(CS3DebugType::CL_Undefined, TEXT("Role::Set_xiuweiLevel, id:%d, newValue:%d, oldValue:%d"), GetEntity()->ID(), newValue, old_xiuweiLevel);
			if (GetEntity()->IsPlayer())
			{
				Cast<APlayerCharacter>(GetActor())->OnRoleXiuweiLevelUp(newValue);
			}
		}
	}
}

void URoleInterface::OnRep_jingjieLevel()
{
	if (GetEntity() != nullptr && IsValid(GetActor()))
	{
		int32 newValue = GetEntity()->GetDefinedProperty(TEXT("jingjieLevel")).GetValue<int32>();
		if (newValue > old_jingjieLevel && old_jingjieLevel != 0)
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("Role::Set_jingjieLevel, id:%d, newValue:%d, oldValue:%d"), GetEntity()->ID(), newValue, old_jingjieLevel);
			UUECS3GameInstance::Instance->ParticleManager->PlayParticle(TEXT("10030"), 0.0f, GetActor(), GetActor());
			if (GetEntity()->IsPlayer())
			{
				Cast<APlayerCharacter>(GetActor())->OnRoleJingjieLevelUp(newValue);
			}
		}
	}
}

int32 URoleInterface::GetXiuwei()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::GetStrXiuwei : GetEntity()!"));
		return 0;
	}
	int32 Intxiuwei = GetEntity()->GetDefinedProperty(TEXT("xiuwei")).GetValue<int32>();
	return Intxiuwei;
}


void URoleInterface::OnRep_onWaterArea()
{
	if (GetEntity() != nullptr && IsValid(GetActor()))
	{
		int32 newValue = GetEntity()->GetDefinedProperty(TEXT("onWaterArea")).GetValue<int32>();
		if (GetEntity()->IsPlayer())
		{
			Cast<APlayerCharacter>(GetActor())->OnRoleOnWaterAreaChange(newValue);
		}
	}
}

void URoleInterface::ReTriggerNearTrap(const float& Range)
{
	TArray<AActor*> MonsterList = UGolbalBPFunctionLibrary::GetActorsInRange(AMonsterCharacter::StaticClass(), Range * 100.0f);
	for (AActor* i : MonsterList) 
	{
		AMonsterCharacter* MonsterAcotor = Cast<AMonsterCharacter>(i);
		if (MonsterAcotor->EntityId != 0) 
		{
			UCS3EntityInterface* BaseInterface = UGolbalBPFunctionLibrary::GetInterfaceByName("GameObjectInterface", MonsterAcotor->EntityId);
			if (IsValid(BaseInterface))
			{
				UMonsterInterface* MonsterInterface = Cast<UMonsterInterface>(BaseInterface);
				if (IsValid(MonsterInterface))
				{
					MonsterInterface->CLIENT_PlayerReTriggerTrap();
				}
			}
		}
	}
}


void URoleInterface::AddAxternalVelocity(const float& WindRotatorX, const float& WindRotatorY, const float& WindRotatorZ, const float& WindSpeed)
{
	FVector WindDirection = UKismetMathLibrary::CreateVectorFromYawPitch(WindRotatorZ, WindRotatorY);
	WindDirection.Normalize();

	float Speed = WindSpeed * 100.0f;

	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());

	if (IsValid(PlayerActor))
	{
		PlayerActor->AddWindForce(Speed, WindDirection);
	}
	else
	{
		CS3_Warning(TEXT("URoleInterface::AddAxternalVelocity-- PlayerActor is NULL !"));
	}
}

void URoleInterface::ChangeAxternalPercentage(const float& Percentage)
{
	UForceManager* ForceManager =  UGolbalBPFunctionLibrary::ForceManager();
	AServerCharacter* PlayerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();

	if (IsValid(ForceManager) && IsValid(PlayerCharacter))
	{
		ForceManager->SetCharacterForcePercentage(PlayerCharacter, Percentage);
	}
}

void URoleInterface::RemoveAxternalVelocity(const float& WindRotatorX, const float& WindRotatorY, const float& WindRotatorZ, const float& WindSpeed)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());

	if (IsValid(PlayerActor))
	{
		PlayerActor->StopAllWindForces();
	}
	else
	{
		CS3_Warning(TEXT("URoleInterface::RemoveAxternalVelocity-- PlayerActor is NULL !"));
	}
}

int32 URoleInterface::GetRelationRule()
{
	if (GetEntity() == nullptr) 
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::GetRelationRule : GetEntity()!"));
		return 0;
	}
	int32 spaceRelRule = GetEntity()->GetDefinedProperty(TEXT("spaceRelationRule")).GetValue<int32>();
	int32 areaRelRule = GetEntity()->GetDefinedProperty(TEXT("areaRelationRule")).GetValue<int32>();
	if (areaRelRule != 0)
	{
		return areaRelRule;
	}
	return spaceRelRule;
}

COMBAT_RELATION URoleInterface::GetPkModeRelation(KBEngine::Entity* TargetPlayer)
{
	if (GetEntity() == nullptr || TargetPlayer == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::GetPkModeRelation : GetEntity()||TargetPlayer!"));
		return COMBAT_RELATION::COMBAT_RELATION_DEFAULT;
	}
	if (GetEntity()->ID() == TargetPlayer->ID())
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	int16 TargetLevel = TargetPlayer->GetDefinedProperty(TEXT("level")).GetValue<int16>();
	if (TargetLevel<30)
	{
		return COMBAT_RELATION::COMBAT_RELATION_DEFAULT;
	}
	APlayerCharacter* SelfActor = Cast<APlayerCharacter>(GetActor());
	APlayerCharacter* TargetActor = Cast<APlayerCharacter>(TargetPlayer->Actor());
	if (!SelfActor || !TargetActor)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::GetPkModeRelation : SelfActor || TargetActor!"));
		return COMBAT_RELATION::COMBAT_RELATION_DEFAULT;
	}

	int32 SelfPkMode = GetEntity()->GetDefinedProperty(TEXT("pkMode")).GetValue<int32>();
	int32 TargetPkMode = TargetPlayer->GetDefinedProperty(TEXT("pkMode")).GetValue<int32>();

	if (SelfPkMode == int(ROLE_PK_MODE::PK_MODE_PEACE)) ///和平模式
	{
		TMap<int32, int32> EnemyList = GetEnemyList();
		if (EnemyList.Contains(TargetPlayer->ID()))
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	else if (SelfPkMode == int(ROLE_PK_MODE::PK_MODE_CAMP)) ///阵营模式
	{
		TMap<int32, int32> EnemyList = GetEnemyList();
		int32 SelfCamp = SelfActor->GetFinalCamp();
		int32 TargetCamp = TargetActor->GetFinalCamp();
		COMBAT_RELATION CampRelation = UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetCampRelation(SelfCamp, TargetCamp);
		if (TargetPkMode == int(ROLE_PK_MODE::PK_MODE_PEACE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}
		if (EnemyList.Contains(TargetPlayer->ID()))
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}
		if (CampRelation != COMBAT_RELATION::COMBAT_RELATION_DEFAULT)
		{
			return CampRelation;
		}
	}
	else if (SelfPkMode == int(ROLE_PK_MODE::PK_MODE_RIGHTFUL)) ///正义模式
	{
		TMap<int32, int32> EnemyList = GetEnemyList();
		int32 KillingValue = TargetPlayer->GetDefinedProperty(TEXT("KillingValue")).GetValue<int32>();
		if (KillingValue >= UUECS3GameInstance::Instance->ConstDataBP->KV_ORANGE_NAME || EnemyList.Contains(TargetPlayer->ID()))
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}
		else 
		{
			COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}
	}
	else if (SelfPkMode == int(ROLE_PK_MODE::PK_MODE_SLAUGHTER))	///恶意模式
	{
		return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
	}

	return COMBAT_RELATION::COMBAT_RELATION_DEFAULT;
}

TMap<int32, int32> URoleInterface::GetEnemyList()
{
	TMap<int32, int32> EnemyList;
	if (!GetEntity())
	{
		CS3_Warning(TEXT("-->Null Pointer error: URoleInterface::GetEnemyList : GetEntity()!"));
		return EnemyList;
	}
	FVariant newValue = GetEntity()->GetDefinedProperty(TEXT("enemyList"));
	KBEngine::FVariantMap mapval = newValue.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray ArrayItems = mapval.Find(TEXT("items"))->GetValue<KBEngine::FVariantArray>();
	for (int i = 0; i < ArrayItems.Num(); ++i)
	{
		KBEngine::FVariantMap v = ArrayItems[i].GetValue<KBEngine::FVariantMap>();
		EnemyList.Add(v[TEXT("entityID")].GetValue<int32>(), v[TEXT("time")].GetValue<int32>());
	}
	return EnemyList;
}

TMap<int32, int32> URoleInterface::GetDamageList()
{
	TMap<int32, int32> DamageList;
	if (!GetEntity())
	{
		return DamageList;
	}
	FVariant newValue = GetEntity()->GetDefinedProperty(TEXT("damageList"));
	KBEngine::FVariantMap mapval = newValue.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray ArrayItems = mapval.Find(TEXT("items"))->GetValue<KBEngine::FVariantArray>();
	for (int i = 0; i < ArrayItems.Num(); ++i)
	{
		KBEngine::FVariantMap v = ArrayItems[i].GetValue<KBEngine::FVariantMap>();
		DamageList.Add(v[TEXT("entityID")].GetValue<int32>(), v[TEXT("value")].GetValue<int32>());
	}
	return DamageList;
}

void URoleInterface::OnMountTalisman_Implementation(float DelayTime, const FString& CarrierId, float InputYawScale)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor))
	{
		///是玩家自己就野外竞速；否则就是同步其他玩家的野外竞速表现，只需要上载具就行了
		if (PlayerActor->ActorIsPlayer())
		{
			PlayerActor->OnStartOutsideCopyGame(DelayTime, CarrierId, InputYawScale);
		}
		else
		{
			if (IsValid(PlayerActor->RideCarrierComponent))
			{
				PlayerActor->RideCarrierComponent->RideOnCarrier(CarrierId);
			}
		}
	}
}

void URoleInterface::OnDismountTalisman()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	AServerCharacter* CS3PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();

	if (IsValid(PlayerActor) && PlayerActor->GetSelfEntity() &&
		IsValid(CS3PlayerActor) && CS3PlayerActor->GetSelfEntity())
	{
		int32 PlayerEntityId = PlayerActor->GetSelfEntity()->ID();
		int32 CS3PlayerEntityId = CS3PlayerActor->GetSelfEntity()->ID();

		///是玩家自己退出野外竞速；否则就是同步其他玩家的野外竞速表现，只需要下载具就行了
		if (CS3PlayerEntityId == PlayerEntityId)
		{
			PlayerActor->OnOverOutsideCopyGame();
		}
		else
		{
			if (PlayerActor->RideCarrierComponent)
			{
				PlayerActor->RideCarrierComponent->DisRideOnCarrier();
			}
		}
	}
}

void URoleInterface::OnStartRoleAutoMove_Implementation(float InputYawScale)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor))
		PlayerActor->OnStartPlayerAutoMoveCopyGame(InputYawScale);
}

void URoleInterface::OnDisRoleAutoMove_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if(IsValid(PlayerActor))
		PlayerActor->OnOverPlayerAutoMoveCopyGame();
}

void URoleInterface::OnPlayerCameraRotation(float RotationTime)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (PlayerActor)
	{
		PlayerActor->OnPlayerCameraRotation(RotationTime);
	}	
}

void URoleInterface::OnSetClientTime_Implementation(const FString& diffTime, const int32& severIndex)
{
	UTimeManager *TimeManager = UUECS3GameInstance::Instance->TimeManager;
	TimeManager->SetDiffTime(diffTime, severIndex);
}

void URoleInterface::OnUpdateMoveType(int32 MoveType)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (PlayerActor)
	{
		PlayerActor->OtherPlayerMoveType = (CS3_MOVE_TYPE)MoveType;
	}
}

void URoleInterface::OnPlayVideo_Implementation(const FString& VideoID)
{
	UMediaPlayerManager* MediaPlayerManager = UUECS3GameInstance::Instance->MediaPlayerManager;
	if(IsValid(MediaPlayerManager))
		MediaPlayerManager->PlayMedia(VideoID);

}

void URoleInterface::CLIENT_BreakFalling_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (PlayerActor)
	{
		PlayerActor->BreakFalling();
	}
}

void URoleInterface::CLIENT_StartConstantFall_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());

	if (!PlayerActor || !PlayerActor->ActorIsPlayer())
	{
		return;
	}


	// 切换到降落模式
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController) && IsValid(PlayerController->GetAtkStateMar()))
	{
		PlayerController->GetAtkStateMar()->SwitchFallMode(true);
	}

	// 开始缓缓下落
	PlayerActor->SetBaseGravityScale(0.5f);
	PlayerActor->GetCharacterMovement()->Velocity.Z = 0.0f;
	PlayerActor->SetCharacterMoveCacheData();///缓存一下数据，后面结束下落时才再能设置回来

	TWeakObjectPtr<URoleInterface> ThisPtr(this);

	if (IsValid(UUECS3GameInstance::Instance))
	{
		ForceID = UUECS3GameInstance::Instance->ForceManager->AddForce(PlayerActor, 600.f, ELOCAL_FORCE_DIRE::FORWARD_DIRE);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DropHandle, FTimerDelegate::CreateLambda([ThisPtr]()
		{
			if (ThisPtr.IsValid())
			{
				URoleInterface* RoleInterface = ThisPtr.Get();
				APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(RoleInterface->GetActor());
				if (PlayerActor && !PlayerActor->GetCharacterMovement()->IsFalling())
				{
					RoleInterface->LandEndFalling(0.0f);
					if (IsValid(UUECS3GameInstance::Instance))
					{
						UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(RoleInterface->DropHandle);
					}
				}
			}
		}), 0.1f, true);
	}
}

void URoleInterface::CLIENT_EndConstantFall_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());

	if (!PlayerActor || !PlayerActor->ActorIsPlayer())
	{
		return;
	}
	// 恢复模式

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController) && IsValid(PlayerController->GetAtkStateMar()))
	{
		PlayerController->GetAtkStateMar()->SwitchFallMode(false);
	}

	// 结束下落
	const FCHARACTER_MOVE_CACHE_DATA& CharacterMoveData = PlayerActor->GetCharacterMoveCacheData();
	PlayerActor->SetGravityScale(CharacterMoveData.GravityScale);///还原重力系数

	UUECS3GameInstance::Instance->ForceManager->StopForces(PlayerActor, ForceID);
}

void URoleInterface::CLIENT_StartParachuteLand_Implementation()
{

}

void URoleInterface::CLIENT_EndParachuteLand_Implementation()
{

}

void URoleInterface::FirstEnterGameNotify_Implementation()
{
	if (UGolbalBPFunctionLibrary::GUIManager())
	{
		UGolbalBPFunctionLibrary::GUIManager()->OnRoleFirstEnterGame();
	}
}

void URoleInterface::onClientSetAoi(const FString& STRING_1)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::onClientSetAoi : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	this->GetEntity()->CellCall(TEXT("onClientSetAoi"), args);
}

void URoleInterface::onClientResetAoi()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::onClientResetAoi : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("onClientResetAoi"), args);
}

void URoleInterface::onPlayerUnderArea()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::onPlayerUnderArea : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("onPlayerUnderArea"), args);
}

void URoleInterface::LandEndFalling(float LastVelocitySize)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::endFalling : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(LastVelocitySize);
	this->GetEntity()->CellCall(TEXT("LandEndFalling"), args);
}

void URoleInterface::enterWaterArea()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::enterWaterArea : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("enterWaterArea"), args);

}

void URoleInterface::leaveWaterArea()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::leaveWaterArea : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("leaveWaterArea"), args);

}

void URoleInterface::enterMaterialArea(const FString& STRING_1)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::enterMaterialArea : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	this->GetEntity()->CellCall(TEXT("enterMaterialArea"), args);

}

void URoleInterface::leaveMaterialArea(const FString& STRING_1)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::leaveMaterialArea : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	this->GetEntity()->CellCall(TEXT("leaveMaterialArea"), args);

}

void URoleInterface::RequestPlayRandomAction()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::RequestPlayRandomAction : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("RequestPlayRandomAction"), args);

}

void URoleInterface::onLandMovingPlatform(const int32& OBJECT_ID_1)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::onLandMovingPlatform : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(OBJECT_ID_1);
	this->GetEntity()->CellCall(TEXT("onLandMovingPlatform"), args);

}

void URoleInterface::onDeviateMovingPlatform()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::onDeviateMovingPlatform : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("onDeviateMovingPlatform"), args);

}

void URoleInterface::setPositionFromClient(const FVector& POSITION_1)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::setPositionFromClient : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("setPositionFromClient"), args);

}

void URoleInterface::verifyClientTime(const int32& INT32_1)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::verifyClientTime : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(INT32_1);
	this->GetEntity()->CellCall(TEXT("verifyClientTime"), args);

}

void URoleInterface::updateMoveType(const int32& INT32_1)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleInterface::updateMoveType : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(INT32_1);
	this->GetEntity()->CellCall(TEXT("updateMoveType"), args);

}

void URoleInterface::RPC_ChangeFlySpaceEffect(const FString& STRING_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleSpaceInterface::RPC_RequestGoToSpace : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	this->GetEntity()->CellCall(TEXT("ChangeFlySpaceEffect"), args);
}

void URoleInterface::CLIENT_SetCopyGameWeapon_Implementation(int32 Type)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor))
	{
		PlayerActor->UpdateWeapontYXFXZ(YXFXZ_COPY_WEAPON_ENUM(Type));
	}
}

void URoleInterface::OnDodgeRotation_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor)&& PlayerActor->ActorIsPlayer())
	{
		PlayerActor->OnDodgeRotation();
	}
}

FORCEINLINE void URoleInterface::updateLHMJChanllengeRelation(const int32& entityID)
{
	ChallengeID_ = entityID;
	UpdateRelation();
}

void URoleInterface::InitBlueCB()
{
	ArrBlueFunc.Add("StartPlayStory");
	ArrBlueFunc.Add("StopStory");
	ArrBlueFunc.Add("PlayRandomAction");
	ArrBlueFunc.Add("ReTriggerNearTrap");
	ArrBlueFunc.Add("AddAxternalVelocity");
	ArrBlueFunc.Add("ChangeAxternalPercentage");
	ArrBlueFunc.Add("RemoveAxternalVelocity");
	ArrBlueFunc.Add("OnMountTalisman");
	ArrBlueFunc.Add("OnDismountTalisman");
	ArrBlueFunc.Add("OnSetBlendDir");
	ArrBlueFunc.Add("OnPlayerCameraRotation");
	ArrBlueFunc.Add("OnSetClientTime");
	ArrBlueFunc.Add("OnStartRoleAutoMove");
	ArrBlueFunc.Add("OnDisRoleAutoMove");
	ArrBlueFunc.Add("OnUpdataEffectData");
	ArrBlueFunc.Add("OnUpdateMoveType");
	ArrBlueFunc.Add("OnPlayVideo");
	ArrBlueFunc.Add("OnSetJumpData");
	ArrBlueFunc.Add("CLIENT_BreakFalling");
	ArrBlueFunc.Add("CLIENT_StartConstantFall");
	ArrBlueFunc.Add("CLIENT_EndConstantFall");
	ArrBlueFunc.Add("FirstEnterGameNotify");
	ArrBlueFunc.Add("CLIENT_SetCopyGameWeapon");
	ArrBlueFunc.Add("CLIENT_SetCopyGameWeapon");
	ArrBlueFunc.Add("OnSetPlayerAddGravityScale");
	ArrBlueFunc.Add("OnDodgeRotation");
	ArrBlueFunc.Add("CLIENT_StartParachuteLand");
	ArrBlueFunc.Add("CLIENT_EndParachuteLand");
	ArrBlueFunc.Add("CLIENT_OnRepYCJMDCopyState");
	ArrBlueFunc.Add("CLIENT_OnSetAimOffsetBlend");
	ArrBlueFunc.Add("CLIENT_OnRepYCJMDAimOffsetState");
	Supper::InitBlueCB();
}

CONTROL_COMPILE_OPTIMIZE_END
