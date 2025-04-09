#pragma once
#include "CoreMinimal.h"
#include "CS3Base/CS3Entity.h"
#include "GameData/GameDeFine.h"
#include "GameData/CS3Object.h"
#include "SkillTargetObjImpl.generated.h"


/*基类*/
UCLASS(BlueprintType)
class CHUANGSHI_API USkillTargetObjImpl :public UCS3Object
{
	GENERATED_BODY()
public:
	USkillTargetObjImpl();
	~USkillTargetObjImpl();
	virtual SKILL_TARGET_TYPE getType();
	virtual CS3Entity* getObject();
	virtual FVector getObjectPosition();
	virtual void onSkillBegin(CS3Entity* caster);

protected:
	SKILL_TARGET_TYPE _type;

};

/*技能对无目标和位置的施法对象的封装*/
UCLASS(BlueprintType)
class CHUANGSHI_API USkillTargetObjNone :public USkillTargetObjImpl
{
	GENERATED_BODY()
public:
	USkillTargetObjNone();
	~USkillTargetObjNone();
public:
	virtual SKILL_TARGET_TYPE getType();
	virtual CS3Entity* getObject();
	virtual FVector getObjectPosition();
};

/*技能对entity的受术或目标的封装*/
UCLASS(BlueprintType)
class CHUANGSHI_API USkillTargetObjEntity :public USkillTargetObjImpl
{
	GENERATED_BODY()
public:
	USkillTargetObjEntity();
	~USkillTargetObjEntity();

public:
	void init(CS3Entity* entity);
	virtual SKILL_TARGET_TYPE getType();
	virtual CS3Entity* getObject();
	virtual FVector getObjectPosition();
	virtual void onSkillBegin(CS3Entity* caster);
private:
	int32 _entityID;
};

/*技能对位置的受术或目标的封装*/
UCLASS(BlueprintType)
class CHUANGSHI_API USkillTargetObjPosition :public USkillTargetObjImpl
{
	GENERATED_BODY()
public:
	USkillTargetObjPosition();
	~USkillTargetObjPosition();
public:
	void init(FVector position);
	virtual SKILL_TARGET_TYPE getType();
	virtual FVector getObjectPosition();
private:
	FVector _entityPosition;
};



