#pragma once

#include "CoreMinimal.h"
#include "Components/Button.h"
#include "SButton.h"

#include "CS3Button.generated.h"

/**
* 文件名称：CS3Button.h
* 功能说明：按钮类
		*创世3所有按钮都应使用UCS3Button
		*处理了特殊鼠标状态
		*处理了新手指引响应
		*处理了音效
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2019-01-24
 */

class CHUANGSHI_API SCS3Button : public SButton
{
public:
	SCS3Button(){}

	virtual FReply OnMouseButtonDown(const FGeometry& MyGeometry, const FPointerEvent& MouseEvent) override;

	virtual FReply OnMouseButtonDoubleClick(const FGeometry& InMyGeometry, const FPointerEvent& InMouseEvent) override
	{
		return SCS3Button::OnMouseButtonDown(InMyGeometry, InMouseEvent);
	}

	virtual FReply OnMouseButtonUp(const FGeometry& MyGeometry, const FPointerEvent& MouseEvent) override;

private:
	/*
	*处理特殊鼠标状态
	*return 是否是特殊鼠标状态
	*/
	bool DealEspecialCursorState(const FPointerEvent& MouseEvent);
	/**
	*检查完成指引，被点击时调用
	*
	*@return 无
	*/
	void CheckFinishTutorial();
};

/**
*按钮类
*创世3所有按钮都应使用UCS3Button
*处理了特殊鼠标状态
*处理了新手指引响应
*处理了音效
*/
UCLASS(Blueprintable)
class CHUANGSHI_API UCS3Button : public UButton
{
	GENERATED_BODY()

public:
	UCS3Button(const FObjectInitializer& ObjectInitializer);

	virtual TSharedRef<SWidget> RebuildWidget() override;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Appearance|Sound")
		FString PressedSoundID = TEXT("other010112");
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Appearance|Sound")
		FString HoveredSoundID;

protected:
	void CS3SlateHandlePressed();
	void CS3SlateHandleHovered();
};