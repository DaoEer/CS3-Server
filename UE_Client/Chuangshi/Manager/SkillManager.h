// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "Manager/CfgManager.h"
#include "GameData/Skill/SkillData.h"
#include "GameData/Skill/PassiveSkillTableData.h"
#include "GameData/Skill/SkillUIData.h"
#include "GameData/CS3Object.h"
#include "SkillManager.generated.h"

/*
* 文件名称：SkillManager.h
* 功能说明：技能数据管理类
* 文件作者：ranxuanwen
* 目前维护：wuxiaoou
* 创建时间：2016-12-07
*/

UCLASS(BlueprintType)
class CHUANGSHI_API USkillManager : public UCS3Object
{
	GENERATED_BODY()

private:
	USkillManager();
	~USkillManager();
	//USkillManager(const USkillManager& copy) = {}
	//virtual const USkillManager& operator=(const USkillManager& copy) { return Super::operator =(const USkillManager&); }

public:

#if WITH_EDITOR
	void UpdateSkillTable(UObject* Asset);
#endif

	static USkillManager* GetInstance();
	/**
	 * 更新玩家自己拥有的技能
	 *
	 * @param SkillId		int32 
	 * @param IsAddSkill	bool 增加技能或者删除技能
	 *
	 *@return 无
	 */
	void UpdateSelfSkillData(int32 SkillId, bool IsAddSkill);
	
	/**
	* 初始化召唤幻兽技能
	*
	* @param SkillIds		TArray<int32>
	*
	*@return 无
	*/
	void InitActPetSkills(TArray<int32> SkillIds);

	/**
	* 移除召唤幻兽技能
	*
	*
	*@return 无
	*/
	void RemoveActPetSkills();

	/**
	 * 更新技能CD
	 *
	 * @param UpdateSkillCdList TMap<int32, FSKILL_UPDATE_COOL_DOWN*> 
	 * @param SkillId  技能ID
	 *
	 *@return 无
	 */
	void UpdateSkillCoolDown(TMap<int32, FSKILL_UPDATE_COOL_DOWN> UpdateSkillCdList);
	
	void ClearSkillCoolDown();///<清理技能CD

	void onEnterWorld();
	void onLeaveWorld(); ///<技能数据清理
	
	/**
	* 通过技能ID获取技能数据
	*
	* @param SkillId  技能ID
	*
	* @return  USkillData* 技能数据
	*/
	UFUNCTION(BlueprintPure, Category = "SkillManager")
	USkillData* GetSkillDataById(int32 SkillId);
	
	/**
	* 获取玩家技能列表
	*
	* @return  TArray<int32>
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
	TArray<int32> GetPlayerSkillIdList();

	/**
	 * 获取玩家技能列表
	 *
	 * @return  TArray<USkillData*>
	 */
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
	TArray<USkillData*> GetPlayerDataSkillList();

	/**
	*设置禁用的三段跳技能
	*/
	void SetForbidJumpSkillIDs(TArray<int32> SkillIDs);

	/**
	*获取禁用的三段跳技能
	 * @return  TArray<int32>
	*/
	TArray<int32> GetForbidJumpSkillIDs();

	/**
	* 获取宠物技能列表
	*
	* @return  TArray<USkillData*>
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		TArray<USkillData*> GetPetDataSkillList();

	/**
	* 通过技能ID创建技能数据
	*
	* @param SkillId 技能ID
	*
	* @return  USkillData* 技能数据
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
	USkillData* CreateSkillDataById(int32 SkillId);

	/**
	* 通过技能ID获得技能图标
	*
	* @param SkillId 技能ID
	*
	* @return  UTexture2D* 技能数据
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
	UTexture2D* GetIconBySkillID(int32 SkillId);

	/**
	* 增加SkillData数据到总列表
	*
	* @param SkillId int32
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		void AddTotalSkillData(int32 SkillId);

	/**
	* 删除SkillData数据到总列表
	*
	* @param SkillId int32
	*
	*@return 无
	*/
	void RemoveTotalSkillData(int32 SkillId);

	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		void IsLearnedSkill(int32 SkillId, bool& isLearned, int32& PlayerSkillID);

	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		void IsInTeachSkillCfg(int32 SkillId, bool& isIn);

#pragma region	/** 主动技能 */

	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		void InitSkillTreeData();

	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		void SetSkillTreeData(int32 SkillID);

	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		void RemoveSkillTreeDataByID(int32 SkillId);

	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		void InitActionSkillData();

	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		TMap<int32, FSKILLLEARN_DATA> GetSkillLearnDatas();

	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		void InitSkillLearnDatasByTeacherID(int32 teacherID);

	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		void AddSkillLearnDataByID(int32 SkillId);

	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		void RemoveSkillLearnDataByID(int32 SkillId);

	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		TMap<int32, FSKILLTREEUI_DATA> GetSkillTreeUIDatas();

	/**
	* BlueprintCallable,获取技能学习数据
	*
	*@param	type 0:为不可学习技能，1:为可学习技能，2:为全部技能
	*@return TArray<FSKILLLEARN_DATA>技能学习数据列表
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		TArray<FSKILLLEARN_DATA> GetSortSkillLearnDatas(int32 type);

	/**
	* BlueprintCallable,获取技能升级面板数据
	*
	*@param	type 0:基础技能面板，1:天怒技能面板，2:神威技能面板 3:轻功技能面板
	*@return 技能树数据列表
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		TArray<FSKILLTREEUI_DATA> GetSkillTreeUIDatasByType( int32 type );

	/**
	* BlueprintCallable,获取技能树数据
	*
	*@param	SkillID 技能ID
	*@return 技能树数据
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		FSKILLTREEUI_DATA GetSkillTreeUIDatasByID(int32 SkillID, bool& IsSuccess);

	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		TMap<int32, FACTIONSKILL_DATA>  GetActionSKillDatas();

	/**
	*设置技能学习表数据
	*/
	void SetSkillLearnTableDatas();
	/**
	* BlueprintCallable,根据技能ID获取技能升级数据
	*
	* @param SkillId 技能ID
	*
	*@return 技能升级数据
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		FSKILLLEARN_DATA GetSkillLearnDataById(int32 SkillId);

	/**
	* BlueprintCallable,获取技能可升级到最大等级的技能ID列表
	*
	* @param SkillId 技能ID
	* @param SkillName 技能名称
	* @param MaxSkillLevel 技能能升到的最大等级
	* @param TotalRepPotential 从当前等级升到最大等级所需消耗的潜能
	*
	*@return 可升级到最大等级的技能ID列表
	*/

	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		TArray<int32> GetMaxUpgrateSkillList(int32 SkillId, FString& SkillName, int32& MaxSkillLevel, int32& TotalRepPotential);
	
	/**
	* BlueprintCallable,检查技能升级条件，用于验证是否可以升级
	*
	* @param SkillID 当前等级技能ID
	*
	*@return 是否可升级
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		bool CheckUpgradeCondition(int32 SkillID);

	/**
	* BlueprintCallable,检查技能是否满级，用于验证是否可以升级
	*
	* @param NextSkillID 下一等级技能ID
	*
	*@return 是否满级
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		bool CheckUpgradeCondition_IsFullLevel(int32 NextSkillID);

	/**
	* BlueprintCallable,检查技能是否达到升级等级，用于验证是否可以升级
	*
	* @param ReqLevel 升级需要的等级
	*
	*@return 是否达到等级
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		bool CheckUpgradeCondition_IsReachLevel(int32 ReqLevel);

	/**
	* BlueprintCallable,检查技能升级是否有足够的技能书，用于验证是否可以升级
	*
	* @param ReqMaterialID 升级需要的材料ID
	* @param ReqMaterialAmount 升级需要的材料数量
	*
	*@return 是否有足够的技能书
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		bool CheckUpgradeCondition_IsReachMaterial(int32 ReqMaterialID, int32 ReqMaterialAmount);

	/**
	* BlueprintCallable,检查技能升级是否有足够的潜能，用于验证是否可以升级
	*
	* @param  升级需要的的潜能
	*
	*@return 是否有足够的潜能
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		bool CheckUpgradeCondition_IsReachPotential(int32 ReqPotential);

	/**
	* BlueprintCallable,检查技能升级是否有足够的金钱，用于验证是否可以升级
	*
	* @param ReqMoney 升级需要的金钱
	*
	*@return 是否有足够的绑定金钱/绑金
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		bool CheckUpgradeCondition_IsReachBindMoney(int32 ReqMoney);

	/**
	* BlueprintCallable,检查技能升级是否有足够的金钱，用于验证是否可以升级
	*
	* @param ReqMoney 升级需要的金钱
	*
	*@return 是否有足够的金钱
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		bool CheckUpgradeCondition_IsReachMoney(int32 ReqMoney);

#pragma endregion

	/**
	* BlueprintCallable,检查心法限制，用于验证是否可以使用
	*
	* @param SkillID 技能ID
	*
	*@return 是否是当前心法可用
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		bool CheckConditionSkillPosture(int32 SkillID);

#pragma region	/** 被动技能 */
	/**
	* BlueprintCallable,获取玩家已经学习的被动技能
	*
	*@return 玩家已经学习的被动技能
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		TArray<FSKILL_PASSIVE_TREE_DATA> GetLearnedPassiveSkillList();
	/**
	* BlueprintCallable,获取所有的被动技能
	*
	*@return 所有的被动技能
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		TArray<FSKILL_PASSIVE_TREE_DATA> GetAllPassiveSkillList(int32 PassiveSkillType);

	/**
	* BlueprintCallable,获取被动技能树所有的被动技能
	*
	*@return 所有的被动技能
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		TMap<int32, FSKILL_PASSIVE_TREE_DATA> GetPassiveSkillTreeDatas();

	/**
	* BlueprintCallable,根据技能ID获取被动技能树数据
	*
	*@return 被动技能技能树数据
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		FSKILL_PASSIVE_TREE_DATA GetPassiveSkillDataBySkillID(int32 SkillID);

	///初始化被动技能列表数据
	void InitSkillPassiveListData();

	///更新被动技能列表数据
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		void SetPassiveListData(int32 SkillID);

	///更新被动技能列表数据
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		void RemovePassiveListDataByID(int32 SkillID);
	
	/**
	* BlueprintCallable,根据技能ID获取被动技能升级数据
	*
	* @param SkillId 技能ID
	*
	*@return 被动技能升级数据
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		FSKILL_PASSIVE_LEARN_DATA GetPassiveSkillLearnDataById(int32 SkillId);

	/**
	* BlueprintCallable,检查被动技能升级条件，用于验证是否可以升级
	*
	* @param SkillID 当前等级技能ID
	*
	*@return 是否可升级
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		bool CheckPassiveUpgradeCondition(int32 SkillID);

	/**
	* BlueprintCallable,获取解锁被动技能栏位消耗
	*
	* @param Index 栏位索引
	*
	*@return 解锁被动技能栏位消耗
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		FPASSIVESKILLBAR_DATA GetUnLockPassiveSkillSlotCost(int32 Index, bool& IsSuccess);

#pragma endregion

#pragma region	/** 传承技能 */
public:
	/**
	*BlueprintCallable  获得传承技能配置数据
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		FSKILL_CHUANCHENG_TREE_CONFIG GetChuanChengSkillTreeCfgBySkillID(int32 SkillID);
	/**
	*是否是传承技能
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		bool IsChuanChengSkill(int32 skillID);

	/**
	* BlueprintCallable,根据技能ID获取传承技能升级数据
	*
	* @param SkillId 技能ID
	*
	*@return 传承技能升级数据
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		FSKILL_CHUANCHENG_LEARN_DATA GetChuanChengSkillLearnDataById(int32 SkillId);

	/**
	*初始化传承技能技能树配置表数据
	*/
	void InitChuanChengSkillTreeTableDatas();

private:
	void InitChuanChengSkillLearnTableDatas();
#pragma endregion

#pragma region	/** 幻兽技能 */
public:
	/**
	* BlueprintCallable,根据技能ID获取幻兽技能升级数据（幻兽打书）
	*
	* @param SkillId 技能ID
	*
	*@return 幻兽技能升级数据
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		FPET_SKILL_PASSIVE_LEARN_DATA GetPetSkillLearnDataById(int32 SkillId, bool& IsSuccess);

private:
	void InitPetSkillLearnTableDatas();
#pragma endregion

public:
	///根据技能ID刷新CD
	void RefreshCDBySkillID(int32 SkillID);

	/**
	* BlueprintCallable,是否是相同技能
	*
	* @param SrcSkillID 技能ID
	* @param DestSkillID 技能ID
	*
	*@return 是否是相同技能
	*/
	UFUNCTION(BlueprintCallable, Category = "SkillManager")
		bool IsSameSkill(int32 SrcSkillID, int32 DestSkillID);

private:
	///设置玩家的跳跃最大次数
	void CheckJumpMaxCount(int32 SkillId);

	void StartCdTime(int32 CDID, float TimeRemaining);///<启动CD计时器

	void StopCdTime(int32 CDID);///<停止CD计时器

	float GetRemainingTime(int32 CDID);///<获取剩余时间

	const FSKILL_TABLE_DATA* GetSkillTableDataById(FString SkillId) const;

	TArray<FName> GetRowNamesFromSkillCfg();

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int TeacherID;	///<导师ID
private:
	UPROPERTY()
	TArray<int32> PlayerSkillIdList;///<玩家的技能ID列表

	UPROPERTY()
	TArray<int32> VPetSkillIdList;			///<出战幻兽的技能ID列表
	UPROPERTY()
	TArray<int32> LearnSkillIDs;			///<导师技能学习ID列表
	UPROPERTY()
		TMap<int32,USkillData*> totalSkillData;///<总技能数据表
	UPROPERTY()
		TMap<int32, FSKILLLEARN_DATA> SkillLearnDatas;///<技能学习数据 skillID:数据
	UPROPERTY()
		TMap<int32, FSKILLLEARN_DATA> SkillLearnTableData;///<技能学习表数据 skillID:数据
	UPROPERTY()
		TMap<int32, FSKILLTREEUI_DATA> SkillTreeUIDatas;///<技能树数据 skillID/1000:数据
	UPROPERTY()
		TMap<int32, FSKILL_PASSIVE_TREE_DATA> SkillPassiveTreeDatas;///<被动技能树数据 skillID/1000:数据
	UPROPERTY()
		TMap<int32, FSKILL_CHUANCHENG_TREE_CONFIG> ChuanChengSkillTreeDatas;  ///<传承技能树数据 skillID/1000:数据
	UPROPERTY()
		TMap<int32, FSKILL_CHUANCHENG_LEARN_DATA> ChuanChengSkillLearnTableData;///<传承技能学习表数据 skillID:数据
	UPROPERTY()
		TMap<int32, FPET_SKILL_PASSIVE_LEARN_DATA> PetSkillLearnTableData;///<幻兽技能学习表数据 skillID:数据
	UPROPERTY()
		TMap<int32, FACTIONSKILL_DATA> ActionSkillDatas;///<行为技能数据 skillID:数据
	UPROPERTY()
		TMap<int32, FSKILL_UPDATE_COOL_DOWN> AttrCooldowns;///<技能cd数据 cdid:cd数据
	UPROPERTY()
		TMap<int32, FTimerHandle> CdTimerHandle;///<cdid:CD计时器句柄

	bool IsInitSkillTree = false;	


	///禁用的三段跳技能
	TArray<int32> ForbidJumpSkillIDs;

	//static USkillManager* Instance;
};
