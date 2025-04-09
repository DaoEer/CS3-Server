#pragma once

#include "Blueprint/UserWidget.h"
#include "HorizontalBox.h"
#include "VerticalBox.h"
#include "CS3Base/CS3UserWidget.h"
#include "CS3Base/BaseWindow.h"
#include "ActivityFuncBtnWidget.h"
#include "ActivityFunctionBarWidget.generated.h"

/*
* 文件名称：ActivityFunctionBarWidget.h
* 功能说明：
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2019-03-22
*/

USTRUCT(BlueprintType)
struct CHUANGSHI_API FBtnArray
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(BlueprintReadWrite)
		TArray<UActivityFuncBtnWidget*> Btns;
};

UCLASS(BlueprintType)
class CHUANGSHI_API UActivityFunctionBarWidget : public UBaseWindow
{
	GENERATED_BODY()
public:
	virtual void NativeOnEnterWorld() override; ///<当角色进入世界时被调用
	virtual void NativeOnLeaveWorld() override; ///<当角色离开世界时被调用
	/**
	*增加活动系统
	*
	*@param BtnTag 按钮标记
	*
	*@return 无
	*/
	void AddActivitySystem(FName BtnTag, int32 RemainTime = 0);
	/**
	*删除活动系统
	*
	*@param BtnTag 按钮标记
	*
	*@return 无
	*/
	void RemoveActivitySystem(FName BtnTag);
	/**
	*获取某个系统的倒计时
	*
	*@param BtnTag 按钮标记
	*
	*@return int32
	*/
	int32 GetRemainTime(FName BtnTag);

private:
	/**
	*排序活动系统ICON
	*
	*@param Row 行
	*
	*@return 无
	*/
	void LayoutSystem(int32 Row);
	/**
	*排序行
	*
	*@param Row 行
	*
	*@return 无
	*/
	void LayoutRow(int32 Row);
	/**
	*获取某一行的全部功能按钮控件
	*
	*@return 无
	*/
	UActivityFuncBtnWidget* GetBtnWidgetByBtnTag(FName BtnTag);

public:
	UPROPERTY(meta = (BindWidget))
		UVerticalBox* BtnsVerticalBox;

private:
	UPROPERTY()
		TMap<int32, UHorizontalBox*> BtnRowBoxMap;
	UPROPERTY()
		TMap<int32, FBtnArray> BtnWidgetMap;
};