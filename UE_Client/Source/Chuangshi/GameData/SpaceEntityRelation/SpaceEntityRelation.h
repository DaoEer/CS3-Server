#pragma once

#include "KBEngine.h"
#include "../CS3Object.h"
#include "GameData/GameDeFine.h"
#include "SpaceEntityRelation.generated.h"


/**
* 文件名称：SpaceEntityRelation.h
* 功能说明：
* 文件作者：chenweilan
* 目前维护：hejingke
* 创建时间：2017-06-29
*/

///基类
UCLASS(BlueprintType)
class CHUANGSHI_API URelationBase : public UCS3Object
{
	GENERATED_BODY()

public:	
	URelationBase();
	virtual COMBAT_RELATION GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity);
};

///通用Monster关系判断实例
UCLASS(BlueprintType)
class CHUANGSHI_API URelMonster_Default : public URelationBase
{
	GENERATED_BODY()

public:
	COMBAT_RELATION GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity) override;
};


///通用CMonster关系判断实例
UCLASS(BlueprintType)
class CHUANGSHI_API URelCMonster_Default : public URelationBase
{
	GENERATED_BODY()

public:
	COMBAT_RELATION GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity) override;
};

///玩家关系判断实例：阵营决定pvp关系
UCLASS(BlueprintType)
class CHUANGSHI_API URelRole_Camp : public URelationBase
{
	GENERATED_BODY()

public:
	COMBAT_RELATION GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity) override;
};

///玩家关系判断实例：pk模式决定pvp关系
UCLASS(BlueprintType)
class CHUANGSHI_API URelRole_PKMode : public URelationBase
{
	GENERATED_BODY()

public:
	COMBAT_RELATION GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity) override;
};

///玩家关系判断实例：与其他玩家完全友好
UCLASS(BlueprintType)
class CHUANGSHI_API URelRole_Peace : public URelationBase
{
	GENERATED_BODY()

public:
	COMBAT_RELATION GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity) override;
};

///玩家关系判断实例：与其他玩家完全敌对
UCLASS(BlueprintType)
class CHUANGSHI_API URelRole_Enemy : public URelationBase
{
	GENERATED_BODY()

public:
	COMBAT_RELATION GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity) override;
};

///玩家关系判断实例：用于帮会之间战斗 不同帮会之间敌对
UCLASS(BlueprintType)
class CHUANGSHI_API URelRole_TongStarcraft : public URelationBase
{
	GENERATED_BODY()

public:
	COMBAT_RELATION GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity) override;
};

///通用TrapObject关系判断实例
UCLASS(BlueprintType)
class CHUANGSHI_API URelTrapObject_Default : public URelationBase
{
	GENERATED_BODY()

public:
	COMBAT_RELATION GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity) override;
};

///通用NPC关系判断实例
UCLASS(BlueprintType)
class CHUANGSHI_API URelNPC_Default : public URelationBase
{
	GENERATED_BODY()

public:
	COMBAT_RELATION GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity) override;
};

///通用SpellBox关系判断实例
UCLASS(BlueprintType)
class CHUANGSHI_API URelSpellBox_Default : public URelationBase
{
	GENERATED_BODY()

public:
	COMBAT_RELATION GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity) override;
};

///通用MovingPlatform关系判断实例
UCLASS(BlueprintType)
class CHUANGSHI_API URelMovingPlatform_Default : public URelationBase
{
	GENERATED_BODY()

public:
	COMBAT_RELATION GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity) override;
};

///宠物关系判断实例
UCLASS(BlueprintType)
class CHUANGSHI_API URelVehiclePet_Default : public URelationBase
{
	GENERATED_BODY()

public:
	COMBAT_RELATION GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity) override;
};
///傀儡关系判断实列
UCLASS(BlueprintType)
class CHUANGSHI_API URelGhostReceiver_Default : public URelationBase
{
	GENERATED_BODY()

public:
	COMBAT_RELATION GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity) override;
};

///玩家关系判断实例：用于队伍之间战斗 不同队伍之间敌对
UCLASS(BlueprintType)
class CHUANGSHI_API URelRole_TeamStarcraft : public URelationBase
{
	GENERATED_BODY()

public:
	COMBAT_RELATION GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity) override;
};

///攻城战玩家关系实例判断
UCLASS(BlueprintType)
class CHUANGSHI_API URelRoleEntityRelationGCZ : public URelationBase
{
	GENERATED_BODY()

public:
	COMBAT_RELATION GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity) override;
};

///攻城战Entity关系实例判断
UCLASS(BlueprintType)
class CHUANGSHI_API URelEntityRelationGCZ : public URelationBase
{
	GENERATED_BODY()

public:
	COMBAT_RELATION GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity) override;
};

///轮回秘境大地图玩家关系实例判断
UCLASS(BlueprintType)
class CHUANGSHI_API URelRoleEntityRelationLHMJ : public URelationBase
{
	GENERATED_BODY()

public:
	COMBAT_RELATION GetRelation(KBEngine::Entity* SrcEntity, KBEngine::Entity* TargetEntity) override;
};

///实例工厂类
UCLASS(BlueprintType)
class CHUANGSHI_API URelationInsFactory : public UCS3Object
{
	GENERATED_BODY()

public:
	static URelationBase* CreateRelationInsByClass(FString ClassName);
};

