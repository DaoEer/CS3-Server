#pragma once
#include "GameData/CS3Object.h"
#include "GameData/Skill/QuickSkillData.h"
#include "QuickBarManager.generated.h"

/*
* 文件名称：QuickBarManager.h
* 功能说明：快捷栏管理类
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2020-07-19
*/

UCLASS(Blueprintable, BlueprintType)
class CHUANGSHI_API UQuickBarManager : public UCS3Object
{
	GENERATED_BODY()
		UQuickBarManager();
	~UQuickBarManager();

public:
	static UQuickBarManager* GetInstance();
	/**
	*初始化
	*
	*@return 无
	*/
	void Init();
	void onLeaveWorld();

	/**
	* BlueprintCallable，根据快捷栏Index位置获取快捷栏ITEM
	*
	* @param Page 快捷栏页（区分心法的，不是翻页）
	* @param Index 快捷栏位置
	*
	* @return FQB_ITEM 根据快捷栏Index位置获取快捷栏ITEM
	*/
	UFUNCTION(BlueprintCallable, Category = "QuickBarManager")
		FQB_ITEM GetQBItemByIndex(const int32& Page, const int32& Index);

	/**
	* BlueprintCallable，根据快捷栏QbID获取快捷栏ITEM
	*
	* @param QbID 技能ID或物品ID
	*
	* @return int32 快捷栏Index位置
	*/
	UFUNCTION(BlueprintCallable, Category = "QuickBarManager")
		int32 GetIndexByQBID(const int32& QbID);

	/**
	* BlueprintCallable，当前页索引值是否有快捷栏ITEM
	*
	* @param Index 当前页面相对索引值（0-9即1-10号位置）
	* @return 当前页索引值是否有快捷栏ITEM
	*/
	UFUNCTION(BlueprintCallable, Category = "QuickBarManager")
		bool HasQuickItemInIndex(int32 Index);

	/**
	* BlueprintCallable，获取当前页的第n个空快捷项索引值
	* @param EmptyIndex 第几个空格子（1-10）
	* @return 索引值
	*/
	UFUNCTION(BlueprintCallable, Category = "QuickBarManager")
		int32 GetQuickBarSlotIndex(int32 EmptyIndex = 1);

	/**
	* BlueprintCallable，获取第n个空快捷项索引值
	* @param page 页数（0-2）
	* @param minIndex 格子索引（第一页0-9，第二页10-19，第三页20-29）
	* @param maxIndex 格子索引（第一页0-9，第二页10-19，第三页20-29）
	* @param EmptyIndex 第几个空格子（1-10）
	* @return 索引值
	*/
	UFUNCTION(BlueprintCallable, Category = "QuickBarManager")
		int32 GetQuickBarMinIndex(int32 page, int32 minIndex, int32 maxIndex, int32 EmptyIndex);

	//获取当前心法的所有技能
	UFUNCTION(BlueprintCallable, Category = "QuickBarManager")
		TArray<FQB_ITEM> GetQbItemList();

	//获取快捷栏翻页当前页面索引（0-2）
	UFUNCTION(BlueprintPure, Category = "QuickBarManager")
		int32 GetCurPage();

	/**
	* BlueprintCallable 设置快捷栏当前页面索引
	*
	* @param CurPage 当前页面索引（0-2即1-3页）
	* @return
	*/
	UFUNCTION(BlueprintCallable, Category = "QuickBarManager")
		void SetQuickBarCurPage(int32 InCurPage);

	/**
	* BlueprintCallable 设置额外快捷栏当前页面索引
	*
	* @param ExtCurPage 当前页面索引（3-5即1-3页）
	* @return
	*/
	UFUNCTION(BlueprintCallable, Category = "QuickBarManager")
		void SetQuickBarExtCurPage1(int32 InCurPage);

	/**
	* BlueprintCallable 设置额外快捷栏当前页面索引
	*
	* @param ExtCurPage 当前页面索引（6-8即1-3页）
	* @return
	*/
	UFUNCTION(BlueprintCallable, Category = "QuickBarManager")
		void SetQuickBarExtCurPage2(int32 InCurPage);

	/**
	* 更新快捷栏Item，修改QbItemList数据
	*
	* @param Index 快捷栏位置
	* @param QbType 快捷栏类型
	* @param Id 快捷栏ID
	* @param BindType 快捷栏绑定类型
	* @param Page 快捷栏页（区分心法的，不是翻页）
	* @param QuickID 容器ID
	* @return 无
	*/
	void OnUpdateQBItem(int32 Index, int32 QbType, int32 Id, int32 BindType, int32 Page, int32 QuickID, FString PetUid);
	/**
	* 移除快捷栏Index位置的Item，删除QbItemList数据
	*
	* @param Index 快捷栏位置
	* @param Page 快捷栏页（区分心法的，不是翻页）
	*
	* @return 无
	*/
	void OnRemoveQBItem(int32 Page, int32 Index);

#pragma region	/** 替换快捷栏 */
	
	//获取替换快捷栏技能
	UFUNCTION(BlueprintPure, Category = "QuickBarManager")
		TArray<FQB_ITEM> GetReplaceQbItemList();

	/**
	* 增加替换快捷栏数据
	*
	* @param Index 快捷栏位置
	* @param QbType 快捷栏类型
	* @param Id 快捷栏ID
	* @param BindType 快捷栏绑定类型
	* @param QuickID 容器ID
	* @param PetUid 幻兽UID
	*
	* @return 无
	*/
	void AddReplaceQBItem(int32 Index, int32 QbType, int32 Id, int32 BindType, int32 QuickID, FString PetUid = "");

	/**
	* 删除替换快捷栏
	*
	* @return 无
	*/
	void RemoveReplaceQBItem();

	/**
	* 获取替换快捷栏长度
	*
	* @return 无
	*/
	int32 GetReplaceQBItemLen();

	/**
	* 设置是否替换快捷栏
	*
	* @return 无
	*/
	void SetIsReplaceQb(bool IsReplaceQb);

#pragma endregion

	/*
	*播放技能时调用
	*/
	void OnPlaySkill(int32 SkillID);

	/*
	*增加玩家身上被动技能持有效果
	*/
	void AddPassiveHoldEffectData(int32 QuickID, int32 PassiveSkillLevel, int32 SkillLevel);

	/*
	*删除玩家身上被动技能持有效果
	*/
	void RemovePassiveHoldEffectData(int32 QuickID, int32 PassiveSkillLevel, int32 SkillLevel);

private:
	/**
	*加载配置表
	*
	*@return 无
	*/
	void LoadCfg();

	//判断是否需要更新快捷栏界面
	bool IsNeedUpdateQuickBar(int32 PosturePage);

	//通知UI更新
	void OnUpdateQBItemUI(FQB_ITEM QBItem);

	//组合数据成结构体
	FQB_ITEM InitQuickItem(int32 Index, int32 QbType, int32 Id, int32 BindType, int32 QuickID, FString PetUid);

	//根据QuickID获取技能切换配置数据
	FQUICKSKILL_CONFIG GetQuickSkillCfgData(int32 QuickID, bool& IsSuccess);

	/**
	* 获取等级切换后的技能ID
	* @param QuickID 容器ID
	* @param SkillID 原技能ID
	* @param QuickData 技能切换配置数据
	* @return 技能ID
	*/
	int32 GetLevelSwitchSkillID(int32 QuickID, int32 SkillID, TArray<FQUICKSKIL_SWITCH_DATA> QuickSkillData);

	/**
	* 获取玩家身上被动技能持有效果
	* @param QuickID 容器ID
	* @return PassiveSkillLevel 被动技能进阶等级， SkillLevel 主动技能进阶等级
	*/
	void GetPassiveHoldEffect(int32 QuickID, int32& PassiveSkillLevel, int32& SkillLevel);

	/**
	* 更新等级切换后的技能ID（增加或删除 被动技能持有进阶效果时调用）
	* @param QuickID 容器ID
	* @return 无
	*/
	void UpdateLevelSwitchSkillID(int32 QuickID);

#pragma region	/** 连携技能 */

	//是否有连携技能
	bool HasStageSkill();

	//更新技能持续时间（增加、删除）
	void UpdateQuickSkillHoldTime();
	/**
	* 启动CD计时器
	* @param TimeRemaining CD时间
	* @return 无
	*/
	void StartCdTimer();

	//CD计时器
	void SetCd();

	//停止CD计时器
	void StopCdTimer();

	//CD计时器中
	bool IsCoolDowning();

	/**
	* 切换到下一阶段技能
	* @param SkillID 释放的技能
	* @return 无
	*/
	void SwitchNextSkillStage(int32 SkillID);

#pragma endregion

public:
	///<是否替换快捷栏
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "QuickBarManager")
		bool IsReplace;

	///<额外快捷栏翻页当前页面索引（3-5）
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "QuickBarManager")
		int32 ExtCurPage_1;

	///<额外快捷栏翻页当前页面索引（6-8）
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "QuickBarManager")
		int32 ExtCurPage_2;

private:
	///<快捷技能配置数据
	TMap<int32, FQUICKSKILL_CONFIG> QuickSkillTableData; ///<key:QuickID，value:配置数据
	FTimerHandle CdTimerHandle;///<CD计时器
	bool HasCD; ///<当前是否在CD计时中

	int32 CurPage;
	TMap<int32, TArray<FQB_ITEM>> QbItemLists;  ///<快捷栏数据 key:心法类型，value:技能数据
	TArray<FQB_ITEM> ReplaceQbItemList;	///<替换快捷栏数据

	TMap<int32, FQB_ITEM> RemoveStageQbItems;  ///<Remove快捷栏技能时保存处于连携中的连携技能数据 key:容器ID，value:技能数据

	TMap<int32, FSKILL_PASSIVE_HOLD_EFFECT_DATA> SkillPassiveHoldEffectDatas;///< 被动技能持有进阶效果 QuickID:效果数据
};
