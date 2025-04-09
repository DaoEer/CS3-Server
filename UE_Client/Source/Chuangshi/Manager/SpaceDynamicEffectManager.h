#pragma once
// Fill out your copyright notice in the Description page of Project Settings.
#include "CoreMinimal.h"
#include "GameData/SpaceDynamicEffectData.h"
#include "GameData/CS3Object.h"
#include "SpaceDynamicEffectManager.generated.h"

/*
* 文件名称：SpaceDynamicEffectManager.h
* 功能说明：
* 文件作者：huting
* 目前维护：huting
* 创建时间：2017-08-16
*/

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FCreateEntityOverDelegate, UBaseEffect*, Effect);
/**
*效果基类
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UBaseEffect : public UCS3Object
{
	GENERATED_BODY()

public:
	UBaseEffect() {}
	virtual void InitData(const FSPACEDYNAMICEFFECT_DATA* dictData) {};
	virtual void StartEffect(const FSPACEDYNAMICEFFECT_DATA* dictData);///<效果开启
	virtual void DestroyEffect() {}///<直接销毁
	virtual void StopEffect() {}///<效果销毁（会淡出处理）
};

/**
*天气效果
*/
UCLASS(BlueprintType)
class CHUANGSHI_API USkyEffect : public UBaseEffect
{
	GENERATED_BODY()
		typedef UBaseEffect Supper;
public:
	USkyEffect() {}
	virtual void InitData(const FSPACEDYNAMICEFFECT_DATA* dictData)override;
	virtual void StartEffect(const FSPACEDYNAMICEFFECT_DATA* dictData)override;///<效果开启
	virtual void DestroyEffect()override; ///<直接销毁
	virtual void StopEffect() override; ///<效果销毁（会淡出处理）
private:
	void OnTriggerDynamicEnvironmentEvent(FString BoxEnvironmentName,float BoxEffectStartTime);///<动态改变环境事件
	void OnTriggerSkyMaterialEvent(FString MaterialName, float MaterialEffectStartTime);
	void OnBackDynamicEnvironmentEvent();
private:
	ESKYEFFECTENUM EffectType= ESKYEFFECTENUM::None;
	FString EffectName;
	float EffectStartTime = -1;///<配置表中默认数据
};

/**
*创建纯客户端entity效果，应用于桥、门
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UCreateEntityEffect : public UBaseEffect
{
	GENERATED_BODY()
		typedef UBaseEffect Supper;
public:
	UCreateEntityEffect() {}
	virtual void InitData(const FSPACEDYNAMICEFFECT_DATA* dictData)override;
	virtual	void StartEffect(const FSPACEDYNAMICEFFECT_DATA* dictData)override;///<效果开启
	virtual void DestroyEffect()override;///<直接销毁
	virtual void StopEffect()override;///<效果销毁（会淡出处理）

	void CreateActor(const FSPACEDYNAMICEFFECT_DATA* dictData);
	int32 GetUId() { return UId; }
	AGameCharacter* GetSceneCharacter() { return SceneActor; }
private:
	void GetActorData(const FSPACEDYNAMICEFFECT_DATA* dictData, FCREATE_ENTITY_EFFECT_DATA &entityData);
	UFUNCTION()
	void SceneCreateApperanceOverEvent(AGameCharacter* SceneCharacter);
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 UId;///<场景entityUId 策划配置
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		AGameCharacter* SceneActor;
	FCreateEntityOverDelegate CreateEntityOver;
};

/**
*改变已有场景entity的动画效果
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UChangeEntityEffect : public UBaseEffect
{
	GENERATED_BODY()
		typedef UBaseEffect Supper;
public:
	UChangeEntityEffect() {}
	virtual void InitData(const FSPACEDYNAMICEFFECT_DATA* dictData)override;
	virtual void StartEffect(const FSPACEDYNAMICEFFECT_DATA* dictData)override;///<效果开启
	virtual void DestroyEffect()override;///<直接销毁
	virtual void StopEffect()override;///<效果销毁（会淡出处理）
	int32 GetUId() { return UId; }
private:
	void GetActorData(const FSPACEDYNAMICEFFECT_DATA* dictData);
	UFUNCTION()
	void CreateEntityOverEvent(UBaseEffect* InEffect);
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 UId;///<场景entityUId 策划配置
	FCREATE_ENTITY_EFFECT_DATA entityData;
};


/**
*销毁已有场景entity
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UDestroyEntityEffect : public UBaseEffect
{
	GENERATED_BODY()
		typedef UBaseEffect Supper;
public:
	UDestroyEntityEffect() {}
	virtual void InitData(const FSPACEDYNAMICEFFECT_DATA* dictData)override;
	virtual void StartEffect(const FSPACEDYNAMICEFFECT_DATA* dictData)override;///<效果开启
	virtual void DestroyEffect()override;///<直接销毁
	virtual void StopEffect()override;///<效果销毁（会淡出处理）

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FTimerHandle> cbids;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int Count = 0;
};

/**
* 根据脚本类型 创建 场景物件
* param1：场景物件脚本（程序提供）
* param2：刷出坐标朝向（11;22;33|0;0;0.4）
* param3~5:供场景物件脚本扩展使用
*/
UCLASS(BlueprintType)
class CHUANGSHI_API UCreateEffectByScript : public UBaseEffect
{
	GENERATED_BODY()
		typedef UBaseEffect Supper;
public:
	UCreateEffectByScript() {}
	virtual void StartEffect(const FSPACEDYNAMICEFFECT_DATA* dictData)override;///<效果开启
	virtual void DestroyEffect()override;///<直接销毁

public:
	class ASceneCharacter* SceneActor;
};


/**
* 根据服务器设置spaceData，客户端动态改变地图相关效果
*/
UCLASS(BlueprintType)
class CHUANGSHI_API USpaceDynamicEffectManager : public UCS3Object
{
	GENERATED_BODY()

public:
	USpaceDynamicEffectManager();
	~USpaceDynamicEffectManager();

	static USpaceDynamicEffectManager* GetInstance();

	virtual void onEnterWorld();            ///< 当Entity进入世界时，此方法被调用
	virtual void onLeaveWorld();            ///< 当Entity离开世界（被销毁时）时，此方法被调用
	virtual void OnEnterScenes() {};		///<开始场景
	virtual void OnLeaveScenes();			///<离开场景
	/*
	*	在当前地图增加一个效果
	*/
	UFUNCTION(BlueprintCallable)
		void AddEffect(int32 effectID);

	void AddAllEffect();///<加载当前地图所有效果
	UFUNCTION(BlueprintCallable)
		void DelEffect(int32 effectID);///<删除一个效果，淡出处理
	UFUNCTION(BlueprintCallable)
		void ClearEffect(int32 effectID);///<清除一个效果，淡出处理
	UFUNCTION(BlueprintCallable)
		void DelAllEffect();///<删除当前地图的所有效果
	UFUNCTION(BlueprintCallable)
		void OnSpaceEffectChanged(TArray<int32> EffectList);///<服务器设置spaceData

	UCreateEntityEffect* GetCreateEntityEffectByUId(int32 entityUId);///<根据EntityUID获取CreateEntityEffect
	
	void ClearEffectByUId(int32 entityUId);///<根据entityUID删掉相关Effect

	void ClearEffectByEffect(UBaseEffect* effect);

	int32 GetEffectIDByEffect(UBaseEffect* effect);
	void ClearAllCB();

	void UpdateModelVisible(TArray<FString> IgnoreUIDs);///<更新现有场景物件的可见性
	
	int32 GetSceneCharacterUID(AActor* Actor);///<获取Acotr的UID
private:
	const FSPACEDYNAMICEFFECT_DATA* GetSpaceDynamicEffectData(const FString& EffectsId);

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TMap<int32, UBaseEffect*> Effects;///<需要保存的效果，离开对应地图时需要删除，比如：雾区效果
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		TArray<FTimerHandle> cbids;

	//static USpaceDynamicEffectManager* Instance;
};

