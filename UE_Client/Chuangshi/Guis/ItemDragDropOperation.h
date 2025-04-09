// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/DragDropOperation.h"
#include "GameData/UIDataDefine.h"
#include "GameData/CursorData.h"
#include "ItemDragDropOperation.generated.h"

/**
* 文件名称：ItemDragDropOperation.h
* 功能说明：道具、技能拖拽操作类
* 文件作者：zhangdan
* 目前维护：zhangdan
* 创建时间：2019-01-23
 */

UCLASS(Blueprintable)
class CHUANGSHI_API UItemDragDropOperation : public UDragDropOperation
{
	GENERATED_BODY()
	
public:
	///道具、技能拖拽数据
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Item Drag and Drop", meta = (ExposeOnSpawn = "true"))
	FDragDropOperationData DragDropData;
};
