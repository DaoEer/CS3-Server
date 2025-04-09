// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "../../GameData/Barracks/BarracksTableData.h"
#include "GameData/Barracks/RoleBarracksItemData.h"
#include "GameData/Barracks/RoleArmyData.h"
#include "GameData/Barracks/BarracksGuardSoldierSkillData.h"
#include "GameData/Barracks/BarracksReviveCostData.h"
#include "RoleBarracksInterface.generated.h"


/*
* 文件名称：RoleBarracksInterface.h
* 功能说明：
* 文件作者：yikun
* 目前维护：yikun
* 创建时间：2019-12-23
*/

/**
 * 玩家兵营接口
 */
UCLASS(BlueprintType)
class CHUANGSHI_API URoleBarracksInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
	typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleBarracksInterface();
	~URoleBarracksInterface();
	static FString GetName() { return TEXT("RoleBarracksInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleBarracksInterface.BP_RoleBarracksInterface_C'"); } //获取蓝图对象路径

	/**
	* BlueprintCallable，请求打开兵营
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
	void RequestOpenBarracks();

	/**
	* Define method
	* 初始化玩家兵营数据
	*
	* @return 无
	*/
	void InitRoleBarracksDatas(const FVariant& Var);

	/**
	* Define method
	* 增加玩家兵营数据
	*
	* @return 无
	*/
	void AddRoleBarracksData(const FVariant& Var);

	UFUNCTION(BlueprintImplementableEvent, Category = "RoleBarracksInterface")
	void OnAddRoleBarracksData(FROLEBARRACKSITEMDATA soldierData);

	/**
	* Define method
	* BlueprintNativeEvent，初始化玩家兵营数据结束
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBarracksInterface")
	void InitRoleBarracksDataOver(const int32& soldierType);

	void InitLoadBarracksCfgDatas(const int32& soldierType);

	void InitLoadBarracksSoldierSkillCfgDatas();

	void InitBarracksReviveCostDatas();
	/**
	* Define method
	* 初始化玩家部队数据
	*
	* @return 无
	*/
	void InitRoleArmyDatas(const FVariant& Var);

	/**
	* Define method
	* 保存玩家部队数据
	*
	* @return 无
	*/
	void SaveArmyDataCB(const FVariant& Var);
	
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleBarracksInterface")
		void OnSaveArmyDataCB(FROLEARMYDATA armyData);

	/**
	*
	* BlueprintCallable，平分经验给小兵
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
		void UpGradeGuardSoldierSkillLevel(const FString& scriptID, const int32& guardSoldierID, const int32& skillID, const int32& exp );
	/**
	* Define method
	* 更新玩家亲卫技能数据
	*
	* @return 无
	*/
	void OnUpdateGuardSoldierSkill(const FString& scriptID, const int32& soldierID,const int32& lastSkillID, const FVariant& Var);
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleBarracksInterface")
		void OnUpdateGuardSoldierSkillBP(const FString& scriptID, const int32& soldierID, const int32& lastSkillID,FPASSIVESKILLDATA skillData);

	/**
	* Define method
	* BlueprintNativeEvent，移除玩家兵营数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBarracksInterface")
		void RemoveRoleBarracksData(const FString& scriptID);

	/**
	* Define method
	* BlueprintNativeEvent，已解锁的兵
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBarracksInterface")
		void InitRoleBarracksUnLockSoldiers(const TArray<FString>& unLockSoldierScriptIDs);

	/**
	* Define method
	* BlueprintNativeEvent，移除玩家兵营兵的数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBarracksInterface")
	void RemoveRoleBarracksSoldierData(const FString& scriptID, const int32& soldierID);

	/**
	* Define method
	* BlueprintNativeEvent，更新玩家兵营兵的等级数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBarracksInterface")
		void UpdateSoldierLevelData(const FString& scriptID, const int32& soldierID,const int32& level);

	/**
	* Define method
	* BlueprintNativeEvent，更新玩家兵营兵的是否在部队数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBarracksInterface")
		void UpdateSoldierIsInArmyData(const FString& scriptID, const int32& soldierID, const int32& isInArmy);


	/**
	* Define method
	* BlueprintNativeEvent，是否激活，将领死亡时，界面需要做一些处理详情见事务：CST-10623 天兵营界面——兵种/亲兵死亡之后复活需求
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBarracksInterface")
		void UpdateSoldierIsActive(const FString& scriptID, const int32& soldierID, const int32& isActive);


	/**
	* Define method
	* BlueprintNativeEvent，更新玩家兵营兵的经验数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBarracksInterface")
		void UpdateSoldierExpData(const FString& scriptID, const int32& soldierID, const int32& exp, const int32& maxExp);

	/**
	*
	* BlueprintCallable，请求招募某个兵
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
	void RequestBuyBarracksSoldier(ENUM_BARRACKS_SOLDIER_TYPE soldierType,const FString& scriptID,const int32& count);


	/**
	*
	* BlueprintCallable，请求复活某个将领
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
		void RequestRevive(const FString& scriptID);

	/**
	*
	* BlueprintCallable，获取复活需要花费的金钱
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
		int32 GetReviveCost(const FString& scriptID, int32 level);

	/**
	*
	* BlueprintCallable，平分经验给小兵
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
		void DivideExpToSoldiers(ENUM_BARRACKS_SOLDIER_TYPE soldierType, const FString& scriptID,const int32& exp);


	/**
	*
	* BlueprintCallable，保存组合
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
	void SaveArmyData(const int32& id,const FString& firstGuardScriptID, const FString& secondGuardScriptID, const FString& soldierScriptID, const TArray<int32>& soldierIDs);

	/**
	* 
	* BlueprintCallable，获得玩家兵营数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
	TArray<FROLEBARRACKSITEMDATA> GetRoleRarracksDatasByScriptID(const FString& scriptID);

	/**
	*
	* BlueprintCallable，获得兵营兵的配置数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
	FBARRACKS_TABLE_DATA GetRarracksCfgDatasByScriptID(const ENUM_BARRACKS_SOLDIER_TYPE soldierType,const FString& scriptID);

	/**
	*
	* BlueprintCallable，获得兵营某个类型的所有数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
	TArray<FBARRACKS_TABLE_DATA> GetRarracksCfgDatasBySoldierType(const ENUM_BARRACKS_SOLDIER_TYPE soldierType);

	/**
	*
	* BlueprintCallable，获得玩家部队数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
	FROLEARMYDATA GetRoleArmyDatasByID(const int32& id);

	/**
	*
	* BlueprintCallable，获得玩家某个类型兵的数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
		TArray<FROLEBARRACKSITEMDATA> GetRoleRarracksDatasBySoldierType(const ENUM_BARRACKS_SOLDIER_TYPE soldierType,const TArray<FString>& removeScriptIDs);

	/**
	*
	* BlueprintCallable，获得玩家兵力经验
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
		FString GetRoleBarracksExp();

	/**
	*
	* BlueprintCallable，获得守卫兵第一级的技能数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
	TArray<FBARRACKS_GUARD_SOLDIER_SKILL_DATA> GetGuardSoldierFirstLevelSkillCfgData(const FString& scriptID);

	/**
	*
	* BlueprintCallable，通过技能ID获得守卫兵技能数据
	*
	* @return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
		FBARRACKS_GUARD_SOLDIER_SKILL_DATA GetGuardSoldierSkillCfgDataBySkillID(const FString& scriptID, const int32& skillID);

	/**
	*barracksExp(兵力经验)属性服务器修改客户端自动调用函数
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
		void OnRep_barracksExp();

	UFUNCTION(BlueprintImplementableEvent, Category = "RoleBarracksInterface")
	void OnBarracksExpChange();

	/**
	*BlueprintCallable 获得等级排序的某种士兵的列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
		TArray<FROLEBARRACKSITEMDATA> GetRoleRarracksDatasBySortLevel(const FString& scriptID, const TArray<int32>& removeSoldierIDs, const int32& count);

	/**
	*检查兵是否解锁
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
	bool CheckSoldierIsUnLock( const FString& scriptID);

	/**
	* 解散某支部队
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
		void DismissArmyData(const int32& armyID);

	/**
	* Define method
	* BlueprintNativeEvent，解散某支部队回调
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleBarracksInterface")
		void CLIENT_OnDismissArmyData(const int32& armyID);


	// 部队被派出去做任务
	void OnArmyDoQuest(const int32& armyID);
	// 部队做任务 消耗 兵种
	void OnArmyDoQuestConsume(const int32& armyID, const int32& num);
	// 部队完成任务回到大本营
	void OnArmyFinishQuestAndBack(const int32& armyID);

	virtual void onLeaveWorld() override;
	virtual void InitBlueCB() override;

	void ClearRoleBarracksData();

	int32 GetArmySoldierNumByScriptID(const FString& scriptID);

	/**
	* 进入练兵场大本营
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
		void EnterTrainSoldierGround();

	void Set_isCanOpenBarracks(const uint8& newVal, const uint8& oldVal);

	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
		bool IsCanOpenRoleBarracks();

	void InitBarracksByOccupyTrainGround(const FVariant& Var);

	void InitBarracksByOccupyTrainGroundOver(const int32& npcID, const int32& requireSoldierAmount, const int32& requireSoldierLevel);
	// 获得可以用于占领的小兵scriptID
	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
	TArray<FString> GetCanUseOccupySoldierScriptID();

	UFUNCTION(BlueprintCallable, Category = "RoleBarracksInterface")
		void SureToOccupyTrainGround(const int32& npcID, const FString& soldierScriptID);

	UPROPERTY(BlueprintReadOnly)
	TMap<int32, FROLEARMYDATA> RoleArmyDatas;
	UPROPERTY(BlueprintReadOnly)
		TArray<FString> RoleUnLockSoldiers; ///<玩家已解锁的兵
	UPROPERTY(BlueprintReadOnly)
		bool IsCanOpenBarracks; /// false 按钮置灰

	UPROPERTY(BlueprintReadOnly)
		int32 OccupySoldierAmount; ///  占领练兵场需要小兵数量
	UPROPERTY(BlueprintReadOnly)
		int32 OccupySoldierLevel; /// 占领练兵场需要小兵等级

private:
	TMap<ENUM_BARRACKS_SOLDIER_TYPE, TMap<FString, FBARRACKS_TABLE_DATA>> BarracksCfgDatas; //{兵类型：{兵ScriptID:兵数据}}
	TMap<FString, TArray<FROLEBARRACKSITEMDATA>> RoleBarracksDatas; //{兵scriptID:[]}
	TMap<FString, TMap<int32, FBARRACKS_GUARD_SOLDIER_SKILL_DATA>> BarracksSoldierSkillCfgData; // {兵ScriptID:{技能ID:技能数据}}
	TMap<FString, TMap<uint32, uint32>> BarracksReviveCostDatas; 
};