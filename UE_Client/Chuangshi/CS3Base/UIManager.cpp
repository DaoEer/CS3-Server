// Fill out your copyright notice in the Description page of Project Settings.


#include "CS3Base/UIManager.h"
// UE4
#include"Chuangshi.h"
#include "Platform.h"
#include "Algo/Reverse.h"
#include "WidgetBlueprintLibrary.h"
#include "SlateApplication.h"
// 数据类型
#include "GameData/StrToClass.h"
// CS3类型
#include "CS3Base/BaseWindow.h"
#include "CS3Base/RootUIWidget.h"
#include "CS3Base/UIDockManager.h"
#include "CS3Base/UIFixerManager.h"
#include "Manager/ResourceManager.h"
#include "Manager/EventManager.h"
#include "Manager/CustomCursorManager.h"
#include "Manager/StoryManager.h"
#include "Manager/MediaPlayerManager.h"
#include "Manager/SystemSwitchManager.h"
#include "Manager/GameStatus.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Manager/TutorialManager.h"

CONTROL_COMPILE_OPTIMIZE_START
UGUIManager::UGUIManager()
{
}

UGUIManager::~UGUIManager()
{
	UIMaps.Empty();	
	UIVSMaps.Empty();
	AllWindows.Empty();
	AllVSWindows.Empty();
	BeforeHideVSWindows.Empty();
	HiddenVSWindows.Empty();
	CanShowWindowTypes.Empty();
	ConfigDataTable = nullptr;
	RootUIWidget = nullptr;
	CurrActWindow = nullptr;
}

UGUIManager* UGUIManager::GetInstance()
{
	cs3_checkNoReentry();

	return NewObject<UGUIManager>();
}

void UGUIManager::OpenWindowWithTabIndex(bool IsIgnoreGameStatus /*= true*/, EGameStatus GameStatus /*= EGameStatus::InWorld*/, FString WindowType /*= TEXT("")*/, FString ParentType /*= TEXT("")*/, int32 TabIndex /*= 0*/)
{
	//先打开界面
	OpenWindow(IsIgnoreGameStatus, GameStatus, WindowType, ParentType);
	
	UBaseWindow* Window = GetWindow(WindowType);
	//界面是否存在且打开
	if (IsValid(Window) && Window->IsVisible())
	{
		//打开标签页
		Window->OnOpenWindowWithTabIndex(TabIndex);
	}
}

/*
void UGUIManager::ClearInstanceData()
{
	Instance->UIMaps.Empty();	///<保存所有的窗口
	Instance->UIVSMaps.Empty();	///<保存所有的可见窗口
	Instance->RootUIWidget = nullptr;
	Instance->AllWindows.Empty();
	Instance->AllVSWindows.Empty();
	Instance->BeforeHideVSWindows.Empty();
	Instance->HiddenVSWindows.Empty();///< 保存需隐藏的窗口列表（用来存放ctrl+G或镜头播放时隐藏所有可见界面之后不需要再显示出来的界面）
	Instance->ConfigDataTable = nullptr;///<UI配置表
	Instance->CurrActWindow = nullptr;///<保存当前激活的窗口
}
*/

UBaseWindow* UGUIManager::CreateUIWindow(FString WindowType, bool IsMultiple /*= false*/)
{
	if (!IsMultiple)
	{
		UBaseWindow* Window = GetWindow(WindowType);
		if (Window)
		{
			return Window;
		}
	}
	return SynchronousCreateWindow(WindowType);
}

void UGUIManager::OpenWindow(bool IsIgnoreGameStatus /*= true*/, EGameStatus GameStatus /*= EGameStatus::InWorld*/, FString WindowType /*= TEXT("")*/, FString ParentType /*= TEXT("")*/)
{
	if (IsIgnoreGameStatus || (UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() == GameStatus))
	{
		CSV_EVENT_GLOBAL(TEXT("OpenWindow %s"), *WindowType);
		UBaseWindow* Window = GetWindow(WindowType);
		if (!IsValid(Window))
		{
			//界面不存在，创建一个
			Window = SynchronousCreateWindow(WindowType);
		}
		if (!IsValid(Window))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UGUIManager::OpenWindow : Window is Null!"));
			return;
		}
		Window->Show(ParentType);
	}
	else
	{
		CS3_Warning(TEXT("-->error:UGUIManager::OpenWindow : GameStatus Is not match!"));
	}
}

void UGUIManager::AsyncOpenWindow(FOnOpenComplete EventBack, bool IsIgnoreGameStatus /*= false*/, EGameStatus GameStatus /*= EGameStatus::InWorld*/, 
	FString WindowType /*= TEXT("")*/, FString ParentType /*= TEXT("")*/)
{
	if (IsIgnoreGameStatus || (UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() == GameStatus))
	{
		CSV_EVENT_GLOBAL(TEXT("AsyncOpenWindow %s"), *WindowType);
		UBaseWindow* Window = GetWindow(WindowType);
		if (!IsValid(Window))
		{
			//异步加载
			TWeakObjectPtr<UGUIManager> DelayThisPtr(this);
			AsyncLoadWindowAsset(FOnLoadComplete::CreateLambda([EventBack](FString WindowType, FString ParentType, UClass* WidgetClass, FUIConfigData* ConfigData, TWeakObjectPtr<UGUIManager> DelayThisPtr)
			{
				//UClass* WidgetClass = Cast<UClass>(ConfigData->Widget.Get());
				UBaseWindow* NewWindow = DelayThisPtr->CreateBaseWindow(WidgetClass, ConfigData);
				if (NewWindow)
				{
					NewWindow->Show(ParentType);
				}
				EventBack.ExecuteIfBound(WindowType);
			}), WindowType, ParentType);
		}
		else
		{
			Window->Show(ParentType);
			EventBack.ExecuteIfBound(WindowType);
		}
	}
	else
	{
		CS3_Warning(TEXT("-->error:UGUIManager::OpenWindow : GameStatus Is not match!"));
	}
}

void UGUIManager::UpdateWindow(bool IsIgnoreGameStatus, EGameStatus GameStatus, FString WindowType, bool RemoveWindowIfClose, FString ParentWindowType /*= TEXT("")*/)
{
	if (IsIgnoreGameStatus || (UUECS3GameInstance::Instance->GameStatus->GetCurrStatus() == GameStatus))
	{
		if (!UUECS3GameInstance::Instance->SystemSwitchManager->CheckOpenByWindowType(WindowType))
		{
			//系统未开放
			return;
		}
		UBaseWindow* Window = GetWindow(WindowType);
		if (!IsValid(Window))
		{
			//界面不存在，创建一个
			Window = SynchronousCreateWindow(WindowType);
			if (!IsValid(Window))
			{
				CS3_Warning(TEXT("-->Null Pointer error:UGUIManager::UpdateWindow : CreateWindow is Fail!"));
				return;
			}
			Window->Show(ParentWindowType);
		}
		else
		{
			if (Window->IsVisible())
			{
				if (RemoveWindowIfClose)
				{
					Window->Destroy();
				}
				else
				{
					Window->Hide();
				}
			}
			else
			{
				Window->Show(ParentWindowType);
			}
		}
	}
	else
	{
		CS3_Warning(TEXT("-->error:UGUIManager::UpdateWindow : GameStatus Is not match!"));
	}
}

UBaseWindow* UGUIManager::GetWindow(FString WindowType)
{
	if (WindowType == TEXT(""))
	{
		return nullptr;
	}
	//遍历所有窗口
	for (auto window : GetWindows())
	{
		if (WindowType == window->WindowType)
		{
			return window;
		}
	}
	return nullptr;
}

void UGUIManager::PreCreateWindows()
{
	//创建界面配置表里LoadType字段为0的所有界面
	if (!IsValid(ConfigDataTable))
	{
		InitUIConfigData();
	}
	if (ConfigDataTable)
	{
		for (auto data : ConfigDataTable->GetRowNames())
		{
			FUIConfigData* ConfigData = (FUIConfigData*)ConfigDataTable->FindRowUnchecked(*data.ToString());
			if (!ConfigData)
			{
				CS3_Warning(TEXT("-->Null Pointer error:UGUIManager::PreCreateWindows : ConfigData!"));
				continue;
			}
			if (GetWindow(ConfigData->WinType) || ConfigData->LoadType == 0)
			{
				continue;
			}
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("-->UGUIManager::PreCreateWindows name=%s"), *data.ToString());
			UClass* WidgetClass = ConfigData->Widget.Get();
			if (!IsValid(WidgetClass) && IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->ResourceManager))
			{
				//同步加载
				WidgetClass = UUECS3GameInstance::Instance->ResourceManager->SynchronousLoadClass(ConfigData->Widget);
			}
			CreateBaseWindow(WidgetClass, ConfigData);
		}
	}
}

void UGUIManager::OnHideMouse()
{
	//取消拖拽事件
	if (UWidgetBlueprintLibrary::IsDragDropping())
	{
		UWidgetBlueprintLibrary::CancelDragDrop();
	}
	//取消界面上的鼠标事件
	if (UGolbalBPFunctionLibrary::GEventManager())
	{
		UGolbalBPFunctionLibrary::GEventManager()->OnCancelMouseEvent.Broadcast();
	}
	//鼠标处理
	if (UGolbalBPFunctionLibrary::CustomCursorManager())
	{
		UGolbalBPFunctionLibrary::CustomCursorManager()->OnHideMouse();
	}
}

void UGUIManager::OnRoleFirstEnterGame()
{
	//打开选择操作模式界面
	UGolbalBPFunctionLibrary::GUIManager()->OpenWindow(false, EGameStatus::InWorld, TEXT("OperationTutorial"));
}

void UGUIManager::OnLeaveSpaceNotify()
{
	TArray<FString> NeedDestroy;
	NeedDestroy.Empty();
	for (TArray<UBaseWindow*>::TConstIterator aiter = AllWindows.CreateConstIterator(); aiter; ++aiter)
	{
		UBaseWindow* Window = *aiter;
		if (IsValid(Window))
		{
			FUIConfigData* ConfigData = GetUIConfigDataByWindowType(Window->WindowType);
			if (ConfigData)
			{
				switch (ConfigData->DestroyType)
				{
				case 0://销毁
				{
					//不能在这里直接Destroy，Destroy会销毁对象，迭代器存储可以变动，但存储的对象销毁也会造成如 在普通循环体中删除 一样的BUG，某些界面关不掉
					NeedDestroy.Add(Window->WindowType);
					break;
				}
				case 1://隐藏
				{
					Window->Hide();
					break;
				}
				default:
					break;
				}
			}
		}
	}

	//销毁
	for (auto WindowType : NeedDestroy)
	{
		UBaseWindow* Window = GetWindow(WindowType);
		if (IsValid(Window))
		{
			Window->Destroy();
		}
	}
}

void UGUIManager::ShowRootUI()
{
	if (!RootUIWidget)
	{
		ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
		if (!IsValid(PlayerController))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UGUIManager::ShowRootUI : PlayerController!"));
			return;
		}
		URootUIWidget* Widget = Cast<URootUIWidget>(CreateWidget<UUserWidget>(PlayerController, UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_RootUIWidget"))));
		RootUIWidget = Widget;
	}
	if (RootUIWidget && !RootUIWidget->IsInViewport())
	{
		RootUIWidget->AddToViewport(0);
	}
}

void UGUIManager::AddToRootUI(UBaseWindow* Window, FVector2D Position)
{
	if (RootUIWidget)
	{
		RootUIWidget->AddToRootUI(Window, Position);
	}
}

void UGUIManager::SetRootUIVisible(ESlateVisibility InVisibility)
{
	if (RootUIWidget)
	{
		RootUIWidget->SetRootUIVisible(InVisibility);
	}
}

void UGUIManager::AddWindowToManager(UBaseWindow* window, FString WindowType)
{
	if (WindowType == TEXT("")) return;
	int zseg = window->PosZSegment;
	window->WindowType = WindowType;
	if (!FindArrayByItem(window, GetWindows()))
	{
		if (!UIMaps.Contains(zseg))
		{
			UIMaps.Add(zseg, {});
		}
		UIMaps[zseg].Add(window);
		AllWindows.Add(window);
	}
	window->PosZ = UIMaps[zseg].Num();
	if (window->IsVisible())
	{
		AddVSWindow(window);
	}
}

void UGUIManager::RemoveWindowFromManager(UBaseWindow* window)
{
	if (FindArrayByItem(window, GetWindows()))
	{
		int zseg = window->PosZSegment;
		UIMaps[zseg].Remove(window);
	}
	RemoveVSWindow(window);
	if (IsActWindow(window))
	{
		ActiveTopWindow();
	}
	AllWindows.Remove(window);
	RemoveBeforeHideVSWindow(window);
	HiddenVSWindows.Remove(window);
}

bool UGUIManager::ActiveWindow(UBaseWindow* window, bool upgrade /*= true*/)
{
	if (!window)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGUIManager::ActiveWindow : window!"));
		return false;
	}
	if (!window->IsVisible() || !window->bActivable || !FindArrayByItem(window, GetWindows()))
	{
		return false;
	}
	if (upgrade)
	{
		UpgradeWindow(window);
	}
	if (IsActWindow(window))
	{
		return true;
	}
	InactiveWindow();
	CurrActWindow = window;
	CurrActWindow->NativeOnAfterActived();
	return true;
}

bool UGUIManager::InactiveWindow(UBaseWindow* window /*= nullptr*/)
{
	if (!CurrActWindow)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGUIManager::InactiveWindow : CurrActWindow!"));
		return false;
	}
	if (!IsValid(window) || IsActWindow(window))
	{
		CurrActWindow = nullptr;
		return true;
	}
	return false;
}

void UGUIManager::UpgradeWindow(UBaseWindow* window)
{
	if (!window)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGUIManager::UpgradeWindow : window!"));
		return;
	}
	int zseg = window->PosZSegment;
	if (!UIVSMaps.Contains(zseg)) return;
	TArray<UBaseWindow*> vsArr = UIVSMaps[zseg];
	Relayout(vsArr, window->PosZ);	// 重新排列同层窗口的层次关系
	int count = vsArr.Num();
	window->PosZ = count;
	RefreshWindowsZOrder(zseg);
}

void UGUIManager::OnWindowShow(UBaseWindow* window)
{
	AddVSWindow(window);
	UpgradeWindow(window);
	if (window->bActivable)
	{
		ActiveWindow(window, false);
	}
}

void UGUIManager::OnWindowHide(UBaseWindow* window)
{
	RemoveVSWindow(window);
	if (IsActWindow(window))
	{
		ActiveTopWindow();
	}
}

void UGUIManager::OnWindowDestroy(UBaseWindow* window)
{
	//从管理器中去掉
	RemoveWindowFromManager(window);			
}

void UGUIManager::OnZSegmentChanged(UBaseWindow* window, int oldSeg, int newSeg)
{
	TArray<UBaseWindow*> wins = UIMaps[oldSeg];
	if (FindArrayByItem(window, GetWindows()))
	{
		wins.Remove(window);
		UIMaps[newSeg].Add(window);
	}
	wins = UIVSMaps[oldSeg];
	if (FindArrayByItem(window, GetVSWindows()))
	{
		wins.Remove(window);
		UIVSMaps[newSeg].Add(window);
	}
}

void UGUIManager::AddVSWindow(UBaseWindow* window)
{
	if (!FindArrayByItem(window, GetVSWindows()))
	{
		int zseg = window->PosZSegment;
		if (!UIVSMaps.Contains(zseg))
		{
			UIVSMaps.Add(zseg, {});
		}
		UIVSMaps[zseg].Add(window);
		AllVSWindows.Add(window);
	}
}

void UGUIManager::AddHiddenVSWindows(UBaseWindow* window)
{
	if(!HiddenVSWindows.Contains(window))
	{
		HiddenVSWindows.Add(window);
	}
}

void UGUIManager::SetCanShowWindowTypes(TArray<FString> WindowTypes)
{
	CanShowWindowTypes = WindowTypes;
}

void UGUIManager::ClearCanShowWindowTypes()
{
	CanShowWindowTypes.Empty();
}

TArray<FString> UGUIManager::GetCanShowWindowTypes()
{
	return CanShowWindowTypes;
}

void UGUIManager::RemoveVSWindow(UBaseWindow* window)
{
	if (FindArrayByItem(window, GetVSWindows()))
	{
		int zseg = window->PosZSegment;
		UIVSMaps[zseg].Remove(window);
		AllVSWindows.Remove(window);
	}
}

void UGUIManager::AddBeforeHideVSWindow(UBaseWindow* window)
{
	if (!HiddenVSWindows.Contains(window) && !BeforeHideVSWindows.Contains(window))
	{ 
		if (window && window->IsStoryHide())
		{
			BeforeHideVSWindows.Add(window);
		}
	}
}

void UGUIManager::RemoveBeforeHideVSWindow(UBaseWindow* window)
{
	if (BeforeHideVSWindows.Num() > 0 && BeforeHideVSWindows.Contains(window))
	{
		BeforeHideVSWindows.Remove(window);
	}	
}

void UGUIManager::ActiveTopWindow()
{
	UBaseWindow* window = nullptr;
	TArray<UBaseWindow*> winArr = GetVSWindows();
	for (int i = 0; i < winArr.Num(); i++)
	{
		//找出第一个可被激活的窗口
		if (winArr[i]->bActivable)
		{
			window = winArr[i];
			break;
		}
	}
	if (window)
	{
		ActiveWindow(window, true);
	}
	else
	{
		InactiveWindow();
	}
}

bool UGUIManager::OrderHideWindows()
{
	for (auto win : GetVSWindows())		//遍历所有可见窗口
	{
		if (win->bEscHide)				//如果窗口允许按 esc 键隐藏
		{
			win->OrderHide();				//则隐藏窗口
			return true;				//返回隐藏成功
		}
	}
	return false;						//返回隐藏不成功
}

void UGUIManager::BeforeStatusChanged(EGameStatus oldStatus, EGameStatus newStatus)
{
	for (auto win : GetWindows())						//遍历所有窗口
	{
		win->BeforeStatusChanged(oldStatus, newStatus);//让状态改变通知所有窗口
	}
}

void UGUIManager::AfterStatusChanged(EGameStatus oldStatus, EGameStatus newStatus)
{
	for (auto win : GetWindows())						//遍历所有窗口
	{
		win->AfterStatusChanged(oldStatus, newStatus);	//让状态改变通知所有窗口
	}
}

void UGUIManager::OnRoleEnterWorld()
{
	//通知位置管理器
	UUECS3GameInstance::Instance->UIFixerManager->OnRoleEnterWorld();
	//遍历所有窗口
	for (auto win : UGolbalBPFunctionLibrary::GUIManager()->GetWindows())
	{
		//通知窗口
		win->NativeOnEnterWorld();
	}
	//通知功能开启管理器
	UUECS3GameInstance::Instance->SystemSwitchManager->OnEnterWorld();
	//通知新手指引管理器
	UUECS3GameInstance::Instance->TutorialManager->OnEnterWorld();
}

void UGUIManager::OnRoleLeaveWorld()
{
	if (UUECS3GameInstance::Instance->bIsShutDown)
	{
		return;
	}
	//遍历所有窗口
	for (auto win : GetWindows())						
	{
		//通知所有窗口角色已离开世界
		win->NativeOnLeaveWorld();
		if (win->WindowType != TEXT("SwitchScene"))
		{
			if (win->IsVisible())
			{
				//隐藏窗口(进度条窗口除外)
				win->Hide();								
			}
		}									
	}
	BeforeHideVSWindows.Empty();
	CanShowWindowTypes.Empty();
	//通知功能开启管理器
	UUECS3GameInstance::Instance->SystemSwitchManager->OnLeaveWorld();
	//通知新手指引管理器
	UUECS3GameInstance::Instance->TutorialManager->OnLeaveWorld();
}

TArray<UBaseWindow*> UGUIManager::GetWindows()
{
	return AllWindows;
}

TArray<UBaseWindow*> UGUIManager::GetVSWindows()
{
	SortVSWindows();
	
	return AllVSWindows;
}

UBaseWindow* UGUIManager::GetActWindow()
{
	return CurrActWindow;
}

/*
TMap<int, TArray<UBaseWindow*> > UGUIManager::GetWindowsTree(UBaseWindow* window)
{
	UBaseWindow* owner = window;
	while (true)
	{
		if (!owner->WndParent) break;
		owner = owner->WndParent;
	}
	TMap<int, TArray<UBaseWindow*> > wnds = GetSubWindows(owner, window);
	float zseg = owner->PosZSegment;
	if (!wnds.Contains(zseg))
	{
		wnds.Add(zseg, {});
	}
	wnds[zseg].Add(owner);
	return wnds;
}

TMap<int, TArray<UBaseWindow*> > UGUIManager::GetSubWindows(UBaseWindow* parent, UBaseWindow* window)
{
	TMap<int, TArray<UBaseWindow*> > wnds = {};
	TArray<UBaseWindow*> traveleds = {};					//临时保存已经遍历的窗口
	TArray<UBaseWindow*> stack;								//创建一个临时栈
	stack.Push(parent);										//指定窗口入栈
	while (stack.Num() > 0)
	{
		UBaseWindow* topWin = stack.Top();					//获取栈顶窗口
		TArray<UBaseWindow*> subWindows = topWin->SubWindows;
		bool isTraveled = traveleds.Find(topWin) < 0 ? false : true;			//栈顶的窗口是否遍历过
		if (!isTraveled && subWindows.Num() > 0)			//如果栈顶的窗口还没遍历过
		{
			traveleds.Add(topWin);
			subWindows.Sort([](const UBaseWindow& win1, const UBaseWindow& win2) { return win1.PosZ > win2.PosZ; });//按 Z 轴坐标顺序重新排列所有同层窗口
			for (int i = 0; i < subWindows.Num(); i++)
			{
				if (subWindows[i]->WindowType == window->WindowType)
				{
					subWindows.Remove(window);
					subWindows.Add(window);					//将指定的窗口放到最前面
					break;
				}
			}
			for (int i = 0; i < subWindows.Num(); i++)		//循环遍历 指定窗口 或 某子窗口 的子窗口
			{
				int zseg = subWindows[i]->PosZSegment;
				if (!wnds.Contains(zseg) || wnds[zseg].Find(subWindows[i]) == -1)//如果该子窗口不在子窗口列表中
				{
					stack.Push(subWindows[i]);				//则入栈
				}
			}
		}
		else if (topWin != parent && topWin->IsVisible())		//如果栈顶的窗口已经遍历过，并且不是最底层的窗口
		{
			UBaseWindow* popWin = stack.Pop();
			int zseg = popWin->PosZSegment;
			TArray<UBaseWindow*> layerWindows = wnds[zseg];
			if (layerWindows.Num() > 0)
			{
				layerWindows.Add(popWin);				//则将该窗口出栈并添加到子窗口列表中
			}
			else
			{
				wnds.Add(zseg, {});
				wnds[zseg].Add(popWin);
			}
		}
		else
		{
			stack.Pop();									//出栈
		}
	}
	return wnds;											//返回各层次子窗口列表
}
*/
bool UGUIManager::FindArrayByItem(UBaseWindow* window, TArray<UBaseWindow*> winsArray)
{
	return winsArray.Find(window) < 0 ? false : true;
}

void UGUIManager::CheckApplicationActivation(bool bIsActive)
{
	if (!bIsActive)
	{
		//清除当前的focus
		FSlateApplication::Get().ClearKeyboardFocus(EFocusCause::SetDirectly);
	}
}

bool UGUIManager::IsActWindow(UBaseWindow* window)
{
	if (!CurrActWindow || !window)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGUIManager::IsActWindow : CurrActWindow||window!"));
		return false;
	}
	if (window == CurrActWindow)
	{
		return true;
	}
	return false;
}

void UGUIManager::HideVSWindows()
{
	for (auto win : GetVSWindows())
	{
		win->Hide();
	}
}

void UGUIManager::HideOrShowVSWindows(bool bHide)
{	
	if (bHide)
	{
		if (BeforeHideVSWindows.Num() == 0)
		{
			TArray<UBaseWindow*> TempVSWindows = GetVSWindows();
			for (auto win : TempVSWindows)
			{
				AddBeforeHideVSWindow(win);
				win->StoryHide();
			}
		}
	}
	else
	{
		if (!bIsHideAllUI && BeforeHideVSWindows.Num() > 0)
		{
			Algo::Reverse(BeforeHideVSWindows);
			for (auto win : BeforeHideVSWindows )
			{
				win->Show(win->LastParentWindowType);
			}
			BeforeHideVSWindows.Empty();
		}
	}
}

void UGUIManager::SetIsHideAllUI(bool bIsHide)
{
	bIsHideAllUI = bIsHide;
}

bool UGUIManager::GetIsHideAllUI()
{
	return bIsHideAllUI;
}

bool UGUIManager::IsCanShowWindowState()
{
	//隐藏所有界面状态
	if (bIsHideAllUI)
	{
		return false;
	}
	//剧情中隐藏界面
	if (UGolbalBPFunctionLibrary::GStoryManager() && UGolbalBPFunctionLibrary::GStoryManager()->IsNeedHideUI())
	{
		return false;
	}
	//视频媒体中隐藏界面
	if (UGolbalBPFunctionLibrary::MediaPlayerManager() && UGolbalBPFunctionLibrary::MediaPlayerManager()->IsNeedHideUI())
	{
		return false;
	}
	return true;
}

bool UGUIManager::IsShowVSWindows()
{
	if (bIsHideAllUI)
	{
		return false;
	}
	if (BeforeHideVSWindows.Num() > 0)
	{
		return false;
	}
	return true;
}

void UGUIManager::InitUIConfigData()
{
	auto CfgManager = UUECS3GameInstance::Instance->CfgManager;
	ConfigDataTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_UI)->GetBaseTable();
}

FUIConfigData* UGUIManager::GetUIConfigDataByWindowType(FString WindowType)
{
	if (!IsValid(ConfigDataTable))
	{
		InitUIConfigData();
	}
	if (ConfigDataTable)
	{
		for (auto data : ConfigDataTable->GetRowNames())
		{
			FUIConfigData* configData = (FUIConfigData*)ConfigDataTable->FindRowUnchecked(*data.ToString());
			if (WindowType == configData->WinType)
			{
				return configData;
			}
		}
	}
	return nullptr;
}

UBaseWindow* UGUIManager::SynchronousCreateWindow(FString WindowType)
{
	FUIConfigData* ConfigData = GetUIConfigDataByWindowType(WindowType);
	if (ConfigData)
	{
		UClass* WidgetClass = ConfigData->Widget.Get();
		if (!IsValid(WidgetClass) && IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->ResourceManager))
		{
			//同步加载
			WidgetClass = UUECS3GameInstance::Instance->ResourceManager->SynchronousLoadClass(ConfigData->Widget);
		}
		if (!IsValid(WidgetClass))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UGUIManager::SynchronousCreateWindow : Load WindowClass Fail!"));
			return nullptr;
		}
		return CreateBaseWindow(WidgetClass, ConfigData);
	}
	else
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGUIManager::SynchronousCreateWindow : ConfigData!"));
	}
	return nullptr;
}

UBaseWindow* UGUIManager::CreateBaseWindow(UClass* WidgetClass, FUIConfigData* ConfigData)
{
	if (!IsValid(WidgetClass) || ConfigData == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGUIManager::CreateBaseWindow : Load WindowClass Fail!"));
		return nullptr;
	}
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGUIManager::CreateBaseWindow : PlayerController!"));
		return nullptr;
	}
	UBaseWindow* NewWindow = Cast<UBaseWindow>(CreateWidget<UUserWidget>(PlayerController, WidgetClass));
	if (IsValid(NewWindow))
	{
		NewWindow->InitConfigData(*ConfigData);
		//添加到管理器
		AddWindowToManager(NewWindow, NewWindow->WindowType);
		//因为聊天子频道制作不符合设计，导致子频道界面比较特殊，并不需要add到RootUI上，先排除掉，待后续优化了聊天子频道再做处理
		if (NewWindow->WindowType != TEXT("ChatChild"))
		{
			//添加到RootUI，需要先将对象add到父节点上，对对象的设置（比如初始化）才有用
			AddToRootUI(NewWindow, FVector2D::ZeroVector);
		}
		//界面初始化
		NewWindow->Init();
		if (NewWindow->WindowType != TEXT("ChatChild"))
		{
			//界面隐藏
			NewWindow->SetVisibility(ESlateVisibility::Collapsed);
		}
		//通知窗口停靠管理器
		if (UUECS3GameInstance::Instance->UIDockManager)
		{
			UUECS3GameInstance::Instance->UIDockManager->OnWindowCreatedOver(NewWindow->WindowType);
		}
	}
	return NewWindow;
}

void UGUIManager::AsyncLoadWindowAsset(FOnLoadComplete DelegateToCall, FString WindowType, FString ParentType /*= TEXT("")*/)
{
	//异步加载
	FUIConfigData* ConfigData = GetUIConfigDataByWindowType(WindowType);
	if (!ConfigData)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGUIManager::AsyncOpenWindow : ConfigData!"));
		return;
	}
	TWeakObjectPtr<UGUIManager> DelayThisPtr(this);
	if (!IsValid(ConfigData->Widget.Get()))
	{
		TArray<FSoftObjectPath> TargetsToStream;
		TargetsToStream.AddUnique(ConfigData->Widget.ToSoftObjectPath());
		if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->ResourceManager))
		{
			UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(this, TargetsToStream,
				FStreamableDelegate::CreateLambda([DelayThisPtr, WindowType, ParentType, ConfigData, TargetsToStream, DelegateToCall]()
			{
				TArray<UObject *> LoadedResourceArray;
				for (int32 i = 0; i < TargetsToStream.Num(); i++)
				{
					FStringAssetReference AssetReference = TargetsToStream[i];
					UObject* NewObject = AssetReference.ResolveObject();
					if (IsValid(NewObject))
					{
						LoadedResourceArray.AddUnique(NewObject);
					}
				}
				UClass* WidgetClass = Cast<UClass>(LoadedResourceArray[0]);
				if (DelegateToCall.IsBound())
				{
					DelegateToCall.Execute(WindowType, ParentType, WidgetClass, ConfigData, DelayThisPtr);
				}
			}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_DEFAULT);
		}
	}
	else if (DelegateToCall.IsBound())
	{
		UClass* WidgetClass = Cast<UClass>(ConfigData->Widget.Get());
		DelegateToCall.Execute(WindowType, ParentType, WidgetClass, ConfigData, DelayThisPtr);
	}
}

void UGUIManager::Relayout(TArray<UBaseWindow*> windows, int oldZOrder)
{
	int count = windows.Num();
	if (count == 0) return;
	for (auto& item : windows)
	{
		if (item && item->PosZ > oldZOrder)
		{
			item->PosZ = item->PosZ - 1;
		}
	}
}

void UGUIManager::RefreshWindowsZOrder(int32 PosZSegment)
{
	if (RootUIWidget)
	{
		RootUIWidget->RefreshChildZOrder(PosZSegment);
	}
}

void UGUIManager::SortVSWindows()
{
	AllVSWindows.Sort([](const UBaseWindow& win1, const UBaseWindow& win2)
	{
		if (win1.PosZSegment == win2.PosZSegment)//同层
		{
			return win1.PosZ > win2.PosZ;
		}
		else
		{
			return win1.PosZSegment > win2.PosZSegment;
		}
	});
}
CONTROL_COMPILE_OPTIMIZE_END
