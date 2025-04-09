// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
//UE4
#include "GameFramework/Character.h"
#include "Animation/AnimInstance.h"
#include "Animation/AnimationAsset.h"
//CS3
#include "GameData/CS3Object.h"
#include "CharacterRideManager.generated.h"

/*
* 文件名称：CharacterRideManager.h
* 功能说明：
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2017-11-29
*/

UCLASS(BlueprintType)
class CHUANGSHI_API UCharacterRideManager : public UCS3Object
{
	GENERATED_BODY()
private:
	UCharacterRideManager();
	~UCharacterRideManager();
	
public:
	static UCharacterRideManager* GetInstance();
	//ride cache
	void LoadRideAsset(FString InPetId);
	void CacheRideAsset(FString AssetPath, UObject* AssetObject);
	void ClearCacheData();

private:

public:
	UPROPERTY(BlueprintReadOnly, Category = "GameCharacter")
		TMap<FString, UObject*> CacheRideAssetDatas;///<缓存资源数据
private:

};
