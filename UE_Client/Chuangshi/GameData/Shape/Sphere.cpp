
#include "Sphere.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "DrawDebugHelpers.h"

UShapeSphere::UShapeSphere()
{
}


UShapeSphere::~UShapeSphere()
{
}

bool UShapeSphere::ActorOnShape()
{
	AActor* Player = Cast<AActor>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

	if (!IsValid(Owner))
	{
		DestoryShape();
	} 
	else
	{
		if (IsValid(Player))
		{
			return  ((Owner->GetActorLocation() - Player->GetActorLocation()).Size() < Radius);
		}
	}

	return false;
}

void UShapeSphere::UpdateBounds(FVector Parameter)
{
	float Temp = Parameter.X < Parameter.Y ? Parameter.X : Parameter.Y;

	Radius = Temp < Parameter.Z ? Temp : Parameter.Z;

	Radius *= SCALE;
}
