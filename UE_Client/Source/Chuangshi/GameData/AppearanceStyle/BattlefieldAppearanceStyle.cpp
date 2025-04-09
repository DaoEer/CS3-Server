#include "GameData/AppearanceStyle/BattlefieldAppearanceStyle.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "Component/AppearanceComponent.h"
#include "Entity/Monster/CMonster.h"
#include "GameData/EnumCsvDefine.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Interface/Role/RoleCommanderInterface.h"
#include "Manager/CfgManager.h"
#include "Util/GolbalBPFunctionLibrary.h"

DECLARE_CYCLE_STAT(TEXT("BattlefieldStyleUtilities::FindStyleResources"), STAT_BattlefieldFindStyleResources, STATGROUP_AppearanceStyle);
DECLARE_CYCLE_STAT(TEXT("BattlefieldStyleUtilities::FindStyle"), STAT_BattlefieldFindStyle, STATGROUP_AppearanceStyle);
DECLARE_CYCLE_STAT(TEXT("BattlefieldStyleUtilities::ApplyAppearanceStyle"), STAT_BattlefieldApplyAppearanceStyle, STATGROUP_AppearanceStyle);

const FAppearanceStyle* BattlefieldStyleUtilities::FindStyle(AMonsterCharacter* Soldier)
{
    SCOPE_CYCLE_COUNTER(STAT_BattlefieldFindStyle);
    if(UUECS3GameInstance::Instance == nullptr && !IsValid(Soldier)) return nullptr;

    const ENTITY_TYPE_EXT EntityType = Soldier->EntityTypeExt;
    if (EntityType != ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT &&
        EntityType != ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_COMMANDER &&
        EntityType != ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_MONSTER_SOLDIER) return nullptr;
    
    if(UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager)
    {
        UAppearanceComponent* AppearanceComponent = Soldier->GetAppearanceComponent();
        if(AppearanceComponent == nullptr) return nullptr;
    
        const FString& ModelCfgRowName = AppearanceComponent->GetModelId();
        const UConfigTable* Table = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_MODIFY_BATTLEFIELD_APPEARANCE);
        const FBattlefieldAppearanceStyle* AppearanceStyle = Table->GetRow<FBattlefieldAppearanceStyle>(ModelCfgRowName);

        if(AppearanceStyle)
        {
            AServerCharacter* PlayerCharacter = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
            if(IsValid(PlayerCharacter))
            {
                COMBAT_RELATION RELATION = PlayerCharacter->QueryRelation(Soldier);
                if (RELATION == COMBAT_RELATION::COMBAT_RELATION_ENEMY)
                {
                    return &AppearanceStyle->Enemy;
                }
                else if(RELATION == COMBAT_RELATION::COMBAT_RELATION_NORMAL)
                {
                    if(EntityType == ENTITY_TYPE_EXT::ENTITY_FLAG_MONSTER_CTRL_BY_CLIENT)
                    {
                        URoleCommanderInterface* Interface = Cast<URoleCommanderInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleCommanderInterface")));
                        if(Interface)
                        {
                            const int32 SoldierId = Soldier->EntityId;
                            const FARMS_DATA& ArmsData = Interface->ArmsData;
                            if(ArmsData.SoldierEntityIDList.Contains(SoldierId) || ArmsData.LeftGuardEntityID == SoldierId || ArmsData.RightGuardEntityID == SoldierId)
                            {
                                return &AppearanceStyle->Subordinates;
                            }
                            return &AppearanceStyle->FriendlyForces;
                        }
                        return nullptr;
                    }
                    return nullptr;
                }
            }
        }
    }

    return nullptr;
}

void BattlefieldStyleUtilities::ApplyAppearanceStyle(AMonsterCharacter* Soldier)
{
    SCOPE_CYCLE_COUNTER(STAT_BattlefieldApplyAppearanceStyle);
    if(const FAppearanceStyle* AppearanceStyle = FindStyle(Soldier))
    {
        AppearanceStyleUtilities::ApplyAppearanceStyle(*Soldier, *AppearanceStyle);
    }
}
