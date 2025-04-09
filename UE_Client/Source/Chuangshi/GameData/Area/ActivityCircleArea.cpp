#include "ActivityCircleArea.h"
#include "Vector.h"
#include "Actor/ServerCharacter.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Interface/Role/RoleActivityInterface.h"


UActivityCircleArea::UActivityCircleArea()
{
}


UActivityCircleArea::~UActivityCircleArea()
{
}

void UActivityCircleArea::InitParams(const FString SpaceScriptID, const FVector position, const float range, const int32 Index)
{
	Point = position;
	Range = range;
	AreaIndex = Index;
	ScriptID = SpaceScriptID;
}
bool UActivityCircleArea::IsPlayerIn()
{
	AServerCharacter* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!PlayerActor)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UActivityCircleArea::IsPlayerIn : PlayerActor!"));
		return false;
	}
	//获取当前Level
	const FString level = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	if (!level.Equals(ScriptID))return false;

	FVector PlayerPosition = PlayerActor->GetActorLocation();
	// 两个坐标点之间的距离
	int Distance = FVector::Dist(Point, PlayerPosition);
	if (Distance > Range)return false;

	return true;
}

void UActivityCircleArea::OnEnter(const FString SpaceScriptID)
{
	URoleActivityInterface* RoleActivityInterface = Cast<URoleActivityInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleActivityInterface"), 0));
	if (RoleActivityInterface)
	{
		RoleActivityInterface->RPC_OnEnterActivityCircleArea(AreaIndex);
	}
}

void UActivityCircleArea::OnLeave(const FString SpaceScriptID)
{
	URoleActivityInterface* RoleActivityInterface = Cast<URoleActivityInterface>(UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("RoleActivityInterface"), 0));
	if (RoleActivityInterface)
	{
		RoleActivityInterface->RPC_OnLeaveActivityCircleArea(AreaIndex);
	}
}