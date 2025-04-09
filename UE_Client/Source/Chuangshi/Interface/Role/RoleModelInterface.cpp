// Fill out your copyright notice in the Description page of Project Settings.

#include "RoleModelInterface.h"
#include "Actor/Player/PlayerCharacter.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/CS3Debug.h"
#include "GameData/ModelPartData.h"
#include "Component/AppearanceComponent.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3PlayerController.h"

#include "Util/ConvertUtil.h"
CONTROL_COMPILE_OPTIMIZE_START

CS3_BEGIN_INTERFACE_METHOD_MAP(URoleModelInterface, Supper)
CS3_DECLARE_INTERFACE_REMOTE_METHOD(CLIENT_OnReqFaceData, &URoleModelInterface::CLIENT_OnReqFaceData, const FVariant&, const FVariant&)
CS3_END_INTERFACE_METHOD_MAP()

CS3_BEGIN_INTERFACE_PROPERTY_MAP(URoleModelInterface, Supper)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(headAdornModel, &URoleModelInterface::Set_headAdornModel, FString)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(faceAdornModel, &URoleModelInterface::Set_faceAdornModel, FString)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(backAdornModel, &URoleModelInterface::Set_backAdornModel, FString)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(waistAdornModel, &URoleModelInterface::Set_waistAdornModel, FString)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(bodyLightEffect, &URoleModelInterface::Set_bodyLightEffect, FString)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(backAdornParam, &URoleModelInterface::Set_backAdornParam, FString)
CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(colorScheme, &URoleModelInterface::Set_colorScheme, uint8)

CS3_END_INTERFACE_PROPERTY_MAP()

URoleModelInterface::URoleModelInterface()
{
	CachePartChangeData.Empty();
}

URoleModelInterface::~URoleModelInterface()
{
}

void URoleModelInterface::OnRep_headModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_headModel : GetEntity()!"));
		return;
	}
	FString headModel = GetEntity()->GetDefinedProperty(TEXT("headModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_HEADS, headModel);
}

void URoleModelInterface::OnRep_cloakModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_cloakModel : GetEntity()!"));
		return;
	}
	FString cloakModel = GetEntity()->GetDefinedProperty(TEXT("cloakModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_CLOAK, cloakModel);
}

void URoleModelInterface::OnRep_bodyModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_bodyModel : GetEntity()!"));
		return;
	}
	FString bodyModel = GetEntity()->GetDefinedProperty(TEXT("bodyModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_BODYS, bodyModel);
}

void URoleModelInterface::OnRep_hairModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_hairModel : GetEntity()!"));
		return;
	}
	FString hairModel = GetEntity()->GetDefinedProperty(TEXT("hairModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_HAIRS, hairModel);
}

void URoleModelInterface::OnRep_adornModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_adornModel : GetEntity()!"));
		return;
	}
	FString adornModel = GetEntity()->GetDefinedProperty(TEXT("adornModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_ADORN, adornModel);
}

void URoleModelInterface::OnRep_hatModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_hatModel : GetEntity()!"));
		return;
	}
	FString hatModel = GetEntity()->GetDefinedProperty(TEXT("hatModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_HAT, hatModel);
}

void URoleModelInterface::OnRep_coatModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_coatModel: GetEntity()!"));
		return;
	}
	FString coatsModel = GetEntity()->GetDefinedProperty(TEXT("coatModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_COATS, coatsModel);
}

void URoleModelInterface::OnRep_wristModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_wristModel : GetEntity()!"));
		return;
	}
	FString wristModel = GetEntity()->GetDefinedProperty(TEXT("wristModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_WRIST, wristModel);
}

void URoleModelInterface::OnRep_handModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_handModel : GetEntity()!"));
		return;
	}
	FString handModel = GetEntity()->GetDefinedProperty(TEXT("handModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_GLOVES, handModel);//手套
}

void URoleModelInterface::OnRep_waistModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_waistModel : GetEntity()!"));
		return;
	}
	FString waistModel = GetEntity()->GetDefinedProperty(TEXT("waistModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_WAIST, waistModel);
}

void URoleModelInterface::OnRep_pantsModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_pantsModel : GetEntity()!"));
		return;
	}
	FString pantsModel = GetEntity()->GetDefinedProperty(TEXT("pantsModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_PANTS, pantsModel);
}

void URoleModelInterface::OnRep_shoesModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_shoesModel : GetEntity()!"));
		return;
	}
	FString shoesModel = GetEntity()->GetDefinedProperty(TEXT("shoesModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_SHOES, shoesModel);
}

void URoleModelInterface::OnRep_necklaceModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_necklaceModel : GetEntity()!"));
		return;
	}
	FString necklaceModel = GetEntity()->GetDefinedProperty(TEXT("necklaceModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_NECKLACE, necklaceModel);
}

void URoleModelInterface::OnRep_lringModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_lringModel : GetEntity()!"));
		return;
	}
	FString lringModel = GetEntity()->GetDefinedProperty(TEXT("lringModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_LHAND_RING, lringModel);
}

void URoleModelInterface::OnRep_rringModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_rringModel : GetEntity()!"));
		return;
	}
	FString rringModel = GetEntity()->GetDefinedProperty(TEXT("rringModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_RHAND_RING, rringModel);
}

void URoleModelInterface::OnRep_weaponModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_weaponModel : GetEntity()!"));
		return;
	}
	FString nullweaponModel;
	//ChangePart(MODEL_PART_TYPE::MODEL_PART_LWEAPON, nullweaponModel);
	//ChangePart(MODEL_PART_TYPE::MODEL_PART_RWEAPON, nullweaponModel);
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
	ChangePart(MODEL_PART_TYPE::MODEL_PART_LWEAPON, lweaponModel);
	ChangePart(MODEL_PART_TYPE::MODEL_PART_RWEAPON, rweaponModel);
}



void URoleModelInterface::OnRep_suitsModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_suitsModel : GetEntity()!"));
		return;
	}
	FString suitsModel = GetEntity()->GetDefinedProperty(TEXT("suitsModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_SUITS, suitsModel);
}


void URoleModelInterface::OnRep_fabaoModel()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_fabaoModel : GetEntity()!"));
		return;
	}
	FString fabaoModel = GetEntity()->GetDefinedProperty(TEXT("fabaoModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_FABAO, fabaoModel);
}

void URoleModelInterface::Set_headAdornModel(const FString & newVal, const FString & oldVal)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_fabaoModel : GetEntity()!"));
		return;
	}
	FString ModelPartId = GetEntity()->GetDefinedProperty(TEXT("headAdornModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_HEAD_ADORN, ModelPartId);
}

void URoleModelInterface::Set_faceAdornModel(const FString & newVal, const FString & oldVal)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_fabaoModel : GetEntity()!"));
		return;
	}
	FString ModelPartId = GetEntity()->GetDefinedProperty(TEXT("faceAdornModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_FACE_ADORN, ModelPartId);
}

void URoleModelInterface::Set_backAdornModel(const FString & newVal, const FString & oldVal)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_fabaoModel : GetEntity()!"));
		return;
	}
	FString ModelPartId = GetEntity()->GetDefinedProperty(TEXT("backAdornModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_BACK_ADORN, ModelPartId);
}

void URoleModelInterface::Set_waistAdornModel(const FString & newVal, const FString & oldVal)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_fabaoModel : GetEntity()!"));
		return;
	}
	FString ModelPartId = GetEntity()->GetDefinedProperty(TEXT("waistAdornModel"));
	ChangePart(MODEL_PART_TYPE::MODEL_PART_WAIST_ADORN, ModelPartId);
}

void URoleModelInterface::Set_bodyLightEffect(const FString & newVal, const FString & oldVal)
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::OnRep_fabaoModel : GetEntity()!"));
		return;
	}
	FString EffectId = GetEntity()->GetDefinedProperty(TEXT("bodyLightEffect"));
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (!PlayerCharacter || !PlayerCharacter->IsInitialized())
	{
		return;
	}
	PlayerCharacter->ChangeBodyLightEffect(EffectId); 
}

void URoleModelInterface::Set_backAdornParam(const FString& newVal, const FString& oldVal)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (!IsValid(PlayerCharacter) || !GetEntity())
	{
		return;
	}
	//正在改变改观中不要改变单个部件
	if (PlayerCharacter->bIsChangeAppearanceling)
	{
		TWeakObjectPtr<URoleModelInterface> DelayThisPtr(this);
		TWeakObjectPtr<APlayerCharacter> AtrPtr(PlayerCharacter);
		if (Handle.IsValid())
		{
			PlayerCharacter->OnModelChangeAppearanceOverDelegate.Remove(Handle);
			Handle.Reset();
		}
		Handle = PlayerCharacter->OnModelChangeAppearanceOverDelegate.AddLambda([DelayThisPtr, AtrPtr]()
			{
				if (DelayThisPtr.IsValid())
				{
					URoleModelInterface* ThisPtr = DelayThisPtr.Get();
					APlayerCharacter* Player = AtrPtr.Get();
					if (IsValid(ThisPtr) && IsValid(Player))
					{
						ThisPtr->StartSetBackAdornParam();
						Player->OnModelChangeAppearanceOverDelegate.Remove(ThisPtr->Handle);
					}
				}
			});
	}
	else
	{
		StartSetBackAdornParam();
	}
}

void URoleModelInterface::StartSetBackAdornParam()
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (!IsValid(PlayerCharacter) || !GetEntity())
	{
		return;
	}

	FPART_TRANSFORM Transfrom;//此变换的值在SetPartCptTransform会统一计算，这里其实就是通知更新变化
	MODEL_PART_TYPE PartType = MODEL_PART_TYPE::MODEL_PART_BACK_ADORN;
	UMeshComponent* BackAdornCpt = PlayerCharacter->GetPartMeshComponent(PartType);
	PlayerCharacter->GetAppearanceComponent()->SetPartCptTransform(PartType, BackAdornCpt, Transfrom);
}

void URoleModelInterface::Set_colorScheme(const uint8 & newValu, const uint8 & oldVal)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (!IsValid(PlayerCharacter))
	{
		return;
	}
	PlayerCharacter->SetModelColorScheme(newValu);
}

void URoleModelInterface::ChangePart(MODEL_PART_TYPE PartType, FString partID)
{
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(GetActor());
	if (!IsValid(PlayerCharacter) || !PlayerCharacter->IsInitialized())
	{
		return;
	}

	CS3_Warning(TEXT("RoleChangePart.[1](EntityID=%d, PartType=%d,  partID=%s, IsChangeAppearanceling=%d)"), 
		PlayerCharacter->GetSelfEntity()->ID(), int32(PartType), *partID, PlayerCharacter->bIsChangeAppearanceling?1:0);

	//正在改变改观中不要改变单个部件
	if (PlayerCharacter->bIsChangeAppearanceling)
	{
		CachePartChangeData.Add(PartType, partID);

		TWeakObjectPtr<URoleModelInterface> DelayThisPtr(this);
		TWeakObjectPtr<APlayerCharacter> DelayMonsterCharacterPtr(PlayerCharacter);
		if (ChangePartHandle.IsValid())
		{
			PlayerCharacter->OnModelChangeAppearanceOverDelegate.Remove(ChangePartHandle);
			ChangePartHandle.Reset();
		}
		ChangePartHandle = PlayerCharacter->OnModelChangeAppearanceOverDelegate.AddLambda([DelayThisPtr, DelayMonsterCharacterPtr]()
		{
			if (DelayThisPtr.IsValid() && DelayMonsterCharacterPtr.IsValid())
			{
				URoleModelInterface* ThisPtr = DelayThisPtr.Get();
				APlayerCharacter* PlayerCharacter = DelayMonsterCharacterPtr.Get();
				if (!IsValid(ThisPtr) || !IsValid(PlayerCharacter))
				{
					return;
				}

				//下面用的for循环是为了保证顺序，须先更新body部位(主mesh)，以防先更新了子部件出显示问题及崩溃！
				int32 Length = (int32)MODEL_PART_TYPE::MODEL_PART_NUM;
				for (size_t i = 0; i < Length; i++)
				{
					MODEL_PART_TYPE FindPartType = (MODEL_PART_TYPE)i;
					if (ThisPtr->CachePartChangeData.Contains(FindPartType))
					{
						FString FindPartID = *ThisPtr->CachePartChangeData.Find(FindPartType);
						ThisPtr->StartChangePart(FindPartType, FindPartID);
					}
				}
				ThisPtr->CachePartChangeData.Empty();
				PlayerCharacter->OnModelChangeAppearanceOverDelegate.Remove(ThisPtr->ChangePartHandle);
			}
		});
	}
	else
	{
		StartChangePart(PartType, partID);
	}
}

void URoleModelInterface::StartChangePart(MODEL_PART_TYPE PartType, FString partID)
{
	AActor* actor = GetActor();
	APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(actor);
	if (!IsValid(PlayerCharacter))
	{
		return;
	}

	//变身状态下，场景中的主角不能更新，否则因为没插槽导致部件显示错乱
	if (!PlayerCharacter->IsChangeModelState())
	{
		PlayerCharacter->ChangeModelPart(PartType, partID);
	}

	//是否是本地玩家
	if (GetEntity()->IsPlayer())
	{
		CS3_Warning(TEXT("RoleChangePart.[3](EntityID=%d, PartType=%d,  partID=%s)"),
			PlayerCharacter->GetSelfEntity()->ID(), int32(PartType), *partID);
		//更新角色面板主角人物部件(需要判断否则可能主mesh的资源是空的)
		ACS3PlayerController* CS3PlayerController = UGolbalBPFunctionLibrary::GetCS3PlayerController();
		if (!CS3PlayerController->GetRoleModelProxy()->bIsChangeAppearanceling)
		{
			CS3PlayerController->GetRoleModelProxy()->ChangeModelPart(PartType, partID);
		}
	}
}

void URoleModelInterface::ReqFaceModelData()
{
	if (GetEntity() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:URoleModelInterface::GetFaceModelData : GetEntity()!"));
		return;
	}
	KBEngine::FVariantArray args;
	this->GetEntity()->CellCall(TEXT("ReqFaceData"), args);
}

void URoleModelInterface::InitBlueCB()
{
}

void URoleModelInterface::CLIENT_OnReqFaceData(const FVariant& FaceModelData, const FVariant& FaceStyleData)
{
	FaceInfoList faceModel;
	FaceStyle faceStyle;
	FFACE_STYLE_DATA faceStyleDatas;
	FaceInfoList::CreateFromVariant(FaceModelData, faceModel);
	FaceStyle::CreateFromVariant(FaceStyleData, faceStyle);
	TArray<TMap<FString, FString>> Bonedatas;
	TArray<FString> boneNames;
	TArray<FString> boneDatas;
	for (FaceInfo faceinfo : faceModel.infolist)
	{
		boneNames.Add(faceinfo.boneName);
		boneDatas.Add(faceinfo.boneData);
	}
	faceStyleDatas.ChunZhuangIndex = faceStyle.ChunzhuangIndex;
	faceStyleDatas.ChunZhuangShape = FSTRING_TO_FLOAT(faceStyle.ChunzhuangShape);
	faceStyleDatas.HuXuIndex = faceStyle.HuXuIndex;
	faceStyleDatas.LianWenIndex = faceStyle.LianWenIndex;
	faceStyleDatas.MeiMaoIndex = faceStyle.MeiMaoIndex;
	faceStyleDatas.MeiMaoShape = FSTRING_TO_FLOAT(faceStyle.MeiMaoShape);
	faceStyleDatas.YanXianIndex = faceStyle.YanXianIndex;
	faceStyleDatas.SaiHongIndex = faceStyle.SaiHongIndex;
	faceStyleDatas.SaiHongShape = FSTRING_TO_FLOAT(faceStyle.SaiHongShape);
	faceStyleDatas.YanYingIndex = faceStyle.YanYingIndex;
	faceStyleDatas.YanYingShape = FSTRING_TO_FLOAT(faceStyle.YanYingShape);
	faceStyleDatas.Brighjtness = FSTRING_TO_FLOAT(faceStyle.Brightness);
	faceStyleDatas.ColorDepth = FSTRING_TO_FLOAT(faceStyle.ColorDepth);
	faceStyleDatas.EyeIndex = faceStyle.EyeIndex;
	faceStyleDatas.EyeScale = FSTRING_TO_FLOAT(faceStyle.EyeScale);


	OnReqFaceModelData(boneNames, boneDatas, faceStyleDatas);
}

CONTROL_COMPILE_OPTIMIZE_END
