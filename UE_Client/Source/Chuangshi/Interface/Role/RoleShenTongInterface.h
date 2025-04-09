#pragma once

#include "Util/CS3Debug.h"
#include "CS3Base/CS3EntityInterface.h"
#include "GameData/Skill/SkillUIData.h"
#include "RoleShenTongInterface.generated.h"

/*
* 文件名称：RoleShenTongInterface.h
* 功能说明：神通技能
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-3-21
*/
/**
 * 玩家神通技能接口类
 */

UCLASS(BlueprintType)
class CHUANGSHI_API URoleShenTongInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleShenTongInterface();
	~URoleShenTongInterface();
	static FString GetName() { return TEXT("RoleShenTongInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleShenTongInterface.BP_RoleShenTongInterface_C'"); } //获取蓝图对象路径

	virtual void InitBlueCB() override;

	/**
	*申请精研神通技能
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_RquestComminution(const FString & Suid, const FString & ItemList);
	/**
	*Define method
	*BlueprintNativeEvent 打开精研界面
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleShenTongInterface")
		void CLIENT_rquestComminution(const int32& npcID);

	/**
	*Define method
	*BlueprintNativeEvent 更新神通物品的动态数据
	*@Param Suid			神通物品UID
	*@Param SkillID			神通物品技能ID
	*@Param Level			神通物品使用等级
	*@Param PreExp			神通物品当前精研经验
	*@Param ReduceUseLevel	神通物品降低使用等级
	*@Param isComminution	神通物品是否可以精研
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "RoleShenTongInterface")
		void CLIENT_UpdateShenTongDynamic(const FString& Suid, const int32& SkillID, const int32& Level, const int32& PreExp, const int32& ReduceUseLevel, const uint8& isComminution);
	UFUNCTION(BlueprintImplementableEvent, Category = "RoleShenTongInterface")
		void OnUpdateShenTongDynamic(const FString& Suid);

	/**
	*Define method
	*@Param SkillID			神通技能ID
	*@Param Times			改神通技能可使用次数
	*@Param isAdd			是否为新增神通技能
	*
	*/
	void UpdateShenTongSKill(const int32& SkillID, const int32& Times, const uint8 isAdd);

	/**
	*Define method  获得所有神通神通技能
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		TMap<int32, int32> GetShenTongSKills();

	/**
	*BlueprintCallable  获得所有神通技能（默认，按配置顺序）
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleShenTongInterface")
		TArray<int32> GetShenTongSKillsSortByIndex();
	/**
	*BlueprintCallable  获得所有神通技能（按等级排序）
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleShenTongInterface")
		TArray<int32> GetShenTongSKillsSortByLevel();
	/**
	*BlueprintCallable  获得所有神通技能（按剩余次数排序）
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleShenTongInterface")
		TArray<int32> GetShenTongSKillsSortByRemainTimes();
	/**
	*BlueprintCallable  获得所有神通技能次数
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleShenTongInterface")
	int32 GetShenTongSKillTimes(const int32& SkillID);

	/**
	*BlueprintCallable 获得神通技能配置数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleShenTongInterface")
		FSKILL_SHEN_TONG_TREE_CONFIG GetShenTongSKillCfgBySkillID(int32 SkillID);

	/**
	*BlueprintCallable  获得幻兽神通技能配置数据
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleShenTongInterface")
		FSKILL_SHEN_TONG_TREE_CONFIG GetPetShenTongSKillCfgBySkillID(int32 SkillID);

	/**
	*申请学习幻兽神通技能
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_LearnPetShenTongSkill(FString PetUid, FString ItemUid);


	/**
	*申请精研神通技能
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_DelPetShenTongSkill(FString PetUid, int32 SkillID);

private:
	/**
	*	获得所有神通技能
	*/
	TArray<int32> GetShenTongSKillIDs();

private:
	UPROPERTY()
	TMap<int32, int32> ShenTongSkills;	//技能ID：技能次数
};
