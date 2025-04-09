#pragma once
#include "CoreMinimal.h"
#include "Components/Button.h"
#include "SButton.h"
#include "CS3Button.h"

#include "CustomButton.generated.h"

/**
* 文件名称：CustomButton.h
* 功能说明：自定义不规则形状按钮类，透明像素不响应
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2019-01-24
 */

class CHUANGSHI_API SCumstomButton : public SCS3Button
{
public:
	UTexture2D* AdvancedHitTexture;
	int32 AdvancedHitAlpha;

	SCumstomButton() : AdvancedHitTexture(NULL), AdvancedHitAlpha(0) {}

	void SetAdvancedHitTexture(UTexture2D* InTexture)
	{
		AdvancedHitTexture = InTexture;
	}

	void SetAdvancedHitAlpha(int32 InAlpha)
	{
		AdvancedHitAlpha = InAlpha;
	}

	virtual FReply OnMouseButtonDown(const FGeometry& MyGeometry, const FPointerEvent& MouseEvent) override
	{
		if (!bIsHovered) return FReply::Unhandled();
		return SCS3Button::OnMouseButtonDown(MyGeometry, MouseEvent);
	}

	virtual FReply OnMouseButtonDoubleClick(const FGeometry& InMyGeometry, const FPointerEvent& InMouseEvent) override
	{
		return SCumstomButton::OnMouseButtonDown(InMyGeometry, InMouseEvent);
	}

	virtual FReply OnMouseButtonUp(const FGeometry& MyGeometry, const FPointerEvent& MouseEvent) override
	{
		if (!bIsHovered) return FReply::Unhandled();
		return SCS3Button::OnMouseButtonUp(MyGeometry, MouseEvent);
	}

	virtual FReply OnMouseMove(const FGeometry& MyGeometry, const FPointerEvent& MouseEvent) override;

	virtual void OnMouseEnter(const FGeometry& MyGeometry, const FPointerEvent& MouseEvent) override
	{
		if (AdvancedHitTexture) return;
		return SCS3Button::OnMouseEnter(MyGeometry, MouseEvent);
	}

	virtual void OnMouseLeave(const FPointerEvent& MouseEvent) override
	{
		return SCS3Button::OnMouseLeave(MouseEvent);
	}

	virtual FCursorReply OnCursorQuery(const FGeometry& MyGeometry, const FPointerEvent& CursorEvent) const override;

	virtual TSharedPtr<IToolTip> GetToolTip() override { return (bIsHovered ? SWidget::GetToolTip() : NULL); }

	void SetIsHovered(uint8 IsHovered);
};

/**
*不规则形状按钮类
*适应不规则形状按钮，透明像素不响应
*/
UCLASS(Blueprintable)
class CHUANGSHI_API UCustomButton : public UCS3Button
{
	GENERATED_BODY()

public:
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "AdvancedHitTest") UTexture2D* AdvancedHitTexture;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "AdvancedHitTest", meta = (ClampMin = "0.0", ClampMax = "255.0", UIMin = "0.0", UIMax = "255.0")) int32 AdvancedHitAlpha;

	UFUNCTION(BlueprintCallable, Category = "AdvancedHitTest") void SetAdvancedHitTexture(UTexture2D* InTexture)
	{
		AdvancedHitTexture = InTexture;
		if (MyButton.IsValid()) (static_cast<SCumstomButton*>(MyButton.Get()))->SetAdvancedHitTexture(AdvancedHitTexture);
	}

	UFUNCTION(BlueprintCallable, Category = "AdvancedHitTest") void SetAdvancedHitAlpha(int32 InAlpha)
	{
		AdvancedHitAlpha = InAlpha;
		if (MyButton.IsValid()) (static_cast<SCumstomButton*>(MyButton.Get()))->SetAdvancedHitAlpha(AdvancedHitAlpha);
	}

	UCustomButton(const FObjectInitializer& ObjectInitializer);

	virtual void SynchronizeProperties() override;

	virtual TSharedRef<SWidget> RebuildWidget() override;

	UFUNCTION(BlueprintCallable)
		bool IsInArea(FVector2D ScreenPos);
	UFUNCTION(BlueprintCallable)
		void SetIsHovered(uint8 IsHovered);
};