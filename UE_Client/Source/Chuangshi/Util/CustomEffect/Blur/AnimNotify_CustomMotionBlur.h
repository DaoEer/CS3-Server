#pragma once

#include "Util/CustomEffect/CS3AnimNotify.h"
#include "MotionBlurMgr.h"
#include "AnimNotify_CustomMotionBlur.generated.h"

/*
* 文件名称：AnimNotify_CustomMotionBlur.h
* 功能说明：自定义运动残影的动画消息
* 文件作者：zhengxuemei
* 目前维护：wuxiaoou
* 创建时间：2016-09-10
*/

class AMotionBlurMgr;

UCLASS(const, hidecategories = Object, collapsecategories, meta = (DisplayName = "CS3Custom Motion Blur"))
class CHUANGSHI_API UAnimNotify_CustomMotionBlur : public UCS3AnimNotify
{
	GENERATED_BODY()
	
public:
	UAnimNotify_CustomMotionBlur();

	virtual void PostLoad() override;
// #if WITH_EDITOR
// 	virtual void PostEditChangeProperty(struct FPropertyChangedEvent& PropertyChangedEvent) override;
// #endif

	virtual FString GetNotifyName_Implementation() const override;

	virtual void Notify(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation) override;

	virtual void StopNotifyEffect(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation) override;

	UPROPERTY(EditAnywhere, Category = "AnimNotify")
		float Lifetime;

// 	UPROPERTY(EditAnywhere, Category = "AnimNotify")
// 		int BlurCount;
// 
// 	UPROPERTY(EditAnywhere, Category = "AnimNotify")
// 		float IntervalTime;

	UPROPERTY(EditAnywhere, Category = "AnimNotify")
	TArray<UMaterialInterface*> Materials;

	// 生成残影的模型，如果为空就用原始模型
	UPROPERTY(EditAnywhere, Category = "AnimNotify")
		USkeletalMesh* DefaultMesh;

	UPROPERTY(EditAnywhere, Category = "AnimNotify")
		uint32 TickPos : 1;

private:

};
