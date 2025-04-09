#include "MovingPlatformVehicle.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Actor/Scene/MovingPlatformVehicleCharacter.h"
#include "GameDevelop/CS3PlayerController.h"

CONTROL_COMPILE_OPTIMIZE_START

DEF_INTERFACE_BEGIN(MovingPlatformVehicle, Supper)
DEF_INTERFACE_END()

KBE_BEGIN_ENTITY_METHOD_MAP(MovingPlatformVehicle, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(MovingPlatformVehicle, Supper)
KBE_END_ENTITY_PROPERTY_MAP()


MovingPlatformVehicle::MovingPlatformVehicle()
{
	_fActorName = FString("MovingPlatformVehicle");
	isOnGround_ = false;
}

MovingPlatformVehicle::~MovingPlatformVehicle()
{

}

void MovingPlatformVehicle::OnLeaveWorld()
{
	//先停止控制再通知父类leaveWorld(以防服务器beforeDestroy后客户端Entity已经销毁了没通知到)
	//这里可能有问题。其他人客户端移动平台销毁也会走这所以加个判断,只通知主控制移动平台的玩家客户端
	if (ControlID != 0 && IsValid(Actor()))
	{
		AMovingPlatformVehicleCharacter* BindActor = Cast<AMovingPlatformVehicleCharacter>(Actor());
		if (IsValid(BindActor))
		{
			ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
			if (UGolbalBPFunctionLibrary::GetPlayerID() == ControlID && IsValid(PlayerController) && PlayerController->GetPawn() == BindActor)
			{
				OnStopControl();
			}
		}
	}
	Supper::OnLeaveWorld();//这个必须放后面，先调用完上面的，再通知父类会解绑Actor
}

void MovingPlatformVehicle::OnStartControl(int32 InDriverID)
{
	ControlID = InDriverID;
	if (IsValid(Actor()))
	{
		AMovingPlatformVehicleCharacter* BindActor = Cast<AMovingPlatformVehicleCharacter>(Actor());
		if (IsValid(BindActor))
		{
			BindActor->SwitchControl(true);
		}
	}
}

void MovingPlatformVehicle::OnStopControl()
{
	if (ControlID == 0) return;
	ControlID = 0;
	if (IsValid(Actor()))
	{
		AMovingPlatformVehicleCharacter* BindActor = Cast<AMovingPlatformVehicleCharacter>(Actor());
		if (IsValid(BindActor))
		{
			BindActor->SwitchControl(false);
		}
	}
}

UClass* MovingPlatformVehicle::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("MovingPlatformVehicleCharacter"));
}

CONTROL_COMPILE_OPTIMIZE_END
