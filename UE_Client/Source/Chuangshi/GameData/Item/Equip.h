// Fill out your copyright notice in the Description page of Project Settings.

#pragma once


#include "GameData/Item/ItemUse.h"
#include "GameData/ModelPartData.h"
#include "ItemIntensifyData.h"
#include "IntensifyLv.h"
#include "IntensifyCost.h"
#include "BackFireCost.h"
#include "Equip.generated.h"

/**
* 文件名称：Equip.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：chendongyong
* 创建时间：2017-01-17
*/

/**
 * 装备类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UEquip : public UItemUse
{
	GENERATED_BODY()
		typedef UItemUse Supper;

public:
	virtual void InitDynamicDataForJson(FString jsonStr) override;
	/**
	*BlueprintCallable，获取装备位置类型
	*
	*@return MODEL_PART_TYPE 装备位置类型
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Use")
		MODEL_PART_TYPE GetModelPartType();

	/**
	*BlueprintCallable，卸下装备
	*
	*@param player 玩家
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Use")
		void UnWield(AServerCharacter* player);

	/**
	*BlueprintCallable，获取装备的位置编号
	*
	*@return int32 装备的位置编号
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Use")
		int32 GetWieldOrder();

	/**
	*BlueprintCallable，获取戒指的位置编号
	*
	*@return int32 戒指的位置编号
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Use")
		int32 GetRingWieldOrder();
	
	/**
	*BlueprintCallable，获取基础属性和附加属性值
	*
	*@return FString 基础属性和附加属性值
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Describe")
		virtual FString GetPropertiesStr();
	
	/**
	*BlueprintCallable，获取解析propstr后的值颜色转换成propcolor之后的描述
	*
	*@param propstr 参数
	*@param propcolor 参数颜色
	*
	*@return FString 解析propstr后的值颜色转换成propcolor之后的描述
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Describe")
		FString ParsePropertiesStr(const FString& propstr, const FString& propcolor);

	/**
	*BlueprintCallable，获取解析propstr后的值颜色转换成propcolor之后的描述
	*
	*@param propstr 参数
	*@param propcolor 参数颜色
	*
	*@return FString 解析propstr后的值颜色转换成propcolor之后的描述
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Describe")
		virtual FString ParseMainPropertiesStr(const FString& propstr, const FString& propcolor);


	
	/**
	*BlueprintCallable，获取对propstr和propvalue封装后的值颜色转换成propcolor之后的描述
	*
	*@param propstr 参数
	*@param propvalue 参数值
	*@param propcolor 参数颜色
	*
	*@return FString 对propstr和propvalue封装后的值颜色转换成propcolor之后的描述
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Describe")
		FString GetPropertyStr(const FString& propid, const FString& propvalue, const FString& propcolor);
	
	/**
	*BlueprintCallable，获取基础属性值
	*
	*@return FString 基础属性
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Describe")
		FString GetAttackPropertyStr();

	/**
	*BlueprintCallable，获取附加属性值
	*
	*@return FString 附加属性值
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Describe")
		virtual FString GetAttachPropertyStr();
	
	/**
	*BlueprintCallable，获取是否绑定的描述
	*
	*@return FString 装备是绑定了返回绑定，否则返回未绑定
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Describe")
		FString GetBindStr();

	/**
	*BlueprintCallable，获取是装备的最大耐久度
	*
	*@return int32 最大耐久度
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Hardiness")
		int32 GetHardinessMax();

	/**
	*BlueprintCallable，获取显示装备的耐久度字符串
	*
	*@return int32 耐久度
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Describe")
		FString GetHardinessStr();

	/**
	*BlueprintCallable，获取是装备的耐久度
	*
	*@return int32 耐久度
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Hardiness")
		int32 GetHardiness();

	/**
	*BlueprintCallable，获取是装备的耐久度百分比
	*
	*@return float 耐久度百分比
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Hardiness")
		float GetHardinessPercent();

	/**
	*BlueprintCallable，更新装备耐久度
	*
	*@return None
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Hardiness")
	void OnRep_Hardiness();

	/**
	*BlueprintCallable，更新装备强化属性
	*
	*@return None
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Hardiness")
		void OnRep_IntensifyDataStr();

	/**
	*BlueprintCallable，更新装备品质
	*
	*@return None
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Hardiness")
		void OnRep_Quality();

	/**
	*BlueprintCallable，获取装备强化和星级的总数
	*
	*@return None
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Intensify")
		void GetIntensifySumStar(int32& SumIron, int32& SumCopper, int32& SumSilver, int32& SumGold);

	/**
	*BlueprintCallable，获取装备强化星级描述
	*
	*@return None
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Describe")
		FString GetStarDescribe();

	/**
	*BlueprintCallable，获取装备多条星级的图标描述
	*
	*@return None
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Describe")
		FString GetStarDesByLv(const EIntensifyLevel& StarLv, const int32& Num);

	/**
	*BlueprintCallable，获取描述中强化的总的强化百分比字符串
	*
	*@return None
	*/
	UFUNCTION(BlueprintCallable, Category = "Equip | Hardiness")
		FString GetIntensifyPercentStr(const int32& Precent);

	/**
	*虚函数，是否可以使用物品
	*
	*@return bool 可以使用物品返回TRUE，否则返回FALSE
	*/
	virtual bool IsCanUse() override;

	/**
	* 检测物品是否为装备
	*
	*@return bool 当前物品为装备返回true，否则为false
	*/
	virtual bool IsEquip() override;

	virtual FString GetItemName()override;
	/**
	*查询使用结果
	*
	*@param player 玩家
	*
	*@return int 使用结果
	*/
	virtual int UseQuery(AServerCharacter* player) override;

	///<获取属性描述，仅描述字符串，无显示相关转换
	UFUNCTION(BlueprintCallable, Category = "Equip | Describe")
	FString GetPropertyStrWithNoColor(const FString& propid, const FString& propvalue);

	/**
	*解析强化字符串
	*
	*/
	void ParseIntensifyStr();

	void ParseSingleIntensifyData(const FString DataStr, FIntensifyData& IntensifyData); ///<解析单条强化数据

	int32 GetHardiness_real();	///<获取耐久度真实当前值，和服务器一直，getHardiness为除以10000再向上取整的结果
	int32 GetHardinessMax_real();	///<获取耐久度真实最大值，和服务器一直，getHardinessMax为除以10000再向上取整的结果
	
	UFUNCTION(BlueprintCallable, Category = "Equip | Hardiness")
		float GetHardinessPercent_real();	///

	virtual void SetDynamicProperty(const int32& combatPowner, const FString& attackStr, const FString& attachStr, const FString& intensifyStr, const int32& hardiness) override;


public:	
	UFUNCTION(BlueprintPure, Category = "Intensify")
		FString GetIntensifyDes(const FString& IntensifyUID); ///<获取某一个强化数据属性描述
	UFUNCTION(BlueprintPure, Category = "Intensify")
		FIntensifyData GetIntensifyDataByUID(const FString& IntensifyUID);///<通过UID获取指定强化数据
	UFUNCTION(BlueprintCallable, Category = "Intensify")
		void GetSortIntensifyDatas(TArray<FIntensifyData>& SortDatas); ///《获取排序的强化数据
	UFUNCTION(BlueprintPure, Category = "Intensify")
		void GetIntensifyLvSection(TArray<int32>& LvSections); ///<获取可以强化的等级区间
	UFUNCTION(BlueprintPure, Category = "Intensify")
		int32 GetMaxIntensifyLv();///<获取装备强化的最高等级
	UFUNCTION(BlueprintPure, Category = "Intensify")
		int32 GetMaxLockNumByBackFair();///<获取装备回火最大锁星数量

	UFUNCTION(BlueprintPure, Category = "Intensify")
		int32 GetCurrIntensifyLv();	///<获取当前强化等级
	UFUNCTION(BlueprintPure, Category = "Intensify")
		FString GetIntensifySumPropertyStr(); ///<获取强化总计属性

	UFUNCTION(BlueprintPure, Category = "Intensify")
		int32 GetMaxLockNumBBiography();///<获取装备传星最大锁星数量

	
	FString GetIntensifyMainPropertyDes(const FString& IntensifyUID);	///<获取强化的主属性描述
	FString GetIntensifyAttachPropertyDes(const FString& IntensifyUID);		///<获取强化的附加属性描述

	TMap<FString, FString> ParsePropertiesToMap(const FString& PropertiesStr); ///<将属性字符串解析到TMap


	UFUNCTION(BlueprintPure, Category = "BackFire")
		int32 GetMaxLockNum();///<获取装备回火锁星上限
	UFUNCTION(BlueprintCallable, Category = "Intensify")
		bool IsCanBackFire();///<能否强化

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Equip | Property")
		FString AttackPropertiesStr;///<基础属性
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Equip | Property")
		FString AttachPropertiesStr;///<附加属性
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Equip | Property")
		FString IntensifyDataStr; ///<强化属性

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Equip | Property")
		int32 CombatPower; ///<战斗力

	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Equip | Property")
		int32 ModelPartType;///<装备位置

	UPROPERTY(BlueprintReadOnly, Category = "ItemBase | Intensify")
		TArray<FIntensifyData> IntensifyArray; ///<强化数据

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Equip | Property")
		int32 Hardiness;///<耐久度
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Equip | Property")
		int32 ReturnBackTime;///<可退货时间
};
