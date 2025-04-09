#pragma once
#include "CoreMinimal.h"
#include "CS3Base/CS3Entity.h"
#include "GameData/CS3Object.h"
#include "SkillTargetObjImpl.h"
#include "GameData/Skill/SkillTableData.h"
#include "ObjectDefine.generated.h"

/*
* 文件名称：ObjectDefine.h
* 功能说明：施法目标的封装
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-10-29
*/

/*基类*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTargetBase :public UCS3Object
{
	GENERATED_BODY()
public:
	UTargetBase();
	~UTargetBase();
public:
	/*初始化数据*/
	virtual void init(const FSKILL_TABLE_DATA* dictDat);
	/*获得类型*/
	virtual ENUM_CAST_TARGET_TYPE GetType();
	/*判断是否可以施法*/
	virtual int32 CastValid(CS3Entity* caster, USkillTargetObjImpl* target);

protected:
	/*施法最大距离*/
	float CastRangeMax;
	/*技能施展方式*/
	ENUM_CAST_TARGET_TYPE type;

};



/*无施法位置和对象*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTargetNothing :public UTargetBase
{
	GENERATED_BODY()
public:
	UTargetNothing();
	~UTargetNothing();

public:
	/*初始化数据*/
	virtual void init(const FSKILL_TABLE_DATA* dictDat);
	/*获得类型*/
	virtual ENUM_CAST_TARGET_TYPE GetType();
	/*判断是否可以施法*/
	virtual int32 CastValid(CS3Entity* caster, USkillTargetObjImpl* target);


}; 

/*施法目标为位置*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTargetPosition : public UTargetBase
{
	GENERATED_BODY()
public:
	UTargetPosition();
	~UTargetPosition();
public:
	virtual void init(const FSKILL_TABLE_DATA* dictDat);
	virtual ENUM_CAST_TARGET_TYPE GetType();
	virtual int32 CastValid(CS3Entity* caster, USkillTargetObjImpl* target);


};

/*施法目标为锁定的Entity*/
UCLASS(BlueprintType)
class CHUANGSHI_API UTargetLock : public UTargetBase
{
	GENERATED_BODY()
public:
	UTargetLock();
	~UTargetLock();

public:
	virtual void init(const FSKILL_TABLE_DATA* dictDat);
	virtual ENUM_CAST_TARGET_TYPE GetType();
	virtual int32 CastValid(CS3Entity* caster, USkillTargetObjImpl* target);

};

/*创建实例*/
UTargetBase * ObjectDefineNewInstance(ENUM_CAST_TARGET_TYPE type);