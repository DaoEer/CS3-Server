// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "GameData/ModifyFaceData.h"
#include "GameData/CharacterData.h"
#include "ModifyfaceSaveActor.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API UModifyfaceSaveActor : public USaveGame
{
	GENERATED_BODY()
public:

	UPROPERTY(BlueprintReadWrite, Category = "GameCharacter")
		FFACE_STYLE_DATA FaceStyleDatas;///脸部样式数据

	UPROPERTY(BlueprintReadOnly, Category = "GameCharacter")
		TArray<FMODIFY_FACE_DATA> ModifyFaceDatas;///<模型捏脸数据

	TMap<MODEL_PART_TYPE, FString> partMesh;


	UModifyfaceSaveActor();
};
