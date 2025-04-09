#pragma once

#include "Distributions/DistributionFloat.h"
#include "GameFramework/Actor.h"
#include "GameData/CharacterData.h"
#include "SkeletalAnimParticle.generated.h"

/*
* 文件名称：SkeletalAnimParticle.h
* 功能说明：新添加一个骨骼动画
* 文件作者：zhengxuemei
* 目前维护：wuxiaoou
* 创建时间：2016-07-01
*/

class UBaseAnimInstance;

UCLASS(BlueprintType)
class CHUANGSHI_API ASkeletalAnimParticle : public AActor
{
	GENERATED_BODY()
	
public:	
	/// Sets default values for this actor's properties
	ASkeletalAnimParticle();

	/// Called when the game starts or when spawned
	virtual void BeginPlay() override;
	virtual void BeginDestroy() override;
	virtual void FinishDestroy() override;

	virtual void Destroyed() override;

	/// Called every frame
	virtual void Tick( float DeltaSeconds ) override;

	virtual bool ShouldTickIfViewportsOnly() const override;// 在world不启动的时候也可以每帧Tick

	void CheckDestroy();

	///绑链条专用
	UFUNCTION(BlueprintCallable, Category = "DecalEffect")
	bool InitLianRen(USkeletalMeshComponent* MeshComp, USkeletalMesh* SkeletalMesh, UAnimationAsset* Animation, UMaterialInterface* Material,
		float MeshScale, float AnimStartTime, float AnimRate,UParticleSystem* BindParticle, FName SocketName, bool BreakWhenAnimStop);

	///绑定mesh骨骼动画
	bool InitOther(USkeletalMeshComponent* MeshComp, USkeletalMesh* SkeletalMesh, UAnimationAsset* Animation, 
		FVector Scale3DOffset, float AnimRate, FName SocketName, bool IsLoop, bool IsAutoDesotry);

	void SetWeapon(bool bWeapon) { isWeapon = bWeapon; }
	UFUNCTION(BlueprintCallable, Category = "DecalEffect")
		bool IsWeapon() { return isWeapon; }

	void DestroyChilds();

	void SetLifeTime(float lifetime);

	UFUNCTION(BlueprintCallable, Category = "DecalEffect")
	void SetPlayRate(float Rate);

	UFUNCTION(BlueprintCallable, Category = "DecalEffect")
	void SetAnimPostion(float InPos);

	UFUNCTION(BlueprintCallable, Category = "DecalEffect")
	void SetPause(bool pause);

	void StopNotifyEffect();
private:
	void OnActionReadyChangeEvent(FACTION_DATA ActionData);

	void OnCheckWeaponBindObj();
	void WeaponBindActor(FPART_SLOT_BIND_OBJ_DATA& InObjData);
	void WeaponBindParticle(FPART_SLOT_BIND_OBJ_DATA& InObjData);
	void ClearWeaponBindObjData();
	void UpdateMaterial(float TimeProgress);
	//实时更新动画速度以及动画生成的相关通知衍生物播放速度
	void UpdateAnimNotifyRelated(USkeletalMeshComponent* SkelMeshComp);
	//销毁动画以及动画生成的相关通知衍生物
	void DestroyAnimNotifyRelated(USkeletalMeshComponent* SkelMeshComp);
	virtual void PostActorCreated() override;
public:
	UPROPERTY(EditAnywhere, AdvancedDisplay)
		USceneComponent* DefaultSceneRoot;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		USkeletalMeshComponent* SkeletalMeshComp;//链子骨骼组件
	void StratFadeInFadeOut(FRawDistributionFloat Value);
	void StratDissolve(FRawDistributionFloat Value, UTexture2D*);
private:
	bool Created;
	float DestroyTime;
	float Lifetime;
	float RecordDestroyTime;///TICK里计录销毁时间
	bool isWeapon;
	bool bBreakWhenAnimStop;
	bool bBreakWhenStopNotify;///<当接收停止通知效果时强制中断所有效果包括多层子效果
	UPROPERTY()
	UParticleSystemComponent* ParticleComp;
	UPROPERTY()
	UBaseAnimInstance * BaseAnimInstance;
	UPROPERTY()
	AActor* CurActor;//当前的对象

	bool UsedFade;
	UPROPERTY()
		FRawDistributionFloat AlphaValue;

	bool UseDissolve;
	UPROPERTY()
	FRawDistributionFloat  DissolveValue;
	UPROPERTY()
		UTexture2D* DissolveTexture;

	float TimeCount;
	bool bLifePause;

	UPROPERTY()
		TArray<ASkeletalAnimParticle*> ChildAnimNotifySkMesh;
	UPROPERTY()
		TArray<UParticleSystemComponent*> ChildAnimNotifyParticle;
public:
#ifdef SEQUENCER_ICESWORD_ON
	IceSwordBaseControler ISBControler;
#endif
};
