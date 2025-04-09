#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "CS3Base/CS3Entity.h"
#include "GameData/GameDeFine.h"
#include "GameData/Skill/SkillTableData.h"
#include "SkillTargetObjImpl.h"
#include "AreaDefine.generated.h"

/*
* 文件名称：AreaDefine.h
* 功能说明：技能作用区域
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-10-29
*/

/*基类*/
UCLASS(BlueprintType)
class CHUANGSHI_API UArea :public UCS3Object
{
	GENERATED_BODY()
public:
	UArea();
	~UArea();
public:
	/*数据加载*/
	virtual void load(FSKILL_HIT_AREA dictDat);

	/**
	*Define method
	*获得技能位置
	*@prama caster 处理消耗的对象
	*@prama target 技能目标
	*@prama receiverList 受术者列表
	*
	*return 被筛选后的受术者列表
	*/
	virtual TArray<CS3Entity*> getObjectList(CS3Entity* caster, USkillTargetObjImpl* target);

	/*获取坐标*/
	virtual FVector GetPosition(CS3Entity* caster, USkillTargetObjImpl* target);
	/*获取朝向*/
	virtual FVector GetDirection(CS3Entity* caster, USkillTargetObjImpl* target);

	/*筛选受术对象 和 法术接收者之间的高度 */
	TArray<CS3Entity*> filterHeight(FVector position, TArray<CS3Entity*> receivers);

	/*计算偏移量*/
	FVector calculateOffset(FVector position, FVector direction);

	/*计算偏移角度*/
	float calculateYaw(float yaw);

	/*筛选圆形范围*/
	TArray<CS3Entity*> filterCircular(TArray<CS3Entity*> receivers, FVector centerPos, float radius);
protected:
	int32 unitReference;	//单位位置基准
	int32 direReference;	//单位朝向基准
	float maxHeight;	//AOE技能加入一个高度的检测
	float height; //搜索高度
	float offsetFront;	//向前偏移量
	float offsetLeft;	//向左偏移量
	float offsetUp;		//向上偏移量
	int32 offsetyaw;	//偏移角度
};


/*无范围(空打击)*/
UCLASS(BlueprintType)
class CHUANGSHI_API UNoRange :public UArea
{
	GENERATED_BODY()
public:
	UNoRange();
	~UNoRange();

public:
	virtual void load(FSKILL_HIT_AREA dictDat);
	virtual TArray<CS3Entity*> getObjectList(CS3Entity* caster, USkillTargetObjImpl* target);
};

/*单体*/
UCLASS(BlueprintType)
class CHUANGSHI_API USingle :public UArea
{
	GENERATED_BODY()
public:
	USingle();
	~USingle();
public:
	virtual void load(FSKILL_HIT_AREA dictDat);
	virtual TArray<CS3Entity*> getObjectList(CS3Entity* caster, USkillTargetObjImpl* target);
};


/*球形状*/
UCLASS(BlueprintType)
class CHUANGSHI_API USphere :public UArea
{
	GENERATED_BODY()
public:
	USphere();
	~USphere();

public:
	virtual void load(FSKILL_HIT_AREA dictDat);
	virtual TArray<CS3Entity*> getObjectList(CS3Entity* caster, USkillTargetObjImpl* target);

private:
	float radius;
};

/*矩形*/
UCLASS(BlueprintType)
class CHUANGSHI_API URectangle :public UArea
{
	GENERATED_BODY()
public:
	URectangle();
	~URectangle();

public:
	virtual void load(FSKILL_HIT_AREA dictDat);
	virtual TArray<CS3Entity*> getObjectList(CS3Entity* caster, USkillTargetObjImpl* target);
	bool inArea(FVector dstPos, FVector srcPos, float yaw);

private:
	float length = 0.0;	 //长
	float width = 0.0;  //宽
};

/*圆柱形*/
UCLASS(BlueprintType)
class CHUANGSHI_API UCircular :public UArea
{
	GENERATED_BODY()
public:
	UCircular();
	~UCircular();

public:
	virtual void load(FSKILL_HIT_AREA dictDat);
	virtual TArray<CS3Entity*> getObjectList(CS3Entity* caster, USkillTargetObjImpl* target);

private:
	float radius = 0.0;
};

/*扇形*/
UCLASS(BlueprintType)
class CHUANGSHI_API USector :public UArea
{
	GENERATED_BODY()
public:
	USector();
	~USector();

public:
	virtual void load(FSKILL_HIT_AREA dictDat);
	virtual TArray<CS3Entity*> getObjectList(CS3Entity* caster, USkillTargetObjImpl* target);
	bool inArea(FVector dstPos, FVector srcPos, float yaw);

private:
	float radius = 0.0; //半径
	float angle = 0.0; //夹角
};

/*环形*/
UCLASS(BlueprintType)
class CHUANGSHI_API UAnnulus :public UArea
{
	GENERATED_BODY()
public:
	UAnnulus();
	~UAnnulus();

public:
	virtual void load(FSKILL_HIT_AREA dictDat);
	virtual TArray<CS3Entity*> getObjectList(CS3Entity* caster, USkillTargetObjImpl* target);

private:
	float outerDiameter = 0.0;  //外径
	float innerDiameter = 0.0; //内径
};



UArea* NewAreaInstance(FSKILL_HIT_AREA dictData);