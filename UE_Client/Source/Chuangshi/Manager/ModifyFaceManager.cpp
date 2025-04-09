// Fill out your copyright notice in the Description page of Project Settings.

#include "ModifyFaceManager.h"
#include"Chuangshi.h"

#if PLATFORM_WINDOWS
#include "WindowsApplication.h"
#include <Commdlg.h>
#endif
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/CfgManager.h"
#include "FileManagerGeneric.h"
#include "Kismet/GameplayStatics.h"
#include "Actor/Player/ModifyfaceSaveActor.h"
#include "SaveGameSystem.h"
#include "PlatformFeatures.h"
#include "ObjectAndNameAsStringProxyArchive.h"
#include "Component/AppearanceComponent.h"
#include "Kismet/KismetStringLibrary.h"

#pragma optimize("", off)


static const int CS3_SAVEGAME_FILE_TYPE_TAG = 0x53415647;		// "sAvG"

struct FCS3_SaveGameFileVersion
{
	enum Type
	{
		InitialVersion = 1,
		// serializing custom versions into the savegame data to handle that type of versioning
		AddedCustomVersions = 2,

		// -----<new versions can be added above this line>-------------------------------------------------
		VersionPlusOne,
		LatestVersion = VersionPlusOne - 1
	};
};


struct FCS3_SaveGameHeader
{
	FCS3_SaveGameHeader();
	FCS3_SaveGameHeader(TSubclassOf<USaveGame> ObjectType);

	void Empty();
	bool IsEmpty() const;

	void Read(FMemoryReader& MemoryReader);
	void Write(FMemoryWriter& MemoryWriter);

	int32 FileTypeTag;
	int32 SaveGameFileVersion;
	int32 PackageFileUE4Version;
	FEngineVersion SavedEngineVersion;
	int32 CustomVersionFormat;
	FCustomVersionContainer CustomVersions;
	FString SaveGameClassName;
};

FCS3_SaveGameHeader::FCS3_SaveGameHeader()
	:FileTypeTag(0)
	, SaveGameFileVersion(0)
 	, PackageFileUE4Version(0)
 	, CustomVersionFormat(static_cast<int32>(ECustomVersionSerializationFormat::Unknown))
{}

FCS3_SaveGameHeader::FCS3_SaveGameHeader(TSubclassOf<USaveGame> ObjectType)
	: FileTypeTag(CS3_SAVEGAME_FILE_TYPE_TAG)
	, SaveGameFileVersion(FCS3_SaveGameFileVersion::LatestVersion)
	, PackageFileUE4Version(GPackageFileUE4Version)
	, SavedEngineVersion(FEngineVersion::Current())
	, CustomVersionFormat(static_cast<int32>(ECustomVersionSerializationFormat::Latest))
	, CustomVersions(FCustomVersionContainer::GetRegistered())
	, SaveGameClassName(ObjectType->GetPathName())
{}
 
void FCS3_SaveGameHeader::Empty()
{
	FileTypeTag = 0;
	SaveGameFileVersion = 0;
	PackageFileUE4Version = 0;
	SavedEngineVersion.Empty();
	CustomVersionFormat = (int32)ECustomVersionSerializationFormat::Unknown;
	CustomVersions.Empty();
	SaveGameClassName.Empty();
}

bool FCS3_SaveGameHeader::IsEmpty() const
{
	return (FileTypeTag == 0);
}

void FCS3_SaveGameHeader::Read(FMemoryReader& MemoryReader)
{
	Empty();

	MemoryReader << FileTypeTag;

	if (FileTypeTag != CS3_SAVEGAME_FILE_TYPE_TAG)
	{
		// this is an old saved game, back up the file pointer to the beginning and assume version 1
		MemoryReader.Seek(0);
		SaveGameFileVersion = FCS3_SaveGameFileVersion::InitialVersion;

		// Note for 4.8 and beyond: if you get a crash loading a pre-4.8 version of your savegame file and 
		// you don't want to delete it, try uncommenting these lines and changing them to use the version 
		// information from your previous build. Then load and resave your savegame file.
		//MemoryReader.SetUE4Ver(MyPreviousUE4Version);				// @see GPackageFileUE4Version
		//MemoryReader.SetEngineVer(MyPreviousEngineVersion);		// @see FEngineVersion::Current()
	}
	else
	{
		// Read version for this file format
		MemoryReader << SaveGameFileVersion;

		// Read engine and UE4 version information
		MemoryReader << PackageFileUE4Version;

		MemoryReader << SavedEngineVersion;

		MemoryReader.SetUE4Ver(PackageFileUE4Version);
		MemoryReader.SetEngineVer(SavedEngineVersion);

		if (SaveGameFileVersion >= FCS3_SaveGameFileVersion::AddedCustomVersions)
		{
			MemoryReader << CustomVersionFormat;

			CustomVersions.Serialize(MemoryReader, static_cast<ECustomVersionSerializationFormat::Type>(CustomVersionFormat));
			MemoryReader.SetCustomVersions(CustomVersions);
		}
	}

	// Get the class name
	MemoryReader << SaveGameClassName;
}

void FCS3_SaveGameHeader::Write(FMemoryWriter& MemoryWriter)
{
	// write file type tag. identifies this file type and indicates it's using proper versioning
	// since older UE4 versions did not version this data.
	MemoryWriter << FileTypeTag;

	// Write version for this file format
	MemoryWriter << SaveGameFileVersion;

	// Write out engine and UE4 version information
	MemoryWriter << PackageFileUE4Version;
	MemoryWriter << SavedEngineVersion;

	// Write out custom version data
	MemoryWriter << CustomVersionFormat;
	CustomVersions.Serialize(MemoryWriter, static_cast<ECustomVersionSerializationFormat::Type>(CustomVersionFormat));

	// Write the class name so we know what class to load to
	MemoryWriter << SaveGameClassName;
}


UModifyFaceManager::UModifyFaceManager()
{

}

UModifyFaceManager* UModifyFaceManager::GetInstance()
{
	cs3_checkNoReentry();
	return NewObject<UModifyFaceManager>();
}

void UModifyFaceManager::SetBoneRef(AGameCharacter* Actor)
{
	if (BoneDataTable)
	{
		FaceBoneRef.Empty();
		TArray<FMODIFY_FACE_DATA*> BoneStructData;
		BoneDataTable->GetAllRows(BoneStructData);

		for (auto Bone : BoneStructData)
		{
			//CST-13795
			if (Bone == nullptr) continue;
			USkeletalMeshComponent* HeadMeshCpt = Cast<USkeletalMeshComponent>(Actor->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_HEADS));
			int32 BoneIndex = HeadMeshCpt->GetBoneIndex(Bone->BoneName);
			if (BoneIndex > -1)
			{
				Bone->BoneIndex = BoneIndex;
				FaceBoneRef.Add(*Bone);
			}
		}
	}
	FaceBoneRef.Sort([](const FMODIFY_FACE_DATA& A, const FMODIFY_FACE_DATA& B)
	{
		return A.BoneIndex < B.BoneIndex;
	});
	BodyBoneRef.Sort([](const FMODIFY_FACE_DATA& A, const FMODIFY_FACE_DATA& B)
	{
		return A.BoneIndex < B.BoneIndex;
	});
	if (BoneLimitTable)
	{
		TArray<FBONE_FACE_LIMIT*> BoneLimitData;
		BoneLimitTable->GetAllRows(BoneLimitData);
		for (auto BoneLimit : BoneLimitData)
			BoneLimitRef.Add(*BoneLimit);
	}
	Actor->ModifyFaceDatas = FaceBoneRef;
	Actor->bIsGetBone = bIsGetBone;
	bIsGetBone = true;
}

void UModifyFaceManager::SetBoneTrans(AGameCharacter* GameActor, FName BoneName, bool bIsSymBone, FTransform BoneTrans, bool IsMouse)
{
	if (!GameActor->IsValidLowLevel())return;
	if (BoneName.IsNone())
	{
		if (CurrentBone)
		{
			TArray<FMODIFY_FACE_DATA>& Bones = GameActor->ModifyFaceDatas;

			for (FMODIFY_FACE_DATA facedata : Bones)
			{
				if (facedata.BoneName.IsEqual( CurrentBone->BoneName))
				{
					SetBoneTrans(GameActor, facedata.BoneName, bIsSymBone, BoneTrans);
				}
			}
			if (CurrentBone->SymName.ToString() != "None")
			{
				FName boneName = CurrentBone->SymName;
				TArray<FMODIFY_FACE_DATA>& BoneArray = GetBoneReference(0);
				FMODIFY_FACE_DATA* bone = BoneArray.FindByPredicate([boneName](FMODIFY_FACE_DATA& a) {return a.BoneName == boneName; });
				if (bone)
					SymBone = bone;
			}
			else
			{
				SymBone = nullptr;
			}	
		}
		if (bIsSymBone && SymBone)
		{	
			TArray<FMODIFY_FACE_DATA>& Bones = GameActor->ModifyFaceDatas;
			for (FMODIFY_FACE_DATA facedata : Bones)
			{
				if (facedata.BoneName.IsEqual(SymBone->BoneName))
				{
					FTransform SymTrans = SymBoneTrans(BoneTrans);
					SetBoneTrans(GameActor, facedata.BoneName, bIsSymBone, SymTrans);
				}
			}
		}
	}
	else
	{
		auto DataTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_MODIFY_FACE__DATA);
		FMODIFY_FACE_DATA* BoneLimit = const_cast<FMODIFY_FACE_DATA*>(DataTable->GetRow<FMODIFY_FACE_DATA>(BoneName));
		if (BoneLimit)
		{
			TArray<FMODIFY_FACE_DATA>& BoneArray = GameActor->ModifyFaceDatas;
			if (BoneArray.Num() < 0)return;
			int32 Index = BoneLimit->Index;
			FMODIFY_FACE_DATA* Bone = BoneArray.FindByPredicate([Index](FMODIFY_FACE_DATA& a) {return a.Index == Index; });
			if (Bone)
			{
				if (IsMouse)
				{
					Bone->BoneTrans *= BoneTrans;
				}
				else
				{
					Bone->BoneTrans = BoneTrans;
				}

				LimitBoneTrans(Bone, 0);
			}
		}
	}

}

void UModifyFaceManager::SetTouchBone(int32 Index, int32 ModifyType /*= 0/*EModifyType Type = EModifyType::Part_Face*/)
{
	bool bIsExist = false;
	TArray<FMODIFY_FACE_DATA>& BoneArray = GetBoneReference(ModifyType);
	if (BoneArray.Num() > 0)
	{
		FMODIFY_FACE_DATA* Bone = BoneArray.FindByPredicate([Index](FMODIFY_FACE_DATA& a) {return a.Index == Index; });
		if (Bone)
		{
			TouchBone = Bone;
			bIsExist = true;
		}
	}
	if (!bIsExist)
		TouchBone = nullptr;
}

void UModifyFaceManager::LimitBoneTrans(FMODIFY_FACE_DATA* Bone, int32 ModifyType)
{
	auto DataTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_BONE_FACE_LIMIT_DATA);
	const FBONE_FACE_LIMIT* BoneLimit = DataTable->GetRow<FBONE_FACE_LIMIT>(Bone->BoneName);
	FVector Loc = Bone->BoneTrans.GetLocation();
	FVector Scal = Bone->BoneTrans.GetScale3D();
	FRotator Rot = Bone->BoneTrans.Rotator();

	if (BoneLimit)
	{
		FTransform MinLimitBone = BoneLimit->MinTransform;
		FTransform MaxLimitBone = BoneLimit->MaxTransform;

		if (BoneLimit->doTranslation)
		{
			Loc.X = FMath::Clamp(Loc.X, MinLimitBone.GetTranslation().X, MaxLimitBone.GetTranslation().X);
			Loc.Y = FMath::Clamp(Loc.Y, MinLimitBone.GetTranslation().Y, MaxLimitBone.GetTranslation().Y);
			Loc.Z = FMath::Clamp(Loc.Z, MinLimitBone.GetTranslation().Z, MaxLimitBone.GetTranslation().Z);
		}
		else
			Loc = FVector(0.0f, 0.0f, 0.0f);
		if (BoneLimit->doScaling)
		{
			if (ModifyType == 0)
			{
				Scal.X = FMath::Clamp(Scal.X, MinLimitBone.GetScale3D().X, MaxLimitBone.GetScale3D().X);
				Scal.Y = FMath::Clamp(Scal.Y, MinLimitBone.GetScale3D().Y, MaxLimitBone.GetScale3D().Y);
				Scal.Z = FMath::Clamp(Scal.Z, MinLimitBone.GetScale3D().Z, MaxLimitBone.GetScale3D().Z);
			}
			else
			{
			/// 因当前没有捏造身体数据 留空 
			}
		}
		else
			Scal = FVector(1.0f, 1.0f, 1.0f);
		if (BoneLimit->doScaling)
		{
			Rot.Yaw = FMath::Clamp(Rot.Yaw, MinLimitBone.Rotator().Yaw, MaxLimitBone.Rotator().Yaw);
			Rot.Pitch = FMath::Clamp(Rot.Pitch, MinLimitBone.Rotator().Pitch, MaxLimitBone.Rotator().Pitch);
			Rot.Roll = FMath::Clamp(Rot.Roll, MinLimitBone.Rotator().Roll, MaxLimitBone.Rotator().Roll);
		}
		else
			Rot = FRotator(0.0f, 0.0f, 0.0f);
	}

	else
	{
		Loc = FVector(0.0f, 0.0f, 0.0f);
		Scal = FVector(1.0f, 1.0f, 1.0f);
		Rot = FRotator(0.0f, 0.0f, 0.0f);
	}

	Bone->BoneTrans.SetLocation(Loc);
	Bone->BoneTrans.SetRotation(FQuat(Rot));
	Bone->BoneTrans.SetScale3D(Scal);
}

FTransform UModifyFaceManager::SymBoneTrans(FTransform BoneTrans)
{
	FTransform SymTrans = BoneTrans;
	FVector Loc = BoneTrans.GetLocation();
	Loc.X = -Loc.X;
	SymTrans.SetTranslation(Loc);

	FRotator Rot = BoneTrans.Rotator();
	Rot.Pitch = -Rot.Pitch;
	Rot.Yaw = -Rot.Yaw;
	SymTrans.SetRotation(FQuat(Rot));

	return SymTrans;
}

FName UModifyFaceManager::GetCurrentBoneName() const
{
	if (CurrentBone)
		return CurrentBone->BoneName;
	else
		return "None";
}

void UModifyFaceManager::SetCurrentBone()
{
	CurrentBone = TouchBone;
	if (CurrentBone)
	{
		if (CurrentBone->SymName.ToString() != "None")
		{
			FName BoneName = CurrentBone->SymName;
			TArray<FMODIFY_FACE_DATA>& BoneArray = GetBoneReference(0);
			FMODIFY_FACE_DATA* bone = BoneArray.FindByPredicate([BoneName](FMODIFY_FACE_DATA& a) {return a.BoneName == BoneName; });
			if (bone)
				SymBone = bone;
		}
		else
			SymBone = nullptr;
	}
}

void UModifyFaceManager::SetModifyData()
{
	const auto ModifyFaceTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_MODIFY_FACE__DATA);
	BoneDataTable = const_cast<UConfigTable*>(ModifyFaceTable);

	const auto BoneLimitTTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_BONE_FACE_LIMIT_DATA);
	BoneLimitTable = const_cast<UConfigTable*>(BoneLimitTTable);
}

TArray<FMODIFY_FACE_DATA>& UModifyFaceManager::GetBoneReference(int32 ModifyType /*= 0/*EModifyType Type = EModifyType::Part_Face*/)
{
	return FaceBoneRef;
}

FName UModifyFaceManager::GetTouchBoneName() const
{
	if (TouchBone)
		return TouchBone->BoneName;
	else
		return "None";
}

FString UModifyFaceManager::SaveFileData(FString name)
{
#if PLATFORM_WINDOWS
	FString Title("Choose a facedata file");
	FString Catalog = FPaths::GetPath(FPaths::GetProjectFilePath()) + "/Saved";
	Catalog = UKismetStringLibrary::Replace(Catalog, ":/", ":\\");
	Catalog = UKismetStringLibrary::Replace(Catalog, "/", "\\");
	IPlatformFile& PlatformFile = FPlatformFileManager::Get().GetPlatformFile();
	if (!PlatformFile.DirectoryExists(*Catalog))
	{
		PlatformFile.CreateDirectory(*Catalog);
		if (!PlatformFile.DirectoryExists(*Catalog))
		{
			CS3_Display(CS3DebugType::CL_GM, TEXT("CS3_CreateFile ------ false"));
		}
	}
	OPENFILENAME ofn;
	ZeroMemory(&ofn, sizeof(ofn));
	ofn.lStructSize = sizeof(ofn);
	const TCHAR* FileName = *name;
	ofn.lpstrFile = name.GetCharArray().GetData();
	ofn.nMaxFile = MAX_PATH;
	ofn.lpstrTitle = Title.GetCharArray().GetData();
	ofn.lpstrFilter = TEXT("FaceData Files (*.sav)\0*.sav\0All Files\0*.*\0\0");
	ofn.lpstrInitialDir = Catalog.GetCharArray().GetData();
	
	ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST;
 	if (GetSaveFileName(&ofn))
 	{
 		if (_tcslen(FileName) != 0)
		{
			FString FliePath = FileName;
			FliePath.Append(".sav");
			if (UModifyfaceSaveActor* SaveGameObject = Cast<UModifyfaceSaveActor>(UGameplayStatics::CreateSaveGameObject(UModifyfaceSaveActor::StaticClass())))
			{
				SaveGameObject->ModifyFaceDatas = GetModifyFaceActor()->ModifyFaceDatas;
				SaveGameObject->FaceStyleDatas = GetModifyFaceActor()->FaceStyleDatas;
				SaveGameObject->partMesh = GetModifyFaceActor()->GetAppearanceComponent()->GetPartMap();

				ISaveGameSystem* SaveSystem = IPlatformFeaturesModule::Get().GetSaveGameSystem();
				// If we have a system and an object to save and a save name...
				if (SaveSystem && SaveGameObject)
				{
					TArray<uint8> ObjectBytes;
					FMemoryWriter MemoryWriter(ObjectBytes, true);

					FCS3_SaveGameHeader SaveHeader(SaveGameObject->GetClass());
					SaveHeader.Write(MemoryWriter);

					// Then save the object state, replacing object refs and names with strings
					FObjectAndNameAsStringProxyArchive Ar(MemoryWriter, false);
					SaveGameObject->Serialize(Ar);
					
					if (FFileHelper::SaveArrayToFile(ObjectBytes, *FliePath))
					{
						return FileName;
					}
				}
			}
 		}
 	}
 #endif

	return FString();

}

FString UModifyFaceManager::LoadFileData()
{
#if PLATFORM_WINDOWS
	FString Title("Choose a facedata file");
	OPENFILENAME ofn;
	ZeroMemory(&ofn, sizeof(ofn));
	TCHAR* FileName = new TCHAR[MAX_PATH];

	ofn.lStructSize = sizeof(ofn);
	ofn.lpstrFile = FileName;
	ofn.lpstrFile[0] = '\0';
	ofn.nMaxFile = MAX_PATH;
	ofn.lpstrTitle = Title.GetCharArray().GetData();
	ofn.lpstrFilter = TEXT("FaceData Files (*.sav)\0*.sav\0All Files\0*.*\0\0");
	ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST;
	if (GetOpenFileName(&ofn))
	{
		if (_tcslen(FileName) != 0)
		{
			ISaveGameSystem* SaveSystem = IPlatformFeaturesModule::Get().GetSaveGameSystem();
			if (SaveSystem)
			{
				TArray<uint8> ObjectBytes;

				if (FFileHelper::LoadFileToArray(ObjectBytes, FileName))
				{
					if (UModifyfaceSaveActor * LoadedGame = Cast<UModifyfaceSaveActor>(UGameplayStatics::LoadGameFromMemory(ObjectBytes)))
					{
						///设置脸部骨骼数据
						FaceBoneRef = LoadedGame->ModifyFaceDatas;
						for (int32 i = 0; i < FaceBoneRef.Num(); ++i)
						{
							SetBoneTrans(GetModifyFaceActor(), FaceBoneRef[i].BoneName, true, FaceBoneRef[i].BoneTrans);
						}
						///设置脸部样式数据
						GetModifyFaceActor()->FaceStyleDatas = LoadedGame->FaceStyleDatas;
						SetModelFaceStyle(GetModifyFaceActor(), GetModifyFaceActor()->FaceStyleDatas);

						for (auto RemovePart : LoadedGame->partMesh)
						{
							if (!RemovePart.Value.IsEmpty())
							{
								GetModifyFaceActor()->ModifyFaceChangePart(RemovePart.Key, RemovePart.Value);
							}
						}
					}
				}
			}
		}
	}
	return FileName;
#endif
}

bool UModifyFaceManager::GetFinishState()
{
	return bIsGetBone;
}

void UModifyFaceManager::ResetFileData(AGameCharacter* GameActor)
{
	TArray<FMODIFY_FACE_DATA>& BoneArray = GameActor->ModifyFaceDatas;
	TArray<FMODIFY_FACE_DATA*> BoneDatas;
	BoneDataTable->GetAllRows(BoneDatas);
	for (FMODIFY_FACE_DATA& bone : GameActor->ModifyFaceDatas)
	{
		bone.BoneTrans = FTransform(FRotator::ZeroRotator, FVector::ZeroVector, FVector::OneVector);
	}
}

TArray<FString> UModifyFaceManager::GetFaceFileName()
{
	TArray<FString> FileNames;
	FString Catalog = FPaths::GetPath(FPaths::GetProjectFilePath()) + "/Saved" + "/FileTeture";
	FString FileExtension ="";
	FFileManagerGeneric::Get().FindFiles(FileNames, *Catalog, *FileExtension);
	return FileNames;

}

AModifyFaceCharacter* UModifyFaceManager::GetModifyFaceActor()
{
	TArray<AActor*> Actors;
	UGameplayStatics::GetAllActorsOfClass(this,AModifyFaceCharacter::StaticClass(), Actors);
	AModifyFaceCharacter* ModifyFaceCharacter = Cast<AModifyFaceCharacter>(Actors[0]);
	return ModifyFaceCharacter;
}

void UModifyFaceManager::SetModelFaceStyle(AGameCharacter* Target, FFACE_STYLE_DATA faceStyleData)
{
	if (IsValid(Target))
	{
		USkeletalMeshComponent* HeadMeshCpt = Cast<USkeletalMeshComponent>(Target->GetPartMeshComponent(MODEL_PART_TYPE::MODEL_PART_HEADS));
		HeadMeshCpt->SetScalarParameterValueOnMaterials(TEXT("ChunZhuangIndex"), faceStyleData.ChunZhuangIndex);
		HeadMeshCpt->SetScalarParameterValueOnMaterials(TEXT("ChunZhuangShape"), faceStyleData.ChunZhuangShape);
		HeadMeshCpt->SetScalarParameterValueOnMaterials(TEXT("HuXuIndex"), faceStyleData.HuXuIndex);
		HeadMeshCpt->SetScalarParameterValueOnMaterials(TEXT("LianWenIndex"), faceStyleData.LianWenIndex);
		HeadMeshCpt->SetScalarParameterValueOnMaterials(TEXT("MeiMaoIndex"), faceStyleData.MeiMaoIndex);
		HeadMeshCpt->SetScalarParameterValueOnMaterials(TEXT("MeiMaoShape"), faceStyleData.MeiMaoShape);
		HeadMeshCpt->SetScalarParameterValueOnMaterials(TEXT("YanXianIndex"), faceStyleData.YanXianIndex);
		HeadMeshCpt->SetScalarParameterValueOnMaterials(TEXT("SaiHongIndex"), faceStyleData.SaiHongIndex);
		HeadMeshCpt->SetScalarParameterValueOnMaterials(TEXT("SaiHongShape"), faceStyleData.SaiHongShape);
		HeadMeshCpt->SetScalarParameterValueOnMaterials(TEXT("YanYingIndex"), faceStyleData.YanYingIndex);
		HeadMeshCpt->SetScalarParameterValueOnMaterials(TEXT("YanYingShape"), faceStyleData.YanYingShape);
		HeadMeshCpt->SetScalarParameterValueOnMaterials(TEXT("Brighjtness"), faceStyleData.Brighjtness);
		HeadMeshCpt->SetScalarParameterValueOnMaterials(TEXT("ColorDepth"), faceStyleData.ColorDepth);
		HeadMeshCpt->SetScalarParameterValueOnMaterials(TEXT("Eyes_TexIrisIndex"), faceStyleData.EyeIndex);
	}
}

void UModifyFaceManager::SetActorFaceData(AGameCharacter* Target, TArray<FMODIFY_FACE_DATA> ModifyFaceDatas, FFACE_STYLE_DATA FaceStyleDatas)
{
	for (FMODIFY_FACE_DATA data : ModifyFaceDatas)
	{
		SetBoneTrans(Target, data.BoneName, false, data.BoneTrans);
	}
	SetModelFaceStyle(Target, FaceStyleDatas);
}

bool UModifyFaceManager::SerialzeData(FString DataPath)
{
	if (DataPath == "")
		return false;

	FBufferArchive ToBinary;
	//ToBinary << FaceBoneRef;
	AModifyFaceCharacter* ModifyFaceCharacter= GetModifyFaceActor();
	if (!IsValid(ModifyFaceCharacter))
	{
		return false;
	}
	//捏脸骨骼数据
	for (int32 i = 0; i < FaceBoneRef.Num(); ++i)
	{
		ToBinary << ModifyFaceCharacter->ModifyFaceDatas[i].BoneIndex;
		ToBinary << ModifyFaceCharacter->ModifyFaceDatas[i].BoneName;
		ToBinary << ModifyFaceCharacter->ModifyFaceDatas[i].BoneTrans;
		ToBinary << ModifyFaceCharacter->ModifyFaceDatas[i].SymName;
		ToBinary << ModifyFaceCharacter->ModifyFaceDatas[i].Index;
	}
	//脸部样式数据
	ToBinary << ModifyFaceCharacter->FaceStyleDatas.ChunZhuangIndex;
	ToBinary << ModifyFaceCharacter->FaceStyleDatas.ChunZhuangShape;
	ToBinary << ModifyFaceCharacter->FaceStyleDatas.HuXuIndex;
	ToBinary << ModifyFaceCharacter->FaceStyleDatas.LianWenIndex;
	ToBinary << ModifyFaceCharacter->FaceStyleDatas.MeiMaoIndex;
	ToBinary << ModifyFaceCharacter->FaceStyleDatas.MeiMaoShape;
	ToBinary << ModifyFaceCharacter->FaceStyleDatas.YanXianIndex;
	ToBinary << ModifyFaceCharacter->FaceStyleDatas.SaiHongIndex;
	ToBinary << ModifyFaceCharacter->FaceStyleDatas.SaiHongShape;
	ToBinary << ModifyFaceCharacter->FaceStyleDatas.YanYingIndex;
	ToBinary << ModifyFaceCharacter->FaceStyleDatas.YanYingShape;
	ToBinary << ModifyFaceCharacter->FaceStyleDatas.Brighjtness;
	ToBinary << ModifyFaceCharacter->FaceStyleDatas.ColorDepth;
	ToBinary << ModifyFaceCharacter->FaceStyleDatas.EyeIndex;
	ToBinary << ModifyFaceCharacter->FaceStyleDatas.EyeScale;
	if (ToBinary.Num() <= 0)
		return false;

	// 保存到硬盘
	bool bResult = FFileHelper::SaveArrayToFile(ToBinary, *DataPath);

	// 清空 buffer
	ToBinary.FlushCache();
	ToBinary.Empty();

	return bResult;
}

bool UModifyFaceManager::DeserialzeData(FString DataPath)
{ 
	if (DataPath == "")
		return false;

	TArray<uint8> BinaryArray;

	// 从硬盘中加载数据
	if (!FFileHelper::LoadFileToArray(BinaryArray, *DataPath))
		return false;

	// 读取加载出来的文件数据
	FMemoryReader FromBinary = FMemoryReader(BinaryArray, true);
	FromBinary.Seek(0);
	//FromBinary << FaceBoneRef;
	for (int32 i = 0; i < FaceBoneRef.Num(); ++i)
	{
		FromBinary << FaceBoneRef[i].BoneIndex;
		FromBinary << FaceBoneRef[i].BoneName;
		FromBinary << FaceBoneRef[i].BoneTrans;
		FromBinary << FaceBoneRef[i].SymName;
		FromBinary << FaceBoneRef[i].Index;
		SetBoneTrans( GetModifyFaceActor(),FaceBoneRef[i].BoneName,true, FaceBoneRef[i].BoneTrans);
	}	
	FromBinary << GetModifyFaceActor()->FaceStyleDatas.ChunZhuangIndex;
	FromBinary << GetModifyFaceActor()->FaceStyleDatas.ChunZhuangShape;
	FromBinary << GetModifyFaceActor()->FaceStyleDatas.HuXuIndex;
	FromBinary << GetModifyFaceActor()->FaceStyleDatas.LianWenIndex;
	FromBinary << GetModifyFaceActor()->FaceStyleDatas.MeiMaoIndex;
	FromBinary << GetModifyFaceActor()->FaceStyleDatas.MeiMaoShape;
	FromBinary << GetModifyFaceActor()->FaceStyleDatas.YanXianIndex;
	FromBinary << GetModifyFaceActor()->FaceStyleDatas.SaiHongIndex;
	FromBinary << GetModifyFaceActor()->FaceStyleDatas.SaiHongShape;
	FromBinary << GetModifyFaceActor()->FaceStyleDatas.YanYingIndex;
	FromBinary << GetModifyFaceActor()->FaceStyleDatas.YanYingShape;
	FromBinary << GetModifyFaceActor()->FaceStyleDatas.Brighjtness;
	FromBinary << GetModifyFaceActor()->FaceStyleDatas.ColorDepth;
	FromBinary << GetModifyFaceActor()->FaceStyleDatas.EyeIndex;
	FromBinary << GetModifyFaceActor()->FaceStyleDatas.EyeScale;

	SetModelFaceStyle(GetModifyFaceActor(), GetModifyFaceActor()->FaceStyleDatas);

	// 清空buffer
	FromBinary.FlushCache();
	BinaryArray.Empty();
	// 关闭流
	FromBinary.Close();

	return true;

}
#pragma optimize("", on)