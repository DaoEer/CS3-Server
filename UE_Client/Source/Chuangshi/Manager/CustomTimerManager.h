// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameData/CS3Object.h"
#include "TimerManager.h"
#include "CustomTimerManager.generated.h"

/*
* 文件名称：CustomTimerManager.h
* 功能说明：定时器管理器
* 文件作者：zhangfudong
* 目前维护：zhangfudong
* 创建时间：2018-10-18
*/

USTRUCT()
struct FTimerStruct
{
	GENERATED_USTRUCT_BODY()

	FTimerHandle Handle;
	void* Object;

	FTimerStruct(){}

	FTimerStruct(FTimerHandle Handle, void* Object)
	{
		this->Handle = Handle;
		this->Object = Object;
	}
};

UCLASS(BlueprintType)
class CHUANGSHI_API UCustomTimerManager : public UCS3Object
{
	GENERATED_BODY()
	
public:
	
	UCustomTimerManager() {}
	~UCustomTimerManager() {}

	/// 获取管理类实例
	static UCustomTimerManager* GetInstance();

	template< class UserClass >
	void SetTimer(FTimerHandle& InOutHandle, UserClass* InObj, typename FTimerDelegate::TUObjectMethodDelegate< UserClass >::FMethodPtr InTimerMethod, float InRate, bool InbLoop = false, float InFirstDelay = -1.f)
	{
		GetTimerManager().SetTimer(InOutHandle, InObj, InTimerMethod, InRate, InbLoop, InFirstDelay);	
		AddAllItemsToMap(InObj, InOutHandle);
	}

	template< class UserClass >
	void SetTimer(FTimerHandle& InOutHandle, UserClass* InObj, typename FTimerDelegate::TUObjectMethodDelegate_Const< UserClass >::FMethodPtr InTimerMethod, float InRate, bool InbLoop = false, float InFirstDelay = -1.f)
	{
		GetTimerManager().SetTimer(InOutHandle, InObj, InTimerMethod, InRate, InbLoop, InFirstDelay);
		AddAllItemsToMap(InObj, InOutHandle);
	}
	
	/** Version that takes any generic delegate. */
	template< class UserClass >
	void SetTimer(UserClass* InObj, FTimerHandle& InOutHandle, FTimerDelegate const& InDelegate, float InRate, bool InbLoop, float InFirstDelay = -1.f)
	{
		GetTimerManager().SetTimer(InOutHandle, InDelegate, InRate, InbLoop, InFirstDelay);
		AddAllItemsToMap(InObj, InOutHandle);
	}
	/** Version that takes a dynamic delegate (e.g. for UFunctions). */
	template< class UserClass >
	void SetTimer(UserClass* InObj, FTimerHandle& InOutHandle, FTimerDynamicDelegate const& InDynDelegate, float InRate, bool InbLoop, float InFirstDelay = -1.f)
	{
		GetTimerManager().SetTimer(InOutHandle, InDynDelegate, InRate, InbLoop, InFirstDelay);
		AddAllItemsToMap(InObj, InOutHandle);
	}

	///将所有的类型的TimerHandle加入到Map中
	template< class UserClass >
	void AddAllItemsToMap(UserClass* InObj, FTimerHandle& InOutHandle)
	{
		FTimerStruct Timer(InOutHandle, (void*)(InObj));
		AddToMap(Timer, (void*)(InObj));
	}
	/**
	* Clears a previously set timer, identical to calling SetTimer() with a <= 0.f rate.
	* Invalidates the timer handle as it should no longer be used.
	*
	* @param InHandle The handle of the timer to clear.
	*/
	void ClearTimer(FTimerHandle& InHandle);

	/** Clears all timers that are bound to functions on the given object. */
	void ClearAllTimersForObject(void const* Object);

	/**
	* Pauses a previously set timer.
	*
	* @param InHandle The handle of the timer to pause.
	*/
	void PauseTimer(FTimerHandle InHandle);

	/**
	* Unpauses a previously set timer
	*
	* @param InHandle The handle of the timer to unpause.
	*/
	void UnPauseTimer(FTimerHandle InHandle);
	
	/**
	* Returns true if the specified timer exists and is not paused
	*
	* @param InHandle The handle of the timer to check for being active.
	* @return true if the timer exists and is active, false otherwise.
	*/
	bool IsTimerActive(FTimerHandle InHandle) const;
	
	/**
	* Returns true if the specified timer exists and is paused
	*
	* @param InHandle The handle of the timer to check for being paused.
	* @return true if the timer exists and is paused, false otherwise.
	*/
	bool IsTimerPaused(FTimerHandle InHandle);
	
	/**
	* Returns true if the specified timer exists and is pending
	*
	* @param InHandle The handle of the timer to check for being pending.
	* @return true if the timer exists and is pending, false otherwise.
	*/
	bool IsTimerPending(FTimerHandle InHandle);

	/**
	* Returns true if the specified timer exists
	*
	* @param InHandle The handle of the timer to check for existence.
	* @return true if the timer exists, false otherwise.
	*/
	bool TimerExists(FTimerHandle InHandle);
	
	/**
	* Gets the time remaining before the specified timer is called
	*
	* @param InHandle The handle of the timer to check the remaining time of.
	* @return	 The current time remaining, or -1.f if timer does not exist
	*/
	float GetTimerRemaining(FTimerHandle InHandle) const;
	
	UFUNCTION(BlueprintCallable, Category = "Timer")
	int32 GetTimerNumberByClassName(const FString& InClassName);

	UFUNCTION(BlueprintCallable, Category = "Timer")
	TMap<FString, int32> GetTimerMap();

	UFUNCTION(BlueprintCallable, Category = "Timer")
	void ClearAllTimer();

	//添加UObject或者Entity到表
	void AddToMap(FTimerStruct& Timer, void* InObj);
	
private:
	///添加元素到Map中
	void AddItemToMap(const FString& ClassName, FTimerStruct& Timer);

	///刷新Map中的元素
	void UpdateMap();

	///获取引擎的Timer管理器
	FTimerManager& GetTimerManager() const;

private:
	
	TMap <FString, TArray<FTimerStruct>> TimerMap;
	
};

//#define SetTimer(x,y,z,w)			SetTimer((x),this,(y),(z),(w))
//#define SetTimer(x,y,z,w,v)			SetTimer((x),(y),(z),(w),(v))
