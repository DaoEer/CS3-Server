// Fill out your copyright notice in the Description page of Project Settings.


#include "ModelInterface.h"
#include "Actor/ServerCharacter.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"

CS3_BEGIN_INTERFACE_METHOD_MAP(UModelInterface, Supper)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(UModelInterface, Supper)
CS3_END_INTERFACE_PROPERTY_MAP()
	
UModelInterface::UModelInterface()
{
}

UModelInterface::~UModelInterface()
{

}

void UModelInterface::OnRep_headModel()
{
	if (GetEntity() == nullptr) 
	{
		CS3_Warning(TEXT("-->Null Pointer error:UModelInterface::OnRep_headModel : GetEntity()!"));
		return;
	}

	FString headModel = GetEntity()->GetDefinedProperty(TEXT("headModel"));
	ChangePart((int)MODEL_PART_TYPE::MODEL_PART_HEADS, headModel);
}

void UModelInterface::OnRep_cloakModel()
{
	if (GetEntity() == nullptr) 
	{
		CS3_Warning(TEXT("-->Null Pointer error:UModelInterface::OnRep_cloakModel : GetEntity()!"));
		return;
	}
	FString cloakModel = GetEntity()->GetDefinedProperty(TEXT("cloakModel"));
	ChangePart((int)MODEL_PART_TYPE::MODEL_PART_CLOAK, cloakModel);
}

void UModelInterface::OnRep_bodyModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UModelInterface::OnRep_bodyModel : GetEntity()!"));
		return;
	}
	FString bodyModel = GetEntity()->GetDefinedProperty(TEXT("bodyModel"));
	ChangePart((int)MODEL_PART_TYPE::MODEL_PART_BODYS, bodyModel);
}

void UModelInterface::OnRep_hairModel()
{
	if (GetEntity() == nullptr) 
	{
		CS3_Warning(TEXT("-->Null Pointer error:UModelInterface::OnRep_hairModel : GetEntity()!"));
		return;
	}
	FString hairModel = GetEntity()->GetDefinedProperty(TEXT("hairModel"));
	ChangePart((int)MODEL_PART_TYPE::MODEL_PART_HAIRS, hairModel);
}

void UModelInterface::OnRep_adornModel()
{
	if (GetEntity() == nullptr) 
	{
		CS3_Warning(TEXT("-->Null Pointer error:UModelInterface::OnRep_adornModel : GetEntity()!"));
		return;
	}
	FString adornModel = GetEntity()->GetDefinedProperty(TEXT("adornModel"));
	ChangePart((int)MODEL_PART_TYPE::MODEL_PART_ADORN, adornModel);
}

void UModelInterface::OnRep_hatModel()
{
	if (GetEntity() == nullptr) 
	{
		CS3_Warning(TEXT("-->Null Pointer error:UModelInterface::OnRep_hatModel : GetEntity()!"));
		return;
	}
	FString hatModel = GetEntity()->GetDefinedProperty(TEXT("hatModel"));
	ChangePart((int)MODEL_PART_TYPE::MODEL_PART_HAT, hatModel);
}

void UModelInterface::OnRep_coatModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UModelInterface::OnRep_coatModel : GetEntity()!"));
		return;
	}
	FString coatsModel = GetEntity()->GetDefinedProperty(TEXT("coatModel"));
	ChangePart((int)MODEL_PART_TYPE::MODEL_PART_COATS, coatsModel);
}

void UModelInterface::OnRep_wristModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UModelInterface::OnRep_wristModel : GetEntity()!"));
		return;
	}
	FString wristModel = GetEntity()->GetDefinedProperty(TEXT("wristModel"));
	ChangePart((int)MODEL_PART_TYPE::MODEL_PART_WRIST, wristModel);
}

void UModelInterface::OnRep_handModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UModelInterface::OnRep_handModel : GetEntity()!"));
		return;
	}
	FString handModel = GetEntity()->GetDefinedProperty(TEXT("handModel"));
	ChangePart((int)MODEL_PART_TYPE::MODEL_PART_GLOVES, handModel);//手套
}

void UModelInterface::OnRep_waistModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UModelInterface::OnRep_waistModel : GetEntity()!"));
		return;
	}
	FString waistModel = GetEntity()->GetDefinedProperty(TEXT("waistModel"));
	ChangePart((int)MODEL_PART_TYPE::MODEL_PART_WAIST, waistModel);
}

void UModelInterface::OnRep_pantsModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UModelInterface::OnRep_pantsModel : GetEntity()!"));
		return;
	}
	FString pantsModel = GetEntity()->GetDefinedProperty(TEXT("pantsModel"));
	ChangePart((int)MODEL_PART_TYPE::MODEL_PART_PANTS, pantsModel);
}

void UModelInterface::OnRep_shoesModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UModelInterface::OnRep_shoesModel : GetEntity()!"));
		return;
	}
	FString shoesModel = GetEntity()->GetDefinedProperty(TEXT("shoesModel"));
	ChangePart((int)MODEL_PART_TYPE::MODEL_PART_SHOES, shoesModel);
}

void UModelInterface::OnRep_necklaceModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UModelInterface::OnRep_necklaceModel : GetEntity()!"));
		return;
	}
	FString necklaceModel = GetEntity()->GetDefinedProperty(TEXT("necklaceModel"));
	ChangePart((int)MODEL_PART_TYPE::MODEL_PART_NECKLACE, necklaceModel);
}

void UModelInterface::OnRep_lringModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UModelInterface::OnRep_lringModel : GetEntity()!"));
		return;
	}
	FString lringModel = GetEntity()->GetDefinedProperty(TEXT("lringModel"));
	ChangePart((int)MODEL_PART_TYPE::MODEL_PART_LHAND_RING, lringModel);
}

void UModelInterface::OnRep_rringModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UModelInterface::OnRep_rringModel : GetEntity()!"));
		return;
	}
	FString rringModel = GetEntity()->GetDefinedProperty(TEXT("rringModel"));
	ChangePart((int)MODEL_PART_TYPE::MODEL_PART_RHAND_RING, rringModel);
}

void UModelInterface::OnRep_weaponModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UModelInterface::OnRep_weaponModel : GetEntity()!"));
		return;
	}
	//武器模型编号配置方式：lweaponModel|rweaponModel
	FString weaponModel = GetEntity()->GetDefinedProperty(TEXT("weaponModel"));
	FString lweaponModel, rweaponModel;
	TArray<FString> weaponModels = UGolbalBPFunctionLibrary::SplitString(weaponModel);
	if (weaponModels.Num() > 0)
	{
		lweaponModel = weaponModels[0];
		if (weaponModels.Num() > 1)
		{
			rweaponModel = weaponModels[1];
		}
	}
	ChangePart((int)MODEL_PART_TYPE::MODEL_PART_LWEAPON, lweaponModel);
	ChangePart((int)MODEL_PART_TYPE::MODEL_PART_RWEAPON, rweaponModel);
}

void UModelInterface::OnRep_suitsModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UModelInterface::OnRep_suitsModel : GetEntity()!"));
		return;
	}
	FString suitsModel = GetEntity()->GetDefinedProperty(TEXT("suitsModel"));
	ChangePart((int)MODEL_PART_TYPE::MODEL_PART_SUITS, suitsModel);
}

void UModelInterface::ChangePart(int equipPos, FString partID)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UModelInterface::ChangePart : GetEntity()!"));
		return;
	}
	FString extraModelNumber = GetEntity()->GetDefinedProperty(TEXT("extraModelNumber"));
	if (!extraModelNumber.IsEmpty())return;

	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(GetActor());
	if (IsValid(ServerCharacter) && ServerCharacter->IsInitialized())
	{
		ServerCharacter->CreateAppearance();						// CST-2145
		//character->GetAppearanceComponent()->ChangePart(MODEL_PART_TYPE(equipPos), partID);
	}	
}

