// Fill out your copyright notice in the Description page of Project Settings.


#include "VisibleManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/ServerCharacter.h"
#include "Components/WidgetComponent.h"
#include "Actor/DropBox/DropBoxCharacter.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Interface/SpellBox/SpellBoxInterface.h"
#include "Interface/SkillInterface.h"
#include "Interface/StateInterface.h"
#include "Manager/StoryManager.h"
#include "Manager/BuffEntityVisibleManager.h"
#include "Manager/QuestEntityVisibleManager.h"
#include"Chuangshi.h"
#include "TransActorCapture.h"
#include "CS3Base/GameObject.h"
CONTROL_COMPILE_OPTIMIZE_START

DECLARE_CYCLE_STAT(TEXT("UVisibleManager::SetModelVisible"), STAT_SetModelVisible, STATGROUP_VisibleManager);
DECLARE_CYCLE_STAT(TEXT("UVisibleManager::GetModelVisibleStyle"), STAT_GetModelVisibleStyle, STATGROUP_VisibleManager);
DECLARE_CYCLE_STAT(TEXT("UVisibleManager::ChoseVisibleStyleByTypes"), STAT_ChoseVisibleStyleByTypes, STATGROUP_VisibleManager);
DECLARE_CYCLE_STAT(TEXT("UVisibleManager::QueryVisibleByRoleState"), STAT_QueryVisibleByRoleState, STATGROUP_VisibleManager);
DECLARE_CYCLE_STAT(TEXT("UVisibleManager::QueryVisibleByEffectHide"), STAT_QueryVisibleByEffectHide, STATGROUP_VisibleManager);
DECLARE_CYCLE_STAT(TEXT("UVisibleManager::QueryVisibleByVehiclePetState"), STAT_QueryVisibleByVehiclePetState, STATGROUP_VisibleManager);
DECLARE_CYCLE_STAT(TEXT("UVisibleManager::QueryVisibleByFlag"), STAT_QueryVisibleByFlag, STATGROUP_VisibleManager);
DECLARE_CYCLE_STAT(TEXT("UVisibleManager::QueryVisibleByRoleFlag"), STAT_QueryVisibleByRoleFlag, STATGROUP_VisibleManager);
DECLARE_CYCLE_STAT(TEXT("UVisibleManager::QueryVisibleByStory"), STAT_QueryVisibleByStory, STATGROUP_VisibleManager);
DECLARE_CYCLE_STAT(TEXT("UVisibleManager::QueryVisibleByDeadEffect"), STAT_QueryVisibleByDeadEffect, STATGROUP_VisibleManager);
DECLARE_CYCLE_STAT(TEXT("UVisibleManager::QueryVisibleByBoxDie"), STAT_QueryVisibleByBoxDie, STATGROUP_VisibleManager);
DECLARE_CYCLE_STAT(TEXT("UVisibleManager::QueryVisibleByDropBox"), STAT_QueryVisibleByDropBox, STATGROUP_VisibleManager);
DECLARE_CYCLE_STAT(TEXT("UVisibleManager::QueryVisibleByQuest"), STAT_QueryVisibleByQuest, STATGROUP_VisibleManager);
DECLARE_CYCLE_STAT(TEXT("UVisibleManager::QueryVisibleByBUFF"), STAT_QueryVisibleByBUFF, STATGROUP_VisibleManager);
DECLARE_CYCLE_STAT(TEXT("UVisibleManager::QueryVisibleByMonsterState"), STAT_QueryVisibleByMonsterState, STATGROUP_VisibleManager);
DECLARE_CYCLE_STAT(TEXT("UVisibleManager::QueryVisibleByFly"), STAT_QueryVisibleByFly, STATGROUP_VisibleManager);
DECLARE_CYCLE_STAT(TEXT("UVisibleManager::QueryVisibleByBuffTransparency"), STAT_QueryVisibleByBuffTransparency, STATGROUP_VisibleManager);
DECLARE_CYCLE_STAT(TEXT("UVisibleManager::QueryVisibleBySkyDiving"), STAT_QueryVisibleBySkyDiving, STATGROUP_VisibleManager);
DECLARE_CYCLE_STAT(TEXT("UVisibleManager::QueryVisibleByTrapSymbol"), STAT_QueryVisibleByTrapSymbol, STATGROUP_VisibleManager);

UVisibleManager::UVisibleManager()
{

}

UVisibleManager::~UVisibleManager()
{

}
UVisibleManager* UVisibleManager::GetInstance()
{
	cs3_checkNoReentry();

	return NewObject<UVisibleManager>();
}

void  UVisibleManager::UpdateModelVisible(AActor* Actor)
{
	if (!IsValid(Actor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UVisibleManager::UpdateModelVisible : Actor!"));
		return;
	}
	VISIBLE_STYLE VisibleStyle = GetModelVisibleStyle(Actor);
	SetModelVisible(Actor, VisibleStyle);
}

VISIBLE_STYLE UVisibleManager::GetModelVisibleStyle(AActor* Actor)
{
	SCOPE_CYCLE_COUNTER(STAT_GetModelVisibleStyle);
	
	AGameCharacter* Character = Cast<AGameCharacter>(Actor);
	if (!IsValid(Character))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UVisibleManager::GetModelVisibleStyle : Character!"));
		return VISIBLE_STYLE::VISIBLE_STYLE_TRUE;
	}
	TArray<VISIBLE_TYPE> VisibleTypes;
	TArray<VISIBLE_RULE> VisibleRules = Character->VisibleRules;
	for (VISIBLE_RULE VisibleRule : VisibleRules)
	{
		VISIBLE_TYPE VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_TRUE;
		switch (VisibleRule)
		{
		case VISIBLE_RULE::VISIBLE_RULE_BY_ROLE_PENDING:
			VisibleType = QueryVisibleByRoleState(Actor);
			break;
		case VISIBLE_RULE::VISIBLE_RULE_BY_BUFF_HIDE:
			VisibleType = QueryVisibleByEffectHide(Actor);
			break;
		case VISIBLE_RULE::VISIBLE_RULE_BY_VEHICLE_PET_PENDING:
			VisibleType = QueryVisibleByVehiclePetState(Actor);
			break;
		case VISIBLE_RULE::VISIBLE_RULE_BY_FLAG:
			VisibleType = QueryVisibleByFlag(Actor);
			break;
		case VISIBLE_RULE::VISIBLE_RULE_BY_ROLE_FLAG:
			VisibleType = QueryVisibleByRoleFlag(Actor);
			break;
		case VISIBLE_RULE::VISIBLE_RULE_BY_STORY:
			VisibleType = QueryVisibleByStory(Actor);
			break;
		case VISIBLE_RULE::VISIBLE_RULE_BY_DEAD_EFFECT:
			VisibleType = QueryVisibleByDeadEffect(Actor);
			break;
		case VISIBLE_RULE::VISIBLE_RULE_BY_BOX_DIE:
			VisibleType = QueryVisibleByBoxDie(Actor);
			break;
		case VISIBLE_RULE::VISIBLE_RULE_BY_DROP_BOX:
			VisibleType = QueryVisibleByDropBox(Actor);
			break;
		case VISIBLE_RULE::VISIBLE_RULE_BY_QUEST:
			VisibleType = QueryVisibleByQuest(Actor);
			break;
		case VISIBLE_RULE::VISIBLE_RULE_BY_BUFF:
			VisibleType = QueryVisibleByBUFF(Actor);
			break;
		case VISIBLE_RULE::VISIBLE_RULE_BY_MONSTER_PENDING:
			VisibleType = QueryVisibleByMonsterState(Actor);
			break;
		case VISIBLE_RULE::VISIBLE_RULE_BY_FLY:
			VisibleType = QueryVisibleByFly(Actor);
			break;
		case VISIBLE_RULE::VISIBLE_RULE_BY_BUFF_TRANSPARENCY:
			VisibleType = QueryVisibleByBuffTransparency(Actor);
			break;
		case VISIBLE_RULE::VISIBLE_RULE_BY_SKYDIVING:
			VisibleType = QueryVisibleBySkyDiving(Actor);
			break;
		case VISIBLE_RULE::VISIBLE_RULE_BY_TRAP_SYMBOL:
			VisibleType = QueryVisibleByTrapSymbol(Actor);
			break;
		default:
			break;
		}
		VisibleTypes.Add(VisibleType);
	}
	return ChoseVisibleStyleByTypes(VisibleTypes);
}

void UVisibleManager::SetModelVisible(AActor* Actor, VISIBLE_STYLE VisibleStyle)
{
	SCOPE_CYCLE_COUNTER(STAT_SetModelVisible);
	
	AGameCharacter* Character = Cast<AGameCharacter>(Actor);
	if (!IsValid(Character))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UVisibleManager::SetModelVisible : Character!"));
		return;
	}
	if (Character->VisibleStyle == VisibleStyle && VisibleStyle != VISIBLE_STYLE::VISIBLE_STYLE_TRUE)
	{
		return;
	}

	VISIBLE_STYLE LastVisibleStyle = Character->VisibleStyle;
	Character->VisibleStyle = VisibleStyle;	// 保存Actor的显示样式

	if (LastVisibleStyle == VISIBLE_STYLE::VISIBLE_STYLE_TRANSLUCENT_FALSE)
	{
		Character->ReSetOpenScen3DUI();
	}
	// 半透明效果 和 隐身效果相互切换，不在处理
	if (LastVisibleStyle == VISIBLE_STYLE::VISIBLE_STYLE_TRANSLUCENT || LastVisibleStyle == VISIBLE_STYLE::VISIBLE_STYLE_TRANSLUCENT_FALSE && VisibleStyle != VISIBLE_STYLE::VISIBLE_STYLE_TRANSLUCENT_VALUE)
	{
		USkillInterface* EntitySkillInterface = GetActorSkillinterface(Actor);
		if (IsValid(EntitySkillInterface))
		{
			if (LastVisibleStyle == VISIBLE_STYLE::VISIBLE_STYLE_TRANSLUCENT)
			{
				EntitySkillInterface->VisibleShowCharacter(0.5);
			}
			else
			{
				EntitySkillInterface->VisibleShowCharacter(0.0);
			}
		}
	}
	else if (LastVisibleStyle == VISIBLE_STYLE::VISIBLE_STYLE_TRANSLUCENT_VALUE && VisibleStyle != VISIBLE_STYLE::VISIBLE_STYLE_TRANSLUCENT)
	{
		USkillInterface* EntitySkillInterface = GetActorSkillinterface(Actor);
		if (IsValid(EntitySkillInterface))
		{
			EntitySkillInterface->VisibleStopTransparency();
		}
	}

	if (VisibleStyle == VISIBLE_STYLE::VISIBLE_STYLE_FALSE)
	{
		UGolbalBPFunctionLibrary::SetActorAndCompVisibility(Actor, UPrimitiveComponent::StaticClass());
		AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Character);
		if (IsValid(ServerCharacter))
		{
			ServerCharacter->ClearTargetActor();
		}
	}
	else if (VisibleStyle == VISIBLE_STYLE::VISIBLE_STYLE_TRANSLUCENT)
	{
		USkillInterface* EntitySkillInterface = GetActorSkillinterface(Actor);
		if (IsValid(EntitySkillInterface))
		{
			EntitySkillInterface->VisibleHideCharacter(0.5);
		}
		UGolbalBPFunctionLibrary::SetActorAndCompVisibility(Actor, UPrimitiveComponent::StaticClass(), true, true);		// CST-9111
	}
	else if (VisibleStyle == VISIBLE_STYLE::VISIBLE_STYLE_TRANSLUCENT_FALSE)
	{
		USkillInterface* EntitySkillInterface = GetActorSkillinterface(Actor);
		if (IsValid(EntitySkillInterface))
		{
			EntitySkillInterface->VisibleHideCharacter(0.0);
		}
		AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Character);
		if (IsValid(ServerCharacter))
		{
			ServerCharacter->ClearTargetActor();
			ServerCharacter->SetOpenScene3DUI(false);
			if (IsValid(ServerCharacter->HeadInfo3DUI))
			{
				ServerCharacter->HeadInfo3DUI->SetVisibility(false);
			}
		}
	}
	else if (VisibleStyle == VISIBLE_STYLE::VISIBLE_STYLE_TRUE)
	{
		UGolbalBPFunctionLibrary::SetActorAndCompVisibility(Actor, UPrimitiveComponent::StaticClass(), true, true);
	}
	else if (VisibleStyle == VISIBLE_STYLE::VISIBLE_STYLE_TRANSLUCENT_VALUE)
	{
		USkillInterface* EntitySkillInterface = GetActorSkillinterface(Actor);
		if (IsValid(EntitySkillInterface))
		{
			EntitySkillInterface->VisibleShowTransparency();
		}
		UGolbalBPFunctionLibrary::SetActorAndCompVisibility(Actor, UPrimitiveComponent::StaticClass(), true, true);
	}
}

USkillInterface* UVisibleManager::GetActorSkillinterface(AActor* Actor)
{
	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Actor);
	if (IsValid(ServerCharacter))
	{
		KBEngine::Entity* _entity = ServerCharacter->GetSelfEntity();
		if (_entity)
		{
			USkillInterface * EntitySkillInterface = ServerCharacter->GetEntityInterface_Cache().SkillInterface;
			
			return EntitySkillInterface;
		}
	}
	return nullptr;
}

VISIBLE_TYPE UVisibleManager::QueryVisibleByRoleState(AActor* Actor)
{
	SCOPE_CYCLE_COUNTER(STAT_QueryVisibleByRoleState);
	VISIBLE_TYPE VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_TRUE;
	if (IsValid(Actor))
	{
		AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Actor);
		if (IsValid(ServerCharacter))
		{
			KBEngine::Entity* Entity = ServerCharacter->GetSelfEntity();
			if (Entity)
			{
				GameObject* GameEntity = (GameObject *)Entity;
				int32 bInPending = UGolbalBPFunctionLibrary::GetIntPropertyValue(Entity->ID(), TEXT("isInPending")); //这是保护buffID
				if (GameEntity && !GameEntity->IsPlayer() && bInPending > 0)
				{
					VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_PENGIND_FALSE;
				}
			}
		}
	}
	return VisibleType;
}

VISIBLE_TYPE UVisibleManager::QueryVisibleByMonsterState(AActor* Actor)
{
	SCOPE_CYCLE_COUNTER(STAT_QueryVisibleByMonsterState);
	VISIBLE_TYPE VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_TRUE;
	if (IsValid(Actor))
	{
		AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Actor);
		if (IsValid(ServerCharacter))
		{
			KBEngine::Entity* Entity = ServerCharacter->GetSelfEntity();
			if (Entity)
			{
				GameObject* GameEntity = (GameObject *)Entity;
				int32 bInPending = UGolbalBPFunctionLibrary::GetIntPropertyValue(Entity->ID(), TEXT("isInPending")); //这是保护buffID
				if (GameEntity && bInPending > 0)
				{
					VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_PENGIND_FALSE;
				}
			}
		}
	}
	return VisibleType;
}

VISIBLE_TYPE UVisibleManager::QueryVisibleByVehiclePetState(AActor* Actor)
{
	SCOPE_CYCLE_COUNTER(STAT_QueryVisibleByVehiclePetState);
	VISIBLE_TYPE VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_TRUE;
	if (IsValid(Actor))
	{
		AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Actor);
		if (IsValid(ServerCharacter))
		{
			KBEngine::Entity* Entity = ServerCharacter->GetSelfEntity();
			if (Entity)
			{
				GameObject* GameEntity = (GameObject *)Entity;
				int32 bInPending = UGolbalBPFunctionLibrary::GetIntPropertyValue(Entity->ID(), TEXT("isInPending")); //这是保护buffID
				if (GameEntity && bInPending > 0)
				{
					VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_PENGIND_FALSE;
				}
			}
		}
	}
	return VisibleType;
}

VISIBLE_TYPE UVisibleManager::QueryVisibleByFlag(AActor* Actor)
{
	SCOPE_CYCLE_COUNTER(STAT_QueryVisibleByFlag);
	VISIBLE_TYPE VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_TRUE;
	if (IsValid(Actor))
	{
		AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Actor);
		if (IsValid(ServerCharacter))
		{
			if (ServerCharacter->HasFlag(ENTITY_FLAG::FLAG_UNVISIBLE))
			{
				VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_FlAG_FALSE;
			}
		}
	}
	return VisibleType;
}

VISIBLE_TYPE UVisibleManager::QueryVisibleByRoleFlag(AActor* Actor)
{
	SCOPE_CYCLE_COUNTER(STAT_QueryVisibleByRoleFlag);
	VISIBLE_TYPE VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_TRUE;
	if (IsValid(Actor))
	{
		APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(Actor);
		if (IsValid(PlayerCharacter))
		{
			if (PlayerCharacter->HasRoleFlag(ROLE_FLAG::ROLE_FLAG_WATCHER))
			{
				VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_TRANSLUCENT;
			}
		}
	}
	return VisibleType;
}

VISIBLE_TYPE UVisibleManager::QueryVisibleByStory(AActor* Actor)
{
	SCOPE_CYCLE_COUNTER(STAT_QueryVisibleByStory);
	VISIBLE_TYPE VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_TRUE;
	if (IsValid(Actor))
	{
		int32 EntityId = 0;
		AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Actor);
		if (IsValid(ServerCharacter))
		{
			EntityId = ServerCharacter->EntityId;
		}
		if (!UGolbalBPFunctionLibrary::GStoryManager()->IsShowModel(Actor, EntityId))
		{
			VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_STORY_FALSE;
		}
	}
	return VisibleType;
}

VISIBLE_TYPE UVisibleManager::QueryVisibleByFly(AActor* Actor)
{
	SCOPE_CYCLE_COUNTER(STAT_QueryVisibleByFly);
	VISIBLE_TYPE VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_TRUE;
	if (IsValid(Actor))
	{
		APlayerCharacter* character = Cast<APlayerCharacter>(Actor);
		if (IsValid(character)&& !character->ActorIsPlayer())
		{
			APlayerCharacter* player = (APlayerCharacter*)UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();

			///<在幻阵迷宫飞行中队员采用假的模型飞行 需隐藏队员模型
			if (character->HasRoleFlag(ROLE_FLAG::ROLE_FLAG_TEAMMING)&&IsValid(player) && player->IsHZMGFlyState())
			{
				VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_STORY_FALSE;
			}
		}
	}
	return VisibleType;
}

VISIBLE_TYPE UVisibleManager::QueryVisibleBySkyDiving(AActor* Actor)
{
	SCOPE_CYCLE_COUNTER(STAT_QueryVisibleBySkyDiving);
	VISIBLE_TYPE VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_TRUE;
	if (IsValid(Actor))
	{
		APlayerCharacter* character = Cast<APlayerCharacter>(Actor);
		APlayerCharacter* player = (APlayerCharacter*)UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();

		if (IsValid(character) && !character->ActorIsPlayer()&&IsValid(player))
		{			
		}
	}
	return VisibleType;
}

VISIBLE_TYPE UVisibleManager::QueryVisibleByDeadEffect(AActor* Actor)
{
	SCOPE_CYCLE_COUNTER(STAT_QueryVisibleByDeadEffect);
	VISIBLE_TYPE VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_TRUE;
	if (IsValid(Actor))
	{
		AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Actor);
		if (IsValid(ServerCharacter))
		{
			if (ServerCharacter->bIsPlayDeadEffect)
			{
				VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_DEAD_FALSE;
			}
		}
	}
	return VisibleType;
}

VISIBLE_TYPE UVisibleManager::QueryVisibleByBoxDie(AActor* Actor)
{
	SCOPE_CYCLE_COUNTER(STAT_QueryVisibleByBoxDie);
	VISIBLE_TYPE VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_TRUE;
	if (IsValid(Actor))
	{
		AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Actor);
		if (IsValid(ServerCharacter))
		{
			KBEngine::Entity* _entity = ServerCharacter->GetSelfEntity();
			if (!_entity)
			{
				return VisibleType;
			}
			else
			{
				USpellBoxInterface * Interface = Cast<USpellBoxInterface>(ServerCharacter->GetEntityInterface_Cache().GameObjectInterface);
				if (IsValid(Interface) && !(Interface->getEntityFlag() == ENTITY_TYPE::ENTITY_FLAG_SPELL))
				{
					return VisibleType;
				}
				if (IsValid(Interface))
				{
					if (Interface->BoxStatus == 0)
					{
						return VISIBLE_TYPE::VISIBLE_TYPE_BOX_DIE_FALSE;
					}
				}
			}
		}
	}	
	return VisibleType;
}

VISIBLE_TYPE UVisibleManager::QueryVisibleByBUFF(AActor * Actor)
{
	SCOPE_CYCLE_COUNTER(STAT_QueryVisibleByBUFF);
	VISIBLE_TYPE VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_TRUE;
	if (IsValid(Actor))
	{
		AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Actor);
		if (IsValid(ServerCharacter))
		{
			KBEngine::Entity* _entity = ServerCharacter->GetSelfEntity();
			if (_entity && _entity->ClassName() != FString("Role") && _entity->ClassName() != FString("VehiclePet"))
			{
				FString scriptID = UGolbalBPFunctionLibrary::GetEntityPropertyValue(_entity->ID(), TEXT("scriptID"));
				UBuffEntityVisibleManager* buffVisibleManager = UUECS3GameInstance::Instance->BuffEntityVisibleManager;
				return buffVisibleManager->GetVisibleTypeByScriptID(scriptID);
			}
		}
	}
	return VisibleType;
}

VISIBLE_TYPE UVisibleManager::QueryVisibleByDropBox(AActor* Actor)
{
	SCOPE_CYCLE_COUNTER(STAT_QueryVisibleByDropBox);
	VISIBLE_TYPE VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_DROP_BOX_FALSE;
	if (IsValid(Actor))
	{
		ADropBoxCharacter* DropBoxCharacter = Cast<ADropBoxCharacter>(Actor);
		if (IsValid(DropBoxCharacter))
		{
			if (DropBoxCharacter->isVisible(uint64(UGolbalBPFunctionLibrary::GetIntPropertyValue(UGolbalBPFunctionLibrary::GetPlayerID(), TEXT("playerDBID")))))
			{
				VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_TRUE;
			}
		}
	}
	return VisibleType;
}

VISIBLE_TYPE UVisibleManager::QueryVisibleByQuest(AActor * Actor)
{
	SCOPE_CYCLE_COUNTER(STAT_QueryVisibleByQuest);
	VISIBLE_TYPE VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_TRUE;
	if (IsValid(Actor))
	{
		AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Actor);
		if (IsValid(ServerCharacter))
		{
			KBEngine::Entity* _entity = ServerCharacter->GetSelfEntity();
			if (_entity && _entity->ClassName() != FString("Role"))	///不是玩家
			{
				UQuestEntityVisibleManager* Manager = UUECS3GameInstance::Instance->QuestEntityVisibleManager;
				FString EntityScriptId = _entity->GetDefinedProperty(TEXT("scriptID")).GetValue<FString>();
				int32 result = Manager->GetEntityVisible(EntityScriptId);
				if (result == 0)
				{
					return VISIBLE_TYPE::VISIBLE_TYPE_QUEST_FALSE;
				}
				else if (result == 1)
				{
					return VISIBLE_TYPE::VISIBLE_TYPE_QUEST_TRUE;
				}
			}
		}
	}
	return VisibleType;
}

VISIBLE_TYPE UVisibleManager::QueryVisibleByEffectHide(AActor* Actor)
{
	SCOPE_CYCLE_COUNTER(STAT_QueryVisibleByEffectHide);
	VISIBLE_TYPE VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_TRUE;
	if (IsValid(Actor))
	{
		AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Actor);
		if (IsValid(ServerCharacter))
		{
			KBEngine::Entity* _entity = ServerCharacter->GetSelfEntity();
			if (_entity)
			{
				UStateInterface * StateInterface = ServerCharacter->GetEntityInterface_Cache().StateInterface;
				if (IsValid(StateInterface))
				{
					if (StateInterface->HasEffectState(EFFECT_STATE::EFFECT_STATE_HIDE))
					{
						AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
						if (PlayerActor)
						{
							KBEngine::Entity* Entity = PlayerActor->GetSelfEntity();
							if (Entity)
							{
								COMBAT_RELATION relation = PlayerActor->QueryRelation(Actor);
								if (relation == COMBAT_RELATION::COMBAT_RELATION_NORMAL)
								{
									return VISIBLE_TYPE::VISIBLE_TYPE_EFFECT_HIDE_TRANSLUCENT;
								}
								else
								{
									return VISIBLE_TYPE::VISIBLE_TYPE_EFFECT_HIDE_FALSE;
								}
							}
						}
					}
				}
				else
				{
					CS3_Warning(TEXT("Entity=%d  SkillInterface or GameObjectInterface is Null "), _entity->ID());
				}
			}
		}
	}
	return VisibleType;
}

VISIBLE_TYPE UVisibleManager::QueryVisibleByBuffTransparency(AActor* Actor)
{
	SCOPE_CYCLE_COUNTER(STAT_QueryVisibleByBuffTransparency);
	VISIBLE_TYPE VisibleType = VISIBLE_TYPE::VISIBLE_TYPE_TRUE;
	if (IsValid(Actor))
	{
		AServerCharacter* ServerCharacter = Cast<AServerCharacter>(Actor);
		if (IsValid(ServerCharacter))
		{
			KBEngine::Entity* _entity = ServerCharacter->GetSelfEntity();
			if (_entity)
			{
				USkillInterface * EntitySkillInterface = ServerCharacter->GetEntityInterface_Cache().SkillInterface;
				if (IsValid(EntitySkillInterface))
				{
					// 因为服务器同步给客户端的数据时，buff的删除数据，较 脚本执行行为慢
					if (EntitySkillInterface->findBuffsByBuffScript("BuffTransparency").Num() > 0 && EntitySkillInterface->CanTransparency())
					{
						return VISIBLE_TYPE::VISIBLE_TYPE_BUFF_TRANSLUCENT;
					}
				}
				else
				{
					CS3_Warning(TEXT("Entity=%d  SkillInterface or GameObjectInterface is Null "), _entity->ID());
				}
			}
		}
	}
	return VisibleType;
}


VISIBLE_TYPE UVisibleManager::QueryVisibleByTrapSymbol(AActor * Actor)
{
	SCOPE_CYCLE_COUNTER(STAT_QueryVisibleByTrapSymbol);
	AServerCharacter* serCharacter = Cast<AServerCharacter>(Actor);
	if (IsValid(serCharacter))
	{
		auto actorEntity = serCharacter->GetSelfEntity();
		auto playerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
		if (actorEntity && playerEntity)
		{
			if (playerEntity->GetDefinedProperty(TEXT("playerDBID")).GetValue<uint64>() == actorEntity->GetDefinedProperty(TEXT("belongDBID")).GetValue<uint64>())
			{
				return VISIBLE_TYPE::VISIBLE_TYPE_TRAP_SYMBOL_TRUE;
			}
		}
	}
	
	return VISIBLE_TYPE::VISIBLE_TYPE_TRAP_SYMBOL_FALSE;
}

VISIBLE_STYLE UVisibleManager::ChoseVisibleStyleByTypes(TArray<VISIBLE_TYPE> VisibleTypes)
{
	if (VisibleTypes.Num() == 0)
	{
		return VISIBLE_STYLE::VISIBLE_STYLE_TRUE;
	}
	if (VisibleTypes.Contains(VISIBLE_TYPE::VISIBLE_TYPE_PENGIND_FALSE))
	{
		return VISIBLE_STYLE::VISIBLE_STYLE_FALSE;
	}
	else if (VisibleTypes.Contains(VISIBLE_TYPE::VISIBLE_TYPE_BOX_DIE_FALSE)) 
	{
		return VISIBLE_STYLE::VISIBLE_STYLE_FALSE;
	}
	else if (VisibleTypes.Contains(VISIBLE_TYPE::VISIBLE_TYPE_STORY_FALSE))
	{
		return VISIBLE_STYLE::VISIBLE_STYLE_FALSE;
	}
	else if (VisibleTypes.Contains(VISIBLE_TYPE::VISIBLE_TYPE_BUFF_FALSE))
	{
		return VISIBLE_STYLE::VISIBLE_STYLE_FALSE;
	}
	else if (VisibleTypes.Contains(VISIBLE_TYPE::VISIBLE_TYPE_BUFF_TRUE))
	{
		return VISIBLE_STYLE::VISIBLE_STYLE_TRUE;
	}
	else if (VisibleTypes.Contains(VISIBLE_TYPE::VISIBLE_TYPE_EFFECT_HIDE_TRANSLUCENT))
	{
		return VISIBLE_STYLE::VISIBLE_STYLE_TRANSLUCENT;
	}
	else if (VisibleTypes.Contains(VISIBLE_TYPE::VISIBLE_TYPE_EFFECT_HIDE_FALSE))
	{
		return VISIBLE_STYLE::VISIBLE_STYLE_TRANSLUCENT_FALSE;
	}
	else if (VisibleTypes.Contains(VISIBLE_TYPE::VISIBLE_TYPE_QUEST_FALSE))
	{
		return VISIBLE_STYLE::VISIBLE_STYLE_FALSE;
	}
	else if (VisibleTypes.Contains(VISIBLE_TYPE::VISIBLE_TYPE_DEAD_FALSE))
	{
		return VISIBLE_STYLE::VISIBLE_STYLE_FALSE;
	}
	else if (VisibleTypes.Contains(VISIBLE_TYPE::VISIBLE_TYPE_QUEST_TRUE))
	{
		return VISIBLE_STYLE::VISIBLE_STYLE_TRUE;
	}
	else if (VisibleTypes.Contains(VISIBLE_TYPE::VISIBLE_TYPE_FlAG_FALSE))
	{
		return VISIBLE_STYLE::VISIBLE_STYLE_FALSE;
	}
	else if (VisibleTypes.Contains(VISIBLE_TYPE::VISIBLE_TYPE_TRANSLUCENT))
	{
		return VISIBLE_STYLE::VISIBLE_STYLE_TRANSLUCENT;
	}
	else if (VisibleTypes.Contains(VISIBLE_TYPE::VISIBLE_TYPE_DROP_BOX_FALSE))
	{
		return VISIBLE_STYLE::VISIBLE_STYLE_FALSE;
	}
	else if (VisibleTypes.Contains(VISIBLE_TYPE::VISIBLE_TYPE_BUFF_TRANSLUCENT))
	{
		return VISIBLE_STYLE::VISIBLE_STYLE_TRANSLUCENT_VALUE;
	}
	else if(VisibleTypes.Contains(VISIBLE_TYPE::VISIBLE_TYPE_SKYDIVING_FALSE))
	{
		return VISIBLE_STYLE::VISIBLE_STYLE_FALSE;
	}
	else if (VisibleTypes.Contains(VISIBLE_TYPE::VISIBLE_TYPE_TRAP_SYMBOL_FALSE))
	{
		return VISIBLE_STYLE::VISIBLE_STYLE_FALSE;
	}
	else if (VisibleTypes.Contains(VISIBLE_TYPE::VISIBLE_TYPE_TRAP_SYMBOL_TRUE))
	{
		return VISIBLE_STYLE::VISIBLE_STYLE_TRUE;
	}
	
	return VISIBLE_STYLE::VISIBLE_STYLE_TRUE;
}
CONTROL_COMPILE_OPTIMIZE_END
