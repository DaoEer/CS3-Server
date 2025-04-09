#pragma once
#include "Engine/Texture2D.h"
#include "SlateWidgetStyleContainerBase.h" 
#include "SlateBrush.h"
#include "AnimatedTexture2D.h"
#include "CS3GlobalStyle.generated.h" 

/*
* 文件名称：CS3GlobalStyle.h
* 功能说明：
* 文件作者：huangshanquan
* 目前维护：huangshanquan
* 创建时间：2017-12-05
*/

/** 富文本图片配置 */
USTRUCT(BlueprintType) 
struct FRichTextImage
{
	GENERATED_USTRUCT_BODY()

public:
	/** 图片 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		UTexture2D* Image;
};

/** 富文本gif图片配置 */
USTRUCT(BlueprintType)
struct FRichTextAnimatedImage
{
	GENERATED_USTRUCT_BODY()

public:
	/** 图片 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		UAnimatedTexture2D* Image;
};

/** 
 * FGlobalCS3Style
 * 创世全局画刷样式配置
 * const FSlateFontInfo &Font = (&FCS3Styles::Get().GetWidgetStyle<FGlobalCS3Style>("CS3SlateWidgetStyleAsset"))->HyperlinkToolTipFont;
 * 获取指定资源HyperlinkToolTipFont,CS3SlateWidgetStyleAsset是蓝图继承类
 */
USTRUCT(BlueprintType)
struct FGlobalCS3Style : public FSlateWidgetStyle
{
	GENERATED_USTRUCT_BODY()

	virtual void GetResources(TArray<const FSlateBrush*>& OutBrushes) const override;

	static const FName TypeName;

	virtual const FName GetTypeName() const override;

	static const FGlobalCS3Style& GetDefault(); 

	/** 富文本图片配置 */
	UPROPERTY(EditAnywhere, Category = Appearance)
	TMap<FName, FRichTextImage> RichTextImageMap;

	/** 富文本gif图片配置 */
	UPROPERTY(EditAnywhere, Category = Appearance)
		TMap<FName, FRichTextAnimatedImage> RichTextAnimatedImageMap;

	/** 富文本连接按键样式配置 */
	UPROPERTY(EditAnywhere, Category = Appearance)
	FButtonStyle HyperlinkButtonStyle;

	/** 是否显示超连接提示框 */
	UPROPERTY(EditAnywhere, Category = Appearance)
	bool IsShowHyperlinkToolTip;

    /** 超连接提示框字体 */
	UPROPERTY(EditAnywhere, Category = Appearance)
	FSlateFontInfo HyperlinkToolTipFont;

    /** 废弃,默认的话使用系统自定义的。 默认超连接提示框背景画刷 */
	UPROPERTY(EditAnywhere, Category = Appearance)
	FSlateBrush HyperlinkToolTipBrush;

    /** 超连接提示框背景画刷 */
	UPROPERTY(EditAnywhere, Category = Appearance)
	TMap<FName, FButtonStyle> HyperlinkButtonStyleMap;
};

/** 
 * 创世全局画刷样式配置资源类
 */
UCLASS(hidecategories = Object, MinimalAPI)
class UCS3Style : public USlateWidgetStyleContainerBase
{
	GENERATED_UCLASS_BODY()

public:

	UPROPERTY(EditAnywhere, Category = Appearance, meta = (ShowOnlyInnerProperties))
	FGlobalCS3Style CS3Style;

	virtual const struct FSlateWidgetStyle* const GetStyle() const override
	{
		return static_cast<const struct FSlateWidgetStyle*>(&CS3Style);
	}

};
