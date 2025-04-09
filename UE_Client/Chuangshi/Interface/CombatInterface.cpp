// Fill out your copyright notice in the Description page of Project Settings.

#include "CombatInterface.h"
#include "Util/ConvertUtil.h"
#include "CS3Base/GameObject.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Actor/ServerCharacter.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/SkillManager.h"
#include "Util/CS3Debug.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/EventManager.h"
#include "Util/GlobalFunctions.h"
#include "Manager/CfgManager.h"
#include "GameData/RoleExpData.h"
#include "Interface/Role/RoleChatInterface.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "Actor/Player/PlayerCharacter.h"

CONTROL_COMPILE_OPTIMIZE_START


CS3_BEGIN_INTERFACE_METHOD_MAP(UCombatInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UCombatInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(MP, &UCombatInterface::Set_MP, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(MP_Max, &UCombatInterface::Set_MP_Max, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(playerName, &UCombatInterface::Set_PlayerName, FString)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(profession, &UCombatInterface::Set_profession, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(level, &UCombatInterface::Set_level, int16)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(exp, &UCombatInterface::Set_exp, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(corporeity, &UCombatInterface::Set_corporeity, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(strength, &UCombatInterface::Set_strength, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(intellect, &UCombatInterface::Set_intellect, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(dexterity, &UCombatInterface::Set_dexterity, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(damage, &UCombatInterface::Set_damage, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(magic_damage, &UCombatInterface::Set_magic_damage, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(armor, &UCombatInterface::Set_armor, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(magic_armor, &UCombatInterface::Set_magic_armor, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(criticalstrike, &UCombatInterface::Set_criticalstrike, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(discern, &UCombatInterface::Set_discern, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(parry, &UCombatInterface::Set_parry, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(speed, &UCombatInterface::Set_speed, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(hitrate, &UCombatInterface::Set_hitrate, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(dodgerate, &UCombatInterface::Set_dodgerate, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(healingrate, &UCombatInterface::Set_healingrate, int32)
//CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(camp, &UCombatInterface::Set_camp, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(feats, &UCombatInterface::Set_feats, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(potential, &UCombatInterface::Set_potential, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(xiuwei, &UCombatInterface::Set_xiuwei, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(xiuweiLevel, &UCombatInterface::Set_xiuweiLevel, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(tempCamp, &UCombatInterface::Set_tempCamp, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(jingjieLevel, &UCombatInterface::Set_jingjieLevel, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(gangQi_qiJieProgress, &UCombatInterface::Set_gangQi_qiJieProgress, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(combatPower, &UCombatInterface::Set_combatPower, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(killingValue, &UCombatInterface::Set_killingValue, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(vitPoint, &UCombatInterface::Set_vitPoint, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(vitPoint_Max, &UCombatInterface::Set_vitPoint_Max, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(cure, &UCombatInterface::Set_cure, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(ice_damage, &UCombatInterface::Set_ice_damage, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(fire_damage, &UCombatInterface::Set_fire_damage, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(thunder_damage, &UCombatInterface::Set_thunder_damage, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(xuan_damage, &UCombatInterface::Set_xuan_damage, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(ice_armor, &UCombatInterface::Set_ice_armor, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(fire_armor, &UCombatInterface::Set_fire_armor, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(thunder_armor, &UCombatInterface::Set_thunder_armor, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(xuan_armor, &UCombatInterface::Set_xuan_armor, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(damage_ignore, &UCombatInterface::Set_damage_ignore, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(magic_damage_ignore, &UCombatInterface::Set_magic_damage_ignore, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(armor_ignore, &UCombatInterface::Set_armor_ignore, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(magic_armor_ignore, &UCombatInterface::Set_magic_armor_ignore, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(criticalstrike_ignore, &UCombatInterface::Set_criticalstrike_ignore, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(parry_ignore, &UCombatInterface::Set_parry_ignore, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(hitrate_ignore, &UCombatInterface::Set_hitrate_ignore, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(dodgerate_ignore, &UCombatInterface::Set_dodgerate_ignore, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(ice_damage_ignore, &UCombatInterface::Set_ice_damage_ignore, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(fire_damage_ignore, &UCombatInterface::Set_fire_damage_ignore, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(thunder_damage_ignore, &UCombatInterface::Set_thunder_damage_ignore, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(xuan_damage_ignore, &UCombatInterface::Set_xuan_damage_ignore, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(ice_armor_ignore, &UCombatInterface::Set_ice_armor_ignore, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(fire_armor_ignore, &UCombatInterface::Set_fire_armor_ignore, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(thunder_armor_ignore, &UCombatInterface::Set_thunder_armor_ignore, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(xuan_armor_ignore, &UCombatInterface::Set_xuan_armor_ignore, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(depress_resist, &UCombatInterface::Set_depress_resist, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(hitback_resist, &UCombatInterface::Set_hitback_resist, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(control_resist, &UCombatInterface::Set_control_resist, int32)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(insane_resist, &UCombatInterface::Set_insane_resist, int32)
CS3_END_INTERFACE_PROPERTY_MAP()

UCombatInterface::UCombatInterface()
{
}

UCombatInterface::~UCombatInterface()
{

}

void UCombatInterface::CLIENT_CheckClientPosition_Implementation()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCombatInterface::CLIENT_CheckClientPosition_Implementation : GetEntity()!"));
		return;
	}
	GameObject* entity = (GameObject *)(this->GetEntity());
	AServerCharacter* actor = Cast<AServerCharacter>(entity->Actor());
	FVector localPos = actor->GetActorLocation();
	FVector serverPos = KBEngine::KBEMath::Unreal2KBEnginePosition(localPos);

	RPC_ReceivePosFromClient(serverPos);
	
}


void UCombatInterface::CLIENT_PlayDeadEffect_Implementation()
{
	PlayDeadEffect_Implementation();
}

void UCombatInterface::PlayDeadEffect_Implementation()
{
	AServerCharacter* Actor = Cast<AServerCharacter>(GetActor());
	if (IsValid(Actor))
	{
		Actor->PlayDeadEffect();
	}
}

void UCombatInterface::PlayDeadMortuaryEffect_Implementation()
{
	AServerCharacter* Actor = Cast<AServerCharacter>(GetActor());
	if (IsValid(Actor))
	{
		Actor->PlayDeadMortuaryEffect();
	}
}

void UCombatInterface::CLIENT_OnWalkAroundTarget_Implementation(int32 targetID)
{
	WalkAroundTargetID = targetID;
}

void UCombatInterface::CLIENT_OnWalkAroundTargetEnd_Implementation()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCombatInterface::CLIENT_OnWalkAroundTargetEnd_Implementation : GetEntity()!"));
		return;
	}
	GameObject* entity = (GameObject *)(this->GetEntity());
	AServerCharacter* actor = Cast<AServerCharacter>(entity->Actor());
	float Yaw = actor->GetActorRotation().Yaw;
	Yaw = FMath::DegreesToRadians(Yaw);
	
	RPC_ReceiveDirectionFromClient(FVector(0.0, 0.0, Yaw));
	WalkAroundTargetID = 0;
}

void UCombatInterface::CLIENT_NotifyStopMoving_Implementation()
{
	GameObject* entity = (GameObject *)(this->GetEntity());
	if (entity != nullptr && entity->IsPlayer())
	{
		APlayerCharacter* actor = Cast<APlayerCharacter>(entity->Actor());
		if (IsValid(actor))
		{
			actor->StopPlayerMove();
		}
	}
}

void UCombatInterface::CLIENT_ShowCombatPowerChangeTips_Implementation(int32 combatpower, int32 value)
{

}


void UCombatInterface::RPC_requestSkillLearn(const FString& STRING_1, const FString& STRING_2)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCombatInterface::RPC_requestSkillLearn : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(STRING_1);
	args.Add(STRING_2);

	entity->CellCall(TEXT("requestSkillLearn"), args);
}

void UCombatInterface::RPC_setPkModeFC(const int32& INT32_1)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCombatInterface::RPC_setPkModeFC : entity!"));
		return;
	}

	KBEngine::FVariantArray args;
	args.Add(INT32_1);

	entity->CellCall(TEXT("setPkModeFC"), args);
}

void UCombatInterface::CLIENT_requestOpenSkillLearn_Implementation(const int32 teacherID)
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		USkillManager* SkillManager = UUECS3GameInstance::Instance->SkillManager;
		if (IsValid(UUECS3GameInstance::Instance->SkillManager))
		{
			SkillManager->InitSkillLearnDatasByTeacherID(teacherID);
		}
	}
}

void UCombatInterface::RPC_CELL_requestSkillUpgrade(const int32& SkillID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCombatInterface::RPC_CELL_requestSkillUpgrade : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(SkillID);

	entity->CellCall(TEXT("requestSkillUpgrade"), args);
}

void UCombatInterface::requestSkillUpgradeMax(const int32& SkillID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCombatInterface::RPC_CELL_requestSkillUpgrade : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(SkillID);

	entity->CellCall(TEXT("requestSkillUpgradeMax"), args);
}

void UCombatInterface::RPC_setAreaRelationRuleFC(FString AreaPvpRule)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCombatInterface::setAreaRelationRuleFC : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(AreaPvpRule);
	entity->CellCall(TEXT("setAreaRelationRuleFC"), args);
}

void UCombatInterface::RPC_ReceivePosFromClient(FVector Position)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCombatInterface::RPC_ReceivePosFromClient : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(Position);
	entity->CellCall(TEXT("CELL_receivePosFromClient"), args);
}

void UCombatInterface::RPC_ReceiveDirectionFromClient(FVector Direction)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCombatInterface::RPC_ReceiveDirectionFromClient : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(Direction);
	entity->CellCall(TEXT("CELL_receiveDirectionFromClient"), args);
}
void UCombatInterface::RPC_requestPassiveSkillLearn(const int32 & SkillID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCombatInterface::RPC_requestPassiveSkillLearn : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(SkillID);

	entity->CellCall(TEXT("requestPassiveSkillLearn"), args);
}

void UCombatInterface::RPC_requestPassiveSkillUpgrade(const int32 & SkillID)
{
	KBEngine::Entity* entity = GetEntity();
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCombatInterface::RPC_requestPassiveSkillUpgrade : entity!"));
		return;
	}
	KBEngine::FVariantArray args;
	args.Add(SkillID);

	entity->CellCall(TEXT("requestPassiveSkillUpgrade"), args);
}

void UCombatInterface::InitBlueCB()
{
	ArrBlueFunc.Add("CLIENT_CheckClientPosition");
	ArrBlueFunc.Add("CLIENT_OnWalkAroundTarget");
	ArrBlueFunc.Add("CLIENT_OnWalkAroundTargetEnd");
	ArrBlueFunc.Add("CLIENT_NotifyStopMoving");
	ArrBlueFunc.Add("CLIENT_PlayDeadEffect");
	ArrBlueFunc.Add("CLIENT_requestOpenSkillLearn");
	ArrBlueFunc.Add("CLIENT_ShowCombatPowerChangeTips");
	ArrBlueFunc.Add("PlayDeadMortuaryEffect");
	Supper::InitBlueCB();
}

TMap<int32, int32> UCombatInterface::GetEnemyList()
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

TMap<int32, int32> UCombatInterface::GetDamageList()
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

void UCombatInterface::Set_HP(const int32& newVal, const int32& oldVal)
{
	HP = newVal;

	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnHPChangedEvent.Broadcast(EntityID, HP, HP_Max);
	}
}

void UCombatInterface::Set_HP_Max(const int32& newVal, const int32& oldVal)
{
	HP_Max = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnHPChangedEvent.Broadcast(EntityID, HP, HP_Max);
	}
}

void UCombatInterface::Set_MP(const int32& newVal, const int32& oldVal)
{
	MP = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnMPChangedEvent.Broadcast(EntityID, MP, MP_Max);
	}
}

void UCombatInterface::Set_MP_Max(const int32& newVal, const int32& oldVal)
{
	MP_Max = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnMPChangedEvent.Broadcast(EntityID, MP, MP_Max);
	}
}

void UCombatInterface::Set_PlayerName(const FString& newVal, const FString& oldVal)
{
	playerName = newVal;
	CS3Entity* selfPtr = GetMyEntity();
	if (selfPtr && selfPtr->IsPlayer())
	{
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnPlayerNameChanged.Broadcast( playerName );
		}
		APlayerCharacter* actorPtr = Cast< APlayerCharacter >( selfPtr->Actor() );
		actorPtr->OnPlayerNameChanged(*playerName);
		
	}
}

void UCombatInterface::Set_profession(const int32& newVal, const int32& oldVal)
{
	profession = newVal;
	CS3Entity* selfPtr = GetMyEntity();
	if (selfPtr && selfPtr->IsPlayer())
	{
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
		{
			UUECS3GameInstance::Instance->GEventManager->OnProfessionChanged.Broadcast( playerName, profession ) ;
		}
	}
}

void UCombatInterface::Set_level(const int16& newVal, const int16& oldVal)
{
	level = newVal;
	if (!IsValid(UUECS3GameInstance::Instance))
		return;

	if( IsValid(UUECS3GameInstance::Instance->GEventManager) )
	{
		UUECS3GameInstance::Instance->GEventManager->OnLevelChanged.Broadcast(EntityID,level);
		

		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		if (!IsValid(CfgManager))
			return;
		if (level > 0)
		{
			const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ROLE_EXP);
			const FRoleExpData* data = ConfigTable->GetRow<FRoleExpData>(FString::FromInt(level));
			if (data)
			{
				UUECS3GameInstance::Instance->GEventManager->OnExpChanged.Broadcast(EntityID, exp, data->maxExp);
			}
		}

	}
	CS3Entity* selfPtr = GetMyEntity();
	if (selfPtr)
	{
		URoleKitBagInterface* kitbagPtr = CS3::GetInterface<URoleKitBagInterface>(selfPtr);
		if (kitbagPtr != nullptr)
			kitbagPtr->OnPlayerLevelChange(level);

		URoleChatInterface* chatPtr = CS3::GetInterface<URoleChatInterface>(selfPtr);
		if (chatPtr != nullptr)
			chatPtr->OnChatShortcutSwitchConditionsChange();
	}
}

void UCombatInterface::Set_exp(const int32& newVal, const int32& oldVal)
{
	exp = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		if (!IsValid(CfgManager))
			return;

		if (level > 0)
		{
			const UConfigTable* ConfigTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ROLE_EXP);
			const FRoleExpData* data = ConfigTable->GetRow<FRoleExpData>(FString::FromInt(level));
			UUECS3GameInstance::Instance->GEventManager->OnExpChanged.Broadcast( EntityID, exp,  data->maxExp);
		}
	}
}

void UCombatInterface::Set_corporeity(const int32& newVal, const int32& oldVal)
{
	corporeity = newVal;
}

void UCombatInterface::Set_strength(const int32& newVal, const int32& oldVal)
{
	strength = newVal;
}

void UCombatInterface::Set_intellect(const int32& newVal, const int32& oldVal)
{
	intellect = newVal;
}

void UCombatInterface::Set_dexterity(const int32& newVal, const int32& oldVal)
{
	dexterity = newVal;
}

void UCombatInterface::Set_damage(const int32& newVal, const int32& oldVal)
{
	damage = newVal;
}

void UCombatInterface::Set_magic_damage(const int32& newVal, const int32& oldVal)
{
	magic_damage = newVal;
}

void UCombatInterface::Set_armor(const int32& newVal, const int32& oldVal)
{
	armor = newVal;
}

void UCombatInterface::Set_magic_armor(const int32& newVal, const int32& oldVal)
{
	magic_armor = newVal;
}

void UCombatInterface::Set_criticalstrike(const int32& newVal, const int32& oldVal)
{
	criticalstrike = newVal;
}

void UCombatInterface::Set_discern(const int32& newVal, const int32& oldVal)
{
	discern = newVal;
}

void UCombatInterface::Set_parry(const int32& newVal, const int32& oldVal)
{
	parry = newVal;
}

void UCombatInterface::Set_speed(const int32& newVal, const int32& oldVal)
{
	speed = newVal;
}

void UCombatInterface::Set_hitrate(const int32& newVal, const int32& oldVal)
{
	hitrate = newVal;
}

void UCombatInterface::Set_dodgerate(const int32& newVal, const int32& oldVal)
{
	dodgerate = newVal;
}

void UCombatInterface::Set_healingrate(const int32& newVal, const int32& oldVal)
{
	healingrate = newVal;
}

void UCombatInterface::Set_camp(const int32& newVal, const int32& oldVal)
{
	camp = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnCampChanged.Broadcast( EntityID, camp );
	}
}

void UCombatInterface::Set_feats(const int32& newVal, const int32& oldVal)
{
	feats = newVal;
}

void UCombatInterface::Set_potential(const int32& newVal, const int32& oldVal)
{
	potential = newVal;
}

void UCombatInterface::Set_xiuwei(const int32& newVal, const int32& oldVal)
{
	xiuwei = newVal;
}

void UCombatInterface::Set_xiuweiLevel(const int32& newVal, const int32& oldVal)
{
	xiuweiLevel = newVal;
}

void UCombatInterface::Set_gangQiValue(const int32& newVal, const int32& oldVal)
{
	gangQiValue = newVal;

	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnGangQiChanged.Broadcast( EntityID, gangQiValue,  gangQiValue_Max);
	}
}

void UCombatInterface::Set_gangQiValue_Max(const int32& newVal, const int32& oldVal)
{
	gangQiValue_Max = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnGangQiChanged.Broadcast( EntityID, gangQiValue,  gangQiValue_Max);
	}
}

void UCombatInterface::Set_gangQiState(const int32& newVal, const int32& oldVal)
{
	gangQiState = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnGangQiStateChanged.Broadcast( EntityID, gangQiState);
	}
}

void UCombatInterface::Set_tempCamp(const int32& newVal, const int32& oldVal)
{
	tempCamp = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnTempCampChanged.Broadcast(  EntityID, tempCamp );
	}
}

void UCombatInterface::Set_jingjieLevel(const int32& newVal, const int32& oldVal)
{
	jingjieLevel = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnJingJieLevelChanged.Broadcast(  EntityID, jingjieLevel );
	}
}

void UCombatInterface::Set_gangQi_qiJieProgress(const int32& newVal, const int32& oldVal)
{
	gangQi_qiJieProgress = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnGangQiProgressChanged.Broadcast( EntityID,  gangQi_qiJieProgress, gangQiValue_Max );
	}
}

void UCombatInterface::Set_combatPower(const int32& newVal, const int32& oldVal)
{
	combatPower = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		TArray<FVariant> args;
		args.Add(EntityID);
		args.Add(combatPower);
		UUECS3GameInstance::Instance->GEventManager->OnCombatPowerChanged.Broadcast(EntityID, combatPower);
	}
}

void UCombatInterface::Set_killingValue(const int32& newVal, const int32& oldVal)
{
	killingValue = newVal;
}

void UCombatInterface::Set_vitPoint(const int32& newVal, const int32& oldVal)
{
	vitPoint = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnPlayerVitPointChanged.Broadcast( EntityID, vitPoint, vitPoint_Max );
	}
}

void UCombatInterface::Set_vitPoint_Max(const int32& newVal, const int32& oldVal)
{
	vitPoint_Max = newVal;
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->GEventManager))
	{
		UUECS3GameInstance::Instance->GEventManager->OnPlayerVitPointChanged.Broadcast( EntityID, vitPoint, vitPoint_Max );
	}
}

void UCombatInterface::Set_cure(const int32 & newVal, const int32 & oldVal)
{
	cure = newVal;
}

void UCombatInterface::Set_ice_damage(const int32 & newVal, const int32 & oldVal)
{
	ice_damage = newVal;
}

void UCombatInterface::Set_fire_damage(const int32 & newVal, const int32 & oldVal)
{
	fire_damage = newVal;
}

void UCombatInterface::Set_thunder_damage(const int32 & newVal, const int32 & oldVal)
{
	thunder_damage = newVal;
}

void UCombatInterface::Set_xuan_damage(const int32 & newVal, const int32 & oldVal)
{
	xuan_damage = newVal;
}

void UCombatInterface::Set_ice_armor(const int32 & newVal, const int32 & oldVal)
{
	ice_armor = newVal;
}

void UCombatInterface::Set_fire_armor(const int32 & newVal, const int32 & oldVal)
{
	fire_armor = newVal;
}

void UCombatInterface::Set_thunder_armor(const int32 & newVal, const int32 & oldVal)
{
	thunder_armor = newVal;
}

void UCombatInterface::Set_xuan_armor(const int32 & newVal, const int32 & oldVal)
{
	xuan_armor = newVal;
}

void UCombatInterface::Set_damage_ignore(const int32 & newVal, const int32 & oldVal)
{
	damage_ignore = newVal;
}

void UCombatInterface::Set_magic_damage_ignore(const int32 & newVal, const int32 & oldVal)
{
	magic_damage_ignore = newVal;
}

void UCombatInterface::Set_armor_ignore(const int32 & newVal, const int32 & oldVal)
{
	armor_ignore = newVal;
}

void UCombatInterface::Set_magic_armor_ignore(const int32 & newVal, const int32 & oldVal)
{
	magic_armor_ignore = newVal;
}

void UCombatInterface::Set_criticalstrike_ignore(const int32 & newVal, const int32 & oldVal)
{
	criticalstrike_ignore = newVal;
}

void UCombatInterface::Set_parry_ignore(const int32 & newVal, const int32 & oldVal)
{
	parry_ignore = newVal;
}

void UCombatInterface::Set_hitrate_ignore(const int32 & newVal, const int32 & oldVal)
{
	hitrate_ignore = newVal;
}

void UCombatInterface::Set_dodgerate_ignore(const int32 & newVal, const int32 & oldVal)
{
	dodgerate_ignore = newVal;
}

void UCombatInterface::Set_ice_damage_ignore(const int32 & newVal, const int32 & oldVal)
{
	ice_damage_ignore = newVal;
}

void UCombatInterface::Set_fire_damage_ignore(const int32 & newVal, const int32 & oldVal)
{
	fire_damage_ignore = newVal;
}

void UCombatInterface::Set_thunder_damage_ignore(const int32 & newVal, const int32 & oldVal)
{
	thunder_damage_ignore = newVal;
}

void UCombatInterface::Set_xuan_damage_ignore(const int32 & newVal, const int32 & oldVal)
{
	xuan_damage_ignore = newVal;
}

void UCombatInterface::Set_ice_armor_ignore(const int32 & newVal, const int32 & oldVal)
{
	ice_armor_ignore = newVal;
}

void UCombatInterface::Set_fire_armor_ignore(const int32 & newVal, const int32 & oldVal)
{
	fire_armor_ignore = newVal;
}

void UCombatInterface::Set_thunder_armor_ignore(const int32 & newVal, const int32 & oldVal)
{
	thunder_armor_ignore = newVal;
}

void UCombatInterface::Set_xuan_armor_ignore(const int32 & newVal, const int32 & oldVal)
{
	xuan_armor_ignore = newVal;

}

void UCombatInterface::Set_depress_resist(const int32 & newVal, const int32 & oldVal)
{
	depress_resist = newVal;
}

void UCombatInterface::Set_hitback_resist(const int32 & newVal, const int32 & oldVal)
{
	hitback_resist = newVal;
}

void UCombatInterface::Set_control_resist(const int32 & newVal, const int32 & oldVal)
{
	control_resist = newVal;
}

void UCombatInterface::Set_insane_resist(const int32 & newVal, const int32 & oldVal)
{
	insane_resist = newVal;
}

CONTROL_COMPILE_OPTIMIZE_END