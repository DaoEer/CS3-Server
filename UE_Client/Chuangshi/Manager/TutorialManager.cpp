// Fill out your copyright notice in the Description page of Project Settings.


#include "TutorialManager.h"
// UE4
#include"Chuangshi.h"
#include "Blueprint/SlateBlueprintLibrary.h"
#include "Blueprint/WidgetLayoutLibrary.h"
#include "Components/VerticalBoxSlot.h"
#include "Components/CanvasPanelSlot.h"
// 数据类型
#include "GameData/TutorialData.h"
#include "GameData/Item/Equip.h"
// CS3类型
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/ConvertUtil.h"
#include "Interface/Role/RoleKitBagInterface.h"
#include "GameDevelop/CS3PlayerController.h"
#include "CS3Base/UIManager.h"
#include "CS3Base/RootUIWidget.h" 
#include "QuestManager.h"
#include "CustomTimerManager.h"
#include "AudioManager.h"
#include "ResourceManager.h"
#include "QuickBarManager.h"
#include "Engine/UserInterfaceSettings.h"

CONTROL_COMPILE_OPTIMIZE_START

UTutorialManager* UTutorialManager::Instance = nullptr;

UTutorialManager* UTutorialManager::GetInstance()
{
	cs3_checkNoReentry();
	return (UTutorialManager*)StaticConstructObject_Internal(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_TutorialManager")));

}

void UTutorialManager::LoadCfg()
{
	TriggerDatasMap.Empty();
	if (!UGolbalBPFunctionLibrary::CfgManager())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::LoadCfg : CfgManager()s!"));
		return;
	}
	const UConfigTable* ConfigTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TRIGGER_TIPS);
	if (!ConfigTable)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::LoadCfg : ConfigTable!"));
		return;
	}
	TArray<FName> Rows = ConfigTable->GetRowNames();
	if (Rows.Num() <= 0) return;
	for (FName& Row : Rows)
	{
		const FTUTORIALDATA* Data = ConfigTable->GetRow<FTUTORIALDATA>(Row);
		if (!Data)
		{
			CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::LoadCfg : Data!"));
			return;
		}
		if (!TriggerDatasMap.Contains(Data->TriggerType))
		{
			FTutorialMap Datas;
			TriggerDatasMap.Add(Data->TriggerType, Datas);
		}
		if (TriggerDatasMap[Data->TriggerType].Datas.Contains(Data->KeyIndex))
		{
			CS3_Warning(TEXT("TutorialCfg Table has two same KeyIndex[%s]"), *(Data->KeyIndex.ToString()));
		}
		//程序赋值KeyIndex
		FTUTORIALDATA* TempData = const_cast<FTUTORIALDATA*>(Data);
		for (FTriggerCondition& Item : TempData->TriggerCnds)
		{
			Item.CndParams.KeyIndex = Data->KeyIndex;
		}
		for (FCloseCondition& Item : TempData->CloseCnds)
		{
			Item.CndParams.KeyIndex = Data->KeyIndex;
		}
		for (FTriggerTutorialAction& Item : TempData->TriggerActs)
		{
			Item.ActParams.KeyIndex = Data->KeyIndex;
			for (FTriggerCondition& Cnd : Item.TriggerCnds)
			{
				Cnd.CndParams.KeyIndex = Data->KeyIndex;
			}
		}
		//加入到指引数据
		TriggerDatasMap[Data->TriggerType].Datas.Add(Data->KeyIndex, *TempData);
	}
}

FTUTORIALDATA UTutorialManager::GetTutorialDataByKeyIndex(FName KeyIndex, bool& IsSuccess)
{
	for (TPair<ETUTORIALTRIGGERTYPE, FTutorialMap>& TutorialMap : TriggerDatasMap)
	{
		TMap<FName, FTUTORIALDATA>& Datas = TutorialMap.Value.Datas;
		for (TPair<FName, FTUTORIALDATA>& TutorialData : Datas)
		{
			if (TutorialData.Key == KeyIndex)
			{
				IsSuccess = true;
				return TutorialData.Value;
			}
		}
	}
	IsSuccess = false;
	return FTUTORIALDATA();
}

void UTutorialManager::ClearDoOnceEvents(TArray<FString> Indexs)
{
	for (TPair<ETUTORIALTRIGGERTYPE, FTutorialMap>& Item : TriggerDatasMap)
	{
		TArray<FString> TempIndexs = Indexs;
		for (FString& Index : Indexs)
		{
			if (Item.Value.Datas.Contains(FSTRING_TO_FNAME(Index)))
			{
				Item.Value.Datas.Remove(FSTRING_TO_FNAME(Index));
				TempIndexs.Remove(Index);
			}
		}
		//清除Remove之后产生的无效数据
		Item.Value.Datas.Compact();
		Item.Value.Datas.Shrink();

		//如果全找完了，则结束
		if (TempIndexs.Num() <= 0) break;
	}
}

#pragma region	/** 查找控件相关 */

UWidget * UTutorialManager::GetWidgetFromWidgetPath(int32 UIType, const FString & WidgetPath)
{
	if (UIType == 1)
	{
		return GetWidgetFromAccurateWidgetPath(WidgetPath);
	}
	else if(UIType == 2)
	{
		return GetWidgetFromDynamicWidgetPath(WidgetPath);
	}
	return nullptr;
}

UWidget * UTutorialManager::GetWidgetFromAccurateWidgetPath(const FString & WidgetPath)
{
	if (!UGolbalBPFunctionLibrary::GUIManager())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::GetWidgetFromAccurateWidgetPath : GUIManager()!"));
		return nullptr;
	}
	TArray<FString> PathArray = UGolbalBPFunctionLibrary::SplitString(WidgetPath, true, ".");
	UWidget* TempWidget = nullptr;
	for (int32 i = 0; i < PathArray.Num(); i++)
	{
		if (i == 0)
		{
			FString WindowType = PathArray[i];
			TempWidget = Cast<UWidget>(UGolbalBPFunctionLibrary::GUIManager()->GetWindow(WindowType));
			continue;
		}
		if (!IsValid(TempWidget))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::GetWidgetFromAccurateWidgetPath : TempWidget!"));
			return nullptr;
		}
		else
		{
			TempWidget = Cast<UUserWidget>(TempWidget)->GetWidgetFromName(FSTRING_TO_FNAME(PathArray[i]));
		}
	}
	if (!IsValid(TempWidget))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::GetWidgetFromAccurateWidgetPath : TempWidget!"));
		return nullptr;
	}
	return TempWidget;
}

UWidget * UTutorialManager::GetWidgetFromDynamicWidgetPath(const FString & WidgetPath)
{
	if (!UGolbalBPFunctionLibrary::GUIManager())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::GetWidgetFromDynamicWidgetPath : GUIManager()!"));
		return nullptr;
	}
	TArray<FString> PathArray = UGolbalBPFunctionLibrary::SplitString(WidgetPath, true, ".");
	UWidget* TempWidget = nullptr;
	UBaseWindow* RootWindow = nullptr;
	for (int32 i = 0; i < PathArray.Num(); i++)
	{
		if (i == 0)
		{
			FString WindowType = PathArray[i];
			RootWindow = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(WindowType);
			TempWidget = Cast<UWidget>(RootWindow);
			continue;
		}
		if (!IsValid(TempWidget))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::GetWidgetFromDynamicWidgetPath : TempWidget!"));
			return nullptr;
		}
		FString WindowName = TEXT("");
		//背包，需要将物品ID转为绝对位置
		if (RootWindow->WindowType == TEXT("KitBag") && i == 1)
		{
			WindowName = AppendWidgetName(RootWindow, WidgetPath, i);
		}
		//任务追踪，需要拼凑任务目标ID，配置：TaskTrack.20101013.1，变成TaskTrack.20101013.201010131
		else if (RootWindow->WindowType == TEXT("TaskTrack") && i == 2)
		{
			WindowName = AppendWidgetName(RootWindow, WidgetPath, i);
		}
		//快捷栏，需要将药品或技能ID转为绝对位置
		else if (RootWindow->WindowType == TEXT("SkillBar") && i == 1)
		{
			WindowName = AppendWidgetName(RootWindow, WidgetPath, i);
		}
		else
		{
			WindowName = PathArray[i];
		}
		TempWidget = Cast<UUserWidget>(TempWidget)->GetWidgetFromName(FSTRING_TO_FNAME(WindowName));
	}
	if (!IsValid(TempWidget))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::GetWidgetFromAccurateWidgetPath : GetWidgetFromDynamicWidgetPath!"));
		return nullptr;
	}
	return TempWidget;
}

FString UTutorialManager::AppendWidgetName(UBaseWindow* RootWindow, const FString& WidgetPath, int32 Index)
{
	if (!IsValid(RootWindow) || WidgetPath == TEXT(""))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::AppendWidgetName : RootWindow||WidgetPath == TEXT("")!"));
		return TEXT("");
	}
	TArray<FString> PathArray = UGolbalBPFunctionLibrary::SplitString(WidgetPath, true, ".");
	if (Index > (PathArray.Num() - 1))
	{
		return TEXT("");
	}
	FString WindowName = TEXT("");
	//背包
	if (RootWindow->WindowType == TEXT("KitBag"))
	{
		URoleKitBagInterface* kbinterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
		if (!IsValid(kbinterface))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::AppendWidgetName : kbinterface!"));
			return TEXT("");
		}
		int32 AbsOrderId = kbinterface->GetAbsOrderIdByItemID(FSTRING_TO_INT(PathArray[Index]));
		WindowName = TEXT("BagSlot") + INT_TO_FSTRING(AbsOrderId);
	}
	//任务追踪
	else if (RootWindow->WindowType == TEXT("TaskTrack"))
	{
		WindowName = PathArray[Index - 1] + PathArray[Index];
	}
	//快捷栏
	else if (RootWindow->WindowType == TEXT("SkillBar"))
	{
		if (!IsValid(UUECS3GameInstance::Instance) || !IsValid(UUECS3GameInstance::Instance->QuickBarManager))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::AppendWidgetName : QuickBarManager!"));
			return TEXT("");
		}
		int32 SlotIndex;
		FString LocalParam = PathArray[Index];
		if (LocalParam.Contains(TEXT("EmptySlot")))
		{
			//参数是第几个空格子，从EmptySlot3获取出3，表示第3个
			FString EmptyIndex = LocalParam.Mid(9, LocalParam.Len() - 9);
			SlotIndex = UUECS3GameInstance::Instance->QuickBarManager->GetQuickBarSlotIndex(FSTRING_TO_INT(EmptyIndex));
		}
		else
		{
			//参数是技能或物品ID
			SlotIndex = UUECS3GameInstance::Instance->QuickBarManager->GetIndexByQBID(FSTRING_TO_INT(LocalParam));
		}
		WindowName = TEXT("SkillSlot_") + INT_TO_FSTRING(SlotIndex);
		CS3_Warning(TEXT("-->QuickBarTest:UTutorialManager::AppendWidgetName : %s"), *WindowName);
	}
	return WindowName;
}

UBaseWindow * UTutorialManager::GetParentWindowFromWidgetPath(const FString & WidgetPath)
{
	if (!UGolbalBPFunctionLibrary::GUIManager())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::GetParentWindowFromWidgetPath : GUIManager()!"));
		return nullptr;
	}
	TArray<FString> PathArray = UGolbalBPFunctionLibrary::SplitString(WidgetPath, true, ".");
	if (PathArray.Num() > 0)
	{
		return UGolbalBPFunctionLibrary::GUIManager()->GetWindow(PathArray[0]);
	}
	return nullptr;
}

#pragma endregion

#pragma region	/** 获取控件位置和尺寸相关 */

FVector2D UTutorialManager::GetWidgetPosition(int32 UIType, const FString& WidgetPath)
{
	UBaseWindow* ParentWidget = GetParentWindowFromWidgetPath(WidgetPath);
	if (!IsValid(ParentWidget))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::GetWidgetPosition : ParentWidget!"));
		return FVector2D(0.0, 0.0);
	}
	UWidget* Widget = GetWidgetFromWidgetPath(UIType, WidgetPath);
	if (!IsValid(Widget))
	{
		return FVector2D(0.0, 0.0);
	}
	FVector2D PixelPosition;	//控件左上角的位置
	FVector2D ViewportPosition;	//控件左上角的位置
								//GetCachedGeometry只有在widget是显示的时候才能获取正确的位置，大小信息
	USlateBlueprintLibrary::LocalToViewport(GetWorld(), Widget->GetCachedGeometry(), FVector2D(0.0, 0.0), PixelPosition, ViewportPosition);
	FVector2D ParentPixelPosition;		//父控件左上角的位置
	FVector2D ParentViewportPosition;	//父控件左上角的位置
	USlateBlueprintLibrary::LocalToViewport(GetWorld(), ParentWidget->GetCachedGeometry(), FVector2D(0.0, 0.0), ParentPixelPosition, ParentViewportPosition);

	FVector2D Position = ViewportPosition - ParentViewportPosition;  //在父控件上的位置
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("UTutorialManager::GetWidgetPosition[%s], WidgetPath=%s"), *(Position.ToString()), *WidgetPath);
	return Position;
}

FVector2D UTutorialManager::GetWidgetPositionInRootUI(int32 UIType, const FString& WidgetPath)
{
	if (!UGolbalBPFunctionLibrary::GUIManager()) return FVector2D(0.0, 0.0);
	UCS3UserWidget* ParentWindow = UGolbalBPFunctionLibrary::GUIManager()->RootUIWidget;
	if (!IsValid(ParentWindow))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::GetWidgetPositionInRootUI : ParentWindow!"));
		return FVector2D(0.0, 0.0);
	}
	UWidget* Widget = GetWidgetFromWidgetPath(UIType, WidgetPath);
	if (!IsValid(Widget))
	{
		return FVector2D(0.0, 0.0);
	}
	FVector2D PixelPosition;	//控件左上角的位置
	FVector2D ViewportPosition;	//控件左上角的位置
								//GetCachedGeometry只有在widget是显示的时候才能获取正确的位置，大小信息
	USlateBlueprintLibrary::LocalToViewport(GetWorld(), Widget->GetCachedGeometry(), FVector2D(0.0, 0.0), PixelPosition, ViewportPosition);
	FVector2D ParentPixelPosition;		//父控件左上角的位置
	FVector2D ParentViewportPosition;	//父控件左上角的位置
	USlateBlueprintLibrary::LocalToViewport(GetWorld(), ParentWindow->GetCachedGeometry(), FVector2D(0.0, 0.0), ParentPixelPosition, ParentViewportPosition);

	FVector2D Position = ViewportPosition - ParentViewportPosition;  //在父控件上的位置
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("UTutorialManager::GetWidgetPosition[%s], WidgetPath=%s"), *(Position.ToString()), *WidgetPath);
	return Position;
}

FVector2D UTutorialManager::GetWidgetPositionInViewport(int32 UIType, const FString& WidgetPath)
{
	UWidget* Widget = GetWidgetFromWidgetPath(UIType, WidgetPath);
	if (!IsValid(Widget))
	{
		return FVector2D(0.0, 0.0);
	}
	FVector2D PixelPosition;	//控件左上角的位置
	FVector2D ViewportPosition;	//控件左上角的位置
	//GetCachedGeometry只有在widget是显示的时候才能获取正确的位置，大小信息
	USlateBlueprintLibrary::LocalToViewport(GetWorld(), Widget->GetCachedGeometry(), FVector2D(0.0, 0.0), PixelPosition, ViewportPosition);
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("Find PositionInViewport:PixelPosition[%s],ViewportPosition[%s]"), *(PixelPosition.ToString()), *(ViewportPosition.ToString()));
	return PixelPosition;
}

FVector2D UTutorialManager::GetWidgetSize(int32 UIType, const FString& WidgetPath)
{
	UWidget* Widget = GetWidgetFromWidgetPath(UIType, WidgetPath);
	if (IsValid(Widget))
	{
		//GetCachedGeometry只有在widget是显示的时候才能获取正确的位置，大小信息
		FVector2D DrawSize = Widget->GetCachedGeometry().GetDrawSize();
		//CS3_Display(CS3DebugType::CL_Undefined, TEXT("UTutorialManager::GetWidgetSize[%s], WidgetPath=%s"), *(DrawSize.ToString()), *WidgetPath);
		return DrawSize;
	}
	CS3_Warning(TEXT("Can't Get Widget Size,Widget is nullptr!"));
	return FVector2D(0.0, 0.0);
}

FVector2D UTutorialManager::GetFilterPos(const FVector2D& Pos, const FVector2D& Size, const FVector2D& WidgetSize, EARROWTYPE ArrowType)
{
	switch (ArrowType)
	{
	case EARROWTYPE::RIGHT_ARROW_TUTORIAL:
	{
		return FVector2D(Pos.X - WidgetSize.X, Pos.Y + (Size.Y - WidgetSize.Y) / 2.0);
	}
	case EARROWTYPE::LEFT_ARROW_TUTORIAL:
	{
		return FVector2D(Pos.X + Size.X, Pos.Y + (Size.Y - WidgetSize.Y) / 2.0);
	}
	case EARROWTYPE::UP_ARROW_TUTORIAL:
	{
		return FVector2D(Pos.X + (Size.X - WidgetSize.X) / 2.0, Pos.Y + Size.Y);
	}
	case EARROWTYPE::DOWN_ARROW_TUTORIAL:
	{
		return FVector2D(Pos.X + (Size.X - WidgetSize.X) / 2.0, Pos.Y - WidgetSize.Y);
	}
	default:
	{
		CS3_Warning(TEXT("Try to get wrong Pos!"));
		return Pos;
	}
	}
}

FVector2D UTutorialManager::GetFilterSize(FString IsShowBox, EARROWTYPE ArrowType)
{
	FVector2D WidgetSize = FVector2D::ZeroVector;
	switch (ArrowType)
	{
	case EARROWTYPE::LEFT_ARROW_TUTORIAL:
	case EARROWTYPE::RIGHT_ARROW_TUTORIAL:
	{
		if (IsShowBox != TEXT(""))
		{
			return FVector2D(255.0, 101.0);
		}
		else
		{
			return FVector2D(74.0, 52.0);
		}
	}
	case EARROWTYPE::UP_ARROW_TUTORIAL:
	case EARROWTYPE::DOWN_ARROW_TUTORIAL:
	{
		if (IsShowBox != TEXT(""))
		{
			return FVector2D(181, 175.0);
		}
		else
		{
			return FVector2D(52.0, 74.0);
		}
	}
	default:
	{
		CS3_Warning(TEXT("Try to get wrong Pos!"));
		return FVector2D::ZeroVector;
	}
	}
}

EARROWTYPE UTutorialManager::GetArrowType(FString ArrowType)
{
	int32 type = FSTRING_TO_INT(ArrowType);
	switch (type)
	{
	case 1:
	{
		return EARROWTYPE::LEFT_ARROW_TUTORIAL;
	}
	case 2:
	{
		return EARROWTYPE::RIGHT_ARROW_TUTORIAL;
	}
	case 3:
	{
		return EARROWTYPE::UP_ARROW_TUTORIAL;
	}
	case 4:
	{
		return EARROWTYPE::DOWN_ARROW_TUTORIAL;
	}
	default:
	{
		CS3_Warning(TEXT("Config ArrowType is wrong!"));
		return EARROWTYPE::RIGHT_ARROW_TUTORIAL;
	}
	}
}

UUserWidget * UTutorialManager::CreateArrowTutorialWidget(EARROWTYPE ArrowType)
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController)) return nullptr;
	switch (ArrowType)
	{
	case EARROWTYPE::LEFT_ARROW_TUTORIAL:
	{
		return CreateWidget<UUserWidget>(PlayerController, UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_LEFTARROW")));
	}
	case EARROWTYPE::RIGHT_ARROW_TUTORIAL:
	{
		return CreateWidget<UUserWidget>(PlayerController, UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_RIGHTARROW")));
	}
	case EARROWTYPE::UP_ARROW_TUTORIAL:
	{
		return CreateWidget<UUserWidget>(PlayerController, UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_UPARROW")));
	}
	case EARROWTYPE::DOWN_ARROW_TUTORIAL:
	{
		return CreateWidget<UUserWidget>(PlayerController, UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_DOWNARROW")));
	}
	default:
	{
		CS3_Warning(TEXT("Try to get wrong ArrowType!"));
		return nullptr;
	}
	}
}

#pragma endregion

#pragma region	/** 点击指引目标相关 */

bool UTutorialManager::CheckInArea(FVector2D LeftTopPos, FVector2D RightBottomPos)
{
	FVector2D MousePosition = FVector2D(0, 0);
	APlayerController* PlayerController = Cast<APlayerController>(UGolbalBPFunctionLibrary::GetCS3PlayerController());
	if (PlayerController)
	{
		PlayerController->GetMousePosition(MousePosition.X, MousePosition.Y);
		//CS3_Display(CS3DebugType::CL_Undefined, TEXT("CheckInArea MousePosition[%s]"), *(MousePosition.ToString()));
		if ((MousePosition.X >= LeftTopPos.X) && (MousePosition.X <= RightBottomPos.X) && (MousePosition.Y >= LeftTopPos.Y) && (MousePosition.Y <= RightBottomPos.Y))
		{
			return true;
		}
	}
	return false;
}

void UTutorialManager::OnTriggerItemClicked()
{
	//CS3_Display(CS3DebugType::CL_Undefined, TEXT("OnTriggerItemClicked[%s]"), *(CurrentShowArrowIndex.ToString()));
	if (HasArrowTutorial())
	{
		FVector2D Position = GetWidgetPositionInViewport(CurrentShowArrowData.UIType, CurrentShowArrowData.UILinkTarget);
		FVector2D Size = GetWidgetSize(CurrentShowArrowData.UIType, CurrentShowArrowData.UILinkTarget);
		bool IsInArea = CheckInArea(Position, FVector2D((Position.X + Size.X), (Position.Y + Size.Y)));
		//CS3_Display(CS3DebugType::CL_Undefined, TEXT("OnTriggerItemClicked[%s],[%s]"), *(Position.ToString()), *(Size.ToString()));
		if (IsInArea)
		{
			//CS3_Display(CS3DebugType::CL_Undefined, TEXT("OnTriggerItemClicked------InArea"));
			bool isWaitFinish = CurrentShowArrowData.isWaitFinish;
			HideCurrentArrowTutorial();
			//如果需要等待功能完成，则点击时不能触发下一步
			if (isWaitFinish) return;
			DoNextArrowAction();
		}
	}
	if (HasImageTutorial())
	{
		if (!CurrentShowImageData.UILinkTarget.Equals(TEXT("")))
		{
			FVector2D Position = GetWidgetPositionInViewport(CurrentShowImageData.UIType, CurrentShowImageData.UILinkTarget);
			FVector2D Size = GetWidgetSize(CurrentShowImageData.UIType, CurrentShowImageData.UILinkTarget);
			bool IsInArea = CheckInArea(Position, FVector2D((Position.X + Size.X), (Position.Y + Size.Y)));
			if (IsInArea)
			{
				bool isWaitFinish = CurrentShowImageData.isWaitFinish;
				HideCurrentImageTutorial();
				//如果需要等待功能完成，则点击时不能触发下一步
				if (isWaitFinish) return;
				DoNextImageAction();
			}
		}
		else
		{
			HideCurrentImageTutorial();
			DoNextImageAction();
		}
	}
}

void UTutorialManager::FinishCurrStep(int32 TutorialType /*= 1*/)
{
	if (TutorialType == 1)
	{
		bool isWaitFinish = CurrentShowArrowData.isWaitFinish;
		HideCurrentArrowTutorial();
		//如果需要等待功能完成，则点击时不能触发下一步
		if (isWaitFinish) return;
		DoNextArrowAction();
	}
	if (TutorialType == 2)
	{
		HideCurrentImageTutorial();
		DoNextImageAction();
	}
	if (TutorialType == 3)
	{
		HideCurrentMessageTutorial();
		DoNextMessageAction();
	}
}

void UTutorialManager::FinishAllStep(int32 TutorialType /*= 1*/)
{
	if (TutorialType == 1)
	{
		//关闭指引
		HideCurrentArrowTutorial();
		//已完成
		OnTutorialFinished(NeedShowMesssageActions.TutorialData);
	}
	if (TutorialType == 2)
	{
		//关闭指引
		HideCurrentImageTutorial();
		//已完成
		OnTutorialFinished(NeedShowMesssageActions.TutorialData);
		//继续指引下一条等待排队的指引
		TriggerNextImage();
	}
	if (TutorialType == 3)
	{
		//关闭指引
		HideCurrentMessageTutorial();
		//已完成
		OnTutorialFinished(NeedShowMesssageActions.TutorialData);
		//继续指引下一条等待排队的指引
		TriggerNextMessage();
	}
}

UObject* UTutorialManager::GetObjectByPath(FString Path)
{
	return (UObject*)UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(FSoftObjectPath(Path));
}

void UTutorialManager::HideTriggerItem(const FName& Index)
{
	if (Index.IsNone())	return;
	if (ShowTriggerWnds.Contains(Index))
	{
		if (ShowTriggerWnds[Index].ShowWndList.Num() > 0)
		{
			for (UUserWidget* Item : ShowTriggerWnds[Index].ShowWndList)
			{
				if (IsValid(Item))
				{
					UBaseWindow* BaseWnd = Cast<UBaseWindow>(Item);
					if (BaseWnd)
					{
						BaseWnd->Destroy();
					}
					else
					{
						Item->RemoveFromParent();
					}
				}
			}
			ShowTriggerWnds.Remove(Index);
		}
	}
	//销毁锁屏
	if (!UGolbalBPFunctionLibrary::GUIManager())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::HideTriggerItem : GUIManager()!"));
		return;
	}
	UBaseWindow* LockScreenWnd = UGolbalBPFunctionLibrary::GUIManager()->GetWindow(TEXT("LockSceneTutorial"));
	if (IsValid(LockScreenWnd))
	{
		LockScreenWnd->Destroy();
	}
	//结束语音
	StopVoice();
}

#pragma endregion

#pragma region	/** 箭头指引相关 */

void UTutorialManager::CheckPanelOpen(const FString& WidgetPath)
{
	IsStartWaitOpenPanel = true;
	WaitOpenWidgetPath = WidgetPath;
	CheckWaitOpenPanelTime = 0.0f;
}

void UTutorialManager::DoArrowAction(const FTUTORIALPARAM & ActParams)
{
	WaitShowData = ActParams;
	if (ActParams.isWaitPanelOpen)
	{
		if (ActParams.Param5 != TEXT(""))
		{
			CheckPanelOpen(ActParams.Param5);
		}
		else
		{
			FString TempStr = INT_TO_FSTRING(ActParams.UIType) + TEXT("|") + ActParams.UILinkTarget;
			CheckPanelOpen(TempStr);
		}
	}
	else
	{
		ShowPanelArrowAction();
	}
}

void UTutorialManager::ShowPanelArrowAction()
{
	HideCurrentArrowTutorial();
	if (WaitShowData.bIsLockScreen)
	{
		ShowLockScreenArrowAction(WaitShowData);
	}
	else
	{
		ShowArrowAction(WaitShowData);
	}
}

void UTutorialManager::ShowArrowAction(const FTUTORIALPARAM& ActParams)
{
	//先判断指引目标是不是存在
	UWidget* TargetWidget = GetWidgetFromWidgetPath(ActParams.UIType, ActParams.UILinkTarget);
	if (!IsValid(TargetWidget))
	{
		//指引目标没有了
		return;
	}

	//触发提示
	FString arg;
	FOutputDeviceNull ar;

	if (!UGolbalBPFunctionLibrary::GUIManager())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::ShowArrowAction : GUIManager()!"));
		return;
	}
	UCS3UserWidget* ParentWindow = nullptr;
	if (ActParams.UILinkTarget == TEXT(""))
	{
		ParentWindow = UGolbalBPFunctionLibrary::GUIManager()->RootUIWidget;
	}
	else
	{
		ParentWindow = UGolbalBPFunctionLibrary::TutorialManager()->GetParentWindowFromWidgetPath(ActParams.UILinkTarget);
	}
	if (!IsValid(ParentWindow))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::ShowArrowAction : ParentWindow!"));
		return;
	}
	//目标的位置和大小
	float ViewportScale = UGolbalBPFunctionLibrary::GetViewportScale();
	FVector2D Pos = GetWidgetPosition(ActParams.UIType, ActParams.UILinkTarget);
	FVector2D Size = GetWidgetSize(ActParams.UIType, ActParams.UILinkTarget);
	Size = Size / ViewportScale;
	//显示箭头指引
	EARROWTYPE ArrowType = GetArrowType(ActParams.Param2);
	UUserWidget* Tips = CreateArrowTutorialWidget(ArrowType);
	if (!IsValid(Tips)) return;
	UPanelSlot* PanelSlot = ParentWindow->AddChild(Tips);
	if (!IsValid(PanelSlot))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::ShowArrowAction : PanelSlot!"));
		return;
	}
	UCanvasPanelSlot* CanvasPanelSlot = Cast<UCanvasPanelSlot>(PanelSlot);
	if (!IsValid(CanvasPanelSlot))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::ShowArrowAction : CanvasPanelSlot!"));
		return;
	}
	CanvasPanelSlot->SetAutoSize(true);
	//根据使用的类型来计算窗口位置
	//FVector2D WidgetSize = Tips->GetCachedGeometry().GetDrawSize();
	FVector2D WidgetSize = GetFilterSize(ActParams.Param4, ArrowType);
	FVector2D FilterPos = GetFilterPos(Pos, Size, WidgetSize, ArrowType);
	CanvasPanelSlot->SetPosition(FilterPos);
	//将指引增加到管理器数组
	AddShowTriggerWnd(ActParams.KeyIndex, Tips);
	//设置提示框标题、内容、是否显示关闭按钮
	arg = TEXT("SetTitleAndContent");
	arg = *FString::Printf(TEXT("%s \"%s\" \"%s\" \"%s\""), *arg, *(ActParams.Param3), *(ActParams.Param4), *(ActParams.Param6));
	Tips->CallFunctionByNameWithArguments(*arg, ar, NULL, true);

	if (ActParams.Param1 == TEXT("1"))
	{
		//显示闪烁框
		ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
		if (!IsValid(PlayerController)) return;
		UUserWidget* HightLight = CreateWidget<UUserWidget>(PlayerController, UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_HighLightBox")));
		if (!IsValid(HightLight)) return;
		PanelSlot = ParentWindow->AddChild(HightLight);
		if (!IsValid(PanelSlot))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::ShowArrowAction : PanelSlot!"));
			return;
		}
		//设置闪烁框的大小，闪烁框边框大约5个像素
		CanvasPanelSlot = Cast<UCanvasPanelSlot>(PanelSlot);
		if (!IsValid(CanvasPanelSlot))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::ShowArrowAction : CanvasPanelSlot!"));
			return;
		}
		FVector2D InSize = FVector2D(Size.X + 10, Size.Y + 10);
		CanvasPanelSlot->SetSize(InSize);
		//设置闪烁框的位置
		CanvasPanelSlot->SetPosition(FVector2D(Pos.X - 5, Pos.Y - 5));
		//将指引增加到管理器数组
		AddShowTriggerWnd(ActParams.KeyIndex, HightLight);
		//设置闪烁框的大小
		arg = TEXT("SetBoxInfo");
		arg = *FString::Printf(TEXT("%s"), *arg);
		HightLight->CallFunctionByNameWithArguments(*arg, ar, NULL, true);
	}
	else if (ActParams.Param1 == TEXT("2"))
	{
		//显示跑马灯
		ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
		if (!IsValid(PlayerController)) return;
		TArray<FString> SplitArray = UGolbalBPFunctionLibrary::SplitString(ActParams.Param5, false, ",");
		for (FString TempStr : SplitArray)
		{
			TArray<FString> PathArray = UGolbalBPFunctionLibrary::SplitString(TempStr, false, "|");
			if (PathArray.Num() != 2)
			{
				return;
			}
			//先判断指引目标是不是存在
			UWidget* LightTargetWidget = GetWidgetFromWidgetPath(FSTRING_TO_INT(PathArray[0]), PathArray[1]);
			if (!IsValid(LightTargetWidget))
			{
				//指引目标没有了
				return;
			}
			UUserWidget* TempHightLight = CreateWidget<UUserWidget>(PlayerController, UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_DynamicHighLightBox")));
			if (!IsValid(TempHightLight)) return;
			PanelSlot = ParentWindow->AddChild(TempHightLight);
			if (!IsValid(PanelSlot))
			{
				CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::ShowArrowAction : PanelSlot!"));
				return;
			}
			CanvasPanelSlot = Cast<UCanvasPanelSlot>(PanelSlot);
			if (!IsValid(CanvasPanelSlot))
			{
				CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::ShowArrowAction : CanvasPanelSlot!"));
				return;
			}
			FVector2D TempBoxPos = GetWidgetPosition(FSTRING_TO_INT(PathArray[0]), PathArray[1]);
			FVector2D TempBoxSize = GetWidgetSize(FSTRING_TO_INT(PathArray[0]), PathArray[1]);
			TempBoxSize = TempBoxSize / ViewportScale;
			//设置跑马灯的大小，跑马灯边框大约30个像素
			FVector2D InSize = FVector2D(TempBoxSize.X + 30, TempBoxSize.Y + 31);
			CanvasPanelSlot->SetSize(InSize);
			//设置跑马灯的位置
			CanvasPanelSlot->SetPosition(FVector2D(TempBoxPos.X - 14, TempBoxPos.Y - 15));
			//将指引增加到管理器数组
			AddShowTriggerWnd(ActParams.KeyIndex, TempHightLight);
		}
	}
	//播放语音
	PlayVoice(ActParams.AudioID, ActParams.KeyIndex, ActParams.bIsAutoNextStep);
	//设置当前箭头指引数据
	SetCurrentShowArrowData(ActParams.KeyIndex, ActParams);
}

void UTutorialManager::ShowLockScreenArrowAction(const FTUTORIALPARAM& ActParams)
{
	//先判断指引目标是不是存在
	UWidget* TargetWidget = GetWidgetFromWidgetPath(ActParams.UIType, ActParams.UILinkTarget);
	if (!IsValid(TargetWidget))
	{
		//指引目标没有了
		return;
	}

	//触发提示
	FString arg;
	FOutputDeviceNull ar;

	if (!UGolbalBPFunctionLibrary::GUIManager())
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::ShowLockScreenArrowAction : GUIManager()!"));
		return;
	}
	//显示锁屏
	//界面用完就销毁了（只是到销毁池了并没有真正销毁），如果马上又触发了同类指引的话，还是能获取到之前的界面对象，所以重新创建一个，并允许创建多个
	UBaseWindow* LockScreenWnd = UGolbalBPFunctionLibrary::GUIManager()->CreateUIWindow(TEXT("LockSceneTutorial"), true);
	if (!IsValid(LockScreenWnd))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::ShowLockScreenArrowAction : LockScreenWnd!"));
		return;
	}
	LockScreenWnd->Show();
	//将指引增加到管理器数组
	AddShowTriggerWnd(ActParams.KeyIndex, LockScreenWnd);
	//获得游戏分辨率和缩放比
	const FVector2D ViewportSize = UGolbalBPFunctionLibrary::GetViewportSize();
	float ViewportScale = GetDefault<UUserInterfaceSettings>(UUserInterfaceSettings::StaticClass())->GetDPIScaleBasedOnSize(FIntPoint(ViewportSize.X, ViewportSize.Y));
	//目标的位置和大小
	FVector2D Pos = GetWidgetPositionInRootUI(ActParams.UIType, ActParams.UILinkTarget);
	FVector2D Size = GetWidgetSize(ActParams.UIType, ActParams.UILinkTarget);
	Size = Size / ViewportScale;

	//设置锁屏参数
	float MinU, MaxU, MinV, MaxV, Alpha;
	Alpha = 0.7;
	MinU = Pos.X * ViewportScale / ViewportSize.X;
	MinV = Pos.Y * ViewportScale / ViewportSize.Y;
	MaxU = (Pos.X + Size.X) * ViewportScale / ViewportSize.X;
	MaxV = (Pos.Y + Size.Y) * ViewportScale / ViewportSize.Y;
	arg = TEXT("SetMaterialParams");
	arg = *FString::Printf(TEXT("%s %f %f %f %f %f"), *arg, MinU, MinV, MaxU, MaxV, Alpha);
	LockScreenWnd->CallFunctionByNameWithArguments(*arg, ar, NULL, true);

	//显示箭头指引
	EARROWTYPE ArrowType = GetArrowType(ActParams.Param2);
	UUserWidget* Tips = CreateArrowTutorialWidget(ArrowType);
	if (!IsValid(Tips)) return;
	UPanelSlot* PanelSlot = LockScreenWnd->AddChild(Tips);
	if (!IsValid(PanelSlot))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::ShowLockScreenArrowAction :PanelSlot!"));
		return;
	}
	UCanvasPanelSlot* CanvasPanelSlot = Cast<UCanvasPanelSlot>(PanelSlot);
	if (!IsValid(CanvasPanelSlot))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::ShowLockScreenArrowAction : CanvasPanelSlot!"));
		return;
	}
	CanvasPanelSlot->SetAutoSize(true);
	//根据使用的类型来计算窗口位置
	//FVector2D WidgetSize = Tips->GetCachedGeometry().GetDrawSize();
	FVector2D WidgetSize = GetFilterSize(ActParams.Param4, ArrowType);
	FVector2D FilterPos = GetFilterPos(Pos, Size, WidgetSize, ArrowType);
	CanvasPanelSlot->SetPosition(FilterPos);
	//设置提示框标题、内容、是否显示关闭按钮
	arg = TEXT("SetTitleAndContent");
	arg = *FString::Printf(TEXT("%s \"%s\" \"%s\" \"%s\""), *arg, *(ActParams.Param3), *(ActParams.Param4), *(ActParams.Param6));
	Tips->CallFunctionByNameWithArguments(*arg, ar, NULL, true);

	if (ActParams.Param1 == TEXT("1"))
	{
		//显示闪烁框
		ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
		if (!IsValid(PlayerController)) return;
		UUserWidget* HightLight = CreateWidget<UUserWidget>(PlayerController, UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_HighLightBox")));
		if (!IsValid(HightLight)) return;
		PanelSlot = LockScreenWnd->AddChild(HightLight);
		if (!IsValid(PanelSlot))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::ShowLockScreenArrowAction : PanelSlot!"));
			return;
		}
		//设置闪烁框的大小，闪烁框边框大约5个像素
		CanvasPanelSlot = Cast<UCanvasPanelSlot>(PanelSlot);
		if (!IsValid(CanvasPanelSlot))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::ShowLockScreenArrowAction : CanvasPanelSlot!"));
			return;
		}
		FVector2D InSize = FVector2D(Size.X + 10, Size.Y + 10);
		CanvasPanelSlot->SetSize(InSize);
		//设置闪烁框的位置
		CanvasPanelSlot->SetPosition(FVector2D(Pos.X - 5, Pos.Y - 5));
		//设置闪烁框的大小
		arg = TEXT("SetBoxInfo");
		arg = *FString::Printf(TEXT("%s"), *arg);
		HightLight->CallFunctionByNameWithArguments(*arg, ar, NULL, true);
	}
	else if (ActParams.Param1 == TEXT("2"))
	{
		//显示跑马灯
		ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
		if (!IsValid(PlayerController)) return;
		TArray<FString> SplitArray = UGolbalBPFunctionLibrary::SplitString(ActParams.Param5, false, ",");
		for (FString TempStr : SplitArray)
		{
			TArray<FString> PathArray = UGolbalBPFunctionLibrary::SplitString(TempStr, false, "|");
			if (PathArray.Num() != 2)
			{
				return;
			}
			//先判断指引目标是不是存在
			UWidget* LightTargetWidget = GetWidgetFromWidgetPath(FSTRING_TO_INT(PathArray[0]), PathArray[1]);
			if (!IsValid(LightTargetWidget))
			{
				//指引目标没有了
				return;
			}
			UUserWidget* TempHightLight = CreateWidget<UUserWidget>(PlayerController, UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_DynamicHighLightBox")));
			if (!IsValid(TempHightLight)) return;
			PanelSlot = LockScreenWnd->AddChild(TempHightLight);
			if (!IsValid(PanelSlot))
			{
				CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::ShowArrowAction : PanelSlot!"));
				return;
			}
			CanvasPanelSlot = Cast<UCanvasPanelSlot>(PanelSlot);
			if (!IsValid(CanvasPanelSlot))
			{
				CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::ShowArrowAction : CanvasPanelSlot!"));
				return;
			}
			FVector2D TempBoxPos = GetWidgetPosition(FSTRING_TO_INT(PathArray[0]), PathArray[1]);
			FVector2D TempBoxSize = GetWidgetSize(FSTRING_TO_INT(PathArray[0]), PathArray[1]);
			TempBoxSize = TempBoxSize / ViewportScale;
			//设置跑马灯的大小，跑马灯边框大约30个像素
			FVector2D InSize = FVector2D(TempBoxSize.X + 30, TempBoxSize.Y + 31);
			CanvasPanelSlot->SetSize(InSize);
			//设置跑马灯的位置
			CanvasPanelSlot->SetPosition(FVector2D(TempBoxPos.X - 14, TempBoxPos.Y - 15));
			//将指引增加到管理器数组
			AddShowTriggerWnd(ActParams.KeyIndex, TempHightLight);
		}
	}
	//播放语音
	PlayVoice(ActParams.AudioID, ActParams.KeyIndex, ActParams.bIsAutoNextStep);
	//设置当前箭头指引数据
	SetCurrentShowArrowData(ActParams.KeyIndex, ActParams);
}

#pragma endregion

#pragma region	/** 指引触发相关 */
void UTutorialManager::OnTrigger(ETUTORIALTRIGGERTYPE TriggerType, const FString& Param1, const FString& Param2)
{
	FTimerHandle DelayHandle;
	TWeakObjectPtr<UTutorialManager> DelayThisPtr(this);
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayHandle, FTimerDelegate::CreateLambda([DelayThisPtr, TriggerType, Param1, Param2]()
	{
		if (DelayThisPtr.IsValid())
		{
			UTutorialManager* ThisPtr = DelayThisPtr.Get();
			ThisPtr->DelayTrigger(TriggerType, Param1, Param2);
		}
	}), 0.1f, false);
}

void UTutorialManager::DelayTrigger(ETUTORIALTRIGGERTYPE TriggerType, const FString& Param1, const FString& Param2)
{
	switch (TriggerType)
	{
	case ETUTORIALTRIGGERTYPE::EquipScoreTrigger:
	{
		OnTriggerUpdateEquip(TriggerType, Param1, Param2);
		break;
	}
	case ETUTORIALTRIGGERTYPE::LevelTrigger:
	{
		OnTriggerLevel(TriggerType, Param1, Param2);
		break;
	}
	default:
	{
		if (TriggerDatasMap.Contains(TriggerType))
		{
			for (TPair<FName, FTUTORIALDATA>& Item : TriggerDatasMap[TriggerType].Datas)
			{
				Item.Value.DoAction( Param1, Param2);
			}
		}
	}
	}
}

void UTutorialManager::OnTriggerUpdateEquip(ETUTORIALTRIGGERTYPE TriggerType, const FString& Param1, const FString& Param2)
{
	//判断获得的装备比当前穿戴装备战力更高，并且相同部位装备的消息提醒只能存在一个
	int32 LocalNewPower = 0;
	int32 LocalOldPower = 0;
	URoleKitBagInterface* RoleKitBagInterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	UItemBase* NewItem = RoleKitBagInterface->FindItemByUID(Param2);
	if (NewItem && NewItem->IsEquip())
	{
		UEquip* NewEquip = Cast<UEquip>(NewItem);
		if (NewEquip)
		{
			if (!NewEquip->IsCanUse())
			{
				return;
			}
			//新装备战斗力
			LocalNewPower = NewEquip->CombatPower;
			//获取玩家身上同部位装备战斗力
			TArray<FString> UIds = RoleKitBagInterface->GetSamePartEquipUIds(Param2);
			if (UIds.Num() > 0)
			{
				UItemBase* OldItem = RoleKitBagInterface->FindItemByUID(UIds[0]);
				if (OldItem && OldItem->IsEquip())
				{
					UEquip* OldEquip = Cast<UEquip>(OldItem);
					if (OldEquip)
					{
						LocalOldPower = OldEquip->CombatPower;
					}
				}
			}
		}
	}
	if (LocalNewPower > LocalOldPower)
	{
		//触发装备提醒
		if (TriggerDatasMap.Contains(TriggerType))
		{
			for (TPair<FName, FTUTORIALDATA>& Item : TriggerDatasMap[TriggerType].Datas)
			{
				Item.Value.DoAction(Param1, Param2);
			}
		}
	}
}

void UTutorialManager::OnTriggerLevel(ETUTORIALTRIGGERTYPE TriggerType, const FString& Param1, const FString& Param2)
{
	//触发指引
	if (TriggerDatasMap.Contains(TriggerType))
	{
		for (TPair<FName, FTUTORIALDATA>& Item : TriggerDatasMap[TriggerType].Datas)
		{
			Item.Value.DoAction(Param1, Param2);
		}
	}
}

void UTutorialManager::CheckAndCloseTutorial(const FString& Param1, UClass* CloseCndClass/* = nullptr*/)
{
	bool IsHideImage = false;
	bool IsHideMessage = false;
	//清除等待排队的图片指引列表中符合关闭条件的数据
	for (TArray<FTutorialListData>::TConstIterator aiter = NeedShowImageDatas.CreateConstIterator(); aiter; ++aiter)
	{
		FTutorialListData data = *aiter;
		if (data.TutorialData.CheckCloseCondition(Param1, false, CloseCndClass))
		{
			FName LocalKey = data.TutorialData.KeyIndex;
			if (LocalKey == CurrentShowArrowIndex
				|| LocalKey == CurrentShowImageIndex
				|| LocalKey == CurrentShowMessageIndex)
			{
				IsHideImage = true;
			}
			NeedShowImageDatas.Remove(data);
		}
	}
	//清除等待排队的消息提示指引列表中符合关闭条件的数据
	for (TArray<FTutorialListData>::TConstIterator aiter = NeedShowMesssageDatas.CreateConstIterator(); aiter; ++aiter)
	{
		FTutorialListData data = *aiter;
		if (data.TutorialData.CheckCloseCondition(Param1, false, CloseCndClass))
		{
			FName LocalKey = data.TutorialData.KeyIndex;
			if (LocalKey == CurrentShowArrowIndex
				|| LocalKey == CurrentShowImageIndex
				|| LocalKey == CurrentShowMessageIndex)
			{
				IsHideMessage = true;
			}
			NeedShowMesssageDatas.Remove(data);
		}
	}
	//循环全部指引数据清除符合关闭条件的指引数据
	for (TPair<ETUTORIALTRIGGERTYPE, FTutorialMap>& TutorialMap : TriggerDatasMap)
	{
		TMap<FName, FTUTORIALDATA>& Datas = TutorialMap.Value.Datas;
		for (TPair<FName, FTUTORIALDATA>& TutorialData : Datas)
		{
			if (TutorialData.Value.CheckCloseCondition(Param1, false, CloseCndClass))
			{
				if (TutorialData.Key == CurrentShowArrowIndex && HasArrowTutorial())
				{
					//指引条件已经不符合了，需要隐藏当前箭头指引
					HideCurrentArrowTutorial();
				}
				else if (TutorialData.Key == CurrentShowImageIndex && HasImageTutorial())
				{
					//指引条件已经不符合了，需要隐藏当前图片指引
					HideCurrentImageTutorial();
				}
				else if (TutorialData.Key == CurrentShowMessageIndex && HasMessageTutorial())
				{
					//指引条件已经不符合了，需要隐藏当前消息指引
					HideCurrentMessageTutorial();
				}
				OnTutorialFinished(TutorialData.Value);
			}
		}
	}
	//如果关掉了当前的图片指引&&还有图片指引，则继续后面的
	if (IsHideImage && (NeedShowImageDatas.Num() > 0))
	{
		FTutorialListData Data = NeedShowImageDatas[0];
		Data.TutorialData.DoAction(Data.Param1, Data.Param2);
	}
	//如果关掉了当前的消息指引&&还有消息指引，则继续后面的
	if (IsHideMessage && (NeedShowMesssageDatas.Num() > 0))
	{
		FTutorialListData Data = NeedShowMesssageDatas[0];
		Data.TutorialData.DoAction(Data.Param1, Data.Param2);
	}
}

#pragma endregion

#pragma region	/** 指引排队相关 */

void UTutorialManager::AddShowTriggerWnd(const FName& Index, UUserWidget* ShowWidget)
{
	if (!ShowTriggerWnds.Contains(Index))
	{
		FWndList Data;
		Data.ShowWndList.AddUnique(ShowWidget);
		ShowTriggerWnds.Add(Index, Data);
	}
	else
	{
		ShowTriggerWnds[Index].ShowWndList.AddUnique(ShowWidget);
	}
}

void UTutorialManager::DoAction(const FName& KeyIndex, const int32& TutorialType, const float& DelayTime, const FString& Param1, const FString& Param2)
{
	if (DelayTime <= 0.0f)
	{
		ShowAction(KeyIndex, TutorialType, Param1, Param2);
	}
	else
	{
		FTimerHandle DelayHandle;
		TWeakObjectPtr<UTutorialManager> DelayThisPtr(this);
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayHandle, FTimerDelegate::CreateLambda([DelayThisPtr, KeyIndex, TutorialType, Param1, Param2]()
		{
			if (DelayThisPtr.IsValid())
			{
				UTutorialManager* ThisPtr = DelayThisPtr.Get();
				ThisPtr->ShowAction(KeyIndex, TutorialType, Param1, Param2);
			}
		}), DelayTime, false);
	}
}

void UTutorialManager::PlayVoice(FString VoiceIds, FName KeyIndex, bool IsAutoNextStep/*= false*/)
{
	// 解析语音相关数据
	if (CurrAudioIds == VoiceIds)
	{
		return;
	}
	LastAudioID = TEXT("");
	CurrAudioIds = VoiceIds;
	CurrAudioIndex = KeyIndex;
	bIsAutoNextStep = IsAutoNextStep;
	AudioIDList = UGolbalBPFunctionLibrary::SplitString(VoiceIds);
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("--------------------UTutorialManager::PlayVoice:Ids[%s]~"), *VoiceIds);
	if (AudioIDList.Num() == 0) return;
	PlayNextVoice();
}

void UTutorialManager::PlayNextVoice()
{
	if (AudioIDList.Num() <= 0)
	{
		return;
	}
	FString AudioID = AudioIDList[0];
	if (AudioIDList.Num() == 1)
	{
		LastAudioID = AudioID;
	}
	///播放语音
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("--------------------UTutorialManager::PlayNextVoice -> %s~"), *AudioID);
	UGolbalBPFunctionLibrary::AudioManager()->ClientVoicePlay(AudioID, FCClientVoiceComplete::CreateLambda([](FString AudioID)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("--------------------UTutorialManager::VoiceComplete -> %s~"), *AudioID);
		//下一条语音
		if (IsValid(UUECS3GameInstance::Instance->TutorialManager))
		{
			if (UUECS3GameInstance::Instance->TutorialManager->LastAudioID == AudioID)
			{
				UUECS3GameInstance::Instance->TutorialManager->OnVoiceComplete(AudioID);
			}
			else
			{
				UUECS3GameInstance::Instance->TutorialManager->PlayNextVoice();
			}
		}
	}));
	AudioIDList.RemoveAt(0);
}

void UTutorialManager::StopVoice()
{
	if (CurrAudioIds == TEXT(""))
	{
		return;
	}
	//停止播放
	UGolbalBPFunctionLibrary::AudioManager()->ClientVoiceStop();
	//清空数据
	ClearVoiceData();
}

void UTutorialManager::ClearVoiceData()
{
	//清空数据
	CurrAudioIds = TEXT("");
	AudioIDList.Empty();
	LastAudioID = TEXT("");
	bIsAutoNextStep = false;
	CurrAudioIndex = TEXT("");
}

void UTutorialManager::ShowAction(const FName& KeyIndex, const int32& TutorialType, const FString& Param1, const FString& Param2)
{
	switch (TutorialType)
	{
	case 1:
	{
		StartArrow(KeyIndex, Param1, Param2);
		break;
	}
	case 2:
	{
		QueueImage(KeyIndex, Param1, Param2);
		break;
	}
	case 3:
	{
		QueueMessage(KeyIndex, Param1, Param2);
		break;
	}
	default:
	{
		break;
	}
	}
}

void UTutorialManager::StartArrow(const FName & KeyIndex, const FString& Param1, const FString& Param2)
{
	bool IsSuccess = false;
	FTUTORIALDATA Data = GetTutorialDataByKeyIndex(KeyIndex, IsSuccess);
	if (!IsSuccess)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("GetTutorialDataByKeyIndex Is Not Success"));
		return;
	}
	NeedShowArrowActions.TutorialData = Data;
	NeedShowArrowActions.Param1 = Param1;
	NeedShowArrowActions.Param2 = Param2;
	NeedShowArrowActions.IsFinished = false;
	DoNextArrowAction();
}

void UTutorialManager::DoNextArrowAction()
{
	//指引是否已完成
	if (NeedShowArrowActions.IsFinished)
	{
		return;
	}
	if (NeedShowArrowActions.TutorialData.TriggerActs.Num() <= 0)
	{
		//数组为空时表示指引已完成
		OnTutorialFinished(NeedShowArrowActions.TutorialData);
		return;
	}
	//显示下一个指引表现
	bool IsSuccess = NeedShowArrowActions.TutorialData.TriggerActs[0].DoAction(NeedShowArrowActions.Param1, NeedShowArrowActions.Param2);
	NeedShowArrowActions.TutorialData.TriggerActs.RemoveAt(0);
	if (!IsSuccess)
	{
		DoNextArrowAction();
	}
}

void UTutorialManager::DoNextImageAction()
{
	//指引是否已完成
	if (NeedShowImageActions.IsFinished)
	{
		return;
	}
	if (NeedShowImageActions.TutorialData.TriggerActs.Num() <= 0)
	{
		//数组为空时表示指引已完成
		OnTutorialFinished(NeedShowImageActions.TutorialData);
		//继续指引下一条等待排队的指引
		TriggerNextImage();
		return;
	}
	//显示下一个指引表现
	bool IsSuccess = NeedShowImageActions.TutorialData.TriggerActs[0].DoAction(NeedShowImageActions.Param1, NeedShowImageActions.Param2);
	NeedShowImageActions.TutorialData.TriggerActs.RemoveAt(0);
	if (!IsSuccess)
	{
		DoNextImageAction();
	}
}

void UTutorialManager::DoNextMessageAction()
{
	//指引是否已完成
	if (NeedShowMesssageActions.IsFinished)
	{
		return;
	}
	if (NeedShowMesssageActions.TutorialData.TriggerActs.Num() <= 0)
	{
		//数组为空时表示指引已完成
		OnTutorialFinished(NeedShowMesssageActions.TutorialData);
		//继续指引下一条等待排队的指引
		TriggerNextMessage();
		return;
	}
	//显示下一个指引表现
	bool IsSuccess = NeedShowMesssageActions.TutorialData.TriggerActs[0].DoAction(NeedShowMesssageActions.Param1, NeedShowMesssageActions.Param2);
	NeedShowMesssageActions.TutorialData.TriggerActs.RemoveAt(0);
	if (!IsSuccess)
	{
		DoNextMessageAction();
	}
}

void UTutorialManager::QueueMessage(const FName & KeyIndex, const FString& Param1, const FString& Param2)
{
	//添加到消息队列
	bool IsSuccess = false;
	FTUTORIALDATA Data = GetTutorialDataByKeyIndex(KeyIndex, IsSuccess);
	if (!IsSuccess)
	{
		CS3_Warning(TEXT("GetTutorialDataByKeyIndex Is Not Success"));
		return;
	}
	AddTriggerMessage(Data, Param1, Param2);
	//当前是否已经有消息提示指引，若有，则不再往下走
	if (HasMessageTutorial())
	{
		return;
	}
	NeedShowMesssageActions.TutorialData = Data;
	NeedShowMesssageActions.Param1 = Param1;
	NeedShowMesssageActions.Param2 = Param2;
	NeedShowMesssageActions.IsFinished = false;
	DoNextMessageAction();
}

void UTutorialManager::QueueImage(const FName& KeyIndex, const FString& Param1, const FString& Param2)
{
	//添加到图片指引队列
	bool IsSuccess = false;
	FTUTORIALDATA Data = GetTutorialDataByKeyIndex(KeyIndex, IsSuccess);
	if (!IsSuccess)
	{
		CS3_Warning(TEXT("GetTutorialDataByKeyIndex Is Not Success"));
		return;
	}
	AddTriggerImage(Data, Param1, Param2);
	//当前是否已经有图片指引，若有，排队等待
	if (HasImageTutorial())
	{
		return;
	}
	NeedShowImageActions.TutorialData = Data;
	NeedShowImageActions.Param1 = Param1;
	NeedShowImageActions.Param2 = Param2;
	NeedShowImageActions.IsFinished = false;
	DoNextImageAction();
}

void UTutorialManager::AddTriggerMessage(const FTUTORIALDATA& TutorialData, const FString& Param1, const FString& Param2)
{
	if (IsInNeedShowMessageList(TutorialData.KeyIndex))
	{
		return;
	}
	FTutorialListData data;
	data.TutorialData = TutorialData;
	data.Param1 = Param1;
	data.Param2 = Param2;
	data.IsFinished = false;
	NeedShowMesssageDatas.Add(data);
	//只有一个的时候不用排序
	if (NeedShowMesssageDatas.Num() > 1)
	{
		//第一个不参与排序
		FTutorialListData Data = NeedShowMesssageDatas[0];
		NeedShowMesssageDatas.RemoveAt(0);
		//排序
		SortMessage();
		NeedShowMesssageDatas.Insert(Data, 0);
	}
}

void UTutorialManager::SortMessage()
{
	NeedShowMesssageDatas.Sort([](const FTutorialListData& Data1, const FTutorialListData& Data2)
	{
		if ((Data2.TutorialData.TriggerType == ETUTORIALTRIGGERTYPE::EquipScoreTrigger) 
			&& (Data1.TutorialData.TriggerType != ETUTORIALTRIGGERTYPE::EquipScoreTrigger))
		{
			return false;
		}
		if ((Data2.TutorialData.TriggerType == ETUTORIALTRIGGERTYPE::AddItemTrigger) 
			&& (Data1.TutorialData.TriggerType != ETUTORIALTRIGGERTYPE::EquipScoreTrigger) 
			&& (Data1.TutorialData.TriggerType != ETUTORIALTRIGGERTYPE::AddItemTrigger))
		{
			return false;
		}
		return true;
	});
}

bool UTutorialManager::IsInNeedShowMessageList(const FName& KeyIndex)
{
	for (auto data : NeedShowMesssageDatas)
	{
		if (data.TutorialData.KeyIndex == KeyIndex)
		{
			return true;
		}
	}
	return false;
}

void UTutorialManager::TriggerNextMessage()
{
	if (NeedShowMesssageDatas.Num() <= 0) return;
	NeedShowMesssageDatas.RemoveAt(0);
	CurrentShowMessageIndex = TEXT("");
	if (NeedShowMesssageDatas.Num() <= 0) return;
	FTutorialListData Data = NeedShowMesssageDatas[0];
	Data.TutorialData.DoAction(Data.Param1, Data.Param2);
}

void UTutorialManager::AddTriggerImage(const FTUTORIALDATA& TutorialData, const FString& Param1, const FString& Param2)
{
	if (IsInNeedShowImageList(TutorialData.KeyIndex))
	{
		return;
	}
	FTutorialListData data;
	data.TutorialData = TutorialData;
	data.Param1 = Param1;
	data.Param2 = Param2;
	data.IsFinished = false;
	NeedShowImageDatas.Add(data);
}

bool UTutorialManager::IsInNeedShowImageList(const FName& KeyIndex)
{
	for (auto data : NeedShowImageDatas)
	{
		if (data.TutorialData.KeyIndex == KeyIndex)
		{
			return true;
		}
	}
	return false;
}

void UTutorialManager::TriggerNextImage()
{
	if (NeedShowImageDatas.Num() <= 0) return;
	NeedShowImageDatas.RemoveAt(0);
	CurrentShowImageIndex = TEXT("");
	if (NeedShowImageDatas.Num() <= 0) return;
	FTutorialListData Data = NeedShowImageDatas[0];
	Data.TutorialData.DoAction( Data.Param1, Data.Param2);
}

void UTutorialManager::OnTutorialFinished(FTUTORIALDATA & Data)
{
	switch (Data.TutorialType)
	{
	case 1:
	{
		NeedShowArrowActions.IsFinished = true;
		break;
	}
	case 2:
	{
		NeedShowImageActions.IsFinished = true;
		break;
	}
	case 3:
	{
		NeedShowMesssageActions.IsFinished = true;
		break;
	}
	default:
		return;
	}
	//保存
	Data.SaveTriggerIndex();
}

void UTutorialManager::SetCurrentShowArrowData(const FName& KeyIndex, const FTUTORIALPARAM& ActParams)
{
	CurrentShowArrowIndex = KeyIndex;
	CurrentShowArrowData = ActParams;
}

void UTutorialManager::SetCurrentShowImageData(const FName& KeyIndex, const FTUTORIALPARAM& ActParams)
{
	CurrentShowImageIndex = KeyIndex;
	CurrentShowImageData = ActParams;
}

void UTutorialManager::SetCurrentShowMessageData(const FName& KeyIndex, const FTUTORIALPARAM& ActParams)
{
	CurrentShowMessageIndex = KeyIndex;
	CurrentShowMessageData = ActParams;
}

bool UTutorialManager::HasArrowTutorial()
{
	if ((!CurrentShowArrowIndex.IsNone()) && (CurrentShowArrowIndex != TEXT("")))
	{
		return true;
	}
	return false;
}

bool UTutorialManager::HasImageTutorial()
{
	if ((!CurrentShowImageIndex.IsNone()) && (CurrentShowImageIndex != TEXT("")))
	{
		return true;
	}
	return false;
}

bool UTutorialManager::HasMessageTutorial()
{
	if ((!CurrentShowMessageIndex.IsNone()) && (CurrentShowMessageIndex != TEXT("")))
	{
		return true;
	}
	return false;
}

void UTutorialManager::HideCurrentArrowTutorial()
{
	if (HasArrowTutorial())
	{
		HideTriggerItem(CurrentShowArrowIndex);
		CurrentShowArrowIndex = TEXT("");
	}
}

void UTutorialManager::HideCurrentImageTutorial()
{
	if (HasImageTutorial())
	{
		HideTriggerItem(CurrentShowImageIndex);
		CurrentShowImageIndex = TEXT("");
	}
}

void UTutorialManager::HideCurrentMessageTutorial()
{
	if (HasMessageTutorial())
	{
		HideTriggerItem(CurrentShowMessageIndex);
		CurrentShowMessageIndex = TEXT("");
	}
}

#pragma endregion

void UTutorialManager::ClearData()
{
	//清空箭头指引
	HideCurrentArrowTutorial();
	//清空图片指引
	NeedShowImageDatas.Empty();
	HideCurrentImageTutorial();
	//清空消息指引
	NeedShowMesssageDatas.Empty();
	HideCurrentMessageTutorial();

	for (TPair<FName, FWndList> &Item : ShowTriggerWnds)
	{
		Item.Value.ShowWndList.Empty();
	}
}

void UTutorialManager::OnResolutionChanged(FVector2D preReso, float PreScale, FVector2D NewReso)
{
	//分辨率改变时将显示在RootUI上的指引（父面板设置为RootUI的箭头指引）删除并重新显示指引
	UBaseWindow* ParentWin = UGolbalBPFunctionLibrary::TutorialManager()->GetParentWindowFromWidgetPath(CurrentShowArrowData.UILinkTarget);
	if (!IsValid(ParentWin))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::OnResolutionChanged : ParentWin!"));
		return;
	}
	
	if (HasArrowTutorial() && (ParentWin->WindowType == TEXT("") || ParentWin->H_DockStyle == EUIHDOCKSTYLE::HFILL || ParentWin->V_DockStyle == EUIVDOCKSTYLE::VFILL))
	{
		FTimerHandle DelayHandle;
		TWeakObjectPtr<UTutorialManager> DelayThisPtr(this);
		FTUTORIALPARAM ShowArrowData = CurrentShowArrowData;
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayHandle, FTimerDelegate::CreateLambda([DelayThisPtr, ShowArrowData]()
		{
			if (DelayThisPtr.IsValid())
			{
				UTutorialManager* ThisPtr = DelayThisPtr.Get();
				ThisPtr->DoArrowAction(ShowArrowData);
			}
		}), 0.1f, false);
	}
}

void UTutorialManager::OnChangeMyRoleLevel(int32 Level)
{
	//处理指引，在等级变化时，重新判断条件，如果条件不符，需要隐藏
	CheckAndCloseTutorial(TEXT(""), UCloseMaxLevelCND::StaticClass());
	//触发新指引
	OnTrigger(ETUTORIALTRIGGERTYPE::LevelTrigger, INT_TO_FSTRING(Level), TEXT(""));
}

void UTutorialManager::OnChangeQuestState(int32 QuestID)
{
	//放弃任务，取消指引
	if (UGolbalBPFunctionLibrary::QuestManager()->IsQuestStatus(QuestID, (int32)QUEST_STATE::QUEST_NOT_ACCEPT))
	{
		AbandonQuest(QuestID);
	}
	//触发新指引
	else
	{
		OnTrigger(ETUTORIALTRIGGERTYPE::QuestTrigger, INT_TO_FSTRING(QuestID), TEXT(""));
	}
}

void UTutorialManager::AbandonQuest(int32 QuestID)
{
	//放弃的是当前指引的任务
	if (HasArrowTutorial() && NeedShowArrowActions.Param1 == INT_TO_FSTRING(QuestID))
	{
		//需要隐藏当前箭头指引
		HideCurrentArrowTutorial();
		OnTutorialFinished(NeedShowArrowActions.TutorialData);
	}
}

void UTutorialManager::OnUpdateQuestTaskState(int32 QuestID, int32 TaskID)
{
	//需要等待功能完成 && 指引未完成 && 当前指引的任务 && 是任务指引 && 任务目标完成 && 不会触发另一条新指引
	if (CurrentShowArrowData.isWaitFinish
		&& !NeedShowArrowActions.IsFinished
		&& NeedShowArrowActions.Param1 == INT_TO_FSTRING(QuestID)
		&& NeedShowArrowActions.TutorialData.TriggerType == ETUTORIALTRIGGERTYPE::QuestTrigger
		&& UGolbalBPFunctionLibrary::QuestManager()->IsTaskStatus(QuestID, TaskID, (int32)QUEST_TASK_STATE::TASK_IS_DONE)
		&& !CanTriggerNew(ETUTORIALTRIGGERTYPE::QuestTrigger, INT_TO_FSTRING(QuestID), INT_TO_FSTRING(TaskID)))
	{
		//触发当前指引的下一步
		DoNextArrowAction();
	}
	else
	{
		//触发新的一条指引
		OnTrigger(ETUTORIALTRIGGERTYPE::QuestTrigger, INT_TO_FSTRING(QuestID), INT_TO_FSTRING(TaskID));
	}
}

void UTutorialManager::OnSkillCanUpgrate(int32 SkillID, int32 index)
{	//可升级技能提示
	OnTrigger(ETUTORIALTRIGGERTYPE::UpgradeSkillTrigger, INT_TO_FSTRING(SkillID), INT_TO_FSTRING(index));
}

void UTutorialManager::OnFirstLearnSkill(int32 SkillID)
{
	//触发到新手玩家技能指引的流程接口：参数为：SkillID 技能ID
	OnTrigger(ETUTORIALTRIGGERTYPE::FirstLearnSkillTrigger, INT_TO_FSTRING(SkillID), TEXT(""));
}

void UTutorialManager::OnAddItem(FString UID)
{
	URoleKitBagInterface * BagInterface = Cast<URoleKitBagInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleKitBagInterface"), 0));
	if (BagInterface)
	{
		UItemBase* ItemInst = BagInterface->FindItemByUID(UID);
		if (ItemInst)
		{
			if (ItemInst->IsEquip())
			{
				//触发装备战力提示
				OnTrigger(ETUTORIALTRIGGERTYPE::EquipScoreTrigger, INT_TO_FSTRING(ItemInst->ItemID), ItemInst->UID);
			}
			else
			{
				//触发获取物品提示
				OnTrigger(ETUTORIALTRIGGERTYPE::AddItemTrigger, INT_TO_FSTRING(ItemInst->ItemID), ItemInst->UID);
			}
			//触发背包满提示
			if (BagInterface->IsBagFull(EKITBAGTYPE::COMMON) || BagInterface->IsBagFull(EKITBAGTYPE::CRYSTAL))
			{
				OnTrigger(ETUTORIALTRIGGERTYPE::BagFullTrigger, INT_TO_FSTRING(ItemInst->ItemID), TEXT(""));
			}
		}
	}
}

void UTutorialManager::OnAddBuff(int32 BuffID)
{
	OnTrigger(ETUTORIALTRIGGERTYPE::AddBuffTrigger, INT_TO_FSTRING(BuffID), TEXT(""));
}

void UTutorialManager::OnRemoveMessageTutorial(FString ItemUID)
{
	//是否是当前显示的
	if (HasMessageTutorial() && (NeedShowMesssageActions.Param2 == ItemUID))
	{
		//关闭指引
		HideCurrentMessageTutorial();
		//已完成
		OnTutorialFinished(NeedShowMesssageActions.TutorialData);
		//继续指引下一条等待排队的指引
		TriggerNextMessage();
	}
	else
	{
		//移除的物品是否在队列中
		for (TArray<FTutorialListData>::TConstIterator aiter = NeedShowMesssageDatas.CreateConstIterator(); aiter; ++aiter)
		{
			FTutorialListData data = *aiter;
			//在队列中
			if (ItemUID == data.Param2)
			{
				//从队列中移除
				NeedShowMesssageDatas.Remove(data);
				break;
			}
		}
	}
}

bool UTutorialManager::CanTriggerNew(ETUTORIALTRIGGERTYPE TriggerType, const FString& Param1, const FString& Param2)
{
	if (TriggerDatasMap.Contains(TriggerType))
	{
		for (TPair<FName, FTUTORIALDATA>& Item : TriggerDatasMap[TriggerType].Datas)
		{
			//是否能够触发新的一条指引
			if (Item.Value.CheckCondition(Param1, Param2) && !Item.Value.CheckCloseCondition(Param1))
			{
				return true;
			}
		}
	}
	return false;
}

void UTutorialManager::OnRemoveItem(FString ItemUID)
{
	OnRemoveMessageTutorial(ItemUID);
}

void UTutorialManager::OnUseEquip(FString ItemUID)
{
	OnRemoveMessageTutorial(ItemUID);
}

void UTutorialManager::OnAddQBItem(int32 QbID)
{
	//处理指引，重新判断条件，如果符合关闭条件，需要过掉这条指引
	CheckAndCloseTutorial(INT_TO_FSTRING(QbID), UCloseSkillInQuickBarCND::StaticClass());
}

void UTutorialManager::OnRemoveQBItem(int32 QbID)
{
	//处理指引，重新判断条件，如果符合关闭条件，需要过掉这条指引
	CheckAndCloseTutorial(INT_TO_FSTRING(QbID), UCloseSkillInQuickBarCND::StaticClass());
}

void UTutorialManager::OnPlaySkill(int32 SkillID)
{
	//处理指引，重新判断条件，如果符合关闭条件，需要过掉这条指引
	CheckAndCloseTutorial(INT_TO_FSTRING(SkillID), UClosePlaySkillCND::StaticClass());
}

void UTutorialManager::OnVoiceComplete(FString AudioID)
{
	//是否配置了自动播放下一步
	if (bIsAutoNextStep)
	{
		bool IsSuccess;
		FTUTORIALDATA Data = GetTutorialDataByKeyIndex(CurrAudioIndex, IsSuccess);
		if (IsSuccess)
		{
			//清空语音数据
			ClearVoiceData();
			//完成当前步骤，进行下一步
			FinishCurrStep(Data.TutorialType);
		}
	}
	else
	{
		//清空语音数据
		ClearVoiceData();
	}
}

void UTutorialManager::OnOpenWindow(FString WindowType)
{
	OnTrigger(ETUTORIALTRIGGERTYPE::OpenWindowTrigger, WindowType, TEXT(""));
}

void UTutorialManager::OnEnterWorld()
{

}

void UTutorialManager::OnLeaveWorld()
{
	ClearData();
}

bool UTutorialManager::IsTickable() const
{
	return IsStartWaitOpenPanel;
}

void UTutorialManager::Tick(float DeltaTime)
{
	CheckWaitOpenPanelTime += DeltaTime;
	//等待时间超过15秒默认指引完成
	if (CheckWaitOpenPanelTime >= 15.0f)
	{
		IsStartWaitOpenPanel = false;
		//指引完成
		OnTutorialFinished(NeedShowArrowActions.TutorialData);
		return;
	}
	TArray<FString> SplitArray = UGolbalBPFunctionLibrary::SplitString(WaitOpenWidgetPath, false, ",");
	//Widget->IsVisible()为true时也get不到位置和尺寸，能Get到Size才算真的能指引
	//锁屏时才需要等待界面打开，不锁屏时，界面在创建完成时（即能Get到Size）就可以增加指引
	if (WaitShowData.bIsLockScreen)
	{
		for (FString TempStr : SplitArray)
		{
			TArray<FString> PathArray = UGolbalBPFunctionLibrary::SplitString(TempStr, false, "|");
			if (PathArray.Num() != 2)
			{
				return;
			}
			UBaseWindow* Widget = GetParentWindowFromWidgetPath(PathArray[1]);
			if (!Widget || (Widget && !Widget->IsVisible()))
			{
				CS3_Warning(TEXT("-->Null Pointer error:UTutorialManager::Tick : Widget || (Widget && Widget->IsVisible())!"));
				return;
			}
		}
	}
	bool CanShow = true;
	for (FString TempStr : SplitArray)
	{
		TArray<FString> PathArray = UGolbalBPFunctionLibrary::SplitString(TempStr, false, "|");
		if (PathArray.Num() != 2)
		{
			return;
		}
		FVector2D Size = GetWidgetSize(FSTRING_TO_INT(PathArray[0]), PathArray[1]);
		if (Size == FVector2D::ZeroVector)
		{
			CanShow = false;
		}
	}
	if (CanShow)
	{
		IsStartWaitOpenPanel = false;
		CheckWaitOpenPanelTime = 0.0f;
		ShowPanelArrowAction();
	}
}

CONTROL_COMPILE_OPTIMIZE_END
