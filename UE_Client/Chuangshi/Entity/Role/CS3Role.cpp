
#include "CS3Role.h"
#include "KBEngine.h"
#include "CoreMinimal.h"
#include "Entity/Alias.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "Interface/Role/RoleBuyNPCShopInterface.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Components/WidgetComponent.h"
#include "GameData/GameDefault.h"
#include "Interface/Role/RoleInterface.h"
#include "Interface/Role/RoleActivityInterface.h"
#include "GameDevelop/CS3GameInstance.h"
#include "CS3Base/CS3Entity.h"
#include "Interface/Role/RolePerformanceInterface.h"
#include "Interface/Role/RoleTeamInterface.h"
#include "Interface/Role/RoleEquipInterface.h"
#include "Interface/Role/RoleStoreInterface.h"
#include "Interface/Role/RoleModelInterface.h"
#include "Manager/GameStatus.h"
#include "Manager/LoginManager.h"
#include "CS3Base/UIManager.h"
#include "Manager/LevelManager.h"
#include "Manager/LocalDataSaveManager.h"
#include "GameData/ConstDataBP.h"
#include "Manager/VisibleManager.h"
#include "Manager/SpaceEntityRelationMgr.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Manager/TimeManager.h"
#include "Util/GlobalFunctions.h"

#include "Interface/Role/RoleDropBoxInterface.h"
#include "Interface/Role/RoleInterface.h"
#include "Interface/Role/RoleCampInterface.h"
#include "Interface/Role/RoleCompeteInterface.h"
#include "Interface/Role/RoleStoryInterface.h"
#include "Interface/Role/RoleSpaceContentInterface.h"
#include "Interface/Role/RoleSpellBoxDropItemInterface.h"
#include "Interface/Role/RoleCommanderInterface.h"
#include "Interface/Monster/CSkillInterface.h"
#include "Interface/Role/RoleLunHuiMiJinInterface.h"
#include "Interface/Role/RoleTitleInterface.h"
#include "Interface/Role/RoleBarracksInterface.h"
#include "Interface/Role/RoleSpaceStrategyInterface.h"
#include "Interface/Role/RolePetInterface.h"
#include "Interface/Role/RoleLingShiTradeInterface.h"
#include "Interface/Role/RoleShopMallInterface.h"
#include "Interface/Role/RoleMemoirInterface.h"
#include "Interface/Role/RoleStallInterface.h"
#include "Interface/Role/RoleSpaceInterface.h"
#include "Interface/Role/RoleTradeInterface.h"
#include "Interface/Role/RoleRankInterface.h"
#include "Interface/Role/RolePerformanceInterface.h"
#include "Interface/Role/QuickBarInterface.h"
#include "Interface/Role/RoleCrondInterface.h"
#include "Interface/Role/RoleEquipInterface.h"
#include "Interface/Role/RoleBuyNPCShopInterface.h"
#include "Interface/StatusMessageInterface.h"
#include "Interface/Role/RoleModelInterface.h"
#include "Interface/Role/RoleTongInterface.h"
#include "Interface/Role/RoleSpaceStageInterface.h"
#include "Interface/Role/RoleReviveInterface.h"
#include "Interface/Role/RoleCombatInterface.h"
#include "Interface/Role/RoleTeamInterface.h"
#include "Interface/EntitySpaceEventInterface.h"
#include "Interface/Role/RoleMilitaryRankInterface.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "Interface/Role/RoleAutoFightInterface.h"
#include "Interface/Role/RoleTutorialInterface.h"
#include "Interface/Role/RoleStateInterface.h"
#include "Interface/Role/RoleQuestInterface.h"
#include "Interface/SkillInterface.h"
#include "Interface/Role/RoleTalkInterface.h"
#include "Interface/Role/RoleChatInterface.h"
#include "Interface/Role/RoleMailInterface.h"
#include "Interface/Role/RoleActivityInterface.h"
#include "Interface/Role/RoleShenTongInterface.h"
#include "Interface/Role/RoleQTEInterface.h"
#include "Interface/Role/RoleGiftInterface.h"
#include "Interface/Role/RoleStoreInterface.h"
#include "Interface/Role/RoleRelationInterface.h"
#include "Interface/Role/RoleWorkShopInterface.h"
#include "Interface/Role/RoleTeleportInterface.h"
#include "Interface/Role/RoleTrainSoldierGroundInterface.h"
#include "Interface/Role/RoleCrossServiceInterface.h"
#include "Interface/Role/RoleLbcTaskInterface.h"
#include "Interface/Role/RoleGameTimeInterface.h"
#include "Interface/Role/RoleChuanChengInterface.h"
#include "Interface/Role/RoleLbcInterface.h"

DECLARE_CYCLE_STAT(TEXT("CS3_RoleEntity_CreateCharacter"), STAT_CS3_RoleEntity_CreateCharacter, STATGROUP_CS3_RoleEntity);



KBE_BEGIN_ENTITY_METHOD_MAP(CS3Role, Supper)
DECLARE_REMOTE_METHOD(OnNetworkTest, &CS3Role::OnNetworkTest)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(CS3Role, Supper)
DECLARE_PROPERTY_CHANGED_NOTIFY(camp, &CS3Role::Set_Camp, int32)
DECLARE_PROPERTY_CHANGED_NOTIFY(gender, &CS3Role::Set_Gender, int32)
DECLARE_PROPERTY_CHANGED_NOTIFY(money, &CS3Role::Set_Money, int64)
DECLARE_PROPERTY_CHANGED_NOTIFY(potential, &CS3Role::Set_Potential, int32)
DECLARE_PROPERTY_CHANGED_NOTIFY(playerName, &CS3Role::Set_PlayerName, FString)
DECLARE_PROPERTY_CHANGED_NOTIFY(profession, &CS3Role::Set_Profession, int32)
DECLARE_PROPERTY_CHANGED_NOTIFY(state, &CS3Role::Set_State, int32)
DECLARE_PROPERTY_CHANGED_NOTIFY(level, &CS3Role::Set_Level, int16)
DECLARE_PROPERTY_CHANGED_NOTIFY(playerDBID,&CS3Role::Set_PlayerDBID, uint64)
KBE_END_ENTITY_PROPERTY_MAP()

DEF_INTERFACE_BEGIN(CS3Role, Supper)
DEF_INTERFACE(URoleInterface)
DEF_INTERFACE(URoleDropBoxInterface)
DEF_INTERFACE(URoleCampInterface)
DEF_INTERFACE(URoleCompeteInterface)
DEF_INTERFACE(URoleStoryInterface)
DEF_INTERFACE(URoleSpaceContentInterface)
DEF_INTERFACE(URoleSpellBoxDropItemInterface)
DEF_INTERFACE(URoleCommanderInterface)
DEF_INTERFACE(UCSkillInterface)
DEF_INTERFACE(URoleLunHuiMiJinInterface)
DEF_INTERFACE(URoleTitleInterface)
DEF_INTERFACE(URoleBarracksInterface)
DEF_INTERFACE(URoleSpaceStrategyInterface)
DEF_INTERFACE(URolePetInterface)
DEF_INTERFACE(URoleLingShiTradeInterface)
DEF_INTERFACE(URoleShopMallInterface)
DEF_INTERFACE(URoleMemoirInterface)
DEF_INTERFACE(URoleStallInterface)
DEF_INTERFACE(URoleSpaceInterface)
DEF_INTERFACE(URoleTradeInterface)
DEF_INTERFACE(URoleRankInterface)
DEF_INTERFACE(URolePerformanceInterface)
DEF_INTERFACE(UQuickBarInterface)
DEF_INTERFACE(URoleCrondInterface)
DEF_INTERFACE(URoleEquipInterface)
DEF_INTERFACE(URoleBuyNPCShopInterface)
DEF_INTERFACE(UStatusMessageInterface)
DEF_INTERFACE(URoleModelInterface)
DEF_INTERFACE(URoleTongInterface)
DEF_INTERFACE(URoleSpaceStageInterface)
DEF_INTERFACE(URoleReviveInterface)
DEF_INTERFACE(URoleCombatInterface)
DEF_INTERFACE(URoleTeamInterface)
DEF_INTERFACE(UEntitySpaceEventInterface)
DEF_INTERFACE(URoleMilitaryRankInterface)
DEF_INTERFACE(URoleKitBagInterface)
DEF_INTERFACE(URoleAutoFightInterface)
DEF_INTERFACE(URoleTutorialInterface)
DEF_INTERFACE(URoleStateInterface)
DEF_INTERFACE(URoleQuestInterface)
DEF_INTERFACE(USkillInterface)
DEF_INTERFACE(URoleTalkInterface)
DEF_INTERFACE(URoleChatInterface)
DEF_INTERFACE(URoleMailInterface)
DEF_INTERFACE(URoleActivityInterface)
DEF_INTERFACE(URoleShenTongInterface)
DEF_INTERFACE(URoleQTEInterface)
DEF_INTERFACE(URoleGiftInterface)
DEF_INTERFACE(URoleStoreInterface)
DEF_INTERFACE(URoleRelationInterface)
DEF_INTERFACE(URoleWorkShopInterface)
DEF_INTERFACE(URoleTeleportInterface)
DEF_INTERFACE(URoleTrainSoldierGroundInterface)
DEF_INTERFACE(URoleCrossServiceInterface)
DEF_INTERFACE(URoleLbcTaskInterface)
DEF_INTERFACE(URoleGameTimeInterface)
DEF_INTERFACE(URoleChuanChengInterface)
DEF_INTERFACE(URoleLbcInterface)
DEF_INTERFACE_END()


CS3Role::CS3Role()
{
	_fActorName = FString("Role");
	isOnGround_ = false;
}

CS3Role::~CS3Role()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Role::~Role!"));

}

void CS3Role::OnSet_flags(const int64 &newValue, const int64 &oldValue)
{
	AServerCharacter* Character = Cast<AServerCharacter>(Actor());
	if (IsValid(Character))
	{
		Character->OnFlagsChanged();
		URoleInterface * Interface = Cast<URoleInterface>(Interface_Cache.GameObjectInterface);
		if (IsValid(Interface))
		{
			//观察者标志位
			if (Interface->IsInFlags(ROLE_FLAG::ROLE_FLAG_WATCHER, newValue) && !Interface->IsInFlags(ROLE_FLAG::ROLE_FLAG_WATCHER, oldValue))
			{
				UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(Actor());
			}
			if (!Interface->IsInFlags(ROLE_FLAG::ROLE_FLAG_WATCHER, newValue) && Interface->IsInFlags(ROLE_FLAG::ROLE_FLAG_WATCHER, oldValue))
			{
				UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(Actor());
			}
		}
	}
}

void CS3Role::InitProperties(KBEngine::ScriptModule & scriptModule)
{
	Supper::InitProperties(scriptModule);
}

void CS3Role::OnDestroy()
{
	Supper::OnDestroy();
}

void CS3Role::OnEnterWorld()
{
	Supper::OnEnterWorld();
}

void CS3Role::OnLeaveWorld()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("Role::OnLeaveWorld!"));
	if (IsValid(UUECS3GameInstance::Instance->LevelManager))
	{
		UUECS3GameInstance::Instance->LevelManager->RequestLeaveScenes(this);
	}
	if (IsValid(UUECS3GameInstance::Instance->TimeManager))
	{
		UUECS3GameInstance::Instance->TimeManager->OnPlayerLeave();
	}
	Supper::OnLeaveWorld();
}

void CS3Role::DoCreateCharacter()
{
	SCOPE_CYCLE_COUNTER(STAT_CS3_RoleEntity_CreateCharacter);
	UClass* BP_Character = UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_Character"));
	//const FVector &Location = Position();
	//const FRotator &Ratation = FRotator(FQuat::MakeFromEuler(Direction()));
	//APlayerCharacter* RoleCharacter = UGolbalBPFunctionLibrary::SpawnActor<APlayerCharacter>(BP_Character, Location, Ratation);
	FTransform SpawnTransform = FTransform();
	SpawnTransform.SetLocation(Position());
	SpawnTransform.SetRotation(FQuat::MakeFromEuler(Direction()));
	APlayerCharacter* RoleCharacter = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::BeginDeferredActorSpawnFromClass(BP_Character, SpawnTransform));
	UGolbalBPFunctionLibrary::SetActorAndCompVisibility(RoleCharacter, UPrimitiveComponent::StaticClass());

	BindActorToEntity(RoleCharacter);

	CS3_Display(CS3DebugType::CL_Undefined, TEXT("RoleCharacter[%d], Position(%f, %f, %f)"), this->ID(), RoleCharacter->GetActorLocation().X, RoleCharacter->GetActorLocation().Y, RoleCharacter->GetActorLocation().Z);
	CS3_Log(TEXT("Create RoleCharacter[%d], PlayerID[%d]"), this->ID(), UGolbalBPFunctionLibrary::GetPlayerID());	
}

void CS3Role::OnEnterScenes()
{
	Supper::OnEnterScenes();
	CreateCharacter();
}

void CS3Role::LoadSpaceCompleted()
{
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("---------------------------LoadSpaceCompleted--------------bFirst:%d"), bFirst);
	bool bFirst = bFirstEnterSpace;
	if (bFirstEnterSpace)
	{
		bFirstEnterSpace = false;
	}
	//获取行为interface
	URolePerformanceInterface* Performance = Cast<URolePerformanceInterface>
		(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RolePerformanceInterface")));
	if (IsValid(Performance))
	{
		Performance->OnLoadSpaceCompleted(bFirst);
	}
	KBEngine::FVariantArray args;
	args.Add((int8)bFirst);
	CellCall(TEXT("loadSpaceCompleted"), args);
	UTimeManager *TimeManager = UUECS3GameInstance::Instance->TimeManager;
	TimeManager->OnPlayerEnter();
}

void CS3Role::RequestPetTeleporToOwner()
{
	//幻兽AI目前是在客户端实现，玩家在切换地图时，如果有幻兽就将幻兽传到玩家身边
	if (UGolbalBPFunctionLibrary::GetIntPropertyValue(ID(), TEXT("activePetID")) != 0 && !bFirstEnterSpace)
	{
		KBEngine::FVariantArray args;
		CellCall(TEXT("CELL_requestTeleporToOwner"), args);
	}
}

void CS3Role::OnBindActorToEntity()
{
	Supper::OnBindActorToEntity();
}

URelationBase* CS3Role::GetEntityRelationIns()
{
	URoleInterface* Interface = Cast<URoleInterface>(Interface_Cache.GameObjectInterface);
	if (!IsValid(Interface))
	{
		CS3_Warning(TEXT("-->Null Pointer error:Role::GetEntityRelationIns : Interface!"));
		return nullptr;
	}

	int32 Rule = Interface->GetRelationRule();
	for (auto i : UUECS3GameInstance::Instance->ConstDataBP->ROLE_RELATION_RULE_TO_REL_CLS)
	{
		if (int(i.Key) == Rule)
		{
			return UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetRelationInsByCls(i.Value);
		}
	}
	return nullptr;
}

void CS3Role::Logoff()
{
	KBEngine::FVariantArray args;
	BaseCall(TEXT("logoff"), args);
}

void CS3Role::Logout()
{
	KBEngine::FVariantArray args;
	BaseCall(TEXT("logout"), args);
}

bool CS3Role::IsState(ENTITY_STATE EntityState)
{
	int32 State = GetDefinedProperty(TEXT("state")).GetValue<int32>();
	return State == int32(EntityState);
}

int32 CS3Role::GetTargetEntityID()
{ 
	return TargetEntityID;
}

void CS3Role::SetTargetEntityID(int32 InTargetEntityID)
{
	TargetEntityID = InTargetEntityID;
}

UClass* CS3Role::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_Character")); 
}


void CS3Role::networkTest()
{
	networkTestRecord = FDateTime::Now().GetTicks();
	KBEngine::FVariantArray args;
	BaseCall( TEXT("networkTest"), args );
}

void CS3Role::OnNetworkTest()
{
	int64 delayTime = (int)(FDateTime::Now().GetTicks() - networkTestRecord) / 2 / 100000;
	APlayerCharacter* PlayerActor = Cast<APlayerCharacter>(Actor());
	if (IsValid(PlayerActor))
	{
		PlayerActor->OnSetNetworkTime(delayTime);
	}
}

void CS3Role::Set_Level(const int16& newVal, const int16& oldVal)
{
	_level = newVal;
	if (IsPlayer())
	{
		URoleKitBagInterface* kitbatPtr = CS3::GetInterface< URoleKitBagInterface>(this);
		kitbatPtr->OnPlayerLevelChange(_level);
		URoleChatInterface* chatPtr = CS3::GetInterface< URoleChatInterface >(this);
		chatPtr->OnChatShortcutSwitchConditionsChange();
		USkillInterface* skillPtr = CS3::GetInterface< USkillInterface>(this);
		skillPtr->OnPlayerLevelChange();
	}
}