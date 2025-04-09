// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CS3Object.h"
#include "Blueprint/UserWidget.h"
#include "GameData/TutorialData.h"
#include "CS3Base/BaseWindow.h"
#include "TutorialManager.generated.h"

/*
* 文件名称：TutorialManager.h
* 功能说明：指引提示管理器
* 文件作者：lizhenghui
* 目前维护：zhangdan
* 创建时间：2017-11-1
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FTutorialMap
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(BlueprintReadWrite)
		TMap<FName, FTUTORIALDATA> Datas;
};

/**
* 一个指引的多个控件
*/
USTRUCT()
struct CHUANGSHI_API FWndList
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY()
	TArray<UUserWidget*> ShowWndList;
};


UCLASS(BlueprintType)
class CHUANGSHI_API UTutorialManager : public UCS3Object, public FTickableGameObject
{
	GENERATED_BODY()
public:
	static UTutorialManager* GetInstance();

	///加载配置
	void LoadCfg();

	FTUTORIALDATA GetTutorialDataByKeyIndex(FName KeyIndex, bool& IsSuccess);

	///删除仅能触发一次（并且已经触 过）的事件
	void ClearDoOnceEvents(TArray<FString> Indexs);

	/**
	*通过控件路径字符串获得控件对象
	*
	*@param	WidgetPath 控件路径字符串，确定的路径
	*以.分隔，格式为 窗口ID.[引用 的外部UMG的控件名称]，例如：60008.bottom.dungeonPanel.dungeonBonusPanel.challengeBtn
	*
	*@return UWidget* 控件对象
	*/
	UFUNCTION(BlueprintCallable, Category = "TutorialManager")
		UWidget* GetWidgetFromWidgetPath(int32 UIType, const FString& WidgetPath);

	/**
	*通过控件路径字符串获得控件对象的父窗口
	*
	*@param	WidgetPath 控件路径字符串
	*以.分隔，格式为 窗口ID.[引用 的外部UMG的控件名称]
	*
	*@return UWidget* 控件对象的父窗口
	*/
	UFUNCTION(BlueprintCallable, Category = "TutorialManager")
		UBaseWindow* GetParentWindowFromWidgetPath(const FString& WidgetPath);

	/**
	*获取控件在父窗口上的位置
	*
	*@param	WidgetPath 控件路径字符串
	*
	*@return FVector2D 控件在父窗口上的位置
	*/
	UFUNCTION(BlueprintCallable, Category = "TutorialManager")
		FVector2D GetWidgetPosition(int32 UIType, const FString& WidgetPath);
	/**
	*获取控件在RootUI上的位置
	*
	*@param	WidgetPath 控件路径字符串
	*
	*@return FVector2D 控件在RootUI上的位置
	*/
	UFUNCTION(BlueprintCallable, Category = "TutorialManager")
		FVector2D GetWidgetPositionInRootUI(int32 UIType, const FString& WidgetPath);
	/**
	*获取控件在视口上的位置
	*
	*@param	WidgetPath 控件路径字符串
	*
	*@return FVector2D 控件在视口上的位置
	*/
	UFUNCTION(BlueprintCallable, Category = "TutorialManager")
		FVector2D GetWidgetPositionInViewport(int32 UIType, const FString& WidgetPath);

	/**
	*获取控件Size
	*
	*@param	WidgetPath 控件路径字符串
	*
	*@return FVector2D 控件Size
	*/
	UFUNCTION(BlueprintCallable, Category = "TutorialManager")
		FVector2D GetWidgetSize(int32 UIType, const FString& WidgetPath);

	/**
	*根据箭头方向来确定显示最终方向
	*
	*@param	Pos  目标Positon
	*@param	Size 目标Size
	*@param	WidgetSize 指引Size
	*@param	ArrowType 箭头指引类型
	*
	*@return FVector2D 指引Positon
	*/
	FVector2D GetFilterPos(const FVector2D& Pos, const FVector2D& Size, const FVector2D& WidgetSize, EARROWTYPE ArrowType);

	/**
	*根据箭头方向和是否显示文字框来确定显示尺寸
	*
	*@param	IsShowBox  指引是否显示文字框
	*@param	ArrowType 箭头指引类型
	*
	*@return FVector2D 指引Size
	*/
	FVector2D GetFilterSize(FString IsShowBox, EARROWTYPE ArrowType);

	/**
	*根据FString配置获得箭头方向类型
	*
	*@param	ArrowType  箭头指引类型配置
	*
	*@return EARROWTYPE 箭头指引类型
	*/
	EARROWTYPE GetArrowType(FString ArrowType);

	/**
	*根据箭头指引类型获得蓝图类
	*
	*@param	EARROWTYPE  箭头指引类型
	*
	*@return FString 指引Size
	*/
	UUserWidget* CreateArrowTutorialWidget(EARROWTYPE ArrowType);

	/**
	*指引目标被点击
	*
	*@return 无
	*/
	void OnTriggerItemClicked();
	/**
	*某步指引完成，进行下一步
	*
	*@param	TutorialType  指引类型（ETUTORIAL_TYPE）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "TutorialManager")
		void FinishCurrStep(int32 TutorialType = 1);
	/**
	*直接完成整条指引所有步骤，并进行下一条等待指引
	*
	*@param	TutorialType  指引类型（ETUTORIAL_TYPE）
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "TutorialManager")
		void FinishAllStep(int32 TutorialType = 1);
	/**
	*根据路径字符串获取资源
	*
	*@return UObject*
	*/
	UFUNCTION(BlueprintCallable, Category = "TutorialManager")
		UObject* GetObjectByPath(FString Path);

	/**
	*箭头指引
	*ActParams的
	Param1是是否显示锁定框,0表示不显示，1表示显示
	Param2是箭头方向
	Param3是标题
	Param4是内容
	*
	*/
	void DoArrowAction(const FTUTORIALPARAM& ActParams);

	/**
	*各种条件下触发指引提示
	*
	*@param	TriggerType 提示类型
	*@param Param1 提示所用参数一，根据提示类型自行解析
	*@param Param2 提示所用参数二，根据提示类型自行解析
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "TutorialManager")
	void OnTrigger(ETUTORIALTRIGGERTYPE TriggerType, const FString& Param1, const FString& Param2);

	///存储显示的指引界面
	void AddShowTriggerWnd(const FName& Index, UUserWidget* ShowWidget);

	///显示指引
	void DoAction(const FName& KeyIndex, const int32& TutorialType, const float& DelayTime, const FString& Param1, const FString& Param2);
	
	///播放语音
	void PlayVoice(FString VoiceIds, FName KeyIndex, bool IsAutoNextStep = false);

	///设置当前箭头指引数据
	void SetCurrentShowArrowData(const FName& KeyIndex, const FTUTORIALPARAM& ActParams);
	///设置当前图片指引数据
	void SetCurrentShowImageData(const FName& KeyIndex, const FTUTORIALPARAM& ActParams);
	///设置当前消息提示指引数据
	void SetCurrentShowMessageData(const FName& KeyIndex, const FTUTORIALPARAM& ActParams);

	///是否有正在显示的箭头指引
	bool HasArrowTutorial();
	///是否有正在显示的图片指引
	bool HasImageTutorial();
	///是否有正在显示的消息提示指引指引
	bool HasMessageTutorial();

	///隐藏当前显示的箭头指引
	void HideCurrentArrowTutorial();
	///隐藏当前显示的图片指引
	void HideCurrentImageTutorial();
	///隐藏当前显示的消息提示指引
	void HideCurrentMessageTutorial();

	/**
	*当分辨率改变时被调用
	*
	*@param preReso 旧分辨率
	*@param PreScale 旧缩放比
	*@param NewReso 新分辨率
	*
	*@return 无
	*/
	void OnResolutionChanged(FVector2D preReso, float PreScale, FVector2D NewReso);
	void OnChangeMyRoleLevel(int32 Level);
	///改变任务状态
	void OnChangeQuestState(int32 QuestID);
	///子任务状态改变
	void OnUpdateQuestTaskState(int32 QuestID, int32 TaskID);
	///技能可升级
	void OnSkillCanUpgrate(int32 SkillID, int32 index);
	///首次学习技能
	void OnFirstLearnSkill(int32 SkillID);
	///获得物品
	void OnAddItem(FString UID);
	///获得Buff
	void OnAddBuff(int32 BuffID);
	/*
	*背包删除物品时调用
	*需求：通过打开背包对当前已在界面显示或等待队列中的物品，进行操作（丢弃、出售、放入仓库、打开物品），关闭界面
	*逻辑实质：所有操作都有一个共同点，就是 物品从背包移除
	*/
	void OnRemoveItem(FString ItemUID);
	/*
	*穿戴装备时调用
	*需求：通过打开背包对当前已在界面显示或等待队列中的物品，进行操作（穿戴），关闭界面
	*/
	void OnUseEquip(FString ItemUID);
	/**
	* 增加快捷栏QbItem时调用
	*需求：如有增加的这个QbItem的指引，则完成这条指引
	*/
	void OnAddQBItem(int32 QbID);
	/**
	* 移除快捷栏QbItem时调用
	*需求：如有删除的这个QbItem的指引，则完成这条指引
	*/
	void OnRemoveQBItem(int32 QbID);
	/*
	*播放技能时调用
	*需求：播放技能时，关闭指引对应界面
	*/
	void OnPlaySkill(int32 SkillID);

	void OnVoiceComplete(FString AudioID);

	void OnOpenWindow(FString WindowType);

	void OnEnterWorld();            ///< 当Entity进入世界时，此方法被调用
	void OnLeaveWorld();            ///< 当Entity离开世界（被销毁时）时，此方法被调用

protected:
	//FTickableGameObject implement
	virtual TStatId GetStatId() const override { RETURN_QUICK_DECLARE_CYCLE_STAT(UTutorialManager, STATGROUP_Tickables); }
	virtual bool IsTickable() const override;
	virtual void Tick(float DeltaTime) override;

private:
	///在角色返回登录或角色选择时清空数据
	void ClearData();

	/**
	*通过控件路径字符串获得控件对象
	*
	*@param	WidgetPath 控件路径字符串，确定的路径
	*以.分隔，格式为 窗口ID.[引用 的外部UMG的控件名称]，例如：79.PetInfoPanel.BattleBtn
	*
	*@return UWidget* 控件对象
	*/
	UWidget* GetWidgetFromAccurateWidgetPath(const FString& WidgetPath);
	/**
	*通过控件路径字符串获得控件对象
	*
	*@param	WidgetPath 控件路径字符串，动态UI路径
	*以.分隔，格式为 窗口ID.物品ID（装备ID等），例如：8.204010002
	*
	*@return UWidget* 控件对象
	*/
	UWidget* GetWidgetFromDynamicWidgetPath(const FString& WidgetPath);
	/**
	*根据指引的目标的路径配置参数拼凑控件名
	*因为为了保持控件名唯一性，在ID前面增加了一些限制字符串，
	*但为了配置简便，配置时只配置ID，在程序中进行拼接
	*
	*@param	RootWindow 窗口界面
	*@param	WidgetPath 控件路径
	*@param	Index 控件路径中第几个控件名
	*
	*@return FString 控件名
	*/
	FString AppendWidgetName(UBaseWindow* RootWindow, const FString& WidgetPath, int32 Index);

	///当前鼠标点击是否在某个区域内
	bool CheckInArea(FVector2D LeftTopPos, FVector2D RightBottomPos);
	///由于条件改变造成指引条件不符，检查能关闭的指引并关闭
	void CheckAndCloseTutorial(const FString& Param1, UClass* CloseCndClass = nullptr);

	/**
	*检查界面是否打开（可检测多个）
	*
	*@param	WidgetPath 控件路径字符串
	*WidgetPath格式为 UIType|UILinkTarget，UIType|UILinkTarget
	*例如 2|102.202010001,2|102.202010012
	*
	*@return 无
	*/
	void CheckPanelOpen(const FString& WidgetPath);
	void ShowPanelArrowAction();

	///延迟0.1秒触发，是由于目前使用的GetCachedGeometry在刚创建时数据是无效的
	void DelayTrigger(ETUTORIALTRIGGERTYPE TriggerType, const FString& Param1, const FString& Param2);
	///触发装备替换指引
	void OnTriggerUpdateEquip(ETUTORIALTRIGGERTYPE TriggerType, const FString& Param1, const FString& Param2);
	///等级改变时，一个触发指引，二是部分显示的指引需要重新判断条件，如果条件不符，需要隐藏
	void OnTriggerLevel(ETUTORIALTRIGGERTYPE TriggerType, const FString& Param1, const FString& Param2);

	///显示指引
	void ShowAction(const FName& KeyIndex, const int32& TutorialType, const FString& Param1, const FString& Param2);
	///开始显示指引,支持多步操作
	void StartArrow(const FName& KeyIndex, const FString& Param1, const FString& Param2);
	///消息提示排队等待，若不用等待则开始显示指引,支持多步操作
	void QueueMessage(const FName& KeyIndex, const FString& Param1, const FString& Param2);
	///图片指引排队等待，若不用等待则开始显示指引,支持多步操作
	void QueueImage(const FName& KeyIndex, const FString& Param1, const FString& Param2);

	///箭头指引
	void ShowArrowAction(const FTUTORIALPARAM& ActParams);
	///锁屏箭头指引
	void ShowLockScreenArrowAction(const FTUTORIALPARAM& ActParams);

	///显示下一步箭头指引
	void DoNextArrowAction();
	///显示下一步图片指引
	void DoNextImageAction();
	///显示下一步消息指引
	void DoNextMessageAction();

	///存储消息提示列表
	void AddTriggerMessage(const FTUTORIALDATA& TutorialData, const FString& Param1, const FString& Param2);
	///消息指引排序
	void SortMessage();
	///图片指引列表已经有某个指引
	bool IsInNeedShowMessageList(const FName& KeyIndex);
	///排队触发消息指引处理
	void TriggerNextMessage();

	///存储图片指引列表
	void AddTriggerImage(const FTUTORIALDATA& TutorialData, const FString& Param1, const FString& Param2);
	///图片指引列表已经有某个指引
	bool IsInNeedShowImageList(const FName& KeyIndex);
	///排队触发图片指引处理
	void TriggerNextImage();

	///指引完成
	void OnTutorialFinished(FTUTORIALDATA& Data);
	/**
	*关闭指引
	*
	*@param	Index 触发指引配置中的唯一行ID
	*
	*@return 无
	*/
	void HideTriggerItem(const FName& Index);

	///放弃任务
	void AbandonQuest(int32 QuestID);

	///需要指引的物品，通过打开背包对它进行操作（丢弃、出售、放入仓库、打开物品），关闭界面
	void OnRemoveMessageTutorial(FString ItemUID);

	bool CanTriggerNew(ETUTORIALTRIGGERTYPE TriggerType, const FString& Param1, const FString& Param2);///<是否能触发新的一条指引

	void PlayNextVoice();
	void StopVoice();
	void ClearVoiceData();

private:
	static UTutorialManager* Instance;
	///配置表数据
	UPROPERTY()
	TMap<ETUTORIALTRIGGERTYPE, FTutorialMap> TriggerDatasMap;
	///记录显示的索引及控件列表 
	UPROPERTY()
	TMap<FName, FWndList> ShowTriggerWnds;

	///当前显示的箭头指引
	FName CurrentShowArrowIndex;
	FTUTORIALPARAM CurrentShowArrowData;
	///后续指引步骤，排队显示
	FTutorialListData NeedShowArrowActions;

	///当前显示的图片指引
	FName CurrentShowImageIndex;
	FTUTORIALPARAM CurrentShowImageData;
	///当前需要显示的图片指引队列，每次仅显示一个
	TArray<FTutorialListData> NeedShowImageDatas;
	///后续指引步骤，排队显示
	FTutorialListData NeedShowImageActions;

	///当前显示的消息指引
	FName CurrentShowMessageIndex;
	FTUTORIALPARAM CurrentShowMessageData;
	///当前需要显示的消息提示队列（包括获得物品、更高战斗力提示），每次仅显示一个
	TArray<FTutorialListData> NeedShowMesssageDatas;
	///后续指引步骤，排队显示
	FTutorialListData NeedShowMesssageActions;

	///开始等待面板打开
	bool IsStartWaitOpenPanel = false;
	///等待打开的面板路径
	int32 WaitOpenPanelUIType;
	FString WaitOpenWidgetPath;
	///等待面板打开的时间
	float CheckWaitOpenPanelTime = 0.0f;
	///等待面板打开的指引
	FTUTORIALPARAM WaitShowData;

	///----------语音相关--------
	///当前正在播放的指引语音
	FString CurrAudioIds;
	///语音列表
	TArray<FString> AudioIDList;
	///最后一条语音
	FString LastAudioID;
	///语音播完是否自动下一步
	bool bIsAutoNextStep;
	///当前正在语音的指引Index
	FName CurrAudioIndex;
	///----------
};
