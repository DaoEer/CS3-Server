#pragma once

#include "GameData/Item/ItemUse.h"
#include "ItemShenTongSkill.generated.h"

/**
* 文件名称：ItemShenTongSkill.h
* 功能说明：
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2019-05-05
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UItemShenTongSkill : public UItemUse
{
	GENERATED_BODY()
		typedef UItemUse Supper;
public:
	UItemShenTongSkill();
	~UItemShenTongSkill();
	void SetDynamicData(int32 SkillID_, int32 Level_, int32 PreExp, int32 ReduceUseLevel, uint8 isComminution_);
public:
	///神通技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemShenTongSkill | Property")
		int32 shenTongSkillID;
	///神通技能等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemShenTongSkill | Property")
		int32 shenTongLevel;
	///当前经验值
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemShenTongSkill | Property")
		int32 preExp;
	///降低使用等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemShenTongSkill | Property")
		int32 reduceUseSkillLevel;
	///是否可以精研
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemShenTongSkill | Property")
		bool isComminution;
	///神通技能消耗
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemShenTongSkill | Property")
		int32 shenTongRequire;
	///神通技能CD
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemShenTongSkill | Property")
		int32 shenTongSkillCD;
};