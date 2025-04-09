// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "CS3Base/CS3Entity.h"
#include "GameData/Skill/SkillData.h"
#include "GameData/Skill/SkillTableData.h"
#include "Engine/Classes/Engine/EngineTypes.h"
#include "FightAssist.generated.h"
/*
* 文件名称：FightAssist.h
* 功能说明：技能施法辅助（条件检测,目标追踪）
* 文件作者：ranxuanwen
* 目前维护：huting
* 创建时间：2016-10-31
*/
class USkillManager;
class UMessageManager;
class UParticleManager;

DECLARE_DYNAMIC_DELEGATE_ThreeParams(FUseSkillForTargetDelegate, int32, SkillID, int32, TargetID, bool, IsSuccess);

UCLASS(BlueprintType)
class CHUANGSHI_API UFightAssist : public UCS3Object
{
	GENERATED_BODY()
public:
	UFightAssist();
	virtual void BeginDestroy() override;
	/**
	 * 检测使用技能的系列条件
	 * @param AtkEntity CS3Entity*   施法者
	 * @param BeAtkEntity CS3Entity* 受击者 
	 * @param SkillId Int32*          当前使用的技能标识
	 * @return bool
	 */
	bool CheckSkillUseCondition(CS3Entity* AtkEntity, CS3Entity* BeAtkEntity, int32 SkillId);

	/**
	* 检测自动使用技能的系列条件
	* @param AtkEntity		施法者(CS3Entity*)  
	* @param BeAtkEntity	受击者(CS3Entity*)
	* @param SkillID		技能ID(int32)
	* @param BShowMsg		是否显示msg(bool)
	* @return bool
	*/
	bool CheckAutoUseSkill(CS3Entity* AtkEntity, CS3Entity* BeAtkEntity, int32 SkillID, bool BShowMsg = true);

	/**
	* 检测自动使用技能的系列条件
	* @param AtkEntity		施法者(CS3Entity*)
	* @param BeAtkEntity	受击者(CS3Entity*)
	* @param SkillID		技能ID(int32)
	* @return bool
	*/
	bool CheckAutoUseItem(AServerCharacter* TargetEntity, int32 ItemID);

	/// 清除战斗辅助UI
	void ClearFightAssistUi(bool bIsNeedCopyAssUI = false);

	void ClearModelAssistUi();

	/// 复制战斗辅助UI
	void CopyFightAssistUi();
	/**
	* 使用位置技能
	* @param  AtkActor AServerCharacter* 当前施法者
	* @param  SkillId int32            使用的技能
	* @param  TargetPostion FVector&	被施法目标位置
	*/
	void UsePostionSkill(AServerCharacter* AtkActor, int32 SkillId, const FVector& TargetPostion);

	/**
	* 使用指向性物品
	* @param  AtkActor AServerCharacter* 当前施法者
	* @param  UID FString	            使用的技能
	* @param  SkillId int32			   使用的物品技能
	* @param  TargetPostion FVector&	被施法目标位置
	*/
	void UsePostionItem(AServerCharacter* AtkActor, FString UID, int32 SkillId, const FVector& TargetPostion);

	/**
	* 使用指向性物品扩展
	* @param  AtkActor AServerCharacter* 当前施法者
	* @param  UID FString	            使用的技能
	* @param  SkillId int32			   使用的物品技能
	* @param  TargetPostion FVector&	被施法目标位置
	*/
	void UsePostionItemExt(AServerCharacter* AtkActor, FString UID, int32 SkillId, const FVector& TargetPostion);

	bool CheckMoveToTraceTargetPostion(CS3Entity* AtkEntity, FVector& TargetPostion, int32 SkillId);

	/**
	* 添加物品辅助UI
	* @param  AtkEntity CS3Entity*   使用者
	* @param  UID		FString		 物品UID
	* @param  SkillId	Int32*       技能ID
	*/
	void AddItemAssistUi(CS3Entity* AtkEntity, FString& UID, int32 SkillId);

	/**
	* 添加物品辅助UI扩展
	* @param  AtkEntity CS3Entity*   使用者
	* @param  UID		FString		 物品UID
	* @param  SkillId	Int32*       技能ID
	*/
	void AddItemAssistUiExt(CS3Entity* AtkEntity, FString& UID, int32& SkillId);

	// 旋转辅助施法模型朝向
	void TurnAssistModelDir(float Scale);
public:
	///战斗辅助贴花
	UPROPERTY()
		class UDecalComponent* FightAssistDecal;
	///战斗辅助水上贴花模型
	UPROPERTY()
		class UStaticMeshComponent* FightAssistMesh;
	UPROPERTY()
		TArray<UMaterialInterface*> DSMaterialList;

	UPROPERTY()
		int32 FightAssistEffectID;

private:
	USkillManager* SkillManager;
	UMessageManager* MessageManager;
	UParticleManager* ParticleManager;
	class UCameraCaptureTranslucentComponent* CameraTranComponent;
	class ASceneCharacter* ModelAssistCharacter;
	UPROPERTY()
	FTimerHandle EffectTimerHandle;
	
	///位置技能辅助施法中
	bool bIsSkillCastAssisting = false;
	/**
	 * 是否在施法中
	 * @param AtkEntity CS3Entity* 
	 * @return bool
	 */
	bool IsCasting(CS3Entity* AtkEntity);
	/**
	 * 是否在冷却中
	 * @param  AtkEntity CS3Entity*施法者
	 * @param  SkillId   Int32      当前使用的技能标识
	 * @return bool
	 */
	bool IsCoolDowning(CS3Entity* AtkEntity, int32 SkillId);
	/**
	 * 是否有足够的消耗品
	 * @param AtkEntity  CS3Entity* 施法者
	 * @param SkillId    Int32       当前使用的技能标识
	 * @return bool
	 */
	bool HasEnoughtConsumables(CS3Entity* AtkEntity, int32 SkillId);
	/**
	 * 检查施法者的条件是否满足
	 * @param  AtkEntity CS3Entity* 施法者
	 * @return bool
	 */
	bool CheckCasterCondition(CS3Entity* AtkEntity, int32 SkillId);
	/**
	* 检查目标的条件是否满足
	* @param AtkEntity 施法者(CS3Entity*)
	* @param BeAtkEntity 受击者(CS3Entity*)
	* @param SkillID 技能ID(int32)
	* @return bool
	*/
	bool CheckTargetCondition(CS3Entity* AtkEntity, CS3Entity* BeAtkEntity, int32 SkillID);
	/**
	 * 施法者是否在死亡状态
	 * @param   AtkEntity CS3Entity* 施法者
	 * @return  bool
	 */
	bool IsAtkEntityDead(CS3Entity* AtkEntity);
	/*
	 * 目标是否在死亡状态
	 * @param  BeAtkEntity CS3Entity*  受击者
	 * @return bool
	 */
	bool IsBeAtkEntityDead(CS3Entity* BeAtkEntity);
	/**
	 * 检查是否需要追踪目标
	 * @param   AtkEntity CS3Entity* 施法者
	 * @param   TargetActor AActor*  目标对象 
	 * @param   SkillId  Int32*      当前使用的技能标识
	 * @return  bool 
	 */
	bool CheckMoveToTraceTargetActor(CS3Entity* AtkEntity, AActor* TargetActor, int32 SkillId);

	
	/**
	 * 添加技能辅助UI
	 * @param  AtkEntity CS3Entity*   施法者
	 * @param  SkillId   Int32*        当前使用的技能标识
	 */
	void AddSkillAssistUi(CS3Entity* AtkEntity, int32 SkillId);

	void AddEffectTimerHander(CS3Entity* AtkEntity, int32 SkillId);

	void AddModelEffectAssist(CS3Entity * AtkEntity, FString & UID, int32& SkillId);

	void UpdateEffectTimerHander(CS3Entity* AtkEntity, int32 SkillId);

	void UpdateModelEffectAssist(CS3Entity * AtkEntity, const FString & UID, const int32& SkillId);
	/**
	 * 使用位置技能
	 * @param  AtkActor AServerCharacter*  当前施法者
	 * @param  SkillId  int32            使用的技能
	 * @param  TargetId	int32			 被施法目标对象
	 */
	void UseTargetSkill(AServerCharacter* AtkActor, int32 SkillId, int32 TargetId);
	
};
