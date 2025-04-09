
#include "Box.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "DrawDebugHelpers.h"

UShapeBox::UShapeBox()
{
}


UShapeBox::~UShapeBox()
{
}

bool UShapeBox::ActorOnShape()
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
	//DrawDebugBox(GetWorld(), Owner->GetActorLocation(), FVector(X,Y,Z), Owner->GetActorRotation().Quaternion(), FColor::White, false, 0.15f, 0, 5);

	// еп╤о╠ъ╫Г
	if (!(FMath::Abs(TestPoint.X) < X))
	{
		return false;
	}
	
	if (!(FMath::Abs(TestPoint.Y) < Y))
	{
		return false;
	}

	if (!(FMath::Abs(TestPoint.Z) < Z))
	{
		return false;
	}

	return true;
}

void UShapeBox::UpdateBounds(FVector Parameter)
{
	X = Parameter.X;
	X *= SCALE;
	Y = Parameter.Y;
	Y *= SCALE;
	Z = Parameter.Z;
	Z *= SCALE;
}
