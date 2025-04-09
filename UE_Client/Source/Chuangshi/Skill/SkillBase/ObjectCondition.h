#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "CS3Base/CS3Entity.h"
#include "GameData/Skill/SkillTableData.h"
#include "SkillTargetObjImpl.h"
#include "ObjectCondition.generated.h"

/*
* 文件名称：ObjectCondition.h
* 功能说明：施法者/受术者条件
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-10-29
*/

/*基类*/
UCLASS(BlueprintType)
class CHUANGSHI_API UConditionBase :public UCS3Object
{
	GENERATED_BODY()
public:
	UConditionBase();
	~UConditionBase();
public:
	virtual void init(FSKILL_USE_CONDITION dictDat );
	virtual int32 valid(CS3Entity* caster, CS3Entity* target, bool isCastValidCheck);
};

/*目标类型、关系*/
UCLASS(BlueprintType)
class CHUANGSHI_API UConditionTypeRelation :public UConditionBase
{
	GENERATED_BODY()
public:
	UConditionTypeRelation();
	~UConditionTypeRelation();
public:
	virtual void init(FSKILL_USE_CONDITION dictDat);
	virtual int32 valid(CS3Entity* caster, CS3Entity* target, bool isCastValidCheck);

private:
	TArray<FString> entityTypes;
	TArray<int32> relationTypes;
};

/*是否处于某状态*/
UCLASS(BlueprintType)
class CHUANGSHI_API UConditionState :public UConditionBase
{
	GENERATED_BODY()
public:
	UConditionState();
	~UConditionState();

public:
	virtual void init(FSKILL_USE_CONDITION dictDat);
	virtual int32 valid(CS3Entity* caster, CS3Entity* target, bool isCastValidCheck);

private:
	TArray<int32> stateList;
	int32 isThisState;
};

/*指定ID的Buff的个数*/
UCLASS(BlueprintType)
class CHUANGSHI_API UConditionBuffCount :public UConditionBase
{
	GENERATED_BODY()
public:
	UConditionBuffCount();
	~UConditionBuffCount();

public:
	virtual void init(FSKILL_USE_CONDITION dictDat);
	virtual int32 valid(CS3Entity* caster, CS3Entity* target, bool isCastValidCheck);

private:
	TArray<int32> _buffIdList;
	int32 _operation = 0;
	float _scale = 0.0;
};

/*指定ID的Buff的层数*/
UCLASS(BlueprintType)
class CHUANGSHI_API UConditionBuffLayer :public UConditionBase
{
	GENERATED_BODY()
public:
	UConditionBuffLayer();
	~UConditionBuffLayer();

public:
	virtual void init(FSKILL_USE_CONDITION dictDat);
	virtual int32 valid(CS3Entity* caster, CS3Entity* target, bool isCastValidCheck);

private:
	int32 _buffID = 0;
	int32 _operation = 0;
	float _scale = 0.0;
};

/*敌对关系*/
UCLASS(BlueprintType)
class CHUANGSHI_API UConditionEnemy :public UConditionBase
{
	GENERATED_BODY()
public:
	UConditionEnemy();
	~UConditionEnemy();

public:
	virtual void init(FSKILL_USE_CONDITION dictDat);
	virtual int32 valid(CS3Entity* caster, CS3Entity* target, bool isCastValidCheck);

private:
	TArray<int32> _assemble;
	int32 _operation;
};

/*是否指定的ID*/
UCLASS(BlueprintType)
class CHUANGSHI_API UConditionScriptID :public UConditionBase
{
	GENERATED_BODY()
public:
	UConditionScriptID();
	~UConditionScriptID();

public:
	virtual void init(FSKILL_USE_CONDITION dictDat);
	virtual int32 valid(CS3Entity* caster, CS3Entity* target, bool isCastValidCheck);

private:
	TArray<int32> ScriptIDList;
	int32 _isThisType = 0;
	int32 needRole = 0;
};

/*效果状态要求*/
UCLASS(BlueprintType)
class CHUANGSHI_API UConditionEffectState :public UConditionBase
{
	GENERATED_BODY()
public:
	UConditionEffectState();
	~UConditionEffectState();

public:
	virtual void init(FSKILL_USE_CONDITION dictDat);
	virtual int32 valid(CS3Entity* caster, CS3Entity* target, bool isCastValidCheck);

private:
	TArray<int32> effectStateList;
	int32 isThisState;
};



UCLASS(BlueprintType)
class CHUANGSHI_API UObjectCondition :public UCS3Object
{
	GENERATED_BODY()
public:
	UObjectCondition();
	~UObjectCondition();

public:
	virtual void init(TArray<FSKILL_USE_CONDITION> Conditions);
	void add(FSKILL_USE_CONDITION Condition);
	virtual int32 valid(CS3Entity* caster, CS3Entity* target, bool isCastValidCheck);
	bool isHasConditions(); 

protected:
	UPROPERTY()
	TArray<UConditionBase *> _conditions;  //条件实列表
};


/*buff替换效果条件*/
UCLASS(BlueprintType)
class CHUANGSHI_API UBuffReplaceCondition :public UObjectCondition
{
	GENERATED_BODY()
public:
	UBuffReplaceCondition();
	~UBuffReplaceCondition();

public:
	virtual int32 valid(CS3Entity* caster, CS3Entity* target, bool isCastValidCheck);
private:

};

/*buff额外效果条件*/
UCLASS(BlueprintType)
class UBuffExtraCondition :public UObjectCondition
{
	GENERATED_BODY()
public:
	UBuffExtraCondition();
	~UBuffExtraCondition();

public:
	virtual int32 valid(CS3Entity* caster, CS3Entity* target, bool isCastValidCheck);
private:

};


