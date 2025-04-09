/**
* 功能说明：战场中根据不同关系显示不同颜色 CST-10559
* 文件作者：yanjingxin
* 目前维护：yanjingxin
* 创建时间：2020/4/26
*/

#pragma once
#include "AppearanceStyle.h"
#include "CoreMinimal.h"
#include "GameData/CsvTableRowBase.h"
#include "BattlefieldAppearanceStyle.generated.h"

class AMonsterCharacter;

/**
 * \brief
 * CSV_CONFIG_MODIFY_BATTLEFIELD_APPEARANCE表的数据结构
 * 表的RowName是对应的是DT_ModelCfg
 * 战场小兵在不同关系下会显示不同的颜色外貌
 * 自己控制的小兵|友军|敌军
 */
USTRUCT(BlueprintType)
struct FBattlefieldAppearanceStyle : public FCSV_TABLE_ROW_BASE
{
    GENERATED_BODY()

    /**
     * \brief 玩家自己控制的士兵外貌样式
     */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="AppearanceStyle")
    FAppearanceStyle Subordinates;
    
    /**
     * \brief 友军士兵外貌样式
     */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="AppearanceStyle")
    FAppearanceStyle FriendlyForces;

    /**
     * \brief 敌军士兵外貌样式
     */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category="AppearanceStyle")
    FAppearanceStyle Enemy;
};

class BattlefieldStyleUtilities
{
 public:
    /**
    * \brief 查找Soldier当前外貌样式
    * \param Soldier 小兵Actor( CMonster|MonsterSoldier )
    * \return Soldier在与当前本地玩家得关系下所需要的外貌样式
    */
    static const FAppearanceStyle* FindStyle(AMonsterCharacter* Soldier);    
    /**
    * \brief 对战场小兵基于当前与本地玩家的关系应用AppearanceStyle外貌样式
    * \param Soldier 目标小兵
    */
    static void ApplyAppearanceStyle(AMonsterCharacter* Soldier);
};