#pragma once
#include "BaseAnimInstance.h"
#include "RoleAnimInstance.generated.h"

/*
* 文件名称：RoleAnimInstance.h
* 功能说明：
* 文件作者：ranyuan
* 目前维护：ranyuan
* 创建时间：2017-02-23
*/
UCLASS(Blueprintable, hideCategories = RoleAnimInstance, BlueprintType, meta = (BlueprintThreadSafe), Within = SkeletalMeshComponent)
class CHUANGSHI_API URoleAnimInstance : public UBaseAnimInstance
{
	GENERATED_BODY()
public:
	URoleAnimInstance();
	~URoleAnimInstance();
	void NativeUpdateAnimation(float DeltaSeconds) override;
	virtual void PlayShouDaoAction(const FActionOverDelegate& InActionOverDelegate = FActionOverDelegate())override;
	virtual void PlayBaDaoAction(const FActionOverDelegate& InActionOverDelegate = FActionOverDelegate())override;
	virtual void PlayClimbLadderAction()override;

protected:
	virtual bool IsInWater()override;
	virtual void UpdateMoveDirection()override;
	virtual FName GetMontageSectionId(FACTION_DATA& InActionData)override;///获取射击蒙太奇片段ID

private:
	void UpdateAimOffsetDirction();

public:

protected:
	UPROPERTY(BlueprintReadOnly, Category = "RoleAnimInstance")
		float CurAimOffsetYaw;///瞄准偏移平移yaw值

	UPROPERTY(BlueprintReadOnly, Category = "RoleAnimInstance")
		float CurAimOffsetPitch;///瞄准偏移上下Pitch值

private:
	bool IsInJumpAir;//是否跳跃至空中
	bool IsOnLandingFromJumpAir;//是否从跳跃空中着陆
};

