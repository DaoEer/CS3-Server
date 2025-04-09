// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Interface/Monster/MonsterInterface.h"
#include "MonsterOptimizeInterface.generated.h"

/**
 * 
 */
UCLASS()
class CHUANGSHI_API UMonsterOptimizeInterface : public UMonsterInterface
{
	GENERATED_BODY()
	CS3_DECLARE_INTERFACE_MAP()
	typedef UMonsterInterface Supper;
public:
	UMonsterOptimizeInterface();
	~UMonsterOptimizeInterface();
	static FString GetName() { return TEXT("GameObjectInterface"); } //获取接口名字
	static FString GetClassPath() { return TEXT("Class'/Script/Chuangshi.MonsterOptimizeInterface'"); } //获取蓝图对象路径

	void Set_Position(const FVector &oldVal);
	void OnMoveOver(const uint32 movingID, const bool isSuccess);

	void movingToPointReady(const uint64& movingID, const FVector& targetPos, const float& pointMaxDis );

	void Set_clientMovingID(const uint64& newVal, const uint64& oldVal);
	void Set_clientMovingPathPoints(const  KBEngine::FVariantArray& newVal, const  KBEngine::FVariantArray& oldVal);
	void Set_clientMovingPathIdx(const uint8& newVal, const uint8& oldVal);
	void Set_clientMovingToEntityID(const int32& newVal, const int32& oldVal);
	void Set_clientMovingToEntityDis(const float& newVal, const float& oldVal);
	void Set_moveScriptID(const uint16& newVal, const uint16& oldVal);
	void Set_useRVOAvoidance(const uint8& newVal, const uint8& oldVal);
	void Set_rvoRadius(const float& newVal, const float& oldVal);

	TArray<FVector> clientMovingPathPoints;

private:
	uint64 clientMovingID;
	uint16 moveScriptID;
	uint8 clientMovingPathIdx;
	int32 movingToEntityID;
	bool clientMovingTempUp;
	float movingToEntityDistance;
	FTimerHandle movingToEntityHandle;

	void moveToPathPoints();
	void moveToPathStep();
	void moveToPathStepOver();
	void moveToPathPointsOver();
	void moveToPathTick();
	FTimerHandle moveToPathHandle;

	void movingToEntityStart();
	void movingToEntityTick();

public:
	int32 MovingToEntityID() { return movingToEntityID; }
};
