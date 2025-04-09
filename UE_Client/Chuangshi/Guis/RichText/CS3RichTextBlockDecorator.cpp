#include "CS3RichTextBlockDecorator.h"
#include "UObject/SoftObjectPtr.h"
#include "Rendering/DrawElements.h"
#include "Framework/Text/SlateTextRun.h"
#include "Components/RichTextBlock.h"
#include "Guis/CS3RichTextBlock.h"

#define LOCTEXT_NAMESPACE "UMG"

#pragma region	/** FCS3RichTextDecorator */
FCS3RichTextDecorator::FCS3RichTextDecorator(UCS3RichTextBlock* InOwner)
	: Owner(InOwner)
{

}

bool FCS3RichTextDecorator::Supports(const FTextRunParseResults& RunParseResult, const FString& Text) const
{
	return (RunParseResult.Name == TEXT("span"));
}

TSharedRef<ISlateRun> FCS3RichTextDecorator::Create(const TSharedRef<class FTextLayout>& TextLayout, const FTextRunParseResults& RunParseResult, const FString& OriginalText, const TSharedRef<FString>& InOutModelText, const ISlateStyle* Style)
{
	FRunInfo RunInfo(RunParseResult.Name);
	for (const TPair<FString, FTextRange>& Pair : RunParseResult.MetaData)
	{
		RunInfo.MetaData.Add(Pair.Key, OriginalText.Mid(Pair.Value.BeginIndex, Pair.Value.EndIndex - Pair.Value.BeginIndex));
	}

	FTextRange ModelRange;
	ModelRange.BeginIndex = InOutModelText->Len();
	*InOutModelText += OriginalText.Mid(RunParseResult.ContentRange.BeginIndex, RunParseResult.ContentRange.EndIndex - RunParseResult.ContentRange.BeginIndex);
	ModelRange.EndIndex = InOutModelText->Len();
	
	return FSlateTextRun::Create(RunInfo, InOutModelText, CreateTextBlockStyle(RunInfo), ModelRange);
}

TSharedPtr<SWidget> FCS3RichTextDecorator::CreateDecoratorWidget(const FTextRunInfo& RunInfo, const FTextBlockStyle& DefaultTextStyle) const
{
	return TSharedPtr<SWidget>();
}

FTextBlockStyle FCS3RichTextDecorator::CreateTextBlockStyle(const FRunInfo& InRunInfo) const
{
	FSlateFontInfo Font;
	FLinearColor FontColor;
	FLinearColor ShadowColorAndOpacity;
	FVector2D ShadowOffset;
	ExplodeRunInfo(InRunInfo, Font, FontColor, ShadowColorAndOpacity, ShadowOffset);

	FTextBlockStyle TextBlockStyle;
	TextBlockStyle.SetFont(Font);
	TextBlockStyle.SetColorAndOpacity(FontColor);
	TextBlockStyle.SetShadowColorAndOpacity(ShadowColorAndOpacity);
	TextBlockStyle.SetShadowOffset(ShadowOffset);

	return TextBlockStyle;
}

void FCS3RichTextDecorator::ExplodeRunInfo(const FRunInfo& InRunInfo, FSlateFontInfo& OutFont, FLinearColor& OutFontColor, FLinearColor& OutFontShadowColor, FVector2D& OutFontShadowOffset) const
{
	const FTextBlockStyle& DefaultTextStyle = Owner->GetDefaultTextStyle();

	OutFont = DefaultTextStyle.Font;

	const FString* const FontFamilyString = InRunInfo.MetaData.Find(TEXT("font"));
	const FString* const FontSizeString = InRunInfo.MetaData.Find(TEXT("size"));
	const FString* const FontStyleString = InRunInfo.MetaData.Find(TEXT("style"));
	const FString* const FontColorString = InRunInfo.MetaData.Find(TEXT("color"));
	const FString* const FontShadowColorString = InRunInfo.MetaData.Find(TEXT("shadowColor"));
	const FString* const FontShadowOffsetString = InRunInfo.MetaData.Find(TEXT("shadowOffset"));

	if (FontFamilyString)
	{
		FSoftObjectPath Font(**FontFamilyString);
		if (UObject* FontAsset = Font.TryLoad())
		{
			OutFont.FontObject = FontAsset;
		}
	}

	if (FontSizeString)
	{
		OutFont.Size = static_cast<uint8>(FPlatformString::Atoi(**FontSizeString));
	}

	if (FontStyleString)
	{
		OutFont.TypefaceFontName = FName(**FontStyleString);
	}

	OutFontColor = DefaultTextStyle.ColorAndOpacity.GetSpecifiedColor();
	if (FontColorString)
	{
		const FString& FontColorStringRef = *FontColorString;

		// Is Hex color?
		if (!FontColorStringRef.IsEmpty() && FontColorStringRef[0] == TCHAR('#'))
		{
			OutFontColor = FLinearColor(FColor::FromHex(FontColorStringRef));
		}
		else if (OutFontColor.InitFromString(*FontColorString))
		{
			// Initialized
		}
		else
		{
			OutFontColor = DefaultTextStyle.ColorAndOpacity.GetSpecifiedColor();
		}
	}

	OutFontShadowColor = DefaultTextStyle.ShadowColorAndOpacity;
	if (FontShadowColorString)
	{
		const FString& FontShadowColorStringRef = *FontShadowColorString;

		// Is Hex color?
		if (!FontShadowColorStringRef.IsEmpty() && FontShadowColorStringRef[0] == TCHAR('#'))
		{
			OutFontShadowColor = FLinearColor(FColor::FromHex(FontShadowColorStringRef));
		}
		else if (OutFontShadowColor.InitFromString(*FontShadowColorString))
		{
			// Initialized
		}
		else
		{
			OutFontShadowColor = DefaultTextStyle.ShadowColorAndOpacity;
		}
	}

	OutFontShadowOffset = DefaultTextStyle.ShadowOffset;
	if (FontShadowOffsetString)
	{
		FString ShadowOffsetStringRef = *FontShadowOffsetString;
		ShadowOffsetStringRef.ReplaceInline(TEXT("["), TEXT(" "));
		ShadowOffsetStringRef.ReplaceInline(TEXT("]"), TEXT(" "));
		ShadowOffsetStringRef.TrimStartAndEndInline();

		TArray<FString> parse;

		ShadowOffsetStringRef.ParseIntoArray(parse, TEXT(","), true);
		if (parse.Num() >= 2) {
			OutFontShadowOffset = FVector2D(FCString::Atof(*parse[0]), FCString::Atof(*parse[1]));
		}
	}
}
#pragma endregion

#pragma region	/** UCS3RichTextBlockDecorator */
UCS3RichTextBlockDecorator::UCS3RichTextBlockDecorator(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
}

TSharedPtr<ITextDecorator> UCS3RichTextBlockDecorator::CreateDecorator(UCS3RichTextBlock* InOwner)
{
	return MakeShareable(new FCS3RichTextDecorator(InOwner));
	//return TSharedPtr<ITextDecorator>();
}
#pragma endregion

#undef LOCTEXT_NAMESPACE