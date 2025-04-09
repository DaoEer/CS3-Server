// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "UObject/NoExportTypes.h"
#include "CharacterData.h"
#include "PetEpitome.generated.h"

/**
* 文件名称：PetEpitome.h
* 功能说明：幻兽虚拟数据
* 文件作者：chendongyong
* 目前维护：chengdongyong
* 创建时间：2017-7-21
*/

//#define  PET_EPITOME_UPDATE_METHOD(attrName,NewValue) OnRep_##attrName(NewValue)

UCLASS(Blueprintable, BlueprintType)
class CHUANGSHI_API UPetEpitome : public UObject
{
	GENERATED_BODY()
	
	typedef  void (UPetEpitome::*ptr_func)(FString&);

public:
	UPetEpitome();
	~UPetEpitome();
	/// 获取幻兽名称
	UFUNCTION(BlueprintCallable, Category = "PetEpitome")
	FString GetName();

	/// 更新幻兽数据
	UFUNCTION(BlueprintCallable, Category = "PetEpitome")
	void UpdateData(FString& attrName, FString& value);

	/// 获得神通技能可使用次数
	UFUNCTION(BlueprintCallable, Category = "PetEpitome")
		void GetPetShenTongSKillTimes(int32 SkillID, int32& Times);
public:
	///uid
	UPROPERTY(BlueprintReadOnly)
		FString uid;
	///scriptID
	UPROPERTY(BlueprintReadOnly)
		FString scriptID;
	///成长度
	UPROPERTY(BlueprintReadOnly)
		int32 ability = 0;
	///成长度
	UPROPERTY(BlueprintReadOnly)
		int32 ability_Max = 0;
	///品质
	UPROPERTY(BlueprintReadOnly)
		int32 quality = 0;
	///介次
	UPROPERTY(BlueprintReadOnly)
		int32 step = 0;
	///经验
	UPROPERTY(BlueprintReadOnly)
		int32 exp = 0;
	//--------------客户端配置---------------------------------
	///默认名字
	UPROPERTY(BlueprintReadOnly)
		FString uname;
	///幻兽头像
	UPROPERTY(BlueprintReadOnly)
		FString icon;
	///骑乘姿势
	UPROPERTY(BlueprintReadOnly)
		RIDE_POSTURE_ENUM RidePosture;
	///种族
	UPROPERTY(BlueprintReadOnly)
		int32 profession = 0;
	///类型
	UPROPERTY(BlueprintReadOnly)
		int32 combatType = 0;
	///族类
	UPROPERTY(BlueprintReadOnly)
		int32 race = 0;
	///携带等级
	UPROPERTY(BlueprintReadOnly)
		int32 takeLevel = 0;
	///幻兽主动技能(数据是读客户端表获得)
	UPROPERTY(BlueprintReadOnly)
		TMap<int32,int32> skills;
	//---------------------------------------------------------
	///休眠时间
	UPROPERTY(BlueprintReadOnly)
		FString sleepTime;
	///主动幻兽技能
	UPROPERTY(BlueprintReadOnly)
		TArray<int32> attrSkillBox;
	///被动幻兽技能
	UPROPERTY(BlueprintReadOnly)
		TArray<int32> passiveSkillBox;
	///未学习主动幻兽技能
	UPROPERTY(BlueprintReadOnly)
		TArray<int32> noLearnedSkillBox;
	///自定义名字
	UPROPERTY(BlueprintReadOnly)
		FString name;
	///筋骨
	UPROPERTY(BlueprintReadOnly)
		int32 corporeity = 0;
	///筋力
	UPROPERTY(BlueprintReadOnly)
		int32 strength = 0;
	///内力
	UPROPERTY(BlueprintReadOnly)
		int32 intellect = 0;
	///洞察
	UPROPERTY(BlueprintReadOnly)
		int32 discern = 0;
	///身法
	UPROPERTY(BlueprintReadOnly)
		int32 dexterity = 0;
	///生命
	UPROPERTY(BlueprintReadOnly)
		int32 HP = 0;
	///法力
	UPROPERTY(BlueprintReadOnly)
		int32 MP = 0;
	///生命
	UPROPERTY(BlueprintReadOnly)
		int32 HP_Max = 0;
	///法力
	UPROPERTY(BlueprintReadOnly)
		int32 MP_Max = 0;
	///物攻
	UPROPERTY(BlueprintReadOnly)
		int32 damage = 0;
	///法功
	UPROPERTY(BlueprintReadOnly)
		int32 magic_damage = 0;
	///物防
	UPROPERTY(BlueprintReadOnly)
		int32 armor = 0;
	///法防
	UPROPERTY(BlueprintReadOnly)
		int32 magic_armor = 0;
	///暴击
	UPROPERTY(BlueprintReadOnly)
		int32 criticalstrike = 0;
	///招架
	UPROPERTY(BlueprintReadOnly)
		int32 parry = 0;
	///移速
	UPROPERTY(BlueprintReadOnly)
		int32 speed = 0;
	///命中率
	UPROPERTY(BlueprintReadOnly)
		int32 hitrate = 0;
	///闪避率
	UPROPERTY(BlueprintReadOnly)
		int32 dodgerate = 0;
	///罡气值
	UPROPERTY(BlueprintReadOnly)
		int32 gangQiValue = 0;
	///罡气最大值
	UPROPERTY(BlueprintReadOnly)
		int32 gangQiValue_Max = 0;
	///罡气攻击
	UPROPERTY(BlueprintReadOnly)
		int32 gangQi_damagePoint = 0;
	///罡气防御
	UPROPERTY(BlueprintReadOnly)
		int32 gangQi_armorPoint = 0;
	///战斗力
	UPROPERTY(BlueprintReadOnly)
		int32 combatPower = 0;
	///治疗成效
	UPROPERTY(BlueprintReadOnly)
		int32 cure = 0;
	///冰元素攻击
	UPROPERTY(BlueprintReadOnly)
		int32 ice_damage = 0;
	///火元素攻击
	UPROPERTY(BlueprintReadOnly)
		int32 fire_damage = 0;
	///雷元素攻击
	UPROPERTY(BlueprintReadOnly)
		int32 thunder_damage = 0;
	///玄元素攻击
	UPROPERTY(BlueprintReadOnly)
		int32 xuan_damage = 0;
	///冰元素防御
	UPROPERTY(BlueprintReadOnly)
		int32 ice_armor = 0;
	///火元素防御
	UPROPERTY(BlueprintReadOnly)
		int32 fire_armor = 0;
	///雷元素防御
	UPROPERTY(BlueprintReadOnly)
		int32 thunder_armor = 0;
	///玄元素防御
	UPROPERTY(BlueprintReadOnly)
		int32 xuan_armor = 0;

	///物攻忽视
	UPROPERTY(BlueprintReadOnly)
		int32 damage_ignore = 0;
	///法攻忽视
	UPROPERTY(BlueprintReadOnly)
		int32 magic_damage_ignore = 0;
	///物防忽视
	UPROPERTY(BlueprintReadOnly)
		int32 armor_ignore = 0;
	///法防忽视
	UPROPERTY(BlueprintReadOnly)
		int32 magic_armor_ignore = 0;
	///暴击忽视
	UPROPERTY(BlueprintReadOnly)
		int32 criticalstrike_ignore = 0;
	///招架忽视
	UPROPERTY(BlueprintReadOnly)
		int32 parry_ignore = 0;
	///命中率忽视
	UPROPERTY(BlueprintReadOnly)
		int32 hitrate_ignore = 0;
	///闪避率忽视
	UPROPERTY(BlueprintReadOnly)
		int32 dodgerate_ignore = 0;

	///冰元素攻击忽视
	UPROPERTY(BlueprintReadOnly)
		int32 ice_damage_ignore = 0;
	///火元素攻击忽视
	UPROPERTY(BlueprintReadOnly)
		int32 fire_damage_ignore = 0;
	///雷元素攻击忽视
	UPROPERTY(BlueprintReadOnly)
		int32 thunder_damage_ignore = 0;
	///玄元素攻击忽视
	UPROPERTY(BlueprintReadOnly)
		int32 xuan_damage_ignore = 0;
	///冰元素防御忽视
	UPROPERTY(BlueprintReadOnly)
		int32 ice_armor_ignore = 0;
	///火元素防御忽视
	UPROPERTY(BlueprintReadOnly)
		int32 fire_armor_ignore = 0;
	///雷元素防御忽视
	UPROPERTY(BlueprintReadOnly)
		int32 thunder_armor_ignore = 0;
	///玄元素防御忽视
	UPROPERTY(BlueprintReadOnly)
		int32 xuan_armor_ignore = 0;

	///减损抵抗率
	UPROPERTY(BlueprintReadOnly)
		int32 depress_resist = 0;
	///击退抵抗率
	UPROPERTY(BlueprintReadOnly)
		int32 hitback_resist = 0;
	///控制抵抗率
	UPROPERTY(BlueprintReadOnly)
		int32 control_resist = 0;
	///心智抵抗率
	UPROPERTY(BlueprintReadOnly)
		int32 insane_resist = 0;

	///幻兽神通技能
	UPROPERTY(BlueprintReadOnly)
		TMap<int32, int32> petShenTongSKill;   ///{神通技能ID:技能可使用次数}

	///幻兽神通技能顺序列表
	UPROPERTY(BlueprintReadOnly)
		TArray<int32> petShenTongSKillList;		///[神通技能ID,....]

protected:
	void OnRep_ability(FString& newValue);
	void OnRep_ability_Max(FString& newValue);
	void OnRep_step(FString& newValue);
	void OnRep_name(FString& newValue);
	void OnRep_sleepTime(FString& newValue);
	void OnRep_attrSkillBox(FString& newValue);
	void OnRep_passiveSkillBox(FString& newValue);
	void OnRep_noLearnedSkillBox(FString& newValue);

	void OnRep_corporeity(FString& newValue);
	void OnRep_strength(FString& newValue);
	void OnRep_intellect(FString& newValue);
	void OnRep_discern(FString& newValue);
	void OnRep_dexterity(FString& newValue);
	void OnRep_HP(FString& newValue);
	void OnRep_MP(FString& newValue);
	void OnRep_HP_Max(FString& newValue);
	void OnRep_MP_Max(FString& newValue);
	void OnRep_damage(FString& newValue);
	void OnRep_magic_damage(FString& newValue);
	void OnRep_armor(FString& newValue);
	void OnRep_magic_armor(FString& newValue);
	void OnRep_criticalstrike(FString& newValue);
	void OnRep_parry(FString& newValue);
	void OnRep_speed(FString& newValue);
	void OnRep_hitrate(FString& newValue);
	void OnRep_dodgerate(FString& newValue);
	void OnRep_gangQiValue(FString& newValue);
	void OnRep_gangQiValue_Max(FString& newValue);
	void OnRep_gangQi_damagePoint(FString& newValue);
	void OnRep_gangQi_armorPoint(FString& newValue);
	void OnRep_combatPower(FString& newValue);
	void OnRep_ice_damage(FString& newValue);
	void OnRep_fire_damage(FString& newValue);
	void OnRep_thunder_damage(FString& newValue);
	void OnRep_xuan_damage(FString& newValue);
	void OnRep_ice_armor(FString& newValue);
	void OnRep_fire_armor(FString& newValue);
	void OnRep_xuan_armor(FString& newValue);
	void OnRep_thunder_armor(FString& newValue);

	void OnRep_damage_ignore(FString& newValue);
	void OnRep_magic_damage_ignore(FString& newValue);
	void OnRep_armor_ignore(FString& newValue);
	void OnRep_magic_armor_ignore(FString& newValue);
	void OnRep_criticalstrike_ignore(FString& newValue);
	void OnRep_parry_ignore(FString& newValue);
	void OnRep_hitrate_ignore(FString& newValue);
	void OnRep_dodgerate_ignore(FString& newValue);

	void OnRep_ice_damage_ignore(FString& newValue);
	void OnRep_fire_damage_ignore(FString& newValue);
	void OnRep_thunder_damage_ignore(FString& newValue);
	void OnRep_xuan_damage_ignore(FString& newValue);
	void OnRep_ice_armor_ignore(FString& newValue);
	void OnRep_fire_armor_ignore(FString& newValue);
	void OnRep_thunder_armor_ignore(FString& newValue);
	void OnRep_xuan_armor_ignore(FString& newValue);

	void OnRep_depress_resist(FString& newValue);
	void OnRep_hitback_resist(FString& newValue);
	void OnRep_control_resist(FString& newValue);
	void OnRep_insane_resist(FString& newValue);

	void OnRep_petShenTongSKill(FString& newValue);
	TMap<FString, ptr_func> PtrMap;
	

};

USTRUCT(BlueprintType)
struct FClientSealPetData
{
	GENERATED_BODY()
public:
	///自定义名字
	UPROPERTY(BlueprintReadOnly)
		FString name;
	///scriptID
	UPROPERTY(BlueprintReadOnly)
		FString scriptID;
	///品质
	UPROPERTY(BlueprintReadOnly)
		int32 quality = 0;
	///介次
	UPROPERTY(BlueprintReadOnly)
		int32 step = 0;
	///经验
	UPROPERTY( BlueprintReadOnly)
		int32 exp = 0;
	///类型
	UPROPERTY(BlueprintReadOnly)
		int32 combatType = 0;
	///生命
	UPROPERTY(BlueprintReadOnly)
		int32 HP = 0;
	///生命
	UPROPERTY(BlueprintReadOnly)
		int32 HP_Max = 0;
	///法力
	UPROPERTY(BlueprintReadOnly)
		int32 MP = 0;
	///法力
	UPROPERTY(BlueprintReadOnly)
		int32 MP_Max = 0;
	///罡气值
	UPROPERTY(BlueprintReadOnly)
		int32 gangQiValue = 0;
	///罡气最大值
	UPROPERTY(BlueprintReadOnly)
		int32 gangQiValue_Max = 0;
	///成长度
	UPROPERTY(BlueprintReadOnly)
		int32 ability = 0;
	///成长度
	UPROPERTY(BlueprintReadOnly)
		int32 ability_Max = 0;
	///移速
	UPROPERTY(BlueprintReadOnly)
		int32 speed = 0;
	///筋力
	UPROPERTY(BlueprintReadOnly)
		int32 strength = 0;
	///内力
	UPROPERTY(BlueprintReadOnly)
		int32 intellect = 0;
	///身法
	UPROPERTY(BlueprintReadOnly)
		int32 dexterity = 0;
	///筋骨
	UPROPERTY(BlueprintReadOnly)
		int32 corporeity = 0;
	///洞察
	UPROPERTY(BlueprintReadOnly)
		int32 discern = 0;
	///物攻
	UPROPERTY(BlueprintReadOnly)
		int32 damage = 0;
	///物防
	UPROPERTY(BlueprintReadOnly)
		int32 armor = 0;
	///法功
	UPROPERTY(BlueprintReadOnly)
		int32 magic_damage = 0;
	///法防
	UPROPERTY(BlueprintReadOnly)
		int32 magic_armor = 0;
	///暴击
	UPROPERTY(BlueprintReadOnly)
		int32 criticalstrike = 0;
	///命中率
	UPROPERTY(BlueprintReadOnly)
		int32 hitrate = 0;
	///招架
	UPROPERTY(BlueprintReadOnly)
		int32 parry = 0;
	///闪避率
	UPROPERTY(BlueprintReadOnly)
		int32 dodgerate = 0;
	///罡气攻击
	UPROPERTY(BlueprintReadOnly)
		int32 gangQi_damagePoint = 0;
	///罡气防御
	UPROPERTY(BlueprintReadOnly)
		int32 gangQi_armorPoint = 0;
	///治疗成效
	UPROPERTY(BlueprintReadOnly)
		int32 cure = 0;
	///主动幻兽技能
	UPROPERTY(BlueprintReadOnly)
		TArray<int32> attrSkillBox;
	///被动幻兽技能
	UPROPERTY(BlueprintReadOnly)
		TArray<int32> passiveSkillBox;
	///未学习主动幻兽技能
	UPROPERTY(BlueprintReadOnly)
		TArray<int32> noLearnedSkillBox;
	///冰元素攻击
	UPROPERTY(BlueprintReadOnly)
		int32 ice_damage = 0;
	///火元素攻击
	UPROPERTY(BlueprintReadOnly)
		int32 fire_damage = 0;
	///雷元素攻击
	UPROPERTY(BlueprintReadOnly)
		int32 thunder_damage = 0;
	///玄元素攻击
	UPROPERTY(BlueprintReadOnly)
		int32 xuan_damage = 0;
	///冰元素防御
	UPROPERTY(BlueprintReadOnly)
		int32 ice_armor = 0;
	///火元素防御
	UPROPERTY(BlueprintReadOnly)
		int32 fire_armor = 0;
	///雷元素防御
	UPROPERTY(BlueprintReadOnly)
		int32 thunder_armor = 0;
	///玄元素防御
	UPROPERTY(BlueprintReadOnly)
		int32 xuan_armor = 0;

	///物攻忽视
	UPROPERTY(BlueprintReadOnly)
		int32 damage_ignore = 0;
	///法攻忽视
	UPROPERTY(BlueprintReadOnly)
		int32 magic_damage_ignore = 0;
	///物防忽视
	UPROPERTY(BlueprintReadOnly)
		int32 armor_ignore = 0;
	///法防忽视
	UPROPERTY(BlueprintReadOnly)
		int32 magic_armor_ignore = 0;
	///暴击忽视
	UPROPERTY(BlueprintReadOnly)
		int32 criticalstrike_ignore = 0;
	///招架忽视
	UPROPERTY(BlueprintReadOnly)
		int32 parry_ignore = 0;
	///命中率忽视
	UPROPERTY(BlueprintReadOnly)
		int32 hitrate_ignore = 0;
	///闪避率忽视
	UPROPERTY(BlueprintReadOnly)
		int32 dodgerate_ignore = 0;

	///冰元素攻击忽视
	UPROPERTY(BlueprintReadOnly)
		int32 ice_damage_ignore = 0;
	///火元素攻击忽视
	UPROPERTY(BlueprintReadOnly)
		int32 fire_damage_ignore = 0;
	///雷元素攻击忽视
	UPROPERTY(BlueprintReadOnly)
		int32 thunder_damage_ignore = 0;
	///玄元素攻击忽视
	UPROPERTY(BlueprintReadOnly)
		int32 xuan_damage_ignore = 0;
	///冰元素防御忽视
	UPROPERTY(BlueprintReadOnly)
		int32 ice_armor_ignore = 0;
	///火元素防御忽视
	UPROPERTY(BlueprintReadOnly)
		int32 fire_armor_ignore = 0;
	///雷元素防御忽视
	UPROPERTY(BlueprintReadOnly)
		int32 thunder_armor_ignore = 0;
	///玄元素防御忽视
	UPROPERTY(BlueprintReadOnly)
		int32 xuan_armor_ignore = 0;

	///减损抵抗率
	UPROPERTY(BlueprintReadOnly)
		int32 depress_resist = 0;
	///击退抵抗率
	UPROPERTY(BlueprintReadOnly)
		int32 hitback_resist = 0;
	///控制抵抗率
	UPROPERTY(BlueprintReadOnly)
		int32 control_resist = 0;
	///心智抵抗率
	UPROPERTY(BlueprintReadOnly)
		int32 insane_resist = 0;
};

// 原兽数据
UCLASS(Blueprintable, BlueprintType)
class CHUANGSHI_API UOriginPetEpitome : public UPetEpitome
{
	GENERATED_BODY()
public:
	///野性
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		int32 wildness;
	///是否已经进化
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		bool bEvolution;
	///幻兽模型id
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FPET_DATA", DisplayName = "ModelNumber")
		FString ModelNumber;
	///幻兽模型大小倍率
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FPET_DATA", DisplayName = "ModelScale")
		float ModelScale;
	///原兽模型id
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FPET_DATA", DisplayName = "OriginModelNumber")
		FString OriginModelNumber;
	///原兽模型大小倍率
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FPET_DATA", DisplayName = "OriginModelScale")
		float OriginModelScale;
	///食材类型
	UPROPERTY(EditAnywhere, BlueprintReadOnly, category = "FPET_DATA", DisplayName = "foodType")
		int32 foodType;
};