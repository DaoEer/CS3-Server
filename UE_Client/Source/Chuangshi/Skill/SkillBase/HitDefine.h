#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "CS3Base/CS3Entity.h"
#include "GameData/GameDeFine.h"
#include "GameData/Skill/SkillTableData.h"
#include "GameData/Skill/BuffTableData.h"
#include "SkillTargetObjImpl.h"
#include "Skill/Effect/EffectSkillBase.h"
#include "AreaDefine.h"
#include "ObjectCondition.h"
#include "FilterCondition.h"
#include "HitDefine.generated.h"

/*
* 文件名称：HitDefine.h
* 功能说明：技能作用对象类
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-10-29
*/

class USkill;
class UBuff;

UCLASS(BlueprintType)
class CHUANGSHI_API UHitDefine:public UCS3Object
{
	GENERATED_BODY()
public:
	UHitDefine();
	~UHitDefine();
public:
	/*初始化数据*/
	virtual void init(FSKILL_HIT dictDat, USkill* skill);

	/*接受打击效果*/
	virtual void receive(USkill* skill, CS3Entity* caster, CS3Entity* receiver);

	/*判断目标是否有效*/
	virtual int32 validReceiver(CS3Entity* caster, CS3Entity* receiver);

	/*筛选出所有合法者*/
	virtual TArray<CS3Entity*> filterReceiver(USkill* skill, CS3Entity* caster, USkillTargetObjImpl* target, TArray<CS3Entity*> receivers);

	/*取得所有的符合条件的受术者Entity列表；*/
	virtual TArray<CS3Entity*> getReceivers(USkill* skill, CS3Entity* caster, USkillTargetObjImpl* target);


	virtual TArray<UEffectSkillBase*> getEffectList();


protected:
	ENUM_HIT_TYPE _hitType;

	UPROPERTY()
	UArea* _hitArea; //打击范围

	UPROPERTY()
	UObjectCondition* _receiverCondition; //受术者条件

	UPROPERTY()
	UFilterCondition* _fliterCondition;  //受术者筛选条件

	UPROPERTY()
	TArray<UEffectSkillBase*>_effectList; //打击效果列表
};


UCLASS(BlueprintType)
class CHUANGSHI_API USkillHitDefine :public UHitDefine
{
	GENERATED_BODY()
public:
	USkillHitDefine();
	~USkillHitDefine();

public:
	/*初始化数据*/
	virtual void init(FSKILL_HIT dictDat, USkill* skill);

	/*开始打击*/
	void onHit(USkill* skill, CS3Entity* caster, USkillTargetObjImpl* target, int32 index);

	/*打击到达*/
	void onHitArrive(USkill* skill, CS3Entity* caster, USkillTargetObjImpl* target, int32 index);

private:
	UPROPERTY()
	int32 _hitTime;
};

UCLASS(BlueprintType)
class CHUANGSHI_API UBuffHitDefine :public UCS3Object
{
	GENERATED_BODY()
public:
	UBuffHitDefine();
	~UBuffHitDefine();

public:
	/*初始化数据*/
	void init(FBUFF_HIT dictDat, UBuff * buff);

	/*接受打击效果*/
	void receive(UBuff * buff, CS3Entity* caster, CS3Entity* receiver);

	/*判断目标是否有效*/
	int32 validReceiver(CS3Entity* caster, CS3Entity* receiver);

	/*筛选出所有合法者*/
	TArray<CS3Entity*> filterReceiver(UBuff * buff, CS3Entity* caster, USkillTargetObjImpl* target, TArray<CS3Entity*> receivers);

	/*取得所有的符合条件的受术者Entity列表；*/
	TArray<CS3Entity*> getReceivers(UBuff * buff, CS3Entity* caster, USkillTargetObjImpl* target);

	TArray<UEffectSkillBase*> getEffectList();

	/*打击到达*/
	void onHitArrive(UBuff* buff, CS3Entity* caster, USkillTargetObjImpl* target, FString attrName, int32 index);


private:
	ENUM_HIT_TYPE _hitType;

	UPROPERTY()
		UArea* _hitArea; //打击范围

	UPROPERTY()
		UObjectCondition* _receiverCondition; //受术者条件

	UPROPERTY()
		UFilterCondition* _fliterCondition;  //受术者筛选条件

	UPROPERTY()
		TArray<UEffectSkillBase*>_effectList; //打击效果列表
};



USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_HIT_DATAS
{
	GENERATED_BODY();
public:
	UPROPERTY()
	TArray< USkillHitDefine* > SkillHitDefines;
};


UCLASS(BlueprintType)
class CHUANGSHI_API USkillHitData :public UCS3Object
{
	GENERATED_BODY()
public:
	USkillHitData();
	~USkillHitData();
public:
	/*初始化数据*/
	void init(TArray<FSKILL_HIT> hitList, USkill* skill);

	/*开始*/
	void begin(USkill* skill, CS3Entity* caster, USkillTargetObjImpl* target);

	/*开始某一时刻的打击*/
	void onHit(USkill* skill, CS3Entity* caster, USkillTargetObjImpl* target, int32 hitTime);

	/*打击到达*/
	void onHitArrive(USkill* skill, CS3Entity* caster, USkillTargetObjImpl* target, int32 hitTime, int32 index);

	USkillHitDefine* getHit(int32 hitTime, int32 index);
	float getTotalTime();
	TMap<int32, FSKILL_HIT_DATAS> getHitData();



private:
	UPROPERTY()
		TMap<int32, FSKILL_HIT_DATAS> _data;
};


UCLASS(BlueprintType)
class CHUANGSHI_API UBuffHitData :public UCS3Object
{
	GENERATED_BODY()
public:
	UBuffHitData();
	~UBuffHitData();

public:
	/*初始化数据*/
	void init(TArray<FBUFF_HIT> hitList, UBuff* buff);

	UBuffHitDefine* getHit(int32 index);

	void onHit(UBuff* buff, CS3Entity* caster, USkillTargetObjImpl* target, FString attrName);
private:
	UPROPERTY()
	TArray< UBuffHitDefine* > _data;
};