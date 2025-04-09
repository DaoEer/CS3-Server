#pragma once

#include "Actor/GameCharacter.h"
#include "GameData/CharacterData.h"
#include "GameData/SpaceDynamicEffectData.h"
#include "SceneCharacter.generated.h"

/*
* 文件名称：SceneCharacter.h
* 功能说明：创建纯客户端entity效果，应用于桥、门
* 文件作者：huting
* 目前维护：huting
* 创建时间：2017-08-8
*/


DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FSceneCreateApperanceOverDelegate, AGameCharacter*, SceneCharacter);
/*
* 场景Character
*/
UCLASS(BlueprintType)
class CHUANGSHI_API ASceneCharacter :public AGameCharacter
{
	GENERATED_BODY()
public:
	ASceneCharacter();///<构造函数
	virtual void BeginPlay()override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
	void CreateActorData(FCREATE_ENTITY_EFFECT_DATA EntityEffectData);

	void SetActionData(TArray<FString> actionName, TArray<float> actionInterval, bool bIsRandom = false);//设置动作数据并重新处理播放动作

	void SetEffectData(TArray<FString> effectID, TArray<float> effectInterval, bool bIsRandom = false);//设置光效数据并重新处理播放动作

	void SetDestroyAction(FString actionName);///<设置死亡动作

	void SetDestroyEffect(FString effectID);///<设置死亡光效

	UFUNCTION(BlueprintImplementableEvent)
		void InitEffectData(const FSPACEDYNAMICEFFECT_DATA dictData);

	void ClearActionData();//清除动作数据
	void ClearEffectData();//清除光效数据

	UFUNCTION(BlueprintNativeEvent)
	void OnBeginDestroyActor();///<开始销毁之前的操作

	UFUNCTION()
	void CheckPlayEffect();///<光效播完事件
	UFUNCTION()
	void OnPlayDestroyEffectOver();///<销毁时光效播完事件
private:
	virtual void InitBaseComponent() override;///<重写InitBaseComponent		
	virtual void OnCreateApperanceOver() override;
	virtual void OnChangePartOver() override;

	void SetModelScale(const float &newValue);
	void SetCollisionType(const FString &newValue);

	void PlayMultiAction();	///<播放动作
	void CheckPlayAction(ACharacter *RoleChar, FACTION_DATA InActionData);///<检测播放动作
	void OnPlayDestroyActionOver(ACharacter *RoleChar, FACTION_DATA InActionData);

	void PlayMultiEffect();	///<播放光效
	void SetMeshCollisionType(ECollisionEnabled::Type CollisionTYpe);
	void SetCollisionCollisionTypeAndResponseToChannel(UMeshComponent* SKComp, ECollisionEnabled::Type CollisionTYpe);

	int GetRandomIndex(int MaxRandomIndex);///<获取随机数
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString ModelNumber;
	float ModelScale;
	FSceneCreateApperanceOverDelegate SceneCreateApperanceOver;

protected:
	//UPROPERTY()
	//	AEffectEmitter* CurEffect;///<当前正在播放的光效

	int32 CurEffectUID = -1;///<当前播放的光效的UID
private:
	bool bIsRandomAction = false;///<是否随机播放动作
	bool bIsRandomEffect = false;///<是否随机播放光效
	FString CollisionType;
	bool bAffectNavigation;///<可以创建寻路
	bool bCameraCollision = false;///<是否与摄像机发生碰撞	
	bool bVisibilityCollision = false;///<是否与可见的对象发生碰撞	
	TArray<FString> ActionNames;///<动作ID
	TArray<float> ActionIntervals;///<播放多个动作的时间间隔 
	TArray<FString> EffectIDs;///<光效ID
	TArray<float> EffectIntervals;///<播放多个光效的时间间隔 
	FString DeathActionID;///<死亡动作ID
	FString DeathEffectID;///<死亡光效ID
	FTimerHandle DelayHandle;///<动作定时器
	FTimerHandle DelayEffectHandle;///<光效定时器
};