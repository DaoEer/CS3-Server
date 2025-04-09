// Fill out your copyright notice in the Description page of Project Settings.


#include "SpecialFontText.h"
#include "GameData/TexturePath.h"
#include "Image.h"
#include "Util/CS3Debug.h"

CONTROL_COMPILE_OPTIMIZE_START

USpecialFontText::USpecialFontText(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
}

void USpecialFontText::SynchronizeProperties()
{
	Super::SynchronizeProperties();
	FontTable = LoadObject<UDataTable>(nullptr, *FontDataTable.ToString());
	if (bVolatile)
	{
		PreLoadFontConfig();
	}
	SetText(TextContent);
}

void USpecialFontText::SetText(FString InString)
{
	TextContent = InString;
	SetAllChildVisibility(ESlateVisibility::Collapsed);///<收缩孩子控件
	for (int32 i = 0; i < InString.Len(); i++)
	{
		UTexture2D* tempDigitTexture = GetDigitTexture(InString.Mid(i, 1));
		if (!IsValid(tempDigitTexture))
		{
			CS3_Warning(TEXT("-->Null Pointer error:USpecialFontText::SetText : tempDigitTexture!"));
			continue;
		}
		if ( i < GetChildrenCount() )
		{
			UWidget* tempChild = GetChildAt(i);
			tempChild->SetVisibility(ESlateVisibility::SelfHitTestInvisible);
			UImage* tempImage = Cast<UImage>(tempChild);
			if (IsValid(tempImage))
			{
				tempImage->SetBrushFromTexture(tempDigitTexture, true);
			}
		}
		else
		{
			UImage* tempImage = NewObject<UImage>();
			tempImage->SetBrushFromTexture(tempDigitTexture, true);
			AddChildToHorizontalBox(tempImage);
		}
	}
	
}

void USpecialFontText::PreLoadFontConfig()
{
	if (IsValid(FontTable))
	{
		TArray<FName> tempRowNames = FontTable->GetRowNames();
		for (auto& row : tempRowNames)
		{
			const FCS3TexturePath* textuerstruct = GetRow<FCS3TexturePath>(FontTable, row);
			if (textuerstruct)
			{
				StreamableManager.LoadSynchronous(textuerstruct->TexturePath.ToSoftObjectPath(), true);
			}
		}
	}
}

UTexture2D* USpecialFontText::GetDigitTexture(FString Digit)
{
	if (IsValid(FontTable))
	{
		TArray<FName> tempRowNames = FontTable->GetRowNames();
		if ( !tempRowNames.Contains(FName(*Digit)) )
		{
			CS3_Warning(TEXT("----------表格没有这一行数据----------"));
			return nullptr;
		}
		const FCS3TexturePath* textuerstruct = GetRow<FCS3TexturePath>(FontTable, FName(*Digit));
		if (textuerstruct)
		{
			if (IsValid(textuerstruct->TexturePath.Get()))
			{
				return textuerstruct->TexturePath.Get();
			}

			if (textuerstruct->TexturePath.ToSoftObjectPath().IsValid())
			{
				StreamableManager.LoadSynchronous(textuerstruct->TexturePath.ToSoftObjectPath());
				return textuerstruct->TexturePath.Get();
			}
		}
	}
	return nullptr;
}

void USpecialFontText::SetAllChildVisibility(ESlateVisibility InVisibility)
{
	for (auto It : GetSlots() )
	{
		It->Content->SetVisibility(InVisibility);
	}
}

CONTROL_COMPILE_OPTIMIZE_END