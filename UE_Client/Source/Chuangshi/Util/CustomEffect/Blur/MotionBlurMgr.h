#pragma once

#include "Components/MeshComponent.h"
#include "Materials/MaterialInterface.h"
#include "MeshBlur.h"
#include "MotionBlurMgr.generated.h"

/*
* 文件名称：MotionBlurMgr.h
* 功能说明：运动残影管理器
* 文件作者：zhengxuemei
* 目前维护：wuxiaoou
* 创建时间：2016-09-10
*/

class AMeshBlur;
class ASkeletalMeshBlur;
class APoseableBlur;

struct MeshMatchData
{
	TWeakObjectPtr<UMeshComponent> MeshComp;	// 要创建的模型组件
	TWeakObjectPtr<UObject> MatchMesh;			// 用来创建残影的mesh(USkeletalMesh,UStaticMesh)，如果此项为空用MeshComp自身的Mesh创建
	MeshMatchData(UMeshComponent* MeshComp, UObject* MatchMesh)
	{
		this->MeshComp = MeshComp;
		this->MatchMesh = MatchMesh;
	}
};

class FBlurData
{
public:
	float Lifetime;
	int Count;
	float IntervalTime;
	float IntervalTimer;
	int CreatedBlurCount;
	bool TickPos;
	TArray<MeshMatchData> Meshes;
	TArray<UMaterialInterface*> Materials;

	FBlurData(TArray<MeshMatchData> Meshes, float Lifetime, int Count, float IntervalTime, TArray<UMaterialInterface*> Materials, bool Tickpos)
	{
		this->Meshes = Meshes;
		this->Lifetime = Lifetime;
		this->Count = Count;
		this->IntervalTime = IntervalTime;
		this->Materials = Materials;
		this->TickPos = Tickpos;
		this->IntervalTimer = 0.0f;
		CreatedBlurCount = 0;
	}
};

UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API AMotionBlurMgr : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	AMotionBlurMgr();

	// Called when the game starts or when spawned
	virtual void BeginPlay() override;
	
	// Called every frame
	virtual void Tick( float DeltaSeconds ) override;

	virtual void Destroyed() override;
	
	virtual bool ShouldTickIfViewportsOnly() const override;// 在world不启动的时候也可以每帧Tick

	void CreateBlurMeshes(const TArray<MeshMatchData>& Meshes, float Lifetime, int Count, float IntervalTime, TArray<UMaterialInterface*> Materials, bool TickPos);

	void CreateBlurOneMesh(const MeshMatchData& Mesh, float Lifetime, int Count, float IntervalTime, TArray<UMaterialInterface*> Materials, bool TickPos);

	APoseableBlur* CreateBlurMeshesDirect(const TArray<MeshMatchData>& Meshes, float Lifetime, UMaterialInterface* Material, bool TickPos);
	//TArray<AMeshBlur*> CreateBlurMeshesDirect(const TArray<MeshMatchData>& Meshes, float Lifetime, UMaterialInterface* Material, bool TickPos);
private:

	AMeshBlur* _CreateSingleBlur(const MeshMatchData& Mesh, float Lifetime, UMaterialInterface* Material, bool TickPos);
	
	TArray<AMeshBlur*> BlurArray;
	
	TArray<FBlurData*> OriginalData;
};
