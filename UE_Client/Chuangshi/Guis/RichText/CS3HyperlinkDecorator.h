#pragma once
#include "CoreMinimal.h"
#include "UObject/ObjectMacros.h"
#include "UObject/Object.h"
#include "Fonts/SlateFontInfo.h"
#include "Styling/SlateTypes.h"
#include "Framework/Text/TextLayout.h"
#include "Framework/Text/ISlateRun.h"
#include "Framework/Text/ITextDecorator.h"
#include "Framework/Text/SlateHyperlinkRun.h"

#include "CS3RichTextBlockDecorator.h"
#include "CS3HyperlinkDecorator.generated.h"

class ISlateStyle;
class UCS3RichTextBlockHyperlinkDecorator;
class UCS3RichTextBlock;

/**
 * FCS3HyperlinkDecorator
 * 富文本中解析超链接资源的类
 */
class FCS3HyperlinkDecorator : public FCS3RichTextDecorator
{
public:
	FCS3HyperlinkDecorator(UCS3RichTextBlock* InOwner, UCS3RichTextBlockHyperlinkDecorator* InDecorator);

	virtual ~FCS3HyperlinkDecorator() {}

	virtual bool Supports(const FTextRunParseResults& RunParseResult, const FString& Text) const override;

	virtual TSharedRef< ISlateRun > Create(const TSharedRef<class FTextLayout>& TextLayout, const FTextRunParseResults& RunParseResult, const FString& OriginalText, const TSharedRef< FString >& InOutModelText, const ISlateStyle* Style) override;
	
	/** 处理超链接提示框样式和字体 */
	static TSharedRef<IToolTip>  DelegateHyperlinkToolTip(const FSlateHyperlinkRun::FMetadata& Metadata);

protected:
	FSlateHyperlinkRun::FOnClick NavigateDelegate;
	FSlateHyperlinkRun::FOnGetTooltipText ToolTipTextDelegate;
	FSlateHyperlinkRun::FOnGenerateTooltip ToolTipDelegate;

private:
	UCS3RichTextBlockHyperlinkDecorator* Decorator;
};

/**
 * UCS3RichTextBlockHyperlinkDecorator
 * 富文本中解析超链接资源的类
 */
UCLASS(Blueprintable)
class CHUANGSHI_API UCS3RichTextBlockHyperlinkDecorator : public UCS3RichTextBlockDecorator
{
	GENERATED_BODY()

public:
	UCS3RichTextBlockHyperlinkDecorator(const FObjectInitializer& ObjectInitializer);

	virtual TSharedPtr<ITextDecorator> CreateDecorator(UCS3RichTextBlock* InOwner) override;

};