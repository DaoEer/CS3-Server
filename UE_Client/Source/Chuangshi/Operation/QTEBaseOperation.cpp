
#include "QTEBaseOperation.h"
#include "GameDevelop/CS3PlayerController.h"
#include "Util/GolbalBPFunctionLibrary.h"

void UQTEBaseOperation::Init()
{

}

float UQTEBaseOperation::ExecuteOperation()
{
	if (IsCanExecuteOperation())
	{
		BP_ExecuteOperation();
	}	
	return Value;
}

bool UQTEBaseOperation::IsCanExecuteOperation()
{
	if (!BP_IsCanExecuteOperation())
	{
		return false;
	}
	return true;
}

bool UQTEBaseOperation::BP_IsCanExecuteOperation_Implementation()
{
	return true;
}

float UMouseQTEOperation::ExecuteOperation()
{
	ACS3PlayerController* PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
	if (IsValid(PlayerController))
	{
		float LocationY;
		PlayerController->GetMousePosition(CurMousePostion, LocationY);
		if (!FMath::IsNearlyZero(OldMousePostion) && !(FMath::IsNearlyEqual(CurMousePostion, OldMousePostion)))
		{
			if (FMath::Abs(CurMousePostion) < (FMath::Abs(OldMousePostion) - 20.0f))
			{
				L_Postion += 0.2f;
			}
			if ((CurMousePostion - 20.0f) > OldMousePostion)
			{
				R_Postion += 0.2f;
			}
		}
		if (FMath::IsNearlyEqual(L_Postion, 1.0f))
		{
			Value += 0.15f;
			L_Postion = 0.0f;
		}
		if (FMath::IsNearlyEqual(R_Postion, 1.0f))
		{
			Value += 0.15f;
			R_Postion = 0.0f;
		}
		PlayerController->GetMousePosition(OldMousePostion, LocationY);

		if (Value > 0.0f)
		{
			Value -= 0.005f;
		}

	}
	return Value;
}
