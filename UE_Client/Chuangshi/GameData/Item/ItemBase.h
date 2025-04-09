// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "Object.h"
#include "GameData/CS3Object.h"
#include "GameData/Item/ItemInfo.h"
#include "GameData/Item/ItemEnum.h"
#include "ItemBase.generated.h"

/**
* 文件名称：ItemBase.h
* 功能说明：
* 文件作者：lizhenghui
* 目前维护：chendongyong
* 创建时间：2016-11-16
*/

/**
 * 物品类
 */


DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FItemInfoChangeDelegate, FString, UID, int32, ItemOrder);

UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UItemBase : public UCS3Object
{
	GENERATED_BODY()

public:
	virtual void InitDynamicDataForJson(FString jsonStr);

	UFUNCTION(BlueprintImplementableEvent, Category = "ItemBase")
		void OnRep_DynamicProperty();///< 蓝图重写，临时存储数据

	/**
	*BlueprintCallable，初始化物品动态数据
	*
	*@param uidstr UID
	*@param num 数量
	*@param iconstr 图标
	*@param isbinded 是否绑定
	*@param name 物品名
	*@param order 物品格位置
	*
	*@return UItemBase 物品类对象
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		UItemBase* InitData(const FString& uidstr, int32 num, int32 isbinded, int32 order);

	//--------------------------------------------check-----------------------------------
	/**
	*BlueprintCallable，物品是否显示“NEW”样式
	*
	*@return bool 显示返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		virtual bool IsShowNew();

	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		void RecordOpertation();

	/**
	*BlueprintCallable，检测物品是否正在使用
	*
	*@return bool 当前正在使用返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		virtual bool IsUsing() { return false; }

	/**
	*BlueprintCallable，检测物品是否可以使用
	*
	*@return bool 当前能使用返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		virtual bool IsCanUse();

	/**
	*BlueprintCallable，检测物品是否为装备
	*
	*@return bool 当前物品为装备返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		virtual bool IsEquip();

	/**
	*BlueprintCallable，根据当前角色职业是否可以使用这个物品
	*
	*@param character 角色
	*
	*@return bool 当前角色可以使用这个物品返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		virtual bool CheckReqClass(AServerCharacter* character);

	/**
	*BlueprintCallable，根据当前角色等级是否可以使用这个物品
	*
	*@param character 角色
	*
	*@return bool 当前角色可以使用这个物品返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool CheckLevel(AServerCharacter* character);

	/**
	*BlueprintCallable，根据当前角色境界等级是否可以使用这个物品
	*
	*@param character 角色
	*
	*@return bool 当前角色可以使用这个物品返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool CheckJingjieLevel(AServerCharacter* character);

	/**
	*BlueprintCallable，是否可以叠加amount的数量
	*
	*@param num 物品数量
	*
	*@return bool 可以叠加amount的数量返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool IsCanStack(int32 num);

	///是否是某个物品大类
	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool CheckItemType(int32 _type);

	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		int32 GetType() { return ItemType; };
	
	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool IsWhite(); ///<物品是否白色

	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool IsBlue();///<物品是否蓝色

	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool IsGold();///<物品是否金色

	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool IsPink();///<物品是否粉色

	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool IsGreen();///<物品是否绿色

	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool IsGreenDi();///<物品是否地阶绿色

	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool IsGreenTian();///<物品是否天阶绿色

	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool IsGreenSheng();///<物品是否圣阶绿色


	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool IsCanSell();///<物品能否出售

	///能否销毁
	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool IsCanDestory();

	///物品能否拖到快捷栏
	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool IsCanDragToQB();

	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool IsNonDestructive();///<是否不可毁损

	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool IsUnique();///<是否唯一

	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool HasLimitTakeAmount();///<是否有携带限制

	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		virtual bool IsBinded();///<是否绑定

	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool isQuest();///<是否是任务物品

	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		bool isSpar();///<是否是晶核

	/**
	*BlueprintCallable，获取能使用物品的职业列表
	*
	*@return TArray<int32> 物品的职业列表
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		TArray<int32> GetReqClasses();

	UFUNCTION(BlueprintCallable, Category = "ItemBase")
		virtual void SetDynamicProperty(const int32& combatPowner, const FString& attackStr, const FString& attachStr, const FString& intensifyStr, const int32& hardiness);

	//--------------------------------------------describe-------------------------------
	/**
	*BlueprintCallable，获取物品名字
	*
	*@return FString 物品名字
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase | Describe")
		virtual FString GetItemName();

	/**
	*BlueprintCallable，获取物品类型的描述
	*
	*@return FString 物品类型
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase | Describe")
		FString GetTypeStr();

	/**
	*BlueprintCallable，获取根据插件格式显示物品总价的字符串
	*
	*@return FString 物品总价字符串
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase | Describe")
		FString GetPriceStr();

	/**
	*BlueprintCallable，获取根据插件格式显示物品等级的字符串
	*
	*@return FString 物品等级字符串
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase | Describe")
		FString GetLevelStr();

	/**
	*BlueprintCallable，获取根据插件格式显示物品描述的字符串
	*
	*@return FString 物品描述字符串
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase | Describe")
		FString GetDescribeStr();

	/**
	*BlueprintCallable，获取根据插件格式显示物品携带数量的字符串
	*
	*@return FString 格式化后的物品携带数量字符串
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase | Describe")
		FString GetTakeStr();

	/**
	*BlueprintCallable，获取根据插件格式显示物品累加次数（叠加、次数、充能）的字符串
	*
	*@return FString 格式化后的物品使用次数字符串
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase | Describe")
		FString GetUseNumberStr();

	/**
	*BlueprintCallable，获取根据插件格式显示物品使用限量的字符串
	*
	*@return FString 格式化后的物品使用限量字符串
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase | Describe")
		FString GetUseAmountStr();

	/**
	*BlueprintCallable，按插件格式化字符串
	*
	*@param inputstr 要格式化的字符串
	*@param colorstr 字体颜色
	*@param shadowcolor 字体阴影颜色
	*@param shadowoffset 字体阴影像素
	*
	*@return FString 按插件格式化后的字符串
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase | Describe")
		FString StrToColorStr(const FString& inputstr, const FString& colorstr, const FString& shadowcolor, const FString& shadowoffset);

	//无换行的转换
	UFUNCTION(BlueprintCallable, Category = "ItemBase | Describe")
		FString StrToColorStrWithoutBr(const FString& inputstr, const FString& colorstr, const FString& shadowcolor, const FString& shadowoffset);

	FString GetPrice();///<根据插件格式将物品单价转换成图文混排的字符串

	//--------------------------------------------Match-------------------------------
	/**
	*BlueprintCallable，professions列表是否与能使用物品的职业匹配
	*
	*@param professions 与物品职业匹配的职业数据
	*
	*@return bool 匹配成功返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase | Match")
		bool IsMatchClasses(TArray<int32> professions);

	/**
	*BlueprintCallable，modelparts列表是否与装备的模型类型匹配
	*
	*@param modelparts 要比较的模型类型数据
	*
	*@return bool 匹配成功返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase | Match")
		bool IsMatchEquipParts(TArray<int32> modelparts);

	/**
	*BlueprintCallable，levels列表是否与能使用物品的等级匹配
	*
	*@param levels 要比较的等级数据
	*
	*@return bool 匹配成功返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase | Match")
		bool IsMatchLevels(TArray<int32> levels);

	/**
	*BlueprintCallable，qualities列表是否与物品的品质匹配
	*
	*@param levels 要比较的品质数据
	*
	*@return bool 匹配成功返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase | Match")
		bool IsMatchQualities(TArray<int32> qualities);

	//--------------------------------------------CD-------------------------------
	/**
	*BlueprintCallable，判断物品是否在使用CD中
	*
	*@return bool 在使用CD返回true，否则为false
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase | CD")
		virtual bool IsCoolDowning();

	/**
	*BlueprintCallable，获取物品在CD中的剩余CD时间
	*
	*@return float 物品使用CD中，剩余CD时间
	*/
	UFUNCTION(BlueprintCallable, Category = "ItemBase | CD")
		virtual float GetCDRemainningTime();


	UFUNCTION(BlueprintCallable, Category = "ItemBase | CD")
		virtual float GetCDPersistTime();

	virtual void SetCDPersistTime(float PersistTime);

	//--------------------------------------------OnRep-------------------------------
	UFUNCTION(BlueprintCallable, Category = "Notify")
		void OnRep_Amount();///< 蓝图可调用，更新物品数量

	UFUNCTION(BlueprintCallable, Category = "Notify")
		void OnRep_BindType();///< 蓝图可调用，更新物品的绑定

	UFUNCTION(BlueprintCallable, Category = "Notify")
		void UpdateBagGrid();///< 蓝图可调用，更新背包/装备/仓库等玩家身上的物品格

	UFUNCTION(BlueprintCallable, Category = "Notify")
		void UpdateQuickBar();///< 蓝图可调用，更新快捷栏物品数量

	//--------------------------------------------Delegate-------------------------------
	/**
	*BlueprintAssignable，物品消息改变消息通知
	*
	*@param UID 物品UID
	*@param ItemOrder 物品在物品格中的位置
	*
	*@return FItemInfoChangeDelegate 物品消息改变消息
	*/
	UPROPERTY(BlueprintAssignable)
		FItemInfoChangeDelegate OnItemInfoChange;

private:
	
	TMap<int32, FString> IntensifyDatas;	///<当前强化数据
	TMap<int32, FString> SaveIntensifyDatas;	///<保存强化数据

	bool IsMatch(const TSet<int32>& src, const TSet<int32>& dst);///<判断两个集合是否有交集

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		FString DynamicProperty;	///<仅供临时存储数据
	///物品限时
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		FString ItemEndTime;

	//--------------------------------------------------------------------------
	// Basic Property
	//--------------------------------------------------------------------------
	///物品ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 ItemID = 0;
	///物品在物品格中的位置
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 ItemOrder = 0;
	///物品数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 Amount = 0;
	///物品绑定类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 BindType = 0;
	///物品UID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		FString UID;
	///物品图标
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		FString Icon;
	///物品名字
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		FString ItemName;
	///物品类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 ItemType = 0;
	///物品服务器的脚本名
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		FString Script;
	///物品拾取类型
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 PickupType = 0;
	///物品等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 Level = 0;
	///物品品质
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 Quality = 0;
	///物品单价
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 Price = 0;
	///物品描述
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		FString Describe;
	///物品是否可以出售
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 CanSell = 0;
	///物品是否可以销毁
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 CanDestroy = 0;
	///物品是否可以拖到快捷栏
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 CanDragToQB = 0;
	///物品可使用的职业
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		FString ReqClasses;
	///物品可使用的等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 ReqLevel = 0;
	///物品可使用的境界等级
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 ReqJingJieLevel = 0;
	///累加类型（@CST-4375）
	///	0：不可叠加
	///	1：可叠加
	///	2：可计次
	///	3：可充能
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 OverlyingType = 0;
	///物品可累加的数量（叠加、计数、充能）
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 OverlyingMax = 0;
	///是否显示数量提示
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		bool CanShowOverlying = 0;
	///物品最大携带数量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 MaxTakeAmount = 0;
	///物品的技能ID
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 SkillID = 0;
	///物品出售之后是否可以回购
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		int32 CanReturn = 0;
	///使用限量
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		FString UseAmount;
	///根据具体脚本解析参数，备用
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		FString Param1;
	///根据具体脚本解析参数，备用
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		FString Param2;
	///根据具体脚本解析参数，备用
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		FString Param3;
	///根据具体脚本解析参数，备用
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		FString Param4;
	///根据具体脚本解析参数，备用
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "ItemBase")
		FString Param5;

};
