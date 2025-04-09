// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "ObjectMacros.h"
#include "GameData/CS3Object.h"
#include "GameData/ModelPartData.h"
#include "Guis/CS3TipsInfoWidget.h"
#include "TipsManager.generated.h"

/*
* 文件名称：TipsManager.h
* 功能说明：
* 文件作者：liyuxia
* 目前维护：liyuxia
* 创建时间：2017-06-27
*/

UENUM(BlueprintType)
enum class INFO_TIPS_TYPE : uint8
{
	TOOL_TIPS_TYPE	= 0 UMETA(DisplayName = "toolTips"),	///<普通信息
	ITEM_TIPS_TYPE	= 1 UMETA(DisplayName = "itemTips"),	///<物品信息
	EQUIP_TIPS_TYPE	= 2 UMETA(DisplayName = "equipTips"),	///<装备信息
	SKILL_TIPS_TYPE	= 3 UMETA(DisplayName = "skillTips"),	///<技能信息
	GOODS_TIPS_TYPE	= 4 UMETA(DisplayName = "goodsTips"),	///<商品信息
	BLUEPRINT_TIPS_TYPE = 5 UMETA(DisplayName = "blueprintTips"),			///<图纸信息
	EQUIPPART_TIPS_TYPE = 6 UMETA(DisplayName = "EquipPartTips"),			///<半成品装备信息
	BUFF_TIPS_TYPE = 7 UMETA(DisplayName = "buffTips"),		///<Buff信息
};

///Buff信息提示数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FBuffTipsData
{
	GENERATED_USTRUCT_BODY()

public:
	///<BuffID
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 BuffID;
	///<Buff名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString BuffName;
	///<BuffIcon
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TSoftObjectPtr<UTexture2D> BuffIcon;
	///<Buff等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 BuffLevel;
	///<Buff持续时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float HoldTime;
	///<Buff剩余时间
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float RemainTime;
	///<Buff开关条件
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString TargetActForbidDescribe;
	///描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString DescribeStr;
};

///装备信息提示数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FEquipTipsData
{
	GENERATED_USTRUCT_BODY()

public:
	///<装备名字 强化等级 富文本
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "name")
		FString Name;
	///<装备品质
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "quality")
		int32 Quality;
	///<装备图标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "icon")
		FString Icon;
	///<装备需要等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "repLevel")
		int32 RepLevel;
	///<装备需要境界等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "repJingJieLevel")
		int32 ReqJingJieLevel;
	///<装备耐久度 字符串
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "hardiness")
		FString Hardiness;
	///<装备所需职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Profession")
		TArray<int32> Profession;
	///<装备部位
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "partType")
		MODEL_PART_TYPE PartType;
	///<装备是否绑定
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "bindType")
		bool bIsBinded;
	///<装备数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "Amount")
		int32 Amount;
	///<装备战斗力
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "CombatPower")
		FString CombatPower;
	///装备星星富文本
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "starText")
		FString StarText;
	///装备基础属性富文本
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "baseProperty")
		FString BaseProperty;
	///装备附加属性富文本
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "baseAttachProperty")
		FString BaseAttachProperty;
	///装备强化附加属性富文本
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "intensifyProperty")
		FString IntensifyProperty;
	///装备套装属性富文本
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "suitProperty")
		FString SuitProperty;
	///装备单价
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "price")
		int32 Price;
	///描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite, DisplayName = "DescribeStr")
		FString DescribeStr;
};

///图纸信息提示数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FBlueprintTipsData
{
	GENERATED_USTRUCT_BODY()

public:
	///<图纸名字（残） 富文本
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Name;
	///<图纸属性（0:没有，1:冰，2:火，3:玄，4:雷）
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 SuitIndex;
	///<打造后的装备名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString EquipName;
	///<图纸品质
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Quality;
	///<图纸需要等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 RepLevel;
	///<图纸需要境界等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ReqJingJieLevel;
	///<图纸所需职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<int32> Profession;
	///<装备部位
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		MODEL_PART_TYPE PartType;
	///<图纸是否绑定
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsBinded;
	///<图纸数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Amount;
	///基础属性富文本
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString BaseProperty;
	///套装基础属性富文本
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString SuitBaseProperty;
	///套装附加属性富文本
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString SuitAttachProperty;
	///所需材料消耗
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Material;
	///初始打造成功率
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 SuccessRate;
	///增加的打造成功率
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		float AddRate;
	///描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString DescribeStr;
};

///半成品装备信息提示数据
USTRUCT(BlueprintType)
struct CHUANGSHI_API FEquipPartTipsData
{
	GENERATED_USTRUCT_BODY()

public:
	///<半成品装备名字 包含属性 富文本
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Name;
	///<半成品装备淬炼次数
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 QuenchingNum;
	///<半成品装备品质
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Quality;
	///<半成品装备图标
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString Icon;
	///<半成品装备等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Level;
	///<装备需要等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 RepLevel;
	///<装备需要境界等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 ReqJingJieLevel;
	///<装备所需职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<int32> Profession;
	///<装备部位
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		MODEL_PART_TYPE PartType;
	///<半成品装备是否绑定
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		bool bIsBinded;
	///<半成品装备数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Amount;
	///装备基础属性富文本
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString BaseProperty;
	///装备附加属性富文本
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString BaseAttachProperty;
	///装备套装属性富文本
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString SuitProperty;
	///装备单价
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Price;
	///描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString DescribeStr;
};

UCLASS(Blueprintable)
class CHUANGSHI_API UToolInfo :public UCS3Object
{
	GENERATED_BODY()

public:					
	/**
	*转义信息
	*
	*@param	InfoKeys 信息关键字
	*
	*@return 无
	*/
	virtual void InitFormatInfoTips(const FString& InfoKeys);

public:
	UPROPERTY(BlueprintReadOnly, Category = "ToolInfo")
		INFO_TIPS_TYPE TipsType;///<提示类型
	UPROPERTY(BlueprintReadOnly, Category = "ToolInfo")
		FString InfoTips;///<信息提示内容
};

UCLASS(BlueprintType)
class CHUANGSHI_API UItemInfo :public UToolInfo
{
	GENERATED_BODY()
public:
	virtual void InitFormatInfoTips(const FString& InfoKeys) override;///<转义信息,InfoKeys可传ItemID或者UID，尽量用UID，因为ItemID只能获得客户端定义的静态属性，服务器的动态属性，比如UID,数量，绑定类型传ItemID都是获取不到的
	void SetItemInfo( UItemBase* ItemBase);

public:
	///<物品UID
	UPROPERTY(BlueprintReadOnly, Category = "ItemInfo")
		FString ItemUId;
	///<物品名字富文本
	UPROPERTY(BlueprintReadOnly, Category = "ItemInfo")
		FString ItemNameInfo;
	///<物品品质
	UPROPERTY(BlueprintReadOnly, Category = "ItemInfo")
		int32 ItemQuality;
	///<物品图标
	UPROPERTY(BlueprintReadOnly, Category = "ItemInfo")
		FString ItemIcon;
	///<道具是否有效
	UPROPERTY(BlueprintReadOnly, Category = "ItemInfo")
		bool IsItemValid;
	///<ItemTipTitlePanel是否显示物品等级
	UPROPERTY(BlueprintReadOnly, Category = "ItemInfo")
		bool IsShowItemLevel;
	///<物品等级
	UPROPERTY(BlueprintReadOnly, Category = "ItemInfo")
		int32 ItemLevel;
	///<物品需要等级
	UPROPERTY(BlueprintReadOnly, Category = "ItemInfo")
		int32 ItemRepLevel;
	///<物品需要境界等级
	UPROPERTY(BlueprintReadOnly, Category = "ItemInfo")
		int32 ReqJingJieLevel;
	///<物品品类
	UPROPERTY(BlueprintReadOnly, Category = "ItemInfo")
		FString ItemType;
	///<物品所需职业
	UPROPERTY(BlueprintReadWrite, Category = "ItemInfo")
		TArray<int32> Profession;
	///<物品是否绑定
	UPROPERTY(BlueprintReadOnly, Category = "ItemInfo")
		bool ItemIsBinded;
	///<物品数量
	UPROPERTY(BlueprintReadOnly, Category = "ItemInfo")
		int32 Amount;
	///<物品单价
	UPROPERTY(BlueprintReadOnly, Category = "ItemInfo")
		int32 Price;
	///<物品使用次数富文本
	UPROPERTY(BlueprintReadOnly, Category = "ItemInfo")
		FString ItemUseNumberInfo;
	///<物品使用限量富文本
	UPROPERTY(BlueprintReadOnly, Category = "ItemInfo")
		FString ItemUseAmountInfo;
	///<物品使用期限
	UPROPERTY(BlueprintReadOnly, Category = "ItemInfo")
		FString ItemUseEndTimeInfo;
};

UCLASS(BlueprintType)
class CHUANGSHI_API UEquipInfo :public UToolInfo
{
	GENERATED_BODY()
public:
	virtual void InitFormatInfoTips(const FString& InfoKeys) override;///<转义信息，InfoKeys可传UID

	///<通过UID获得装备属性Data
	UFUNCTION(BlueprintPure, Category = "EquipInfo")
	FEquipTipsData GetEquipTipsDataByUId(const FString& UId);
	///<根据装备实例获得装备数据
	FEquipTipsData GetEquipTipsData( UItemBase* Equip );

public:
	///<装备UID
	UPROPERTY(BlueprintReadOnly, Category = "EquipInfo")
		FString EquipUId;
	///<装备数据
	UPROPERTY(BlueprintReadOnly, Category = "EquipInfo")
		FEquipTipsData EquipTipsData;
	///<玩家身上与该装备对应部位相同的装备UIDs
	UPROPERTY(BlueprintReadOnly, Category = "EquipInfo")
		TArray<FString> PlayerEquipUIds;
	///<装备属性对比富文本
	UPROPERTY(BlueprintReadOnly, Category = "EquipInfo")
		FString EquipPropertyCompare;

};

UCLASS(BlueprintType)
class CHUANGSHI_API USkillInfo :public UToolInfo
{
	GENERATED_BODY()
public:
	virtual void InitFormatInfoTips(const FString& InfoKeys) override;///<转义信息，InfoKeys可传技能ID

public:
	UPROPERTY(BlueprintReadOnly, Category = "SkillInfo")
		int32 SkillID;///<技能ID
};

UCLASS(BlueprintType)
class CHUANGSHI_API UBuffInfo :public UToolInfo
{
	GENERATED_BODY()
public:
	virtual void InitFormatInfoTips(const FString& InfoKeys) override;///<转义信息，InfoKeys可传技能ID

public:
	UPROPERTY(BlueprintReadOnly, Category = "BuffInfo")
		int32 BuffIndex;///<Buff索引（服务器标识）
	UPROPERTY(BlueprintReadOnly, Category = "BuffInfo")
		int32 BuffID;///<BuffID
	UPROPERTY(BlueprintReadOnly, Category = "BuffInfo")
		FBuffTipsData BuffTipsData;
};

UCLASS(BlueprintType)
class CHUANGSHI_API UGoodsInfo :public UToolInfo
{
	GENERATED_BODY()
public:
	virtual void InitFormatInfoTips(const FString& InfoKeys) override;///<转义信息

public:
	UPROPERTY(BlueprintReadOnly, Category = "GoodsID")
		FString GoodsID;///<商品ID

};

UCLASS(BlueprintType)
class CHUANGSHI_API UBlueprintInfo :public UToolInfo
{
	GENERATED_BODY()
public:
	virtual void InitFormatInfoTips(const FString& InfoKeys) override;///<转义信息，InfoKeys可传UID

private:
	void GetNameData(int32 SuitIndex, FString ItemName, int32 Quality, FString EquipName, FString& BlueprintName, FString& ComposeEquipName);
	FString GetItemName(FString SuitTitle, FString ItemName, int32 Quality);
	FString StrToColorStr(const FString& inputstr, const FString& colorstr, const FString& shadowcolor, const FString& shadowoffset);
	FString GetEquipName(FString SuitName, FString EquipName);
	FString GetMaterial(int32 SuitIndex, int32 EquipID);
public:
	///<图纸UID
	UPROPERTY(BlueprintReadOnly, Category = "BlueprintInfo")
		FString BlueprintUId;
	///<图纸数据
	UPROPERTY(BlueprintReadOnly, Category = "BlueprintInfo")
		FBlueprintTipsData BlueprintTipsData;

};

UCLASS(BlueprintType)
class CHUANGSHI_API UEquipPartInfo :public UToolInfo
{
	GENERATED_BODY()
public:
	virtual void InitFormatInfoTips(const FString& InfoKeys) override;///<转义信息，InfoKeys可传UID

public:
	///<半成品装备UID
	UPROPERTY(BlueprintReadOnly, Category = "EquipPartInfo")
		FString EquipPartUId;
	///<半成品装备数据
	UPROPERTY(BlueprintReadOnly, Category = "EquipPartInfo")
		FEquipPartTipsData EquipPartTipsData;
};

/**
* 文件名称：TipsManager.h
* 功能说明：鼠标移上信息提示管理类
* 涉及配置：
* 文件作者：liyuxia
* 创建时间：2017/7/21/14:09
* 更改记录:
*/

/**
信息提示管理类 : UTipsManager
*/
UCLASS(Blueprintable)
class CHUANGSHI_API UTipsManager : public UCS3Object
{
	GENERATED_BODY()
public:
	///构造函数
	UTipsManager();

	static UTipsManager* GetInstance();

	/**
	*BlueprintCallable，显示信息提示
	*
	*@param  TipsType	提示类型
	*@param  InfoKeys	提示关键字
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "TipsManager")
		void ShowInfoTips(INFO_TIPS_TYPE TipsType = INFO_TIPS_TYPE::TOOL_TIPS_TYPE, const FString& InfoKeys = TEXT(""));

	/**
	*BlueprintCallable，显示信息提示
	*
	*@param  ItemBase 物品实例（因为用的是UItemBase*所以传装备实例也可以，装备是继承ItemBase的）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "TipsManager")
		void ShowInfoTipsByItem(UItemBase* ItemBase);

	/**
	*BlueprintCallable，创建信息提示控件
	*
	*@param  widgetClass 信息提示控件类
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "TipsManager")
		UCS3TipsInfoWidget* CreateTipWidget(INFO_TIPS_TYPE TipsType);

private:
	/**
	*显示普通信息提示内容
	*
	*@param  info 普通信息提示类
	*
	*@return 无
	*/
	void ShowToolTips(const UToolInfo* info);

	/**
	*显示物品信息提示内容
	*
	*@param  info 物品信息提示类
	*
	*@return 无
	*/
	void ShowItemTips(const UItemInfo* info);
	/**
	*显示装备信息提示内容
	*
	*@param  info 装备信息提示类
	*
	*@return 无
	*/
	void ShowEquipTips(const UEquipInfo* info);
	/**
	*显示技能信息提示内容
	*
	*@param  info 技能信息提示类
	*
	*@return 无
	*/
	void ShowSkillTips(const USkillInfo* info);

	/**
	*显示Buff信息提示内容
	*
	*@param  info Buff信息提示类
	*
	*@return 无
	*/
	void ShowBuffTips(const UBuffInfo* info);

	/**
	*显示商品信息提示内容
	*
	*@param  info 商品信息提示类
	*
	*@return 无
	*/
	void ShowGoodsTips(const UGoodsInfo* info);
	/**
	*显示图纸信息提示内容
	*
	*@param  info 图纸信息提示类
	*
	*@return 无
	*/
	void ShowBlueprintTips(const UBlueprintInfo* info);

	/**
	*显示半成品装备信息提示内容
	*
	*@param  info 半成品装备信息提示类
	*
	*@return 无
	*/
	void ShowEquipPartTips(const UEquipPartInfo* info);

/*
private:
	static UTipsManager* Instance;*/

public:
	///<提示信息实例
	UPROPERTY(BlueprintReadOnly, Category = "TipsManager")
		UToolInfo* TipsInfoInst;
	///<普通信息提示
	UPROPERTY(BlueprintReadOnly, Category = "TipsManager")
		UCS3TipsInfoWidget* ToolInfoTips;
	///<物品信息提示
	UPROPERTY(BlueprintReadOnly, Category = "TipsManager")
		UCS3TipsInfoWidget* ItemInfoTips;
	///<装备信息提示
	UPROPERTY(BlueprintReadOnly, Category = "TipsManager")
		UCS3TipsInfoWidget* EquipInfoTips;
	///<商品信息提示
	UPROPERTY(BlueprintReadOnly, Category = "TipsManager")
		UCS3TipsInfoWidget* GoodsInfoTips;
	///<技能信息提示
	UPROPERTY(BlueprintReadOnly, Category = "TipsManager")
		UCS3TipsInfoWidget* SkillInfoTips;
	///<Buff信息提示
	UPROPERTY(BlueprintReadOnly, Category = "TipsManager")
		UCS3TipsInfoWidget* BuffInfoTips;
	///<图纸信息提示
	UPROPERTY(BlueprintReadOnly, Category = "TipsManager")
		UCS3TipsInfoWidget* BlueprintInfoTips;
	///<半成品装备信息提示
	UPROPERTY(BlueprintReadOnly, Category = "TipsManager")
		UCS3TipsInfoWidget* EquipPartInfoTips;
};