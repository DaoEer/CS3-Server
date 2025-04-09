

#include "CS3Styles.h"
#include "SlateGameResources.h" 

TSharedPtr<FSlateStyleSet> FCS3Styles::CS3StyleInstance = NULL; 

void FCS3Styles::Initialize()
{
	if (!CS3StyleInstance.IsValid())
	{
		CS3StyleInstance = Create();
		FSlateStyleRegistry::RegisterSlateStyle(*CS3StyleInstance);
	}
}

void FCS3Styles::Shutdown()
{
	FSlateStyleRegistry::UnRegisterSlateStyle(*CS3StyleInstance);
	ensure(CS3StyleInstance.IsUnique()); 
	CS3StyleInstance.Reset();
}

FName FCS3Styles::GetStyleSetName()
{
	static FName StyleSetName(TEXT("CS3Styles"));
	return StyleSetName;
}
/** 
 * 创建资源路径
 **/
TSharedRef<FSlateStyleSet> FCS3Styles::Create()
{
	TSharedRef<FSlateStyleSet> StyleRef = FSlateGameResources::New(FCS3Styles::GetStyleSetName(), "/Game/BluePrints/UI/Styles", "/Game/BluePrints/UI/Styles");
	return StyleRef;
}

const ISlateStyle& FCS3Styles::Get()
{
	return *CS3StyleInstance;
}


