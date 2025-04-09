// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "../Util/CustomEffect/Blur/MotionBlurMgr.h"
#include "GameData/CS3Object.h"
#include "Components/MeshComponent.h"
#include "Materials/MaterialInterface.h"
#include "MotionBlurManager.generated.h"

/*
* 文件名称：MotionBlurManager.h
* 功能说明：贴花粒子管理器
* 文件作者：zhengxuemei
* 创建时间：2020年3月20日09:28:44
*/
class AMotionBlurMgr;

UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API UMotionBlurManager : public UCS3Object
{
	GENERATED_BODY()

public:
	UMotionBlurManager();
	~UMotionBlurManager();

	//编辑器模式下会使用的单例，做特殊处理不和UUECS3GameInstance绑定
	// zhengxuemei,2020年3月19日09:51:39，如需修改请慎重。
	static UMotionBlurManager* GetInstance();
	static void ClearInstance();

	virtual void BeginDestroy()override;

	// 创建残影模型
	// ParentMeshComp：需要创建的模型的主模型组件。如主角分多个部件，只要输入一个主UMeshComponent即可
	//（内部会自动查找Attach到这个UMeshComponent的所有UMeshComponent，包括StaticMesh和SkeletalMesh）
	// Lifetime：残影模型的生命时间
	UFUNCTION(BlueprintCallable, Category = "MotionBlurManager")
	void CreateBlurMeshes(UMeshComponent* ParentMeshComp, float Lifetime, USkeletalMesh* DefaultMesh = nullptr, bool TickPos = false);

	// 创建残影模型
	// ParentMeshComp：需要创建的模型的主模型组件。如主角分多个部件，只要输入一个主UMeshComponent即可
	//（内部会自动查找Attach到这个UMeshComponent的所有UMeshComponent，包括StaticMesh和SkeletalMesh）
	// Lifetime：残影模型的生命时间
	// Count: 残影的个数
	// IntervalTime：生成每个残影的间隔时间s
	// Materials: 每个残影的材质，如为空则用模型原始材质
	void CreateBlurMeshes(UMeshComponent* ParentMeshComp, float Lifetime, int Count, float IntervalTime, 
		TArray<UMaterialInterface*> Materials, USkeletalMesh* DefaultMesh = nullptr, bool TickPos = false);

	// 直接创建残影模型（直接返回）
	// return: 返回创建的Actor列表
	UFUNCTION(BlueprintCallable, Category = "MotionBlurManager")
	APoseableBlur* CreateBlurMeshesDirect(UMeshComponent* ParentMeshComp, float Lifetime, UMaterialInterface* Material, USkeletalMesh* DefaultMesh = nullptr, bool TickPos = false);
	
	// 获取MeshComp包括Attach到MeshComp上的所有模型
	TArray<MeshMatchData> GetAttachedOriginMesh(UMeshComponent* ParentMeshComp, USkeletalMesh* DefaultMesh);

	// 在World中删除真正的管理器AMotionBlurMgr
	void DestroyRealMgrInWorld(UWorld* World);

private:
	// 在World中查找并创建真正的管理器AMotionBlurMgr
	AMotionBlurMgr* FindOrSpawnMotionBlurMgr(UWorld* World);
	// 在World中查找真正的管理器AMotionBlurMgr
	AMotionBlurMgr* GetMotionBlurMgr(UWorld* World);


private:
	static UMotionBlurManager* Instance;
};
