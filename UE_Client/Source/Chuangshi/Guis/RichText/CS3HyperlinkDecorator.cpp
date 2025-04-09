#include "CS3HyperlinkDecorator.h"
#include "UObject/SoftObjectPtr.h"
#include "Widgets/Input/SRichTextHyperlink.h"
#include "Templates/SharedPointer.h"
#include "Guis/CS3RichTextBlock.h"
#include "Guis/CS3Styles.h"
#include "Guis/CS3GlobalStyle.h"

#define LOCTEXT_NAMESPACE "UMG"
class CSSRichTextHyperlink : public SHyperlink
{
public:

	SLATE_BEGIN_ARGS(CSSRichTextHyperlink)
		: _Text()
		, _Style(&FCoreStyle::Get().GetWidgetStyle< FHyperlinkStyle >("Hyperlink"))
		, _OnNavigate()
		, _TextShapingMethod()
		, _TextFlowDirection()
	{}
	SLATE_ATTRIBUTE(FText, Text)
		SLATE_STYLE_ARGUMENT(FHyperlinkStyle, Style)
		SLATE_EVENT(FSimpleDelegate, OnNavigate)
		SLATE_ARGUMENT(TOptional<ETextShapingMethod>, TextShapingMethod)
		SLATE_ARGUMENT(TOptional<ETextFlowDirection>, TextFlowDirection)
		SLATE_END_ARGS()

public:

	void Construct(const FArguments& InArgs, const TSharedRef< FSlateHyperlinkRun::FWidgetViewModel >& InViewModel)
	{
		ViewModel = InViewModel;

		SHyperlink::Construct(
			SHyperlink::FArguments()
			.Text(InArgs._Text)
			.Style(InArgs._Style)
			.Padding(FMargin(0))
			.OnNavigate(InArgs._OnNavigate)
			.TextShapingMethod(InArgs._TextShapingMethod)
			.TextFlowDirection(InArgs._TextFlowDirection)
		);
		//CST-9777 这个为true会导致焦点切换，当一直按住某键时会被判断双击。
		bIsFocusable = false;
	}

	virtual void OnMouseEnter(const FGeometry& MyGeometry, const FPointerEvent& MouseEvent) override
	{
		SHyperlink::OnMouseEnter(MyGeometry, MouseEvent);
		ViewModel->SetIsHovered(true);
	}

	virtual void OnMouseLeave(const FPointerEvent& MouseEvent) override
	{
		SHyperlink::OnMouseLeave(MouseEvent);
		ViewModel->SetIsHovered(false);
	}

	virtual FReply OnMouseButtonDown(const FGeometry& MyGeometry, const FPointerEvent& MouseEvent) override
	{
		FReply Reply = SHyperlink::OnMouseButtonDown(MyGeometry, MouseEvent);
		ViewModel->SetIsPressed(bIsPressed);

		return Reply;
	}

	virtual FReply OnMouseButtonUp(const FGeometry& MyGeometry, const FPointerEvent& MouseEvent) override
	{
		FReply Reply = SHyperlink::OnMouseButtonUp(MyGeometry, MouseEvent);
		ViewModel->SetIsPressed(bIsPressed);

		return Reply;
	}

	virtual bool IsHovered() const override
	{
		return ViewModel->IsHovered();
	}

	virtual bool IsPressed() const override
	{
		return ViewModel->IsPressed();
	}

private:

	TSharedPtr< FSlateHyperlinkRun::FWidgetViewModel > ViewModel;
};

class  FCSSlateHyperlinkRun : public FSlateHyperlinkRun //, public TSharedFromThis< FCSSlateHyperlinkRun >
{
public:

	static TSharedRef< FCSSlateHyperlinkRun > CSCreate(const FRunInfo& InRunInfo, const TSharedRef< const FString >& InText, const FHyperlinkStyle& InStyle, FOnClick NavigateDelegate, FOnGenerateTooltip InTooltipDelegate, FOnGetTooltipText InTooltipTextDelegate);

	static TSharedRef< FCSSlateHyperlinkRun > CSCreate(const FRunInfo& InRunInfo, const TSharedRef< const FString >& InText, const FHyperlinkStyle& InStyle, FOnClick NavigateDelegate, FOnGenerateTooltip InTooltipDelegate, FOnGetTooltipText InTooltipTextDelegate, const FTextRange& InRange);

	FCSSlateHyperlinkRun(const FRunInfo& InRunInfo, const TSharedRef< const FString >& InText, const FHyperlinkStyle& InStyle, FOnClick InNavigateDelegate, FOnGenerateTooltip InTooltipDelegate, FOnGetTooltipText InTooltipTextDelegate):
		FSlateHyperlinkRun(InRunInfo, InText, InStyle, InNavigateDelegate, InTooltipDelegate, InTooltipTextDelegate)
	{
	}

	FCSSlateHyperlinkRun(const FRunInfo& InRunInfo, const TSharedRef< const FString >& InText, const FHyperlinkStyle& InStyle, FOnClick InNavigateDelegate, FOnGenerateTooltip InTooltipDelegate, FOnGetTooltipText InTooltipTextDelegate, const FTextRange& InRange):
		FSlateHyperlinkRun(InRunInfo, InText, InStyle, InNavigateDelegate, InTooltipDelegate, InTooltipTextDelegate, InRange)
	{
	}

	FCSSlateHyperlinkRun(const FSlateHyperlinkRun& Run):
		FSlateHyperlinkRun(Run)
	{
	}

	virtual TSharedRef< ILayoutBlock > CreateBlock(int32 StartIndex, int32 EndIndex, FVector2D Size, const FLayoutBlockTextContext& TextContext, const TSharedPtr< IRunRenderer >& Renderer) override;
};

TSharedRef< FCSSlateHyperlinkRun > FCSSlateHyperlinkRun::CSCreate(const FRunInfo& InRunInfo, const TSharedRef< const FString >& InText, const FHyperlinkStyle& InStyle, FOnClick NavigateDelegate, FOnGenerateTooltip InTooltipDelegate, FOnGetTooltipText InTooltipTextDelegate)
{
	return MakeShareable(new FCSSlateHyperlinkRun(InRunInfo, InText, InStyle, NavigateDelegate, InTooltipDelegate, InTooltipTextDelegate));
}

TSharedRef< FCSSlateHyperlinkRun > FCSSlateHyperlinkRun::CSCreate(const FRunInfo& InRunInfo, const TSharedRef< const FString >& InText, const FHyperlinkStyle& InStyle, FOnClick NavigateDelegate, FOnGenerateTooltip InTooltipDelegate, FOnGetTooltipText InTooltipTextDelegate, const FTextRange& InRange)
{
	return MakeShareable(new FCSSlateHyperlinkRun(InRunInfo, InText, InStyle, NavigateDelegate, InTooltipDelegate, InTooltipTextDelegate, InRange));
}

TSharedRef< ILayoutBlock > FCSSlateHyperlinkRun::CreateBlock(int32 StartIndex, int32 EndIndex, FVector2D Size, const FLayoutBlockTextContext& TextContext, const TSharedPtr< IRunRenderer >& Renderer)
{
	FText ToolTipText;
	TSharedPtr<IToolTip> ToolTip;

	if (TooltipDelegate.IsBound())
	{
		ToolTip = TooltipDelegate.Execute(RunInfo.MetaData);
	}
	else
	{
		const FString* Url = RunInfo.MetaData.Find(TEXT("href"));
		if (TooltipTextDelegate.IsBound())
		{
			ToolTipText = TooltipTextDelegate.Execute(RunInfo.MetaData);
		}
		else if (Url != nullptr)
		{
			ToolTipText = FText::FromString(*Url);
		}
	}

	TSharedRef< SWidget > Widget = SNew(CSSRichTextHyperlink, ViewModel)
		.Style(&Style)
		.Text(FText::FromString(FString(EndIndex - StartIndex, **Text + StartIndex)))
		.ToolTip(ToolTip)
		.ToolTipText(ToolTipText)
		.OnNavigate(this, &FCSSlateHyperlinkRun::OnNavigate)
		.TextShapingMethod(TextContext.TextShapingMethod);

	// We need to do a prepass here as CreateBlock can be called after the main Slate prepass has been run, 
	// which can result in the hyperlink widget not being correctly setup before it is painted
	Widget->SlatePrepass();

	Children.Add(Widget);

	return FWidgetLayoutBlock::Create(SharedThis(this), Widget, FTextRange(StartIndex, EndIndex), Size, TextContext, Renderer);
}

#pragma region	/** FCS3HyperlinkDecorator */
FCS3HyperlinkDecorator::FCS3HyperlinkDecorator(UCS3RichTextBlock* InOwner, UCS3RichTextBlockHyperlinkDecorator* InDecorator)
	: FCS3RichTextDecorator(InOwner)
	, ToolTipTextDelegate(nullptr)
	, ToolTipDelegate(FSlateHyperlinkRun::FSlateHyperlinkRun::FOnGenerateTooltip::CreateStatic(&FCS3HyperlinkDecorator::DelegateHyperlinkToolTip))
	, Decorator(InDecorator)
{
	NavigateDelegate = FSlateHyperlinkRun::FOnClick::CreateLambda([InOwner](const FSlateHyperlinkRun::FMetadata& Metadata)
	{
		InOwner->OnHyperlinkDecoratorClicked(Metadata);
	});
}

bool FCS3HyperlinkDecorator::Supports(const FTextRunParseResults& RunParseResult, const FString& Text) const
{
	if (RunParseResult.Name == TEXT("a") && RunParseResult.MetaData.Contains(TEXT("id")))
	{
		const FTextRange* const MetaDataIdRange = RunParseResult.MetaData.Find(TEXT("id"));
		FString MetaDataId;
		if (MetaDataIdRange)
		{
			MetaDataId = Text.Mid(MetaDataIdRange->BeginIndex, MetaDataIdRange->EndIndex - MetaDataIdRange->BeginIndex);
		}

		return (MetaDataId == TEXT("HyperlinkDecorator"));
	}

	return false;
}

/**
 * 处理超链接提示框样式和字体
 */
TSharedRef<IToolTip> FCS3HyperlinkDecorator::DelegateHyperlinkToolTip(const FSlateHyperlinkRun::FMetadata& Metadata)
{
	const FString* URL = Metadata.Find(TEXT("href"));
	bool IsShowHyperlinkToolTip = (&FCS3Styles::Get().GetWidgetStyle<FGlobalCS3Style>("CS3SlateWidgetStyleAsset"))->IsShowHyperlinkToolTip;
	FText ToolTipText;
	if (URL != nullptr && IsShowHyperlinkToolTip)
	{
		ToolTipText = FText::AsCultureInvariant(*URL);
	}
	else
	{
		ToolTipText = FText::AsCultureInvariant("");
	}

	//获取提示框字体和背景画刷配置,配置路径BluePrints\UI\Styles\CS3SlateWidgetStyleAsset
	const FSlateFontInfo &Font = (&FCS3Styles::Get().GetWidgetStyle<FGlobalCS3Style>("CS3SlateWidgetStyleAsset"))->HyperlinkToolTipFont;
	const FSlateBrush &BorderImage = (&FCS3Styles::Get().GetWidgetStyle<FGlobalCS3Style>("CS3SlateWidgetStyleAsset"))->HyperlinkToolTipBrush;

	return SNew(SToolTip)
		.BorderImage(&BorderImage)
		[
			SNew(STextBlock)
			.Text(ToolTipText)
		.Font(Font)
		.ColorAndOpacity(FSlateColor::UseForeground())
		.WrapTextAt_Static(&SToolTip::GetToolTipWrapWidth)
		];
}
/**
 * 解析富文本中的超链接进行显示
 * <a id="HyperlinkDecorator" style="Hyperlink" href="AABBCCDD" textstyle="MonospacedText" size="52" color="#FF0000">Hyperlink</>
 **/
TSharedRef< ISlateRun > FCS3HyperlinkDecorator::Create(const TSharedRef<class FTextLayout>& TextLayout, const FTextRunParseResults& RunParseResult, const FString& OriginalText, const TSharedRef< FString >& InOutModelText, const ISlateStyle* Style)
{
	FString StyleName = TEXT("Hyperlink");

	const FTextRange* const MetaDataStyleNameRange = RunParseResult.MetaData.Find(TEXT("style"));
	const FTextRange* const FontFamilyString = RunParseResult.MetaData.Find(TEXT("font"));
	const FTextRange* const FontSizeString = RunParseResult.MetaData.Find(TEXT("size"));
	const FTextRange* const FontColorString = RunParseResult.MetaData.Find(TEXT("color"));
	const FTextRange* const ButtonStyleRange = RunParseResult.MetaData.Find(TEXT("bstyle"));
	const FTextRange* const FontShadowColorString = RunParseResult.MetaData.Find(TEXT("shadowColor"));
	const FTextRange* const FontShadowOffsetString = RunParseResult.MetaData.Find(TEXT("shadowOffset"));

	if (MetaDataStyleNameRange != NULL)
	{
		const FString MetaDataStyleName = OriginalText.Mid(MetaDataStyleNameRange->BeginIndex, MetaDataStyleNameRange->EndIndex - MetaDataStyleNameRange->BeginIndex);
		StyleName = *MetaDataStyleName;
	}

	FTextRange ModelRange;
	ModelRange.BeginIndex = InOutModelText->Len();
	*InOutModelText += OriginalText.Mid(RunParseResult.ContentRange.BeginIndex, RunParseResult.ContentRange.EndIndex - RunParseResult.ContentRange.BeginIndex);
	ModelRange.EndIndex = InOutModelText->Len();

	if (!Style->HasWidgetStyle<FHyperlinkStyle>(FName(*StyleName)))
	{
		Style = &FCoreStyle::Get();
	}

	FRunInfo RunInfo(RunParseResult.Name);
	for (const TPair<FString, FTextRange>& Pair : RunParseResult.MetaData)
	{
		RunInfo.MetaData.Add(Pair.Key, OriginalText.Mid(Pair.Value.BeginIndex, Pair.Value.EndIndex - Pair.Value.BeginIndex));
	}

	//字体样式
	FHyperlinkStyle HyperlinkStyle = Style->GetWidgetStyle<FHyperlinkStyle>(FName(*StyleName));
	const FTextBlockStyle& DefaultTextStyle = Owner->GetDefaultTextStyle();
	HyperlinkStyle.TextStyle = DefaultTextStyle;

	//显示文字大小
	if (FontSizeString)
	{
		const FString FontSize = OriginalText.Mid(FontSizeString->BeginIndex, FontSizeString->EndIndex - FontSizeString->BeginIndex);
		HyperlinkStyle.TextStyle.Font.Size = static_cast<uint8>(FPlatformString::Atoi(*FontSize));
	}

	//显示文字颜色
	if (FontColorString)
	{
		FLinearColor OutFontColor;
		const FString FontColor = OriginalText.Mid(FontColorString->BeginIndex, FontColorString->EndIndex - FontColorString->BeginIndex);
		const FString& FontColorStringRef = *FontColor;

		if (!FontColorStringRef.IsEmpty() && FontColorStringRef[0] == TCHAR('#'))
		{
			OutFontColor = FLinearColor(FColor::FromHex(FontColorStringRef));
		}

		HyperlinkStyle.TextStyle.SetColorAndOpacity(OutFontColor);
	}

	//获取背景按键画刷
	if (ButtonStyleRange)
	{
		const FString ButtonStyleString = OriginalText.Mid(ButtonStyleRange->BeginIndex, ButtonStyleRange->EndIndex - ButtonStyleRange->BeginIndex);
		FName ButtonStyleName(*ButtonStyleString);
		const FButtonStyle *RichTextHyperlinkButton = (&FCS3Styles::Get().GetWidgetStyle<FGlobalCS3Style>("CS3SlateWidgetStyleAsset"))->HyperlinkButtonStyleMap.Find(ButtonStyleName);
		if (RichTextHyperlinkButton)
		{
			HyperlinkStyle.SetUnderlineStyle(*RichTextHyperlinkButton);
		}
	}
	else
	{
		//const FButtonStyle &RichTextHyperlinkButton = (&FCS3Styles::Get().GetWidgetStyle<FGlobalCS3Style>("CS3SlateWidgetStyleAsset"))->HyperlinkButtonStyle;
		//HyperlinkStyle.SetUnderlineStyle(RichTextHyperlinkButton);
	}

	//显示文字阴影颜色
	if (FontShadowColorString)
	{
		FLinearColor OutFontShadowColor;
		const FString FontShadowColor = OriginalText.Mid(FontShadowColorString->BeginIndex, FontShadowColorString->EndIndex - FontShadowColorString->BeginIndex);
		const FString& FontShadowColorStringRef = *FontShadowColor;

		if (!FontShadowColorStringRef.IsEmpty() && FontShadowColorStringRef[0] == TCHAR('#'))
		{
			OutFontShadowColor = FLinearColor(FColor::FromHex(FontShadowColorStringRef));
		}

		HyperlinkStyle.TextStyle.SetShadowColorAndOpacity(OutFontShadowColor);
	}

	//文字阴影
	if (FontShadowOffsetString)
	{
		FVector2D OutFontShadowOffset;
		FString FontShadowOffset = OriginalText.Mid(FontShadowOffsetString->BeginIndex, FontShadowOffsetString->EndIndex - FontShadowOffsetString->BeginIndex);
		FontShadowOffset.ReplaceInline(TEXT("["), TEXT(" "));
		FontShadowOffset.ReplaceInline(TEXT("]"), TEXT(" "));
		FontShadowOffset.TrimStartAndEndInline();

		TArray<FString> parse;

		FontShadowOffset.ParseIntoArray(parse, TEXT(","), true);
		if (parse.Num() >= 2) {
			OutFontShadowOffset = FVector2D(FCString::Atof(*parse[0]), FCString::Atof(*parse[1]));
		}
		HyperlinkStyle.TextStyle.SetShadowOffset(OutFontShadowOffset);
	}

	return FCSSlateHyperlinkRun::CSCreate(RunInfo, InOutModelText, HyperlinkStyle, NavigateDelegate, ToolTipDelegate, ToolTipTextDelegate, ModelRange);
}
#pragma endregion

#pragma region	/** UCS3RichTextBlockHyperlinkDecorator */
UCS3RichTextBlockHyperlinkDecorator::UCS3RichTextBlockHyperlinkDecorator(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{

}

TSharedPtr<ITextDecorator> UCS3RichTextBlockHyperlinkDecorator::CreateDecorator(UCS3RichTextBlock* InOwner)
{
	return MakeShareable(new FCS3HyperlinkDecorator(InOwner, this));
}
#pragma endregion

#undef LOCTEXT_NAMESPACE