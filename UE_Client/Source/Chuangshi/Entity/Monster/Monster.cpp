
#include "Monster.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "KBEngine.h"
#include "Util/CS3Debug.h"
#include "Actor/Monster/MonsterCharacter.h"

#include "Interface/Monster/MonsterInterface.h"
#include "Interface/StateInterface.h"
#include "Interface/Monster/BehaviourInterface.h"
#include "Interface/Monster/CSkillInterface.h"
#include "Interface/SkillInterface.h"
#include "Interface/Monster/MonsterCombatInterface.h"
#include "Interface/EntitySpaceEventInterface.h"
#include "Interface/Monster/MonsterAppearInterface.h"
#include "Interface/Monster/MonsterOwnerInterface.h"
#include "Interface/ModelInterface.h"

DEF_INTERFACE_BEGIN(Monster, Supper)
DEF_INTERFACE(UMonsterInterface)
DEF_INTERFACE(UStateInterface)
DEF_INTERFACE(UMonsterCombatInterface)
DEF_INTERFACE(UBehaviourInterface)
DEF_INTERFACE(USkillInterface)
DEF_INTERFACE(UCSkillInterface)
DEF_INTERFACE(UEntitySpaceEventInterface)
DEF_INTERFACE(UMonsterAppearInterface)
DEF_INTERFACE(UMonsterOwnerInterface)
DEF_INTERFACE(UModelInterface)
DEF_INTERFACE_END()


CONTROL_COMPILE_OPTIMIZE_START
KBE_BEGIN_ENTITY_METHOD_MAP(Monster, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(Monster, Supper)
DECLARE_PROPERTY_CHANGED_NOTIFY(useRVOAvoidance, &Monster::Set_useRVOAvoidance, uint8)
KBE_END_ENTITY_PROPERTY_MAP()

Monster::Monster()
{
	_fActorName = FString( "Monster" );
	//_fCompontentName = FName("UMonsterActorComponent");
}

Monster::~Monster()
{
}

void Monster::InitInterfaceCache()
{
	Supper::InitInterfaceCache();
	BehaviourInterface = Cast< UBehaviourInterface >( *( m_interfaceContainer.Find("BehaviourInterface")) );
	CombatInterface = Cast< UMonsterCombatInterface >( *( m_interfaceContainer.Find("CombatInterface")) );
}

void Monster::DestroyInterfaces()
{
	BehaviourInterface = nullptr;
	CombatInterface = nullptr;
	Supper::DestroyInterfaces();
}

bool Monster::IsState(ENTITY_STATE EntityState)
{
	int32 State = GetDefinedProperty(TEXT("state")).GetValue<int32>();
	return State == int32(EntityState);
}

UClass* Monster::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_Monster")); 
}

void Monster::OnMoveOver(const uint32 movingID, const bool isSuccess)
{
	
}

void Monster::RPC_CELL_ChangeMonsterParent(KBEngine::FVariantArray Args)
{
	CellCall(TEXT("CELL_ChangeMonsterParent"), Args);
}



void Monster::Set_useRVOAvoidance(const uint8& newVal, const uint8& oldVal)
{
	AMonsterCharacter* Character = Cast<AMonsterCharacter>(Actor());
	if (IsValid(Character))
	{
		if (newVal && AvoidanceConsiderationRadius > 0)
		{
			Character->GetCharacterMovement()->AvoidanceConsiderationRadius = AvoidanceConsiderationRadius;
		}
		
		Character->GetCharacterMovement()->bUseRVOAvoidance = bool(newVal);
	}
}

CONTROL_COMPILE_OPTIMIZE_END
