#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "CS3Base/CS3Entity.h"
#include "GameData/Skill/SkillTableData.h"
#include "RequireDefine.generated.h"

/**
*
* 技能消耗类
*
*/

class USkill;
/*基类*/
UCLASS(BlueprintType)
class CHUANGSHI_API URequire :public UCS3Object
{
	GENERATED_BODY()
public:
	URequire();
	~URequire();
public:
	/*数据加载*/
	virtual void load(FSKILL_REQUIRE Args);

	/**
	*Define method
	*校验对象是否满足需求
	*@prama caster 处理消耗的对象
	*@prama skillInstance 技能实例
	*return 技能消息
	*/
	virtual int32 validObject(CS3Entity* caster, USkill* SkillInstance);

	/**
	*Define method
	*支付消耗物
	*@prama caster 处理消耗的对象
	*@prama skillInstance 技能实例
	*return 无
	*/
	virtual void pay(CS3Entity* caster, USkill* SkillInstance);

	/**
	*
	*获取消耗物
	*@prama caster 处理消耗的对象
	*@prama skillInstance 技能实例
	*return 技能消息
	*/
	virtual int32 getPay(CS3Entity* caster, USkill* skillInstance);

protected:
	int32 _value;
	float _percent;
};

/*蓝量(MP)消耗*/
UCLASS(BlueprintType)
class CHUANGSHI_API URequireMp :public URequire
{
	GENERATED_BODY()
public:
	URequireMp();
	~URequireMp();
public:
	
	virtual void load(FSKILL_REQUIRE Args);

	virtual int32 validObject(CS3Entity* caster, USkill* SkillInstance);

	virtual void pay(CS3Entity* caster, USkill* SkillInstance);

	virtual int32 getPay(CS3Entity* caster, USkill* skillInstance);
};

/*血量(HP)消耗*/
UCLASS(BlueprintType)
class CHUANGSHI_API URequireHp :public URequire
{
	GENERATED_BODY()
public:
	URequireHp();
	~URequireHp();
public:
	virtual void load(FSKILL_REQUIRE Args);

	virtual int32 validObject(CS3Entity* caster, USkill* SkillInstance);

	virtual void pay(CS3Entity* caster, USkill* SkillInstance);

	virtual int32 getPay(CS3Entity* caster, USkill* skillInstance);
};

/*罡气消耗*/
UCLASS(BlueprintType)
class CHUANGSHI_API URequireGangQi :public URequire
{
	GENERATED_BODY()
public:
	URequireGangQi();
	~URequireGangQi();

public:
	virtual void load(FSKILL_REQUIRE Args);

	virtual int32 validObject(CS3Entity* caster, USkill* SkillInstance);

	virtual void pay(CS3Entity* caster, USkill* SkillInstance);

	virtual int32 getPay(CS3Entity* caster, USkill* skillInstance);
};

/*物品消耗*/
UCLASS(BlueprintType)
class CHUANGSHI_API URequireCostItem :public URequire
{
	GENERATED_BODY()
public:
	URequireCostItem();
	~URequireCostItem();

public:
	virtual void load(FSKILL_REQUIRE Args);

	virtual int32 validObject(CS3Entity* caster, USkill* SkillInstance);

	virtual void pay(CS3Entity* caster, USkill* SkillInstance);

	virtual int32 getPay(CS3Entity* caster, USkill* skillInstance);

private:
	int32 _itemID;
	int32 _amount;
};



UCLASS(BlueprintType)
class CHUANGSHI_API URequireDefine : public UCS3Object
{
	GENERATED_BODY()
public:
	URequireDefine();
	~URequireDefine();
public:
	/*数据加载*/
	void load(TArray<FSKILL_REQUIRE> Args);

	/*校验对象是否满足需求。*/
	int32 validObject(CS3Entity* caster, USkill* SkillInstance);
	/*支付*/
	void pay(CS3Entity* caster, USkill* SkillInstance);

private:
	
	UPROPERTY()
	TArray<URequire*> _requires; //消耗实例列表
};