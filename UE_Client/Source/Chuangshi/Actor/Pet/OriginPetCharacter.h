// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Actor/NPC/ClientGameCharacter.h"
#include "Entity/Alias.h"
#include "OriginPetCharacter.generated.h"

/**
* 文件名称：OriginPetCharacter.h
* 功能说明：
* 文件作者：chendongyong
* 创建时间：2020-02-7
*/
UCLASS()
class CHUANGSHI_API AOriginPetCharacter : public AClientGameCharacter
{
	GENERATED_BODY()

		
public:
	virtual void BeginPlay()override;

	void InitOriginPet(const ORIGIN_PET_CLIENT_SIMPLE_DATA& Data);

	virtual void CreateAppearance() override;
	virtual void OnCreateModelOver() override;
	virtual float GetMoveSpeed();
	virtual bool IsActiveMoveing();///是否主动移动中（不包括击飞相关的位移）

	void MoveLeaveBeforeDestroy();

public:
	UPROPERTY(BlueprintReadOnly)
		FString UID;
	UPROPERTY(BlueprintReadOnly)
		FString ScriptID;
	UPROPERTY(BlueprintReadOnly)
		FString ModelNumber;
	UPROPERTY(BlueprintReadOnly)
		float ModelScale;

	FTimerHandle MoveTimer;
private:
	void MoveChangeImp();
	void RandomMove();

private:
	int8 index;
	bool IsMoveDisAppear;	
	FVector TargetPos;
	float changeDelta;				// 半透明渐变
};
