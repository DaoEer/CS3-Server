// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "Components/RichTextBlock.h"
#include "SRichTextBlock.h"
#include "SlateHyperlinkRun.h"
#include "Tickable.h"
#include "CS3RichTextBlock.generated.h"

/*
* 文件名称：CS3RichTextBlock.h
* 功能说明：
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2017-09-01
*/

class UCS3RichTextBlockDecorator;

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnHyperTextClickedEvent);

/**
 * 富文本控件类
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UCS3RichTextBlock : public UTextLayoutWidget, public FTickableGameObject
{
	GENERATED_BODY()
	
	
public:
	UCS3RichTextBlock(const FObjectInitializer& ObjectInitializer);

	// UWidget interface
	virtual void SynchronizeProperties() override;
	// End of UWidget interface

	// UVisual interface
	virtual void ReleaseSlateResources(bool bReleaseChildren) override;
	// End of UVisual interface

#if WITH_EDITOR
	// UWidget interface
	virtual const FText GetPaletteCategory() override;
	virtual void OnCreationFromPalette() override;
	// End UWidget interface
#endif
	virtual void OnHyperlinkDecoratorClicked(const FSlateHyperlinkRun::FMetadata& Metadata);
	/*{
		//RichTextHelper::SpawnProClickerPopUp(LOCTEXT("HyperlinkDecoratorExamplePopUpMessage", "You're a <RichText.Tagline.TextHighlight>pro</> at clicking!"), AsShared());
	}*/

protected:
	//FTickableGameObject implement
	virtual TStatId GetStatId() const override { RETURN_QUICK_DECLARE_CYCLE_STAT(UCS3RichTextBlock, STATGROUP_Tickables); }
	virtual bool IsTickable() const override;
	virtual void Tick(float DeltaTime) override;
	virtual bool IsTickableInEditor() const override { return true; }

protected:
	/** The text to display */
	UPROPERTY(EditAnywhere, Category = Content, meta = (MultiLine = "true"))
		FText Text;

	/** A bindable delegate to allow logic to drive the text of the widget */
	UPROPERTY()
	FGetText TextDelegate;

	/** The default font for the text. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Appearance)
	FSlateFontInfo Font;

	/** The default color for the text. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Appearance)
	FSlateColor ColorAndOpacity;

	/** How much should the shadow be offset? An offset of 0 implies no shadow. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Appearance)
	FVector2D ShadowOffset;

	/** The color and opacity of the shadow */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Appearance)
	FLinearColor ShadowColorAndOpacity;

	/* 装饰器 用于解析文本，需要用到哪个增加哪个，比如有图片，则增加UCS3RichTextBlockImageDecorator*/
	UPROPERTY(EditAnywhere, Category = Appearance)
	TArray<TSubclassOf<UCS3RichTextBlockDecorator>> DecoratorClasses;

	//因为使用的富文本太多，要一个个去手动增加Decorator，很麻烦，暂时先全部创建好
	UPROPERTY()
	TArray<TSubclassOf<UCS3RichTextBlockDecorator>> PreDecoratorClasses;

protected:

	FTextBlockStyle DefaultStyle;

	UPROPERTY(Transient)
	TArray<UCS3RichTextBlockDecorator*> InstanceDecorators;

	/** Native Slate Widget */
	TSharedPtr<SRichTextBlock> MyRichTextBlock;

	PROPERTY_BINDING_IMPLEMENTATION(FText, Text);

	// UWidget interface
	virtual TSharedRef<SWidget> RebuildWidget() override;
	// End of UWidget interface	
	virtual void OnWidgetRebuilt() override;

	virtual void UpdateStyleData();
	virtual void CreateDecorators(TArray< TSharedRef< class ITextDecorator > >& OutDecorators);

public:
	/** Called when the HyperText is clicked */
	UPROPERTY(BlueprintAssignable, Category = "CS3RichTextBlock|Event")
		FOnHyperTextClickedEvent OnHyperTextClicked;

	const FTextBlockStyle& GetDefaultTextStyle() const;

	/**
	* Directly sets the widget text.
	* Warning: This will wipe any binding created for the Text property!
	* @param InText The text to assign to the widget
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3RichTextBlock|Widget", meta = (DisplayName = "SetText (RichText)"))
		void SetText(FText InText);
	/**
	* Gets the widget text
	* @return The widget text
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3RichTextBlock|Widget", meta = (DisplayName = "GetText (RichText)"))
		FText GetText() const;

	/**
	* Dynamically set the font info for this text block
	*
	* @param InFontInfo THe new font info
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3RichTextBlock|Widget")
		void SetFont(FSlateFontInfo InFontInfo);

	UFUNCTION(BlueprintCallable, Category = "CS3RichTextBlock|Widget")
		void SetFontSize(int fontSize);

	/**
	*  Set the text justification for this text block
	*
	*  @param Justification new justification
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3RichTextBlock|Widget")
		void SetJustification(ETextJustify::Type InJustification);
	UFUNCTION(BlueprintCallable, Category = "CS3RichTextBlock|Widget")
		TEnumAsByte<ETextJustify::Type> GetJustification() const;

	/** The color and opacity of this text */
	UFUNCTION(BlueprintCallable, Category = "CS3RichTextBlock|Widget")
		void SetColorAndOpacity(FSlateColor InColorAndOpacity);

	/**
	* Sets the opacity of the text in this text block
	*
	* @param InOpacity		The new text opacity
	*/
	UFUNCTION(BlueprintCallable, Category = "CS3RichTextBlock|Widget")
		void SetOpacity(float InOpacity);

	/** How much should the shadow be offset? An offset of 0 implies no shadow. */
	UFUNCTION(BlueprintCallable, Category = "CS3RichTextBlock|Widget")
		void SetShadowOffset(FVector2D InShadowOffset);

	/** The color and opacity of the shadow */
	UFUNCTION(BlueprintCallable, Category = "CS3RichTextBlock|Widget")
		void SetShadowColorAndOpacity(FLinearColor InShadowColorAndOpacity);

	/** Set WrapTextAt */
	UFUNCTION(BlueprintCallable, Category = "CS3RichTextBlock|Widget")
	void SetWrapTextAt(float InWrapTextAt);

	/** Set AutoWrapText */
	UFUNCTION(BlueprintCallable, Category = "CS3RichTextBlock|Widget")
	void SetAutoWrapText(bool InAutoWrapText);

public:
	FText ReplaceSpecialValue(FText InText);

	/** bIsFadeText 淡入淡出*/
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "TextBehavior")
		bool bIsFadeText = false;
	UFUNCTION(BlueprintCallable, Category = "TextBehavior")
	void SetIsFadeText(bool bIsFade);

	/** should we start tick Fade*/
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "TextBehavior")
		bool bIsStartTickFadeText = false;
	UFUNCTION(BlueprintCallable, Category = "TextBehavior")
	void SetIsStartTickFadeText(bool bIsStartTickFade);

	/** FadeSpeed 淡入淡出时间*/
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "TextBehavior")
		float FadeSpeed = 1.0f;//淡入淡出时间
	UFUNCTION(BlueprintCallable, Category = "TextBehavior")
	void SetFadeSpeed(float InFadeSpeed);

	/** FadeInterval 淡出延时时间，淡入和淡出之间间隔*/
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "TextBehavior")
		float FadeInterval = 0.0f;//淡出延时
	UFUNCTION(BlueprintCallable, Category = "TextBehavior")
	void SetFadeInterval(float InFadeInterval);

	virtual void ResetFadeText();
	virtual void RebuildFadeText();

	UFUNCTION(BlueprintCallable, Category = "TextBehavior")
		virtual void StopFade();
	UFUNCTION(BlueprintCallable, Category = "TextBehavior")
		virtual void StartFade();

protected:
	bool bCreationFromPalette = false;
	float FadeDeltaTime = 0.0f;//淡入淡出时间
	bool bIsFadeIn = false;//淡入
	bool bIsFadeOut = false;//淡出
	float TextFadeTimer = 0.0f;//淡出延时

private:
	bool bNeedRebuildFadeText = false;//是否需要重编
};
