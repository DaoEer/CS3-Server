#pragma once

#include "Util/CS3Debug.h"
#include "CS3Base/CS3EntityInterface.h"
#include "GameData/Skill/SkillUIData.h"
#include "Entity/Alias.h"
#include "RoleChuanChengInterface.generated.h"

/*
* 文件名称：RoleChuanChengInterface.h
* 功能说明：传承技能
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2020-8-24
*/
/**
 * 玩家传承技能接口类
 */

UCLASS(BlueprintType)
class CHUANGSHI_API URoleChuanChengInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
		typedef UCS3EntityInterface Supper;
	CS3_DECLARE_INTERFACE_MAP()
public:
	URoleChuanChengInterface();
	~URoleChuanChengInterface();
	static FString GetName() { return TEXT("RoleChuanChengInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_RoleChuanChengInterface.BP_RoleChuanChengInterface_C'"); } //获取蓝图对象路径

	virtual void onEnterWorld() override;        ///< 当Entity进入世界时，此方法被调用
	virtual void onLeaveWorld() override;		///< 当Entity离开世界（被销毁时）时，此方法被调用

	void Init();
	void ClearAllData();

	/**
	*Define method
	*BlueprintCallable,解锁传承技能栏栏位成功回调
	*
	*@param index 栏位ID
	*
	*@return 无
	*/
	void OnUnlockChuanChengSkillBar(const int32 & index);

	/**
	*Define method
	*BlueprintCallable,更新传承技能栏栏位（装备、卸下、升级、解锁 调用）
	*
	*@param val
	*
	*@return 无
	*/
	void UpdateChuanChengSkillBar(const FVariant& data);

	/**
	* BlueprintCallable，根据栏位ID获取栏位数据
	*
	* @param id 栏位ID
	*
	* @return true:
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleChuanChengInterface")
		void GetChuanChengSkillBarData(int32 id, uint8& isLock, int32& skillID);
	
	/**
	* BlueprintCallable，根据技能ID判断技能是否已装备
	*
	* @param SkillID 技能ID
	*
	* @return 是否已装备
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleChuanChengInterface")
		bool IsLoadChuanChengSkill(int32 SkillID);

	/**
	*BlueprintCallable  获得已拥有的传承技能（按配置顺序）
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleChuanChengInterface")
		TArray<int32> GetSortChuanChengSkillList();

	/**
	*BlueprintCallable  获得已装备的传承技能（按栏位顺序）
	*/
	UFUNCTION(BlueprintCallable, Category = "RoleChuanChengInterface")
		TArray<int32> GetLoadChuanChengSkillList();

	/**
	*BlueprintCallable 装上传承技能
	*@param skillID
	*@param index 栏位id
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
	void RPC_RequestFitChuanChengSkill(int32 skillID, int32 index);

	/**
	*BlueprintCallable 卸下传承技能
	*@param index 栏位id
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_RequestUnloadChuanChengSkill(int32 index);

	/**
	*BlueprintCallable 开启传承技能栏位
	*@param index 栏位id
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_RequestUnlockChuanChengSkillBar(int32 index);

	/**
	*BlueprintCallable 升级传承技能
	*@param skillID
	*/
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_RequestChuanChengSkillUpgrade(int32 skillID);

private:
	
private:
	TMap<int32, FCHUANCHENG_SKILL_BAR_DATA> ChuanChengSkillBarData; ///<玩家传承技能栏数据  栏位：数据
};
