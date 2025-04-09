#pragma once
#include "CoreMinimal.h"
#include "UObject/ObjectMacros.h"
#include "UObject/Object.h"
#include "Fonts/SlateFontInfo.h"
#include "Styling/SlateTypes.h"
#include "Framework/Text/TextLayout.h"
#include "Framework/Text/ISlateRun.h"
#include "Framework/Text/ITextDecorator.h"

#include "CS3RichTextBlockDecorator.h"
#include "AnimatedTexture2D.h"
#include "CS3RichTextBlockImageDecorator.generated.h"

class ISlateStyle;
class UCS3RichTextBlockImageDecorator;
class UCS3RichTextBlock;

/**
 * FCS3RichTextBlockImageDecorator
 * 富文本中解析图片资源的类
 */
class FCS3ImageDecorator : public FCS3RichTextDecorator
{
public:
	FCS3ImageDecorator(UCS3RichTextBlock* InOwner, UCS3RichTextBlockImageDecorator* InDecorator);
	
	virtual ~FCS3ImageDecorator() {}
	
	virtual bool Supports(const FTextRunParseResults& RunParseResult, const FString& Text) const override;

	virtual TSharedRef< ISlateRun > Create(const TSharedRef<class FTextLayout>& TextLayout, const FTextRunParseResults& RunParseResult, const FString& OriginalText, const TSharedRef< FString >& InOutModelText, const ISlateStyle* Style) override;
	
private:
	UCS3RichTextBlockImageDecorator* Decorator;
};

/**
 * UCS3RichTextBlockImageDecorator
 * 富文本中解析图片资源的类
 */
UCLASS(Blueprintable)
class CHUANGSHI_API UCS3RichTextBlockImageDecorator : public UCS3RichTextBlockDecorator
{
	GENERATED_BODY()

public:
	UCS3RichTextBlockImageDecorator(const FObjectInitializer& ObjectInitializer);

	~UCS3RichTextBlockImageDecorator();

	virtual TSharedPtr<ITextDecorator> CreateDecorator(UCS3RichTextBlock* InOwner) override;

	const FSlateBrush* FindImageBrush(FString BrushNameString);
	
	UPROPERTY()
		UTexture2D* ImageTexture;
	UPROPERTY()
		UAnimatedTexture2D* ImageAnimatedTexture;
};