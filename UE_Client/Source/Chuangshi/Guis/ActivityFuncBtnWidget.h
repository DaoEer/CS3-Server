#pragma once

#include "Blueprint/UserWidget.h"
#include "Button.h"
#include "Image.h"
#include "Overlay.h"
#include "TextBlock.h"
#include "CS3Base/CS3UserWidget.h"
#include "ActivityFuncBtnWidget.generated.h"



/*
* 文件名称：ActivityFuncBtnWidget.h
* 功能说明：
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2019-03-22
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UActivityFuncBtnWidget : public UCS3UserWidget
{
	GENERATED_BODY()
public:

	UActivityFuncBtnWidget(const FObjectInitializer& ObjectInitializer);
	virtual void NativeConstruct();
	/**
	*设置功能按钮信息
	*
	*@param InBtnTag 按钮标记
	*@param InPriority 按钮显示优先级，按钮由右往左排，越右值越小
	*
	*@return 无
	*/
	void SetBtnInfo(FName InBtnTag, int32 InPriority, int32 InRemainTime);
	/**
	*开启活动（先播光效再显示功能按钮）
	*
	*@param InBtnTag 按钮标记
	*@param InPriority 按钮显示优先级，按钮由右往左排，越右值越小
	*
	*@return 无
	*/
	void OpenActivity(FName InBtnTag, int32 InPriority);
	/**
	*设置倒计时
	*
	*@param InBtnTag 按钮标记
	*@param InRemainTime 剩余时间
	*
	*@return 无
	*/
	void SetCountDown(int32 InRemainTime);
	/**
	*按钮点击事件回调方法
	*必须加 UFUNCTION()
	*
	*@return 无
	*/
	UFUNCTION()
		void OnClickedFuncBtn();
private:
	/**
	*播光效
	*
	*@return 无
	*/
	void ShowOpenEffect();
	/**
	*播光效Timer
	*
	*@return 无
	*/
	void PlayEffectTimer();
	/**
	*删除光效
	*
	*@return 无
	*/
	void ClearOpenEffect();
	/**
	*开始倒计时
	*
	*@return 无
	*/
	void StartCountDown();
	/**
	*清除倒计时
	*
	*@return 无
	*/
	void ClearCountDown();

public:
	UPROPERTY(meta = (BindWidget))
		UButton* FuncBtn;
	UPROPERTY(meta = (BindWidget))
		UImage* EffectImg;
	UPROPERTY(meta = (BindWidget))
		UOverlay* TextPanel;
	UPROPERTY(meta = (BindWidget))
		UTextBlock* RemainTimeText;

public:
	//按钮标记
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FName BtnTag;
	//按钮打开的界面类型
	UPROPERTY(EditAnywhere, BlueprintReadOnly)
		FString WindowType;
	//按钮显示优先级，按钮由右往左排，越右值越小
	int32 Priority;
	int32 RemainTime;

private:
	float PhaseValue;
	float EffectTimer = 0.01;
	FTimerHandle EffectHandle;
	FTimerHandle CountdownHandle;
};