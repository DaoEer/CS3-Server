#pragma once
#include "CoreMinimal.h"
#include "CS3Base/CS3Entity.h"
#include "GameData/CS3Object.h"
#include "GameData/Skill/SkillTableData.h"
#include "HitTypeDefine.generated.h"

/*
* 文件名称：HitTypeDefine.h
* 功能说明：命中类型定义
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-10-29
*/

/*基类*/
UCLASS(BlueprintType)
class CHUANGSHI_API UHitBase :public UCS3Object
{
	GENERATED_BODY()
public:
	UHitBase();
	~UHitBase();

public:
	/*
	*Define method
	*判断是否命中
	*/
	SKILL_HIT_TYPE isHit(CS3Entity* caster, CS3Entity* receiver);
};

/*基类*/
UCLASS(BlueprintType)
class CHUANGSHI_API UHitDirect : public UHitBase
{
	GENERATED_BODY()
public:
	UHitDirect();
	~UHitDirect();

public:
	/*
	*Define method
	*判断是否命中
	*/
	SKILL_HIT_TYPE isHit(CS3Entity* caster, CS3Entity* receiver);
};
UCLASS(BlueprintType)
class CHUANGSHI_API UHitDodge : public UHitBase
{
	GENERATED_BODY()
public:
	UHitDodge();
	~UHitDodge();

public:
	/*
	*Define method
	*判断是否命中
	*/
	SKILL_HIT_TYPE isHit(CS3Entity* caster, CS3Entity* receiver);
};

UCLASS(BlueprintType)
class CHUANGSHI_API UHitTypeDefine:public UCS3Object
{
	GENERATED_BODY()
public:
	~UHitTypeDefine();
	/*单例*/
	static UHitTypeDefine* GetInstance();
	SKILL_HIT_TYPE isHit(ENUM_HIT_TYPE type, CS3Entity* caster, CS3Entity* receiver);
private:
	UHitTypeDefine();

	static UHitTypeDefine* Instance;
};

UHitTypeDefine* UHitTypeDefine::Instance = nullptr;