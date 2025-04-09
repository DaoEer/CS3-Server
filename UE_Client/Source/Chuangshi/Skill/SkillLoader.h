#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "Skill/SkillBase/Skill.h"
#include "SkillLoader.generated.h"

/*
* 文件名称：SkillLoader.h
* 功能说明：技能实例创建文件
* 文件作者：xuyongqi
* 目前维护：all
* 创建时间：2019-10-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API USkillLoader :public UCS3Object
{
	GENERATED_BODY()
public:
	~USkillLoader();
	/*获得/创建单例*/
	static USkillLoader* GetInstance();

	void loadAllSkill();
	USkill* CreateSkill(FString SkillID, const FSKILL_TABLE_DATA* SkillData);
	USkill* getSkillByID(int32 SkillID);
	
private:
	USkillLoader();


private:
	UPROPERTY()
	TMap<int32, USkill*> _skills;

};

