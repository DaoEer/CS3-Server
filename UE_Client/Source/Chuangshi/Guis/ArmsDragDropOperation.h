// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/DragDropOperation.h"
#include "GameData/UIDataDefine.h"
#include "GameData/CursorData.h"
#include "ArmsDragDropOperation.generated.h"

/**
 * 
 */

UCLASS(Blueprintable)
class CHUANGSHI_API UArmsDragDropOperation : public UDragDropOperation
{
	GENERATED_BODY()

public:
	///Ê¿±ø¡¢ÍÏ×§Êý¾Ý
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Arms Drag and Drop", meta = (ExposeOnSpawn = "true"))
		FArmsDragDropOperationData ArmsDragDropData;
};
