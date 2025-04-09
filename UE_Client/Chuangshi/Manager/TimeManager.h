#pragma once
#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "TimeManager.generated.h"

/*
* 文件名称：TimeManager.h
* 功能说明：时间管理器。
* 文件作者：xuyongqi
* 目前维护：xuyongqi
* 创建时间：2018-03-10
*/

#define		MYTICKTIME					30.0f						/*验证间隔*/
#define		TIME_ENLARGE_MULTIPLE		10000000					/*扩大时间倍数*/
#define		TIME_PERMISSIBLE_ERROR		(0.5 * TIME_ENLARGE_MULTIPLE)	/*允许误差*/

UCLASS(BlueprintType)
class CHUANGSHI_API UTimeManager : public UCS3Object
{
	GENERATED_BODY()
public:
	static UTimeManager* GetInstance();

	/**
	*获得客户端时间（扩大倍数）
	*返回FDateTime格式
	*/
	UFUNCTION(BlueprintPure, Category = "TimeManager")
	FDateTime GetClientTime();
	/**
	*获得扩大倍数的时间
	*/
	int64 GetMultipleClientTime();
	/**
	* 返回false说明此时客户端处于高延迟状态
	*/
	UFUNCTION(BlueprintCallable, Category = "TimeManager")
	bool ISTimeValid();

	/**
	*将服务器时间转化成客户端时间
	*返回FDateTime格式
	*/
	FDateTime ServerTimeToClientTime(const int64& severTime);

public:
	void SetDiffTime(const FString& serverTime, const int32& severIndex);
	void VerifyClientTime();
	void OnPlayerEnter();
	void OnPlayerLeave();

	UTimeManager();
	~UTimeManager();
private:
	FDateTime SetTimeToDateTime(const int64& MulTime);
	void SetIndex();
	bool IsValid = false;
	int64 DiffTime = 0;
	int32 Index = 0;
	FTimerHandle CycleHandle;
};

