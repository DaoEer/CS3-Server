#pragma once

#include "CoreMinimal.h"
#include "UObject/ObjectMacros.h"
#include "UObject/Object.h"
#include "Fonts/SlateFontInfo.h"
#include "Styling/SlateTypes.h"
#include "Framework/Text/TextLayout.h"
#include "Framework/Text/ISlateRun.h"
#include "Framework/Text/ITextDecorator.h"
#include "CS3RichTextBlockDecorator.generated.h"

class ISlateStyle;
class UCS3RichTextBlockDecorator;
class UCS3RichTextBlock;

/**
* FCS3RichTextDecorator
* 富文本中解析文本资源的类
*/
class FCS3RichTextDecorator : public ITextDecorator
{
public:
	FCS3RichTextDecorator(UCS3RichTextBlock* InOwner);

	virtual ~FCS3RichTextDecorator() {}

	virtual bool Supports(const FTextRunParseResults& RunParseResult, const FString& Text) const override;

	virtual TSharedRef<ISlateRun> Create(const TSharedRef<class FTextLayout>& TextLayout, const FTextRunParseResults& RunParseResult, const FString& OriginalText, const TSharedRef<FString>& InOutModelText, const ISlateStyle* Style) override;

protected:
	virtual TSharedPtr<SWidget> CreateDecoratorWidget(const FTextRunInfo& RunInfo, const FTextBlockStyle& DefaultTextStyle) const;

private:
	FTextBlockStyle CreateTextBlockStyle(const FRunInfo& InRunInfo) const;

	void ExplodeRunInfo(const FRunInfo& InRunInfo, FSlateFontInfo& OutFont, FLinearColor& OutFontColor, FLinearColor& OutFontShadowColor, FVector2D& OutFontShadowOffset) const;

protected:
	UCS3RichTextBlock* Owner;
};

/**
* UCS3RichTextBlockDecorator
* 富文本中解析文本资源的类
*/
UCLASS(Blueprintable)
class CHUANGSHI_API UCS3RichTextBlockDecorator : public UObject
{
	GENERATED_BODY()

public:
	UCS3RichTextBlockDecorator(const FObjectInitializer& ObjectInitializer);

	virtual TSharedPtr<ITextDecorator> CreateDecorator(UCS3RichTextBlock* InOwner);
};