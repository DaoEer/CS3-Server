#pragma once

#include "GameFramework/Actor.h"
#include "MeshBlur.generated.h"

/*
* 文件名称：MeshBlur.h
* 功能说明：StaticMesh残影
* 文件作者：zhengxuemei
* 目前维护：wuxiaoou
* 创建时间：2016-09-10
*/

UCLASS(BlueprintType)
class CHUANGSHI_API AMeshBlur : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	AMeshBlur();

	// Called when the game starts or when spawned
	virtual void BeginPlay() override;
	
	// Called every frame
	virtual void Tick( float DeltaSeconds ) override;

	virtual void Destroyed() override;

	virtual bool ShouldTickIfViewportsOnly() const override;
	
	// 创建一个StaticMesh的Blur，解决武器没有残影的问题
	virtual bool CreateBlur(UMeshComponent* Mesh, UObject* Obj, float Life, UMaterialInterface* Material, bool TickPos = false);
	float Lifetime;
	float Lifetimer;
	// 渐变时间
	float FadeOutTime;
	float FadeOutTimer;
	UMaterialInstanceDynamic* DynamicMaterial;

	UPROPERTY(EditAnywhere, AdvancedDisplay)
		USceneComponent* DefaultSceneRoot;

	// 指针指向StaticMeshComp或者PoseableMesh
	UPROPERTY(EditAnywhere, AdvancedDisplay)
		UMeshComponent* MeshComp;

	UStaticMeshComponent* GetStaticMesh();

	FVector DeviationTransform = FVector::ZeroVector;

private:
	bool m_TickPos;///静态网格物体位置跟随
	UPROPERTY(VisibleDefaultsOnly, Category = "AnimNotify")
		UStaticMeshComponent* StaticMeshComp;

	const UStaticMeshComponent* ParentStaticMesh;
	FVector MeshDeviationTransform = FVector::ZeroVector;
};
