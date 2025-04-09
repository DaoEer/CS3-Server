

#include "BaseShape.h"
// CS3ÀàÐÍ
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/ShapeManager.h"
#include "Manager/CustomTimerManager.h"

UBaseShape::UBaseShape()
{
}


UBaseShape::~UBaseShape()
{
}

void UBaseShape::EnableTick()
{
	UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(TickHandle, this, &UBaseShape::Tick, 0.1f, true);
}

void UBaseShape::DisableTick()
{
	if (bOverlap)
	{
		EndOverlap.Broadcast();
		//EndOverlapSingle.ExecuteIfBound();
		bOverlap = false;
	}
	UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(TickHandle);
}

void UBaseShape::Tick()
{
	if (!bOverlap && ActorOnShape())
	{
		BeginOverlap.Broadcast();
		BeginOverlapSingle.ExecuteIfBound();
		bOverlap = true;
	}
	else if (bOverlap && !ActorOnShape())
	{
		EndOverlap.Broadcast();
		EndOverlapSingle.ExecuteIfBound();
		bOverlap = false;
	}
}

void UBaseShape::DestoryShape()
{
	DisableTick();
	UUECS3GameInstance::Instance->ShapeManager->ShapeList.Remove(this);
}

void UBaseShape::Reset()
{
	bOverlap = false;
}

void UBaseShape::BeginDestroy()
{
	if (UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->ShapeManager && UUECS3GameInstance::Instance->ShapeManager->ShapeList.Contains(this))
	{
		DestoryShape();
	}

	Super::BeginDestroy();
}

