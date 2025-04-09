// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Image.h"
#include "GameData/CursorData.h"
#include "Blueprint/UserWidget.h"
#include "CS3Base/CS3UserWidget.h"
#include "CursorUIWidget.generated.h"

/*
* 文件名称：CursorUIWidget.h
* 功能说明：
* 文件作者：yanghan
* 目前维护：wuxiaoou
* 创建时间：2017-08-30
*/

/**
 * 
 */
UCLASS(BlueprintType)
class CHUANGSHI_API UCursorUIWidget : public UCS3UserWidget
{
	GENERATED_BODY()
	
public:
	/**
	*获取鼠标用的Image
	*
	*@param CursorState 鼠标状态
	*
	*@return 鼠标用Image
	*/
	void SetCursorTexture(FString CursorState);
	
	/**
	*更新鼠标图标
	*
	*@param CursorState 鼠标状态
	*
	*@return 鼠标用Image
	*/
	UFUNCTION(BlueprintCallable, Category = "CursorUIWidget")
	void UpdataImage(UObject* Texture, FVector2D TextureSize);

public:
	UPROPERTY(meta = (BindWidget))
		UImage* CursorImage;
};
