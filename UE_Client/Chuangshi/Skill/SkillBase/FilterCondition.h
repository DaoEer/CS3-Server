#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "CS3Base/CS3Entity.h"
#include "GameData/Skill/SkillTableData.h"
#include "SkillTargetObjImpl.h"
#include "FilterCondition.generated.h"

/*
* 文件名称：FilterCondition.h
* 功能说明：受术者筛选条件
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-10-29
*/

class USkill;

/*基类*/
UCLASS(BlueprintType)
class CHUANGSHI_API UFilterBase :public UCS3Object
{
	GENERATED_BODY()
public:
	UFilterBase();
	~UFilterBase();

public:
	/*数据加载*/
	virtual void init(FRECEIVER_FLITER_CONDITION dictDat);

	/**
	*Define method
	*条件检测
	*@prama caster 处理消耗的对象
	*@prama target 技能目标
	*@prama receiverList 受术者列表
	*
	*return 被筛选后的受术者列表
	*/
	virtual TArray<CS3Entity*> filter(CS3Entity* caster, USkillTargetObjImpl* target, TArray<CS3Entity*> receiverList);
};

/*随机最大受术人数*/
UCLASS(BlueprintType)
class CHUANGSHI_API UOrderByRandom :public UFilterBase
{
	GENERATED_BODY()
public:
	UOrderByRandom();
	~UOrderByRandom();
public:
	virtual void init(FRECEIVER_FLITER_CONDITION dictDat);
	virtual TArray<CS3Entity*> filter(CS3Entity* caster, USkillTargetObjImpl* target, TArray<CS3Entity*> receiverList);
private:
	int32 _maxNumber;
};

/*单位属性排序*/
UCLASS(BlueprintType)
class CHUANGSHI_API UOrderByProperty :public UFilterBase
{
	GENERATED_BODY()
public:
	UOrderByProperty();
	~UOrderByProperty();
public:
	virtual void init(FRECEIVER_FLITER_CONDITION dictDat);
	virtual TArray<CS3Entity*> filter(CS3Entity* caster, USkillTargetObjImpl* target, TArray<CS3Entity*> receiverList);
private:
	FString _property;
	int32 _operation;
	int32 _maxNumber;
};

/*施法者距离排序*/
UCLASS(BlueprintType)
class CHUANGSHI_API UOrderByDistanceToCaster :public UFilterBase
{
	GENERATED_BODY()
public:
	UOrderByDistanceToCaster();
	~UOrderByDistanceToCaster();
public:
	virtual void init(FRECEIVER_FLITER_CONDITION dictDat);
	virtual TArray<CS3Entity*> filter(CS3Entity* caster, USkillTargetObjImpl* target, TArray<CS3Entity*> receiverList);
private:
	FString _property;
	int32 _operation;
	int32 _maxNumber;
};


/*施法目标距离排序*/
UCLASS(BlueprintType)
class CHUANGSHI_API UOrderByDistanceToTarget :public UFilterBase
{
	GENERATED_BODY()
public:
	UOrderByDistanceToTarget();
	~UOrderByDistanceToTarget();
public:
	virtual void init(FRECEIVER_FLITER_CONDITION dictDat);
	virtual TArray<CS3Entity*> filter(CS3Entity* caster, USkillTargetObjImpl* target, TArray<CS3Entity*> receiverList);
private:
	FString _property;
	int32 _operation;
	int32 _maxNumber;
};


UCLASS(BlueprintType)
class CHUANGSHI_API UFilterCondition :public UCS3Object
{
	GENERATED_BODY()
public:
	UFilterCondition();
	~UFilterCondition();
public:
	/*数据加载*/
	void init(TArray<FRECEIVER_FLITER_CONDITION> conditionList);
	void add(FRECEIVER_FLITER_CONDITION Condition);
	/*条件检测*/
	TArray<CS3Entity*> filter(USkill* Skill, CS3Entity* caster, USkillTargetObjImpl* target, TArray<CS3Entity*> receiverList);
public:
	UPROPERTY()
		TArray <UFilterBase *> _conditions;  //条件实列表
};

