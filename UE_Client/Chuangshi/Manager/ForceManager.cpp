// Fill out your copyright notice in the Description page of Project Settings.


#include "ForceManager.h"
#include "Component/Role/OtherDirForceComponent.h"
#include"Chuangshi.h"

UForceManager::UForceManager()
{
	ForceCount = 0;
}


UForceManager* UForceManager::GetInstance()
{
	cs3_checkNoReentry();

	return NewObject<UForceManager>();
}

int32 UForceManager::AddForce(ACharacter* AddForceCharacter, float _ForceSpeed, FVector _ForceDirection)
{
	//判断角色有效性
	if (IsValid(AddForceCharacter))
	{
		//创建组件
		UForceComponent* NewComponent = NewObject<UForceComponent>(AddForceCharacter, "");

		if (IsValid(NewComponent))
		{
			//添加组件到角色
			AddForceCharacter->AddOwnedComponent(NewComponent);
			//注册组件
			NewComponent->RegisterComponent();
			//绑定到根组件
			NewComponent->AttachToComponent(AddForceCharacter->GetRootComponent(), FAttachmentTransformRules::KeepRelativeTransform);
			//开始力
			NewComponent->BeginForce(_ForceSpeed, _ForceDirection);

			//计算力的ID
			if (0 == ForceDictionarie.Num())
			{
				ForceCount = 0;
			}
			else
			{
				ForceCount++;
			}

			//添加到数组
			ForceDictionarie.Add(ForceCount, NewComponent);

			//设置此力的额外百分比
			if (ForcePercentageMap.Contains(AddForceCharacter))
			{
				SetForcePercentageByCharacter(AddForceCharacter);
			}
			else
			{
				SetCharacterForcePercentage(AddForceCharacter, 0.0f);
			}

			return ForceCount;
		}

		return -1;
	}

	return -1;
}

int32 UForceManager::AddForce(ACharacter* AddForceCharacter, float _ForceSpeed, ELOCAL_FORCE_DIRE ForceDire)
{
	if (IsValid(AddForceCharacter))
	{
		UForceComponent* NewComponent = NewObject<UForceComponent>(AddForceCharacter, "");

		if (IsValid(NewComponent))
		{
			//添加组件到角色
			AddForceCharacter->AddOwnedComponent(NewComponent);
			//注册组件
			NewComponent->RegisterComponent();
			//绑定到根组件
			NewComponent->AttachToComponent(AddForceCharacter->GetRootComponent(), FAttachmentTransformRules::KeepRelativeTransform);
			//开始力
			NewComponent->BeginForce(_ForceSpeed, ForceDire);

			//计算力的ID
			if (0 == ForceDictionarie.Num())
			{
				ForceCount = 1;
			}
			else
			{
				ForceCount++;
			}

			//添加到MAPS
			ForceDictionarie.Add(ForceCount, NewComponent);

			//设置此力的额外百分比
			if (ForcePercentageMap.Contains(AddForceCharacter))
			{
				SetForcePercentageByCharacter(AddForceCharacter);
			}
			else
			{
				SetCharacterForcePercentage(AddForceCharacter, 0.0f);
			}

			return ForceCount;
		}

		return -1;
	}

	return -1;
}

int32 UForceManager::AddForceUseOtherLocDire(ACharacter* AddForceCharacter, ACharacter* OtherCharacter, float _ForceSpeed, ELOCAL_FORCE_DIRE ForceDire)
{
	if (IsValid(AddForceCharacter))
	{
		UOtherDirForceComponent* NewComponent = NewObject<UOtherDirForceComponent>(AddForceCharacter, "");

		if (IsValid(NewComponent))
		{
			//添加组件到角色
			AddForceCharacter->AddOwnedComponent(NewComponent);
			//注册组件
			NewComponent->RegisterComponent();
			//绑定到根组件
			NewComponent->AttachToComponent(AddForceCharacter->GetRootComponent(), FAttachmentTransformRules::KeepRelativeTransform);
			//开始力
			NewComponent->BeginForce(_ForceSpeed, ForceDire);

			//计算力的ID
			if (0 == ForceDictionarie.Num())
			{
				ForceCount = 1;
			}
			else
			{
				ForceCount++;
			}

			//添加到MAPS
			ForceDictionarie.Add(ForceCount, NewComponent);

			//添加额外的角色
			NewComponent->SetOtherCharacter(OtherCharacter);

			//设置此力的额外百分比
			if (ForcePercentageMap.Contains(AddForceCharacter))
			{
				SetForcePercentageByCharacter(AddForceCharacter);
			}
			else
			{
				SetCharacterForcePercentage(AddForceCharacter, 0.0f);
			}

			return ForceCount;
		}

		return -1;
	}

	return -1;
}

bool UForceManager::BeginForce(int32 ForceID, float _ForceSpeed /*= -1.0f*/, FVector _ForceDirection /*= FVector::ZeroVector*/)
{
	//判断是否有这个ID
	if (!ForceDictionarie.Contains(ForceID))
	{
		return false;
	}

	UForceComponent* Force = *ForceDictionarie.Find(ForceID);
	if (IsValid(Force))
	{
		Force->BeginForce(_ForceSpeed, _ForceDirection);
		return true;
	}
	else
	{
		return false;
	}
}

bool UForceManager::BeginForce(int32 ForceID, ELOCAL_FORCE_DIRE ForceDire, float _ForceSpeed)
{
	//判断是否有这个ID
	if (!ForceDictionarie.Contains(ForceID))
	{
		return false;
	}

	UForceComponent* Force = *ForceDictionarie.Find(ForceID);
	if (IsValid(Force))
	{
		Force->BeginForce(_ForceSpeed, ForceDire);
		return true;
	}
	else
	{
		return false;
	}
}

bool UForceManager::PauseForce(int32 ForceID)
{
	//判断是否有这个ID
	if (!ForceDictionarie.Contains(ForceID))
	{
		return false;
	}

	UForceComponent* Force = *ForceDictionarie.Find(ForceID);
	if (IsValid(Force))
	{
		Force->StopForce();
		return true;
	}
	else
	{
		return false;
	}
}

void UForceManager::StopForces(ACharacter* DetachForceCharacter, int32 ForceID)
{
	if (!IsValid(DetachForceCharacter))
	{
		CS3_Warning(TEXT("UForceManager::StopForces-- DetachForceCharacter Is Not Valid!"));
		return;
	}
	if (ForceDictionarie.Num() > 0)
	{
		auto TeamFind = ForceDictionarie.Find(ForceID);
		if (nullptr != TeamFind)
		{
			auto TemForce = *TeamFind;
			if (IsValid(TemForce) && TemForce->GetOwner() == DetachForceCharacter)
			{
				TemForce->DestroyComponent();
				ForceDictionarie.Remove(ForceID);
			}
		}
	}
}

void UForceManager::StopAllForces(ACharacter* DetachForceCharacter, TArray<int32>& ForceArr)
{
	if (!IsValid(DetachForceCharacter))
	{
		CS3_Warning(TEXT("UForceManager::StopAllForces-- DetachForceCharacter Is Not Valid!"));
		return;
	}
	
	//清空力
	for (auto ForceID : ForceArr)
	{
		auto TeamFind = ForceDictionarie.Find(ForceID);

		if (nullptr != TeamFind)
		{
			auto TemForce = *TeamFind;
			if (IsValid(TemForce) && TemForce->GetOwner() == DetachForceCharacter)
			{
				TemForce->DestroyComponent();
				ForceDictionarie.Remove(ForceID);
			}
		}
	
	}

	ForceArr.Empty();
}

void UForceManager::SetCharacterForcePercentage(ACharacter* Character, float Percentage)
{
	//判断角色的有效性
	if (!IsValid(Character))
	{
		return;
	}

	//判断角色是否已经设置了百分比
	if (ForcePercentageMap.Contains(Character))
	{
		ForcePercentageMap[Character] = Percentage;
	}
	else
	{
		ForcePercentageMap.Add(Character, Percentage);
	}

	SetForcePercentageByCharacter(Character);
}

void UForceManager::SetForcePercentageByCharacter(ACharacter* Character)
{
	float Percentage = 0.0f;

	if (ForcePercentageMap.Contains(Character))
	{
		Percentage = ForcePercentageMap[Character];
	}
	else
	{
		return;
	}

	//给所有的力更新百分比
	for (auto force : ForceDictionarie)
	{
		if (IsValid(force.Value) && force.Value->GetOwner() == Character)
		{
			force.Value->ForcePercentage = Percentage;
		}
	}
}

