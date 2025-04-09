// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "SkillTableData.h"
#include "PassiveSkillTableData.h"
#include "GameData/CS3Object.h"
#include "Component/CS3AudioComponent.h"
#include "SkillData.generated.h"

/**
* 文件名称：SkillData.h
* 功能说明：
* 文件作者：ranxuanwen
* 目前维护：wuxiaoou
* 创建时间：2016-10-18
*/

///技能使用效果
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_USE_RESULT
{
	GENERATED_BODY();
public:
	FString CasterCastEffectId;///<光效ID
	FString CasterCastSoundId;///<音效ID
	FString TargetCastEffectId;///<对技能目标释放的光效ID
	FString TargetCastSoundId;///<技能目标音效ID
	
	FString SkillName;///<技能名称
	bool IsPromptSkillName;///是否显示技能名称的头顶冒字
};


///服务器技能冷却数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FSKILL_UPDATE_COOL_DOWN
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere)
	int32 CooldownId = 0;///<冷却ID标识符

	UPROPERTY(EditAnywhere)
	int64 EndTime; ///<结束时间

	UPROPERTY(EditAnywhere)
	float RemainingTime;///<剩余冷却时间

	UPROPERTY(EditAnywhere)
	float PersistTime;///<总冷却时间
};


///持续效果光效、动作
UCLASS(BlueprintType)
class CHUANGSHI_API UHoldEffectData : public UCS3Object
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "EffectIndex")
		int32 EffectIndex = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Effect")
		TArray<int32> EffectUIDList;

};

///持续效果声音
UCLASS(BlueprintType)
class CHUANGSHI_API UHoldEffectAudioData : public UCS3Object
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "EffectIndex")
		int32 EffectIndex;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "AudioComp")
		TArray<UCS3AudioComponent*> AudioCompList;
};


/**
* 文件名称：SkillData.h
* 功能说明：技能数据
* 涉及配置：
* 文件作者：JACK
* 创建时间：2016/10/11/8:52
* 更改记录:
*/
UCLASS(BlueprintType)
class CHUANGSHI_API USkillData : public UCS3Object
{
	GENERATED_BODY()
public:
	virtual void BeginDestroy()override;
	/**
	* 创建技能数据
	* @param TableData Buff数据
	* @return USkillData* 技能数据
	*/
	static USkillData* CreateSkillData(const FSKILL_TABLE_DATA* TableData);

	/**
	* 创建被动技能数据
	* @param TableData Buff数据
	* @return USkillData* 技能数据
	*/
	static USkillData* CreatePassiveSkillData(const FPASSIVE_SKILL_TABLE_DATA* TableData);

	/**
	* 施法者效果
	* @return FSKILL_USE_RESULT 施法者效果
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		FSKILL_USE_RESULT GetCasterResult();

	/**
	* 是否瞬发技能
	* @return bool 是瞬发技能返回TRUE，否则返回FALSE
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillData")
		bool IsInstantSkill();

	/**
	* 是否被动技能
	* @return bool 是被动技能返回TRUE，否则返回FALSE
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillData")
		bool IsPassiveSkill();

	/**
	* 是否CD中
	* @return bool 在CD中返回TRUE，否则返回FALSE
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		bool IsCoolDowning();

	/**
	* 启动CD计时器
	* @param TimeRemaining CD时间
	* @return 无
	*/
	void StartCdTime(float TimeRemaining);

	void StopCdTime();///<停止CD计时器

	void SetPersistTime(float PersistTime);//设置CD总持续时间

	/**
	* 获取剩余时间
	* @return int32
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		int32 GetRemainingTime();

	//获取CD总持续时间
	UFUNCTION(BlueprintPure, Category = "SkillData")
		float GetPersistTime();
	/**
	* 获取目标类型
	* @return ENUM_CAST_TARGET_TYPE
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		ENUM_CAST_TARGET_TYPE GetTargetType();

	/**
	* 获取辅助目标指定类型
	* @return ENUM_SKILL_ASSIST_TARGET_TYPE
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		ENUM_SKILL_ASSIST_TARGET_TYPE GetAssistTargetType();

	/**
	* 获取消耗需求
	* @return TArray<FSKILL_REQUIRE>
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		TArray<FSKILL_REQUIRE> GetCasterRequireList();

	/**
	* 获取施法者条件
	* @return TArray<FSKILL_USE_CONDITION>
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		TArray<FSKILL_USE_CONDITION> GetCasterCondition();

	/**
	* 获取所有目标条件列表
	* @return TArray<FSKILL_USE_CONDITION>
	*/
	TArray<TArray<FSKILL_USE_CONDITION>> GetTargetCondition();

	/**
	* 获取施法辅助
	* @return FSKILL_ASSIST_EFFECT
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		const FSKILL_ASSIST_EFFECT& GetAssistEffect();

	/**
	* 获取最大施法距离
	* @return float
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		float GetRangeMax();

	/**
	* 获取是否转向目标
	* @return bool
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		bool GetTurnToTarget();
	/**
	* 获取技能ID
	* @return FName
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillData")
		FName GetID();

	/**
	* 获取冷却时间
	* @return TArray<FSKILL_COOL_DOWN>
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillData")
		TArray<FSKILL_COOL_DOWN> GetCasterCoolDown();

	/**
	* 获取Icon
	* @return UTexture2D
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillData")
		UTexture2D* GetIcon();

	/**
	* 获取技能描述
	* @return FString
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		FString GetDescription();

	/**
	* 获取消耗显示描述
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		FString GetCasterRequireDescribe();

	/**
	* 获取冷却时间显示描述
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		FString GetCasterCoolDownDescribe();

	/**
	* 获取技能类型
	* @return FString
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		ENUM_SKILL_CLASS_TYPE GetSkillType();

	/**
	* 获取技能名称
	* @return FString
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		FString GetSkillName();

	/**
	* 获取技能等级
	* @return FString
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		int32 GetSkillLevel();

	/**
	* 获取技能品质
	* @return FString
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		int32 GetSkillQuality();

	/**
	* 获取CasterActForbid
	* @return FString
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		ACTION_FLAG GetCasterActForbid();
	/**
	* 获取TargetActForbid
	* @return FString
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		ACTION_FLAG GetTargetActForbid();
	/**
	* 是否可以主动中断技能
	* @return bool
	*/
	UFUNCTION(BlueprintPure, Category = "SkillData")
		bool CanInitiaiveInterrupt();

	//bool IsDataValid();	//和UObject新加的IsDataValid(TArray<FText>& ValidationErrors)重名，且返回值不一样，修改为下面的
	bool IsSkillDataValid();

private:
	/**
	* 设置UID
	* @param UId 技能UID
	* @return 无
	*/
	void SetUId(int32 UId);

	int32 GetUId();///<获取UID

private:
	const FSKILL_TABLE_DATA* SkillTableData;///<技能配置数据
	const FPASSIVE_SKILL_TABLE_DATA* PassiveSkillTableData;///<被动技能配置数据
	UPROPERTY()
		int32 UId;///<服务器唯一标识
	UPROPERTY()
		FTimerHandle CdTimerHandle;///<CD计时器
	UPROPERTY()
		float CDPersistTime;///CD持续总时间
};
