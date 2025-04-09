// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CS3Base/CS3EntityInterface.h"
#include "GameData/RoleCommanderData.h"
#include "GameData/ClientMonsterAIData.h"
#include "Manager/CfgManager.h"
#include "RoleCommanderInterface.generated.h"

/*
* 文件名称：RoleCommanderInterface.h
* 功能说明：玩家统帅小兵接口类
* 文件作者：liaojing
* 目前维护：liaojing
* 创建时间：2019-11-16
*/


UCLASS(BlueprintType)
class CHUANGSHI_API URoleCommanderInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()

private:
	TMap<FString, int32 > EquipData;
	const FCLIENT_MOSNTER_AI_DATA* SoldierMonsterAIData;

public:
	static FString GetName() { return TEXT("RoleCommanderInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleCommanderInterface.BP_RoleCommanderInterface_C'"); } //获取蓝图对象路径

	void InitSoldierFollow(int32 entityID);
	void CalcInitSoldierFollow(const float& Distance, const float& Extension, const int32& IndexMax, const int32& ArmIndex, const FVector& CenterPos, FVector& TargetPos, FVector& RelativePos, const FRotator& TargetRotator);
	void ResetGuardFollow(int32 entityID);
	void SoldierFollow();
	void SoldierFormationRect();
	void SoldierFormationCircle();
	void SoldierAttack();

	void GuardFollow();
	void GuardAttack();

	FVector GetVerticalPos(FVector Pos);
	void UpdateSoldierFollow(int32 entityID);

	const FCLIENT_MOSNTER_AI_DATA* GetClientMonsterAIConfig(FString scriptID);
	const UConfigTable* MonsterAIDatas;

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FowllowData", DisplayName = "FollowStartDist")
		float FollowStartDist = 300.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FowllowData", DisplayName = "FollowSpace")
		float FollowSpace =  300.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FowllowData", DisplayName = "FollowMaxIndex")
		int FollowMaxIndex = 5;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FormationRectData", DisplayName = "FormationRectStartDist")
		float FormationRectStartDist = 300.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FormationRectData", DisplayName = "FormationRectSpace")
		float FormationRectSpace = 300.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FormationRectData", DisplayName = "FormationRectMaxIndex")
		int FormationRectMaxIndex = 5;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FormationCircleData", DisplayName = "FormationCircleStartDist")
		float FormationCircleStartDist = 300.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FormationCircleData", DisplayName = "FormationCircleSpace")
		float FormationCircleSpace = 300.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "FormationCircleData", DisplayName = "FormationCircleMaxIndex")
		int FormationCircleMaxIndex = 5;
	
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FowllowArmsData", DisplayName = "ArmsData")
		FARMS_DATA ArmsData;


public:
	virtual void InitBlueCB() override;
	//---------------------------------BlueprintCallable------------------

	/** 跟随指令 */
	UFUNCTION(BlueprintCallable, Category = "cs3|URoleCommanderInterface")
	void CommandFollow();

	/** 攻击指令 */
	UFUNCTION(BlueprintCallable, Category = "cs3|URoleCommanderInterface")
		void CommandAttack();

	/** 士兵使用技能指令 */
	UFUNCTION(BlueprintCallable, Category = "cs3|URoleCommanderInterface")
		void CommandUseSkill();

	/** 列阵指令 矩形*/
	UFUNCTION(BlueprintCallable, Category = "cs3|URoleCommanderInterface")
		void CommandArrayRectangle();

	/** 列阵指令 圆形*/
	UFUNCTION(BlueprintCallable, Category = "cs3|URoleCommanderInterface")
		void CommandArrayCircle();

	/** 士兵技能 对位置释放*/
	UFUNCTION(BlueprintCallable, Category = "cs3|URoleCommanderInterface")
		void CmdUseSkillToPosition(int32 SkillID, FVector TargetPos);

	/** 士兵技能 对目标释放*/
	UFUNCTION(BlueprintCallable, Category = "cs3|URoleCommanderInterface")
		void CmdUseSkillToEntity(int32 SkillID, int32 TargetID);

	/** 士兵技能 对自身释放*/
	UFUNCTION(BlueprintCallable, Category = "cs3|URoleCommanderInterface")
		void CmdUseSkillToSelf(int32 SkillID);

	/** 攀爬指令，爬梯子*/
	UFUNCTION(BlueprintCallable, Category = "cs3|URoleCommanderInterface")
		void CmdClimb();

	//-----------------------------RPC ServerMethods----------------------------------
	void RPC_CmdFollow();
	void RPC_CmdAttack();
	void RPC_CmdUseSkill();
	void RPC_CmdArrayRectangle();
	void RPC_CmdArrayCircle();

	//-----------------------------RPC ClientMethods----------------------------------
	void RoleCmdOnControlled(const FString& ScriptID, const int32& entityID);

	void RoleDestroyArms();

	void RoleCmdUseSkillToPosition(const int32& SkillID, const FVector& TargetPos);

	void RoleCmdUseSkillToEntity(const int32& SkillID, const int32& TargetID);

	void RoleCmdUseSkillToSelf(const int32& SkillID);

	void InitRoleCmdArmsScriptID(const FString& leftGuardScriptID, const FString& rightGuardScriptID, const FString& soldierScriptID);

	//UFUNCTION(BlueprintNativeEvent, Category = "cs3|URoleCommanderInterface")
	void ShowRoleCmdUI(const uint8& isShow);

	void RoleRemoveSoldier(const int32& soldierID);

	void RoleCmdClimb();
};