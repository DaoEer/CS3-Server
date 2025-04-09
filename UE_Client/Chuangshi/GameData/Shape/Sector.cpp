
#include "Sector.h"
#include "Util/GolbalBPFunctionLibrary.h"

UShapeSector::UShapeSector()
{
}


UShapeSector::~UShapeSector()
{
}

bool UShapeSector::ActorOnShape()
{
	AActor* Player = Cast<AActor>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());

	if (!Player || !Owner)
	{
		if (!Owner)
		{
			DestoryShape();
		}

		return false;
	}

	FVector TestPoint = FTransform(Owner->GetActorRotation(), Owner->GetActorLocation(), FVector(1)).InverseTransformPosition(Player->GetActorLocation());

	float AbsZ = FMath::Abs(TestPoint.Z);
	float Size2D = TestPoint.Size2D();

	
	if (AbsZ > Height / 2 || Size2D > Radius)
	{
		return false;
	}

	float Direction = FMath::Abs(FMath::RadiansToDegrees(FMath::Atan2(TestPoint.Y, TestPoint.X)));

	if (Direction < Angle / 2)
	{
		return true;
	}

	return false;
}

void UShapeSector::UpdateBounds(FVector Parameter)
{
	Radius = Parameter.X;
	Radius *= SCALE;

	Angle = FMath::Clamp(Parameter.Y, 0.f, 180.f);

	Height = Parameter.Z > 0.f ? Parameter.Z : 2.f;
	Height *= SCALE;
}

