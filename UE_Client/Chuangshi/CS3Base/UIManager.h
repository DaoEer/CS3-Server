// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "GameData/CS3Object.h"
#include "GameData/GameDeFine.h"
#include "GameData/UIConfigData.h"
#include "UMG/Public/Components/SlateWrapperTypes.h"
#include "UIManager.generated.h"

/*
* 文件名称：UIManager.h
* 功能说明：界面管理类
* 文件作者：lizhenghui
* 目前维护：zhangdan
* 创建时间：2016-09-08
*/

class UBaseWindow;
class URootUIWidget;
class UGUIManager;

DECLARE_DELEGATE_FiveParams(FOnLoadComplete, FString, FString, UClass*, FUIConfigData*, TWeakObjectPtr<UGUIManager>);
DECLARE_DYNAMIC_DELEGATE_OneParam(FOnOpenComplete, FString, WindowType);

UCLASS(Blueprintable, BlueprintType)
class CHUANGSHI_API UGUIManager : public UCS3Object
{
	GENERATED_BODY()
	UGUIManager();
	~UGUIManager();

public:
	static UGUIManager* GetInstance();

	//static void ClearInstanceData();

	/**
	*BlueprintCallable，根据界面类型和标签打开界面标签页
	*
	*@param WindowType 界面类型
	*@param TabIndex 界面标签
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		void OpenWindowWithTabIndex(bool IsIgnoreGameStatus = false, EGameStatus GameStatus = EGameStatus::InWorld, FString WindowType = TEXT(""), FString ParentType = TEXT(""), int32 TabIndex = 0);
	/**
	*BlueprintPure，根据界面类型获取界面
	*
	*@param WindowType 界面类型
	*
	*@return UBaseWindow* 根据界面类型获取到界面
	*/
	UFUNCTION(BlueprintPure, Category = "UIManager")
		UBaseWindow* GetWindow(FString WindowType);
	/**
	*BlueprintPure，获取管理器中所有的窗口
	*
	*@return TArray<UBaseWindow*> 所有的窗口
	*/
	UFUNCTION(BlueprintPure, Category = "UIManager")
		TArray<UBaseWindow*> GetWindows();
	/**
	*BlueprintPure，获取管理器中所有可见的窗口
	*
	*@return TArray<UBaseWindow*> 所有可见的窗口
	*/
	UFUNCTION(BlueprintPure, Category = "UIManager")
		TArray<UBaseWindow*> GetVSWindows();
	/**
	*BlueprintPure，获取当前被激活的窗口
	*
	*@return UBaseWindow* 当前被激活的窗口
	*/
	UFUNCTION(BlueprintPure, Category = "UIManager")
		UBaseWindow* GetActWindow();
	/**
	*BlueprintCallable，创建界面
	*
	*@param WindowType 界面类型
	*@param IsMultiple 同一界面类型的对象是否可创建多个，为true可创建多个同类型的界面
	*
	*@return UBaseWindow* 新界面
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		UBaseWindow* CreateUIWindow(FString WindowType, bool IsMultiple = false);
	/**
	*BlueprintCallable，打开界面，没有对象会先创建再打开
	*
	*@param IsIgnoreGameStatus 是否忽略游戏状态
	*@param GameStatus 游戏状态
	*@param WindowType 界面类型
	*@param ParentType 父界面类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		void OpenWindow(bool IsIgnoreGameStatus = false, EGameStatus GameStatus = EGameStatus::InWorld, FString WindowType = TEXT(""), FString ParentType = TEXT(""));
	/**
	*BlueprintCallable，异步打开界面，没有对象会先创建再打开
	*
	*@param IsIgnoreGameStatus 是否忽略游戏状态
	*@param GameStatus 游戏状态
	*@param WindowType 界面类型
	*@param ParentType 父界面类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		void AsyncOpenWindow(FOnOpenComplete EventBack, bool IsIgnoreGameStatus = false, EGameStatus GameStatus = EGameStatus::InWorld, FString WindowType = TEXT(""), FString ParentType = TEXT(""));
	/**
	*打开或关闭窗口，如果界面不存在会创建再打开
	*
	*@param IsIgnoreGameStatus 是否忽略游戏状态
	*@param GameStatus 游戏状态
	*@param WindowTypeIfCreate 界面类型
	*@param RemoveWindowIfClose 关闭时是否销毁界面
	*@param ParentWindowTypeIfShow 打开时设置父界面
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		void UpdateWindow(bool IsIgnoreGameStatus, EGameStatus GameStatus, FString WindowType, bool RemoveWindowIfClose, FString ParentWindowType = TEXT(""));

	/**
	*添加一个窗口到BeforeHideVSWindows列表中
	*
	*@param window 界面
	*
	*@return 无
	*/
	void AddBeforeHideVSWindow(UBaseWindow* window);
	/**
	*从BeforeHideVSWindows列表中删除一个窗口
	*
	*@param window 界面
	*
	*@return 无
	*/
	void RemoveBeforeHideVSWindow(UBaseWindow* window);

	/**
	*BlueprintCallable，添加一个窗口到隐藏窗口列表中
	*
	*@param window 界面
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		void AddHiddenVSWindows(UBaseWindow* window);
	/**
	*BlueprintCallable，设置摆摊状态可以打开的窗口类型列表
	*用于控制摆摊状态下能打开的窗口
	*进入状态时设置列表，出状态时一定要清除列表
	*
	*@param WindowTypes 窗口类型列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		void SetCanShowWindowTypes(TArray<FString> WindowTypes);
	/**
	*BlueprintCallable，清除可以打开的窗口类型列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		void ClearCanShowWindowTypes();
	/**
	*BlueprintPure，获得可以打开的窗口类型列表
	*
	*@param TArray<FString> 窗口类型列表
	*
	*@return 无
	*/
	UFUNCTION(BlueprintPure, Category = "UIManager")
		TArray<FString> GetCanShowWindowTypes();

	/**
	*BlueprintCallable，顺序隐藏当前打开的窗口
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		bool OrderHideWindows();
	/**
	*BlueprintCallable，隐藏所有窗口
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		void HideVSWindows();
	/**
	*BlueprintCallable，关闭所有打开的界面，并且记住这些界面，下次再调用能打开之前关闭的界面
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		void HideOrShowVSWindows(bool bHide);
	/**
	*BlueprintCallable，快捷键设置是否隐藏所有界面
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		void SetIsHideAllUI(bool bIsHide);
	/**
	*BlueprintCallable，获取快捷键设置是否隐藏所有界面
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		bool GetIsHideAllUI();
	/**
	*BlueprintCallable，是否能显示界面
	*剧情时或快捷键隐藏全部界面时，不能马上打开界面，需要把要打开的界面保存下来
	*等离开剧情且没有用快捷键隐藏全部界面时再打开
	*
	*@return 是否能显示界面
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		bool IsCanShowWindowState();
	/**
	*BlueprintCallable，是否已经显示了之前隐藏的界面
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		bool IsShowVSWindows();
	/**
	*BlueprintPure,判断指定窗口是否是激活窗口
	*
	*@param window 指定窗口
	*
	*@return bool 指定窗口是激活窗口返回TRUE，否则返回FALSE
	*/
	UFUNCTION(BlueprintPure, Category = "UIManager")
		bool IsActWindow(UBaseWindow* window);
	/**
	*BlueprintCallable，激活一个窗口，如果激活成功则返回 true，否则返回 false
	*
	*@param window 界面对象
	*@param upgrade 界面是否提到前面显示
	*
	*@return bool 激活成功则返回 true，否则返回 false
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		bool ActiveWindow(UBaseWindow* window, bool upgrade = true);
	/**
	*当有一个窗口显示时被调用
	*
	*@param window 界面
	*
	*@return 无
	*/
	void OnWindowShow(UBaseWindow* window);
	/**
	*当有一个窗口隐藏时被调用
	*
	*@param window 界面
	*
	*@return 无
	*/
	void OnWindowHide(UBaseWindow* window);
	/**
	*当有一个窗口被销毁时被调用
	*
	*@param window 界面
	*
	*@return 无
	*/
	void OnWindowDestroy(UBaseWindow* window);
	/**
	*游戏状态改变前被调用
	*
	*@param oldStatus 界面旧的状态
	*@param newStatus 界面新的状态
	*
	*@return 无
	*/
	void BeforeStatusChanged(EGameStatus oldStatus, EGameStatus newStatus);
	/**
	*游戏状态改变后被调用
	*
	*@param oldStatus 界面旧的状态
	*@param newStatus 界面新的状态
	*
	*@return 无
	*/
	void AfterStatusChanged(EGameStatus oldStatus, EGameStatus newStatus);
	/**
	*当角色进入世界时被调用
	*
	*@return 无
	*/
	void OnRoleEnterWorld();
	/**
	*当角色离开世界时被调用
	*
	*@return 无
	*/
	void OnRoleLeaveWorld();
	/**
	*需要预先创建界面（界面配置表里LoadType字段为0的所有界面），以便entity创建之后，界面接收entity转发的消息的处理
	*
	*@return 无
	*/
	void PreCreateWindows();
	/**
	*当隐藏鼠标操作时被调用
	*
	*@return 无
	*/
	void OnHideMouse();
	/**
	*首次进入游戏时被调用
	*
	*@return 无
	*/
	void OnRoleFirstEnterGame();
	/**
	*离开地图时被调用
	*
	*@return 无
	*/
	void OnLeaveSpaceNotify();

#pragma region	/** RootUI相关 */
	/**
	*禁止调用，界面架构专用
	*显示RootUI
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		void ShowRootUI();
	/**
	*BlueprintCallable，界面添加到RootUI上
	*
	*@param Window 界面
	*@param Position 位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		void AddToRootUI(UBaseWindow* Window, FVector2D Position);
	/**
	*设置RootUI可见性
	*
	*@param InVisibility 可见性
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		void SetRootUIVisible(ESlateVisibility InVisibility);
#pragma endregion

private:
	/**
	*初始化UI配置表
	*
	*@return 无
	*/
	void InitUIConfigData();
	/**
	*通过界面类型找到配置数据
	*
	*@return FUIConfigData
	*/
	FUIConfigData* GetUIConfigDataByWindowType(FString WindowType);
	/**
	*创建界面(同步加载)
	*
	*@param WindowType 界面类型
	*
	*@return UBaseWindow* 新界面
	*/
	UBaseWindow* SynchronousCreateWindow(FString WindowType);
	/**
	*创建界面
	*
	*@param WidgetClass 界面类
	*
	*@return UBaseWindow* 新界面
	*/
	UBaseWindow* CreateBaseWindow(UClass* WidgetClass, FUIConfigData* ConfigData);
	/**
	*异步加载界面资源
	*
	*@param DelegateToCall 回调
	*@param WindowType 界面类型
	*@param ParentType 父界面类型
	*
	*@return 无
	*/
	void AsyncLoadWindowAsset(FOnLoadComplete DelegateToCall, FString WindowType, FString ParentType = TEXT(""));
	/**
	*添加一个顶层窗口到管理器
	*
	*@param window 界面对象
	*@param WindowType 界面类型
	*
	*@return 无
	*/
	void AddWindowToManager(UBaseWindow* window, FString WindowType);
	/**
	*从管理器中删除一个窗口
	*
	*@param window 界面对象
	*
	*@return 无
	*/
	void RemoveWindowFromManager(UBaseWindow* window);
	/**
	*添加一个可见窗口到可见窗口列表
	*
	*@param window 界面
	*
	*@return 无
	*/
	void AddVSWindow(UBaseWindow* window);
	/**
	*从可见窗口列表中删除一个窗口
	*
	*@param window 界面
	*
	*@return 无
	*/
	void RemoveVSWindow(UBaseWindow* window);
	/**
	*激活最顶层的窗口
	*
	*@return 无
	*/
	void ActiveTopWindow();
	/**
	*将一个窗口提到同层最顶层显示
	*
	*@param window 界面
	*
	*@return 无
	*/
	void UpgradeWindow(UBaseWindow* window);
	/**
	*取消一个窗口的激活状态。如果 window 为 nullptr，则取消当前激活窗口的激活状态，并返回 true，
	*如果 window 不为 nullptr，则判断当前激活的窗口是否是指定的窗口，如果不是，则返回 false，否则取消它的激活状态并返回 true
	*
	*@param window 界面
	*
	*@return bool 取消一个窗口的激活状态返回TRUE，否则返回FALSE
	*/
	bool InactiveWindow(UBaseWindow* window = nullptr);
	/**
	*对当前可见界面进行排序
	*
	*@return 无
	*/
	void SortVSWindows();
	/**
	*重新布局
	*
	*@param windows 指定窗口列表
	*@param oldZOrder 窗口深度
	*
	*@return 无
	*/
	void Relayout(TArray<UBaseWindow*> windows, int oldZOrder);
	/**
	*更改窗口深度
	*
	*@param window 界面
	*@param oldSeg 旧的深度
	*@param newSeg 新的深度
	*
	*@return 无
	*/
	void OnZSegmentChanged(UBaseWindow* window, int oldSeg, int newSeg);
	/**
	*BlueprintCallable，刷新同层窗口的深度
	*
	*@param PosZSegment 窗口的层级
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "UIManager")
		void RefreshWindowsZOrder(int32 PosZSegment);
	/**
	/**
	*判断指定窗口是否已经存在于指定Array中
	*
	*@param window 指定窗口
	*@param winsArray 指定Array
	*
	*@return bool 判断指定窗口是否已经存在于指定Array中
	*/
	bool FindArrayByItem(UBaseWindow* window, TArray<UBaseWindow*> winsArray);

	/**
	*获取指定窗口的所有父窗口和子窗口列表
	*
	*@param window 指定窗口
	*
	*@return TMap<int, TArray<UBaseWindow*> > 指定窗口的所有父窗口和子窗口列表
	*/
	//TMap<int, TArray<UBaseWindow*> > GetWindowsTree(UBaseWindow* window);

	/**
	*获取指定窗口的所有子窗口
	*
	*@param parent 父窗口
	*@param window 指定窗口
	*
	*@return TMap<int, TArray<UBaseWindow*> > 指定窗口的所有子窗口
	*/
	//TMap<int, TArray<UBaseWindow*> > GetSubWindows(UBaseWindow* parent, UBaseWindow* window);

public:
	void CheckApplicationActivation(bool bIsActive);

public:
	UPROPERTY(BlueprintReadWrite, Category = "UIManager")
		URootUIWidget* RootUIWidget;

private:
	TMap<int, TArray<UBaseWindow*> > UIMaps;	///<保存所有的窗口
	TMap<int, TArray<UBaseWindow*> > UIVSMaps;	///<保存所有的可见窗口
	UPROPERTY()
		TArray<UBaseWindow*> AllWindows;///<保存所有的窗口
	UPROPERTY()
		TArray<UBaseWindow*> AllVSWindows;///<保存所有的可见窗口
	UPROPERTY()
		TArray<UBaseWindow*> BeforeHideVSWindows;///< 保存关闭所有界面前所有打开的窗口列表
	UPROPERTY()
		TArray<UBaseWindow*> HiddenVSWindows;///< 保存需隐藏的窗口列表（用来存放ctrl+G或镜头播放时隐藏所有可见界面之后不需要再显示出来的界面）
	UPROPERTY()
		TArray<FString> CanShowWindowTypes;///< 保存某种状态下可以打开的窗口列表（用来存放某种状态下可以打开的界面）

	const UDataTable* ConfigDataTable = nullptr;///<UI配置表
	UBaseWindow* CurrActWindow = nullptr;///<保存当前激活的窗口

	bool bIsHideAllUI = false; ///是否屏蔽所有UI
	//static UGUIManager* Instance;
};