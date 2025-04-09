#include "CS3RichTextBlockImageDecorator.h"
#include "UObject/SoftObjectPtr.h"
#include "Framework/Text/SlateImageRun.h"
#include "Styling/SlateBrush.h"

#include "Guis/CS3RichTextBlock.h"
#include "Guis/CS3Styles.h"
#include "Guis/CS3GlobalStyle.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"

#define LOCTEXT_NAMESPACE "UMG"
CONTROL_COMPILE_OPTIMIZE_START
#pragma region	/** FCS3ImageDecorator */
FCS3ImageDecorator::FCS3ImageDecorator(UCS3RichTextBlock* InOwner, UCS3RichTextBlockImageDecorator* InDecorator)
	: FCS3RichTextDecorator(InOwner)
	, Decorator(InDecorator)
{

}


bool FCS3ImageDecorator::Supports(const FTextRunParseResults& RunParseResult, const FString& Text) const
{
	if (RunParseResult.Name == TEXT("img") && RunParseResult.MetaData.Contains(TEXT("src")))
	{
		const FTextRange& IdRange = RunParseResult.MetaData[TEXT("src")];
		const FString TagId = Text.Mid(IdRange.BeginIndex, IdRange.EndIndex - IdRange.BeginIndex);

		return Decorator->FindImageBrush(TagId) != nullptr;
	}

	return false;
}

/**
 * 处理富文本中的图像
 * <img src="A1"/> 读取BluePrints\UI\Styles\CS3SlateWidgetStyleAsset资源RichTextImageMap中的画刷进行显示
 **/
TSharedRef< ISlateRun > FCS3ImageDecorator::Create(const TSharedRef<class FTextLayout>& TextLayout, const FTextRunParseResults& RunParseResult, const FString& OriginalText, const TSharedRef< FString >& InOutModelText, const ISlateStyle* Style)
{
	const FTextRange* const BrushNameRange = RunParseResult.MetaData.Find(TEXT("src"));

	FTextRange ModelRange;
	ModelRange.BeginIndex = InOutModelText->Len();
	*InOutModelText += TEXT('\x200B');
	ModelRange.EndIndex = InOutModelText->Len();

	FRunInfo RunInfo(RunParseResult.Name);
	for (const TPair<FString, FTextRange>& Pair : RunParseResult.MetaData)
	{
		RunInfo.MetaData.Add(Pair.Key, OriginalText.Mid(Pair.Value.BeginIndex, Pair.Value.EndIndex - Pair.Value.BeginIndex));
	}

	if (BrushNameRange != NULL)
	{
		const FString BrushNameString = OriginalText.Mid(BrushNameRange->BeginIndex, BrushNameRange->EndIndex - BrushNameRange->BeginIndex);
		const FSlateBrush* InImage = Decorator->FindImageBrush(RunInfo.MetaData[TEXT("src")]);
		if (InImage)
		{
			return FSlateImageRun::Create(RunInfo, InOutModelText, InImage, 0, ModelRange);
		}
	}

	//默认显示
	const FInlineTextImageStyle& ImageStyle = FInlineTextImageStyle::GetDefault();
	return FSlateImageRun::Create(RunInfo, InOutModelText, &ImageStyle.Image, ImageStyle.Baseline, ModelRange);
}
#pragma endregion

#pragma region	/** UCS3RichTextBlockImageDecorator */
UCS3RichTextBlockImageDecorator::UCS3RichTextBlockImageDecorator(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{

}

UCS3RichTextBlockImageDecorator::~UCS3RichTextBlockImageDecorator()
{
	/*if (ImageTexture)
	{
		ImageTexture->RemoveFromRoot();
	}*/
}

TSharedPtr<ITextDecorator> UCS3RichTextBlockImageDecorator::CreateDecorator(UCS3RichTextBlock* InOwner)
{
	return MakeShareable(new FCS3ImageDecorator(InOwner, this));
}

const FSlateBrush* UCS3RichTextBlockImageDecorator::FindImageBrush(FString BrushNameString)
{
	if (BrushNameString != TEXT(""))
	{
		FName BrushName(*BrushNameString);
		const FRichTextImage* RichTextImage = (&FCS3Styles::Get().GetWidgetStyle<FGlobalCS3Style>("CS3SlateWidgetStyleAsset"))->RichTextImageMap.Find(BrushName);
		if (RichTextImage)
		{
			ImageTexture = RichTextImage->Image;
			if (IsValid(ImageTexture))
			{
				//ImageTexture->AddToRoot();
				//显示配置中的图片资源
				//不能使用MakeShareable，显示不出图片
				//TSharedPtr<FSlateBrush> InImage = MakeShareable(new FSlateBrush());
				FSlateBrush* InImage = new FSlateBrush();
				InImage->SetResourceObject(ImageTexture);
				InImage->ImageSize = FVector2D(ImageTexture->GetSizeX(), ImageTexture->GetSizeY());
				InImage->DrawAs = ESlateBrushDrawType::Image;
				return InImage;
			}
		}
		else
		{
			const FRichTextAnimatedImage* AnimatedImage = (&FCS3Styles::Get().GetWidgetStyle<FGlobalCS3Style>("CS3SlateWidgetStyleAsset"))->RichTextAnimatedImageMap.Find(BrushName);
			if (AnimatedImage)
			{
				ImageAnimatedTexture = AnimatedImage->Image;
				if (IsValid(ImageAnimatedTexture))
				{
					FSlateBrush* InImage = new FSlateBrush();
					InImage->SetResourceObject(ImageAnimatedTexture);
					InImage->ImageSize = FVector2D(ImageAnimatedTexture->GetSurfaceWidth(), ImageAnimatedTexture->GetSurfaceHeight());
					InImage->DrawAs = ESlateBrushDrawType::Image;
					return InImage;
				}
			}
		}
	}
	return nullptr;
}
#pragma endregion
CONTROL_COMPILE_OPTIMIZE_END
#undef LOCTEXT_NAMESPACE