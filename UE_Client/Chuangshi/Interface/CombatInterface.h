// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CS3Base/CS3EntityInterface.h"
#include "CombatInterface.generated.h"

/*
* 文件名称：CombatInterface.h
* 功能说明：
* 文件作者：wangzheng
* 目前维护：all
* 创建时间：2016-10-25
*/

/**
 * 战斗类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UCombatInterface : public UCS3EntityInterface
{
	GENERATED_BODY()
	CS3_DECLARE_INTERFACE_MAP();
	typedef UCS3EntityInterface Supper;
public:
	UCombatInterface();
	~UCombatInterface();
	static FString GetName() { return TEXT("CombatInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("BlueprintGeneratedClass'/Game/BluePrints/Entity/Interface/BP_CombatInterface.BP_CombatInterface_C'"); } //获取蓝图对象路径

	/**
	*Define method
	*BlueprintCallable,位置同步检测S2C
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "CombatInterface")
		void CLIENT_CheckClientPosition();

	/**
	* Define method
	* BlueprintImplementableEvent,服务器回调函数,通知客户端打开技能学习界面
	*
	* @param teacherID 导师ID
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "cs3|Entity")
		void CLIENT_requestOpenSkillLearn(const int32 teacherID);



	/**
	* Define method
	* BlueprintCallable,怪物播放暴尸效果
	*
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "CombatInterface")
		void CLIENT_PlayDeadEffect();

	UFUNCTION(BlueprintNativeEvent, Category = "CombatInterface")
		void PlayDeadEffect();

	/**
	* Define method
	* BlueprintCallable,怪物播放停尸效果
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "CombatInterface")
		void PlayDeadMortuaryEffect();

	/**
	* Define method
	* BlueprintCallable，以给定速度靠近到某个点
	*
	* @param targetID ，目标ID（int32）
	*
	* @return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "CombatInterface")
		void CLIENT_OnWalkAroundTarget(int32 targetID);

	/**
	* Define method
	* BlueprintCallable，以给定速度靠近到某个点结束
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "CombatInterface")
		void CLIENT_OnWalkAroundTargetEnd();

	int32 GetWalkAroundTargetID() { return WalkAroundTargetID; };

	/**
	* Define method
	* BlueprintCallable,服务器通知客户端停止移动
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "CombatInterface")
		void CLIENT_NotifyStopMoving();

	/**
	* Define method
	* BlueprintCallable,战斗力改变提示
	*@param value 变化值
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "CombatInterface")
		void CLIENT_ShowCombatPowerChangeTips(int32 combatpower, int32 value);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestSkillLearn(const FString& STRING_1, const FString& STRING_2);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_setPkModeFC(const int32& INT32_1);

	/// SkillID 为下一等级技能
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_CELL_requestSkillUpgrade(const int32& SkillID);
	/// 将SkillID升级到最大等级
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void requestSkillUpgradeMax(const int32& SkillID);

	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestPassiveSkillLearn(const int32& SkillID);
	/// SkillID 为下一等级技能
	UFUNCTION(BlueprintCallable, Category = "Game|RPC")
		void RPC_requestPassiveSkillUpgrade(const int32& SkillID);

	virtual void InitBlueCB() override;

	void RPC_setAreaRelationRuleFC(FString AreaPvpRule);

	void RPC_ReceivePosFromClient(FVector Position);
	void RPC_ReceiveDirectionFromClient(FVector Direction);

	TMap<int32, int32> GetEnemyList();
	TMap<int32, int32> GetDamageList();

private:
	int32 WalkAroundTargetID = 0;

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 HP;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 HP_Max;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 MP;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 MP_Max;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		FString playerName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 profession;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 level;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 exp;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 MaxExp;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 corporeity;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 strength;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 intellect;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 dexterity;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 damage;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 magic_damage;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 armor;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 magic_armor;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 criticalstrike;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 discern;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 parry;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 speed;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 hitrate;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 dodgerate;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 healingrate;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 camp;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 feats;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 potential;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 xiuwei;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 xiuweiLevel;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 gangQiValue;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 gangQiValue_Max;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 gangQiState;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 tempCamp;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 jingjieLevel;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 gangQi_qiJieProgress;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 combatPower;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 killingValue;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 vitPoint;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 vitPoint_Max;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 cure;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 ice_damage;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 fire_damage;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 thunder_damage;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 xuan_damage;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 ice_armor;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 fire_armor;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 thunder_armor;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 xuan_armor;
	
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 damage_ignore;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 magic_damage_ignore;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 armor_ignore;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 magic_armor_ignore;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 criticalstrike_ignore;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 parry_ignore;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 hitrate_ignore;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 dodgerate_ignore;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 ice_damage_ignore;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 fire_damage_ignore;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 thunder_damage_ignore;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 xuan_damage_ignore;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 ice_armor_ignore;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 fire_armor_ignore;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 thunder_armor_ignore;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 xuan_armor_ignore;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 depress_resist;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 hitback_resist;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 control_resist;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "combat")
		int32 insane_resist;

	virtual void Set_HP(const int32& newVal, const int32& oldVal);
	virtual void Set_HP_Max(const int32& newVal, const int32& oldVal);
	virtual void Set_MP(const int32& newVal, const int32& oldVal);
	virtual void Set_MP_Max(const int32& newVal, const int32& oldVal);
	virtual void Set_PlayerName(const FString& newVal, const FString& oldVal);
	virtual void Set_profession(const int32& newVal, const int32& oldVal);
	virtual void Set_level(const int16& newVal, const int16& oldVal);
	virtual void Set_exp(const int32& newVal, const int32& oldVal);
	virtual void Set_corporeity(const int32& newVal, const int32& oldVal);
	virtual void Set_strength(const int32& newVal, const int32& oldVal);
	virtual void Set_intellect(const int32& newVal, const int32& oldVal);
	virtual void Set_dexterity(const int32& newVal, const int32& oldVal);
	virtual void Set_damage(const int32& newVal, const int32& oldVal);
	virtual void Set_magic_damage(const int32& newVal, const int32& oldVal);
	virtual void Set_armor(const int32& newVal, const int32& oldVal);
	virtual void Set_magic_armor(const int32& newVal, const int32& oldVal);
	virtual void Set_criticalstrike(const int32& newVal, const int32& oldVal);
	virtual void Set_discern(const int32& newVal, const int32& oldVal);
	virtual void Set_parry(const int32& newVal, const int32& oldVal);
	virtual void Set_speed(const int32& newVal, const int32& oldVal);
	virtual void Set_hitrate(const int32& newVal, const int32& oldVal);
	virtual void Set_dodgerate(const int32& newVal, const int32& oldVal);
	virtual void Set_healingrate(const int32& newVal, const int32& oldVal);
	virtual void Set_camp(const int32& newVal, const int32& oldVal);
	virtual void Set_feats(const int32& newVal, const int32& oldVal);
	virtual void Set_potential(const int32& newVal, const int32& oldVal);
	virtual void Set_xiuwei(const int32& newVal, const int32& oldVal);
	virtual void Set_xiuweiLevel(const int32& newVal, const int32& oldVal);
	virtual void Set_gangQiValue(const int32& newVal, const int32& oldVal);
	virtual void Set_gangQiValue_Max(const int32& newVal, const int32& oldVal);
	virtual void Set_gangQiState(const int32& newVal, const int32& oldVal);
	//virtual void Set_title(const int32& newVal, const int32& oldVal);
	virtual void Set_tempCamp(const int32& newVal, const int32& oldVal);
	virtual void Set_jingjieLevel(const int32& newVal, const int32& oldVal);
	virtual void Set_gangQi_qiJieProgress(const int32& newVal, const int32& oldVal);
	virtual void Set_combatPower(const int32& newVal, const int32& oldVal);
	virtual void Set_killingValue(const int32& newVal, const int32& oldVal);
	virtual void Set_vitPoint(const int32& newVal, const int32& oldVal);
	virtual void Set_vitPoint_Max(const int32& newVal, const int32& oldVal);
	virtual void Set_cure(const int32& newVal, const int32& oldVal);
	virtual void Set_ice_damage(const int32& newVal, const int32& oldVal);
	virtual void Set_fire_damage(const int32& newVal, const int32& oldVal);
	virtual void Set_thunder_damage(const int32& newVal, const int32& oldVal);
	virtual void Set_xuan_damage(const int32& newVal, const int32& oldVal);
	virtual void Set_ice_armor(const int32& newVal, const int32& oldVal);
	virtual void Set_fire_armor(const int32& newVal, const int32& oldVal);
	virtual void Set_thunder_armor(const int32& newVal, const int32& oldVal);
	virtual void Set_xuan_armor(const int32& newVal, const int32& oldVal);

	virtual void Set_damage_ignore(const int32& newVal, const int32& oldVal);
	virtual void Set_magic_damage_ignore(const int32& newVal, const int32& oldVal);
	virtual void Set_armor_ignore(const int32& newVal, const int32& oldVal);
	virtual void Set_magic_armor_ignore(const int32& newVal, const int32& oldVal);
	virtual void Set_criticalstrike_ignore(const int32& newVal, const int32& oldVal);
	virtual void Set_parry_ignore(const int32& newVal, const int32& oldVal);
	virtual void Set_hitrate_ignore(const int32& newVal, const int32& oldVal);
	virtual void Set_dodgerate_ignore(const int32& newVal, const int32& oldVal);

	virtual void Set_ice_damage_ignore(const int32& newVal, const int32& oldVal);
	virtual void Set_fire_damage_ignore(const int32& newVal, const int32& oldVal);
	virtual void Set_thunder_damage_ignore(const int32& newVal, const int32& oldVal);
	virtual void Set_xuan_damage_ignore(const int32& newVal, const int32& oldVal);
	virtual void Set_ice_armor_ignore(const int32& newVal, const int32& oldVal);
	virtual void Set_fire_armor_ignore(const int32& newVal, const int32& oldVal);
	virtual void Set_thunder_armor_ignore(const int32& newVal, const int32& oldVal);
	virtual void Set_xuan_armor_ignore(const int32& newVal, const int32& oldVal);

	virtual void Set_depress_resist(const int32& newVal, const int32& oldVal);
	virtual void Set_hitback_resist(const int32& newVal, const int32& oldVal);
	virtual void Set_control_resist(const int32& newVal, const int32& oldVal);
	virtual void Set_insane_resist(const int32& newVal, const int32& oldVal);
};