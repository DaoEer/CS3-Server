// Fill out your copyright notice in the Description page of Project Settings.
#pragma once
#include "CoreMinimal.h"
#include "CS3Base/CS3UserWidget.h"
#include "GameData/UIDataDefine.h"
#include "Delegate.h"
#include "GameData/UIConfigData.h"
#include "BaseWindow.generated.h"

/*
* 文件名称：BaseWindow.h
* 功能说明：窗口基类
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2016-09-14
*/

class UBaseWindow;
DECLARE_MULTICAST_DELEGATE_OneParam(FOnBeforeShowDelegate, UBaseWindow*);
DECLARE_MULTICAST_DELEGATE_OneParam(FOnAfterClosedDelegate, UBaseWindow*);

UCLASS(BlueprintType)
class CHUANGSHI_API UBaseWindow : public UCS3UserWidget
{
	GENERATED_BODY()
public:
	UBaseWindow(const FObjectInitializer& ObjectInitializer);
	~UBaseWindow();
public:
	virtual FReply NativeOnMouseButtonDown(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent) override;
	virtual FReply NativeOnMouseButtonUp(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent);
	virtual FReply NativeOnMouseButtonDoubleClick(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent);
	virtual FReply NativeOnMouseMove(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent);
	virtual void NativeOnEnterWorld(); ///<当角色进入世界时被调用
	virtual void NativeOnLeaveWorld();///<当角色离开世界时被调用
	virtual void NativeOnAfterActived();///<窗口被激活之后被调用

	bool OnClickDrop(const FDragDropOperationData& MouseCaptureData);
	/**
	*BlueprintCallable，显示窗口
	*
	*@param	ParentType 父窗口类型
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "BaseWindow")
		void Show(FString ParentType = TEXT(""));
	/**
	*BlueprintCallable，隐藏窗口
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "BaseWindow")
		void Hide();
	/**
	*按ESC隐藏窗口
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "BaseWindow")
	void OrderHide();
	/**
	*镜头或剧情隐藏窗口
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "BaseWindow")
		void StoryHide();
	/**
	*BlueprintCallable，销毁窗口
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "BaseWindow")
		void Destroy();
	/**
	*BlueprintCallable,是否可显示界面
	*
	*@return 是否可显示
	*/
	UFUNCTION(BlueprintCallable, Category = "BaseWindow")
		bool IsCanShow(FString ParentType);
	/**
	*BlueprintCallable,是否受剧情或快捷键隐藏全部界面功能影响
	*
	*@return 是否在触发剧情时隐藏或快捷键隐藏全部界面时隐藏
	*/
	UFUNCTION(BlueprintCallable, Category = "BaseWindow")
		bool IsStoryHide();
	/**
	*BlueprintCallable,设置窗口位置
	*
	*@param	position 要设置的位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "BaseWindow")
		void SetPosition(FVector2D InPosition);
	/**
	*BlueprintCallable,设置窗口Size
	*
	*@param	size 要设置的size
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "BaseWindow")
		void SetSize(FVector2D InSize);	
	/**
	*BlueprintCallable,刷新位置，用于动态Size的界面，根据内容设置Size后刷新界面位置
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "BaseWindow")
		void UpdatePosition();
	/**
	*BlueprintCallable,设置窗口DockStyle
	*
	*@param	InHDockStyle 要设置的水平DockStyle
	*@param	InVDockStyle 要设置的垂直DockStyle
	*
	*@return 无
	*/
	UFUNCTION(BlueprintCallable, Category = "BaseWindow")
		void SetDockStyle(EUIHDOCKSTYLE InHDockStyle, EUIVDOCKSTYLE InVDockStyle);
	/**
	*初始化界面配置数据，创建时调用
	*
	*@return 无
	*/
	void InitConfigData(FUIConfigData data);
	/**
	*初始化界面，创建时调用
	*
	*@return 无
	*/
	void Init();
	/**
	*BlueprintImplementableEvent，初始化蓝图，创建时调用，只执行一次
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "BaseWindow")
		void InitOnes();
	/**
	*BlueprintImplementableEvent，打开界面子面板
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "BaseWindow")
		void OnOpenWindowWithTabIndex(int32 TabIndex);
	/**
	*BlueprintImplementableEvent，窗口显示之前给蓝图的回调	
	*
	*@return 是否阻止界面打开，返回false则继续Show()打开界面
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "BaseWindow")
	bool OnBeforeShowBP();
	/**
	*BlueprintImplementableEvent，窗口显示之后给蓝图的回调
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "BaseWindow")
	void OnAfterShowedBP();
	/**
	*BlueprintImplementableEvent，窗口隐藏之前给蓝图的回调
	*
	*@return 是否阻止界面关闭，返回false则继续Hide()关闭界面
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "BaseWindow")
	bool OnBeforeHideBP();
	/**
	*BlueprintImplementableEvent，窗口隐藏之后给蓝图的回调
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "BaseWindow")
	void OnAfterHideBP();
	/**
	*BlueprintImplementableEvent，按ESC隐藏，窗口隐藏之前给蓝图的回调
	*
	*@return 是否阻止界面关闭，返回false则继续Hide()关闭界面
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "BaseWindow")
		bool OnBeforeOrderHideBP();
	/**
	*BlueprintImplementableEvent，窗口销毁之前给蓝图的回调
	*
	*@return 是否阻止界面销毁，返回false则继续Destroy()销毁界面
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "BaseWindow")
		bool OnBeforeDestroyBP();
	/**
	*BlueprintImplementableEvent，游戏状态改变前被调用
	*
	*@param	oldStatus old状态
	*@param	newStatus new状态
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "BaseWindow")
	void BeforeStatusChanged(EGameStatus oldStatus, EGameStatus newStatus);
	
	/**
	*BlueprintImplementableEvent，游戏状态改变后被调用
	*
	*@param	oldStatus old状态
	*@param	newStatus new状态
	*
	*@return 无
	*/
	UFUNCTION(BlueprintImplementableEvent, Category = "BaseWindow")
	void AfterStatusChanged(EGameStatus oldStatus, EGameStatus newStatus);

	UFUNCTION(BlueprintImplementableEvent, Category = "BaseWindow")
	void OnEnterWorld(); ///<BlueprintImplementableEvent，当角色进入世界时被调用
	
	UFUNCTION(BlueprintImplementableEvent, Category = "BaseWindow")
	void OnLeaveWorld();///<BlueprintImplementableEvent,当角色离开世界时被调用

	UFUNCTION(BlueprintImplementableEvent, Category = "BaseWindow")
	void OnAfterActived();///<BlueprintImplementableEvent,窗口被激活之后被调用

	UFUNCTION(BlueprintImplementableEvent, Category = "BaseWindow")
	void OnFailedLogin();///BlueprintImplementableEvent，登录失败蓝图通知事件

private:
	/**
	*@return 是否隐藏成功
	*/
	bool DoHide();
	void DoWindowTreeHide();///<界面隐藏时处理父界面和子界面
	void AddSubWindow(UBaseWindow* Window);///<添加一个子窗口	
	void RemoveSubWindow(UBaseWindow* Window);///<删除一个子窗口
	void OnParentHide();///<当窗口的父窗口隐藏时被调用	
	void OnBeforeShow();///<窗口显示之前被调用	
	void OnAfterShowed();///<窗口显示之后被调用	
	void OnBeforeClose();///<窗口隐藏之前被调用	
	void OnAfterClosed();///<窗口隐藏之后被调用
	void OnBeforeDestroy();///<窗口销毁之前被调用

public:
	//打开界面消息通知
	FOnBeforeShowDelegate OnBeforeShowDelegate;
	//关闭界面消息通知
	FOnAfterClosedDelegate OnAfterClosedDelegate;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BaseWindow | ReadWrite")
	FVector2D DragWindowOffest;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "BaseWindow | ReadOnly")
	FString WindowType;			///<窗口类型

	UPROPERTY(EditAnywhere, BlueprintReadWrite, category = "BaseWindow | ReadWrite")
	FVector2D Size;							///< 获取/设置大小（像素坐标） 
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "BaseWindow | ReadOnly")
	FVector2D Pos;							///< 获取/设置坐标( 像素坐标 )
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "BaseWindow | ReadOnly")
	int PosZSegment;						///< 窗口层次
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "BaseWindow | ReadOnly")
	int PosZ;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "BaseWindow | ReadOnly")
	bool bMoveable;							///<标示窗口是否可以移动
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "BaseWindow | ReadOnly")
	bool bActivable;						///< 标示窗口是否可被激活
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "BaseWindow | ReadOnly")
	bool bHitable;							///< 如果为 False，鼠标点击在窗口上时，仍然判断鼠标点击的是屏幕
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "BaseWindow | ReadOnly")
	bool bEscHide;							///< 按 esc 键是否会隐藏
	
	FString ParentWindowType;		///<父窗口类型，默认WINDOW_TYPE_NO
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, category = "BaseWindow | ReadOnly")
		FString LastParentWindowType;	///< 上次显示时的父窗口，用于隐藏之后的恢复
	UPROPERTY(VisibleAnywhere, category = "BaseWindow | ReadOnly")
	TArray<UBaseWindow*> SubWindows;		///< 子窗口列表 

	
	EUIHDOCKSTYLE H_DockStyle;				///< 获取/设置相对其父UI的水平停靠方式："LEFT", "CENTER", "RIGHT","HFILL", "S_LEFT", "S_CENTER", "S_RIGHT"
	EUIVDOCKSTYLE V_DockStyle;				///< 获取/设置相对其父UI的垂直停靠方式："TOP", "MIDDLE", "BOTTOM","VFILL", "S_TOP", "S_MIDDLE", "S_BOTTOM"
	float Left;								///< 获取/设置左距( 像素坐标 )
	float Top;								///< 获取/设置顶距( 像素坐标 )
	float Center;							///< 获取/设置水平中距( 像素坐标 ),偏左设置负数，偏右设置正数
	float Middle;							///< 获取/设置垂直中距( 像素坐标 ),偏上设置负数，偏下设置正数
	float Right;							///< 获取/设置右距( 像素坐标 )
	float Bottom;							///< 获取/设置底距( 像素坐标 )
	
	float R_Left;							///< 获取/设置左距( 相对坐标 )
	float R_Top;							///< 获取/设置顶距( 相对坐标 )
	float R_Center;							///< 获取/设置水平中距( 相对坐标 )
	float R_Middle;							///< 获取/设置垂直中距( 相对坐标 )
	float R_Right;							///< 获取/设置右距( 相对坐标 )
	float R_Bottom;							///< 获取/设置底距( 相对坐标 )
};