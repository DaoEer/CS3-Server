#pragma once

#include "MeshBlur.h"
#include "SkeletalMeshBlur.generated.h"

/*
* 文件名称：SkeletalMeshBlur.h
* 功能说明：SkeletalMesh残影
* 文件作者：zhengxuemei
* 目前维护：wuxiaoou
* 创建时间：2016-09-10
*/

class UPoseableMeshComponent;

UCLASS(BlueprintType)
class CHUANGSHI_API ASkeletalMeshBlur : public AMeshBlur
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	ASkeletalMeshBlur();

	// Called every frame
	virtual void Tick(float DeltaSeconds) override;

	virtual void Destroyed() override;
	// 创建一个SkeletalMesh的Blur
	virtual bool CreateBlur(UMeshComponent* ParentMesh, UObject* Obj, float Life, UMaterialInterface* Material, bool TickPos = false) override;

	UPoseableMeshComponent* GetPoseableMesh();

	USkeletalMeshComponent* ParentPoseMesh;

private:

	UPROPERTY(VisibleDefaultsOnly, Category = "AnimNotify")
	UPoseableMeshComponent* PoseableMesh;
	
	USkeletalMeshComponent* m_ParentMesh;

	bool m_bTickPos;

	FTimerHandle CopyTimeHandle;
	void CopyTimerEvent();
};
