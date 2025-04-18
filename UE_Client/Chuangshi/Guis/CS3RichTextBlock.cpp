// Fill out your copyright notice in the Description page of Project Settings.

#include "CS3RichTextBlock.h"
#include "Kismet/KismetTextLibrary.h"
#include "Kismet/KismetStringLibrary.h"
#include "Engine/Font.h"
#include "UObject/ConstructorHelpers.h"
#include "UnrealString.h"

#include "Manager/HyperlinkManager.h"
#include "Manager/TextParseManager.h"
#include "RichText/CS3RichTextBlockDecorator.h"
#include "RichText/CS3HyperlinkDecorator.h"
#include "RichText/CS3RichTextBlockImageDecorator.h"
#include "SlateHyperlinkRun.h"
#include "Util/CS3Debug.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/ConvertUtil.h"

#define LOCTEXT_NAMESPACE "UMG"

UCS3RichTextBlock::UCS3RichTextBlock(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
	if (!IsRunningDedicatedServer())
	{
		static ConstructorHelpers::FObjectFinder<UFont> RobotoFontObj(TEXT("/Engine/EngineFonts/Roboto"));
		Font = FSlateFontInfo(RobotoFontObj.Object, 12, FName("Regular"));
	}
	ColorAndOpacity = FLinearColor::White;
	PreDecoratorClasses.Add(UCS3RichTextBlockDecorator::StaticClass());
	PreDecoratorClasses.Add(UCS3RichTextBlockImageDecorator::StaticClass());
	PreDecoratorClasses.Add(UCS3RichTextBlockHyperlinkDecorator::StaticClass());
}

void UCS3RichTextBlock::ReleaseSlateResources(bool bReleaseChildren)
{
	Super::ReleaseSlateResources(bReleaseChildren);

	MyRichTextBlock.Reset();
}

bool UCS3RichTextBlock::IsTickable() const
{
	return (bIsStartTickFadeText || bNeedRebuildFadeText) && MyRichTextBlock.IsValid();
}

void UCS3RichTextBlock::Tick(float DeltaTime)
{
	if (bNeedRebuildFadeText)
	{
		auto geometry = GetCachedGeometry();
		if (geometry.Size.X > 0 && geometry.Size.Y > 0)
		{
			bNeedRebuildFadeText = false;
			RebuildFadeText();
		}
		return;
	}

	//淡入
	if (bIsFadeIn)
	{
		FadeDeltaTime += DeltaTime;
		float CurrOpacity = FadeDeltaTime / FadeSpeed;
		//CS3_Display(CS3DebugType::CL_Undefined, TEXT("Tick-----bIsFadeIn:CurrOpacity[%f,%f]"), FadeDeltaTime, CurrOpacity);
		int32 TempOpacity = (CurrOpacity + 0.005) * 100;
		CurrOpacity = TempOpacity / 100.0f;
		if (CurrOpacity >= 0.00f && CurrOpacity <= 1.00f)
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("Tick-----SetOpacity(%f)"), CurrOpacity);
			SetOpacity(CurrOpacity);
		}
		else
		{
			SetOpacity(1.0f);
			bIsFadeIn = false;
			bIsFadeOut = true;
			FadeDeltaTime = 0.0f;
		}
	}
	else if (bIsFadeOut)
	{
		TextFadeTimer -= DeltaTime;
		if (TextFadeTimer <= 0.0f)
		{
			//淡出
			FadeDeltaTime += DeltaTime;
			float CurrOpacity = 1.00f - FadeDeltaTime / FadeSpeed;
			//CS3_Display(CS3DebugType::CL_Undefined, TEXT("Tick-----bIsFadeOut:CurrOpacity[%f,%f]"), FadeDeltaTime, CurrOpacity);
			int32 TempOpacity = (CurrOpacity + 0.005) * 100;
			CurrOpacity = TempOpacity / 100.0f;
			if (CurrOpacity >= 0.00f && CurrOpacity <= 1.00f)
			{
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("Tick-----SetOpacity(%f)"), CurrOpacity);
				SetOpacity(CurrOpacity);
			}
			else
			{
				bIsFadeOut = false;
				SetOpacity(0.0f);
				SetIsStartTickFadeText(false);
			}
		}
	} 
	else
	{
		SetIsStartTickFadeText(false);
	}
}

TSharedRef<SWidget> UCS3RichTextBlock::RebuildWidget()
{
	DefaultStyle.SetFont(Font);
	DefaultStyle.SetColorAndOpacity(ColorAndOpacity);
	DefaultStyle.SetShadowOffset(ShadowOffset);
	DefaultStyle.SetShadowColorAndOpacity(ShadowColorAndOpacity);

	UpdateStyleData();

	TArray< TSharedRef< class ITextDecorator > > CreatedDecorators;
	CreateDecorators(CreatedDecorators);
	
	MyRichTextBlock =
		SNew(SRichTextBlock)
		.TextStyle(&DefaultStyle)
		.AutoWrapText(true)
		.Justification(ETextJustify::Left)
		.Decorators(CreatedDecorators);

	return MyRichTextBlock.ToSharedRef();
}

void UCS3RichTextBlock::OnWidgetRebuilt()
{
	Super::OnWidgetRebuilt();
	if (!bCreationFromPalette) {

		bNeedRebuildFadeText = true;
	}
	else {
		bCreationFromPalette = false;
	}
}

void UCS3RichTextBlock::UpdateStyleData()
{
	if (IsDesignTime())
	{
		InstanceDecorators.Reset();
	}
	for (TSubclassOf<UCS3RichTextBlockDecorator> DecoratorClass : PreDecoratorClasses)
	{
		if (DecoratorClass && !DecoratorClass->GetClass()->HasAnyClassFlags(CLASS_Abstract))
		{
			UCS3RichTextBlockDecorator* Decorator = NewObject<UCS3RichTextBlockDecorator>(this, DecoratorClass.Get());
			InstanceDecorators.Add(Decorator);
		}
	}
}

void UCS3RichTextBlock::CreateDecorators(TArray< TSharedRef< class ITextDecorator > >& OutDecorators)
{
	for (UCS3RichTextBlockDecorator* Decorator : InstanceDecorators)
	{
		if (Decorator)
		{
			TSharedPtr<ITextDecorator> TextDecorator = Decorator->CreateDecorator(this);
			if (TextDecorator.IsValid())
			{
				OutDecorators.Add(TextDecorator.ToSharedRef());
			}
		}
	}
}

void UCS3RichTextBlock::SynchronizeProperties()
{
	Super::SynchronizeProperties();

	Text = ReplaceSpecialValue(Text);
	TAttribute<FText> TextBinding = PROPERTY_BINDING(FText, Text);

	if (MyRichTextBlock.IsValid())
	{
		MyRichTextBlock->SetText(TextBinding);
		MyRichTextBlock->SetJustification(Justification);
		DefaultStyle.SetFont(Font);
		DefaultStyle.SetColorAndOpacity(ColorAndOpacity);
		DefaultStyle.SetShadowOffset(ShadowOffset);
		DefaultStyle.SetShadowColorAndOpacity(ShadowColorAndOpacity);
		MyRichTextBlock->SetTextStyle(DefaultStyle);

		SetIsFadeText(bIsFadeText);
		SetIsStartTickFadeText(bIsStartTickFadeText);

		Super::SynchronizeTextLayoutProperties(*MyRichTextBlock);
	}
}

#if WITH_EDITOR

const FText UCS3RichTextBlock::GetPaletteCategory()
{
	return LOCTEXT("Common", "Common");
}

void UCS3RichTextBlock::OnCreationFromPalette()
{
// 	Decorators.Add(NewObject<UCS3RichTextBlockDecorator>(this, NAME_None, RF_Transactional));
// 	Text = FText::FromString("Rich Text Block");
	bCreationFromPalette = true;
}

#endif

/////////////////////////////////////////////////////
void UCS3RichTextBlock::OnHyperlinkDecoratorClicked(const FSlateHyperlinkRun::FMetadata& Metadata)
{
	//超链接点击事件
	OnHyperTextClicked.Broadcast();
	//解析超链接数据
	const FString* URL = Metadata.Find(TEXT("href"));
	if (URL && UUECS3GameInstance::Instance)
	{
		UHyperlinkManager* HyperlinkManager = UUECS3GameInstance::Instance->HyperlinkManager;
		HyperlinkManager->OnHyperlinkClicked(this, *URL);
	}
}

const FTextBlockStyle& UCS3RichTextBlock::GetDefaultTextStyle() const
{
	return DefaultStyle;
}

void UCS3RichTextBlock::SetText(FText InText)
{
#if WITH_EDITOR  // 在CST-7688需求中,需要在游戏未启动得时候使用富文本控件
	static UTextParseManger* TempTextParseMgr = NewObject<UTextParseManger>();
	static bool once = true;
	if (once)
	{
		TempTextParseMgr->Init(); //只执行一遍的代码
		TempTextParseMgr->AddToRoot();

		once = false;
	}
#else
	if (!IsValid(UUECS3GameInstance::Instance)) return;
	UTextParseManger* TempTextParseMgr = UUECS3GameInstance::Instance->TextParseMgr;
	if (!IsValid(TempTextParseMgr)) return;
#endif

	FString TransformStr = TempTextParseMgr->TransformText(InText.ToString());
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("TransformStr is %s,InText is %s"), *TransformStr, *(InText.ToString()));
	FText TransformText = UKismetTextLibrary::Conv_StringToText(TransformStr);
	Text = ReplaceSpecialValue(TransformText);
	if (MyRichTextBlock.IsValid())
	{
		MyRichTextBlock->SetText(Text);
	}
	RebuildFadeText();
}

FText UCS3RichTextBlock::GetText() const
{
	return Text;
}

void UCS3RichTextBlock::SetJustification(ETextJustify::Type InJustification)
{
	Justification = InJustification;
	if (MyRichTextBlock.IsValid())
	{
		MyRichTextBlock->SetJustification(Justification);
	}
}

TEnumAsByte<ETextJustify::Type> UCS3RichTextBlock::GetJustification() const
{
	return Justification;
}

#pragma region	/** 下面这些设置对于富文本都不生效，因为富文本是通过解析Text中的配置去设置Style的，要改变富文本的Style需要改变Text */
void UCS3RichTextBlock::SetFont(FSlateFontInfo InFontInfo)
{
	Font = InFontInfo;
	DefaultStyle.SetFont(Font);
	if (MyRichTextBlock.IsValid())
	{
		MyRichTextBlock->SetTextStyle(DefaultStyle);
	}
}

void UCS3RichTextBlock::SetFontSize(int fontSize)
{
	Font.Size = fontSize;
	DefaultStyle.SetFont(Font);
	if (MyRichTextBlock.IsValid())
	{
		MyRichTextBlock->SetTextStyle(DefaultStyle);
	}
}

void UCS3RichTextBlock::SetColorAndOpacity(FSlateColor InColorAndOpacity)
{
	ColorAndOpacity = InColorAndOpacity;
	DefaultStyle.SetColorAndOpacity(ColorAndOpacity);
	if (MyRichTextBlock.IsValid())
	{
		MyRichTextBlock->SetTextStyle(DefaultStyle);
	}
}

void UCS3RichTextBlock::SetShadowOffset(FVector2D InShadowOffset)
{
	ShadowOffset = InShadowOffset;
	DefaultStyle.SetShadowOffset(ShadowOffset);
	if (MyRichTextBlock.IsValid())
	{
		MyRichTextBlock->SetTextStyle(DefaultStyle);
	}
}

void UCS3RichTextBlock::SetShadowColorAndOpacity(FLinearColor InShadowColorAndOpacity)
{
	ShadowColorAndOpacity = InShadowColorAndOpacity;
	DefaultStyle.SetShadowColorAndOpacity(ShadowColorAndOpacity);
	if (MyRichTextBlock.IsValid())
	{
		MyRichTextBlock->SetTextStyle(DefaultStyle);
	}
}

#pragma endregion

void UCS3RichTextBlock::SetOpacity(float InOpacity)
{
	if (!MyRichTextBlock.IsValid())
	{
		return;
	}
	FString TextString = Text.ToString();
	//是富文本
	if (TextString.Contains(TEXT("<span")))
	{
		//新富文本字符串
		FString NewTextString = TEXT("");
		//有color字段
		if (TextString.Contains(TEXT("color=\"#")))
		{
			FString Left, Right;
			bool Result = TextString.Split("color=\"#", &Left, &Right, ESearchCase::Type::CaseSensitive);
			if (!Result) return;

			//A
			FColor Color(255, 255, 255, InOpacity * 255);
			FString TempOpacityStr = UKismetStringLibrary::GetSubstring(Color.ToHex(), 6, 2);
			//color，如color="#FFFFFFFF
			FString ColorAndOpacityStr = TEXT("color=\"#") + UKismetStringLibrary::GetSubstring(Right, 0, 6) + TempOpacityStr;

			//color="#FFFFFFFF后面的字符串
			FString NewRight = UKismetStringLibrary::GetSubstring(Right, 8, Right.Len() - 8);
			//新富文本字符串
			NewTextString = Left + ColorAndOpacityStr + NewRight;
			
		}
		else
		{
			FString Left, Right;
			bool Result = TextString.Split("<span", &Left, &Right, ESearchCase::Type::CaseSensitive);
			if (!Result) return;

			//color，如color="#FFFFFFFF"
			FColor Color(ColorAndOpacity.GetSpecifiedColor().R, ColorAndOpacity.GetSpecifiedColor().G, ColorAndOpacity.GetSpecifiedColor().B, InOpacity * 255);
			FString ColorAndOpacityStr = TEXT(" color=\"#") + Color.ToHex() + TEXT("\"");

			//新富文本字符串
			NewTextString = Left + TEXT("<span") + ColorAndOpacityStr + Right;
		}

		//有ShadowColor字段
		if (NewTextString.Contains(TEXT("shadowColor=\"#")))
		{
			FString Left, Right;
			bool Result = NewTextString.Split("shadowColor=\"#", &Left, &Right, ESearchCase::Type::CaseSensitive);
			if (!Result) return;

			//A
			FColor Color(255, 255, 255, InOpacity * 255);
			FString TempOpacityStr = UKismetStringLibrary::GetSubstring(Color.ToHex(), 6, 2);
			//shadowColor，如shadowColor="#FFFFFFFF
			FString ShadowColorAndOpacityStr = TEXT("shadowColor=\"#") + UKismetStringLibrary::GetSubstring(Right, 0, 6) + TempOpacityStr;

			//shadowColor="#FFFFFFFF后面的字符串
			FString NewRight = UKismetStringLibrary::GetSubstring(Right, 8, Right.Len() - 8);
			//新富文本字符串
			NewTextString = Left + ShadowColorAndOpacityStr + NewRight;

		}
		//没有ShadowColor字段，但有shadowOffset字段，说明有阴影且颜色使用的ShadowColorAndOpacity
		else if (NewTextString.Contains(TEXT("shadowOffset=\"#")))
		{
			FString Left, Right;
			bool Result = NewTextString.Split("<span", &Left, &Right, ESearchCase::Type::CaseSensitive);
			if (!Result) return;

			//shadowColor，如shadowColor="#FFFFFFFF"
			FColor Color(ShadowColorAndOpacity.R, ShadowColorAndOpacity.G, ShadowColorAndOpacity.B, InOpacity * 255);
			FString ShadowColorAndOpacityStr = TEXT(" shadowColor=\"#") + Color.ToHex() + TEXT("\"");

			//新富文本字符串
			NewTextString = Left + TEXT("<span") + ShadowColorAndOpacityStr + Right;
		}
		if (MyRichTextBlock.IsValid())
		{
			MyRichTextBlock->SetText(FSTRING_TO_FTEXT(NewTextString));
		}
	}
	else
	{
		FLinearColor CurrentColor = ColorAndOpacity.GetSpecifiedColor();
		CurrentColor.A = InOpacity;
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("Tick-----SetOpacity:CurrOpacity[%f]"), CurrentColor.A);
		SetColorAndOpacity(FSlateColor(CurrentColor));
	}
}

void UCS3RichTextBlock::SetWrapTextAt(float InWrapTextAt)
{
	WrapTextAt = InWrapTextAt;
	if (MyRichTextBlock.IsValid())
	{
		MyRichTextBlock->SetWrapTextAt(WrapTextAt);
	}
}

void UCS3RichTextBlock::SetAutoWrapText(bool InAutoWrapText)
{
	AutoWrapText = InAutoWrapText;
	if (MyRichTextBlock.IsValid())
	{
		MyRichTextBlock->SetAutoWrapText(InAutoWrapText);
	}
}

FText UCS3RichTextBlock::ReplaceSpecialValue(FText InText)
{
	FString value = InText.ToString();
	//这里标签与HorizonUI不一致，将HorizonUI格式的标签替换为RichTextBlock格式
	value.ReplaceInline(TEXT("<text"), TEXT("<span"), ESearchCase::CaseSensitive);
	value.ReplaceInline(TEXT("</text>"), TEXT("</>"), ESearchCase::CaseSensitive);
	value.ReplaceInline(TEXT("filePath="), TEXT("src="), ESearchCase::CaseSensitive);
	value.ReplaceInline(TEXT("<br/>"), TEXT("\r\n"), ESearchCase::CaseSensitive);
	value.ReplaceInline(TEXT("fontPath="), TEXT("font="), ESearchCase::CaseSensitive);
	value.ReplaceInline(TEXT("fontType="), TEXT("style="), ESearchCase::CaseSensitive);
	value.ReplaceInline(TEXT("fontSize="), TEXT("size="), ESearchCase::CaseSensitive);
	//特殊字符
	value.ReplaceInline(TEXT("&nbsp;"), TEXT(" "), ESearchCase::CaseSensitive);
	value.ReplaceInline(TEXT("&quot;"), TEXT("\""), ESearchCase::CaseSensitive);
	value.ReplaceInline(TEXT("&amp;"), TEXT("&"), ESearchCase::CaseSensitive);
	value.ReplaceInline(TEXT("&apos;"), TEXT("'"), ESearchCase::CaseSensitive);
	value.ReplaceInline(TEXT("&lt;"), TEXT("<"), ESearchCase::CaseSensitive);
	value.ReplaceInline(TEXT("&gt;"), TEXT(">"), ESearchCase::CaseSensitive);
	return UKismetTextLibrary::Conv_StringToText(value);
}

#pragma region	/** 文本淡入淡出 */
void UCS3RichTextBlock::SetIsFadeText(bool bIsFade)
{
	bIsFadeText = bIsFade;
}

void UCS3RichTextBlock::SetIsStartTickFadeText(bool bIsStartTickFade)
{
	bIsStartTickFadeText = bIsStartTickFade;
	if (bIsStartTickFadeText) {
		ResetFadeText();
	}
}

void UCS3RichTextBlock::SetFadeSpeed(float InFadeSpeed)
{
	FadeSpeed = InFadeSpeed;
}

void UCS3RichTextBlock::SetFadeInterval(float InFadeInterval)
{
	FadeInterval = InFadeInterval;
}

void UCS3RichTextBlock::ResetFadeText()
{
	FadeDeltaTime = 0.0f;
	TextFadeTimer = FadeInterval;
	bIsFadeIn = true;
	SetOpacity(0.0f);
}

void UCS3RichTextBlock::RebuildFadeText()
{
	if (bIsFadeText) {
		SetIsStartTickFadeText(true);
	}
	else {
		SetIsStartTickFadeText(false);
	}
}

void UCS3RichTextBlock::StopFade()
{
	//reset
	ResetFadeText();
	//stop tick
	SetIsStartTickFadeText(false);
}

void UCS3RichTextBlock::StartFade()
{
	SetIsStartTickFadeText(true);
}

#pragma endregion

#undef LOCTEXT_NAMESPACE



