// Fill out your copyright notice in the Description page of Project Settings.

#include "SkillInterface.h"
// UE4
#include "PhysicsEngine/PhysicsSettings.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Components/PoseableMeshComponent.h"
#include "Components/AudioComponent.h"
#include "Components/CapsuleComponent.h"
// 插件
#include "KBEngine.h"
#include "JsonFieldData.h"
#include "TransActorCapture.h"
//CS3数据
#include "GameData/ConstDataBP.h"
//CS3
#include "CS3Base/CS3Entity.h"
#include "CS3Base/GameObject.h"
#include "GameDevelop/CS3PlayerController.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Actor/Particle/EffectEmitter.h"
#include "Component/RoleFilterActorComponent.h"
#include "Component/Role/RideCarrierComponent.h"
#include "Component/FightComponent.h"
#include "Component/Role/JumpComponent.h"
#include "Manager/VisibleManager.h"
#include "Manager/AudioManager.h"
#include "Manager/BuffEntityVisibleManager.h"
#include "Manager/AtkStateMar.h"
#include "Manager/TimeManager.h"
#include "Manager/SkillManager.h"
#include "Manager/BuffManager.h"
#include "Manager/MessageManager.h"
#include "Manager/ParticleManager.h"
#include "Manager/QuickBarManager.h"
#include "GameObjectInterface.h"
#include "GameData/GameDefine.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
#include "Util/ConvertUtil.h"
#include "Util/CustomEffect/SkeletalAnimParticle.h"
#include "Manager/CustomTimerManager.h"
#include "Kismet/KismetMathLibrary.h"
#include "Role/RoleKitBagInterface.h"
#include "GameData/Item/ItemUse.h"
#include "Component/SpringArmComponentEX.h"
#include "Manager/TutorialManager.h"
#include "Role/RoleInterface.h"
#include "Interface/Monster/CSkillInterface.h"
#include "CollisionQueryParams.h"

CONTROL_COMPILE_OPTIMIZE_START
	
CS3_BEGIN_INTERFACE_METHOD_MAP(USkillInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(InitPassiveSkillBar, &USkillInterface::InitPassiveSkillBar, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(updatePassiveSkillBar, &USkillInterface::updatePassiveSkillBar, const FVariant&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(IntensifySkill, &USkillInterface::IntensifySkill, const int32&, const int32&, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CancelIntensifySkill, &USkillInterface::CancelIntensifySkill, const int32&, const int32&, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnCreateTrace, &USkillInterface::OnCreateTrace, const int32&, const FString&, const float&, const float&, const int32&, const int32&, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(OnFinishCreateTrace, &USkillInterface::OnFinishCreateTrace, const int32&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_SetForbidJumpSkillIDs, &USkillInterface::CLIENT_SetForbidJumpSkillIDs, const FString&)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(EnterToxicosis, &USkillInterface::EnterToxicosis)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(LeaveToxicosis, &USkillInterface::LeaveToxicosis)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(USkillInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(attrBuffsForClient, &USkillInterface::Set_attrBuffsForClient, KBEngine::FVariantArray)
CS3_END_INTERFACE_PROPERTY_MAP()
	
// 只是添加了调用比较频繁得函数
DECLARE_CYCLE_STAT(TEXT("AddBuff"), STAT_AddBuff, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("RemoveBuff"), STAT_RemoveBuff, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("OnAddBuff"), STAT_OnAddBuff, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("OnRemoveBuff"), STAT_OnRemoveBuff, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("PlayBuffEffect"), STAT_PlayBuffEffect, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("RealUseSkill"), STAT_RealUseSkill, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("CastSkillToTarget"), STAT_CastSkillToTarget, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("CastSkillToPosition"), STAT_CastSkillToPosition, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("BeHitPlayEffect"), STAT_BeHitPlayEffect, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("HoldEffectPlayEffect"), STAT_HoldEffectPlayEffect, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("ReceiveSkill"), STAT_ReceiveSkill, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("OnBeHitBackNew"), STAT_OnBeHitBackNew, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("OnEndHitBack"), STAT_OnEndHitBack, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("CLIENT_ControlledOnBeHitBack"), STAT_CLIENT_ControlledOnBeHitBack, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("CLIENT_ControlledEndHitBack"), STAT_CLIENT_ControlledEndHitBack, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("PlayModleHighlight"), STAT_PlayModleHighlight, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("Set_attrBuffsForClient"), STAT_Set_attrBuffsForClient, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("GetEntityBuffUIData"), STAT_GetEntityBuffUIData, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("OnRiseBegin"), STAT_OnRiseBegin, STATGROUP_USkillInterface);
DECLARE_CYCLE_STAT(TEXT("OnRiseEnd"), STAT_OnRiseEnd, STATGROUP_USkillInterface);

//初始化
bool Console_IsPromptSkillName = true;

USkillInterface::USkillInterface()
{
	m_CatchTargetID = 0;
	CurrentUsePosItemUID = "";
}

USkillInterface::~USkillInterface()
{

}
void USkillInterface::PostInitProperties()
{
	Super::PostInitProperties();
	if (UUECS3GameInstance::Instance)
	{
		FightAssist = NewObject<UFightAssist>();
		//AtkStateCtrl = NewObject<UAtkStateCtrl>();
	}
}

void USkillInterface::onEnterWorld()
{
	AServerCharacter* ServerActor = Cast<AServerCharacter>(GetActor());
	if (IsValid(ServerActor))
	{
		m_BeforUpForceMoveMode = ServerActor->GetCharacterMovement()->MovementMode;
	}
	if (GetEntity() && GetEntity()->IsPlayer() && IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillManager))
	{
		UUECS3GameInstance::Instance->SkillManager->onEnterWorld();
	}
	Super::onEnterWorld();
}

void USkillInterface::onLeaveWorld()
{
	CancelSkillAssistUi(); //需要销毁组件
	if (GetEntity() && GetEntity()->IsPlayer() && IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillManager))
	{
		UUECS3GameInstance::Instance->SkillManager->onLeaveWorld();
	}

	if (UseSkillForTargetDelegate.IsBound())
	{
		UseSkillForTargetDelegate.Clear();
	}

	Super::onLeaveWorld();
}

void USkillInterface::InitSkills_Implementation(const TArray<int32>& SkillIDs)
{
	if (!IsValid(UUECS3GameInstance::Instance) || !IsValid(UUECS3GameInstance::Instance->SkillManager))
	{
		return;
	}
	for (int32 SkillId : SkillIDs)
	{
		UUECS3GameInstance::Instance->SkillManager->UpdateSelfSkillData(SkillId, true);
	}
	UUECS3GameInstance::Instance->SkillManager->InitSkillTreeData();
	UUECS3GameInstance::Instance->SkillManager->InitSkillPassiveListData();
	UUECS3GameInstance::Instance->SkillManager->InitChuanChengSkillTreeTableDatas();
}

void USkillInterface::OnActorCreaterFinish()
{
	//actor创建好后向服务器请求buff
	TArray<FString> args;
	UGolbalBPFunctionLibrary::CellCall(EntityID, TEXT("skill_onClientActorCreate"), args);
	UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), EntityID));
	if (IsValid(CSkillInterface))
	{
		CSkillInterface->CSkill_onClientActorCreate();
	}
}

void USkillInterface::OnAddSkill_Implementation(const int32& SkillID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillManager))
	{
		UUECS3GameInstance::Instance->SkillManager->UpdateSelfSkillData(SkillID, true);
		this->UpdateSkillList(SkillID, true);
	}
}

void USkillInterface::OnRemoveSkill_Implementation(const int32& SkillID)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillManager))
	{
		UUECS3GameInstance::Instance->SkillManager->UpdateSelfSkillData(SkillID, false);
		this->UpdateSkillList(SkillID, false);
	}
}

void USkillInterface::OnPlayerLevelChange()
{
	USkillManager* SkillManager = UUECS3GameInstance::Instance->SkillManager;
	TArray<int32>PlayerSkillIDList = SkillManager->GetPlayerSkillIdList();
	int32 index = 1;
	for (auto skillID: PlayerSkillIDList)
	{
		int32 nextSkillID = SkillManager->GetSkillLearnDataById(skillID).NextLevelID;
		if (SkillManager->CheckUpgradeCondition(skillID))
		{
			UGolbalBPFunctionLibrary::TutorialManager()->OnSkillCanUpgrate(nextSkillID, index++);
		}
	}
}

void USkillInterface::AddBuff( const BuffDataType& buffData)
{
	SCOPE_CYCLE_COUNTER(STAT_AddBuff);

	if (!IsValid(UUECS3GameInstance::Instance) || !IsValid(UUECS3GameInstance::Instance->BuffManager))
	{
		return;
	}
	int32 buffIdx = buffData.index;
	if (AttrBuffs.Contains(buffIdx))
		RemoveBuff(buffIdx);

	AttrBuffs.Add(buffIdx, buffData);

	TWeakObjectPtr<USkillInterface> DelayThisPtr(this);
	UUECS3GameInstance::Instance->BuffManager->AsyncLoadBuffAsset(FStreamableDelegate::CreateLambda([DelayThisPtr, buffIdx ]()
	{
		if (DelayThisPtr.IsValid())
		{
			USkillInterface* DelayThis = DelayThisPtr.Get();
			DelayThis->OnAddBuff(buffIdx);
		}
	}), buffIdx);
}

void USkillInterface::OnAddBuff(int32 buffIdx)
{
	SCOPE_CYCLE_COUNTER(STAT_OnAddBuff);
	if (!IsValid(UUECS3GameInstance::Instance))
		return;

	if (!IsValid(UUECS3GameInstance::Instance->BuffManager))
		return;

	if (!AttrBuffs.Contains(buffIdx)) return; 
	BuffDataType newBuff = AttrBuffs[buffIdx];
	UTimeManager *TimeManager = UUECS3GameInstance::Instance->TimeManager;
	float BuffTime = (newBuff.endTime - TimeManager->GetMultipleClientTime()) / (float)TIME_ENLARGE_MULTIPLE;
	FBuffUIData UIData = UUECS3GameInstance::Instance->BuffManager->CreateBuffUIData(newBuff.index, newBuff.buffID, newBuff.holdTime, BuffTime, newBuff.layer);
	OnAddBuffBP(UIData);
	if (!IsValid(UUECS3GameInstance::Instance->BuffEntityVisibleManager))
		return;
	if (auto _entity = GetEntity())
	{
		if (_entity && _entity->IsPlayer())
		{
			UUECS3GameInstance::Instance->BuffEntityVisibleManager->OnAddBuff(newBuff.buffID);
			//新手指引
			if (IsValid(UUECS3GameInstance::Instance->TutorialManager))
			{
				UUECS3GameInstance::Instance->TutorialManager->OnAddBuff(newBuff.buffID);
			}
		}
	}
	
}

void USkillInterface::RemoveBuff(int32 BuffIndex)
{
	SCOPE_CYCLE_COUNTER(STAT_RemoveBuff);
	if (BuffIndex != -1)
	{
		if (!AttrBuffs.Contains(BuffIndex)) return;
		int32 BuffID = AttrBuffs[BuffIndex].buffID;
		FString BuffScript = AttrBuffs[BuffIndex].className;
		AttrBuffs.Remove(BuffIndex);
		OnRemoveBuff(BuffIndex, BuffID, BuffScript);
	}
	else
	{
		TMap<int32, BuffDataType> tempAttrBuffs = AttrBuffs;
		AttrBuffs.Reset();
		for (auto it = tempAttrBuffs.CreateIterator(); it; ++it)
		{
			OnRemoveBuff(it.Value().index, it.Value().buffID, it.Value().className );
		}
	}
}

void USkillInterface::OnRemoveBuff( int32 BuffIndex, int32 BuffID, FString BuffScript)
{
	SCOPE_CYCLE_COUNTER(STAT_OnRemoveBuff);

	if (auto _entity = GetEntity())
	{
		if (_entity && _entity->IsPlayer() && UUECS3GameInstance::Instance)
		{
			UUECS3GameInstance::Instance->BuffEntityVisibleManager->OnRemoveBuff(BuffID);
		}
	}

	if (GetEntity() == nullptr)
		return;

	OnRemoveBuffBP(BuffIndex);
}

void USkillInterface::PlayBuffEffect_Implementation(const int32 BuffIndex, const int32 CasterID, const int32& ContinuousId, const TArray<FString>& ActionID, const TArray<FString>& BeginTime, const FString & EffectID, const FString & SoundID)
{
	SCOPE_CYCLE_COUNTER(STAT_PlayBuffEffect);

	if (GetActor() == nullptr) 
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::PlayBuffEffect_Implementation : GetActor()!"));
		return;
	}
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::PlayBuffEffect_Implementation : GetEntity()!"));
		return;
	}
	AServerCharacter* ServerActor = Cast<AServerCharacter>(GetActor());

	TArray<float> ActionStartTimes;
	TArray<FName> ActionIds;
	for (int i = 0; i < ActionID.Num();i++)
	{
		if (ActionID[i] != "")
		{
			ActionIds.Add(FSTRING_TO_FNAME(ActionID[i]));
			ActionStartTimes.Add(FSTRING_TO_FLOAT(BeginTime[i]));
		}
		else
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("-----USkillInterface::PlayBuffEffect[EntityId=%d, ActionID = %s"),
				this->GetEntity()->ID(), *ActionID[i]);
		}
	}
	if (ActionIds.Num())
	{
		ServerActor->PlayContinuousActions(ContinuousId, ActionIds, ActionStartTimes);
	}

	if (EffectID != "")
	{
		AActor* CasterActor = UGolbalBPFunctionLibrary::GetActorByID(CasterID);
		if (IsValid(CasterActor))
		{
			TArray<FString>EffectIdList = UGolbalBPFunctionLibrary::SplitString(EffectID, false, TEXT("|"));
			for (auto effectId : EffectIdList)
			{
				UUECS3GameInstance::Instance->ParticleManager->PlayParticle(effectId, 0.0f, CasterActor, GetActor());
			}
		}
	}

	if (SoundID != "" && ServerActor->IsShowEffect(SignificanceType::Near))
	{
		TArray<FString>SoundIDList = UGolbalBPFunctionLibrary::SplitString(SoundID, false, TEXT("|"));
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->AudioManager))
		{
			for (auto SoundId : SoundIDList)
			{
				UUECS3GameInstance::Instance->AudioManager->AsyncPlay3DSound(ServerActor, SoundId);
			}
		}
	}
}

TArray<int32> USkillInterface::findBuffsByBuffScript(FString BuffScript)
{
	TArray<int32> IndexList;
	for (auto i = AttrBuffs.CreateIterator(); i; ++i)
	{
		if (BuffScript == i.Value().className)
		{
			IndexList.Add(i.Key());
		}
	}
	return IndexList;
}

TArray<int32> USkillInterface::findBuffsByBuffID(const int32& BuffID)
{
	TArray<int32> IndexList;
	for (auto i = AttrBuffs.CreateIterator(); i; ++i)
	{
		if (BuffID == i.Value().buffID)
		{
			IndexList.Add(i.Key());
		}
	}
	return IndexList;
}


bool USkillInterface::HasBuffByID(const int32& BuffID)
{
	if (findBuffsByBuffID(BuffID).Num() > 0)
	{
		return true;
	}
	else
	{
		return false;
	}
}

TMap<int32, BuffDataType> USkillInterface::getAttrBuffs()
{
	return AttrBuffs;
}

bool USkillInterface::HasBuffByIndex(const int32& BuffIndex)
{
	return AttrBuffs.Contains(BuffIndex);
}

void USkillInterface::UseSkill(int32 SkillID, int32 TargetID)
{
	FUseSkillForTargetDelegate NullDelegate;
	RealUseSkill(SkillID, TargetID, NullDelegate);
}

void USkillInterface::RealUseSkill(int32 SkillID, int32 TargetID, FUseSkillForTargetDelegate& OnUseSkill)
{
	SCOPE_CYCLE_COUNTER(STAT_RealUseSkill);

	CS3_Display(CS3DebugType::CL_Undefined, TEXT("-----USkillInterface::UseSkill[SkillID = %d, TargetID = %d]-----"), SkillID, TargetID);
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::RealUseSkill : GetEntity()!"));
		return;
	}
	CS3Entity* AtkEntity = static_cast<CS3Entity*>(this->GetEntity());
	CS3Entity* BeAtkEntity = TargetID == 0 ? nullptr : static_cast<CS3Entity*>(UUECS3GameInstance::Instance->pKBEApp->FindEntity(TargetID));
	bool IsPassConditional = FightAssist->CheckSkillUseCondition(AtkEntity, BeAtkEntity, SkillID);


	if (!IsPassConditional)
	{
		if (OnUseSkill.IsBound() && BeAtkEntity)
		{
			OnUseSkill.ExecuteIfBound(BeAtkEntity->ID(), SkillID, false);
			OnUseSkill.Clear();
		}
	}
	if (OnUseSkill.IsBound())
	{
		UseSkillForTargetDelegate = OnUseSkill;
	}

	if (IsPassConditional)
	{
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillManager))
		{
			USkillData* SkillData = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(SkillID);
			if (!IsValid(SkillData))
			{
				CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::RealUseSkill : SkillData!"));
				return;
			}
			CancelSkillAssistUi(); //中断施法辅助

			if (SkillData->GetSkillType() == ENUM_SKILL_CLASS_TYPE::CombatSkillClient
				|| SkillData->GetSkillType() == ENUM_SKILL_CLASS_TYPE::InstantSkillClient || SkillData->GetSkillType() == ENUM_SKILL_CLASS_TYPE::SkillClientCharge
				|| SkillData->GetSkillType() == ENUM_SKILL_CLASS_TYPE::SkillClientJump || SkillData->GetSkillType() == ENUM_SKILL_CLASS_TYPE::SkillClientSing)
			{
				UCSkillInterface *CSkillInterface = Cast<UCSkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("CSkillInterface"), GetEntity()->ID()));
				if (!IsValid(CSkillInterface))
				{
					return;
					
				}
				if (SkillData->GetTargetType() == ENUM_CAST_TARGET_TYPE::TargetPosition && BeAtkEntity && BeAtkEntity->Actor())
				{
					FVector targetLocation = BeAtkEntity->Actor()->GetActorLocation();
					CSkillInterface->RequestUseCSkillToPosition(SkillID, targetLocation);
				}
				else
				{
					CSkillInterface->RequestUseCSkillToEntity(SkillID, TargetID);
				}
				return;
			}
			if (SkillData->GetTargetType() == ENUM_CAST_TARGET_TYPE::TargetPosition && BeAtkEntity && BeAtkEntity->Actor())
			{
				const FVector targetLocation = BeAtkEntity->Actor()->GetActorLocation();
				UsePostionSkill(SkillID, targetLocation);
			}
			else
			{
				KBEngine::FVariantArray args;
				args.Add(SkillID);
				args.Add(TargetID);
				this->GetEntity()->CellCall(TEXT("useSkillToEntityFC"), args);
			}
		}
	}
}

bool USkillInterface::CheckAutoUseSkill(int32 SkillID, int32 TargetID, bool BShowMsg)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::CheckAutoUseSkill : GetEntity()!"));;
		return false;
	}
	CS3Entity* AtkEntity = static_cast<CS3Entity*>(this->GetEntity());
	CS3Entity* BeAtkEntity = TargetID == 0 ? nullptr : static_cast<CS3Entity*>(UUECS3GameInstance::Instance->pKBEApp->FindEntity(TargetID));
	if (AtkEntity == nullptr || BeAtkEntity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::CheckAutoUseSkill : AtkEntity||BeAtkEntity!"));
		return false;
	}
	return FightAssist->CheckAutoUseSkill(AtkEntity, BeAtkEntity, SkillID, BShowMsg);
}

bool USkillInterface::CheckAutoUseItem(int32 ItemID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::CheckAutoUseItem : GetEntity()!"));
		return false;
	}
	AServerCharacter* AtkCharacter = Cast<AServerCharacter>(this->GetActor());
	
	if (!IsValid(AtkCharacter) )
	{
		return false;
	}
	return FightAssist->CheckAutoUseItem(AtkCharacter, ItemID);
}

void USkillInterface::UsePostionSkill(const int32&  SkillID, const FVector& TargetPostion)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("-----USkillInterface::UsePostionSkill[SkillID = %d, PosX = %f, PosX = %f, PosX = %f]-----"), TargetPostion.X, TargetPostion.Y, TargetPostion.Z);
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::UsePostionSkill : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(SkillID);
	args.Add(TargetPostion);
	this->GetEntity()->CellCall(TEXT("useSkillToPositionFC"), args);
}

void USkillInterface::CLIENT_SetForbidJumpSkillIDs(const FString& SkillIDs)
{
	TArray<FString> TempSplitArray = UGolbalBPFunctionLibrary::SplitString(SkillIDs, false, TEXT("|"));
	TArray<int32> TempSkillIDs;
	for (auto ID: TempSplitArray)
	{
		TempSkillIDs.Add(FSTRING_TO_INT(ID));
	}
	UUECS3GameInstance::Instance->SkillManager->SetForbidJumpSkillIDs(TempSkillIDs);
}

void USkillInterface::SetCastingSkill(const int32& SkillID)
{
	CastingSkill = SkillID;

	if (0 == CastingSkill)
	{
		if (UseSkillForTargetDelegate.IsBound())
		{
			UseSkillForTargetDelegate.ExecuteIfBound(UGolbalBPFunctionLibrary::GetTargetEntityID(), SkillID, true);
			UseSkillForTargetDelegate.Clear();
		}
	}
}

bool USkillInterface::IsCastingSkill()
{
	return CastingSkill != 0;
}


void USkillInterface::SkillInterrupted_Implementation(int32 SkillID, int32 Reason, const int32& actionIndex)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("-----USkillInterface::SkillInterrupted[SkillID = %d]-----"), SkillID);
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::SkillInterrupted_Implementation : GetEntity()!"));
		return;
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillManager))
	{
		USkillData* SkillData = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(SkillID);
		if (IsValid(SkillData))
		{
			CS3Entity* AtkEntity = (CS3Entity *)(this->GetEntity());
			AServerCharacter* AtkActor = Cast<AServerCharacter>(AtkEntity->Actor());
			AtkActor->StopContinuousAction(actionIndex);
			///中止播放光效
			for (auto EffectUID : SkillEffectUIDList)
			{
				UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(EffectUID, true, true, false);
				/*if (IsValid(Effect))
				{
					Effect->Stop();
				}*/
			}
			SkillEffectUIDList.Empty();
			///中止播放音效	
			if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->AudioManager))
			{
				if (AudioComponents.Contains(SkillID) && AudioComponents[SkillID])
				{
					UUECS3GameInstance::Instance->AudioManager->Stop3DSound(AudioComponents[SkillID]);
				}
				if (TargetAudioComponents.Contains(SkillID) && TargetAudioComponents[SkillID])
				{
					UUECS3GameInstance::Instance->AudioManager->Stop3DSound(TargetAudioComponents[SkillID]);
				}
			}
		}
	}
}

void USkillInterface::CastSkillToTarget_Implementation(int32& SkillID, const uint8& isInstantSkill, 
	const int32& TargetID, const TArray<FString>& ActionID, const TArray<FString>& BeginTime, 
	const int32& ContinuousId, const int32& CasterID)
{
	StartCastSkillToTarget(SkillID, isInstantSkill, TargetID, ActionID, BeginTime, ContinuousId, CasterID);
}

void USkillInterface::CastSkillToPosition_Implementation(int32& SkillID,const uint8& isInstantSkill, const float& PosX, const float& PosY, const float& PosZ, const TArray<FString>& ActionID, const TArray<FString>& BeginTime, const int32& ContinuousId, const int32& CasterID)
{
	StartCastSkillToPosition(SkillID, isInstantSkill, PosX, PosY, PosZ, ActionID, BeginTime, ContinuousId, CasterID);
}

void USkillInterface::StartCastSkillToTarget(int32& SkillID, const uint8& isInstantSkill,
	const int32& TargetID, const TArray<FString>& ActionID, const TArray<FString>& BeginTime,
	const int32& ContinuousId, const int32& CasterID, const int32& ProxyID/* = -1*/)
{
	SCOPE_CYCLE_COUNTER(STAT_CastSkillToTarget);

	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::CastSkillToTarget_Implementation : GetEntity()!"));
		return;
	}
	CS3Entity* AtkEntity = (CS3Entity *)(this->GetEntity());
	INT32 Eid = AtkEntity->ID();
	TWeakObjectPtr<USkillInterface> ThisPtr(this);
	auto ExcetPlaySkill = [ThisPtr, Eid, SkillID, CasterID, isInstantSkill, TargetID, ActionID, BeginTime, ContinuousId, ProxyID]()
	{
		Entity* AtkEntity = UGolbalBPFunctionLibrary::FindEntity(Eid);
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillManager))
		{
			USkillData* SkillData = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(SkillID);
			if (ThisPtr.IsValid())
			{
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("-----USkillInterface::CastSkillToTarget[EntityId = %d, SkillData=%d,  SkillID=%d,   TargetID=%d]-----"), ThisPtr.Get()->GetEntity()->ID(), SkillData ? 1 : 0, SkillID, TargetID);
			}
			if (IsValid(SkillData) && AtkEntity != nullptr)
			{
				AServerCharacter* AtkActor = Cast<AServerCharacter>(AtkEntity->Actor());
				if (!IsValid(AtkActor))return;

				AServerCharacter* BeAtkActor = nullptr;
				KBEngine::Entity* BeAtkEntity = UGolbalBPFunctionLibrary::FindEntity(TargetID);
				if (nullptr != BeAtkEntity)
				{
					BeAtkActor = Cast<AServerCharacter>(((CS3Entity *)BeAtkEntity)->Actor());
				}
				const FSKILL_USE_RESULT CasterResult = SkillData->GetCasterResult();
				bool IsPromptSkillName = Console_IsPromptSkillName && CasterResult.IsPromptSkillName;
				if (AtkEntity->IsPlayer() && IsValid(AtkActor->GetFightComponent()))
				{
					AtkActor->GetFightComponent()->OnCastSkill.Broadcast(CasterResult.SkillName, IsPromptSkillName);
				}
				if (IsValid(AtkActor->GetFightComponent()) && AtkActor->GetFightComponent()->OnBeCastSkill.IsBound())
				{
					AtkActor->GetFightComponent()->OnBeCastSkill.Broadcast(CasterResult.SkillName, IsPromptSkillName, TargetID);
				}
				//FActionOverDelegate Delegate;
				//Delegate.AddUObject(this, &USkillInterface::CallBackCeSHi);
				///动作
				TArray<float> ActionStartTimes;
				TArray<FName> ActionIds;
				for (int i = 0; i < ActionID.Num(); i++)
				{
					if (ActionID[i] != "")
					{
						ActionIds.Add(FSTRING_TO_FNAME(ActionID[i]));
						ActionStartTimes.Add(FSTRING_TO_FLOAT(BeginTime[i]));
					}
					else
					{
						if (ThisPtr.IsValid())
						{
							CS3_Display(CS3DebugType::CL_Undefined, TEXT("-----USkillInterface::CastSkillToTarget[EntityId=%d, ActionID = %s"),
								ThisPtr.Get()->GetEntity()->ID(), *ActionID[i]);
						}
					}
				}
				if (ActionIds.Num())
				{
					AtkActor->PlayContinuousActions(ContinuousId, ActionIds, ActionStartTimes);

				}
				if (isInstantSkill == 0)	///不是瞬发技能才播动作
				{
					if (ThisPtr.IsValid())
					{
						ThisPtr.Get()->SkillEffectUIDList.Empty();
					}
				}
				///播施法光效
				TArray<FString>EffectIdList = UGolbalBPFunctionLibrary::SplitString(CasterResult.CasterCastEffectId, false, TEXT("|"));
				for (auto EffectId : EffectIdList)
				{
					///对自己播施法光效
					int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectId, 0.0f, AtkActor, AtkActor, FEffectCreate::CreateLambda([ProxyID](int32 UID)
					{
						AActor* Effect = UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID);
						if (Effect)
						{
							Cast<AEffectEmitter>(Effect)->SetEmitterCollisionData(ProxyID);
						}
					}));
					if (ThisPtr.IsValid())
					{
						ThisPtr.Get()->SkillEffectUIDList.Add(EffectUID);
					}
				}
				TArray<FString>TargetEffectIdList = UGolbalBPFunctionLibrary::SplitString(CasterResult.TargetCastEffectId, false, TEXT("|"));
				for (auto TargetEffectId : TargetEffectIdList)
				{
					///播目标投递光效
					int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(TargetEffectId, 0.0f, AtkActor, BeAtkActor, FEffectCreate::CreateLambda([ProxyID](int32 UID)
					{
						AActor* Effect = UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID);
						if (Effect)
						{
							Cast<AEffectEmitter>(Effect)->SetEmitterCollisionData(ProxyID);
						}
					}));
					if (ThisPtr.IsValid())
					{
						ThisPtr.Get()->SkillEffectUIDList.Add(EffectUID);
					}
				}
				///技能释放音效
				if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->AudioManager))
				{
					if (AtkActor->IsShowEffect(SignificanceType::Near))
					{
						TArray<FString>SoundIdList = UGolbalBPFunctionLibrary::SplitString(CasterResult.CasterCastSoundId, false, TEXT("|"));
						for (auto SoundId : SoundIdList)
						{
							UCS3AudioComponent* AudioComponent = UUECS3GameInstance::Instance->AudioManager->AsyncPlay3DSound(AtkActor, SoundId, FVector::ZeroVector, EAUDIOCOMPTYLE::SKILL);
							ThisPtr.Get()->AudioComponents.Add(SkillID, AudioComponent);
						}
					}

					if (IsValid(BeAtkActor) && BeAtkActor->IsShowEffect(SignificanceType::Near))
					{
						TArray<FString>TargetSoundIdList = UGolbalBPFunctionLibrary::SplitString(CasterResult.TargetCastSoundId, false, TEXT("|"));
						for (auto SoundId : TargetSoundIdList)
						{
							UCS3AudioComponent* AudioComponent = UUECS3GameInstance::Instance->AudioManager->AsyncPlay3DSound(BeAtkActor, SoundId, FVector::ZeroVector, EAUDIOCOMPTYLE::SKILL);
							ThisPtr.Get()->TargetAudioComponents.Add(SkillID, AudioComponent);
						}
					}
				}
#if WITH_EDITOR
				APlayerCharacter* player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
				AActor* Target = UGolbalBPFunctionLibrary::GetActorByID(TargetID);
				if (IsValid(player))
				{
					player->OnScopeActor(SkillID, Target, CasterID);
				}
#endif
			}
		}
	};

	//骑乘状态下放技能，需要先下马，再放技能
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(AtkEntity->Actor());
	if (IsValid(PlayerCharacter) && PlayerCharacter->IsDisCarrierState())
	{
		PlayerCharacter->OnDisRideOnPetOver = FDisRideOnPetOverDelegate::CreateLambda(
			[ThisPtr, Eid, SkillID, isInstantSkill, TargetID, ActionID, BeginTime, ContinuousId, ExcetPlaySkill]()
		{
			Entity* AtkEntity = UGolbalBPFunctionLibrary::FindEntity(Eid);

			ExcetPlaySkill();

			if (AtkEntity != nullptr)
			{
				APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(AtkEntity->Actor());
				if (IsValid(PlayerCharacter))
				{
					PlayerCharacter->OnDisRideOnPetOver = nullptr;
				}
			}
		});
	}
	else
	{

		ExcetPlaySkill();
	}

	//USkillInterface::RealUseSkill函数得技能使用回调
	if (AtkEntity->IsPlayer() && isInstantSkill)
	{
		if (UseSkillForTargetDelegate.IsBound())
		{
			UseSkillForTargetDelegate.ExecuteIfBound(UGolbalBPFunctionLibrary::GetTargetEntityID(), SkillID, true);
			UseSkillForTargetDelegate.Clear();
		}
	}

	if (GetEntity()->IsPlayer())
	{
		//播放技能
		UGolbalBPFunctionLibrary::TutorialManager()->OnPlaySkill(SkillID);
		UGolbalBPFunctionLibrary::QuickBarManager()->OnPlaySkill(SkillID);
	}
}

void USkillInterface::StartCastSkillToPosition(int32& SkillID, const uint8& isInstantSkill, const float& PosX, const float& PosY, const float& PosZ, const TArray<FString>& ActionID, const TArray<FString>& BeginTime, const int32& ContinuousId, const int32& CasterID, const int32& ProxyID/* = -1*/)
{
	SCOPE_CYCLE_COUNTER(STAT_CastSkillToPosition);

	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::CastSkillToPosition_Implementation : GetEntity()!"));
		return;
	}
	CS3Entity* AtkEntity = (CS3Entity *)(this->GetEntity());
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillManager))
	{
		USkillData* SkillData = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(SkillID);
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("-----USkillInterface::CastSkillToPosition[EntityId=%d, SkillID = %d, PosX = %f, PosX = %f, PosX = %f, SkillData=%d]-----"), this->GetEntity()->ID(), SkillID, PosX, PosY, PosZ, SkillData ? 1 : 0);
		if (IsValid(SkillData))
		{
			AServerCharacter* AtkActor = Cast<AServerCharacter>(AtkEntity->Actor());
			const FSKILL_USE_RESULT CasterResult = SkillData->GetCasterResult();
			if (AtkEntity->IsPlayer())
			{
				AtkActor->GetFightComponent()->OnCastSkill.Broadcast(CasterResult.SkillName, CasterResult.IsPromptSkillName);
			}

			///动作
			TArray<float> ActionStartTimes;
			TArray<FName> ActionIds;
			for (int i = 0; i < ActionID.Num(); i++)
			{
				if (ActionID[i] != "")
				{
					ActionIds.Add(FSTRING_TO_FNAME(ActionID[i]));
					ActionStartTimes.Add(FSTRING_TO_FLOAT(BeginTime[i]));
				}
				else
				{
					CS3_Display(CS3DebugType::CL_Undefined, TEXT("-----USkillInterface::CastSkillToPosition[EntityId=%d, ActionID = %s"),
						this->GetEntity()->ID(), *ActionID[i]);
				}
			}
			if (ActionIds.Num())
			{
				AtkActor->PlayContinuousActions(ContinuousId, ActionIds, ActionStartTimes);
			}
			if (isInstantSkill == 0)	///不是瞬发技能才播动作
			{
				SkillEffectUIDList.Empty();
			}
			///播施法光效
			TArray<FString>EffectIdList = UGolbalBPFunctionLibrary::SplitString(CasterResult.CasterCastEffectId, false, TEXT("|"));
			for (auto EffectId : EffectIdList)
			{
				///对自己播施法光效
				int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(CasterResult.CasterCastEffectId, 0.0f, AtkActor, AtkActor, FEffectCreate::CreateLambda([ProxyID](int32 UID)
				{
					AActor* Effect = UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID);
					if (Effect)
					{
						Cast<AEffectEmitter>(Effect)->SetEmitterCollisionData(ProxyID);
					}
				}));
				SkillEffectUIDList.Add(EffectUID);
			}
			UClass *actor = UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("TargetActor"));
			AActor* TargetActor = UGolbalBPFunctionLibrary::SpawnActor<AActor>(actor);
			if (FVector(PosX, PosY, PosZ) != FVector::ZeroVector)
			{
				TargetActor->SetActorLocation(FVector(PosX, PosY, PosZ));
			}
			else
			{
				TargetActor->SetActorLocation(FVector::ZeroVector);
			}

			TArray<FString>TargetEffectIdList = UGolbalBPFunctionLibrary::SplitString(CasterResult.TargetCastEffectId, false, TEXT("|"));
			for (auto TargetEffectId : TargetEffectIdList)
			{
				int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(TargetEffectId, 0.0f, UGolbalBPFunctionLibrary::GetActorByID(CasterID), TargetActor, FEffectCreate::CreateLambda([PosX, PosY, PosZ, CasterID, ProxyID](int32 UID)
				{
					AActor* Effect = UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID);
					if (Effect)
					{
						Cast<AEffectEmitter>(Effect)->SetEmitterCollisionData(ProxyID);
					}
					if (FVector(PosX, PosY, PosZ) == FVector::ZeroVector)
					{
						return;
					}
				}));
				SkillEffectUIDList.Add(EffectUID);
			}
			///技能释放音效
			if (AtkActor->IsShowEffect(SignificanceType::Near))
			{
				TArray<FString>SoundIdList = UGolbalBPFunctionLibrary::SplitString(CasterResult.CasterCastSoundId, false, TEXT("|"));
				if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->AudioManager))
				{
					for (auto SoundId : SoundIdList)
					{
						UUECS3GameInstance::Instance->AudioManager->AsyncPlay3DSound(AtkActor, SoundId, FVector::ZeroVector, EAUDIOCOMPTYLE::SKILL);
					}
				}
			}

			//USkillInterface::RealUseSkill函数得技能使用回调
			if (AtkEntity->IsPlayer() && isInstantSkill)
			{
				if (UseSkillForTargetDelegate.IsBound())
				{
					UseSkillForTargetDelegate.ExecuteIfBound(UGolbalBPFunctionLibrary::GetTargetEntityID(), SkillID, true);
					UseSkillForTargetDelegate.Clear();
				}
			}

			//CST-6177 - 程序功能需求（0级）--研究实现一种直观显示技能作用目标和范围的调试方法
#if WITH_EDITOR
			APlayerCharacter* player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
			player->OnScopeLocation(SkillID, FVector(PosX, PosY, PosZ), CasterID);
#endif
		}
	}

	if (GetEntity()->IsPlayer())
	{
		//播放技能
		UGolbalBPFunctionLibrary::TutorialManager()->OnPlaySkill(SkillID);
		UGolbalBPFunctionLibrary::QuickBarManager()->OnPlaySkill(SkillID);
	}
}

void USkillInterface::CastCSkillToTarget_Implementation(int32&  SkillID, const uint8& isInstantSkill, const int32&  TargetID,
	const TArray<FString>& ActionID, const TArray<FString>& BeginTime, const int32& ContinuousId, const int32& CasterID, const int32& ProxyID)
{
	StartCastSkillToTarget(SkillID, isInstantSkill, TargetID, ActionID, BeginTime, ContinuousId, CasterID, ProxyID);
}

void USkillInterface::CastCSkillToPosition_Implementation(int32&  SkillID, const uint8& isInstantSkill, const float& PosX, const float& PosY,
	const float&  PosZ, const TArray<FString>& ActionID, const TArray<FString>& BeginTime,
	const int32& ContinuousId, const int32& CasterID, const int32& ProxyID)
{
	StartCastSkillToPosition(SkillID, isInstantSkill, PosX, PosY, PosZ, ActionID, BeginTime, ContinuousId, CasterID, ProxyID);
}

void USkillInterface::BeHitPlayEffect_Implementation(int32 const& CasterID, int32 const& TargetID, const int32& ContinuousId, const TArray<FString>& ActionID, const FString& EffectID, const FString& SoundID, const TArray<FString>& BeginTime)
{
	SCOPE_CYCLE_COUNTER(STAT_BeHitPlayEffect);

	KBEngine::Entity* AtkEntity = UGolbalBPFunctionLibrary::FindEntity(CasterID);
	KBEngine::Entity* BeAtkEntity = UGolbalBPFunctionLibrary::FindEntity(TargetID);

	if (GetEntity() == nullptr || AtkEntity == nullptr || BeAtkEntity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error: GetEntity() == nullptr && AtkEntity == nullptr && BeAtkEntity == nullptr!"));
		return;
	}
	AServerCharacter* AtkActor = Cast<AServerCharacter>(((CS3Entity*)AtkEntity)->Actor());
	AServerCharacter* BeAtkActor = Cast<AServerCharacter>(((CS3Entity*)BeAtkEntity)->Actor());

	if (!IsValid(AtkActor) || !IsValid(BeAtkActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error: !IsValid(AtkActor) && !IsValid(BeAtkActor)!"));
		return;
	}

	// 这里的优化暂时关闭,因为有一些类似替身术的技能,没有包围盒,导致BeAtkActor重要度是最低的,就没效果了
	//if (!BeAtkActor->IsShowEffect(SignificanceType::Complete)) //受击效果不太明显,所以只在SignificanceType::Complete时显示
	//{
	//	return;
	//}

	TArray<float> ActionStartTimes;
	TArray<FName> ActionIds;
	for (int i = 0; i < ActionID.Num();i++)
	{
		if (ActionID[i] != "")
		{
			ActionIds.Add(FSTRING_TO_FNAME(ActionID[i]));
			ActionStartTimes.Add(FSTRING_TO_FLOAT(BeginTime[i]));
		}
		else
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("-----USkillInterface::BeHitPlayEffect[EntityId=%d, ActionID = %s"),
				this->GetEntity()->ID(), *ActionID[i]);
		}
	}
	if (ActionIds.Num()>0)
	{
		BeAtkActor->PlayContinuousActions(ContinuousId, ActionIds, ActionStartTimes);
	}
	
	///受击播放光效
	TArray<FString>EffectIdList = UGolbalBPFunctionLibrary::SplitString(EffectID, false, TEXT("|"));
	for (auto EffectId : EffectIdList )
	{
		UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectId, 0.0f, AtkActor, BeAtkActor);
	}
	///技能打击音效
	TArray<FString>SoundIdList = UGolbalBPFunctionLibrary::SplitString(SoundID, false, TEXT("|"));
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->AudioManager))
	{
		for (auto SoundId : SoundIdList)
		{
			UUECS3GameInstance::Instance->AudioManager->AsyncPlay3DSound(BeAtkActor, SoundId);
		}
	}
}
void USkillInterface::BeHitPlayEffectLocal_Implementation(int32 const& CasterID, int32 const& TargetID, const int32& actionIndex, const TArray<FString>& ActionID, const FString& EffectID, const FString& SoundID, const TArray<FString>& BeginTime)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::BeHitPlayEffectLocal_Implementation : GetEntity()!"));
		return;
	}
	GameObject* BeAtkEntity = (GameObject *)(GetEntity());
	if (!BeAtkEntity->IsPlayer()) return;
	BeHitPlayEffect(CasterID, TargetID, actionIndex, ActionID, EffectID, SoundID, BeginTime);
}

void USkillInterface::HoldEffectPlayEffect_Implementation(int32 CasterID, int32 EffectIndex, const int32& ContinuousId, const TArray<FString>& ActionID, const FString& EffectID, const FString& SoundID, const TArray<FString>& BeginTime)
{
	SCOPE_CYCLE_COUNTER(STAT_HoldEffectPlayEffect);

	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::HoldEffectPlayEffect_Implementation : GetEntity()!"));
		return;
	}
	GameObject* AtkEntity = (GameObject *)(this->GetEntity());
	AServerCharacter* AtkActor = Cast<AServerCharacter>(AtkEntity->Actor());
	AServerCharacter* CasterActor = nullptr;
	KBEngine::Entity* CasterEntity = UGolbalBPFunctionLibrary::FindEntity(CasterID);
	if (nullptr != CasterEntity)
	{
		CasterActor = Cast<AServerCharacter>(((CS3Entity *)CasterEntity)->Actor());
	}

	UHoldEffectData* EffectData = NewObject<UHoldEffectData>();
	EffectData->EffectIndex = EffectIndex;
	
	///动作
	TArray<float> ActionStartTimes;
	TArray<FName> ActionIds;
	for (int i = 0; i < ActionID.Num();i++)
	{
		if (ActionID[i] != "")
		{
			ActionIds.Add(FSTRING_TO_FNAME(ActionID[i]));
			ActionStartTimes.Add(FSTRING_TO_FLOAT(BeginTime[i]));
		}
		else
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("-----USkillInterface::HoldEffectPlayEffect[EntityId=%d, ActionID = %s"),
				this->GetEntity()->ID(), *ActionID[i]);
		}
	}
	if (ActionIds.Num())
	{
		AtkActor->PlayContinuousActions(ContinuousId, ActionIds, ActionStartTimes);
	}

	if (HoldEffectDatas.Contains(EffectIndex))
	{	
		///移除光效
		for (auto EffectUID : HoldEffectDatas[EffectIndex]->EffectUIDList)
		{
			UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(EffectUID, true, true, false);
			/*if (IsValid(effect))
			{
				effect->Stop();
			}*/
		}
		HoldEffectDatas.Remove(EffectIndex);
	}

	///光效
	TArray<FString>EffectIdList = UGolbalBPFunctionLibrary::SplitString(EffectID, false, TEXT("|"));
	for (auto EffectId : EffectIdList)
	{
		int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectId, 0.0f, CasterActor, AtkActor);
		EffectData->EffectUIDList.Add(EffectUID);
	}

	HoldEffectDatas.Add(EffectIndex, EffectData);
	

	///声音
	UHoldEffectAudioData* EffectAudioData = NewObject<UHoldEffectAudioData>();
	EffectAudioData->EffectIndex = EffectIndex;

	TArray<FString>SoundIdList = UGolbalBPFunctionLibrary::SplitString(SoundID, false, TEXT("|"));
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->AudioManager))
	{
		for (auto SoundId : SoundIdList)
		{
			UCS3AudioComponent* SkillAudioComponent = UUECS3GameInstance::Instance->AudioManager->AsyncPlay3DSound(AtkActor, SoundId);
			///保存声音组件，用于持续效果结束时终止声音
			if (IsValid(SkillAudioComponent))
			{
				EffectAudioData->AudioCompList.Add(SkillAudioComponent);
			}
		}
	}
	AtkActor->HoldEffectAudioDatas.Add(EffectIndex, EffectAudioData);

}

void USkillInterface::HoldEffectEndEffect_Implementation(int32 EffectIndex, const int32& actionIndex)
{
	GameObject* SelfEntity = (GameObject *)(this->GetEntity());
	if (SelfEntity == nullptr) 
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::HoldEffectEndEffect_Implementation : SelfEntity!"));
		return;
	}
	AServerCharacter* SelfActor = Cast<AServerCharacter>(SelfEntity->Actor());

	if (HoldEffectDatas.Contains(EffectIndex)) 
	{
		///回到待机动作
		SelfActor->StopContinuousAction(actionIndex);
		if (SelfActor->GetBaseAnimInstance())
		{
			SelfActor->GetBaseAnimInstance()->PlayStandbyAction();
		}

		if (HoldEffectDatas[EffectIndex]->EffectUIDList.Num())
		{
			///移除光效
			for (auto EffectUID : HoldEffectDatas[EffectIndex]->EffectUIDList)
			{
				UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(EffectUID, true, true, false);
				/*if (IsValid(effect))
				{
					effect->Stop();
				}*/
			}
			HoldEffectDatas.Remove(EffectIndex);
		}
	}

	///移除声音
	if (SelfActor->HoldEffectAudioDatas.Contains(EffectIndex)) 
	{
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->AudioManager))
		{
			for (auto audio : SelfActor->HoldEffectAudioDatas[EffectIndex]->AudioCompList)
			{
				if (IsValid(audio))
				{
					UUECS3GameInstance::Instance->AudioManager->Stop3DSound(audio);
				}
			}
		}
		SelfActor->HoldEffectAudioDatas.Remove(EffectIndex);
	}
}

void USkillInterface::BuffPlayLinkEffect_Implementation(int32 BeLinkerID, int32 BuffIndex, const FString& EffectID)
{
	if (BuffLinkEffectUID.Contains(BuffIndex))	///因为流程问题可能会重复添加
	{
		BuffEndPlayLinkEffect(BuffIndex);
	}
	GameObject* SelfEntity = (GameObject *)(this->GetEntity());
	KBEngine::Entity* BeLinkerEntity = UGolbalBPFunctionLibrary::FindEntity(BeLinkerID);
	if (nullptr == SelfEntity || nullptr == BeLinkerEntity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::BuffPlayLinkEffect_Implementation: SelfEntity || BeLinkerEntity!"));
		return;
	}

	AServerCharacter* SelfActor = nullptr;
	AServerCharacter* BeLinkerActor = nullptr;
	SelfActor = Cast<AServerCharacter>(((CS3Entity *)SelfEntity)->Actor());
	BeLinkerActor = Cast<AServerCharacter>(((CS3Entity *)BeLinkerEntity)->Actor());
	if (!IsValid(SelfActor) || !IsValid(BeLinkerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::BuffPlayLinkEffect_Implementation: SelfActor || BeLinkerActor!"));
		return;
	}

	int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID, 0.0f, SelfActor, BeLinkerActor);
	BuffLinkEffectUID.Add(BuffIndex, EffectUID);

}

void USkillInterface::BuffEndPlayLinkEffect_Implementation(int32 BuffIndex)
{
	if (BuffLinkEffectUID.Find(BuffIndex))
	{
		UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(BuffLinkEffectUID[BuffIndex], true, true, false);
		BuffLinkEffectUID.Remove(BuffIndex);
	}
}

void USkillInterface::ReceiveSkill_Implementation(int32 CasterID, int32 SkillID, int32 DamageType, int32 Damage, uint8 IsCritical, uint8 IsParry)
{
	SCOPE_CYCLE_COUNTER(STAT_ReceiveSkill);

	CS3Entity* BeAtkEntity = (CS3Entity *)(this->GetEntity());
	if (BeAtkEntity)
	{
		AServerCharacter* BeAtkActor = Cast<AServerCharacter>(BeAtkEntity->Actor());
		BeAtkActor->GetFightComponent()->OnReceiveSkill.Broadcast(CasterID, Damage, IsCritical, IsParry);
	}
}

void USkillInterface::onDodgeSkillHit_Implementation(int32 CasterID)
{
	CS3Entity* BeAtkEntity = (CS3Entity *)(this->GetEntity());
	if (BeAtkEntity)
	{
		AServerCharacter* BeAtkActor = Cast<AServerCharacter>(BeAtkEntity->Actor());
		BeAtkActor->GetFightComponent()->onDodgeSkillHit.Broadcast(CasterID);
	}
}

void USkillInterface::SetCooldown_Implementation(TArray<FString>& CooldownIDs, TArray<FString>& EndTimes, TArray<FString>& PersistTimes)
{
	checkf((CooldownIDs.Num() == EndTimes.Num()) && (CooldownIDs.Num() == PersistTimes.Num()), TEXT("-----USkillInterface::SetCooldown Param Error!"));

	if (CooldownIDs.Num() == 0)
	{
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillManager))
		{
			UUECS3GameInstance::Instance->SkillManager->ClearSkillCoolDown();
		}
	}
	else
	{
		TMap<int32, FSKILL_UPDATE_COOL_DOWN> UpdateSkillCdList;
		UTimeManager *TimeManager = UUECS3GameInstance::Instance->TimeManager;
		int64 _ClientTime = TimeManager->GetMultipleClientTime();
		for (size_t i = 0; i < CooldownIDs.Num(); i++)
		{
			if (!CooldownIDs[i].IsEmpty())
			{
				FSKILL_UPDATE_COOL_DOWN UpdateCoolDown = FSKILL_UPDATE_COOL_DOWN();
				UpdateCoolDown.CooldownId = FSTRING_TO_INT(CooldownIDs[i]);
				float RemainTime = (FSTRING_TO_INT64(EndTimes[i]) - _ClientTime) / (float)TIME_ENLARGE_MULTIPLE;
				UpdateCoolDown.PersistTime = FSTRING_TO_FLOAT(PersistTimes[i]);
				UpdateCoolDown.RemainingTime = RemainTime < UpdateCoolDown.PersistTime ? RemainTime : UpdateCoolDown.PersistTime;
				UpdateSkillCdList.Emplace(UpdateCoolDown.CooldownId, UpdateCoolDown);
			}
		}
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillManager))
		{
			UUECS3GameInstance::Instance->SkillManager->UpdateSkillCoolDown(UpdateSkillCdList);
		}
	}
}

void USkillInterface::ClearCooldown_Implementation(bool isClear)
{
	if (isClear)
	{
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillManager))
		{
			UUECS3GameInstance::Instance->SkillManager->ClearSkillCoolDown();
		}
	}
}

void USkillInterface::OnBeHitBackNew_Implementation(float DX, float DY, float DZ, int32 buffID, float MoveSpeed, const FString& ActionID, float ActionBeginTime, int32 CasterID)
{
	SCOPE_CYCLE_COUNTER(STAT_OnBeHitBackNew);

	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::RealUseSkill : OnBeHitBackNew_Implementation!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("-----USkillInterface::OnBeHitBackNew[EntityId=%d, ActionID = %s, ActionBeginTime = %f"),
		EntityID, *ActionID, ActionBeginTime);

	//EndHitBack(CasterID, ActionID, "");

	FVector Dest = FVector(DX, DY, DZ);
	GameObject* BeAtkEntity = (GameObject *)(this->GetEntity());
	if (BeAtkEntity == nullptr) return;
	AServerCharacter* BeAtkActor = Cast<AServerCharacter>(BeAtkEntity->Actor());
	if (!IsValid(BeAtkActor)) return;
	FVector StartPos = BeAtkActor->GetActorLocation();
	if (BeAtkEntity->Parent())//有parent服务器发的是相对坐标
	{
		Dest = BeAtkEntity->Parent()->PositionLocalToWorld(Dest);
	}

	FHitResult HitOut(ForceInit);
	FCollisionQueryParams TraceParams = FCollisionQueryParams(FName(TEXT("SplineLightWall")), true, BeAtkActor);
	TraceParams.bTraceComplex = false;
	TraceParams.bReturnPhysicalMaterial = false;
	TraceParams.bIgnoreTouches = true;	
	//射线追踪空气墙
	bool IsFind = false;
	if (this->GetWorld()->LineTraceSingleByChannel(HitOut, StartPos,
		Dest, ECC_GameTraceChannel12, TraceParams))
	{
		if (!HitOut.bStartPenetrating)
		{
			Dest = HitOut.ImpactPoint + HitOut.ImpactNormal * (BeAtkActor->GetCapsuleComponent()->GetScaledCapsuleRadius()+5.f);
			RPC_OnSynHitBackPos(buffID, Dest);
			IsFind = true;
		}
	}
	if (!IsFind)
	{
// 		FRotator DestAdjust(0.f, 5.f, 0.f);
// 		Dest = DestAdjust.RotateVector(Dest);
		Dest.X += 5.f;
		Dest.Y += 5.f;
		if (this->GetWorld()->LineTraceSingleByChannel(HitOut, StartPos,
			Dest, ECC_GameTraceChannel12, TraceParams))
		{
			if (!HitOut.bStartPenetrating)
			{
				Dest = HitOut.ImpactPoint + HitOut.ImpactNormal * (BeAtkActor->GetCapsuleComponent()->GetScaledCapsuleRadius() + 5.f);
				RPC_OnSynHitBackPos(buffID, Dest);
				IsFind = true;
			}
		}
	}

// 	if (this->GetWorld()->SweepSingleByChannel(HitOut, StartPos, Dest, FQuat::Identity, ECC_GameTraceChannel12, FCollisionShape::MakeCapsule(BeAtkActor->GetCapsuleComponent()->GetScaledCapsuleRadius(), BeAtkActor->GetCapsuleComponent()->GetScaledCapsuleHalfHeight())))
// 	{
// 		if (!HitOut.bStartPenetrating)
// 		{
// 			Dest = HitOut.Location + HitOut.Normal * 5.f;
// 			RPC_OnSynHitBackPos(buffID, Dest);
// 		}
// 		UKismetSystemLibrary::DrawDebugSphere(GetWorld(), Dest, 15.f, 12, FLinearColor::Blue, 5.0);
// 	}

	///动作
	BeAtkActor->PlayAction(FSTRING_TO_FNAME(ActionID), ActionBeginTime);
	UGameObjectInterface * Interface = ((GameObject*)BeAtkEntity)->Interface_Cache.GameObjectInterface;
	if (IsValid(Interface))
	{
		///位移
		if (Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER))
		{
			if (BeAtkEntity->Parent())//怪物模拟用相对位置，以防怪物站在移动平台上
			{
				Dest = BeAtkEntity->Parent()->PositionWorldToLocal(Dest);
			}
			MonsterBeHitBackNew(BeAtkEntity, BeAtkActor, MoveSpeed, Dest, CasterID);
		}
		else if (Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
		{
			RoleBeHitBackNew(BeAtkEntity, BeAtkActor, MoveSpeed, Dest, CasterID);//玩家模拟用世界位置
		}
	}
}
void USkillInterface::MonsterBeHitBackNew(GameObject* BeAtkEntity, AServerCharacter* BeAtkActor, float MoveSpeed, FVector Dest, int32 CasterID)
{
	BeAtkActor->GetCharacterMovement()->StopMovementImmediately();
	BeAtkActor->ChangeFilter(MoveSpeed, false, Dest);
	BeAtkActor->GetFightComponent()->OnBeHitBackNew.Broadcast(CasterID, Dest, MoveSpeed);
}

void USkillInterface::RoleBeHitBackNew(GameObject* BeAtkEntity, AServerCharacter* BeAtkActor, float MoveSpeed, FVector Dest, int32 CasterID)
{
	if (BeAtkEntity->IsPlayer())
	{

		ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(BeAtkActor->GetController());
		if (IsValid(PlayerController))
		{
			PlayerController->MoveBackToPostion(MoveSpeed, Dest);
		}
	}
	BeAtkActor->GetFightComponent()->OnBeHitBackNew.Broadcast(CasterID, Dest, MoveSpeed);
}

void USkillInterface::RPC_OnSynHitBackPos(int32 buffID, FVector desPosition)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:OnSynHitBackPos : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray Args;
	Args.Add(buffID);
	Args.Add(desPosition);
	GetEntity()->CellCall(TEXT("OnSynHitBackPos"), Args);
}

void USkillInterface::OnEndHitBack_Implementation(int32 CasterID, const FString& HitBackActionId, const FString& GetUpActionId)
{
	SCOPE_CYCLE_COUNTER(STAT_OnEndHitBack);
	EndHitBack(CasterID, HitBackActionId, GetUpActionId);
}

void USkillInterface::EndHitBack(int32 CasterID, const FString& HitBackActionId, const FString& GetUpActionId)
{
	GameObject* SelfEntity = (GameObject *)(this->GetEntity());
	if (SelfEntity)
	{
		AServerCharacter* SelfActor = Cast<AServerCharacter>(SelfEntity->Actor());
		SelfActor->StopActionById(FSTRING_TO_FNAME(HitBackActionId));
		SelfActor->StopActionById(FSTRING_TO_FNAME(GetUpActionId));

		UGameObjectInterface * Interface = ((GameObject*)SelfEntity)->Interface_Cache.GameObjectInterface;;
		if (IsValid(Interface))
		{
			if (Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER))
			{
				SelfActor->ResetFilter();
				SelfActor->GetFightComponent()->OnEndHitBack.Broadcast(CasterID);
				SelfActor->GetCharacterMovement()->StopMovementImmediately();
			}
			else if (Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
			{
				if (SelfEntity->IsPlayer())
				{
					ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(SelfActor->GetController());
					if (IsValid(PlayerController) && PlayerController->GetMoveType() ==  CS3_MOVE_TYPE::MOVE_TYPE_BACK)
					{
						PlayerController->EndMoveBack();
					}
				}
				SelfActor->GetFightComponent()->OnEndHitBack.Broadcast(CasterID);
			}
		}
	}
}

void USkillInterface::CLIENT_ControlledOnBeHitBack_Implementation(float DX, float DY, float DZ, float MoveSpeed, 
	const FString& ActionID, float ActionBeginTime, int32 CasterID)
{
	SCOPE_CYCLE_COUNTER(STAT_CLIENT_ControlledOnBeHitBack);

	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::RealUseSkill : OnBeHitBackNew_Implementation!"));
		return;
	}

	CS3_Display(CS3DebugType::CL_Undefined, TEXT("-----USkillInterface::OnBeHitBackNew[EntityId=%d, ActionID = %s, ActionBeginTime = %f"),
		EntityID, *ActionID, ActionBeginTime);

	FVector Dest = FVector(DX, DY, DZ);
	GameObject* BeAtkEntity = (GameObject *)(this->GetEntity());
	if (BeAtkEntity->Parent())//有parent服务器发的是相对坐标，UHitBackMoveFilterActorComponent组件写的是世界位置（被客户端控制的怪）
	{
		Dest = BeAtkEntity->Parent()->PositionLocalToWorld(Dest);
	}
	AServerCharacter* BeAtkActor = Cast<AServerCharacter>(BeAtkEntity->Actor());

	if (IsValid(BeAtkActor))
	{
		///动作
		BeAtkActor->PlayAction(FSTRING_TO_FNAME(ActionID), ActionBeginTime);
		BeAtkActor->ChangeHitBackMoveFilter(MoveSpeed, Dest);
		///显示受击光效
		BeAtkActor->GetFightComponent()->OnBeHitBackNew.Broadcast(CasterID, Dest, MoveSpeed);
	}
}

void USkillInterface::CLIENT_ControlledEndHitBack_Implementation(int32 CasterID, 
	const FString& HitBackActionId, const FString& GetUpActionId)
{
	SCOPE_CYCLE_COUNTER(STAT_CLIENT_ControlledEndHitBack);

	GameObject* BeAtkEntity = (GameObject *)(this->GetEntity());
	if (!BeAtkEntity) return;
	AServerCharacter* BeAtkActor = Cast<AServerCharacter>(BeAtkEntity->Actor());
	if (!BeAtkActor) return;
	BeAtkActor->EndHitBack();
}

void USkillInterface::OnPull_Implementation(float DX, float DY, float DZ, float MoveSpeed, const FString& ActionID, float ActionBeginTime, int32 CasterID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::OnPull_Implementation : GetEntity()!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("-----USkillInterface::OnPull[EntityId=%d, ActionID = %s, ActionBeginTime = %f"),
		this->GetEntity()->ID(), *ActionID, ActionBeginTime);
	FVector Dest = FVector(DX, DY, DZ);
	GameObject* BeAtkEntity = (GameObject *)(this->GetEntity());
	if (BeAtkEntity->Parent())//有parent服务器发的是相对坐标
	{
		Dest = BeAtkEntity->Parent()->PositionLocalToWorld(Dest);
	}
	AServerCharacter* BeAtkActor = Cast<AServerCharacter>(BeAtkEntity->Actor());

	///动作、光效、声音
	BeAtkActor->PlayAction(FSTRING_TO_FNAME(ActionID), ActionBeginTime);

	UGameObjectInterface * Interface = ((GameObject*)BeAtkEntity)->Interface_Cache.GameObjectInterface;;
	if (IsValid(Interface))
	{
		///位移
		if (Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER))
		{
			PullMonster(BeAtkEntity, BeAtkActor, MoveSpeed, CasterID, FVector(DX, DY, DZ));//怪物模拟用相对位置，以防怪物站在移动平台上
		}
		else if (Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
		{
			PullRole(BeAtkEntity, BeAtkActor, MoveSpeed, CasterID, Dest);//玩家模拟用世界位置
		}
	}
}
void USkillInterface::PullMonster(GameObject* BeAtkEntity, AServerCharacter* BeAtkActor, float MoveSpeed, int32 CasterID, FVector Dest)
{
	BeAtkActor->ChangeFilter(MoveSpeed, false, Dest);
	BeAtkActor->GetFightComponent()->OnPull.Broadcast(CasterID, Dest, MoveSpeed);
}

void USkillInterface::OnDissolve_Implementation(int32 TargetID, const FString& DissolveColor, const FString& DissolveDirection, float StarDissolveDegree, float EndDissolveDegree, float DissolveTime, float StartDelayTime)
{
	AServerCharacter* Target = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(TargetID));
	TArray<FString> ColorList = UGolbalBPFunctionLibrary::SplitString(DissolveColor);
	FVector DissolveColorVector = FVector(FSTRING_TO_FLOAT(ColorList[0]), FSTRING_TO_FLOAT(ColorList[1]), FSTRING_TO_FLOAT(ColorList[2]));

	TArray<FString> DirectionList = UGolbalBPFunctionLibrary::SplitString(DissolveDirection);
	FLinearColor DissolveDirectionVector = FLinearColor(FSTRING_TO_FLOAT(DirectionList[0]), FSTRING_TO_FLOAT(DirectionList[1]), FSTRING_TO_FLOAT(DirectionList[2]), FSTRING_TO_FLOAT(DirectionList[3]));
	UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(Target->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));

	if (IsValid(Target->GetMesh()->SkeletalMesh))
	{
		UGolbalBPFunctionLibrary::CS3SetVectorParameterOnMaterials(Target->GetMesh(),TEXT("DissolveColor"), DissolveColorVector);
		UGolbalBPFunctionLibrary::CS3SetScalarParameterOnMaterials(Target->GetMesh(), TEXT("DissolveEnable"), 1.0f);
		UGolbalBPFunctionLibrary::CS3SetLinearParameterOnMaterials(Target->GetMesh(),TEXT("DissolveDirection"), DissolveDirectionVector);
	}
	else if (DefaultStaticMeshCpt->GetMaterials().Num()>0)
	{     
		UGolbalBPFunctionLibrary::CS3SetVectorParameterOnMaterials(DefaultStaticMeshCpt, TEXT("DissolveColor"), DissolveColorVector);
		UGolbalBPFunctionLibrary::CS3SetLinearParameterOnMaterials(DefaultStaticMeshCpt, TEXT("DissolveDirection"), DissolveDirectionVector);
		UGolbalBPFunctionLibrary::CS3SetScalarParameterOnMaterials(DefaultStaticMeshCpt, TEXT("DissolveEnable"), 1.0f);
	}

	if (m_DissolveHandle.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(m_DissolveHandle);
	}
	DissolveTimer = 0.0f;
	TWeakObjectPtr<USkillInterface> ThisPtr(this);
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, m_DissolveHandle, FTimerDelegate::CreateLambda(
		[TargetID, ThisPtr, StarDissolveDegree, DissolveTime, EndDissolveDegree]()
	{
		if (ThisPtr.IsValid())
		{
			USkillInterface* SkillInterface = ThisPtr.Get();
			AServerCharacter* Target = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(TargetID));
			if (IsValid(SkillInterface) && IsValid(Target))
			{
				if (SkillInterface->DissolveTimer < 1)
				{
					SkillInterface->DissolveTimer += 0.1f / DissolveTime;
					float CurDegree = UKismetMathLibrary::Ease(StarDissolveDegree, EndDissolveDegree, SkillInterface->DissolveTimer, EEasingFunc::Linear);
					UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(Target->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));

					if (IsValid(Target->GetMesh()->SkeletalMesh))
					{
						UGolbalBPFunctionLibrary::CS3SetScalarParameterOnMaterials(Target->GetMesh(), TEXT("DissolveDegree"), CurDegree);
					}
					else if (DefaultStaticMeshCpt->GetMaterials().Num() > 0)
					{
						UGolbalBPFunctionLibrary::CS3SetScalarParameterOnMaterials(DefaultStaticMeshCpt, TEXT("DissolveDegree"), CurDegree);
					}
				}
				else
				{
					UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(SkillInterface->m_DissolveHandle);
				}
			}
		}
	}), 0.1, true, StartDelayTime);

}

void USkillInterface::EndDissolve_Implementation(int32 TargetID, float StarDissolveDegree, float EndDissolveDegree, float DissolveTime)
{
	AServerCharacter* Target = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(TargetID));
	if (m_DissolveHandle.IsValid())
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(m_DissolveHandle);
	}
	DissolveTimer = 0.0f;
	TWeakObjectPtr<USkillInterface> ThisPtr(this);
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, m_DissolveHandle, FTimerDelegate::CreateLambda([TargetID, ThisPtr, StarDissolveDegree, DissolveTime, EndDissolveDegree]()
	{
		if (ThisPtr.IsValid())
		{
			USkillInterface* SkillInterface = ThisPtr.Get();
			AServerCharacter* Target = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(TargetID));
			if (IsValid(SkillInterface) && IsValid(Target))
			{
				UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(Target->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
				if (SkillInterface->DissolveTimer < 1)
				{
					SkillInterface->DissolveTimer += 0.1f / DissolveTime;
					float CurDegree = UKismetMathLibrary::Ease(StarDissolveDegree, EndDissolveDegree, SkillInterface->DissolveTimer, EEasingFunc::Linear);
					
					if (IsValid(Target->GetMesh()->SkeletalMesh))
					{
						UGolbalBPFunctionLibrary::CS3SetScalarParameterOnMaterials(Target->GetMesh(), TEXT("DissolveDegree"), CurDegree);
					}
					else if (DefaultStaticMeshCpt->GetMaterials().Num() > 0)
					{
						UGolbalBPFunctionLibrary::CS3SetScalarParameterOnMaterials(DefaultStaticMeshCpt, TEXT("DissolveDegree"), CurDegree);
					}
				}
				else
				{
					UGolbalBPFunctionLibrary::CS3SetScalarParameterOnMaterials(DefaultStaticMeshCpt, TEXT("DissolveEnable"), 0.0f);
					UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(SkillInterface->m_DissolveHandle);
				}
			}
		}
	}), 0.1, true);
}

void USkillInterface::PullRole(GameObject* BeAtkEntity, AServerCharacter* BeAtkActor, float MoveSpeed, int32 CasterID, FVector Dest)
{
	if (BeAtkEntity->IsPlayer())
	{
		ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(BeAtkActor->GetController());
		if (IsValid(PlayerController))
		{
			PlayerController->MoveBackToPostion(MoveSpeed, Dest);
		}
	}
	BeAtkActor->GetFightComponent()->OnPull.Broadcast(CasterID, Dest, MoveSpeed);
}

void USkillInterface::EndPull_Implementation(int32 CasterID)
{
	GameObject* SelfEntity = (GameObject *)(this->GetEntity());
	if (SelfEntity)
	{
		AServerCharacter* SelfActor = Cast<AServerCharacter>(SelfEntity->Actor());
		//停止当前动作，回到待机动作
		SelfActor->StopAction();

		UGameObjectInterface * Interface = ((GameObject*)SelfEntity)->Interface_Cache.GameObjectInterface;;
		if (IsValid(Interface))
		{
			if (Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER))
			{
				SelfActor->ResetFilter();
				SelfActor->GetFightComponent()->EndPull.Broadcast(CasterID);
			}
			else if (Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
			{
				if (SelfEntity->IsPlayer())
				{
					Cast<APlayerCharacter>(SelfActor)->StopPlayerMove();
				}
				SelfActor->GetFightComponent()->EndPull.Broadcast(CasterID);
			}
		}
	}
}

void USkillInterface::OnChargeToPosition_Implementation(float X, float Y, float Z, float MoveSpeed)
{
	if (this->GetEntity() == nullptr)return;
	GameObject* BeAtkEntity = (GameObject *)(this->GetEntity());
	AServerCharacter* BeAtkActor = Cast<AServerCharacter>(BeAtkEntity->Actor());
	if (!IsValid(BeAtkActor))return;
	UGameObjectInterface * Interface = ((GameObject*)BeAtkEntity)->Interface_Cache.GameObjectInterface;;
	if (IsValid(Interface)&& Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER))
	{
		//BeAtkEntity->SetForbidMoveAction(true); 
		BeAtkActor->ChangeFilter(MoveSpeed, true, FVector(X, Y, Z));
	}
}

void USkillInterface::onEndChargeToPosition_Implementation()
{
	GameObject* BeAtkEntity = (GameObject *)(this->GetEntity());
	if (BeAtkEntity != nullptr)
	{
		AServerCharacter* BeAtkActor = Cast<AServerCharacter>(BeAtkEntity->Actor());
		if (IsValid(BeAtkActor))
		{
			UGameObjectInterface * Interface = ((GameObject*)BeAtkEntity)->Interface_Cache.GameObjectInterface;;
			if (IsValid(Interface) && Interface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER))
			{
				BeAtkActor->ResetFilter();
			}
		}
	}
}

void USkillInterface::OnRage_Implementation(int32 TargetID, float vector_r, float vector_g, float vector_b, float vector_a)
{
	AServerCharacter* TargetActor = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(TargetID));
	FLinearColor LinearColor = FLinearColor(vector_r, vector_g, vector_b, vector_a);
	TargetActor->OnShowRageEffect(LinearColor);
}

void USkillInterface::EndRage_Implementation(int32 TargetID)
{
	AServerCharacter* TargetActor = Cast<AServerCharacter>(UGolbalBPFunctionLibrary::GetActorByID(TargetID));
	TargetActor->OnEndRageEffect();
}

void USkillInterface::PlayModleHighlight_Implementation(int32 CasterID)
{
	SCOPE_CYCLE_COUNTER(STAT_PlayModleHighlight);

	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::PlayModleHighlight_Implementation : GetEntity()!"));
		return;
	}
	FVector Dest = FVector(0.0f, 0.0f, 0.0f);
	float MoveSpeed = 0.0f;
	GameObject* BeAtkEntity = (GameObject *)(this->GetEntity());
	AServerCharacter* BeAtkActor = Cast<AServerCharacter>(BeAtkEntity->Actor());
	BeAtkActor->GetFightComponent()->OnBeHitBackNew.Broadcast(CasterID, Dest, MoveSpeed);
}

bool USkillInterface::ChangeAttackState(EATTACT_STATE AttackState)
{
	//if (IsValid(AtkStateCtrl))
	//{
	//	if (AtkStateCtrl->GetCurrAttState() != AttackState)
	//	{
	//		return AtkStateCtrl->ChangeAttackState(EntityID, AttackState);
	//	}
	//	else
	//	{
	//		CS3_Display(CS3DebugType::CL_Undefined, TEXT("USkillInterface::ChangeAttackState -> The Attack State Is Same~"));
	//	}
	//}
	return false;
}

void USkillInterface::SetAnimRateScale_Implementation(float RateScale)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::SetAnimRateScale_Implementation : GetEntity()!"));
		return;
	}
	AServerCharacter* SelfActor = Cast<AServerCharacter>(this->GetEntity()->Actor());
	SelfActor->SetAnimRate(RateScale);
}

void USkillInterface::StartSkillHitSlow_Implementation(float actionSpeed, float actionTime, float hitSlowTime)
{
	SetAnimRateScale(actionSpeed);
}

void USkillInterface::StopSkillHitSlow_Implementation()
{
	SetAnimRateScale(1.0);
}

bool USkillInterface::CancelSkillAssistUi()
{
	SetCurrentUsePosItemUID(TEXT(""));
	APlayerCharacter* player = Cast<APlayerCharacter>(GetActor());
	if (!IsValid(player)) return false;
	if (player->GetSkillAssistUi())
	{
		FightAssist->ClearFightAssistUi();
		FightAssist->ClearModelAssistUi();
		player->AddSkillAssistUiToScene(false);
		return true;
	}
	return false;
}

void USkillInterface::intonateSpell_Implementation(float intonateTime, const int32& SkillID)
{
	this->OnIntonateSpellBP(intonateTime, SkillID, false);

}

void USkillInterface::intonateSpellOver_Implementation()
{
	this->OnIntonateSpellOverBP();
}

void USkillInterface::OnShowIntonateBar_Implementation(const int32 CasterID, const float HoldTime, const int32 SkillId)
{
	AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(UGolbalBPFunctionLibrary::GetActorByID(CasterID));
	if (MonsterCharacter)
	{
		MonsterCharacter->OnShowMonsterIntonateBarBP(CasterID, HoldTime, SkillId);
	}

}

void USkillInterface::OnHideIntonateBar_Implementation(const int32 CasterID)
{
	AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(UGolbalBPFunctionLibrary::GetActorByID(CasterID));
	if (MonsterCharacter)
	{
		MonsterCharacter->OnHideMonsterIntonateBarBP(CasterID);
	}

}

void USkillInterface::intonateSparSpell_Implementation(float intonateTime, const int32& SkillID)
{
	this->OnIntonateSpellBP(intonateTime, SkillID, true);
}

void USkillInterface::intonateSparSpellOver_Implementation()
{
	this->OnIntonateSpellOverBP();
}

void USkillInterface::OnMoveTypeChange(CS3_MOVE_TYPE NewMOveType, CS3_MOVE_TYPE OldMovetype)
{
	if (OldMovetype == CS3_MOVE_TYPE::MOVE_TYPE_NONE && NewMOveType != CS3_MOVE_TYPE::MOVE_TYPE_NONE)
	{
		this->OnPlayerMoveChange(0, 1);							/*全部移动开始时*/
		if (NewMOveType == CS3_MOVE_TYPE::MOVE_TYPE_BACK)
		{
			this->OnPlayerMoveChange(2, 1);						/*被动移动开始时*/
		}
		else
		{
			this->OnPlayerMoveChange(1, 1);						/*主动移动开始时*/
		}
	}
	if (OldMovetype != CS3_MOVE_TYPE::MOVE_TYPE_NONE && NewMOveType == CS3_MOVE_TYPE::MOVE_TYPE_NONE)
	{
		this->OnPlayerMoveChange(0, 0);							/*全部移动结束时*/
		if (OldMovetype == CS3_MOVE_TYPE::MOVE_TYPE_BACK)
		{
			this->OnPlayerMoveChange(2, 0);						/*被动移动结束时*/
		}
		else
		{
			this->OnPlayerMoveChange(1, 0);						/*主动移动结束时*/
		}
	}
}

void USkillInterface::OnPlayerMoveChange(int32 MoveType, int32 MoveState)
{
	if (GetEntity() != nullptr)
	{
		KBEngine::FVariantArray Args;
		Args.Add(MoveType);
		Args.Add(MoveState);
		GetEntity()->CellCall(TEXT("OnPlayerMoveChange"), Args);
	}
}

void USkillInterface::OnBuffBulletBegin_Implementation(const FString& EffectID, const float EffectSendAngle, const int32 CasterID, const int32 BuffIndex, const int32 ProxyID, const int32 EffectCustomIndex)
{
	if (!IsValid(GetActor()))
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::OnBuffBulletBegin_Implementation : GetActor()!"));
		return;
	}
	int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID, EffectSendAngle, UGolbalBPFunctionLibrary::GetActorByID(CasterID),
		GetActor(), FEffectCreate::CreateLambda([BuffIndex, ProxyID, DelayEntityID = EntityID, EffectCustomIndex](int32 UID)
	{
		AEffectEmitter* Effect = Cast<AEffectEmitter>(UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID));
		if (Effect)
		{
			Effect->SetBuffBulletData(BuffIndex, ProxyID, DelayEntityID, 0, EffectCustomIndex);
		}
	}));
	if (!BuffBulletEffectUID.Find(BuffIndex))
	{
		TMap<int32, int32> Temp;
		Temp.Add(EffectCustomIndex, EffectUID);
		BuffBulletEffectUID.Add(BuffIndex, Temp);
	}
	else
	{
		BuffBulletEffectUID[BuffIndex].Add(EffectCustomIndex, EffectUID);
	}	
}

void USkillInterface::OnBuffBulletEnd_Implementation(const int32 BuffIndex, const int32 EffectCustomIndex)
{
	if (BuffBulletEffectUID.Find(BuffIndex)&& BuffBulletEffectUID[BuffIndex].Find(EffectCustomIndex))
	{
		UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(BuffBulletEffectUID[BuffIndex][EffectCustomIndex], true, true, false);
		BuffBulletEffectUID[BuffIndex].Remove(EffectCustomIndex);
		if (BuffBulletEffectUID[BuffIndex].Num()==0)
		{
			BuffBulletEffectUID.Remove(BuffIndex);
		}
	}
}

void USkillInterface::OnBuffBulletMultipleBegin_Implementation(const FString& EffectID, const float EffectSendAngle, const int32 EffectIndex, const int32 CasterID, const int32 BuffIndex, const int32 ProxyID)
{
	if (!IsValid(GetActor()))
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::OnBuffBulletMultipleBegin_Implementation : GetActor()!"));
		return;
	}

	int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID, EffectSendAngle, UGolbalBPFunctionLibrary::GetActorByID(CasterID),
		GetActor(), FEffectCreate::CreateLambda([BuffIndex, ProxyID, DelayEntityID = EntityID, EffectIndex](int32 UID)
	{
		AEffectEmitter* Effect = Cast<AEffectEmitter>(UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID));
		if (Effect)
		{
			Effect->SetBuffBulletData(BuffIndex, ProxyID, DelayEntityID, EffectIndex, 0);
		}
	}));

	if (BuffBulletEffectsMultiple.Find(BuffIndex))
	{
		FBUFF_BULLET_EFFECT_MUTIPLE_DATA& MutipleEffectInfo = BuffBulletEffectsMultiple[BuffIndex];
		if (MutipleEffectInfo.BuffBulletEffectData.Find(EffectID))
		{
			FBUFF_BULLET_EFFECT_DATA &EffectInfo = MutipleEffectInfo.BuffBulletEffectData[EffectID];
			EffectInfo.EffectData.Add(EffectIndex, EffectUID);
		}
		else
		{
			FBUFF_BULLET_EFFECT_DATA EffectInfo;
			EffectInfo.EffectData.Add(EffectIndex, EffectUID);
			MutipleEffectInfo.BuffBulletEffectData.Add(EffectID, EffectInfo);
		}
	}
	else
	{
		FBUFF_BULLET_EFFECT_MUTIPLE_DATA MutipleEffectInfo;
		FBUFF_BULLET_EFFECT_DATA EffectInfo;
		EffectInfo.EffectData.Add(EffectIndex, EffectUID);
		MutipleEffectInfo.BuffBulletEffectData.Add(EffectID, EffectInfo);
		BuffBulletEffectsMultiple.Add(BuffIndex, MutipleEffectInfo);
	}
}

void USkillInterface::OnBuffBulletMultipleEnd_Implementation(const int32 BuffIndex, const FString& EffectID, const int32 EffectIndex)
{
	if (BuffBulletEffectsMultiple.Find(BuffIndex))
	{
		FBUFF_BULLET_EFFECT_MUTIPLE_DATA & MutipleEffectInfo = BuffBulletEffectsMultiple[BuffIndex];
		if (MutipleEffectInfo.BuffBulletEffectData.Find(EffectID))
		{
			FBUFF_BULLET_EFFECT_DATA &EffectInfo = MutipleEffectInfo.BuffBulletEffectData[EffectID];
			if (EffectInfo.EffectData.Find(EffectIndex))
			{
				int32 EffectUID = EffectInfo.EffectData[EffectIndex];
				UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(EffectUID, true, true, false);
				/*if (IsValid(Effect))
				{
					Effect->Stop();
				}*/
				EffectInfo.EffectData.Remove(EffectIndex);
			}
			if (EffectInfo.EffectData.Num() == 0)
			{
				MutipleEffectInfo.BuffBulletEffectData.Remove(EffectID);
			}
		}
		if (MutipleEffectInfo.BuffBulletEffectData.Num() == 0)
		{
			BuffBulletEffectsMultiple.Remove(BuffIndex);
		}
	}
}

void USkillInterface::CreateDataFromStream(TMap<int32, FBuffData>& Buffs, const FVariant& val)
{
	KBEngine::FVariantMap mapval = val.GetValue<KBEngine::FVariantMap>();
	KBEngine::FVariantArray ArraybuffData = mapval.Find(TEXT("buffData"))->GetValue<KBEngine::FVariantArray>();
	int ArraybuffDataNum = ArraybuffData.Num();
	for (int i = 0; i < ArraybuffDataNum; i++)
	{
		FBuffData value;
		KBEngine::FVariantMap v = ArraybuffData[i].GetValue<KBEngine::FVariantMap>();
		value.createFromStream(v);
		Buffs.Add(value.BuffIndex, value);
	}
}

void USkillInterface::OnRep_isInPending()
{
	if (GetActor())
	{
		UGolbalBPFunctionLibrary::VisibleManager()->UpdateModelVisible(GetActor());
		
	}
}

void USkillInterface::Set_attrBuffsForClient(const  KBEngine::FVariantArray& newVal, const  KBEngine::FVariantArray& oldVal )
{
	SCOPE_CYCLE_COUNTER(STAT_Set_attrBuffsForClient);

	if (GetActor() && GetEntity())
	{
		//解析服务器数据
		TMap<int32, BuffDataType> newBuffDataList;
		for (int i = 0; i < newVal.Num(); ++i)
		{
			KBEngine::FVariantMap v = newVal[i].GetValue<KBEngine::FVariantMap>();
			BuffDataType newBuffData;
			BuffDataType::CreateFromVariant(v, newBuffData);
			newBuffDataList.Add(newBuffData.index, newBuffData);
		}
		//删除原来的Buff属性数组里面已经删除的元素
		TMap<int32, BuffDataType> oldAttrBuffs = AttrBuffs;
		for (auto it = oldAttrBuffs.CreateIterator(); it; ++it)
		{
			if (!newBuffDataList.Contains(it.Key()))
			{
				RemoveBuff(it.Key());
			}
		}
		//新增新Buff属性数据
		for (auto it = newBuffDataList.CreateIterator(); it; ++it)
		{
			if (AttrBuffs.Contains(it.Key()))
			{
				continue;
			}
			else
			{
				AddBuff(it.Value());
			}
		}
	}
}

TArray<FBuffUIData> USkillInterface::GetEntityBuffUIData(const int32 OtherPlayID)
{
	SCOPE_CYCLE_COUNTER(STAT_GetEntityBuffUIData);

	TArray<FBuffUIData> _BuffUIData;
	KBEngine::Entity* OtherPlay = UGolbalBPFunctionLibrary::FindEntity(OtherPlayID);
	if (OtherPlay == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::GetEntityBuffUIData : OtherPlay!"));
		return _BuffUIData;
	}

	UTimeManager *TimeManager = UUECS3GameInstance::Instance->TimeManager;
	if (!IsValid(TimeManager))
	{
		return _BuffUIData;
	}
	if (!IsValid(UUECS3GameInstance::Instance) || !IsValid(UUECS3GameInstance::Instance->BuffManager))
	{
		return _BuffUIData;
	}
	uint64 _ClientTime = (uint64)TimeManager->GetMultipleClientTime();

	FBuffUIData UIData;
	for (auto it = AttrBuffs.CreateIterator(); it; ++it)
	{
		if (it.Value().holdTime > 0 && it.Value().endTime < _ClientTime)
		{
			continue;
		}
		float _RemainTime = (it.Value().endTime - _ClientTime) / (float)TIME_ENLARGE_MULTIPLE;
		UIData = UUECS3GameInstance::Instance->BuffManager->CreateBuffUIData(it.Value().index, it.Value().buffID, it.Value().holdTime, _RemainTime, it.Value().layer);
		_BuffUIData.Add(UIData);
	}

	for (auto it = AttrClientBuffs.CreateIterator(); it; ++it)
	{
		if (it.Value().holdTime > 0 && it.Value().endTime < _ClientTime)
		{
			continue;
		}
		float _RemainTime = (it.Value().endTime - _ClientTime) / (float)TIME_ENLARGE_MULTIPLE;
		UIData = UUECS3GameInstance::Instance->BuffManager->CreateBuffUIData(it.Value().index, it.Value().buffID, it.Value().holdTime, _RemainTime, it.Value().layer);
		_BuffUIData.Add(UIData);
	}
	return _BuffUIData;
}

void USkillInterface::ChangeToNormalModelVisible_Implementation()
{
	//透明Buff后续改进
	GameObject* SelfEntity = (GameObject *)(this->GetEntity());
	UVisibleManager* visibleMgr = UGolbalBPFunctionLibrary::VisibleManager();
	if (SelfEntity && visibleMgr)
	{
		AServerCharacter* SelfActor = Cast<AServerCharacter>(SelfEntity->Actor());
		visibleMgr->UpdateModelVisible(SelfActor);
	}
}

void USkillInterface::OnRiseBegin_Implementation(const int32& ContinuousId, const TArray<FString>& ActionID, const TArray<FString>& BeginTime, const float& hitTime, const float& speed)
{
	SCOPE_CYCLE_COUNTER(STAT_OnRiseBegin);

	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::OnRiseBegin_Implementation : GetEntity()!"));
	}
	//判断时间和速度是否非法
	if (hitTime <= 0.0f || speed <= 0.0f)
	{
		CS3_Warning(TEXT("USkillInterface::OnRiseBegin--- hitTime OR speed <= 0 !"));
		return;
	}

	//获取被击飞的Character
	AServerCharacter* ServerActor = Cast<AServerCharacter>(GetActor());

	if (IsValid(ServerActor))
	{
		//清除计时器
		if (m_UpForceHandle.IsValid())
		{
			if (IsValid(UUECS3GameInstance::Instance))
			{
				UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(m_UpForceHandle);
			}

			CloseUpForce();
		}

		m_BeforUpForceMoveMode = ServerActor->GetCharacterMovement()->MovementMode;

		//开启飞行模式
		ServerActor->GetCharacterMovement()->SetMovementMode(MOVE_Flying);
		ServerActor->GetCharacterMovement()->BrakingDecelerationFlying = 100000000.0f;
		//添加向上的力 乘以100是由于服务器速度单位为m/s而客户端是cm/s
		ServerActor->OpenUpForce(speed * 100);
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(m_UpForceHandle, this, 
				&USkillInterface::CloseUpForce, hitTime, false);
		}
		
		TArray<float> ActionStartTimes;
		TArray<FName> ActionIds;
		for (int i = 0; i < ActionID.Num();i++)
		{
			if (ActionID[i] != "")
			{
				ActionIds.Add(FSTRING_TO_FNAME(ActionID[i]));
				ActionStartTimes.Add(FSTRING_TO_FLOAT(BeginTime[i]));
			}
			else
			{
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("-----USkillInterface::OnRiseBegin[EntityId=%d, ActionID = %s"),
					this->GetEntity()->ID(), *ActionID[i]);
			}
		}
		if (ActionIds.Num())
		{
			ServerActor->PlayContinuousActions(ContinuousId, ActionIds, ActionStartTimes);
		}
		
	}
}

void USkillInterface::OnRiseEnd_Implementation(const int32& actionIndex)
{
	SCOPE_CYCLE_COUNTER(STAT_OnRiseEnd);

	if (m_UpForceHandle.IsValid())
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(m_UpForceHandle);
		}

		CloseUpForce();
	}
	AServerCharacter* ServerActor = Cast<AServerCharacter>(GetActor());
	ServerActor->StopContinuousAction(actionIndex);
}

void USkillInterface::PlayArtificeSpar_Implementation(const FString& PreActionID, const FString& CycleActionID_)
{
	AGameCharacter* playerActor = Cast<AGameCharacter>(GetActor());
	if (IsValid(playerActor))
	{
		if (PreActionID.IsEmpty())
		{
			playerActor->PlayAction(FSTRING_TO_FNAME(CycleActionID_));
		}
		else
		{

			FActionOverDelegate Delegate;
			Delegate.AddUObject(this, &USkillInterface::OnPlayArtificeSpar);
			CycleActionID = FSTRING_TO_FNAME(CycleActionID_);
			playerActor->PlayAction(FSTRING_TO_FNAME(PreActionID), 0.0f, Delegate);
		}

	}
}

void USkillInterface::OnPlayArtificeSpar(ACharacter* Character, FACTION_DATA InActionData)
{
	AGameCharacter* playerActor = Cast<AGameCharacter>(GetActor());
	if (IsValid(playerActor))
	{
		playerActor->PlayAction(CycleActionID);
	}
}

void USkillInterface::SetCatchTargetId(const int32& CatchTargetId)
{
	m_CatchTargetID = CatchTargetId;
}

const int32& USkillInterface::GetCatchTargetId()
{
	return m_CatchTargetID;
}

void USkillInterface::StopArtificeSpar_Implementation(const FString& PostActionID)
{
	AGameCharacter* playerActor = Cast<AGameCharacter>(GetActor());
	if (IsValid(playerActor))
	{
		playerActor->PlayAction(FSTRING_TO_FNAME(PostActionID));
	}
}

void USkillInterface::CloseUpForce()
{
	AServerCharacter* ServerActor = Cast<AServerCharacter>(GetActor());

	if (m_UpForceHandle.IsValid())
	{
		if (IsValid(UUECS3GameInstance::Instance))
		{
			UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(m_UpForceHandle);
		}
	}

	if (IsValid(ServerActor))
	{
		ServerActor->CloseUpForce();
		ServerActor->GetCharacterMovement()->SetMovementMode(m_BeforUpForceMoveMode);
		ServerActor->GetCharacterMovement()->BrakingDecelerationFlying = 0.0f;
	}
}

void USkillInterface::HomingLookAtTarget(AActor*AtkTarget, AActor* BeTarget)
{
	//非Z值的坐标
	FVector AtkTargetVecter = AtkTarget->GetActorLocation();
	AtkTargetVecter.Z = 0;
	FVector BeTargetVecter = BeTarget->GetActorLocation();
	BeTargetVecter.Z = 0;

	FRotator LookR = FRotationMatrix::MakeFromX(BeTargetVecter - AtkTargetVecter).Rotator();
	AtkTarget->SetActorRotation(LookR);
}

void USkillInterface::UsePositionItem(FString UID, int32 SkillId)
{
	CS3Entity* ent = (CS3Entity*)GetEntity();
	if (ent)
	{
		FightAssist->AddItemAssistUi(ent, UID, SkillId);
		SetCurrentUsePosItemUID(UID);
	}
	
}

void USkillInterface::UsePositionItemExt(FString UID, int32 SkillId)
{
	CS3Entity* ent = (CS3Entity*)GetEntity();
	if (ent)
	{
		FightAssist->AddItemAssistUiExt(ent, UID, SkillId);
		SetCurrentUsePosItemUID(UID);
	}
}

FString USkillInterface::GetBuffExtraTips(const int32& buffIndex, const FString& colorstr)
{
	FString result;
	if (BuffExtraData.Contains(buffIndex))
	{
		UJsonFieldData* temp = UJsonFieldData::Create(this);
		auto returnvalue = temp->FromString(BuffExtraData.FindRef(buffIndex));
		for (FString key : returnvalue->GetObjectKeys(UUECS3GameInstance::Instance->GetWorld()))
		{
			FString tempString = "";
			tempString += UGolbalBPFunctionLibrary::GetChinese(key);
			tempString += TEXT(": ");
			tempString += INT_TO_FSTRING(FSTRING_TO_INT(returnvalue->GetString(key)));///因为JSON打包的整型自动变成浮点型了，所以需转换
			result.Append(UGolbalBPFunctionLibrary::StrToColorStr(tempString, colorstr));
			result.Append(TEXT("<br/>"));
		}
	}
	return result;
}

void USkillInterface::EndTransparency(float outTime, float endTP, float startTP)
{
	BTranAnamorphism = false;
	TempFValue.Empty();
	TempFValue.Add(outTime);
	TempFValue.Add(endTP);
	TempFValue.Add(startTP);
	UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(GetActor());
}

void USkillInterface::VisibleStopTransparency()
{
	float outTime(0.0);
	float endTP(0.0);
	float startTP(0.0);
	if (TempFValue.Num() >= 3)
	{
		outTime = TempFValue[0];
		endTP = TempFValue[1];
		startTP = TempFValue[2];
	}
	StopTransparency(outTime, endTP, startTP);
}

void USkillInterface::StartTransparency(float enterTime, float startTP, float endTP)
{
	BTranAnamorphism = true;
	TempFValue.Empty();
	TempFValue.Add(enterTime);
	TempFValue.Add(startTP);
	TempFValue.Add(endTP);
	UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(GetActor());
}

void USkillInterface::VisibleShowTransparency()
{
	float enterTime(0.0);
	float startTP(0.0);
	float endTP(0.0);
	if (TempFValue.Num() >= 3)
	{
		enterTime = TempFValue[0];
		startTP = TempFValue[1];
		endTP = TempFValue[2];

		TempFValue.RemoveAt(0);
		TempFValue.Insert(0.0, 0);
	}
	ShowTransparency(enterTime, startTP, endTP);
}

void USkillInterface::StartHideCharacter(float enterTime)
{
	TempChangeTime = enterTime;
	UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(GetActor());
}

void USkillInterface::VisibleHideCharacter(float endTP)
{
	ShowTransparency(TempChangeTime, 1.0, endTP);
}

void USkillInterface::EndHideCharacter(float outTime)
{
	TempChangeTime = outTime;
	UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(GetActor());
}

void USkillInterface::VisibleShowCharacter(float startTP)
{
	StopTransparency(TempChangeTime, startTP, 1.0);
}

void USkillInterface::OnReplaceSkillBarEnd_Implementation()
{
	CS3Entity* SelfEntity = (CS3Entity *)(this->GetEntity());
	if (SelfEntity)
	{
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuickBarManager))
		{
			UUECS3GameInstance::Instance->QuickBarManager->SetIsReplaceQb(false);
			UUECS3GameInstance::Instance->QuickBarManager->RemoveReplaceQBItem();
		}
	}
}

void USkillInterface::ReplaceSkillBar_Implementation(const FString& jsonData)
{
	CS3Entity* SelfEntity = (CS3Entity *)(this->GetEntity());
	if (SelfEntity)
	{
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuickBarManager))
		{
			UUECS3GameInstance::Instance->QuickBarManager->RemoveReplaceQBItem();
			auto JsonData = UJsonFieldData::Create(this)->FromString(jsonData);
			TArray<FString> indexs = JsonData->GetObjectKeys(this);
			for (auto index : indexs)
			{
				auto skillData = JsonData->GetObject(index);
				UUECS3GameInstance::Instance->QuickBarManager->AddReplaceQBItem(FSTRING_TO_INT(index), FSTRING_TO_INT(skillData->GetString("QbType")), FSTRING_TO_INT(skillData->GetString("ID")), 0, 0);
			}
			UUECS3GameInstance::Instance->QuickBarManager->SetIsReplaceQb(true);
			//替换技能栏后应退出自动战斗CST-10788
			if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
			{
				UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchAutoFight(false, EBreakAutomaticType::StateBreakType);
			}
		}
	}
}

void USkillInterface::AddReplaceSkillBar_Implementation(const FString& jsonData)
{
	CS3Entity* SelfEntity = (CS3Entity *)(this->GetEntity());
	if (SelfEntity)
	{
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuickBarManager))
		{
			auto JsonData = UJsonFieldData::Create(this)->FromString(jsonData);
			TArray<FString> indexs = JsonData->GetObjectKeys(this);
			int32 indexLength = UUECS3GameInstance::Instance->QuickBarManager->GetReplaceQBItemLen();
			for (auto index : indexs)
			{
				int32 WholeIndex = indexLength + FSTRING_TO_INT(index);
				auto skillData = JsonData->GetObject(index);
				UUECS3GameInstance::Instance->QuickBarManager->AddReplaceQBItem( WholeIndex, FSTRING_TO_INT(skillData->GetString("QbType")), FSTRING_TO_INT(skillData->GetString("ID")), 0, 0);
			}
			UUECS3GameInstance::Instance->QuickBarManager->SetIsReplaceQb(true);
			//替换技能栏后应退出自动战斗CST-10788
			if (IsValid(UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()))
			{
				UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar()->SwitchAutoFight(false, EBreakAutomaticType::StateBreakType);
			}
		}
	}
}

void USkillInterface::RefreshReplaceSkillBar_Implementation(const int32& index)
{
	
}


void USkillInterface::LXDistortScene_Implementation(float fDitortAngle, float fDistortMask, float fStartTimeDistort, float fRecoveryTimeDistort, float HoldTimer)
{
	GameObject* SelfEntity = (GameObject *)(this->GetEntity());
	if (nullptr == SelfEntity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::LXDistortScene_Implementation: SelfEntity!"));
		return;
	}
	APlayerCharacter* Character = Cast<APlayerCharacter>(SelfEntity->Actor());
	if (Character)
	{
		Character->LXDistortScene_P(fDitortAngle, fDistortMask, fStartTimeDistort, fRecoveryTimeDistort,HoldTimer);
	}
}

void USkillInterface::RemoveBuffExtraTips_Implementation(const int32& buffIndex)
{
	if (BuffExtraData.Contains(buffIndex))
	{
		BuffExtraData.Remove(buffIndex);
	}
}

void USkillInterface::AddShowBuffExtraTips_Implementation(const int32& buffIndex, const FString& jsonData)
{
	if (BuffExtraData.Contains(buffIndex))
	{
		BuffExtraData.Remove(buffIndex);
	}
	BuffExtraData.Add(buffIndex, jsonData);
}

void USkillInterface::TeleportToDstPosition_Implementation(FVector& position)
{
	AServerCharacter* playerCharacter = Cast<AServerCharacter>(GetActor());
	if (IsValid(playerCharacter))
	{
		playerCharacter->SetActorLocation(position, false, nullptr, ETeleportType::TeleportPhysics);
	}

	if (Cast<AMonsterCharacter>(playerCharacter))
	{
		playerCharacter->ResetFilterData();
	}
}


void USkillInterface::ShowBuffExtraSkillBar_Implementation(const FString& SkillIDStr)
{
	BuffExtraSkillIDs.Empty();
	//显示额外技能栏
	if (SkillIDStr.IsEmpty())
	{
		return;
	}

	TArray<FString> SkillIDStrList = UGolbalBPFunctionLibrary::SplitString(SkillIDStr, false, TEXT("|"));
	for (FString IT : SkillIDStrList)
	{
		BuffExtraSkillIDs.Add(FSTRING_TO_INT(IT));
	}

// 	for (auto skillID : BuffExtraSkillIDs)
// 	{
// 		CS3_Display(CS3DebugType::CL_Undefined, TEXT("v=================%d"), skillID);
// 	}
}

void USkillInterface::CloseBuffExtraSkillBar_Implementation()
{
	//移除额外技能栏
	BuffExtraSkillIDs.Empty();
}

void USkillInterface::ShowBuffExtraFaBaoSkillBar_Implementation(const FString& SkillIDStr)
{
	BuffExtraFaBaoSkillIDs.Empty();
	//显示额外法宝技能栏
	if (SkillIDStr.IsEmpty())
	{
		return;
	}

	TArray<FString> SkillIDStrList = UGolbalBPFunctionLibrary::SplitString(SkillIDStr, false, TEXT("|"));
	for (FString IT : SkillIDStrList)
	{
		BuffExtraFaBaoSkillIDs.Add(FSTRING_TO_INT(IT));
	}

	// 	for (auto skillID : BuffExtraFaBaoSkillIDs)
	// 	{
	// 		CS3_Display(CS3DebugType::CL_Undefined, TEXT("v=================%d"), skillID);
	// 	}
}

void USkillInterface::CloseBuffExtraFaBaoSkillBar_Implementation()
{
	//移除额外法宝技能栏
	BuffExtraFaBaoSkillIDs.Empty();  
}

void USkillInterface::BeCapture_Implementation(const int32& SourceEntityID,const int32& DesEntityID, 
	const FString& Slot, const FVector &Position, const FVector &direction)
{
	if (UUECS3GameInstance::pKBEApp == nullptr)
	{
		return;
	}
	KBEngine::Entity* ControlEntity = UUECS3GameInstance::pKBEApp->FindEntity(DesEntityID);
	KBEngine::Entity* SourceEntity = UUECS3GameInstance::pKBEApp->FindEntity(SourceEntityID);
	if (SourceEntity && ControlEntity && IsValid(SourceEntity->Actor()) && IsValid(ControlEntity->Actor()))
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("USkillInterface::BeCapture[EntityId=%d]"), SourceEntity->ID());
		AServerCharacter* SourceEntityActor = Cast<AServerCharacter>(SourceEntity->Actor());

		//关闭碰撞
		SourceEntityActor->GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
		//绑定
		SourceEntityActor->GetRootComponent()->SetAbsolute(false, false, true);
		SourceEntityActor->AttachToComponent(Cast<AServerCharacter>(ControlEntity->Actor())->GetMesh(), 
			FAttachmentTransformRules::SnapToTargetNotIncludingScale, FSTRING_TO_FNAME(Slot));
		
		//关闭重力
		if (SourceEntity->ClassName() == "Role")
		{
			if (IsValid(SourceEntityActor->Controller))
				SourceEntityActor->Controller->StopMovement();//非玩家没有Controller
			SourceEntityActor->GetCharacterMovement()->Velocity = FVector();
			SourceEntityActor->GetCharacterMovement()->SetMovementMode(EMovementMode::MOVE_Flying);
			SourceEntityActor->SetBaseGravityScale(0.0f);
		}
		//设置本地坐标偏移
		SourceEntityActor->SetActorRelativeLocation(Position);
		SourceEntityActor->SetActorRelativeRotation(FRotator(direction.Y, direction.Z, direction.X));
		//关闭服务器位置同步

		if (!SourceEntity->IsPlayer())
		{
			AServerCharacter* OtherCharacter = Cast<AServerCharacter>(SourceEntityActor);
			if (OtherCharacter)
			{
				OtherCharacter->SetEnableSyncServerPos(false);
			}
		}
	}
}

void USkillInterface::BeReleased_Implementation(const int32& SourceEntityID)
{
	if (UUECS3GameInstance::pKBEApp == nullptr)
	{
		return;
	}
	KBEngine::Entity* SourceEntity = UUECS3GameInstance::pKBEApp->FindEntity(SourceEntityID);
	if (SourceEntity && SourceEntity->Actor())
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("USkillInterface::BeReleased[EntityId=%d]"), SourceEntity->ID());
		AServerCharacter* SourceEntityActor = Cast<AServerCharacter>(SourceEntity->Actor());

		//解绑并设置朝向
		SourceEntityActor->DetachFromActor(FDetachmentTransformRules::KeepWorldTransform);
		SourceEntityActor->SetActorRotation(FRotator(0.f, SourceEntity->Actor()->GetActorRotation().Yaw, 0.f));
		//更新碰撞
		SourceEntityActor->GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	
		if (SourceEntity->ClassName() != "Role")
		{
			//贴地
			SourceEntityActor->SetActorLocation(Cast<AServerCharacter>(SourceEntity->Actor())->FloorTrace(SourceEntity->Actor()->GetActorLocation()));
		}

		if (SourceEntity->ClassName() == "Role")
		{
			SourceEntityActor->GetCharacterMovement()->SetMovementMode(EMovementMode::MOVE_Walking);
			//开启重力
			if (SourceEntity->ID() == UGolbalBPFunctionLibrary::GetPlayerID())
			{
				SourceEntityActor->SetBaseGravityScale(5.0f);
			}
			else
			{
				SourceEntityActor->SetBaseGravityScale(1.0f);
			}
		}

		if (!SourceEntity->IsPlayer())
		{
			if (!SourceEntity->IsPlayer())
			{
				AServerCharacter* OtherCharacter = Cast<AServerCharacter>(SourceEntityActor);
				if (OtherCharacter)
				{
					OtherCharacter->SetEnableSyncServerPos(true);
				}
			}
		}
	}
}

void  USkillInterface::SkillTurnToPos_Implementation(const FVector& Position)
{
	if (GetEntity()->IsPlayer())
	{
		UAtkStateMar* AtkStateMar = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar();
		if (IsValid(AtkStateMar)&&AtkStateMar->IsActivateState(EATTACT_STATE::NULL_ATT))
		{
			return;
		}
	}
	AServerCharacter* PlayerActor = Cast<AServerCharacter>(GetEntity()->Actor());
	if(PlayerActor)
	{
		FVector StartLoction = PlayerActor->GetActorLocation();
		FRotator Rotation = UGolbalBPFunctionLibrary::GetLookAtRotator(StartLoction, Position);
		PlayerActor->SetActorRotation(Rotation);
	}
}



void USkillInterface::RequestInitiaiveStopBuffEvent(const FString& buffIndex)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:RequestInitiaiveStopBuffEvent : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray Args;
	Args.Add(buffIndex);
	GetEntity()->CellCall(TEXT("onInitiaiveStopBuffEvent"), Args);
}

bool USkillInterface::CheckSkillUseCondition(int32 SkillID)
{
	if (!IsValid(UUECS3GameInstance::Instance)) return false;
	USkillManager* SkillManager = UUECS3GameInstance::Instance->SkillManager;
	if (!IsValid(SkillManager)) return false;
	USkillData* SkillData = SkillManager->GetSkillDataById(SkillID);
	if (!IsValid(SkillData))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFightAssist::CheckSkillUseCondition : SkillData!"));
		return false;
	}
	if (SkillData->IsPassiveSkill())
	{
		return false;				//被动技能不能主动使用
	}
	if (SkillData->IsCoolDowning())
	{
		return false;
	}

	bool CheckReslut = true;
	TArray<FSKILL_REQUIRE> CasterRequireDefineList = SkillData->GetCasterRequireList();
	for (FSKILL_REQUIRE RequireData : CasterRequireDefineList)
	{
		switch (RequireData.Type)
		{
		case ENUM_SKILL_REQUIRE_TYPE::RequireHp:
		{
			int32 HP = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("HP"));
			int32 HP_Max = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("HP_Max"));
			int32 RequireValue = FSTRING_TO_INT(RequireData.Param1) + int(HP_Max * FSTRING_TO_FLOAT(RequireData.Param2));
			CheckReslut = HP >= RequireValue ? true : false;
			if (!CheckReslut)
			{
				return CheckReslut;
			}
			break;
		}
		case ENUM_SKILL_REQUIRE_TYPE::RequireMp:
		{
			int32 MP = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("MP"));
			int32 MP_Max = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("MP_Max"));
			int32 RequireValue = FSTRING_TO_INT(RequireData.Param1) + int(MP_Max * FSTRING_TO_FLOAT(RequireData.Param2));
			CheckReslut = MP >= RequireValue ? true : false;
			if (!CheckReslut)
			{
				return CheckReslut;
			}
			break;
		}
		case ENUM_SKILL_REQUIRE_TYPE::RequireGangQi:
		{
			int32 gangQiValue = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("gangQiValue"));
			int32 gangQiValue_Max = UGolbalBPFunctionLibrary::GetIntPropertyValue(EntityID, TEXT("gangQiValue_Max"));
			int32 RequireValue = FSTRING_TO_INT(RequireData.Param1) + int(gangQiValue_Max * FSTRING_TO_FLOAT(RequireData.Param2));
			CheckReslut = gangQiValue >= RequireValue ? true : false;
			if (!CheckReslut)
			{
				return CheckReslut;
			}
			break;
		}
		default:
		{
			break;
		}
		}
	}
	return true;
}

bool USkillInterface::RequestInitiaiveStopSkillEvent()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::RequestInitiaiveStopSkillEvent : GetEntity()!"));
		return false;
	}
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->SkillManager))
	{
		USkillData* SkillData = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(CastingSkill);
		if (IsValid(SkillData) && SkillData->CanInitiaiveInterrupt())
		{
			KBEngine::FVariantArray Args;
			GetEntity()->CellCall(TEXT("onInitiaiveStopSkillEvent"), Args);
			return true;
		}
	}
	return false;
}

void USkillInterface::OnMountCarrier_Implementation(const FString& modelID)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (PlayerCharacter)
	{
		PlayerCharacter->RideCarrierComponent->RideOnCarrier(modelID);
	}
}

void USkillInterface::OnDisMountCarrier_Implementation()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (PlayerCharacter)
	{
		PlayerCharacter->RideCarrierComponent->DisRideOnCarrier();
	}
}

void USkillInterface::CLIENT_RotateCamera_Implementation(const FString& Rotaitones , const float& ArmLength)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (PlayerCharacter)
	{
		TArray<FString> Rotators = UGolbalBPFunctionLibrary::SplitString(Rotaitones);
		PlayerCharacter->AddControllerPitchInput(FSTRING_TO_INT(Rotators[0]));
		PlayerCharacter->AddControllerYawInput(FSTRING_TO_INT(Rotators[1]));
		PlayerCharacter->AddControllerRollInput(FSTRING_TO_INT(Rotators[2]));
		UGolbalBPFunctionLibrary::SetCameraTargetArmLength(PlayerCharacter->SpringArmCompent, ArmLength);
	}
}

void USkillInterface::Frozee()
{
	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(GetActor());
	if (!IsValid(ServerCharacter))
	{
		return; 
	}

	if (ServerCharacter->bIsChangeAppearanceling)
	{
		TWeakObjectPtr<USkillInterface> DelayThisPtr(this);
		TWeakObjectPtr<AServerCharacter> DelayServerCharacterPtr(ServerCharacter);
		if (FrozeeDelegateHandle.IsValid())
		{
			ServerCharacter->OnModelChangeAppearanceOverDelegate.Remove(FrozeeDelegateHandle);
			FrozeeDelegateHandle.Reset();
		}
		FrozeeDelegateHandle = ServerCharacter->OnModelChangeAppearanceOverDelegate.AddLambda([
			DelayThisPtr, DelayServerCharacterPtr]()
			{
				if (DelayThisPtr.IsValid() && DelayServerCharacterPtr.IsValid())
				{
					USkillInterface* ThisPtr = DelayThisPtr.Get();
					AServerCharacter* ServerCharacter = DelayServerCharacterPtr.Get();
					if (IsValid(ThisPtr) && IsValid(ServerCharacter))
					{
						ThisPtr->StartFrozee();
						ServerCharacter->OnModelChangeAppearanceOverDelegate.Remove(ThisPtr->FrozeeDelegateHandle);
					}
				}
			});
	}
	else
	{
		StartFrozee();
	}
}

void USkillInterface::StartFrozee()
{
	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(GetActor());
	if (!IsValid(ServerCharacter))
	{
		return;
	}

	TArray<USceneComponent*> ComponentList;
	ServerCharacter->GetMesh()->GetChildrenComponents(false, ComponentList);
	ComponentList.Insert(ServerCharacter->GetMesh(), 0);
	for (USceneComponent* Component : ComponentList)
	{
		USkeletalMeshComponent* SkeletalMeshCpt = Cast<USkeletalMeshComponent>(Component);
		if (IsValid(SkeletalMeshCpt))
		{
			SkeletalMeshCpt->SetForcedLOD(SkeletalMeshCpt->PredictedLODLevel + 1);
			SkeletalMeshCpt->bPauseAnims = true;
			SkeletalMeshCpt->SuspendClothingSimulation();
		}
	}
}

void USkillInterface::Unfreeze()
{
	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(GetActor());
	if (!IsValid(ServerCharacter))
	{
		return;
	}

	TArray<USceneComponent*> ComponentList;
	ServerCharacter->GetMesh()->GetChildrenComponents(false, ComponentList);
	ComponentList.Insert(ServerCharacter->GetMesh(), 0);
	for (USceneComponent* Component : ComponentList)
	{
		USkeletalMeshComponent* SkeletalMeshCpt = Cast<USkeletalMeshComponent>(Component);
		if (IsValid(SkeletalMeshCpt))
		{
			SkeletalMeshCpt->bPauseAnims = false;
			SkeletalMeshCpt->ResumeClothingSimulation();
			SkeletalMeshCpt->SetForcedLOD(0); 
		}
	}
	ServerCharacter->StopAction();
}

void USkillInterface::CLIENT_AutoRise_Implementation(const float& UpSpeed, 
	const float& RightSpeed, const float& CameraLength)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (!PlayerActor || !PlayerActor->ActorIsPlayer())
	{
		return;
	}
	PlayerActor->FeiShengUpSpeed = UpSpeed * 100.0f;
	PlayerActor->FeiShengRightSpeed = RightSpeed * 100.0f;
	PlayerActor->FeiShengCameraLength = CameraLength * 100.0f;
	//切换到飞升模式
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController) && IsValid(PlayerController->GetAtkStateMar()))
	{
		PlayerController->GetAtkStateMar()->SwitchFeiShengMode(true);
	}
	//设置飞升时平滑的时间
	UAvatarFilterActorComponent* Comp = Cast<UAvatarFilterActorComponent>(
		PlayerActor->GetFilterComponent());
	if (IsValid(Comp))
	{
		Comp->SetSmoothFilterLatencyFrames(10.0f);
	}

}

void USkillInterface::CLIENT_StopRise_Implementation()
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (!PlayerActor || !PlayerActor->ActorIsPlayer())
	{
		return;
	}

	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController) && IsValid(PlayerController->GetAtkStateMar()))
	{
		PlayerController->GetAtkStateMar()->SwitchFeiShengMode(false);
	}
	//这是飞升时平滑的时间
	UAvatarFilterActorComponent* Comp = Cast<UAvatarFilterActorComponent>(
		PlayerActor->GetFilterComponent());
	if (IsValid(Comp))
	{
		Comp->SetSmoothFilterLatencyFrames(0.1f);
	}
}

void USkillInterface::RPC_OnChasePlayerFinish()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::RPC_OnChasePlayerFinish : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("OnChasePlayerFinish"), args);
}

void USkillInterface::RPC_stopRefineSpar()
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::RPC_stopRefineSpar : entity!"));
		return;
	}

	KBEngine::FVariantArray args;

	entity->CellCall(TEXT("stopRefineSpar"), args);
}

bool USkillInterface::ChangePosture(int32 SkilID)
{
	if (SkilID <= 0) return false;
	UUECS3GameInstance* CS3GameInstance = UUECS3GameInstance::Instance;
	if (IsValid(CS3GameInstance))
	{
		if (nullptr != GetEntity() && IsValid(CS3GameInstance->SkillManager) && IsValid(CS3GameInstance->ConstDataBP))
		{
			USkillManager* SkillManager = CS3GameInstance->SkillManager;
			int32 Profession = GetEntity()->GetDefinedProperty(TEXT("profession")).GetValue<int32>();
			TArray<int32> InitPostureSkills = PROFESSION_POSTURE_MAP[Profession];
			TArray<int32> PlayerSkillIdList = SkillManager->GetPlayerSkillIdList();
			for (auto& InitSkillID : InitPostureSkills)
			{
				if (SkilID / 1000 == InitSkillID / 1000) continue;
				for (auto& PlayerSkillId : PlayerSkillIdList)
				{
					if (PlayerSkillId / 1000 == InitSkillID / 1000)
					{
						UseSkill(PlayerSkillId, UGolbalBPFunctionLibrary::GetPlayerID());
						return true;
					}
				}
			}
		}
		CS3GameInstance->MessageManager->ShowMessage(548);
	}
	return false;
}

void USkillInterface::SetCurrentUsePosItemUID(FString itemUID)
{
	if (CurrentUsePosItemUID == itemUID)
	{
		return;
	}
	if (itemUID.IsEmpty() && !CurrentUsePosItemUID.IsEmpty())
	{
		URoleKitBagInterface * Interface = Cast<URoleKitBagInterface>(GetInterfaceByName("RoleKitBagInterface"));
		UItemUse* itemUse = Cast<UItemUse>(Interface->FindItemByUID(CurrentUsePosItemUID));
		if (itemUse)
		{
			itemUse->CancelUseItemToPositionBeforeNotifyServer();
		}
		CurrentUsePosItemUID = itemUID;
	}
	else
	{
		CurrentUsePosItemUID = itemUID;
		URoleKitBagInterface * Interface = Cast<URoleKitBagInterface>(GetInterfaceByName("RoleKitBagInterface"));
		UItemUse* itemUse = Cast<UItemUse>(Interface->FindItemByUID(CurrentUsePosItemUID));
		if (itemUse)
		{
			itemUse->SetUseItemToPositionBeforeNotifyServer();
		}
	}
}

void USkillInterface::CLIENT_OnMonsterCopyEnterPicture_Implementation(const int32& AttributeType)
{
	FString EffectID = TEXT("");
	AMonsterCharacter* monster = Cast<AMonsterCharacter>(GetActor());
	//根据属性类型设置金木水火土对应分身进入画卷的粒子
	switch (AttributeType)
	{
		case 0:
			EffectID = TEXT("102270");
			break;
		case 1:
			EffectID = TEXT("102272");
			break;
		case 2:
			EffectID = TEXT("102274");
			break;
		case 3:
			EffectID = TEXT("102276");
			break;
		case 4:
			EffectID = TEXT("102278");
			break;
		default:
		{
			EffectID = TEXT("102270");
		}
	}
	if (IsValid(monster))
	{
		UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(monster->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
		DefaultStaticMeshCpt->bReceivesDecals = true;
		int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID, 0.0f, monster, monster);
	}
}

void USkillInterface::CLIENT_OnBulletHitPicture_Implementation(const int32& ResultType, const int32& AttributeType)
{
	FString EffectID = TEXT("");
	AMonsterCharacter* monster = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(monster)) return;
	//根据属性类型设置金木水火土对应分身从画卷中出来的粒子
	switch (AttributeType)
	{
		case 0:
			EffectID = TEXT("102269");
			break;
		case 1:
			EffectID = TEXT("102271");
			break;
		case 2:
			EffectID = TEXT("102273");
			break;
		case 3:
			EffectID = TEXT("102275");
			break;
		case 4:
			EffectID = TEXT("102277");
			break;
		default:
		{
			EffectID = TEXT("102269");
		}
	}
	//击中画卷抖动效果
	monster->BP_OnPictureScrollShake(2000.0, 3.0);
	if (ResultType == 0)
	{
		//击中空白画卷(对应画卷发光)
		monster->SetCustomDepthStncilValue(CUSTOM_DEPTH_STENCIL::CUSTOM_DEEPTH_STENCIL_WXHJ);
	}
	else
	{
		UStaticMeshComponent* DefaultStaticMeshCpt = Cast<UStaticMeshComponent>(monster->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_STATIC));
		//播怪物从画卷中出来的效果（画卷贴花扭曲）
		DefaultStaticMeshCpt->bReceivesDecals = true;
		TWeakObjectPtr<AMonsterCharacter> DelayActorPtr(monster);
		int32 EffectUID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID, 0.0f, monster, monster);
	}
}

void USkillInterface::CLIENT_OnPictureStopHighlight_Implementation()
{
	AMonsterCharacter* monster = Cast<AMonsterCharacter>(GetActor());
	if (!IsValid(monster)) return;
	//停止空白画卷发光
	monster->SetCustomDepthStncilValue(CUSTOM_DEPTH_STENCIL::CUSTOM_DEPTH_STENCIL_NORMAL);
}

void USkillInterface::CLIENT_StartSubmerge_Implementation(const FString& EffectID)
{
	KBEngine::Entity* entity = GetEntity();
	if (!entity)
	{
		return;
	}
	float Speed = entity->GetDefinedProperty(TEXT("speed"));
	
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, Submerge, FTimerDelegate::CreateLambda([this, EffectID]()
		{
			// 判断Actor是否有效
			if (!IsValid(GetActor()))
			{
				for (auto UID : BuffUIDList)
				{
					UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(UID);
				}
				if (IsValid(UUECS3GameInstance::Instance))
				{
					UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(Submerge);
				}

				return;
			}
			this->BuffUIDList.Add(UUECS3GameInstance::Instance->ParticleManager->PlayParticle(EffectID, 0.f, GetActor(), GetActor()));

		}), 1.f / Speed, true);
	}
}

void USkillInterface::CLIENT_EndSubmerge_Implementation()
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(Submerge);
	}

	for (auto UID : BuffUIDList)
	{
		UUECS3GameInstance::Instance->ParticleManager->StopEffectByUID(UID);
	}
}

void USkillInterface::CLIENT_StartFog_Implementation(const int32& TargetID, const FString& Albedo, const FString& ExtinctionMulity, const FString& HoleRadius, const FString& InsideExtinction, const FString& OutsideExtinction, const float& EnterTime)
{

}

void USkillInterface::CLIENT_EndFog_Implementation()
{

}

void USkillInterface::RPC_onStopFlyPatrol(FString CurFlyPatrolID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::RPC_onStopFlyPatrol : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(CurFlyPatrolID);
	entity->CellCall(TEXT("removeFlyPatrolEffectList"), Args);
	entity->CellCall(TEXT("onStopFlyPatrol"), Args);
}

void USkillInterface::RPC_onBulletCollisionBegin(KBEngine::FVariantArray args)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::RPC_onBulletCollisionBegin : entity!"));
		return;
	};
	entity->CellCall(TEXT("onBulletCollisionBegin"), args);
}

void USkillInterface::onBulletCollisionArrive(KBEngine::FVariantArray args)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::onBulletCollisionArrive : entity!"));
		return;
	};
	entity->CellCall(TEXT("onBulletCollisionArrive"), args);
}

void USkillInterface::CLIENT_FirstLearnSkillNotify_Implementation(const int32& SkillID)
{
	//触发首次学习技能：参数为：SkillID 技能ID
	UGolbalBPFunctionLibrary::TutorialManager()->OnFirstLearnSkill(SkillID);
}

void USkillInterface::CLIENT_RoleChaseEntity_Implementation(
	const int32& SkillID, const int32& TargetID, const float& Distance, const float& Speed)
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(PlayerController) || !IsValid(PlayerCharacter))
	{
		return;
	}

	AActor* MoveToTarget = UGolbalBPFunctionLibrary::GetActorByID(TargetID);
	const FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	CacheSkillID = SkillID;
	CacheMaxWalkSpeed = PlayerCharacter->GetCharacterMovement()->MaxWalkSpeed;
	CacheMaxAcceleration = PlayerCharacter->GetCharacterMovement()->MaxAcceleration;
	PlayerCharacter->SetMaxWalkSpeed(Speed * 100.0f);
	PlayerCharacter->GetCharacterMovement()->MaxAcceleration = 20000.0f;//使角色快速达到最大速度MaxWalkSpeed
	
	float NewDistance = Distance;
	float CapsuleRadius = PlayerCharacter->GetCapsuleComponent()->GetScaledCapsuleRadius();
	//下面公式是UAIBlueprintHelperLibrary::SimpleMoveToLocation里面的计算能移动到目标位置的最小距离的算法
	//UPathFollowingComponent::HasReachedInternal 1202行
	const float UseRadius = 3.4f + (CapsuleRadius * 1.1);
	if (Distance * 100.0f < UseRadius)
	{
		NewDistance = UseRadius * 0.01f;//这里判断计算是为了让角色永远能触发移动到目标位置
	}

	if (!PlayerController->MoveControlComponent->OnPlayerMoveTypeChange.IsAlreadyBound(this,
		&USkillInterface::OnAddEventChangMoveType))
	{
		PlayerController->MoveControlComponent->OnPlayerMoveTypeChange.AddDynamic(this,
			&USkillInterface::OnAddEventChangMoveType);
	}

	TWeakObjectPtr<USkillInterface> DelayThisPtr(this);
	PlayerController->MoveControlComponent->TraceTargetPostion(
		MoveToTarget->GetActorLocation(), NewDistance,
		FTraceCallback::CreateLambda([DelayThisPtr](bool IsSuccess)
			{
				if (DelayThisPtr.IsValid() && IsSuccess)
				{
					USkillInterface* ThisPtr = DelayThisPtr.Get();
					ThisPtr->CLIENT_RoleChaseEntityEnd();
					ThisPtr->RPC_OnRoleChaseEntityOver(ThisPtr->CacheSkillID, true);
				}
			}));

	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, RoleChaseEntityHandle,
		FTimerDelegate::CreateLambda([DelayThisPtr, MoveToTarget, NewDistance]()
			{
				ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
				if (IsValid(PlayerController))
				{
					PlayerController->MoveControlComponent->TraceTargetPostion(
						MoveToTarget->GetActorLocation(), NewDistance,
						FTraceCallback::CreateLambda([DelayThisPtr](bool IsSuccess)
							{
								if (DelayThisPtr.IsValid() && IsSuccess)
								{
									USkillInterface* ThisPtr = DelayThisPtr.Get();
									ThisPtr->CLIENT_RoleChaseEntityEnd();
									ThisPtr->RPC_OnRoleChaseEntityOver(ThisPtr->CacheSkillID, true);
								}
							}));
				}
			}), 1.0f, true);
}

void USkillInterface::OnAddEventChangMoveType_Implementation(
	CS3_MOVE_TYPE NewMoveType, CS3_MOVE_TYPE OldMoveType)
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController))
	{
		if (NewMoveType == CS3_MOVE_TYPE::MOVE_TYPE_CONTROL &&
			OldMoveType == CS3_MOVE_TYPE::MOVE_TYPE_AUTO_NAVIGATE)
		{
			CLIENT_RoleChaseEntityEnd();
			RPC_OnRoleChaseEntityOver(CacheSkillID, true);
			PlayerController->MoveControlComponent->OnPlayerMoveTypeChange.RemoveDynamic(this,
				&USkillInterface::OnAddEventChangMoveType);
		}
	}
}


void USkillInterface::CLIENT_RoleChaseEntityEnd_Implementation()
{
	UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(RoleChaseEntityHandle);
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if(IsValid(PlayerCharacter))
	{
		PlayerCharacter->SetMaxWalkSpeed(CacheMaxWalkSpeed);
		PlayerCharacter->GetCharacterMovement()->MaxAcceleration = CacheMaxAcceleration;
	}
}

void USkillInterface::RPC_OnRoleChaseEntityOver(const int32& SkillID, const int32& isSuccess)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::RPC_OnRoleChaseEntityOver : entity!"));
		return;
	};
	KBEngine::FVariantArray Args;
	Args.Add(SkillID);
	Args.Add(isSuccess);
	entity->CellCall(TEXT("onRoleChaseEntityOver"), Args); 
}

void USkillInterface::CLIENT_RoleChargePosition_Implementation(
	const FVector &Position, const float& Speed)
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	CacheMaxWalkSpeed = PlayerCharacter->GetCharacterMovement()->MaxWalkSpeed;
	CacheMaxAcceleration = PlayerCharacter->GetCharacterMovement()->MaxAcceleration;
	PlayerCharacter->SetMaxWalkSpeed(Speed * 100.0f);
	PlayerCharacter->GetCharacterMovement()->MaxAcceleration = 20000.0f;//使角色快速达到最大速度MaxWalkSpeed

	TWeakObjectPtr<USkillInterface> DelayThisPtr(this);
	PlayerController->MoveControlComponent->TraceTargetPostion(Position, 0.1f,
		FTraceCallback::CreateLambda([DelayThisPtr, PlayerCharacter](bool IsSuccess)
			{
				if (DelayThisPtr.IsValid())
				{
					USkillInterface* ThisPtr = DelayThisPtr.Get();
					PlayerCharacter->SetMaxWalkSpeed(ThisPtr->CacheMaxWalkSpeed);
					PlayerCharacter->GetCharacterMovement()->MaxAcceleration = ThisPtr->CacheMaxAcceleration;
				}
			}));
}


void USkillInterface::CLIENT_OnMountSlide(const float& DelayTime, const float & SpeedScale, const float & ASpeed, const FString & ModelID, const float & InputYawScale, const int32& IsNewBuff)
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(GetActor());
	if (IsValid(Player))
	{
		if (Player->RideCarrierComponent)
		{
			Player->RideCarrierComponent->RideOnCarrier(ModelID);
		}

		UCustomTimerManager* TimeMgr = UUECS3GameInstance::Instance->CustomTimerManager;
		if (Player->ActorIsPlayer() && IsValid(TimeMgr))
		{
			if (TimeMgr->IsTimerActive(DelayMove))
			{
				UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(DelayMove);
			}

			MoveScale = SpeedScale;
			AccelerateSpeed = ASpeed;

			ACS3PlayerController* Controller = UGolbalBPFunctionLibrary::GetCS3PlayerController();
			if (IsValid(Controller))
			{
				CameraHandle = Controller->SetCameraRotateScale(InputYawScale / Controller->InputYawScale, CameraHandle);
			}
			Player->SetWalkOffLedges(false);
			IsNewSkiBuff = bool(IsNewBuff); // 这是旧滑雪效果的Buff
			TimeMgr->SetTimer(DelayMove, this, &USkillInterface::OnMountSlideFinishRideOnModel, DelayTime, false);

		}

	}
}

void USkillInterface::OnMountSlideFinishRideOnModel_Implementation()
{
	ACS3PlayerController* Control = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(Control))
	{
		Control->GetAtkStateMar()->SwitchMiJingMode(true);

	}

	APlayerCharacter* Player = Cast<APlayerCharacter>(GetActor());
	if (IsValid(Player))
	{
		Player->SetWalkOffLedges(true);
	}
}

void USkillInterface::CLIENT_OnDismountSlide_Implementation()
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(GetActor());
	if (Player && Player->ActorIsPlayer())
	{
		ACS3PlayerController* Controller = UGolbalBPFunctionLibrary::GetCS3PlayerController();
		if (IsValid(Controller))
		{
			Controller->RemoveCameraRotateScale(CameraHandle);
			Controller->GetAtkStateMar()->SwitchMiJingMode(false);
		}
		if (IsValid(Player->SpringArmCompent))
		{
			UGolbalBPFunctionLibrary::SetCameraSocketOffset(Player->SpringArmCompent, FVector(-300.f, 0.f, 0.f));
		}
	}
	Player->RideCarrierComponent->DisRideOnCarrier();
}


void USkillInterface::EnterDark_Implementation()
{

}

void USkillInterface::LeaveDark_Implementation()
{

}

void USkillInterface::CLIENT_TurnOnLight_Implementation(const float& lightRange)
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(Player))
	{
		return;
	}
	USkeletalMeshComponent* HairMeshCpt = Cast<USkeletalMeshComponent>(Player->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_HAIRS));
	USkeletalMeshComponent* AdornMeshCpt = Cast<USkeletalMeshComponent>(Player->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_ADORN));
	if (IsValid(HairMeshCpt))
	{
		HairMeshCpt->LightingChannels.bChannel0 = false;
		HairMeshCpt->MarkRenderStateDirty();
	}

	if (IsValid(AdornMeshCpt))
	{
		AdornMeshCpt->LightingChannels.bChannel0 = false;
		AdornMeshCpt->MarkRenderStateDirty();
	}
}

void USkillInterface::CLIENT_TurnOffLight_Implementation()
{
	APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
	if (!IsValid(Player))
	{
		return;
	}

	USkeletalMeshComponent* HairMeshCpt = Cast<USkeletalMeshComponent>(Player->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_HAIRS));
	USkeletalMeshComponent* AdornMeshCpt = Cast<USkeletalMeshComponent>(Player->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_ADORN));
	if (IsValid(HairMeshCpt))
	{
		HairMeshCpt->LightingChannels.bChannel0 = true;
		HairMeshCpt->MarkRenderStateDirty();
	}

	if (IsValid(AdornMeshCpt))
	{
		AdornMeshCpt->LightingChannels.bChannel0 = true;
		AdornMeshCpt->MarkRenderStateDirty();
	}
}

/*--------------------------------玩家被动技能栏-------------------------------------------------*/
void USkillInterface::InitPassiveSkillBar(const FVariant& datas)
{
	FPASSIVE_SKILL_BAR_DATAS* _datas = new FPASSIVE_SKILL_BAR_DATAS(datas);
	for (auto i : _datas->datas)
	{
		if (passiveSkillBarData.Contains(i.id))
		{
			passiveSkillBarData.Remove(i.id);
		}
		passiveSkillBarData.Add(i.id, i);
	}
}

void USkillInterface::RPC_requestUnlockPassiveSkillBar(int32 index)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::RPC_requestUnlockPassiveSkillBar : entity!"));
		return;
	};

	if (!passiveSkillBarData.Contains(index)) return;
	if (passiveSkillBarData[index].isLock == 0) return;
	if (!IsCanUnlockPassiveSkillBar(index)) return;
	
	KBEngine::FVariantArray Args;
	Args.Add(index);
	entity->CellCall(TEXT("requestUnlockPassiveSkillBar"), Args);
}

bool USkillInterface::IsCanUnlockPassiveSkillBar(int32 index)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::IsCanUnlockPassiveSkillBar : entity!"));
		return false;
	};

	//判断前面的栏位是否已经解锁
	if (passiveSkillBarData.Contains(index - 1) && (passiveSkillBarData[index - 1].isLock != 0))
	{
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(5300);
		return false;
	}

	const UConfigTable* datas = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_PASSIVESKILLBAR_DATA);
	TArray<FName> rows = datas->GetRowNames();
	for (auto row : rows)
	{
		const FPASSIVESKILLBAR_DATA* data = datas->GetRow<FPASSIVESKILLBAR_DATA>(row);
		if (data->id == index)
		{
			int32 level = UGolbalBPFunctionLibrary::GetIntPropertyValue(entity->ID(), TEXT("level")); 
			if (data->level > level)
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(5301);
				return false;
			}
			URoleInterface* RoleInterface = Cast<URoleInterface>(UGolbalBPFunctionLibrary::GetCS3PlayerEntity() ? UGolbalBPFunctionLibrary::GetCS3PlayerEntity()->Interface_Cache.GameObjectInterface : nullptr);
			int64 money = RoleInterface->GetMoney();
			if (data->money > money)
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(5302);
				return false;
			}
			int32 xianshi = UGolbalBPFunctionLibrary::GetIntPropertyValue(entity->ID(), TEXT("xianshi"));
			if (data->xianshi > xianshi)
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(5303);
				return false;
			}

			URoleKitBagInterface* kitbatInst = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
			int32 num = kitbatInst->GetAmountByKBType(EKITBAGTYPE::COMMON, data->material_1, FIND_BINDTYPE_ENUM::NONE_BIND);
			if (num < data->mNum_1)
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(5304);
				return false;
			}
			num = kitbatInst->GetAmountByKBType(EKITBAGTYPE::COMMON, data->material_2, FIND_BINDTYPE_ENUM::NONE_BIND);
			if (num < data->mNum_2)
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(5304);
				return false;
			}
			num = kitbatInst->GetAmountByKBType(EKITBAGTYPE::COMMON, data->material_3, FIND_BINDTYPE_ENUM::NONE_BIND);
			if (num < data->mNum_3)
			{
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(5304);
				return false;
			}
		}
	}
	return true;
}

void USkillInterface::RPC_requestCancelUnActivatePassiveSkill(int32 index)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::RPC_requestCancelUnActivatePassiveSkill : entity!"));
		return;
	};

	if (!passiveSkillBarData.Contains(index)) return;
	if (passiveSkillBarData[index].isLock != 0) return;
	if (passiveSkillBarData[index].skillID == 0) return;

	KBEngine::FVariantArray Args;
	Args.Add(index);
	entity->CellCall(TEXT("requestCancelUnActivatePassiveSkill"), Args);
}

void USkillInterface::RPC_requestActivatePassiveSkill(int32 skillID, int32 index)
{
	if (!passiveSkillBarData.Contains(index))return;
	if (passiveSkillBarData[index].isLock != 0) return;
	if (passiveSkillBarData[index].skillID == skillID) return;

	TArray<int32> PlayerSkillIdList = UUECS3GameInstance::Instance->SkillManager->GetPlayerSkillIdList();
	if (!PlayerSkillIdList.Contains(skillID)) return;

	USkillData* SkillData = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(skillID);
	if (IsValid(SkillData) && SkillData->IsPassiveSkill())
	{
		KBEngine::Entity* entity = GetEntity();
		if (entity == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:USkillInterface::RPC_requestActivatePassiveSkill : entity!"));
			return;
		};

		KBEngine::FVariantArray Args;
		Args.Add(skillID);
		Args.Add(index);
		entity->CellCall(TEXT("requestActivatePassiveSkill"), Args);
	}
}

void USkillInterface::updatePassiveSkillBar(const FVariant& data)
{
		FPASSIVE_SKILL_BAR_DATA* _data = new FPASSIVE_SKILL_BAR_DATA(data);
		if (passiveSkillBarData.Contains(_data->id))
		{
			passiveSkillBarData.Remove(_data->id);
		}
		passiveSkillBarData.Add(_data->id, *_data);
		BP_updatePassiveSkillBar(_data->id);
}

void USkillInterface::GetPassiveSkillBarData(int32 id, uint8& isLock, int32& skillID)
{
	isLock = 1;//锁住
	skillID = 0;

	if (passiveSkillBarData.Contains(id))
	{
		isLock = passiveSkillBarData[id].isLock;
		skillID = passiveSkillBarData[id].skillID;
	}
}

bool USkillInterface::CheckPassiveSkillActiveSate(int32 SkillID)
{
	for (TPair<int32, FPASSIVE_SKILL_BAR_DATA>& passiveSkillData : passiveSkillBarData)
	{
		if (passiveSkillData.Value.skillID == SkillID)
		{
			return true;
		}
	}
	return false;
}

void USkillInterface::IntensifySkill(const int32 & QuickID, const int32 &PassiveSkillLevel, const int32 & SkillLevel)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuickBarManager))
	{
		//保存被动技能持有进阶效果
		UUECS3GameInstance::Instance->QuickBarManager->AddPassiveHoldEffectData(QuickID, PassiveSkillLevel, SkillLevel);
	}
}

void USkillInterface::CancelIntensifySkill(const int32 & QuickID, const int32 &PassiveSkillLevel, const int32 & SkillLevel)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->QuickBarManager))
	{
		//保存被动技能持有进阶效果
		UUECS3GameInstance::Instance->QuickBarManager->RemovePassiveHoldEffectData(QuickID, PassiveSkillLevel, SkillLevel);
	}
}

void USkillInterface::RPC_AddFlyPatrolEffectList(const FString & FlyPatrolID, const TArray<int32>& HoldEffectList)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--USkillInterface::RPC_AddFlyPatrolEffectList no this Entity!"));
		return;
	}
	KBEngine::FVariantArray Args;
	Args.Add(FlyPatrolID);
	Args.Add(UGolbalBPFunctionLibrary::ListToFVariant(HoldEffectList));
	entity->CellCall(TEXT("addFlyPatrolEffectList"), Args);

}

void USkillInterface::RPC_RemoveFlyPatrolEffectList(const FString & FlyPatrolID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("--USkillInterface::RPC_RemoveFlyPatrolEffectList no this Entity!"));
		return;
	}
	KBEngine::FVariantArray Args;
	Args.Add(FlyPatrolID);
	entity->CellCall(TEXT("removeFlyPatrolEffectList"), Args);
}

void USkillInterface::OnCreateTrace(const int32 & EntityID_, const FString & EffectID, const float & DrawDist, const float & LifeTime, const int32& Width, const int32& Hight, const int32 & SkillID)
{
	USkillInterface* TSInterface = Cast<USkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(USkillInterface::GetName(), EntityID_));
	if (IsValid( TSInterface))
	{
		TSInterface->OnCreateSelfTraceBP(EffectID, DrawDist, LifeTime, Width, Hight, SkillID);
	}
}

void USkillInterface::OnFinishCreateTrace(const int32 & EntityID_)
{
	USkillInterface* TSInterface = Cast<USkillInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(USkillInterface::GetName(), EntityID_));
	if (IsValid(TSInterface))
	{
		TSInterface->OnFinishCreateSelfTraceBP();
	}
}

void USkillInterface::EnterToxicosis()
{
}

void USkillInterface::LeaveToxicosis()
{
}

void USkillInterface::CLIENT_OnMountStone_Implementation(const int32& EntityID_, const int32& BBegin)
{
// 	if (AActor* Actor_ = UGolbalBPFunctionLibrary::GetActorByID(EntityID_))
// 	{
// 		UMonsterInterface* monsterInterface = Cast<UMonsterInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("GameObjectInterface"), EntityID_));
// 		if (IsValid(monsterInterface))
// 		{
// 			monsterInterface->OnMountStone(EntityID, BBegin);
// 		}
// 	}
// 	else
// 	{
// 		FindCharacterTime = 0;
// 		TWeakObjectPtr<USkillInterface> DelaySkill(this);
// 
// 		UGolbalBPFunctionLibrary::CustomTimerManager()->SetTimer(DelaySkill, FindCharacterHandle, FTimerDelegate::CreateLambda[DelaySkill](EntityID_, BBegin)
// 		{
// 			USkillInterface* skillThis = DelaySkill.Get();
// 			if (IsValid(skillThis))
// 			{
// 				if (AActor* Actor_ = UGolbalBPFunctionLibrary::GetActorByID(EntityID_))
// 				{
// 					UMonsterInterface* monsterInterface = Cast<UMonsterInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("GameObjectInterface"), EntityID_));
// 					if (IsValid(monsterInterface))
// 					{
// 						monsterInterface->OnMountStone(EntityID, BBegin);
// 						UGolbalBPFunctionLibrary::CustomTimerManager()->ClearTimer(skillThis->FindCharacterHandle);
// 						return;
// 					}
// 				}
// 				skillThis->FindCharacterTime += 1;
// 				if (skillThis->FindCharacterTime >= 5)
// 				{
// 					UGolbalBPFunctionLibrary::CustomTimerManager()->ClearTimer(skillThis->FindCharacterHandle);
// 				}
// 			}
// 
// 		}
// 			
// 		)
// 	}
}

void USkillInterface::CLIENT_OnDisMountStone_Implementation(const int32& EntityID_)
{
// 	UMonsterInterface* monsterInterface = Cast<UMonsterInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("GameObjectInterface"), EntityID_));
// 	if (IsValid(monsterInterface))
// 	{
// 		monsterInterface->OnDisMountStone(EntityID);
// 	}
}

void USkillInterface::CLIENT_ForcedJump_Implementation(float Height)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor) || IsValid(PlayerActor->JumpComponent))
	{
		PlayerActor->JumpComponent->OnStartPassiveJump(Height);
	}
}

void USkillInterface::CLIENT_StopFlyPatrol_Implementation(const FString& FlyPatrolID)
{
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(GetActor());
	if (IsValid(PlayerActor))
	{	
		 ///<停止飞行传送
		if (FlyPatrolID.IsEmpty()|| !FlyPatrolID.Compare(""))
		{
			if (PlayerActor->ActorIsPlayer())
			{
				PlayerActor->SwitchOffFlyOrbitMode();
			}
			else
			{
				PlayerActor->StopFlyPatrol();
			}			
		}
		else
		{
			PlayerActor->StopCycleFlyPatrol(FlyPatrolID);
		}
	}
}

void USkillInterface::StartOverLookScene_Implementation(const FString& CameraLoaction, const FString& CameraRotation, float StartTime, float LoopTime, float EndTime)
{

}

void USkillInterface::EndOverLookScene_Implementation(float EndTime)
{

}

void USkillInterface::InitBlueCB()
{
	ArrBlueFunc.Add("SkillInterrupted");
	ArrBlueFunc.Add("SetCastingSkill");
	ArrBlueFunc.Add("CastSkillToTarget");
	ArrBlueFunc.Add("CastSkillToPosition");
	ArrBlueFunc.Add("CastCSkillToTarget");
	ArrBlueFunc.Add("CastCSkillToPosition");
	ArrBlueFunc.Add("intonateSpell");
	ArrBlueFunc.Add("intonateSpellOver");
	ArrBlueFunc.Add("BeHitPlayEffect");
	ArrBlueFunc.Add("HoldEffectPlayEffect");
	ArrBlueFunc.Add("HoldEffectEndEffect");
	ArrBlueFunc.Add("ReceiveSkill");
	ArrBlueFunc.Add("SetCooldown");
	ArrBlueFunc.Add("ClearCooldown");
	ArrBlueFunc.Add("FlyPatrol");
	ArrBlueFunc.Add("OnBeHitBackNew");
	ArrBlueFunc.Add("OnEndHitBack");
	ArrBlueFunc.Add("OnPull");
	ArrBlueFunc.Add("EndPull");
	ArrBlueFunc.Add("OnChargeToPosition");
	ArrBlueFunc.Add("onEndChargeToPosition");
	ArrBlueFunc.Add("ReplaceSkillBar");
	ArrBlueFunc.Add("AddReplaceSkillBar");
	ArrBlueFunc.Add("OnReplaceSkillBarEnd");
	ArrBlueFunc.Add("SetAnimRateScale");
	ArrBlueFunc.Add("StartSkillHitSlow");
	ArrBlueFunc.Add("StopSkillHitSlow");
	ArrBlueFunc.Add("OnChasePlayer");
	ArrBlueFunc.Add("OnStopMoving");
	ArrBlueFunc.Add("OnBuffLayerChange");
	ArrBlueFunc.Add("onCasterSkillEnd");
	ArrBlueFunc.Add("OnResetBuffEndTime");
	ArrBlueFunc.Add("OnNotifyPlayActions");
	ArrBlueFunc.Add("sparShowInfo");
	ArrBlueFunc.Add("intonateSparSpell");
	ArrBlueFunc.Add("intonateSparSpellOver");
	ArrBlueFunc.Add("OnChangePosture");
	ArrBlueFunc.Add("OnBuffBulletBegin");
	ArrBlueFunc.Add("OnBuffBulletEnd");
	ArrBlueFunc.Add("OnBuffBulletMultipleBegin");
	ArrBlueFunc.Add("OnBuffBulletMultipleEnd");
	ArrBlueFunc.Add("InitSkills");
	ArrBlueFunc.Add("OnAddSkill");
	ArrBlueFunc.Add("OnRemoveSkill");
	ArrBlueFunc.Add("ChangeToNormalModelVisible");
	ArrBlueFunc.Add("OnRiseBegin");
	ArrBlueFunc.Add("OnRiseEnd");
	ArrBlueFunc.Add("PlayArtificeSpar");
	ArrBlueFunc.Add("StopArtificeSpar");
	ArrBlueFunc.Add("BuffPlayLinkEffect");
	ArrBlueFunc.Add("BuffEndPlayLinkEffect");
	ArrBlueFunc.Add("PlayBuffEffect");
	ArrBlueFunc.Add("onDodgeSkillHit");
	ArrBlueFunc.Add("DistortScene");
	ArrBlueFunc.Add("EndDistortScene");
	ArrBlueFunc.Add("TeleportToDstPosition");
	ArrBlueFunc.Add("AddShowBuffExtraTips");
	ArrBlueFunc.Add("RemoveBuffExtraTips");
	ArrBlueFunc.Add("ShowBuffExtraSkillBar");
	ArrBlueFunc.Add("CloseBuffExtraSkillBar");
	ArrBlueFunc.Add("ShowBuffExtraFaBaoSkillBar");
	ArrBlueFunc.Add("CloseBuffExtraFaBaoSkillBar");
	ArrBlueFunc.Add("LXDistortScene");
	ArrBlueFunc.Add("SetCatchTargetId");
	ArrBlueFunc.Add("BeCapture");
	ArrBlueFunc.Add("BeReleased");
	ArrBlueFunc.Add("RefreshReplaceSkillBar");
	ArrBlueFunc.Add("SkillTurnToPos");
	ArrBlueFunc.Add("OnRage");
	ArrBlueFunc.Add("EndRage");
	ArrBlueFunc.Add("OnMountCarrier");
	ArrBlueFunc.Add("OnDisMountCarrier");
	ArrBlueFunc.Add("Frozee");
	ArrBlueFunc.Add("Unfreeze");
	ArrBlueFunc.Add("PlayModleHighlight");
	ArrBlueFunc.Add("StartTransparency");
	ArrBlueFunc.Add("EndTransparency");
	ArrBlueFunc.Add("StartHideCharacter");
	ArrBlueFunc.Add("EndHideCharacter");
	ArrBlueFunc.Add("BeHitPlayEffectLocal");
	ArrBlueFunc.Add("OnShowIntonateBar");
	ArrBlueFunc.Add("OnHideIntonateBar");
	ArrBlueFunc.Add("CLIENT_StartSubmerge");
	ArrBlueFunc.Add("CLIENT_EndSubmerge");
	ArrBlueFunc.Add("CLIENT_ControlledOnBeHitBack");
	ArrBlueFunc.Add("CLIENT_ControlledEndHitBack");
	ArrBlueFunc.Add("CLIENT_StartFog");
	ArrBlueFunc.Add("CLIENT_EndFog");
	ArrBlueFunc.Add("OnDissolve");
	ArrBlueFunc.Add("EndDissolve");
	ArrBlueFunc.Add("CLIENT_AutoRise");
	ArrBlueFunc.Add("CLIENT_StopRise");
	ArrBlueFunc.Add("CLIENT_FirstLearnSkillNotify");
	ArrBlueFunc.Add("CLIENT_RotateCamera");
	ArrBlueFunc.Add("CLIENT_OnBulletHitPicture");
	ArrBlueFunc.Add("CLIENT_OnMonsterCopyEnterPicture");
	ArrBlueFunc.Add("CLIENT_OnPictureStopHighlight");
	ArrBlueFunc.Add("CLIENT_RoleChaseEntity");
	ArrBlueFunc.Add("CLIENT_RoleChargePosition");
	ArrBlueFunc.Add("CLIENT_OnMountSlide");
	ArrBlueFunc.Add("CLIENT_OnDismountSlide");
	ArrBlueFunc.Add("CLIENT_RoleChaseEntityEnd");
	ArrBlueFunc.Add("InitPassiveSkillBar");
	ArrBlueFunc.Add("updatePassiveSkillBar");
	ArrBlueFunc.Add("StartOverLookScene");
	ArrBlueFunc.Add("EndOverLookScene");
	ArrBlueFunc.Add("CLIENT_ForcedJump");
	ArrBlueFunc.Add("EnterDark");
	ArrBlueFunc.Add("LeaveDark");
	ArrBlueFunc.Add("CLIENT_TurnOnLight");
	ArrBlueFunc.Add("CLIENT_TurnOffLight");
	ArrBlueFunc.Add("CLIENT_StopFlyPatrol");
	Supper::InitBlueCB();
}
CONTROL_COMPILE_OPTIMIZE_END