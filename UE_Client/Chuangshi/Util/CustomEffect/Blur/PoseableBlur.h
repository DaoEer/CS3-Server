#pragma once
#include "MotionBlurMgr.h"
#include "GameFramework/Actor.h"
#include "Components/PoseableMeshComponent.h"
#include "PoseableBlur.generated.h"

/*
* 文件名称：PoseableBlur.h
* 功能说明：StaticMesh残影
* 文件作者：zhengxuemei
* 目前维护：wuxiaoou
* 创建时间：2016-09-10
*/

UCLASS(BlueprintType)
class CHUANGSHI_API APoseableBlur : public AActor
{
	GENERATED_BODY()

public:
	// Sets default values for this actor's properties
	APoseableBlur();

	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

	// Called every frame
	virtual void Tick(float DeltaSeconds) override;

	virtual void Destroyed() override;

	virtual bool ShouldTickIfViewportsOnly() const override;

	virtual bool CreateBlur(const TArray<MeshMatchData>& Meshes, float Life, UMaterialInterface* Material, bool TickPos = false);
	float Lifetime;
	float Lifetimer;
	// 渐变时间
	float FadeOutTime;
	float FadeOutTimer;
	UMaterialInstanceDynamic* DynamicMaterial;

	UPROPERTY(EditAnywhere, AdvancedDisplay)
		USceneComponent* DefaultSceneRoot;

	UPROPERTY(EditAnywhere, AdvancedDisplay)
		UPoseableMeshComponent* PoseableBlurMesh;

	// 	UPROPERTY(VisibleDefaultsOnly, Category = "AnimNotify")
	// 		UStaticMeshComponent* StaticMeshComp;

		//FVector DeviationTransform = FVector::ZeroVector;
	TArray<UMeshComponent*> m_MesheComps;
private:
	bool FirstAnimation;
	bool SkeletalAttachMesh =false;
	bool m_bTickPos;///静态网格物体位置跟随
	//UPROPERTY(VisibleDefaultsOnly, Category = "AnimNotify")
		//UStaticMeshComponent* StaticMeshComp;

	//TArray<UStaticMeshComponent*> StaticMeshes;
	//TArray<USkeletalMeshComponent*> SkeletalMeshes;

	USkeletalMeshComponent* ParentPoseMesh;
	//const UStaticMeshComponent* ParentStaticMesh;
	//FVector MeshDeviationTransform = FVector::ZeroVector;

	FTimerHandle CopyTimeHandle;
	FTimerHandle DelaySkeletalTimeHandle;
	void CopyTimerEvent();
	void SetMeshVisable();

	void CreateSkeletalPoseableMesh(UPoseableMeshComponent* mesh,MeshMatchData data, UMaterialInterface* Material);
};
