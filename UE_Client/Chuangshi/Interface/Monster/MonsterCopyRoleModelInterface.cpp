// Fill out your copyright notice in the Description page of Project Settings.


#include "MonsterCopyRoleModelInterface.h"


int32 UMonsterCopyRoleModelInterface::GetOwnerID()
{
	if (GetEntity() != nullptr)
	{
		return GetEntity()->GetDefinedProperty(TEXT("ownerID")).GetValue<int32>();
	}
	return 0;
}

void UMonsterCopyRoleModelInterface::DelayCreateApperance()
{
	WaitTime = 0;
	TWeakObjectPtr<UMonsterCopyRoleModelInterface> ThisPtr(this);
	UGolbalBPFunctionLibrary::CustomTimerManager()->SetTimer(this, DelayCreateAppearHandle, FTimerDelegate::CreateLambda([ThisPtr]()
	{
		if (ThisPtr.IsValid())
		{
			UMonsterCopyRoleModelInterface* thisObj = ThisPtr.Get();
			AMonsterCharacter* monster = Cast<AMonsterCharacter>(thisObj->GetActor());
			if (IsValid(monster))
			{
				monster->CreateAppearance();
				UGolbalBPFunctionLibrary::CustomTimerManager()->ClearTimer(thisObj->DelayCreateAppearHandle);
				return;
			}
			thisObj->WaitTime += 1;
			if (thisObj->WaitTime >= 10)
			{
				UGolbalBPFunctionLibrary::CustomTimerManager()->ClearTimer(thisObj->DelayCreateAppearHandle);
			}
		}
	}), 1.0, true);
}