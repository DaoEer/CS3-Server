#pragma once
#include "Blueprint/UserWidget.h"
#include "CS3Base/CS3UserWidget.h"
#include "CS3TipsInfoWidget.generated.h"

/*
* 文件名称：TipsInfoWidget.h
* 功能说明：
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2019-01-03
*/

class UTipsManager;

UCLASS(BlueprintType)
class CHUANGSHI_API UCS3TipsInfoWidget : public UCS3UserWidget
{
	GENERATED_BODY()
public:

	/**
	*BlueprintNativeEvent，初始化
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "CS3TipsInfoWidget")
		void InitInfo();

	/**
	*BlueprintNativeEvent，显示普通信息提示内容
	*
	*@param  Infos 普通信息提示类
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "CS3TipsInfoWidget")
		void ShowToolTips(const FString& Infos);

	/**
	*BlueprintNativeEvent，显示物品信息提示内容
	*
	*@param  ItemInfo 物品信息提示类
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "CS3TipsInfoWidget")
		void ShowItemInfo(const UItemInfo* ItemInfo);

	/**
	*BlueprintNativeEvent，显示装备信息提示内容
	*
	*@param  EquipInfo 装备信息提示类
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "CS3TipsInfoWidget")
		void ShowEquipInfo(const UEquipInfo* EquipInfo);

	/**
	*BlueprintNativeEvent，显示商品信息提示内容
	*
	*@param  GoodsInfo 商品信息提示类
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "CS3TipsInfoWidget")
		void ShowGoodsInfo(const UGoodsInfo* GoodsInfo);


	/**
	*BlueprintNativeEvent，显示技能信息提示内容
	*
	*@param  GoodsInfo 技能信息提示类
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "CS3TipsInfoWidget")
		void ShowSkillInfo(const USkillInfo* SkillInfo);

	/**
	*BlueprintNativeEvent，显示Buff信息提示内容
	*
	*@param  BuffInfo Buff信息提示类
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "CS3TipsInfoWidget")
		void ShowBuffInfo(const UBuffInfo* BuffInfo);

	/**
	*BlueprintNativeEvent，显示图纸信息提示内容
	*
	*@param  EquipInfo 图纸信息提示类
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "CS3TipsInfoWidget")
		void ShowBlueprintInfo(const UBlueprintInfo* BlueprintInfo);

	/**
	*BlueprintNativeEvent，显示半成品装备信息提示内容
	*
	*@param  EquipInfo 半成品装备信息提示类
	*
	*@return 无
	*/
	UFUNCTION(BlueprintNativeEvent, Category = "CS3TipsInfoWidget")
		void ShowEquipPartInfo(const UEquipPartInfo* EquipPartInfo);
};