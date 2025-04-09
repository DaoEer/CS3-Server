
#include "Cylinder.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "DrawDebugHelpers.h"

UShapeCylinder::UShapeCylinder()
{
}


UShapeCylinder::~UShapeCylinder()
{
}

bool UShapeCylinder::ActorOnShape()
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
	//DrawDebugCylinder(GetWorld(), Owner->GetActorLocation() + 0.5*Height, Owner->GetActorLocation() - 0.5*Height, Radius, 20, FColor::White, false, 0.15f, 0, 5);
	if (AbsZ < Height / 2 && Size2D < Radius)
	{
		return true;
	}

	return false;
}

void UShapeCylinder::UpdateBounds(FVector Parameter)
{
	//半径取XY的最小值
	Radius = Parameter.X < Parameter.Y ? Parameter.X : Parameter.Y;
	Radius *= SCALE;
	Height = Parameter.Z;
	Height *= SCALE;
}


