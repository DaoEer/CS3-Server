#pragma once
#include "CoreMinimal.h"
#include "Actor/Scene/MovingPlatformCharacter.h"
#include "../../Component/CS3LightComponent.h"
#include "MovingPlatformVehicleCharacter.generated.h"

/*
* 文件名称：MovingPlatformVehicleCharacter.h
* 功能说明：多人可移动骑乘
* 文件作者：liyuxia
* 目前维护：liyuxia
* 创建 2020/9/8
*/

class USpringArmComponentEX;
class UCS3CameraComponent;
class UPosSyncComponent;

UCLASS(BlueprintType, Blueprintable)
class AMovingPlatformVehicleCharacter : public AMovingPlatformCharacter
{
	GENERATED_BODY()
public:
	AMovingPlatformVehicleCharacter();
	virtual void BeginPlay()override;
	virtual void OnCreateApperanceOver() override;
	virtual void OnBindToEntity()override;
	virtual void OnUnBindActorCallBack()override;
	virtual void InitCharacterComponent()override;
	virtual float GetMoveSpeed() override;
	virtual bool IsActiveMoveing()override;
	bool SwitchControl(bool InIsControl);
	bool SwitchMoveVehicleMode(bool IsActive);
	void CreateVehicleAppearance(FString CarrierModelId);//创建载具外观
	void SwitchCamera( bool IsActive);

private:
	void SetMovementActive(bool bNewActive);
	void InitCameraComponent();//初始化摄像机组件
	void InitPosSyncComponent();//初始化位置同步组件
	void InitLightComponent();///<初始化光照组件

public:
	UPROPERTY()
	USpringArmComponentEX* SpringArmCompent;
	UPROPERTY()
	UCS3CameraComponent* CameraComponent;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	UCS3LightComponent* CS3LightComponent;///<光照组件
	UPROPERTY()
	UPosSyncComponent* PosSyncComp;
	bool bIsControl;
};
