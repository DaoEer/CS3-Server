
#include "Capsule.h"
#include "Util/GolbalBPFunctionLibrary.h"

UShpaeCapsule::UShpaeCapsule()
{
}


UShpaeCapsule::~UShpaeCapsule()
{
}

bool UShpaeCapsule::ActorOnShape()
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

	// 当点Z小于胶囊HalfHeight的时候
	if (AbsZ < HalfHeight)
	{
		if (Size2D < Radius)
		{
			return true;
		}
	}
	// 当点的Z小于胶囊体高度时
	else if (FMath::Abs(TestPoint.Z) < HalfHeight + Radius)
	{
		float CurrentRadius = FMath::Sqrt(Radius * Radius - (TestPoint.Z - HalfHeight) * (TestPoint.Z - HalfHeight));

		if (Size2D < CurrentRadius)
		{
			return true;
		}
	}

	return false;
}

void UShpaeCapsule::UpdateBounds(FVector Parameter)
{
	//半径取XY的最小值
	Radius = Parameter.X < Parameter.Y ? Parameter.X : Parameter.Y;
	Radius *= SCALE;
	HalfHeight = Parameter.Z;
	HalfHeight *= SCALE;
}
