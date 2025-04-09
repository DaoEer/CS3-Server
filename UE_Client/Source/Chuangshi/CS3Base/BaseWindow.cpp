// Fill out your copyright notice in the Description page of Project Settings.


#include "BaseWindow.h"
//UE4
#include "Blueprint/WidgetLayoutLibrary.h"
#include "Components/CanvasPanelSlot.h"
#include "Runtime/Engine/Classes/Engine/UserInterfaceSettings.h"
//CS3
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CS3Base/RootUIWidget.h"
#include "CS3Base/UIManager.h"
#include "CS3Base/UIFixerManager.h"
#include "Manager/GameStatus.h"
#include "Manager/StoryManager.h"
#include "Manager/CustomCursorManager.h"
#include "Manager/SystemSwitchManager.h"
#include "Manager/TutorialManager.h"
#include "Util/CS3Debug.h"
#include "Interface/Role/RoleTradeInterface.h"
#include "Manager/MessageManager.h"
#include "Manager/MediaPlayerManager.h"

CONTROL_COMPILE_OPTIMIZE_START
UBaseWindow::UBaseWindow(const FObjectInitializer& ObjectInitializer) 
	: Super(ObjectInitializer)
{
	H_DockStyle = EUIHDOCKSTYLE::CENTER;//默认窗口居中显示
	V_DockStyle = EUIVDOCKSTYLE::MIDDLE;
	Left = 0;
	Top = 0;
	Center = 0;
	Middle = 0;
	Right = 0;
	Bottom = 0;

	R_Left = 0;
	R_Top = 0;
	R_Center = 0.5;
	R_Middle = 0.5;
	R_Right = 1;
	R_Bottom = 1;

	Pos.X = 0;
	Pos.Y = 0;

	PosZSegment = 0;
	PosZ = 0;
	bMoveable = true;
	bActivable = true;
	bHitable = true;
	bEscHide = true;
	
	ParentWindowType = TEXT("");
	LastParentWindowType = TEXT("");
	SubWindows.Empty();
}

UBaseWindow::~UBaseWindow()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("UBaseWindow::~UBaseWindow is dispose------------------>>>"));
}

FReply UBaseWindow::NativeOnMouseButtonDown(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent)
{
	//如果是特殊鼠标状态，不响应
	if (UGolbalBPFunctionLibrary::CustomCursorManager() && UGolbalBPFunctionLibrary::CustomCursorManager()->IsEspecialCursorState())
	{
		return FReply::Handled();
	}
	//激活界面
	if (UGolbalBPFunctionLibrary::GUIManager())
	{
		UGolbalBPFunctionLibrary::GUIManager()->ActiveWindow(this);
	}
	//界面拖拽
	if (InMouseEvent.IsMouseButtonDown(EKeys::LeftMouseButton))
	{
		DragWindowOffest = InGeometry.AbsoluteToLocal(InMouseEvent.GetScreenSpacePosition());
	}

	TSharedPtr<SWidget> CapturingSlateWidget = this->GetCachedWidget();
	if (CapturingSlateWidget.IsValid())
	{
		return FReply::Handled().CaptureMouse(CapturingSlateWidget.ToSharedRef());
	}
	else
	{
		return FReply::Handled();
	}
}

FReply UBaseWindow::NativeOnMouseButtonUp(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent)
{
	return FReply::Handled().ReleaseMouseCapture();
}

FReply UBaseWindow::NativeOnMouseButtonDoubleClick(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent)
{
	return FReply::Handled().ReleaseMouseCapture();
}

FReply UBaseWindow::NativeOnMouseMove(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent)
{
	// 鼠标捕获中 && 窗口能移动 && 鼠标左键
	if (HasMouseCapture() && bMoveable && InMouseEvent.IsMouseButtonDown(EKeys::LeftMouseButton) && UGolbalBPFunctionLibrary::GUIManager() && UGolbalBPFunctionLibrary::GUIManager()->RootUIWidget)
	{
		FVector2D Offest = UGolbalBPFunctionLibrary::GUIManager()->RootUIWidget->GetCachedGeometry().AbsoluteToLocal(InMouseEvent.GetScreenSpacePosition());
		SetPosition(Offest - DragWindowOffest);

		TSharedPtr<SWidget> CapturingSlateWidget = this->GetCachedWidget();
		if (CapturingSlateWidget.IsValid())
		{
			return FReply::Handled().CaptureMouse(CapturingSlateWidget.ToSharedRef());
		}
		else
		{
			return FReply::Handled();
		}
	}
	return FReply::Unhandled();
}

void UBaseWindow::NativeOnEnterWorld()
{
	OnEnterWorld();
}

void UBaseWindow::NativeOnLeaveWorld()
{
	OnLeaveWorld();
}

void UBaseWindow::NativeOnAfterActived()
{
	OnAfterActived();
}

bool UBaseWindow::OnClickDrop(const FDragDropOperationData& MouseCaptureData)
{
	return true;
}

bool UBaseWindow::IsCanShow(FString ParentType)
{
	if (!IsValid(UUECS3GameInstance::Instance) || !IsValid(UUECS3GameInstance::Instance->GameStatus) || !IsValid(UGolbalBPFunctionLibrary::GUIManager()))
	{
		return false;
	}
	//视频界面一直不受限制
	if (WindowType.Equals(TEXT("CreateCG")))
	{
		return true;
	}
	//是否屏蔽了UI
	if (UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() == EGameStatus::InWorld && UGolbalBPFunctionLibrary::GUIManager()->GetIsHideAllUI())
	{
		if (UGolbalBPFunctionLibrary::GUIManager()->GetIsHideAllUI())
		{
			LastParentWindowType = ParentType;
			UGolbalBPFunctionLibrary::GUIManager()->AddBeforeHideVSWindow(this);
		}
		return false;
	}
	//可打开界面列表有数据，并且当前界面不在可打开界面列表里
	if (UGolbalBPFunctionLibrary::GUIManager()->GetCanShowWindowTypes().Num() > 0 && !UGolbalBPFunctionLibrary::GUIManager()->GetCanShowWindowTypes().Contains(WindowType))
	{
		return false;
	}
	//处于剧情状态，不能马上打开界面，需要把要打开的界面保存下来，等离开剧情时再打开
	if (UGolbalBPFunctionLibrary::GStoryManager() && UGolbalBPFunctionLibrary::GStoryManager()->IsNeedHideUI())
	{
		if (IsStoryHide())
		{
			LastParentWindowType = ParentType;
			UGolbalBPFunctionLibrary::GUIManager()->AddBeforeHideVSWindow(this);
			return false;
		}
	}
	//处于视频状态，不能马上打开界面，需要把要打开的界面保存下来，等视频播完再打开
	if (UGolbalBPFunctionLibrary::MediaPlayerManager() && UGolbalBPFunctionLibrary::MediaPlayerManager()->IsNeedHideUI())
	{
		LastParentWindowType = ParentType;
		UGolbalBPFunctionLibrary::GUIManager()->AddBeforeHideVSWindow(this);
		return false;
	}
	//交易状态中，玩家想要打开邮件、商店、商城界面时，弹出提示“交易状态下，无法打开该界面”,ID 1421 
	URoleTradeInterface* TradeInterface = Cast<URoleTradeInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleTradeInterface"), 0));
	if (IsValid(TradeInterface) && TradeInterface->GetRoleTradeState() != TRADE_STATE::TRADE_STATE_NULL)
	{
		//打开邮件、商店、商城界面时
		if (WindowType == TEXT("Mail")
			|| WindowType == TEXT("NPCShop")
			|| WindowType == TEXT("Mall"))
		{
			//提示“交易状态下，无法打开该界面”, ID 1421
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(1421);
			return false;
		}
	}
	return true;
}

bool UBaseWindow::IsStoryHide()
{
	if (WindowType != TEXT("SwitchScene")
		&& WindowType != TEXT("PortraitDialog")
		&& WindowType != TEXT("MonsterAIDialog")
		&& WindowType != TEXT("Story")
		&& WindowType != TEXT("StoryText")
		&& WindowType != TEXT("HaoLingGuQTE")
		&& WindowType != TEXT("CreateCG"))
	{
		return true;
	}
	return false;
}

void UBaseWindow::InitConfigData(FUIConfigData data)
{
	WindowType = data.WinType;
	PosZSegment = data.PosZSegment;
	bMoveable = data.IsMoveable;
	bActivable = data.IsActivable;
	bHitable = data.IsHitable;
	bEscHide = data.IsEscHide;

	H_DockStyle = data.H_DockStyle;
	V_DockStyle = data.V_DockStyle;
	Left = data.Left;
	Top = data.Top;
	Center = data.Center;
	Middle = data.Middle;
	Right = data.Right;
	Bottom = data.Bottom;

	R_Left = data.R_Left;
	R_Top = data.R_Top;
	R_Center = data.R_Center;
	R_Middle = data.R_Middle;
	R_Right = data.R_Right;
	R_Bottom = data.R_Bottom;
}

void UBaseWindow::Init()
{
	this->InitOnes();//蓝图界面初始化
	if (UUECS3GameInstance::Instance)
	{
		if (UUECS3GameInstance::Instance->SystemSwitchManager)
		{
			UUECS3GameInstance::Instance->SystemSwitchManager->InitOpenStateByWindowType(WindowType);
		}
		if (UUECS3GameInstance::Instance->UIFixerManager)
		{
			UUECS3GameInstance::Instance->UIFixerManager->OnWindowInit(this);
		}
	}
}

void UBaseWindow::Show(FString ParentType /*= TEXT("")*/)
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("before UBaseWindow::Show name:%s"), *this->GetFullName());
	if (IsVisible()) return;
	if (!IsCanShow(ParentType)) return;
	if (OnBeforeShowBP()) return;
	
	//打开窗口之前需要做的处理
	this->OnBeforeShow();

	ParentWindowType = ParentType;
	LastParentWindowType = ParentWindowType;

	UBaseWindow* ParentWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(ParentWindowType);
	if (ParentWindow)
	{
		//添加本窗口为父窗口的子窗口
		ParentWindow->AddSubWindow(this);
	}

	if (!IsVisible())
	{
		//显示窗口
		SetVisibility(ESlateVisibility::SelfHitTestInvisible);
	}
	//打开窗口之后需要做的处理
	this->OnAfterShowed();
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("end UBaseWindow::Show name:%s"), *this->GetFullName());
}

void UBaseWindow::Hide()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("before UBaseWindow::Hide name:%s"),*this->GetFullName());
	if (!IsVisible())
	{
		//剧情中，剧情开始时关闭了界面，然后服务器来消息要关闭界面（说明这个界面不需要在出剧情后打开了），这个时候需要从BeforeHideVSWindow列表移除界面
		UGolbalBPFunctionLibrary::GUIManager()->RemoveBeforeHideVSWindow(this);
		return;
	}
	bool IsSuccess = DoHide();
	if (IsSuccess)
	{
		UGolbalBPFunctionLibrary::GUIManager()->RemoveBeforeHideVSWindow(this);
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("end UBaseWindow::Hide name:%s"), *this->GetFullName());
}

bool UBaseWindow::DoHide()
{
	if (OnBeforeHideBP())
	{
		return false;
	}

	//关闭前的处理
	this->OnBeforeClose();
	
	if (IsVisible())
	{
		//隐藏窗口
		SetVisibility(ESlateVisibility::Collapsed);
	}

	//如果隐藏成功
	if (!IsVisible())
	{
		DoWindowTreeHide();
	}

	//关闭后的处理
	this->OnAfterClosed();
	return true;
}

void UBaseWindow::DoWindowTreeHide()
{
	UBaseWindow* ParentWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(ParentWindowType);
	if (ParentWindow)
	{
		//则从父窗口列表中清除我自己
		ParentWindow->RemoveSubWindow(this);
	}
	//隐藏所有子窗口
	for (int i = 0; i < SubWindows.Num(); i++)
	{
		SubWindows[i]->OnParentHide();
	}
	SubWindows.Empty();
}

void UBaseWindow::OrderHide()
{
	if (OnBeforeOrderHideBP()) return;
	if (OnBeforeHideBP()) return;

	//关闭前的处理
	this->OnBeforeClose();

	if (IsVisible())
	{
		//隐藏窗口
		SetVisibility(ESlateVisibility::Collapsed);
	}

	//如果隐藏成功
	if (!IsVisible())
	{
		UBaseWindow* ParentWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(ParentWindowType);
		if (ParentWindow)
		{
			//则从父窗口列表中清除我自己
			ParentWindow->RemoveSubWindow(this);
		}
	}

	//关闭后的处理
	this->OnAfterClosed();
}

void UBaseWindow::StoryHide()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("before UBaseWindow::StoryHide name:%s"), *this->GetFullName());
	if (!IsVisible())
	{
		return;
	}
	DoHide();
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("end UBaseWindow::StoryHide name:%s"), *this->GetFullName());
}

void UBaseWindow::Destroy()
{
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("before UBaseWindow::Destroy name:%s"), *this->GetFullName());
	if (OnBeforeDestroyBP()) return;

	//销毁前的处理
	this->OnBeforeDestroy();
	
	DoWindowTreeHide();

	//销毁
	this->RemoveFromParent();
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("end UBaseWindow::Destroy name:%s"), *this->GetFullName());
}

void UBaseWindow::SetPosition(FVector2D InPosition)
{
	//处理界面移动到屏幕外的情况
	const FVector2D ViewportSize = UGolbalBPFunctionLibrary::GetViewportSize();
	const float ViewportScale = GetDefault<UUserInterfaceSettings>(UUserInterfaceSettings::StaticClass())->GetDPIScaleBasedOnSize(FIntPoint(ViewportSize.X, ViewportSize.Y));
	if (InPosition.X < (-Size.X + 20))//左边
	{
		InPosition.X = -Size.X + 20;
	}
	if (InPosition.X > (ViewportSize.X / ViewportScale - 20))//右边
	{
		InPosition.X = ViewportSize.X / ViewportScale - 20;
	}
	if (InPosition.Y < (-Size.Y + 20))//上边
	{
		InPosition.Y = -Size.Y + 20;
	}
	if (InPosition.Y > (ViewportSize.Y / ViewportScale - 20))//下边
	{
		InPosition.Y = ViewportSize.Y / ViewportScale - 20;
	}
	//设置位置
	Pos = InPosition;
	UCanvasPanelSlot* canvasPanelSlot = Cast<UCanvasPanelSlot>(UWidgetLayoutLibrary::SlotAsCanvasSlot(this));
	if (canvasPanelSlot)
	{
		canvasPanelSlot->SetPosition(Pos);
	}
}

void UBaseWindow::SetSize(FVector2D InSize)
{
	Size = InSize;
	UCanvasPanelSlot* canvasPanelSlot = Cast<UCanvasPanelSlot>(UWidgetLayoutLibrary::SlotAsCanvasSlot(this));
	if (canvasPanelSlot)
	{
		if (Size == FVector2D::ZeroVector)
		{
			CS3_Warning(TEXT("-->error:UBaseWindow::SetSize : %s WindowSize IsZero !"), *WindowType);
			canvasPanelSlot->SetAutoSize(true);
		}
		else
		{
			canvasPanelSlot->SetSize(Size);
		}
	}
}

void UBaseWindow::SetDockStyle(EUIHDOCKSTYLE InHDockStyle, EUIVDOCKSTYLE InVDockStyle)
{
	H_DockStyle = InHDockStyle;
	V_DockStyle = InVDockStyle;
	if (UUECS3GameInstance::Instance->UIFixerManager)
	{
		UUECS3GameInstance::Instance->UIFixerManager->UpdateDockStyle(this);
	}
}

void UBaseWindow::AddSubWindow(UBaseWindow* Window)
{
	if (SubWindows.Num() <= 0)
	{
		SubWindows.Add(Window);
	}
	else
	{
		bool isIn = SubWindows.Find(Window) < 0 ? false : true;
		if (!isIn)
		{
			SubWindows.Add(Window);
		}
	}
}

void UBaseWindow::RemoveSubWindow(UBaseWindow* Window)
{
	if (SubWindows.Num() <= 0)
	{
		return;
	}
	else
	{
		bool isIn = SubWindows.Find(Window) < 0 ? false : true;
		if (isIn)
		{
			SubWindows.Remove(Window);
		}
	}
}

void UBaseWindow::OnParentHide()
{
	Hide();
	ParentWindowType = TEXT("");
}

void UBaseWindow::OnBeforeShow()
{
	//发送广播事件
	OnBeforeShowDelegate.Broadcast(this);
}

void UBaseWindow::OnAfterShowed()
{
	if (UGolbalBPFunctionLibrary::GUIManager())
	{
		//告诉管理器显示本窗口
		UGolbalBPFunctionLibrary::GUIManager()->OnWindowShow(this);
	}
	OnAfterShowedBP();
	if (UGolbalBPFunctionLibrary::TutorialManager())
	{
		//触发新手指引
		UGolbalBPFunctionLibrary::TutorialManager()->OnOpenWindow(WindowType);
	}
}

void UBaseWindow::OnBeforeClose()
{
	if (UGolbalBPFunctionLibrary::GUIManager())
	{
		//告诉管理器有一个 UI 隐藏
		UGolbalBPFunctionLibrary::GUIManager()->OnWindowHide(this);
	}
}

void UBaseWindow::OnAfterClosed()
{
	OnAfterClosedDelegate.Broadcast(this);
	OnAfterHideBP();
}

void UBaseWindow::OnBeforeDestroy()
{
	if (UGolbalBPFunctionLibrary::GUIManager())
	{
		UGolbalBPFunctionLibrary::GUIManager()->OnWindowDestroy(this);
	}
}

void UBaseWindow::UpdatePosition()
{
	const FVector2D ViewportSize = UGolbalBPFunctionLibrary::GetViewportSize();
	const float ViewportScale = GetDefault<UUserInterfaceSettings>(UUserInterfaceSettings::StaticClass())->GetDPIScaleBasedOnSize(FIntPoint(ViewportSize.X, ViewportSize.Y));
	FVector2D NewPos = Pos;
	//水平方向
	if (H_DockStyle == EUIHDOCKSTYLE::LEFT)
	{
		NewPos.X = Left;
	}
	else if (H_DockStyle == EUIHDOCKSTYLE::CENTER)
	{
		NewPos.X = ViewportSize.X / ViewportScale * 0.5 - Size.X * 0.5 + Center;
	}
	else if (H_DockStyle == EUIHDOCKSTYLE::RIGHT)
	{
		NewPos.X = ViewportSize.X / ViewportScale - Size.X - Right;
	}
	else if (H_DockStyle == EUIHDOCKSTYLE::S_LEFT)
	{
		NewPos.X = ViewportSize.X / ViewportScale * R_Left;
	}
	else if (H_DockStyle == EUIHDOCKSTYLE::S_CENTER)
	{
		NewPos.X = ViewportSize.X / ViewportScale * R_Center - Size.X * 0.5;
	}
	else if (H_DockStyle == EUIHDOCKSTYLE::S_RIGHT)
	{
		NewPos.X = ViewportSize.X / ViewportScale * R_Right - Size.X;
	}
	else if (H_DockStyle == EUIHDOCKSTYLE::HFILL)
	{
		NewPos.X = 0;
	}
	//垂直方向
	if (V_DockStyle == EUIVDOCKSTYLE::TOP)
	{
		NewPos.Y = Top;
	}
	else if (V_DockStyle == EUIVDOCKSTYLE::MIDDLE)
	{
		NewPos.Y = ViewportSize.Y / ViewportScale * 0.5 - Size.Y * 0.5 + Middle;
	}
	else if (V_DockStyle == EUIVDOCKSTYLE::BOTTOM)
	{
		NewPos.Y = ViewportSize.Y / ViewportScale - Size.Y - Bottom;
	}
	else if (V_DockStyle == EUIVDOCKSTYLE::S_TOP)
	{
		NewPos.Y = ViewportSize.Y / ViewportScale * R_Top;
	}
	else if (V_DockStyle == EUIVDOCKSTYLE::S_MIDDLE)
	{
		NewPos.Y = ViewportSize.Y / ViewportScale * R_Middle - Size.Y * 0.5;
	}
	else if (V_DockStyle == EUIVDOCKSTYLE::S_BOTTOM)
	{
		NewPos.Y = ViewportSize.Y / ViewportScale * R_Bottom - Size.Y;
	}
	else if (V_DockStyle == EUIVDOCKSTYLE::VFILL)
	{
		NewPos.Y = 0;
	}
	SetPosition(NewPos);
}

CONTROL_COMPILE_OPTIMIZE_END
