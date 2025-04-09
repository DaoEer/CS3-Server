
#include "FightAssist.h"
#include "Components/DecalComponent.h"
#include "Util/ConvertUtil.h"
#include "CS3Base/CS3Entity.h"
#include "Interface/SkillInterface.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Actor/Scene/SceneCharacter.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "Interface/Role/RoleStateInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "GameData/GameDeFine.h"
#include "GameDevelop/CS3PlayerController.h"
#include "GameData/Item/ItemUse.h"
#include "GameData/Item/ItemUseAssist.h"
#include "Particles/ParticleSystemComponent.h"
#include "Actor/Particle/EffectEmitter.h"
#include "Particles/ParticleModule.h"
#include "Particles/TypeData/ParticleModuleTypeDataMesh.h"
#include "Component/Role/CameraCaptureTranslucentComponent.h"
#include "Particles/ParticleLODLevel.h"
#include "Particles/ParticleEmitter.h"
#include "Manager/ParticleManager.h"
#include "Manager/MessageManager.h"
#include "GameData/MessageID.h"
#include "Manager/SkillManager.h"
#include "Manager/CustomTimerManager.h"
#include "Manager/AtkStateMar.h"
#include "Kismet/GameplayStatics.h"


CONTROL_COMPILE_OPTIMIZE_START
UFightAssist::UFightAssist()
{
	if (UUECS3GameInstance::Instance)
	{
		SkillManager = UUECS3GameInstance::Instance->SkillManager;
		MessageManager = UUECS3GameInstance::Instance->MessageManager;
		ParticleManager = UUECS3GameInstance::Instance->ParticleManager;
	}
}

void UFightAssist::BeginDestroy()
{
	Super::BeginDestroy();
}

bool UFightAssist::CheckSkillUseCondition(CS3Entity* AtkEntity, CS3Entity* BeAtkEntity, int32 SkillId)
{
	USkillData* SkillData = SkillManager->GetSkillDataById(SkillId);
	if (!IsValid(SkillData))
	{
		MessageManager->ShowMessage(4);//指定的技能不存在
		CS3_Warning(TEXT("-->Null Pointer error:UFightAssist::CheckSkillUseCondition : SkillData!"));
		return false;
	}
	if (SkillData->IsPassiveSkill())
	{
		return false;				//被动技能不能主动使用
	}
	if (SkillData->GetTargetType() == ENUM_CAST_TARGET_TYPE::TargetNothing)
	{
		BeAtkEntity = AtkEntity;	//TargetNothing默认对施法者自身释放
	}

	if (SkillData->IsInstantSkill())
	{

		if (SkillData->GetTargetType() == ENUM_CAST_TARGET_TYPE::TargetPosition)
		{
			//获取玩家控制器
			auto PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
			if (IsValid(PlayerController))
			{
				UAtkStateMar* AtkStateMar = PlayerController->GetAtkStateMar();
				if (IsValid(AtkStateMar) && !AtkStateMar->IsActivateState(EATTACT_STATE::AUTO_ATT))
				{
					AddSkillAssistUi(AtkEntity, SkillId);
					return false;
				}
			}
			else
			{
				return false;
			}			
		}
		//return true;				瞬发技能不判断通用条件，直接通过
	}
	/*取消"禁止施法"开关状态
	URoleStateInterface* RoleStateInterface = Cast<URoleStateInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("StateInterface")));
	if (RoleStateInterface && RoleStateInterface->IsActionForbid(ACTION_FLAG::ACTION_FORBID_SPELL))
	{
		MessageManager->ShowMessage(17);//当前状态下,无法进行该操作
		return false;
	}
	*/
	if (SkillData->GetTargetType() != ENUM_CAST_TARGET_TYPE::TargetPosition)
	{
		if (!BeAtkEntity)
		{
			MessageManager->ShowMessage(14);//没有找到施法目标
			return false;
		}
	}
	if (this->IsCasting(AtkEntity) && !SkillData->IsInstantSkill())
	{
		MessageManager->ShowMessage(19);//正在施法中,请稍后再试
		return false;
	}
	if (this->IsCoolDowning(AtkEntity, SkillId))
	{
		MessageManager->ShowMessage(6);//该技能冷却中，请稍后再试
		return false;
	}
	if(!this->HasEnoughtConsumables(AtkEntity, SkillId))
	{
		return false;
	}
	if (!this->CheckCasterCondition(AtkEntity, SkillId))
	{
		MessageManager->ShowMessage(21);//施法者条件不满足
		return false;
	}
	else
	{
		if (SkillData->GetTargetType() == ENUM_CAST_TARGET_TYPE::TargetPosition)
		{
			//获取玩家控制器
			auto PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
			UAtkStateMar* AtkStateMar = nullptr;
			if (IsValid(PlayerController))
			{
				AtkStateMar = PlayerController->GetAtkStateMar();
			}
			else
			{
				return false;
			}
			if (!AtkStateMar->IsActivateState(EATTACT_STATE::AUTO_ATT))
			{
				AddSkillAssistUi(AtkEntity, SkillId);
				return false;
			}
		}
		else
		{
			//获得施法范围
			float RangMax = SkillData->GetRangeMax();

			if (RangMax >= SKILL_CAST_RANGE_MAX)
			{
				return true;
			}
			else
			{
				if (IsValid(AtkEntity->Actor()) && IsValid(BeAtkEntity->Actor()))
				{
					float AtBeDis = FVector::Distance(AtkEntity->Actor()->GetActorLocation(), BeAtkEntity->Actor()->GetActorLocation());
					//判断距离
					if (SkillData->GetTargetType() == ENUM_CAST_TARGET_TYPE::TargetLock && (AtBeDis - (RangMax * 100.0f)) > 50.0f)
					{
						MessageManager->ShowMessage(12);//目标距离过远，请靠近后使用
						return false;
					}
				}
			}
		}	
	}
	return true;
}

bool UFightAssist::CheckAutoUseSkill(CS3Entity* AtkEntity, CS3Entity* BeAtkEntity, int32 SkillID, bool BShowMsg)
{
	USkillData* SkillData = SkillManager->GetSkillDataById(SkillID);
	if (!IsValid(SkillData))
	{
		if (BShowMsg)
		{
			MessageManager->ShowMessage(4);//指定的技能不存在
		}
		CS3_Warning(TEXT("-->Null Pointer error:UFightAssist::CheckAutoUseSkill : SkillData!"));
		return false;
	}
	if (SkillData->IsPassiveSkill())
	{
		return false;
	}
	if (AtkEntity == nullptr || BeAtkEntity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFightAssist::CheckAutoUseSkill : AtkEntity||BeAtkEntity!"));
		return false;
	}
	if (SkillData->IsInstantSkill())
	{
		if (SkillData->GetTargetType() == ENUM_CAST_TARGET_TYPE::TargetPosition)
		{
			//获取玩家控制器
			auto PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
			UAtkStateMar* AtkStateMar = nullptr;
			if (IsValid(PlayerController))
			{
				AtkStateMar = PlayerController->GetAtkStateMar();
			}
			else
			{
				return false;
			}
			if (!AtkStateMar->IsActivateState(EATTACT_STATE::AUTO_ATT))
			{
				AddSkillAssistUi(AtkEntity, SkillID);
				return false;
			}
		}
	}
	//开关判断
	UStateInterface* StateInterface = AtkEntity->Interface_Cache.StateInterface;
	if (IsValid(StateInterface) && StateInterface->IsActionForbid(SkillData->GetCasterActForbid()))
	{
		if (BShowMsg)
		{
			MessageManager->ShowMessage(17);//当前状态下,无法进行该操作
		}
		return false;
	}
	if (this->IsCasting(AtkEntity) && !SkillData->IsInstantSkill())
	{
		if (BShowMsg)
		{
			MessageManager->ShowMessage(19);//正在施法中,请稍后再试
		}
		return false;
	}
	if (IsCoolDowning(AtkEntity, SkillID))
	{
		if (BShowMsg)
		{
			MessageManager->ShowMessage(6);//该技能冷却中，请稍后再试
		}
		return false;
	}
	if (!HasEnoughtConsumables(AtkEntity, SkillID))
	{
		return false;
	}
	if (!CheckCasterCondition(AtkEntity, SkillID))
	{
		if (BShowMsg)
		{
			MessageManager->ShowMessage(21);//施法者条件不满足
		}
		return false;
	}
	if (!CheckTargetCondition(AtkEntity, BeAtkEntity, SkillID))
	{	
		return false;
	}
	return true;
}

bool UFightAssist::CheckAutoUseItem(AServerCharacter* TargetEntity, int32 ItemID)
{
	if (!IsValid(TargetEntity))
	{
		return false;
	}
	URoleKitBagInterface* RoleKitBagInterface = Cast<URoleKitBagInterface>
		(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface")));
	
	//在快捷栏中的物品
	TArray<UItemBase*> Items = RoleKitBagInterface->GetItemsByItemID(ItemID);
	UItemUse* ItemUse;
	if (Items.Num() <= 0)
	{		
		//在背包中
		ItemUse = Cast<UItemUse>(RoleKitBagInterface->FindItemByUID(INT_TO_FSTRING(ItemID)));
		//判断参数
		if (!IsValid(ItemUse))
		{
			CS3_Warning(TEXT("CheckAutoUseItem --- ItemUse Is Null !"));
			return false;
		}

		if (!ItemUse->IsCanUse())
		{
			CS3_Warning(TEXT("此物品不能使用"));
			return false;
		}

		if (ItemUse->IsCoolDowning())
		{
			if (!IsValid(MessageManager))
			{
				CS3_Warning(TEXT("UFightAssist::CheckAutoUseItem --- MessageManager Is Null !"));
				return false;
			}

			MessageManager->ShowMessage(6);
		}
		else
		{
			ItemUse->Use(TargetEntity);
			return true;
		}
	}
	else 
	{
		//获取物品
		ItemUse = Cast<UItemUse>(Items[0]);
		//判断参数
		if (!IsValid(ItemUse))
		{
			CS3_Warning(TEXT("CheckAutoUseItem --- ItemUse Is Null !"));
			return false;
		}
		int32 CheckUseResult = ItemUse->UseQuery(TargetEntity);
		//判断物品是否符合使用的条件
		if (UUECS3GameInstance::Instance->GMessageID->ITEM_USE_GO_ON_MSG == CheckUseResult)
		{
			if (!ItemUse->IsUseItemToPosition())
			{
				RoleKitBagInterface->RPC_uesItemByShortcutBar(ItemUse->ItemID, UGolbalBPFunctionLibrary::GetTargetEntityID());
			}
			return true;
		}
		else
		{
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(CheckUseResult);
			return false;
		}
	}
	return false;
}

void UFightAssist::ClearFightAssistUi(bool bIsNeedCopyAssUI/* = false*/)
{
	bIsSkillCastAssisting = false;
	if (FightAssistDecal)
	{
		if (bIsNeedCopyAssUI)
		{
			CopyFightAssistUi();
 		}		
		FightAssistDecal->DestroyComponent(false);
		FightAssistDecal = nullptr;	
		if (FightAssistMesh)
		{
			FightAssistMesh->DestroyComponent(false);
			FightAssistMesh = nullptr;
		}
		DSMaterialList.Empty();
		ParticleManager->StopEffectByUID(FightAssistEffectID);
	}
}

void UFightAssist::ClearModelAssistUi()
{
	bIsSkillCastAssisting = false;
	if (IsValid(CameraTranComponent))
	{
		CameraTranComponent->RemoveTranslucentComponent(ModelAssistCharacter);
		CameraTranComponent->DestroyComponent(true);
		CameraTranComponent = nullptr;
	}
	if (IsValid(ModelAssistCharacter))
	{
		ModelAssistCharacter->Destroy();
		ModelAssistCharacter = nullptr;
	}
	
}

void UFightAssist::CopyFightAssistUi()
{
	return;					// 下面的代码，不知道什么情况！！先return
	if (IsValid(FightAssistDecal))
	{
		UWorld* CurWorld = UUECS3GameInstance::Instance->GetWorld();
		UDecalComponent* FightAssistDecalTemp = NewObject<UDecalComponent>((UObject*)CurWorld);
		FightAssistDecalTemp->DecalSize = FightAssistDecal->DecalSize;
		FightAssistDecalTemp->SetRelativeRotation(FightAssistDecal->RelativeRotation);
		FightAssistDecalTemp->RegisterComponentWithWorld(CurWorld);
		//FightAssistDecalTemp->SetDecalMaterial(FightAssistDecal->DecalMaterial);
		FightAssistDecalTemp->SetDecalMaterial(FightAssistDecal->GetDecalMaterial());
		FightAssistDecalTemp->SetWorldLocation(FightAssistDecal->RelativeLocation);
		FightAssistDecalTemp->AddToRoot();
		FTimerHandle EffectTempTimerHandle;
		TWeakObjectPtr<UDecalComponent> DelayFightAssistDecalTempPtr(FightAssistDecalTemp);
		if (DelayFightAssistDecalTempPtr.IsValid())
		{
			UDecalComponent* FightAssistDecalTempPtr = DelayFightAssistDecalTempPtr.Get();
			FightAssistDecalTempPtr->RemoveFromRoot();
			FightAssistDecalTempPtr->DestroyComponent(false);
		}
	}
}

bool UFightAssist::IsCasting(CS3Entity* AtkEntity)
{
	return UGolbalBPFunctionLibrary::GetIntPropertyValue(AtkEntity->ID(), TEXT("castingSkillID")) != 0;
}

bool UFightAssist::IsCoolDowning(CS3Entity* AtkEntity, int32 SkillId)
{
	USkillData* SkillData = SkillManager->GetSkillDataById(SkillId);
	return SkillData->IsCoolDowning();
}

bool UFightAssist::HasEnoughtConsumables(CS3Entity* AtkEntity, int32 SkillId)
{
	bool CheckReslut = true;
	USkillData* SkillData = SkillManager->GetSkillDataById(SkillId);
	TArray<FSKILL_REQUIRE> CasterRequireDefineList = SkillData->GetCasterRequireList();
	for (FSKILL_REQUIRE RequireData : CasterRequireDefineList)
	{
		switch (RequireData.Type)
		{
			case ENUM_SKILL_REQUIRE_TYPE::RequireHp:
			{
				int32 HP = UGolbalBPFunctionLibrary::GetIntPropertyValue(AtkEntity->ID(), TEXT("HP"));
				int32 HP_Max = UGolbalBPFunctionLibrary::GetIntPropertyValue(AtkEntity->ID(), TEXT("HP_Max"));
				int32 RequireValue = FSTRING_TO_INT(RequireData.Param1) + int(HP_Max * FSTRING_TO_FLOAT(RequireData.Param2));
				CheckReslut = HP >= RequireValue ? true : false;
				if (!CheckReslut)
				{
					MessageManager->ShowMessage(16);//血量不足	
					return CheckReslut;
				}
				break;
			}
			case ENUM_SKILL_REQUIRE_TYPE::RequireMp:
			{
				int32 MP = UGolbalBPFunctionLibrary::GetIntPropertyValue(AtkEntity->ID(), TEXT("MP"));
				int32 MP_Max = UGolbalBPFunctionLibrary::GetIntPropertyValue(AtkEntity->ID(), TEXT("MP_Max"));
				int32 RequireValue = FSTRING_TO_INT(RequireData.Param1) + int(MP_Max * FSTRING_TO_FLOAT(RequireData.Param2));
				CheckReslut = MP >= RequireValue ? true : false;
				if (!CheckReslut)
				{
					MessageManager->ShowMessage(9);//法力值不足
					return CheckReslut;
				}
				break;
			}
			case ENUM_SKILL_REQUIRE_TYPE::RequireGangQi:
			{
				int32 gangQiValue = UGolbalBPFunctionLibrary::GetIntPropertyValue(AtkEntity->ID(), TEXT("gangQiValue"));
				int32 gangQiValue_Max = UGolbalBPFunctionLibrary::GetIntPropertyValue(AtkEntity->ID(), TEXT("gangQiValue_Max"));
				int32 RequireValue = FSTRING_TO_INT(RequireData.Param1) + int(gangQiValue_Max * FSTRING_TO_FLOAT(RequireData.Param2));
				CheckReslut = gangQiValue >= RequireValue ? true : false;
				if (!CheckReslut)
				{
					MessageManager->ShowMessage(25);//罡气值不足
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
	return CheckReslut;
}

bool UFightAssist::CheckCasterCondition(CS3Entity* AtkEntity, int32 SkillId)
{
	bool CheckResult = true;
	USkillData* SkillData = SkillManager->GetSkillDataById(SkillId);
	TArray<FSKILL_USE_CONDITION> CasterConditionList = SkillData->GetCasterCondition();
	for (auto ConditionData : CasterConditionList)
	{
		switch (ConditionData.ConditionType)
		{
		case ENUM_USE_CONDITION_TYPE::ConditionState:
			{
				ENTITY_STATE NeedState = (ENTITY_STATE)FSTRING_TO_INT(ConditionData.Param1);
				ENTITY_STATE RoleState = (ENTITY_STATE)UGolbalBPFunctionLibrary::GetIntPropertyValue(AtkEntity->ID(), TEXT("state"));

				if (FSTRING_TO_INT(ConditionData.Param2) != 0)
				{
					CheckResult = (RoleState == NeedState);
				}
				else
				{
					CheckResult = (RoleState != NeedState);
				}
				if (!CheckResult)
				{
					return CheckResult;
				}
			}
			break;
		default:
			break;
		}
	}
	return CheckResult;
}

bool UFightAssist::CheckTargetCondition(CS3Entity* AtkEntity, CS3Entity* BeAtkEntity, int32 SkillID)
{
	USkillData* SkillData = SkillManager->GetSkillDataById(SkillID);
	TArray<TArray<FSKILL_USE_CONDITION>> TargetConditionList = SkillData->GetTargetCondition();
	TArray<bool> CheckResults;	//需要符合所有条件
	bool ConditionTypeRelationIsAllFalse = true; //自动战斗 关系中有一个是配置有的，那就应该能释放出来。 默认全部为false 
	for (auto TargetCondition : TargetConditionList)
	{
		bool CheckResult = true;
		for (auto Condition : TargetCondition)
		{
			switch (Condition.ConditionType)
			{
			case ENUM_USE_CONDITION_TYPE::ConditionTypeRelation:
			{
				FString ClassTypes = Condition.Param1;
				FString RelationTypes = Condition.Param2;
				if (ClassTypes.Contains(BeAtkEntity->ClassName()))
				{
					ConditionTypeRelationIsAllFalse = false;  //自动战斗 只要一个受击对象 在配置中的一个有 那么就能释放出来。
					break;
				}
				if (AtkEntity->Actor() && BeAtkEntity->Actor())
				{
					COMBAT_RELATION Relation = Cast<AServerCharacter>(AtkEntity->Actor())->QueryRelation(Cast<AServerCharacter>(BeAtkEntity->Actor()));
					if (!RelationTypes.Contains(INT_TO_FSTRING(int32(Relation))))
					{
						CheckResult = false;
						break;
					}
				}
			}
			break;
			case ENUM_USE_CONDITION_TYPE::ConditionState:
			{
				ENTITY_STATE NeedState = (ENTITY_STATE)FSTRING_TO_INT(Condition.Param1);
				int32 bIsThisState = FSTRING_TO_INT(Condition.Param2);
				AServerCharacter* TargetActor = Cast<AServerCharacter>(BeAtkEntity->Actor());
				if (TargetActor)
				{
					if (bIsThisState != 0)
					{
						if (!TargetActor->IsState(NeedState))
						{
							CheckResult = false;
							break;
						}
					}
					else
					{
						if (TargetActor->IsState(NeedState))
						{
							CheckResult = false;
							break;
						}
					}
				}
			}
			break;
			default:
				break;
			}
		}
		CheckResults.Add(CheckResult);
	}
	if (CheckResults.Contains(false) && ConditionTypeRelationIsAllFalse)
	{
		return false;
	}
	return true;
}

bool UFightAssist::IsAtkEntityDead(CS3Entity* AtkEntity)
{
	int32 AtkEntityState = UGolbalBPFunctionLibrary::GetIntPropertyValue(AtkEntity->ID(), TEXT("state"));
	if (AtkEntityState == int32(ENTITY_STATE::EntityStateDead))
	{
		return true;
	}
	return false;
}

bool UFightAssist::IsBeAtkEntityDead(CS3Entity* BeAtkEntity)
{
	int32 BeAtkEntityState = UGolbalBPFunctionLibrary::GetIntPropertyValue(BeAtkEntity->ID(), TEXT("state"));
	if (BeAtkEntityState == int32(ENTITY_STATE::EntityStateDead))
	{
		return true;
	}
	return false;
}

void UFightAssist::AddSkillAssistUi(CS3Entity* AtkEntity, int32 SkillId)
{
	ClearFightAssistUi();
	ClearModelAssistUi();
	APlayerCharacter* AtkActor = Cast<APlayerCharacter>(AtkEntity->Actor());
	if (IsValid(AtkActor))
	{
		AtkActor->AddSkillAssistUiToScene(true, SkillId, this);
	}
	// 自动攻击模式和半自动模式（有目标）射击模式情况下不要施法辅助
	UAtkStateMar* AtkStateMar = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar();
	if (((AtkStateMar->IsActivateState(EATTACT_STATE::AUTO_HOMING_SPELL_ATT)
		|| AtkStateMar->IsActivateState(EATTACT_STATE::HALF_HOMING_SPELL_ATT)) && AtkActor->CurPlayerTarget)||
		AtkStateMar->IsActivateState(EATTACT_STATE::BEHAVIOR_SHOOT))
	{
		return;
	}
	AddEffectTimerHander(AtkEntity, SkillId);
}

void UFightAssist::AddItemAssistUi(CS3Entity* AtkEntity, FString& UID, int32 SkillId)
{
	ClearFightAssistUi();
	ClearModelAssistUi();
	APlayerCharacter* AtkActor = Cast<APlayerCharacter>(AtkEntity->Actor());
	if (IsValid(AtkActor))
	{
		AtkActor->AddItemAssistUiToScene(true, UID, SkillId, this);
	}
	// 自动攻击模式和半自动模式（有目标）情况下不要施法辅助
	UAtkStateMar* AtkStateMar = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar();
	if ((AtkStateMar->IsActivateState(EATTACT_STATE::AUTO_HOMING_SPELL_ATT)
		|| AtkStateMar->IsActivateState(EATTACT_STATE::HALF_HOMING_SPELL_ATT)) && AtkActor->CurPlayerTarget)
	{
	return;
	}
	AddEffectTimerHander(AtkEntity, SkillId);
}

void UFightAssist::AddItemAssistUiExt(CS3Entity * AtkEntity, FString & UID, int32& SkillId)
{
	ClearFightAssistUi();
	ClearModelAssistUi();
	APlayerCharacter* AtkActor = Cast<APlayerCharacter>(AtkEntity->Actor());
	if (IsValid(AtkActor))
	{
		AtkActor->AddItemAssistUiToSceneExt(true, UID, SkillId, this);
	}
	// 自动攻击模式和半自动模式（有目标）情况下不要施法辅助
	UAtkStateMar* AtkStateMar = UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetAtkStateMar();
	if ((AtkStateMar->IsActivateState(EATTACT_STATE::AUTO_HOMING_SPELL_ATT)
		|| AtkStateMar->IsActivateState(EATTACT_STATE::HALF_HOMING_SPELL_ATT)) && AtkActor->CurPlayerTarget)
	{
		return;
	}
	AddModelEffectAssist(AtkEntity, UID, SkillId);
}

void UFightAssist::TurnAssistModelDir(float Scale)
{
	if (IsValid(ModelAssistCharacter))
	{
		FRotator dir = ModelAssistCharacter->GetActorRotation();
		ModelAssistCharacter->SetActorRotation(dir + FRotator(0.0, Scale, 0.0));
	}
}

void UFightAssist::AddEffectTimerHander(CS3Entity* AtkEntity, int32 SkillId)
{	
	bIsSkillCastAssisting = true;
	APlayerCharacter* AtkActor = Cast<APlayerCharacter>(AtkEntity->Actor());
	if (!IsValid(AtkActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFightAssist::AddEffectTimerHander : AtkActor!"));
		return ;
	}
	USkillData* SkillData = SkillManager->GetSkillDataById(SkillId);
	FSKILL_ASSIST_EFFECT AssistEffect = SkillData->GetAssistEffect();

	TWeakObjectPtr<UFightAssist> DelayThisPtr(this);

	FightAssistEffectID = UUECS3GameInstance::Instance->ParticleManager->PlayParticle(AssistEffect.DecalEffectID, 0.0f, AtkActor, AtkActor, 
		FEffectCreate::CreateLambda([ AtkEntity, SkillId, DelayThisPtr, AssistEffect](int32 UID)
	{
		AEffectEmitter* Effect = Cast<AEffectEmitter>(UUECS3GameInstance::Instance->ParticleManager->FindEmitterByUID(UID));
		
		if (DelayThisPtr.IsValid() && Effect)
		{
			UFightAssist* ThisPtr = DelayThisPtr.Get();
			UWorld* CurWorld = UUECS3GameInstance::Instance->GetWorld();
			ThisPtr->ParticleManager->HideByUID(ThisPtr->FightAssistEffectID);
			///初始化贴花以及模型的材质并加入数组
			ThisPtr->DSMaterialList.Add(Effect->GetParticleSystemComponent()->GetMaterial(0));
			ThisPtr->DSMaterialList.Add(Effect->GetParticleSystemComponent()->GetMaterial(1));
			ThisPtr->DSMaterialList.Add(Effect->GetParticleSystemComponent()->GetMaterial(2));
			ThisPtr->DSMaterialList.Add(Effect->GetParticleSystemComponent()->GetMaterial(3));
			///初始化贴花
			ThisPtr->FightAssistDecal = NewObject<UDecalComponent>((UObject*)CurWorld);
			ThisPtr->FightAssistDecal->DecalSize = FVector(AssistEffect.DecalSize.Z, AssistEffect.DecalSize.Y, AssistEffect.DecalSize.X);
			ThisPtr->FightAssistDecal->SetWorldRotation(FRotator(-90.0f,0.0f, 0.0f));
			ThisPtr->FightAssistDecal->RegisterComponentWithWorld(CurWorld);
			///初始化贴花水上模型
			ThisPtr->FightAssistMesh = NewObject<UStaticMeshComponent>((UObject*)CurWorld);
			ThisPtr->FightAssistMesh->SetWorldLocation(FVector(0.0f, 0.0f, 0.0f));
			ThisPtr->FightAssistMesh->SetWorldRotation(FRotator(90.0f, 0.0f, 0.0f).Quaternion());
			ThisPtr->FightAssistMesh->SetWorldScale3D(AssistEffect.DecalSize / 100);
			ThisPtr->FightAssistMesh->RegisterComponentWithWorld(CurWorld);
			ThisPtr->FightAssistMesh->AttachToComponent(ThisPtr->FightAssistDecal, FAttachmentTransformRules::KeepRelativeTransform);
			ThisPtr->FightAssistMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
			///从粒子中获取模型进行初始化模型的Mesh设置
			TArray<UParticleEmitter*> EmitterList = Effect->GetParticleSystemComponent()->Template->Emitters;
			for (UParticleEmitter* emitter : EmitterList)
			{
				for (UParticleLODLevel* LODlevel : emitter->LODLevels)
				{
					UParticleModuleTypeDataMesh * MeshData = Cast<UParticleModuleTypeDataMesh>(LODlevel->TypeDataModule);
					if (IsValid(MeshData))
					{
						if (!IsValid(ThisPtr->FightAssistMesh->GetStaticMesh()))
						{
							ThisPtr->FightAssistMesh->SetStaticMesh(MeshData->Mesh);
							ThisPtr->FightAssistMesh->SetMaterial(0,ThisPtr->DSMaterialList[1]);
						}
					}
				}
			}
			ThisPtr->UpdateEffectTimerHander(AtkEntity, SkillId);
			UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(ThisPtr, ThisPtr->EffectTimerHandle, FTimerDelegate::CreateLambda([DelayThisPtr, AtkEntity, SkillId]()
			{
				if (DelayThisPtr.IsValid())
				{
					UFightAssist* ThisPtr = DelayThisPtr.Get();
					if (IsValid(ThisPtr->ParticleManager->FindEmitterByUID(ThisPtr->FightAssistEffectID)))
					{
						ThisPtr->UpdateEffectTimerHander(AtkEntity, SkillId);
					}
				}
			}), 0.01f, true);
		}
	}));
}

void UFightAssist::AddModelEffectAssist(CS3Entity * AtkEntity, FString & UID, int32 & SkillId)
{
	bIsSkillCastAssisting = true;
	APlayerCharacter* AtkActor = Cast<APlayerCharacter>(AtkEntity->Actor());
	if (!IsValid(AtkActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFightAssist::AddEffectTimerHander : AtkActor!"));
		return;
	}
	if (!IsValid(CameraTranComponent))
	{
		CameraTranComponent = NewObject<UCameraCaptureTranslucentComponent>(AtkActor, TEXT("SceneCapture"));
		CameraTranComponent->AttachToComponent(AtkActor->CameraComponent, FAttachmentTransformRules::KeepRelativeTransform);
		CameraTranComponent->RegisterComponent();
	}

	URoleKitBagInterface* kitBagInterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface")));
	if (!IsValid(kitBagInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFightAssist::AddEffectTimerHander : RoleKitBagInterface!"));
		return;
	}
	UItemUseAssist* item = Cast<UItemUseAssist>(kitBagInterface->FindItemByUID(UID));
	if (!IsValid(item))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFightAssist::AddEffectTimerHander : UItemUseAssist!"));
		return;
	}
	UClass *ClientActor = UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_Scene"));
	ModelAssistCharacter = UGolbalBPFunctionLibrary::SpawnActor<ASceneCharacter>(ClientActor);
	if (IsValid(ModelAssistCharacter))
	{
		ModelAssistCharacter->SetActorEnableCollision(false);
		ModelAssistCharacter->ModelScale = 1.0f;
		ModelAssistCharacter->GetAppearanceComponent()->CreateAppearance(item->GetModelAssist());
		ModelAssistCharacter->SetActorRotation(item->GetModelRotationAssist(AtkActor));
		CameraTranComponent->AddTranslucentComponent(ModelAssistCharacter);
		UpdateModelEffectAssist(AtkEntity, UID, SkillId);

		if (item->IsUseDirection())
		{
			CameraTranComponent->SetWarnTips(1);
		}
		TWeakObjectPtr<UFightAssist> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, EffectTimerHandle, FTimerDelegate::CreateLambda([DelayThisPtr, AtkEntity, UID, SkillId]()
		{
			if (DelayThisPtr.IsValid())
			{
				UFightAssist* ThisPtr = DelayThisPtr.Get();
				if (IsValid(ThisPtr))
				{
					ThisPtr->UpdateModelEffectAssist(AtkEntity, UID, SkillId);
				}
			}
		}), 0.01f, true);
	}
	
}

void UFightAssist::UpdateEffectTimerHander(CS3Entity* AtkEntity, int32 SkillId)
{
	APlayerCharacter* AtkActor = Cast<APlayerCharacter>(AtkEntity->Actor());	
	
	if (!IsValid(AtkActor)|| !bIsSkillCastAssisting)
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(EffectTimerHandle);
		return;
	}
	AtkActor->OnMouseisWaterBP();
	if (IsValid(ParticleManager->FindEmitterByUID(FightAssistEffectID)))
	{
		FightAssistMesh->SetVisibility(AtkActor->MouseisWater);
	}
	USkillData* SkillData = SkillManager->GetSkillDataById(SkillId);
	FSKILL_ASSIST_EFFECT AssistEffect = SkillData->GetAssistEffect();
	if (IsValid(FightAssistDecal) && IsValid(AtkActor))
	{
		FHitResult OutHit;
		UGolbalBPFunctionLibrary::GetCS3PlayerController()->GetHitResultUnderCursor(ECollisionChannel::ECC_Visibility, true, OutHit);
		FVector MousePos = OutHit.Location;
		//获取玩家控制器
		auto PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
		UAtkStateMar* AtkStateMar = nullptr;
		if (IsValid(PlayerController))
		{
			AtkStateMar = PlayerController->GetAtkStateMar();
		}
		if (AtkActor->GetSelfEntity() != nullptr&&AtkActor->GetSelfEntity()->IsPlayer() && IsValid(AtkStateMar))
		{
			if (IsValid(AtkActor->CurPlayerTarget) && (AtkStateMar->IsActivateState(EATTACT_STATE::AUTO_HOMING_SPELL_ATT) || AtkStateMar->IsActivateState(EATTACT_STATE::HALF_HOMING_SPELL_ATT)))
			{
				MousePos = AtkActor->CurPlayerTarget->GetActorLocation();
			}
			else if (AtkStateMar->IsActivateState(EATTACT_STATE::BEHAVIOR_SHOOT))
			{
				int32 SizeX = 0, SizeY = 0;
				PlayerController->GetViewportSize(SizeX, SizeY);
				FHitResult TraceHitResult;
				FCollisionQueryParams TraceParams = FCollisionQueryParams(FName(TEXT("ComputeFloorDistSweep")), true);
				TraceParams.bTraceComplex = true;
			/*	TraceParams.AddIgnoredActor(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
				TraceParams.AddIgnoredActors(UGolbalBPFunctionLibrary::GetActorsInRange(nullptr, 8000.f));*/
				PlayerController->GetHitResultAtScreenPosition(FVector2D(SizeX / 2.0f, SizeY / 2.0f), PlayerController->CurrentClickTraceChannel, TraceParams, TraceHitResult);
				if (TraceHitResult.bBlockingHit)
				{
					MousePos = TraceHitResult.ImpactPoint;
				}
				else
				{
					MousePos = FVector::ZeroVector;
				}
			}
		}
		
		if (!MousePos.IsZero())
		{
			FVector PlayerPos = AtkActor->GetActorLocation();
			//超过施法范围贴花显示错误样式
			if (FVector::Dist(PlayerPos, MousePos) > SkillData->GetRangeMax()*100.0f /*|| !UGolbalBPFunctionLibrary::FindPathToLocation(MousePos)*/)
			{
				if (DSMaterialList.Num()>=4)
				{
					FightAssistDecal->SetDecalMaterial(DSMaterialList[2]);//距离过远或者显示错误贴花材质
					FightAssistMesh->SetMaterial(0, DSMaterialList[3]);
				}
			}
			else if (DSMaterialList.Num()>= 4)
			{
				FightAssistDecal->SetDecalMaterial(DSMaterialList[0]);//距离过远或者显示错误贴花材质
				FightAssistMesh->SetMaterial(0, DSMaterialList[1]);
			}			
			FightAssistDecal->SetWorldLocation(MousePos);
			CS3_Warning(TEXT("---->UFightAssist::UpdateEffectTimerHander : %s  "),*MousePos.ToString());
			float InYaw = UGolbalBPFunctionLibrary::GetLookAtRotator(PlayerPos, MousePos).Yaw;
			FightAssistDecal->SetWorldRotation(FRotator(-90.0f, InYaw, 0.0f));
		}
	}
	
}

void UFightAssist::UpdateModelEffectAssist(CS3Entity * AtkEntity, const FString & UID, const int32 & SkillId)
{
	APlayerCharacter* AtkActor = Cast<APlayerCharacter>(AtkEntity->Actor());
	auto PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();

	if (!IsValid(AtkActor) || !IsValid(PlayerController) || !bIsSkillCastAssisting)
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(EffectTimerHandle);
		return;
	}
	FVector MousePos = UGolbalBPFunctionLibrary::GetMouseWorldPos();

	UAtkStateMar* AtkStateMar = PlayerController->GetAtkStateMar();
	if (AtkActor->GetSelfEntity() != nullptr&&AtkActor->GetSelfEntity()->IsPlayer() && IsValid(AtkStateMar))
	{
		if (IsValid(AtkActor->CurPlayerTarget) && (AtkStateMar->IsActivateState(EATTACT_STATE::AUTO_HOMING_SPELL_ATT) || AtkStateMar->IsActivateState(EATTACT_STATE::HALF_HOMING_SPELL_ATT)))
		{
			MousePos = AtkActor->CurPlayerTarget->GetActorLocation();
		}
		else if (AtkStateMar->IsActivateState(EATTACT_STATE::BEHAVIOR_SHOOT))
		{
			int32 SizeX = 0, SizeY = 0;
			PlayerController->GetViewportSize(SizeX, SizeY);
			FHitResult TraceHitResult;
			FCollisionQueryParams TraceParams = FCollisionQueryParams(FName(TEXT("ComputeFloorDistSweep")), true);
			TraceParams.bTraceComplex = true;
			/*	TraceParams.AddIgnoredActor(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
				TraceParams.AddIgnoredActors(UGolbalBPFunctionLibrary::GetActorsInRange(nullptr, 8000.f));*/
			PlayerController->GetHitResultAtScreenPosition(FVector2D(SizeX / 2.0f, SizeY / 2.0f), PlayerController->CurrentClickTraceChannel, TraceParams, TraceHitResult);
			if (TraceHitResult.bBlockingHit)
			{
				MousePos = TraceHitResult.ImpactPoint;
			}
			else
			{
				MousePos = FVector::ZeroVector;
			}
		}
	}
	
	URoleKitBagInterface* kitbag = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName("RoleKitBagInterface", AtkActor->EntityId));
	if (IsValid(kitbag) && IsValid(SkillManager))
	{
		USkillData* SkillData = SkillManager->GetSkillDataById(SkillId);
		UItemUseAssist* item = Cast<UItemUseAssist>(kitbag->FindItemByUID(UID));
		if (IsValid(item))
		{
			ModelAssistCharacter->SetActorLocation(MousePos + FVector(0, 0, item->GetModelAssistOffsetH()));

			if (!item->IsUseDirection())
			{
				if (item->CheckModelAssistValid(MousePos) && FVector::Dist(AtkActor->GetActorLocation(), MousePos) <= SkillData->GetRangeMax()*100.0f)
				{
					CameraTranComponent->SetWarnTips(1);
				}
				else
				{
					CameraTranComponent->SetWarnTips(0);
				}
			}
			
		}
	}
}

bool UFightAssist::CheckMoveToTraceTargetActor(CS3Entity* AtkEntity, AActor* TargetActor, int32 SkillId)
{
	//MessageManager->ShowMessage(12);//目标距离过远，请靠近后使用
	bool IsTraceTarget = false;
	USkillData* SkillData = SkillManager->GetSkillDataById(SkillId);
	float CastRange = SkillData->GetRangeMax();
	APlayerCharacter* AtkActor = Cast<APlayerCharacter>(AtkEntity->Actor());
	if (!IsValid(AtkActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFightAssist::CheckMoveToTraceTargetActor : AtkActor!"));
		return false;
	}

	if (UGolbalBPFunctionLibrary::GetActorDistance(AtkActor, TargetActor) > CastRange * 100.0f)
	{
		ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(AtkActor->GetController());
		if (IsValid(PlayerController))
		{
			IsTraceTarget = true;
			TWeakObjectPtr<UFightAssist> DelayThisPtr(this);
			TWeakObjectPtr<APlayerCharacter> DelayAtkActorPtr(AtkActor);
			TWeakObjectPtr<AActor> DelayTargetActorPtr(TargetActor);
			PlayerController->TraceTargetActor(TargetActor, CastRange*0.67f, FTraceCallback::CreateLambda([DelayThisPtr, DelayAtkActorPtr, SkillId, DelayTargetActorPtr](bool IsSuccess)
			{
				if (DelayThisPtr.IsValid() && DelayAtkActorPtr.IsValid() && DelayTargetActorPtr.IsValid())
				{
					UFightAssist* ThisPtr = DelayThisPtr.Get();
					APlayerCharacter* AtkActorPtr = DelayAtkActorPtr.Get();
					AActor* TargetActorPtr = DelayTargetActorPtr.Get();
					if (IsSuccess)
					{
						ThisPtr->UseTargetSkill(AtkActorPtr, SkillId, Cast<AServerCharacter>(TargetActorPtr)->EntityId);
					}
				}
			}));
		}
	}
	return IsTraceTarget;
}

bool UFightAssist::CheckMoveToTraceTargetPostion(CS3Entity* AtkEntity, FVector& TargetPostion, int32 SkillId)
{
	//MessageManager->ShowMessage(12);//目标距离过远，请靠近后使用
	bool IsTraceTarget = false;
	USkillData* SkillData = SkillManager->GetSkillDataById(SkillId);
	float CastRange = SkillData->GetRangeMax();
	FVector StartPostion = AtkEntity->Actor()->GetActorLocation();
	APlayerCharacter* AtkActor = Cast<APlayerCharacter>(AtkEntity->Actor());
	if (!IsValid(AtkActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UFightAssist::CheckMoveToTraceTargetPostion : AtkActor!"));
		return false;
	}
	if (FVector::Dist(StartPostion, TargetPostion) > CastRange * 100.0f)
	{
		ACS3PlayerController* PlayerController = Cast<ACS3PlayerController>(AtkActor->GetController());
		if (IsValid(PlayerController))
		{
			IsTraceTarget = true;
			PlayerController->TraceTargetPostion(TargetPostion, CastRange*0.67f, FTraceCallback::CreateLambda([this, AtkActor, SkillId, TargetPostion](bool IsSuccess)
			{
				if (IsSuccess)
				{
					this->UsePostionSkill(AtkActor, SkillId, TargetPostion);
				}
			}));
		}
	}
	return IsTraceTarget;
}


void UFightAssist::UseTargetSkill(AServerCharacter* AtkActor, int32 SkillId, int32 TargetId)
{
	if (IsValid(AtkActor))
	{
		USkillInterface* SkillInterface = AtkActor->GetEntityInterface_Cache().SkillInterface;
		SkillInterface->UseSkill(SkillId, TargetId);
	}
}

void UFightAssist::UsePostionSkill(AServerCharacter* AtkActor, int32 SkillId, const FVector& TargetPostion)
{
	UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(EffectTimerHandle);
	ClearFightAssistUi(true);
	Cast<APlayerCharacter>(AtkActor)->AddSkillAssistUiToScene(false);
	USkillInterface* SkillInterface = AtkActor->GetEntityInterface_Cache().SkillInterface;
	SkillInterface->UsePostionSkill(SkillId, TargetPostion);
}

void UFightAssist::UsePostionItem(AServerCharacter* AtkActor, FString UID, int32 SkillId, const FVector& TargetPostion)
{
	UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(EffectTimerHandle);
	ClearFightAssistUi(true);
	Cast<APlayerCharacter>(AtkActor)->AddSkillAssistUiToScene(false);
	USkillInterface* SkillInterface = AtkActor->GetEntityInterface_Cache().SkillInterface;
	if (SkillInterface)
	{
		SkillInterface->SetCurrentUsePosItemUID(TEXT(""));
	}
	URoleKitBagInterface* kitbag = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName("RoleKitBagInterface",AtkActor->EntityId));
	if (IsValid(kitbag))
	{
		kitbag->OnUseItemByPos(UID, TargetPostion);
	}
}

void UFightAssist::UsePostionItemExt(AServerCharacter * AtkActor, FString UID, int32 SkillId, const FVector & TargetPostion)
{
	FVector Dir(FVector::ZeroVector);
	if (IsValid(ModelAssistCharacter))
	{
		Dir.Z = ModelAssistCharacter->GetActorRotation().Euler().Z;
	}
	UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(EffectTimerHandle);
	ClearModelAssistUi();
	USkillInterface* SkillInterface = AtkActor->GetEntityInterface_Cache().SkillInterface;
	if (SkillInterface)
	{
		SkillInterface->SetCurrentUsePosItemUID(TEXT(""));
	}
	URoleKitBagInterface* kitbag = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName("RoleKitBagInterface", AtkActor->EntityId));
	if (IsValid(kitbag))
	{
		UItemUseAssist* item = Cast<UItemUseAssist>(kitbag->FindItemByUID(UID));
		if (item->IsUseDirection())
		{
			kitbag->OnUseItemByPosAndDir(UID, TargetPostion, Dir);
		}
		else
		{
			kitbag->OnUseItemByPos(UID, TargetPostion);
		}
		
	}
}

CONTROL_COMPILE_OPTIMIZE_END
