#include "ActivityFunctionBarWidget.h"
#include "VerticalBoxSlot.h"
#include "../GameDevelop/CS3PlayerController.h"
#include "GameDevelop/CS3GameInstance.h"
#include "../Util/GolbalBPFunctionLibrary.h"
#include "GameData/UIConfigData.h"
#include "Util/ConvertUtil.h"
#include "Manager/SystemSwitchManager.h"

void UActivityFunctionBarWidget::NativeOnEnterWorld()
{
	Show();
	Super::NativeOnEnterWorld();
}

void UActivityFunctionBarWidget::NativeOnLeaveWorld()
{
	BtnRowBoxMap.Empty();
	BtnWidgetMap.Empty();
	BtnsVerticalBox->ClearChildren();
	Super::NativeOnLeaveWorld();
}

void UActivityFunctionBarWidget::AddActivitySystem(FName BtnTag, int32 RemainTime /*= 0*/)
{
	UActivityFuncBtnWidget* FuncBtnWidget = GetBtnWidgetByBtnTag(BtnTag);
	if (IsValid(FuncBtnWidget))
	{
		//已经有这个系统ICON
		//更新倒计时
		FuncBtnWidget->SetCountDown(RemainTime);
		return;
	}
	bool IsSuccess;
	FFunctionBtnData BtnData = UUECS3GameInstance::Instance->SystemSwitchManager->GetBtnCfgByBtnTag(BtnTag, IsSuccess);
	if (!IsSuccess)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UActivityFunctionBarWidget::AddActivitySystem : BtnData!"));
		return;
	}
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (!IsValid(PlayerController)) return;
	UActivityFuncBtnWidget* IconWidget = CreateWidget<UActivityFuncBtnWidget>(PlayerController, UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_ActivityFuncBtnWidget")));
	if (!IsValid(IconWidget)) return;

	TArray<FString> SplitArray = UGolbalBPFunctionLibrary::SplitString(BtnData.BtnPosition, false, "|");
	int32 Row = 0;
	int32 InPriority = 0;
	if (SplitArray.Num() == 2)
	{
		Row = FSTRING_TO_INT(SplitArray[0]);
		InPriority = FSTRING_TO_INT(SplitArray[1]);
	}
	//加入BtnWidgetMap
	if (!BtnWidgetMap.Contains(Row))
	{
		FBtnArray Btns;
		BtnWidgetMap.Add(Row, Btns);
	}
	BtnWidgetMap[Row].Btns.Add(IconWidget);
	//是否需要另增一行
	if (!BtnRowBoxMap.Contains(Row))
	{
		UHorizontalBox* BtnRowBox = NewObject<UHorizontalBox>();
		UVerticalBoxSlot* BoxSlot = Cast<UVerticalBoxSlot>(BtnsVerticalBox->AddChild(BtnRowBox));
		BoxSlot->SetHorizontalAlignment(HAlign_Right);
		BoxSlot->SetVerticalAlignment(VAlign_Top);

		BtnRowBoxMap.Add(Row);
		BtnRowBoxMap[Row] = BtnRowBox;
		//排序行
		LayoutRow(Row);
	}
	//要在排序之前设置数据，不然排序需要的数据不对
	IconWidget->SetBtnInfo(BtnTag, InPriority, RemainTime);
	//新加新ICON并刷新顺序
	LayoutSystem(Row);
	//ICON显示，播放特效
	IconWidget->OpenActivity(BtnTag, InPriority);
}

void UActivityFunctionBarWidget::RemoveActivitySystem(FName BtnTag)
{
	bool IsSuccess;
	FFunctionBtnData BtnData = UUECS3GameInstance::Instance->SystemSwitchManager->GetBtnCfgByBtnTag(BtnTag, IsSuccess);
	if (!IsSuccess)
	{
		CS3_Warning(TEXT("-->Null Pointer error:RemoveActivitySystem::AddActivitySystem : BtnData!"));
		return;
	}
	TArray<FString> SplitArray = UGolbalBPFunctionLibrary::SplitString(BtnData.BtnPosition, false, "|");
	int Row = 0;
	if (SplitArray.Num() == 2)
	{
		Row = FSTRING_TO_INT(SplitArray[0]);
	}
	for (TPair<int32, FBtnArray>& Widgets : BtnWidgetMap)
	{
		for (UActivityFuncBtnWidget* BtnWidget : Widgets.Value.Btns)
		{
			if (BtnWidget->BtnTag == BtnTag)
			{
				//移除控件
				BtnRowBoxMap[Row]->RemoveChild(BtnWidget);
				//移除引用
				Widgets.Value.Btns.Remove(BtnWidget);
				return;
			}
		}
	}
}

int32 UActivityFunctionBarWidget::GetRemainTime(FName BtnTag)
{
	for (TPair<int32, FBtnArray>& Widgets : BtnWidgetMap)
	{
		for (UActivityFuncBtnWidget* BtnWidget : Widgets.Value.Btns)
		{
			if (BtnWidget->BtnTag == BtnTag)
			{
				return BtnWidget->RemainTime;
			}
		}
	}
	return 0;
}

void UActivityFunctionBarWidget::LayoutSystem(int32 Row)
{
	//移除这一行所有活动ICON
	BtnRowBoxMap[Row]->ClearChildren();
	//排序
	BtnWidgetMap[Row].Btns.Sort([](const UActivityFuncBtnWidget& Widget1, const UActivityFuncBtnWidget& Widget2)
	{
		return Widget1.Priority > Widget2.Priority;
	});
	//排完序后全部重新添加
	for (UActivityFuncBtnWidget* Widget : BtnWidgetMap[Row].Btns)
	{
		BtnRowBoxMap[Row]->AddChild(Widget);
	}
}

void UActivityFunctionBarWidget::LayoutRow(int32 Row)
{
	//判断一下是否需要排序
	bool IsNeedSort = false;
	for (TPair<int32, UHorizontalBox*>& BtnRowBox : BtnRowBoxMap)
	{
		if (BtnRowBox.Key > Row)
		{
			//如果已经有的行号比新加的要大，则需要排序
			IsNeedSort = true;
			break;
		}
	}
	if (!IsNeedSort)
	{
		return;
	}
	//移除所有行
	BtnsVerticalBox->ClearChildren();
	//排序
	BtnRowBoxMap.KeySort(TLess<int32>());
	//重新添加
	for (TPair<int32, UHorizontalBox*>& BtnRowBox : BtnRowBoxMap)
	{
		BtnsVerticalBox->AddChild(BtnRowBox.Value);
	}
}

UActivityFuncBtnWidget* UActivityFunctionBarWidget::GetBtnWidgetByBtnTag(FName BtnTag)
{
	for (TPair<int32, FBtnArray>& Widgets : BtnWidgetMap)
	{
		for (UActivityFuncBtnWidget* BtnWidget : Widgets.Value.Btns)
		{
			if (BtnWidget->BtnTag == BtnTag)
			{
				return BtnWidget;
			}
		}
	}
	return nullptr;
}