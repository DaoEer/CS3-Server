#pragma once
#include "CoreMinimal.h"
#include "Actor/Monster/MonsterCharacter.h"
#include "MonsterGhostEyeCharacter.generated.h"

/*
* 文件名称：MonsterGhostEye.h
* 功能说明：鬼瞳之眼
* 文件作者：liyuxia
* 目前维护：liyuxia
* 创建 2020/4/2
*/

class USpringArmComponentEX;
class UCS3CameraComponent;
class UPosSyncComponent;

UCLASS(BlueprintType, Blueprintable)
class CHUANGSHI_API AMonsterGhostEyeCharacter : public AMonsterCharacter
{
	GENERATED_BODY()


public:
	AMonsterGhostEyeCharacter();
	virtual void BeginPlay()override;
	virtual void OnCreateApperanceOver() override;
	virtual void OnBindToEntity()override;
	virtual void OnUnBindActorCallBack()override;
	virtual void InitCharacterComponent()override;

private:
	bool SwitchControlToCharacter();
	bool SwitchControlToPlayer();
	void SetCharacterMovementActive(bool bNewActive);
	void InitCameraComponent();//初始化摄像机组件
	void InitPosSyncComponent();//初始化位置同步组件

public:
	UPROPERTY()
	USpringArmComponentEX* SpringArmCompent;
	UPROPERTY()
	UCS3CameraComponent* CameraComponent;
	UPROPERTY()
	UPosSyncComponent* PosSyncComp;
};