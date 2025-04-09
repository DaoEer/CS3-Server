// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "Engine/StreamableManager.h"
#include "GameData/CS3Object.h"
#include "GameData/GameDeFine.h"
#include "ResourceManager.generated.h"



/*
* 文件名称：ResourceManager.h
* 功能说明：资源加载管理类
* 文件作者：hezhiming
* 目前维护：hezhiming
* 创建时间：2018-01-11
*/
DECLARE_DYNAMIC_DELEGATE_OneParam(FResourceLoaderDelegate, const TArray<UObject *> &, LoadedResourceArray);
DECLARE_DYNAMIC_DELEGATE_TwoParams(FResourceLoaderIconDelegate, const int32, itemid, const UObject*, iconObj );

UCLASS(BlueprintType)
class CHUANGSHI_API UResourceManager : public UCS3Object
{
	GENERATED_BODY()
public:
	UResourceManager();
	static UResourceManager* GetInstance();
	
#pragma region
	 /**
	 *异步加载多个资源
	 *
	 *@param TargetsToStream 资源
	 *@param DelegateToCall 回调
	 *@param RESOURCE_LOAD_PRIORITY_TYPE 加载类型
	 *@param FVector 位置
	 *@param bool 加载完以后是否streamable handle激活直到手动释放
	 *
	 *@return TSharedPtr<FStreamableHandle>
	 */
	TSharedPtr<FStreamableHandle> RequestAsyncLoad(const void * UserObject, const TArray<FStringAssetReference>& TargetsToStream, FStreamableDelegate DelegateToCall, RESOURCE_LOAD_PRIORITY_TYPE type = RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_DEFAULT, FVector Position = FVector::ZeroVector, bool bManageActiveHandle = false);

	UFUNCTION(BlueprintCallable, Category = "Global|RequestAsyncLoad")
		void RequestAsyncLoad(const UObject* UserObject, const TArray<TSoftObjectPtr<UObject>>& TargetsToStream, FResourceLoaderDelegate DelegateToCall, RESOURCE_LOAD_PRIORITY_TYPE type = RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_DEFAULT, FVector Position = FVector::ZeroVector, bool bManageActiveHandle = false);

	UFUNCTION(BlueprintCallable, Category = "Global|RequestAsyncItemIconLoad")
		void RequestAsyncItemIconLoad(const UObject* UserObject, const TSoftObjectPtr<UObject>& TargetToStream, FResourceLoaderIconDelegate DelegateToCall, int32 itemid, RESOURCE_LOAD_PRIORITY_TYPE type = RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_DEFAULT, FVector Position = FVector::ZeroVector, bool bManageActiveHandle = false);


	//只用来后台加载永远不会释放的核心资源(优先级最低)
	UFUNCTION(BlueprintCallable, Category = "Global|RequestAsyncLoad")
		void BackstageAsyncLoad_ObjectPath(const FSoftObjectPath& TargetToStream);

	//只用来后台加载永远不会释放的核心资源(优先级最低)
	UFUNCTION(BlueprintCallable, Category = "Global|RequestAsyncLoad")
		void BackstageAsyncLoad_ClassPtr(const TSoftClassPtr<UObject>& TargetToStream);

	//只用来后台加载永远不会释放的核心资源(优先级最低)
	UFUNCTION(BlueprintCallable, Category = "Global|RequestAsyncLoad")
		void BackstageAsyncLoad_ObjectPtr(const TSoftObjectPtr<UObject>& TargetToStream);
	
	 /**
	 *异步加载单个资源
	 *
	 *@param TargetToStream 资源
	 *@param DelegateToCall 回调
	 *@param RESOURCE_LOAD_PRIORITY_TYPE 加载类型
	 *@param FVector 位置
	 *@param bool 加载完以后是否streamable handle激活直到手动释放
	 *
	 *@return TSharedPtr<FStreamableHandle>
	 */
	TSharedPtr<FStreamableHandle> RequestAsyncLoad(const void * UserObject, const FStringAssetReference& TargetToStream, FStreamableDelegate DelegateToCall, RESOURCE_LOAD_PRIORITY_TYPE type = RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_DEFAULT, FVector Position = FVector::ZeroVector, bool bManageActiveHandle = false);
	

	 /**
	 *异步加载多个资源
	 *
	 *@param TargetsToStream 资源
	 *@param DelegateToCall 回调
	 *@param RESOURCE_LOAD_PRIORITY_TYPE 加载类型
	 *@param FVector 位置
	 *@param bool 加载完以后是否streamable handle激活直到手动释放
	 *
	 *@return TSharedPtr<FStreamableHandle>
	 */
	TSharedPtr<FStreamableHandle> RequestAsyncLoad(const void * UserObject, const TArray<FStringAssetReference>& TargetsToStream, TFunction<void()>&& Callback, RESOURCE_LOAD_PRIORITY_TYPE type = RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_DEFAULT, FVector Position = FVector::ZeroVector, bool bManageActiveHandle = false);

	 /**
	 *异步加载单个资源
	 *
	 *@param TargetToStream 资源
	 *@param DelegateToCall 回调
	 *@param RESOURCE_LOAD_PRIORITY_TYPE 加载类型
	 *@param FVector 位置
	 *@param bool 加载完以后是否streamable handle激活直到手动释放
	 *
	 *@return TSharedPtr<FStreamableHandle>
	 */
	TSharedPtr<FStreamableHandle> RequestAsyncLoad(const void * UserObject, const FStringAssetReference& TargetToStream, TFunction<void()>&& Callback, RESOURCE_LOAD_PRIORITY_TYPE type = RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_DEFAULT, FVector Position = FVector::ZeroVector, bool bManageActiveHandle = false);

	 /**
	 *异步加载多个资源
	 *
	 *@param TargetsToStream 资源
	 *@param DelegateToCall 回调
	 *@param Priority 加载优先级
	 *@param bool 加载完以后是否streamable handle激活直到手动释放
	 *
	 *@return TSharedPtr<FStreamableHandle>
	 */
	TSharedPtr<FStreamableHandle> RequestAsyncLoad(const void * UserObject, const TArray<FStringAssetReference>& TargetsToStream, FStreamableDelegate DelegateToCall, TAsyncLoadPriority Priority = 0, bool bManageActiveHandle = false);

	/**
	*异步加载单个资源
	*
	*@param TargetToStream 资源
	*@param DelegateToCall 回调
	*@param Priority 加载优先级
	*@param bool 加载完以后是否streamable handle激活直到手动释放
	*
	*@return TSharedPtr<FStreamableHandle>
	*/
	TSharedPtr<FStreamableHandle> RequestAsyncLoad(const void * UserObject, const FStringAssetReference& TargetToStream, FStreamableDelegate DelegateToCall, TAsyncLoadPriority Priority = 0, bool bManageActiveHandle = false);

	/**
	*异步加载多个资源
	*
	*@param TargetsToStream 资源
	*@param DelegateToCall 回调
	*@param Priority 加载优先级
	*@param bool 加载完以后是否streamable handle激活直到手动释放
	*
	*@return TSharedPtr<FStreamableHandle>
	*/
	TSharedPtr<FStreamableHandle> RequestAsyncLoad(const void * UserObject, const TArray<FStringAssetReference>& TargetsToStream, TFunction<void()>&& Callback, TAsyncLoadPriority Priority = 0, bool bManageActiveHandle = false);

	/**
	*异步加载单个资源
	*
	*@param TargetToStream 资源
	*@param DelegateToCall 回调
	*@param Priority 加载优先级
	*@param bool 加载完以后是否streamable handle激活直到手动释放
	*
	*@return TSharedPtr<FStreamableHandle>
	*/
	TSharedPtr<FStreamableHandle> RequestAsyncLoad(const void * UserObject, const FStringAssetReference& TargetToStream, TFunction<void()>&& Callback, TAsyncLoadPriority Priority = 0, bool bManageActiveHandle = false);

	UObject* SynchronousLoad(const FStringAssetReference& TargetToStream, bool bManageActiveHandle = false);

	UFUNCTION(BlueprintPure, Category = "Global|SynchronousLoad")
	UObject* SynchronousLoad(const TSoftObjectPtr<UObject>& TargetToStream, bool bManageActiveHandle = false);

	UFUNCTION(BlueprintPure, Category = "Global|SynchronousLoad")
	UClass* SynchronousLoadClass(const TSoftClassPtr<UObject>& TargetToStream, bool bManageActiveHandle = false);

	TAsyncLoadPriority GetAsyncLoadPriority(RESOURCE_LOAD_PRIORITY_TYPE type, FVector Position);

	void ReleaseManageActiveHandles();

	void ReleaseHandlesByObject(const void * UserObject);

	void ReleaseAllHandles();

	void AddResourceHandles(const void * UserObject, TSharedPtr<FStreamableHandle> StreamableHandle, bool bManageActiveHandle = false);
	
	/**
	*查找加载失败的资源路径（注:此方法只作为调试用，不用时请屏蔽，因为有加载，所以消耗比较久）
	*@param LoadPartArray 要查找的资源路径数组
	* 
	*@return 无  
	*/
	void FindLoadFaileAssetPathToLog(TArray<FStringAssetReference> LoadPartArray);

	void CheckMultipleAssetFileIsExist(TArray<FStringAssetReference> LoadPartArray, int32 EntityID, FString ModelID);

	bool CheckAssetFileIsExist(const FStringAssetReference& TargetToStream);


#pragma endregion
private:
	FStreamableManager StreamManager;///<资源流管理器
	TMap<RESOURCE_LOAD_PRIORITY_TYPE, TArray<int32>> ResourceLoadPriority;
	TArray<TSharedPtr<FStreamableHandle>> ManagedActiveStreamableHandles;
	TMap<const void *, TSet<TWeakPtr<FStreamableHandle>>> AllStreamableHandles;
	//static UAssetManager* Instance;
};