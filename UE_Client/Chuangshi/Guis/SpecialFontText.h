// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Components/HorizontalBox.h"
#include "Engine/DataTable.h"
#include "Engine/StreamableManager.h"
#include "Util/CS3Debug.h"
#include "SpecialFontText.generated.h"

/*
* 文件名称：.SpecialFontText
* 功能说明：美术字特殊字体文本
* 文件作者：liyuxia
* 目前维护：liyuxia
* 创建时间：2018-8-2
*/

UCLASS()
class CHUANGSHI_API USpecialFontText : public UHorizontalBox
{
	GENERATED_UCLASS_BODY()
	
public:
	///<特殊字体表格配置路径
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Appearance)
	TSoftObjectPtr<UDataTable> FontDataTable;
	///<bVolatile为True代表这个数字经常变动（经常变动的数字需要预加载资源贴图减少调用的时候时间消耗）
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = Appearance)
	bool bVolatile;
	UPROPERTY(EditAnywhere, Category = Content)
	FString TextContent;

private:
	UPROPERTY()
	UDataTable* FontTable;
	FStreamableManager	StreamableManager;
	

public:
	UFUNCTION(BlueprintCallable, Category = "SpecialFontText")
		void SetText(FString InString);
	//~ Begin UWidget Interface
	virtual void SynchronizeProperties() override;

private:
	///<预加载特殊字体配置表的图片资源
	void PreLoadFontConfig();
	///<获得数字图片
	UTexture2D* GetDigitTexture(FString Digit);
	///<设置所有孩子控件可见性
	UFUNCTION(BlueprintCallable, Category = "Widget")
		 void SetAllChildVisibility(ESlateVisibility InVisibility);

	template < class T = FCSV_TABLE_ROW_BASE> const T* GetRow(UDataTable* Table, FName RowName) const
	{
		uint8* tempRowData = Table->FindRowUnchecked(RowName);
		if (tempRowData == nullptr)
		{
			CS3_Warning(TEXT("-->Null Pointer error:SetAllChildVisibility : tempRowData!"));
			return nullptr;
		}
		T* RowTable = (T*)tempRowData;
		if (RowTable != nullptr)
		{
			RowTable->RowName = RowName;
		}
		else
		{
			//CS3_Display(CS3DebugType::CL_Undefined, TEXT("config ：%s\t%s\t is invalid"), *Table->GetName(), *RowName);
		}

		return RowTable;
	}
};
