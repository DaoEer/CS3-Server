
#include "SpaceEntityRelation.h"
#include "Util/CS3Debug.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Interface/SkillInterface.h"
#include "Interface/GameObjectInterface.h"
#include "Interface/Role/RoleTeamInterface.h"
#include "Interface/Role/RoleInterface.h"
#include "Interface/Role/RoleTongInterface.h"
#include "Manager/SpaceEntityRelationMgr.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CS3Base/GameObject.h"
#include "Entity/Monster/CMonster.h"
#include "Entity/Role/CS3Role.h"

CONTROL_COMPILE_OPTIMIZE_START

URelationBase::URelationBase()
{
	//AddToRoot();
}

COMBAT_RELATION URelationBase::GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity)
{
	return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
}

COMBAT_RELATION URelMonster_Default::GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity)
{
	AMonsterCharacter* SrcCharacter = Cast<AMonsterCharacter>(SrcEntity->Actor());
	AServerCharacter* TargetCharacter = Cast<AServerCharacter>(TargetEntity->Actor());
	if (!IsValid(SrcCharacter) || !IsValid(TargetCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelMonster_Default::GetRelation: SrcCharacter || TargetCharacter!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	///潜入Buff
	USkillInterface* SrcSkillInterface = ((GameObject*)SrcEntity)->Interface_Cache.SkillInterface;
	UGameObjectInterface* TargetInterface =((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	if (!IsValid(TargetInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelMonster_Default::GetRelation: TargetInterface!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	if (IsValid(SrcSkillInterface) && SrcSkillInterface->findBuffsByBuffScript("BuffSlipInto").Num() > 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	///替身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///分身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_FENSHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///CMonster
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT))
	{
		TargetEntity = static_cast< CMonster* >(TargetEntity)->GetControlEntity();
	}
	///幻兽
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_VEHICLEPET))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "baseOwnerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///傀儡
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_GHOST_RECEIVER))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	/// 这里做的原因:(TargetEntity 可能会变) 玩家召唤替身(Monster)，当另一个玩家查看与该替身关系时，就是查看与召唤出该替身的玩家的关系
	TargetInterface =((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	USkillInterface * TargetSkillInterface = ((GameObject*)TargetEntity)->Interface_Cache.SkillInterface;
	if (!IsValid(TargetInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelMonster_Default::GetRelation: TargetInterface!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	if (IsValid(TargetSkillInterface) && TargetSkillInterface->findBuffsByBuffScript("BuffSlipInto").Num() > 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	int32 SrcCamp = SrcCharacter->GetFinalCamp();
	
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
	{
		APlayerCharacter* RoleCharacter = Cast<APlayerCharacter>(TargetEntity->Actor());
		if (RoleCharacter && RoleCharacter->HasRoleFlag(ROLE_FLAG::ROLE_FLAG_WATCHER))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}
		if (SrcCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_NORMAL_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}
		if (SrcCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_ENEMY_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}
		if (IsValid(RoleCharacter))
		{
			int32 TargetCamp = RoleCharacter->GetFinalCamp();
			COMBAT_RELATION CampRelation = UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetCampRelation(SrcCamp, TargetCamp);
			if (CampRelation != COMBAT_RELATION::COMBAT_RELATION_DEFAULT)
			{
				return CampRelation;
			}
		}
		return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
	}
	else if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER))
	{
		AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(TargetEntity->Actor());
		if (SrcCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_NORMAL_TO_MONSTER)&& TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_NORMAL_TO_MONSTER))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}
		else if(SrcCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_ENEMY_TO_MONSTER) && TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_ENEMY_TO_MONSTER))
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}
		///势力判断
		int32 SrcFaction = SrcCharacter->GetFinalfaction();
		int32 TargetFaction = MonsterCharacter->GetFinalfaction();
		COMBAT_RELATION FactionRelation = UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetCampRelation(SrcFaction, TargetFaction);
		if (FactionRelation != COMBAT_RELATION::COMBAT_RELATION_DEFAULT)
		{
			return FactionRelation;
		}
		///阵营判断
		int32 TargetCamp = MonsterCharacter->GetFinalCamp();
		COMBAT_RELATION CampRelation = UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetCampRelation(SrcCamp, TargetCamp);
		if (CampRelation != COMBAT_RELATION::COMBAT_RELATION_DEFAULT)
		{
			return CampRelation;
		}
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;	
	}else {
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
}

COMBAT_RELATION URelCMonster_Default::GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity)
{

	CMonster* selfEntity = StaticCast<CMonster*>(SrcEntity);
	CS3Role* ctrlRole = selfEntity->GetControlRole();
	if (ctrlRole == nullptr)
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;

	return ctrlRole->QueryRelation(TargetEntity);
}

COMBAT_RELATION URelRole_Camp::GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity)
{
	APlayerCharacter* RoleCharacter = Cast<APlayerCharacter>(SrcEntity->Actor());
	AServerCharacter* TargetCharacter = Cast<AServerCharacter>(TargetEntity->Actor());
	if (!IsValid(RoleCharacter)  || !IsValid(TargetCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_Camp::GetRelation: RoleCharacter || TargetCharacter!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	///观察者标志位
	if (RoleCharacter->HasRoleFlag(ROLE_FLAG::ROLE_FLAG_WATCHER))
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	
	///潜入Buff
	USkillInterface * RoleSkillInterface = ((GameObject*)SrcEntity)->Interface_Cache.SkillInterface;
	UGameObjectInterface* TargetInterface =((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	if (!IsValid(TargetInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_Camp::GetRelation: TargetInterface!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	if (IsValid(RoleSkillInterface) && RoleSkillInterface->findBuffsByBuffScript("BuffSlipInto").Num() > 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	///替身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///分身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_FENSHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///CMonster
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT))
	{
		TargetEntity = static_cast<CMonster*>(TargetEntity)->GetControlEntity();
	}
	///幻兽
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_VEHICLEPET))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "baseOwnerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///傀儡
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_GHOST_RECEIVER))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	if (nullptr == TargetEntity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_Camp::GetRelation: TargetEntity!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	/// 这里做的原因:(TargetEntity 可能会变) 玩家召唤替身(Monster)，当另一个玩家查看与该替身关系时，就是查看与召唤出该替身的玩家的关系
	TargetInterface =((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	USkillInterface * TargetSkillInterface = ((GameObject*)TargetEntity)->Interface_Cache.SkillInterface;
	if (!IsValid(TargetInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_Camp::GetRelation: TargetInterface!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	if (IsValid(TargetSkillInterface) && TargetSkillInterface->findBuffsByBuffScript("BuffSlipInto").Num() > 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	int32 RoleCamp = RoleCharacter->GetFinalCamp();
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
	{
		///心魔buff
		if ((IsValid(RoleSkillInterface) && RoleSkillInterface->findBuffsByBuffScript("BuffXinMoCtrl").Num() > 0)
			|| (IsValid(TargetSkillInterface) && TargetSkillInterface->findBuffsByBuffScript("BuffXinMoCtrl").Num() > 0))
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}

		///队伍成员友好
		URoleTeamInterface* RoleTeamInterface = ((GameObject*)SrcEntity)->Interface_Cache.RoleTeamInterface;
		if (RoleTeamInterface)
		{
			if (RoleTeamInterface->IsTeammate(TargetEntity->ID()))
			{
				return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
			}
		}
		
		int32 TargetCamp = TargetCharacter->GetFinalCamp();
		COMBAT_RELATION CampRelation = UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetCampRelation(RoleCamp, TargetCamp);
		if (CampRelation != COMBAT_RELATION::COMBAT_RELATION_DEFAULT)
		{
			return CampRelation;
		}

		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	else if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER))
	{
		int32 TargetState = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), TEXT("state"));
		if (TargetState == int32(ENTITY_STATE::EntityStateReset))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NONE;
		}
		
		if (TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_NORMAL_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}

		if (TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_ENEMY_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}

		int32 TargetCamp = TargetCharacter->GetFinalCamp();
		COMBAT_RELATION CampRelation = UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetCampRelation(RoleCamp, TargetCamp);
		if (CampRelation != COMBAT_RELATION::COMBAT_RELATION_DEFAULT)
		{
			return CampRelation;
		}

		return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
	}
	else if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_NPC))
	{
		int32 TargetCamp = TargetCharacter->GetFinalCamp();
		COMBAT_RELATION CampRelation = UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetCampRelation(RoleCamp, TargetCamp);
		if (CampRelation != COMBAT_RELATION::COMBAT_RELATION_DEFAULT)
		{
			return CampRelation;
		}

		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	else
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
}

COMBAT_RELATION URelRole_PKMode::GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity)
{
	if (nullptr == TargetEntity || SrcEntity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_PKMode::GetRelation: TargetInterface!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	APlayerCharacter* RoleCharacter = Cast<APlayerCharacter>(SrcEntity->Actor());
	AServerCharacter* TargetCharacter = Cast<AServerCharacter>(TargetEntity->Actor());
	if (!IsValid(RoleCharacter) || !IsValid(TargetCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_PKMode::GetRelation: RoleCharacter || TargetCharacter!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	///观察者标志位
	if (RoleCharacter->HasRoleFlag(ROLE_FLAG::ROLE_FLAG_WATCHER))
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	///潜入Buff
	USkillInterface * RoleSkillInterface = ((GameObject*)SrcEntity)->Interface_Cache.SkillInterface;

	if (!IsValid(RoleSkillInterface) || RoleSkillInterface->findBuffsByBuffScript("BuffSlipInto").Num() > 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	UGameObjectInterface* TargetInterface =((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	if (IsValid(TargetInterface))
	{
		///替身
		if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN))
		{
			int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
			TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
		}
		///分身
		if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_FENSHEN))
		{
			int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
			TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
		}
		///CMonster
		if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT))
		{
			TargetEntity = static_cast<CMonster*>(TargetEntity)->GetControlEntity();
		}
		///幻兽
		if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_VEHICLEPET))
		{
			int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "baseOwnerID");
			TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
		}
		///傀儡
		if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_GHOST_RECEIVER))
		{
			int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
			TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
		}
	}
	if (nullptr == TargetEntity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_PKMode::GetRelation: TargetEntity!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	USkillInterface * TargetSkillInterface = ((GameObject*)TargetEntity)->Interface_Cache.SkillInterface;
	if (IsValid(TargetSkillInterface) && TargetSkillInterface->findBuffsByBuffScript("BuffSlipInto").Num() > 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	TargetInterface =((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	if (!IsValid(TargetInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_PKMode::GetRelation: TargetInterface!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	int32 RoleCamp = RoleCharacter->GetFinalCamp();
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
	{
		///心魔buff
		if ((RoleSkillInterface->findBuffsByBuffScript("BuffXinMoCtrl").Num() > 0)
			|| (IsValid(TargetSkillInterface) && TargetSkillInterface->findBuffsByBuffScript("BuffXinMoCtrl").Num() > 0))
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}

		///队伍成员友好
		URoleTeamInterface* RoleTeamInterface = ((GameObject*)SrcEntity)->Interface_Cache.RoleTeamInterface;
		if (RoleTeamInterface)
		{
			if (RoleTeamInterface->IsTeammate(TargetEntity->ID()))
			{
				return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
			}
		}

		URoleInterface* RoleInterface = Cast<URoleInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("GameObjectInterface"), SrcEntity->ID()));
		if (RoleInterface)
		{
			COMBAT_RELATION CampRelation = RoleInterface->GetPkModeRelation(TargetEntity);
			if (CampRelation != COMBAT_RELATION::COMBAT_RELATION_DEFAULT)
			{
				return CampRelation;
			}
		}

		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	else if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER))
	{
		int32 TargetState = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), TEXT("state"));
		if (TargetState == int32(ENTITY_STATE::EntityStateReset))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NONE;
		}

		if (TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_NORMAL_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}

		if (TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_ENEMY_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}

		int32 TargetCamp = TargetCharacter->GetFinalCamp();
		COMBAT_RELATION CampRelation = UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetCampRelation(RoleCamp, TargetCamp);
		if (CampRelation != COMBAT_RELATION::COMBAT_RELATION_DEFAULT)
		{
			return CampRelation;
		}

		return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
	}
	else if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_NPC))
	{
		int32 TargetCamp = TargetCharacter->GetFinalCamp();
		COMBAT_RELATION CampRelation = UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetCampRelation(RoleCamp, TargetCamp);
		if (CampRelation != COMBAT_RELATION::COMBAT_RELATION_DEFAULT)
		{
			return CampRelation;
		}

		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	else
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
}

COMBAT_RELATION URelRole_Peace::GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity)
{
	if (nullptr == TargetEntity || SrcEntity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_Peace::GetRelation:TargetEntity || SrcEntity!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	APlayerCharacter* RoleCharacter = Cast<APlayerCharacter>(SrcEntity->Actor());
	AServerCharacter* TargetCharacter = Cast<AServerCharacter>(TargetEntity->Actor());
	if (!IsValid(RoleCharacter) || !IsValid(TargetCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_Peace::GetRelation:RoleCharacter || TargetCharacter!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	///观察者标志位
	if (RoleCharacter->HasRoleFlag(ROLE_FLAG::ROLE_FLAG_WATCHER))
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	///潜入Buff
	USkillInterface * RoleSkillInterface = ((GameObject*)SrcEntity)->Interface_Cache.SkillInterface;
	UGameObjectInterface* TargetInterface =((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;

	if (!IsValid(RoleSkillInterface) || !IsValid(TargetInterface) || RoleSkillInterface->findBuffsByBuffScript("BuffSlipInto").Num() > 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	///替身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///分身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_FENSHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///CMonster
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT))
	{
		TargetEntity = static_cast<CMonster*>(TargetEntity)->GetControlEntity();
	}
	///幻兽
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_VEHICLEPET))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "baseOwnerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///傀儡
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_GHOST_RECEIVER))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	if (nullptr == TargetEntity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_Peace::GetRelation:TargetEntity!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	USkillInterface * TargetSkillInterface = ((GameObject*)TargetEntity)->Interface_Cache.SkillInterface;
	if (IsValid(TargetSkillInterface) && TargetSkillInterface->findBuffsByBuffScript("BuffSlipInto").Num() > 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	TargetInterface =((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	if (!IsValid(TargetInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_Peace::GetRelation:TargetInterface!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	int32 RoleCamp = RoleCharacter->GetFinalCamp();
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	else if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER))
	{
		int32 TargetState = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), TEXT("state"));
		if (TargetState == int32(ENTITY_STATE::EntityStateReset))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NONE;
		}

		if (TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_NORMAL_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}

		if (TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_ENEMY_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}

		int32 TargetCamp = TargetCharacter->GetFinalCamp();
		COMBAT_RELATION CampRelation = UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetCampRelation(RoleCamp, TargetCamp);
		if (CampRelation != COMBAT_RELATION::COMBAT_RELATION_DEFAULT)
		{
			return CampRelation;
		}

		return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
	}
	else if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_NPC))
	{
		int32 TargetCamp = TargetCharacter->GetFinalCamp();
		COMBAT_RELATION CampRelation = UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetCampRelation(RoleCamp, TargetCamp);
		if (CampRelation != COMBAT_RELATION::COMBAT_RELATION_DEFAULT)
		{
			return CampRelation;
		}

		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	else
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
}

COMBAT_RELATION URelRole_Enemy::GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity)
{
	if (nullptr == TargetEntity || SrcEntity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_Enemy::GetRelation:TargetEntity || SrcEntity!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	APlayerCharacter* RoleCharacter = Cast<APlayerCharacter>(SrcEntity->Actor());
	AServerCharacter* TargetCharacter = Cast<AServerCharacter>(TargetEntity->Actor());
	if (!IsValid(RoleCharacter) || !IsValid(TargetCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_Enemy::GetRelation:RoleCharacter || TargetCharacter!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	///观察者标志位
	if (RoleCharacter->HasRoleFlag(ROLE_FLAG::ROLE_FLAG_WATCHER))
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	///潜入Buff
	USkillInterface * RoleSkillInterface = ((GameObject*)SrcEntity)->Interface_Cache.SkillInterface;
	UGameObjectInterface* TargetInterface =((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	if (!IsValid(RoleSkillInterface) || !IsValid(TargetInterface)|| RoleSkillInterface->findBuffsByBuffScript("BuffSlipInto").Num() > 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	///替身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///分身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_FENSHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///CMonster
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT))
	{
			TargetEntity = static_cast<CMonster*>(TargetEntity)->GetControlEntity();
	}
	///幻兽
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_VEHICLEPET))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "baseOwnerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///傀儡
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_GHOST_RECEIVER))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	if (nullptr == TargetEntity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_Enemy::GetRelation:TargetEntity!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	USkillInterface * TargetSkillInterface = ((GameObject*)TargetEntity)->Interface_Cache.SkillInterface;
	if (IsValid(TargetSkillInterface) && TargetSkillInterface->findBuffsByBuffScript("BuffSlipInto").Num() > 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	TargetInterface =((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	if (!IsValid(TargetInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_Enemy::GetRelation:TargetInterface!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	int32 RoleCamp = RoleCharacter->GetFinalCamp();
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
	{
		if (TargetInterface->GetEntity()->ID() == SrcEntity->ID())
		{
			return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}
		else
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}
		
	}
	else if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER))
	{
		int32 TargetState = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), TEXT("state"));
		if (TargetState == int32(ENTITY_STATE::EntityStateReset))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NONE;
		}

		if (TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_NORMAL_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}

		if (TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_ENEMY_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}

		int32 TargetCamp = TargetCharacter->GetFinalCamp();
		COMBAT_RELATION CampRelation = UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetCampRelation(RoleCamp, TargetCamp);
		if (CampRelation != COMBAT_RELATION::COMBAT_RELATION_DEFAULT)
		{
			return CampRelation;
		}

		return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
	}
	else if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_NPC))
	{
		int32 TargetCamp = TargetCharacter->GetFinalCamp();
		COMBAT_RELATION CampRelation = UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetCampRelation(RoleCamp, TargetCamp);
		if (CampRelation != COMBAT_RELATION::COMBAT_RELATION_DEFAULT)
		{
			return CampRelation;
		}

		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	else
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
}
COMBAT_RELATION URelRole_TongStarcraft::GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity)
{
	if (nullptr == TargetEntity || SrcEntity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_TongStarcraft::GetRelation:TargetEntity || SrcEntity!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	APlayerCharacter* RoleCharacter = Cast<APlayerCharacter>(SrcEntity->Actor());
	AServerCharacter* TargetCharacter = Cast<AServerCharacter>(TargetEntity->Actor());
	if (!IsValid(RoleCharacter) || !IsValid(TargetCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_TongStarcraft::GetRelation:RoleCharacter ||  TargetCharacter!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	///观察者标志位
	if (RoleCharacter->HasRoleFlag(ROLE_FLAG::ROLE_FLAG_WATCHER))
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	///潜入Buff
	USkillInterface * RoleSkillInterface = ((GameObject*)SrcEntity)->Interface_Cache.SkillInterface;
	UGameObjectInterface* TargetInterface =((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	if (!IsValid(RoleSkillInterface) || !IsValid(TargetInterface) || RoleSkillInterface->findBuffsByBuffScript("BuffSlipInto").Num() > 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	///替身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///分身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_FENSHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///CMonster
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT))
	{
		TargetEntity = static_cast<CMonster*>(TargetEntity)->GetControlEntity();
	}
	///幻兽
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_VEHICLEPET))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "baseOwnerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///傀儡
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_GHOST_RECEIVER))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	if (nullptr == TargetEntity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_TongStarcraft::GetRelation:TargetEntity!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	USkillInterface * TargetSkillInterface = ((GameObject*)TargetEntity)->Interface_Cache.SkillInterface;
	if (IsValid(TargetSkillInterface) && TargetSkillInterface->findBuffsByBuffScript("BuffSlipInto").Num() > 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	TargetInterface =((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	if (!IsValid(TargetInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_TongStarcraft::GetRelation:TargetInterface!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	int32 RoleCamp = RoleCharacter->GetFinalCamp();
	uint64 srcDBID = SrcEntity->GetDefinedProperty(TEXT("tongDBID")).GetValue<uint64>();
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE) && !(TargetEntity->GetDefinedProperty(TEXT("tongDBID")).GetValue<uint64>() == srcDBID))
	{
		return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
	}
	else if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER))
	{
		int32 TargetState = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), TEXT("state"));
		if (TargetState == int32(ENTITY_STATE::EntityStateReset))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NONE;
		}

		if (TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_NORMAL_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}

		if (TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_ENEMY_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}

		int32 TargetCamp = TargetCharacter->GetFinalCamp();
		COMBAT_RELATION CampRelation = UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetCampRelation(RoleCamp, TargetCamp);
		if (CampRelation != COMBAT_RELATION::COMBAT_RELATION_DEFAULT)
		{
			return CampRelation;
		}

		return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
	}
	else if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_NPC))
	{
		int32 TargetCamp = TargetCharacter->GetFinalCamp();
		COMBAT_RELATION CampRelation = UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetCampRelation(RoleCamp, TargetCamp);
		if (CampRelation != COMBAT_RELATION::COMBAT_RELATION_DEFAULT)
		{
			return CampRelation;
		}

		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	else
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
}

COMBAT_RELATION URelTrapObject_Default::GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity)
{
	if (nullptr == TargetEntity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_TongStarcraft::GetRelation:TargetEntity!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	AServerCharacter* TargetCharacter = Cast<AServerCharacter>(TargetEntity->Actor());
	if (!IsValid(TargetCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_TongStarcraft::GetRelation:TargetCharacter!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	UGameObjectInterface* TargetInterface =((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	if (!IsValid(TargetInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_TongStarcraft::GetRelation:TargetInterface!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
	{
		if (TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_EMENY_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}
		if (TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_FRIEND_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}
	}
	return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
}

COMBAT_RELATION URelNPC_Default::GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity)
{
	return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
}

COMBAT_RELATION URelSpellBox_Default::GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity)
{
	return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
}

COMBAT_RELATION URelMovingPlatform_Default::GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity)
{
	return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
}

COMBAT_RELATION URelVehiclePet_Default::GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity)
{
	if (nullptr == TargetEntity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelVehiclePet_Default::GetRelation:TargetEntity!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	UGameObjectInterface* TargetInterface =((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	if (!IsValid(TargetInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelVehiclePet_Default::GetRelation:TargetInterface!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	///替身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///分身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_FENSHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///CMonster
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT))
	{
		TargetEntity = static_cast<CMonster*>(TargetEntity)->GetControlEntity();
	}
	///幻兽
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_VEHICLEPET))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "baseOwnerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///傀儡
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_GHOST_RECEIVER))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	if (!TargetEntity)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	int32 SrcOwnerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(SrcEntity->ID(), "baseOwnerID");
	GameObject* OwnerEntity = (GameObject*)UGolbalBPFunctionLibrary::FindEntity(SrcOwnerID);
	if (OwnerEntity)
	{
		return OwnerEntity->QueryRelation(TargetEntity);
	}else{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
}


COMBAT_RELATION URelGhostReceiver_Default::GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity)
{
	if (nullptr == TargetEntity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelVehiclePet_Default::GetRelation:TargetEntity!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	UGameObjectInterface* TargetInterface =((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	if (!IsValid(TargetInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelVehiclePet_Default::GetRelation:TargetInterface!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	///替身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///分身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_FENSHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///CMonster
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT))
	{
		TargetEntity = static_cast<CMonster*>(TargetEntity)->GetControlEntity();
	}
	///幻兽
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_VEHICLEPET))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "baseOwnerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///傀儡
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_GHOST_RECEIVER))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	if (!TargetEntity)
	{
		return COMBAT_RELATION::COMBAT_RELATION_DEFAULT;
	}
	int32 SrcOwnerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(SrcEntity->ID(), "baseOwnerID");
	GameObject* OwnerEntity = (GameObject*)UGolbalBPFunctionLibrary::FindEntity(SrcOwnerID);
	if (OwnerEntity)
	{
		return OwnerEntity->QueryRelation(TargetEntity);
	}
	else {
		return COMBAT_RELATION::COMBAT_RELATION_DEFAULT;
	}
}

COMBAT_RELATION URelRole_TeamStarcraft::GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity)
{
	if (nullptr == TargetEntity || SrcEntity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_TeamStarcraft::GetRelation:TargetEntity || SrcEntity!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	APlayerCharacter* RoleCharacter = Cast<APlayerCharacter>(SrcEntity->Actor());
	AServerCharacter* TargetCharacter = Cast<AServerCharacter>(TargetEntity->Actor());
	if (!IsValid(RoleCharacter) || !IsValid(TargetCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_TeamStarcraft::GetRelation:RoleCharacter ||  TargetCharacter!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	///观察者标志位
	if (RoleCharacter->HasRoleFlag(ROLE_FLAG::ROLE_FLAG_WATCHER))
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	///潜入Buff
	USkillInterface * RoleSkillInterface = ((GameObject*)SrcEntity)->Interface_Cache.SkillInterface;
	UGameObjectInterface* TargetInterface =((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	if (!IsValid(RoleSkillInterface) || !IsValid(TargetInterface) || RoleSkillInterface->findBuffsByBuffScript("BuffSlipInto").Num() > 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	///替身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///分身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_FENSHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///CMonster
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT))
	{
		TargetEntity = static_cast<CMonster*>(TargetEntity)->GetControlEntity();
	}
	///幻兽
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_VEHICLEPET))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "baseOwnerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///傀儡
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_GHOST_RECEIVER))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	if (nullptr == TargetEntity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_TeamStarcraft::GetRelation:TargetEntity!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	USkillInterface * TargetSkillInterface = ((GameObject*)TargetEntity)->Interface_Cache.SkillInterface;
	if (IsValid(TargetSkillInterface) && TargetSkillInterface->findBuffsByBuffScript("BuffSlipInto").Num() > 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	TargetInterface =((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	if (!IsValid(TargetInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRole_TeamStarcraft::GetRelation:TargetInterface!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	int32 RoleCamp = RoleCharacter->GetFinalCamp();
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
	{
		URoleTeamInterface* SrcEntityTeamID = ((GameObject*)SrcEntity)->Interface_Cache.RoleTeamInterface;
		URoleTeamInterface* TargetEntityTeamID = ((GameObject*)TargetEntity)->Interface_Cache.RoleTeamInterface;
		if (SrcEntityTeamID && TargetEntityTeamID && !(SrcEntityTeamID->Team_ID ==TargetEntityTeamID->Team_ID))
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	else if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER))
	{
		int32 TargetState = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), TEXT("state"));
		if (TargetState == int32(ENTITY_STATE::EntityStateReset))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NONE;
		}

		if (TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_NORMAL_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}

		if (TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_ENEMY_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}

		int32 TargetCamp = TargetCharacter->GetFinalCamp();
		COMBAT_RELATION CampRelation = UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetCampRelation(RoleCamp, TargetCamp);
		if (CampRelation != COMBAT_RELATION::COMBAT_RELATION_DEFAULT)
		{
			return CampRelation;
		}

		return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
	}
	else if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_NPC))
	{
		int32 TargetCamp = TargetCharacter->GetFinalCamp();
		COMBAT_RELATION CampRelation = UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetCampRelation(RoleCamp, TargetCamp);
		if (CampRelation != COMBAT_RELATION::COMBAT_RELATION_DEFAULT)
		{
			return CampRelation;
		}

		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	else
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
}

COMBAT_RELATION URelRoleEntityRelationGCZ::GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity)
{
	APlayerCharacter* RoleCharacter = Cast<APlayerCharacter>(SrcEntity->Actor());
	AServerCharacter* TargetCharacter = Cast<AServerCharacter>(TargetEntity->Actor());
	if (!IsValid(RoleCharacter) || !IsValid(TargetCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRoleEntityRelationGCZ::GetRelation: RoleCharacter || TargetCharacter!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	///观察者标志位
	if (RoleCharacter->HasRoleFlag(ROLE_FLAG::ROLE_FLAG_WATCHER))
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	///潜入Buff
	USkillInterface * RoleSkillInterface = ((GameObject*)SrcEntity)->Interface_Cache.SkillInterface;
	UGameObjectInterface* TargetInterface = ((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	if (!IsValid(TargetInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRoleEntityRelationGCZ::GetRelation: TargetInterface!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	if (IsValid(RoleSkillInterface) && RoleSkillInterface->findBuffsByBuffScript("BuffSlipInto").Num() > 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	///替身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///分身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_FENSHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///CMonster
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT))
	{
		TargetEntity = static_cast<CMonster*>(TargetEntity)->GetControlEntity();
	}
	///幻兽
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_VEHICLEPET))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "baseOwnerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///傀儡
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_GHOST_RECEIVER))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	if (nullptr == TargetEntity)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRoleEntityRelationGCZ::GetRelation: TargetEntity!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	/// 这里做的原因:(TargetEntity 可能会变) 玩家召唤替身(Monster)，当另一个玩家查看与该替身关系时，就是查看与召唤出该替身的玩家的关系
	TargetInterface = ((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	USkillInterface * TargetSkillInterface = ((GameObject*)TargetEntity)->Interface_Cache.SkillInterface;
	if (!IsValid(TargetInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelRoleEntityRelationGCZ::GetRelation: TargetInterface!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	if (IsValid(TargetSkillInterface) && TargetSkillInterface->findBuffsByBuffScript("BuffSlipInto").Num() > 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER))
	{
		int32 TargetState = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), TEXT("state"));
		if (TargetState == int32(ENTITY_STATE::EntityStateReset))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NONE;
		}

		if (TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_NORMAL_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}

		if (TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_ENEMY_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}
	}
	int32 targetBelongSide = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), TEXT("belongSide"));
	int32 srcBelongSide = UGolbalBPFunctionLibrary::GetIntPropertyValue(SrcEntity->ID(), TEXT("belongSide"));
	if (targetBelongSide != srcBelongSide)
	{
		return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
	}
	else
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
}

COMBAT_RELATION URelEntityRelationGCZ::GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity)
{
	AServerCharacter* SrcCharacter = Cast<AServerCharacter>(SrcEntity->Actor());
	AServerCharacter* TargetCharacter = Cast<AServerCharacter>(TargetEntity->Actor());
	if (!IsValid(SrcCharacter) || !IsValid(TargetCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelEntityRelationGCZ::GetRelation: SrcCharacter || TargetCharacter!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	///潜入Buff
	USkillInterface* SrcSkillInterface = ((GameObject*)SrcEntity)->Interface_Cache.SkillInterface;
	UGameObjectInterface* TargetInterface = ((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	if (!IsValid(TargetInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelEntityRelationGCZ::GetRelation: TargetInterface!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	if (IsValid(SrcSkillInterface) && SrcSkillInterface->findBuffsByBuffScript("BuffSlipInto").Num() > 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	///替身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_EXT_TISHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///分身
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_FENSHEN))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///CMonster
	if (TargetInterface->IsEntityFlagExt(ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT))
	{
		TargetEntity = static_cast<CMonster*>(TargetEntity)->GetControlEntity();
	}
	///幻兽
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_VEHICLEPET))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "baseOwnerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	///傀儡
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_GHOST_RECEIVER))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "ownerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
	}
	/// 这里做的原因:(TargetEntity 可能会变) 玩家召唤替身(Monster)，当另一个玩家查看与该替身关系时，就是查看与召唤出该替身的玩家的关系
	if (!TargetEntity)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	TargetInterface = ((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	USkillInterface * TargetSkillInterface = ((GameObject*)TargetEntity)->Interface_Cache.SkillInterface;
	if (!IsValid(TargetInterface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelEntityRelationGCZ::GetRelation: TargetInterface!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	if (IsValid(TargetSkillInterface) && TargetSkillInterface->findBuffsByBuffScript("BuffSlipInto").Num() > 0)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
	{
		APlayerCharacter* RoleCharacter = Cast<APlayerCharacter>(TargetEntity->Actor());
		if (RoleCharacter && RoleCharacter->HasRoleFlag(ROLE_FLAG::ROLE_FLAG_WATCHER))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}
		if (SrcCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_NORMAL_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}
		if (SrcCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_ENEMY_TO_ROLE))
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}
	}
	else if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_MONSTER))
	{
		AMonsterCharacter* MonsterCharacter = Cast<AMonsterCharacter>(TargetEntity->Actor());
		if (SrcCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_NORMAL_TO_MONSTER) && TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_NORMAL_TO_MONSTER))
		{
			return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}
		else if (SrcCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_ENEMY_TO_MONSTER) && TargetCharacter->HasFlag(ENTITY_FLAG::FLAG_RELATION_ENEMY_TO_MONSTER))
		{
			return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
		}
	}
	int32 targetBelongSide = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), TEXT("belongSide"));
	int32 srcBelongSide = UGolbalBPFunctionLibrary::GetIntPropertyValue(SrcEntity->ID(), TEXT("belongSide"));
	if (targetBelongSide == srcBelongSide)
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
}


COMBAT_RELATION URelRoleEntityRelationLHMJ::GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity)
{
	UGameObjectInterface* TargetInterface = ((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	UGameObjectInterface* SrcEntityInterface = ((GameObject*)SrcEntity)->Interface_Cache.GameObjectInterface;
	if (!IsValid(TargetInterface) || !IsValid((SrcEntityInterface)))
	{
		CS3_Warning(TEXT("-->Null Pointer error:URelEntityRelationGCZ::GetRelation: TargetInterface!"));
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	///幻兽
	if (SrcEntityInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_VEHICLEPET))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(SrcEntity->ID(), "baseOwnerID");
		SrcEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
		if (SrcEntity == nullptr)
		{
			return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}
		SrcEntityInterface = ((GameObject*)SrcEntity)->Interface_Cache.GameObjectInterface;
	}
	///幻兽
	if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_VEHICLEPET))
	{
		int32 ownerID = UGolbalBPFunctionLibrary::GetIntPropertyValue(TargetEntity->ID(), "baseOwnerID");
		TargetEntity = UGolbalBPFunctionLibrary::FindEntity(ownerID);
		if (TargetEntity == nullptr)
		{
			return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
		}
		TargetInterface = ((GameObject*)TargetEntity)->Interface_Cache.GameObjectInterface;
	}
	// 因为只有玩家自己有这个属性
	if (SrcEntity->IsPlayer())
	{
		URoleInterface* RoleInterface_ = Cast<URoleInterface>(SrcEntityInterface);
		if (IsValid(RoleInterface_) && TargetEntity)
		{
			if (TargetInterface->isEntityFlag(ENTITY_TYPE::ENTITY_FLAG_ROLE))
			{
				if (RoleInterface_->ChallengePlayerID() && RoleInterface_->ChallengePlayerID() == TargetEntity->ID())
				{
					return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
				}
			}
		}
	}
	else if(TargetEntity->IsPlayer())
	{
		URoleInterface* RoleInterface_ = Cast<URoleInterface>(TargetInterface);
		if (IsValid(RoleInterface_) && SrcEntityInterface)
		{
			if (RoleInterface_->ChallengePlayerID() && RoleInterface_->ChallengePlayerID() == SrcEntity->ID())
			{
				return COMBAT_RELATION::COMBAT_RELATION_ENEMY;
			}
		}
	}

	return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
}

URelationBase* URelationInsFactory::CreateRelationInsByClass(FString ClassName)
{
	if (ClassName == "RelMonster_Default")
	{
		return NewObject<URelMonster_Default>();
	}
	else if (ClassName == "URelCMonster_Default")
	{
		return NewObject<URelCMonster_Default>();
	}
	else if (ClassName == "RelRole_Camp")
	{
		return NewObject<URelRole_Camp>();
	}
	else if (ClassName == "RelRole_PKMode")
	{
		return NewObject<URelRole_PKMode>();
	}
	else if (ClassName == "RelRole_Peace")
	{
		return NewObject<URelRole_Peace>();
	}
	else if (ClassName == "RelRole_Enemy")
	{
		return NewObject<URelRole_Enemy>();
	}
	else if (ClassName == "RelRole_TongStarcraft")
	{
		return NewObject<URelRole_TongStarcraft>();
	}
	else if(ClassName == "RelTrapObject_Default")
	{
		return NewObject<URelTrapObject_Default>();
	}
	else if(ClassName == "RelNPC_Default")
	{
		return NewObject<URelNPC_Default>();
	}
	else if(ClassName == "RelSpellBox_Default")
	{
		return NewObject<URelSpellBox_Default>();
	}
	else if(ClassName == "RelMovingPlatform_Default")
	{
		return NewObject<URelMovingPlatform_Default>();
	}
	else if (ClassName == "RelVehiclePet_Default")
	{
		return NewObject<URelVehiclePet_Default>();
	}
	else if (ClassName == "RelGhostReceiver_Default")
	{
		return NewObject<URelGhostReceiver_Default>();
	}
	else if (ClassName == "RelRole_TeamStarcraft")
	{
		return NewObject<URelRole_TeamStarcraft>();
	}
	else if (ClassName == "RelEntityRelationGCZ")
	{
		return NewObject<URelEntityRelationGCZ>();
	}
	else if (ClassName == "RelRoleEntityRelationGCZ")
	{
		return NewObject<URelRoleEntityRelationGCZ>();
	}
	else if (ClassName == "RelRoleEntityRelationLHMJ")
	{
		return NewObject<URelRoleEntityRelationLHMJ>();
	}
	return nullptr;
}

CONTROL_COMPILE_OPTIMIZE_END
