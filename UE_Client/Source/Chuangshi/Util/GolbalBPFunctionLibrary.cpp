// Fill out your copyright notice in the Description page of Project Settings.
#include "Util/GolbalBPFunctionLibrary.h"
// UE4
#include "DelayAction.h"
#include "Internationalization/Regex.h"
#include "FileManagerGeneric.h"
#include "Engine/UserInterfaceSettings.h"
#include "Component/SpringArmComponentEX.h"
#include "WidgetComponent.h"
#include "Camera/CameraComponent.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Kismet/KismetMathLibrary.h"
#include "Kismet/GameplayStatics.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Kismet/KismetTextLibrary.h"
#include "AssetRegistryModule.h"
#include "ModuleManager.h"
#include "AIModule/Classes/AIController.h"
#include "NavigationSystem/Public/NavigationSystem.h"
#include "NavigationSystem/Public/NavigationPath.h"
#include "Navigation/PathFollowingComponent.h"
#include "Kismet/KismetStringLibrary.h"
#if WITH_EDITOR
#include "DesktopPlatformModule.h"
#endif
// CS3
#include "Actor/ServerCharacter.h"
#include "Actor/Player/PlayerCharacter.h"
#include "Actor/NPC/ClientGameCharacter.h"
#include "Actor/Particle/EffectEmitter.h"
#include "Component/AppearanceComponent.h"
#include "GameData/GameDefault.h"
#include "GameData/Chinese.h"
#include "GameData/StrToClass.h"
#include "GameData/Item/ItemFactory.h"
#include "GameData/SpawnTransform.h"
#include "GameData/TexturePath.h"
#include "CS3Base/CS3Entity.h"
#include "CS3Base/GameObject.h"
#include "CS3Base/UIManager.h"
#include "CS3Base/UIDockManager.h"
#include "Interface/StatusMessageInterface.h"
#include "GameDevelop/CS3PlayerController.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/ConvertUtil.h"
#include "Util/CS3Algorithms.h"
#include "Util/ImageLoader.h"
#include "Manager/ResourceManager.h"
#include "Manager/LoginManager.h"
#include "Manager/StoryManager.h"
#include "Manager/ParticleManager.h"
#include "Manager/ActionManager.h"
#include "Manager/LevelManager.h"
#include "Manager/MessageManager.h"
#include "Manager/AudioManager.h"
#include "Manager/LocalDataSaveManager.h"
#include "Manager/CustomCursorManager.h"
#include "Manager/MapManager.h"
#include "Manager/QuestManager.h"
#include "Manager/LoaderManager.h"
#include "Manager/VisibleManager.h"
#include "Manager/EventManager.h"
#include "Manager/TipsManager.h"
#include "Manager/EmoteManager.h"
#include "Manager/DecalManager.h"
#include "Manager/TextParseManager.h"
#include "Manager/ForceManager.h"
#include "Manager/TutorialManager.h"
#include "Manager/Operation/ControllerModeMgr.h"
#include "Manager/Operation/OperationModeMgr.h"
#include "Manager/TimeManager.h"
#include "Manager/AutoFightMar.h"
#include "Manager/MediaPlayerManager.h"
#include "Manager/SkillManager.h"
#include "Manager/MotionBlurManager.h"
#include "Manager/CustomTimerManager.h"
#include "Manager/GameplayEventManager.h"
#include "GameData/ConstData.h"
#include "GameData/ProfessionData.h"
#include "Actor/Scene/MovingPlatformCharacter.h"

#include "AllowWindowsPlatformTypes.h"
#include <windows.h> ///<使用windowsAPI 详见GetMouseMoveSpeed()函数

#include "EngineUtils.h"
#include "HideWindowsPlatformTypes.h"
#include "Components/CapsuleComponent.h"
#include "Entity/Role/CS3Role.h"
#include "GameData/EnumCsvDefine.h"
#include "NoExportTypes.h"
#include "Engine/Texture2D.h"
#include "GameData/LevelHashMap.h"
#include "GameData/MinimapData.h"
#include "Kismet/KismetStringLibrary.h"
#include "PaperFlipbook.h"
#include "JsonReader.h"
#include "JsonSerializer.h"
#include "JsonObject.h"
#include "Engine/TextureRenderTarget2D.h"
#include "ImageUtils.h"
#include "IImageWrapperModule.h"
#include "IImageWrapper.h"
#include "GameFramework/SaveGame.h"
#include "SaveGameSystem.h"
#include "ObjectAndNameAsStringProxyArchive.h"
#include "PlatformFeatures.h"
#include "SharedPointer.h"
#include "Manager/HyperlinkManager.h"
#include "Manager/TextShieldMgr.h"
#include "GameData/ConstDataBP.h"

CONTROL_COMPILE_OPTIMIZE_START

DECLARE_CYCLE_STAT(TEXT("GetFStringPropertyValue"), STAT_GetFStringPropertyValue, STATGROUP_UGolbalBPFunctionLibrary);
DECLARE_CYCLE_STAT(TEXT("GetInterfaceByName"), STAT_GetInterfaceByName, STATGROUP_UGolbalBPFunctionLibrary);
DECLARE_CYCLE_STAT(TEXT("GetIntPropertyValue"), STAT_GetIntPropertyValue, STATGROUP_UGolbalBPFunctionLibrary);
DECLARE_CYCLE_STAT(TEXT("GetEntityPropertyValue"), STAT_GetEntityPropertyValue, STATGROUP_UGolbalBPFunctionLibrary);
DECLARE_CYCLE_STAT(TEXT("GetFloatPropertyValue"), STAT_GetFloatPropertyValue, STATGROUP_UGolbalBPFunctionLibrary);
DECLARE_CYCLE_STAT(TEXT("GetDoublePropertyValue"), STAT_GetDoublePropertyValue, STATGROUP_UGolbalBPFunctionLibrary);
DECLARE_CYCLE_STAT(TEXT("FindEntity"), STAT_FindEntity, STATGROUP_UGolbalBPFunctionLibrary);
DECLARE_CYCLE_STAT(TEXT("GetActorByID"), STAT_GetActorByID, STATGROUP_UGolbalBPFunctionLibrary);
DECLARE_CYCLE_STAT(TEXT("GetActorsInRange"), STAT_GetActorsInRange, STATGROUP_UGolbalBPFunctionLibrary);
	
void UGolbalBPFunctionLibrary::SetModelTextNumber(int32 modenumber)
{
	 ModelTextNumber = modenumber;
}

int32 UGolbalBPFunctionLibrary::GetModelTextNumber()
{
	return ModelTextNumber;
}

int32 UGolbalBPFunctionLibrary::ModelTextNumber = 0;
UUECS3GameInstance* UGolbalBPFunctionLibrary::GameInstance()
{
	return UUECS3GameInstance::Instance;
}

UCfgManager* UGolbalBPFunctionLibrary::CfgManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->CfgManager : nullptr;
}

UResourceManager* UGolbalBPFunctionLibrary::ResourceManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->ResourceManager : nullptr;
}

ULoginManager* UGolbalBPFunctionLibrary::LoginManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->LoginManager : nullptr;
}

ULevelManager* UGolbalBPFunctionLibrary::LevelManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->LevelManager : nullptr;
}

UActionManager* UGolbalBPFunctionLibrary::ActionManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->ActionManager : nullptr;
}

UParticleManager* UGolbalBPFunctionLibrary::ParticleManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->ParticleManager : nullptr;
}

AAudioManager* UGolbalBPFunctionLibrary::AudioManager()
{
	UUECS3GameInstance* gameInstance = UUECS3GameInstance::Instance;
	if (!IsValid(gameInstance)) return nullptr;

	if (!IsValid(gameInstance->AudioManager) && IsValid(gameInstance->GetWorld()))
	{
		gameInstance->AudioManager = SpawnActor<AAudioManager>(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_AudioManager")));
	}
	return gameInstance->AudioManager;
}

ULocalDataSaveManager* UGolbalBPFunctionLibrary::LocalDataSaveManager()
{
	return  IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->LocalDataSaveManager : nullptr;
}

UCustomCursorManager* UGolbalBPFunctionLibrary::CustomCursorManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->CustomCursorManager : nullptr;
}

class UMediaPlayerManager* UGolbalBPFunctionLibrary::MediaPlayerManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->MediaPlayerManager : nullptr;
}

class UGStoryManager* UGolbalBPFunctionLibrary::GStoryManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->GStoryManager : nullptr;
}

UMessageManager* UGolbalBPFunctionLibrary::MessageManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->MessageManager : nullptr;
}

UMapManager * UGolbalBPFunctionLibrary::MapManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->MapManager : nullptr;
}

UQuestManager * UGolbalBPFunctionLibrary::QuestManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->QuestManager : nullptr;
}


UGLoaderManager* UGolbalBPFunctionLibrary::GLoaderManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->GLoaderManager : nullptr;
}

UVisibleManager * UGolbalBPFunctionLibrary::VisibleManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->VisibleManager : nullptr;
}

UGUIManager* UGolbalBPFunctionLibrary::GUIManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->GUIManager : nullptr;
}

UUIFixerManager* UGolbalBPFunctionLibrary::UIFixerManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->UIFixerManager : nullptr;
}

UUIDockManager* UGolbalBPFunctionLibrary::UIDockManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->UIDockManager : nullptr;
}

UGEventManager* UGolbalBPFunctionLibrary::GEventManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->GEventManager : nullptr;
}

UGameplayEventManager* UGolbalBPFunctionLibrary::GameplayEventManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->GameplayEventManager : nullptr;
}

UTipsManager* UGolbalBPFunctionLibrary::TipsManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->TipsManager : nullptr;
}


UEmoteManager* UGolbalBPFunctionLibrary::EmoteManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->EmoteManager : nullptr;
}


UDecalManager* UGolbalBPFunctionLibrary::DecalManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->DecalManager : UDecalManager::GetInstance();
}

USkillManager* UGolbalBPFunctionLibrary::SkillManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->SkillManager : nullptr;
}

UForceManager* UGolbalBPFunctionLibrary::ForceManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->ForceManager : nullptr;
}

UTutorialManager* UGolbalBPFunctionLibrary::TutorialManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->TutorialManager : nullptr;
}

UAutoFightMar* UGolbalBPFunctionLibrary::AutoFightMar()
{
	return UAutoFightMar::GetInstanceByCS3GameInstance();
}

UControllerModeMgr* UGolbalBPFunctionLibrary::ControllerModeMgr()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->ControllerModeMgr : nullptr;
}

UOperationModeMgr* UGolbalBPFunctionLibrary::OperationModeMgr()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->OperationModeMgr : nullptr;
}

UTimeManager* UGolbalBPFunctionLibrary::TimeManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->TimeManager : nullptr;
}

UCustomTimerManager* UGolbalBPFunctionLibrary::CustomTimerManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->CustomTimerManager : nullptr;
}

class UModifyFaceManager* UGolbalBPFunctionLibrary::ModifyFaceManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->ModifyFaceManager : nullptr;
}

class AHeadManager* UGolbalBPFunctionLibrary::HeadManager()
{
	UUECS3GameInstance* gameInstance = UUECS3GameInstance::Instance;
	if (!IsValid(gameInstance)) return nullptr;

	if (!IsValid(gameInstance->HeadManager) && IsValid(gameInstance->GetWorld()))
	{
		gameInstance->HeadManager = SpawnActor<AHeadManager>(UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_HeadManager")));
	}
	return gameInstance->HeadManager;
}

class UQuickBarManager* UGolbalBPFunctionLibrary::QuickBarManager()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->QuickBarManager : nullptr;
}

class UImageLoader* UGolbalBPFunctionLibrary::ImageLoader()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->ImageLoader : nullptr;
}

class UMotionBlurManager* UGolbalBPFunctionLibrary::MotionBlurManager()
{
	//return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->MotionBlurManager : nullptr;
	// 编辑器不启动游戏也需要能获取此单键，所以不希望和UUECS3GameInstance绑定，zhengxuemei,2020年3月19日09:51:39
	return UMotionBlurManager::GetInstance();
}


bool UGolbalBPFunctionLibrary::IsPositionInSectorRange(FVector InPos, FVector InSectorPos, FVector InSectorForwadDir, float InSectorAngle, float InSectorDistance, float InSectorHeight)
{
	float InRad = InSectorAngle * (PI / 180);
	if (InRad < 0)
	{
		InRad = 0;
	}
	else if (InRad > PI)
	{
		InRad = PI;
	}
	if (FMath::Abs(InPos.Z - InSectorPos.Z) > InSectorHeight)
	{
		return false;
	}
	FVector2D InPosToInSectorPosDir2D = FVector2D(InPos.X - InSectorPos.X, InPos.Y - InSectorPos.Y);

	FVector2D InSectorForwadDir2D = FVector2D(InSectorForwadDir.X, InSectorForwadDir.Y);

	float len = FMath::Sqrt(InPosToInSectorPosDir2D.X*InPosToInSectorPosDir2D.X + InPosToInSectorPosDir2D.Y*InPosToInSectorPosDir2D.Y);
	if (len > InSectorDistance)
	{
		return false;
	}

	InPosToInSectorPosDir2D.Normalize();
	InSectorForwadDir2D.Normalize();

	float Rad = FMath::Acos(FVector2D::DotProduct(InSectorForwadDir2D, InPosToInSectorPosDir2D));

	if (FMath::Abs(Rad) > (InRad / 2))
	{
		return false;
	}
	return true;
}


void UGolbalBPFunctionLibrary::SortActorByDistance(const TArray<AActor*>& Array, AActor* Actor)
{
	TArray<AActor*>& src = const_cast<TArray<AActor*>&>(Array);

	auto func = [=](AActor& a, AActor& b) -> bool
	{
		float da = GetActorDistance(&a, Actor);
		float db = GetActorDistance(&b, Actor);
		return da < db;
	};
	src.Sort(func);
}

TArray<FString> UGolbalBPFunctionLibrary::SplitString(const FString& InString, bool IsElemUnique, FString SplitChar)
{
	TArray<FString> SplitArray;
	FString SplitStr(InString);
	FString Left, Right;
	bool Result = true;
	while (!SplitStr.IsEmpty())
	{
		Result = SplitStr.Split(SplitChar, &Left, &Right, ESearchCase::Type::CaseSensitive);
		if (Result)
		{
			SplitStr = Right;
			if (IsElemUnique)
				SplitArray.AddUnique(Left);
			else
				SplitArray.Add(Left);
		}
		else
		{
			if (IsElemUnique)
				SplitArray.AddUnique(SplitStr);
			else
				SplitArray.Add(SplitStr);
			SplitStr = TEXT("");
		}
	}
	return SplitArray;
}

FString UGolbalBPFunctionLibrary::TypeValidation(const FString InString)
{
	if (InString == "")
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("-----------------类型转换错误，传入参数为空--------------------%s"), *InString);
		return InString;
	}
	FString point = ".+-";
	FString number = "0123456789";

	FString CopyString = InString;

	if (CopyString[0] == point[1] || CopyString[0] == point[2])
	{
		CopyString.RemoveAt(0, 1);
	}

	int32 count = 0;
	int32 pointCount = 0;
	for (auto element : CopyString)
	{
		for (int i = 0; i < number.Len(); i++)
		{
			if (element == number[i] || element == point[0])
			{
				count = 0;
				if (element == point[0])
				{
					pointCount++;
				}
				break;
			}
			else count++;
		}

		if (count == number.Len())
		{
			CS3_Display(CS3DebugType::CL_Undefined, TEXT("-----------------类型转换错误，有不是小数点和数字的字符--------------------%s"), *InString);
			return InString;
		}
	}

	if (pointCount > 1)
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("-----------------类型转换错误，有两个以上小数点--------------------%s"), *InString);
		return InString;
	}
	return InString;
}

TArray<FVector> UGolbalBPFunctionLibrary::ConvertStringToVectors(const FString& VectorString)
{
	TArray<FString> SplitArray = SplitString(VectorString, false, ",");
	TArray<FVector> WorldLocation;
	for (int i = 0; i < SplitArray.Num(); i += 3)
	{
		FVector TempVector;
		TempVector.X = FSTRING_TO_FLOAT(SplitArray[i]);
		TempVector.Y = FSTRING_TO_FLOAT(SplitArray[i + 1]);
		TempVector.Z = FSTRING_TO_FLOAT(SplitArray[i + 2]);
		WorldLocation.Add(TempVector);
	}
	return WorldLocation;
}

TArray<FVector> UGolbalBPFunctionLibrary::ConvertFVector2DToFVector(const TArray<FVector2D>& Target)
{
	TArray<FVector> WorldLocation;
	for (auto vector : Target)
	{
		FVector temp;
		temp.X = vector.X;
		temp.Y = vector.Y;
		temp.Z = 0;
		WorldLocation.Add(temp);
	}
	return WorldLocation;
}

FText UGolbalBPFunctionLibrary::GetPercent(int32 InCurValue, int32 InMaxValue)
{
	//用双精度，因为整型是2的32次方，转float会精度丢失
	double result = static_cast<double>(InCurValue) / static_cast<double>(InMaxValue);
	//精确到小数后2位，以防有 .0000000001这样的数计算不准
	float tempPercent = (float)(FMath::FloorToDouble(result * 100) / 100.0);
	return UKismetTextLibrary::AsPercent_Float( tempPercent, ERoundingMode::HalfToEven);
}

int32 UGolbalBPFunctionLibrary::GetBloodStage(float& OnProgressPercent, int32 InCurHP, int32 InMaxHP, int32 DefaultBloodNum /*= 1*/)
{
	double TempCurHP = static_cast<double>(InCurHP);
	double TempMaxHP = static_cast<double>(InMaxHP);
	double TempDefaultBloodNum = static_cast<double>(DefaultBloodNum);
	//血条段数=math.ceil(CurHP/(MaxHP/DefaultBloodNum))
	double StageMaxHP = FMath::FloorToDouble((TempMaxHP / TempDefaultBloodNum) * 100) / 100.0;
	int32 BloodStage = UKismetMathLibrary::FCeil(FMath::FloorToDouble((TempCurHP / StageMaxHP) * 100) / 100.0);
	//当前阶段进度条百分比=(CurHP % (MaxHP / BloodNum)) / (MaxHP / BloodNum)
	double TempPercent = static_cast<double>(InCurHP % (InMaxHP / DefaultBloodNum)) / StageMaxHP;
	//等于0有2种可能，一种是能被整除，进度条百分比应该是100%，一种是CurHP=0，进度条百分比是0
	if ( UKismetMathLibrary::NearlyEqual_FloatFloat(TempPercent, 0.0) && InCurHP != 0)
	{
		OnProgressPercent = 1.0;
	}
	else
	{
		OnProgressPercent = (float)(FMath::FloorToDouble(TempPercent * 100) / 100.0);
	}
	return BloodStage;
}

bool UGolbalBPFunctionLibrary::IsContainStr(const FString Str, const TArray<FString> Array)
{
	for (auto& Elem : Array)
	{
		if (!Str.Compare(Elem))
		{
			return true;
		}
	}
	return false;
}

const FString & UGolbalBPFunctionLibrary::GetSpaceData(const FString & key)
{
	if (UUECS3GameInstance::pKBEApp && UUECS3GameInstance::pKBEApp->pBaseApp())
	{
		return UUECS3GameInstance::pKBEApp->pBaseApp()->GetSpaceData(key);
	}
	static FString s_null_data;
	return s_null_data;
}

FDateTime UGolbalBPFunctionLibrary::FromServerTimeToClientTime(int32 ctime)
{
	if (ctime < 0)
	{
		ctime = 0;
	}
	if (UUECS3GameInstance::Instance)
	{
		return UUECS3GameInstance::Instance->RecordServerTime + ctime * ETimespan::TicksPerSecond;
	}
	return FDateTime(1970, 1, 1) + ((int64)8 * 3600) * ETimespan::TicksPerSecond + ctime * ETimespan::TicksPerSecond;
}

FDateTime UGolbalBPFunctionLibrary::FromServerStrTimeToClientTime(FString strTime)
{
	int64 itime = FCString::Atoi64(*strTime);
	if (itime < 0)
	{
		itime = 0;
	}
	if (UUECS3GameInstance::Instance)
	{
		UTimeManager *TimeManager = UUECS3GameInstance::Instance->TimeManager;
		return TimeManager->ServerTimeToClientTime(itime);
		/*return UUECS3GameInstance::Instance->RecordServerTime + itime;*/
	}
	return FDateTime(1970, 1, 1) + ((int64)8 * 3600) * ETimespan::TicksPerSecond + itime;
}

float UGolbalBPFunctionLibrary::FromClientTimeToServerTime(FDateTime ctime)
{
	int64 num = ctime.GetTicks();
	if (num < 0)
	{
		num = 0;
	}
	if (UUECS3GameInstance::Instance)
	{
		return (float)((ctime - UUECS3GameInstance::Instance->RecordServerTime).GetTicks()) / (float)(ETimespan::TicksPerSecond);
	}
	return (float)((num - FDateTime(1970, 1, 1).GetTicks() - ((int64)8 * 3600) * ETimespan::TicksPerSecond)) / (float)(ETimespan::TicksPerSecond);
}

int64 UGolbalBPFunctionLibrary::FromClientTimeToServerStrTime(FDateTime ctime)
{
	int64 num = ctime.GetTicks();
	if (num < 0)
	{
		num = 0;
	}
	if (UUECS3GameInstance::Instance)
	{
		return (ctime - UUECS3GameInstance::Instance->RecordServerTime).GetTicks();
	}
	return (ctime - FDateTime(1970, 1, 1) - ((int64)8 * 3600) * ETimespan::TicksPerSecond).GetTicks();
}

int64 UGolbalBPFunctionLibrary::FromServerStrTimeToSecond(int64 time)
{
	return time / ETimespan::TicksPerSecond;
}

int UGolbalBPFunctionLibrary::GetPlayerID()
{
	if (UUECS3GameInstance::pKBEApp == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetPlayerID : pKBEApp!"));
		return 0;
	}
	return UUECS3GameInstance::pKBEApp->PlayerID();
}

int UGolbalBPFunctionLibrary::GetPlayerPropertyInt(const FString& pName)
{
	if ((!IsValid(UUECS3GameInstance::Instance)) || (UUECS3GameInstance::pKBEApp == nullptr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetPlayerPropertyInt : Instance||pKBEApp!"));
		return 0;
	}
	CS3PlayRole *entity = UUECS3GameInstance::Instance->CS3Player();
	if (entity != nullptr)
	{
		FVariant propvalue = entity->GetDefinedProperty(pName);
		if (propvalue != FVariant(NULL))
		{
			//int32 type = propvalue.GetType();
			switch (propvalue.GetType())
			{
			case EVariantTypes::UInt8:
			{
				return int32(propvalue.GetValue<uint8>());
			}
			case EVariantTypes::UInt16:
			{
				return int32(propvalue.GetValue<uint16>());
			}
			case EVariantTypes::UInt32:
			{
				uint32 value = propvalue.GetValue<uint32>();
				//判断value > 2147483647，就崩溃
				check(value < 2147483648);
				return int32(propvalue.GetValue<uint32>());
			}
			case EVariantTypes::UInt64:
			{
				return int32(propvalue.GetValue<uint64>());
			}
			case EVariantTypes::Int8:
			{
				return int32(propvalue.GetValue<int8>());
			}
			case EVariantTypes::Int16:
			{
				return int32(propvalue.GetValue<int16>());
			}
			case EVariantTypes::Int32:
			{
				return int32(propvalue.GetValue<int32>());
			}
			default:
				check(false);
				break;
			}
		}
	}
	return 0;

}

float UGolbalBPFunctionLibrary::GetPlayerPropertyFloat(const FString& pName)
{
	SCOPE_CYCLE_COUNTER(STAT_GetFloatPropertyValue);
	if ((!IsValid(UUECS3GameInstance::Instance)) || (UUECS3GameInstance::pKBEApp == nullptr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetFloatPropertyValue : Instance||pKBEApp!"));
		return 0;
	}
	CS3PlayRole *entity = UUECS3GameInstance::Instance->CS3Player();
	if (entity != nullptr)
	{
		FVariant propvalue = entity->GetDefinedProperty(pName);
		if (propvalue != FVariant(NULL))
		{
			//int32 type = propvalue.GetType();
			switch (propvalue.GetType())
			{
			case EVariantTypes::Float:
			{
				return propvalue.GetValue<float>();
			}
			default:
				check(false);
				break;
			}
		}
	}
	return 0;
}

double UGolbalBPFunctionLibrary::GetPlayerPropertyDouble(const FString& pName)
{
	SCOPE_CYCLE_COUNTER(STAT_GetDoublePropertyValue);
	if ((!IsValid(UUECS3GameInstance::Instance)) || (UUECS3GameInstance::pKBEApp == nullptr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetDoublePropertyValue : Instance||pKBEApp!"));
		return 0.0;
	}
	CS3PlayRole *entity = UUECS3GameInstance::Instance->CS3Player();
	if (entity != nullptr)
	{
		FVariant propvalue = entity->GetDefinedProperty(pName);
		if (propvalue != FVariant(NULL))
		{
			//int32 type = propvalue.GetType();
			switch (propvalue.GetType())
			{
			case EVariantTypes::Double:
			{
				return propvalue.GetValue<double>();
			}
			default:
				check(false);
				break;
			}
		}
	}
	return 0.0;
}

FString UGolbalBPFunctionLibrary::GetPlayerPropertyString(const FString& pName)
{
	SCOPE_CYCLE_COUNTER(STAT_GetFStringPropertyValue);
	if ((!IsValid(UUECS3GameInstance::Instance)) || (UUECS3GameInstance::pKBEApp == nullptr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetFStringPropertyValue : Instance||pKBEApp!"));
		return TEXT("");
	}
	CS3PlayRole *entity = UUECS3GameInstance::Instance->CS3Player();
	if (entity != nullptr)
	{
		FVariant propvalue = entity->GetDefinedProperty(pName);
		if (propvalue != FVariant(NULL))
		{
			//int32 type = propvalue.GetType();
			switch (propvalue.GetType())
			{
			case EVariantTypes::String:
			case EVariantTypes::Widechar:
			{
				return propvalue.GetValue<FString>();
			}
			default:
				check(false);
				break;
			}
		}
	}
	return TEXT("");
}

int32 UGolbalBPFunctionLibrary::GetPlayerCamp()
{
	if ((!IsValid(UUECS3GameInstance::Instance)) || (UUECS3GameInstance::pKBEApp == nullptr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetPlayerCamp : Instance||pKBEApp!"));
		return 0;
	}
	CS3PlayRole *entity = UUECS3GameInstance::Instance->CS3Player();
	if (entity != nullptr)
	{
		return entity->Camp();
	}
	return 0;
}

int32 UGolbalBPFunctionLibrary::GetPlayerGender()
{
	if ((!IsValid(UUECS3GameInstance::Instance)) || (UUECS3GameInstance::pKBEApp == nullptr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetPlayerGender : Instance||pKBEApp!"));
		return 0;
	}
	CS3PlayRole *entity = UUECS3GameInstance::Instance->CS3Player();
	if (entity != nullptr)
	{
		return entity->Gender();
	}
	return 0;
}

int64 UGolbalBPFunctionLibrary::GetPlayerMoney()
{
	if ((!IsValid(UUECS3GameInstance::Instance)) || (UUECS3GameInstance::pKBEApp == nullptr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetPlayerMoney : Instance||pKBEApp!"));
		return 0;
	}
	CS3PlayRole *entity = UUECS3GameInstance::Instance->CS3Player();
	if (entity != nullptr)
	{
		return entity->Money();
	}
	return 0;
}

int32 UGolbalBPFunctionLibrary::GetPlayerPotential()
{
	if ((!IsValid(UUECS3GameInstance::Instance)) || (UUECS3GameInstance::pKBEApp == nullptr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetPlayerPotential : Instance||pKBEApp!"));
		return 0;
	}
	CS3PlayRole *entity = UUECS3GameInstance::Instance->CS3Player();
	if (entity != nullptr)
	{
		return entity->Potential();
	}
	return 0;
}

FString UGolbalBPFunctionLibrary::GetPlayerName()
{
	if ((!IsValid(UUECS3GameInstance::Instance)) || (UUECS3GameInstance::pKBEApp == nullptr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetPlayerName : Instance||pKBEApp!"));
		return TEXT("");
	}
	CS3PlayRole *entity = UUECS3GameInstance::Instance->CS3Player();
	if (entity != nullptr)
	{
		return entity->PlayerName();
	}
	return TEXT("");
}

int32 UGolbalBPFunctionLibrary::GetPlayerProfession()
{
	if ((!IsValid(UUECS3GameInstance::Instance)) || (UUECS3GameInstance::pKBEApp == nullptr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetPlayerProfession : Instance||pKBEApp!"));
		return 0;
	}
	CS3PlayRole *entity = UUECS3GameInstance::Instance->CS3Player();
	if (entity != nullptr)
	{
		return entity->Profession();
	}
	return 0;
}

int32 UGolbalBPFunctionLibrary::GetPlayerState()
{
	if ((!IsValid(UUECS3GameInstance::Instance)) || (UUECS3GameInstance::pKBEApp == nullptr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetPlayerState : Instance||pKBEApp!"));
		return 0;
	}
	CS3PlayRole *entity = UUECS3GameInstance::Instance->CS3Player();
	if (entity != nullptr)
	{
		return entity->State();
	}
	return 0;
}

int32 UGolbalBPFunctionLibrary::GetPlayerLevel()
{
	if ((!IsValid(UUECS3GameInstance::Instance)) || (UUECS3GameInstance::pKBEApp == nullptr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetPlayerLevel : Instance||pKBEApp!"));
		return 0;
	}
	CS3PlayRole *entity = UUECS3GameInstance::Instance->CS3Player();
	if (entity != nullptr)
	{
		return entity->Level();
	}
	return 0;
}

uint64 UGolbalBPFunctionLibrary::GetPlayerPlayerDBID()
{
	if ((!IsValid(UUECS3GameInstance::Instance)) || (UUECS3GameInstance::pKBEApp == nullptr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetPlayerPlayerDBID : Instance||pKBEApp!"));
		return 0;
	}
	CS3PlayRole *entity = UUECS3GameInstance::Instance->CS3Player();
	if (entity != nullptr)
	{
		return entity->PlayerDBID();
	}
	return 0;
}

int UGolbalBPFunctionLibrary::GetTargetEntityID()
{
	if (UUECS3GameInstance::pKBEApp == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetTargetEntityID : pKBEApp!"));
		return 0;
	}
	CS3PlayRole *entity = UUECS3GameInstance::Instance->CS3Player();
	if (entity)
	{
		CS3Role* SelfRole = (CS3Role*)(entity);
		if (SelfRole && SelfRole->IsPlayerRole())
		{
			int32 TargetEntityID = SelfRole->GetTargetEntityID();
			return TargetEntityID;
		}
	}
	return 0;
}

void UGolbalBPFunctionLibrary::SetTargetEntity(const AActor* InTargetActor)
{
	if (!UUECS3GameInstance::pKBEApp)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::SetTargetEntity : pKBEApp!"));
		return;
	}

	CS3PlayRole *MyRolePlayer = UUECS3GameInstance::Instance->CS3Player();
	if (!MyRolePlayer)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::SetTargetEntity : MyRolePlayer!"));
		return;
	} 

	AServerCharacter* TargetCharacter = ((AServerCharacter*)InTargetActor);
	if (TargetCharacter)
	{
		KBEngine::Entity* TargetEntity = TargetCharacter->GetSelfEntity();
		if (TargetEntity)
		{
			MyRolePlayer->SetTargetEntityID(TargetEntity->ID());
		}
	}
	else
	{
		MyRolePlayer->SetTargetEntityID(MyRolePlayer->ID());
	}
}

void UGolbalBPFunctionLibrary::CellCall(int EntityID, const FString &methodname, const TArray<FString> &arguments)
{
	KBEngine::Entity* ent = UGolbalBPFunctionLibrary::FindEntity(EntityID);
	if (ent != NULL)
	{
		TArray<FVariant> arg;
		for (int i = 0; i < arguments.Num(); i++) {
			arg.Add(arguments[i]);
		}
		ent->CellCall(methodname, arg);
	}
}

void UGolbalBPFunctionLibrary::CellCallWithIntList(int EntityID, const FString &methodname, const TArray<int32> &arguments)
{
	KBEngine::Entity* ent = UGolbalBPFunctionLibrary::FindEntity(EntityID);
	if (ent != NULL)
	{
		KBEngine::FVariantArray arg;
		arg.Add(ListToFVariant(arguments));
		ent->CellCall(methodname, arg);
	}
}

void UGolbalBPFunctionLibrary::CellCallWithFStringList(int EntityID, const FString &methodname, const TArray<FString> &arguments)
{
	KBEngine::Entity* ent = UGolbalBPFunctionLibrary::FindEntity(EntityID);
	if (ent != NULL)
	{
		KBEngine::FVariantArray arg;
		arg.Add(ListToFVariant(arguments));
		ent->CellCall(methodname, arg);
	}
}

void UGolbalBPFunctionLibrary::BaseCall(int EntityID, const FString &methodname, const TArray<FString> &arguments)
{
	KBEngine::Entity* ent = UGolbalBPFunctionLibrary::FindEntity(EntityID);
	if (ent != NULL)
	{
		TArray<FVariant> arg;
		for (int i = 0; i < arguments.Num(); i++) {
			arg.Add(arguments[i]);
		}
		ent->BaseCall(methodname, arg);
	}
}

void UGolbalBPFunctionLibrary::BaseCallWithIntList(int EntityID, const FString &methodname, const TArray<int32> &arguments)
{
	KBEngine::Entity* ent = UGolbalBPFunctionLibrary::FindEntity(EntityID);
	if (ent != NULL)
	{
		KBEngine::FVariantArray arg;
		arg.Add(ListToFVariant(arguments));
		ent->BaseCall(methodname, arg);
	}
}

void UGolbalBPFunctionLibrary::BaseCallWithFStringList(int EntityID, const FString &methodname, const TArray<FString> &arguments)
{
	KBEngine::Entity* ent = UGolbalBPFunctionLibrary::FindEntity(EntityID);
	if (ent != NULL)
	{
		KBEngine::FVariantArray arg;
		arg.Add(ListToFVariant(arguments));
		ent->BaseCall(methodname, arg);
	}
}

bool UGolbalBPFunctionLibrary::SGreaterThan(FString StringA, FString StringB)
{
	return (FCString::Strcmp(*StringA, *StringB) > 0);
}


bool UGolbalBPFunctionLibrary::SLessThan(FString StringA, FString StringB)
{
	return (FCString::Strcmp(*StringA, *StringB) < 0);
}

class UCS3EntityInterface* UGolbalBPFunctionLibrary::GetInterfaceByName(const FString& name, int32 id /*= 0*/)
{
	SCOPE_CYCLE_COUNTER(STAT_GetInterfaceByName);
	KBEngine::Entity* Entity = nullptr;
	if (UUECS3GameInstance::pKBEApp == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetInterfaceByName : pKBEApp!"));
		return nullptr;
	}
	if (id == 0)
	{
		Entity = UUECS3GameInstance::pKBEApp->Player();
		if (Entity && !Entity->IsPlayer())
		{
			Entity = nullptr;
		}
	}
	else
	{
		Entity = FindEntity(id);
	}

	if (nullptr != Entity)
	{
		CS3Entity* cs3Entity = static_cast<CS3Entity*>(Entity);
		return cs3Entity->GetInterfaceByName(name);
	}

	return nullptr;
}

void UGolbalBPFunctionLibrary::SetActorAndCompVisibility(AActor* Actor, TSubclassOf<USceneComponent> CompClass, bool bShowActor, bool bShowComp)
{
	// CST-10700
	if (IsValid(Actor) && Actor->bHidden == bShowActor)
	{
		// 对象组件
		UGolbalBPFunctionLibrary::SetComponentsVisiable(Actor, CompClass, bShowComp);
		// 对象自身
		Actor->SetActorHiddenInGame(!bShowActor);

		// 对象创建的不绑定的光效
		UUECS3GameInstance::Instance->ParticleManager->SetVisiableByActor(Actor, bShowActor);

		// 对象绑定子对象
		TArray<AActor*> AttachedActors;
		//对象的子Actor
		TArray<AActor*> ChildActors;
		Actor->GetAttachedActors(AttachedActors);
		Actor->GetAllChildActors(ChildActors, true);
		AttachedActors.Append(ChildActors);
		for (auto& AttachedActor : AttachedActors)
		{
			AttachedActor->SetActorHiddenInGame(!bShowActor);
			UGolbalBPFunctionLibrary::SetComponentsVisiable(AttachedActor, CompClass, bShowComp);
		}
		AServerCharacter* Character = Cast<AServerCharacter>(Actor);
		if (!IsValid(Character))
		{
			CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::SetActorAndCompVisibility : Character!"));
			return;
		}
		if (!bShowComp)
		{
			Character->SetOpenScene3DUI(false);
		}
		else
		{
			Character->ReSetOpenScen3DUI();
		}
		Character->OnVisibleChangedEvent.Broadcast();
	}
}

void UGolbalBPFunctionLibrary::SetComponentsVisiable(AActor* Actor, TSubclassOf<USceneComponent> CompClass, const bool& Visiable)
{
	if (IsValid(Actor))
	{
		// 对象组件
		TArray<UActorComponent*> ActorCompList = Actor->GetComponentsByClass(CompClass);

		for (auto& ActorComp : ActorCompList)
		{
			if (USceneComponent* SceneComp = Cast<USceneComponent>(ActorComp))
			{
				if (!SceneComp->ComponentHasTag("NoUpdateVisible"))
				{
					SceneComp->SetVisibility(Visiable);
				}
				if (SceneComp->IsA(UWidgetComponent::StaticClass()))
				{
					if (UWidgetComponent*WidgetComp = Cast<UWidgetComponent>(ActorComp))
					{
						if (UUserWidget * WidgetObj = Cast<UWidgetComponent>(ActorComp)->GetUserWidgetObject())
						{
							if (Visiable)
							{
								WidgetObj->SetVisibility(ESlateVisibility::SelfHitTestInvisible);
							}
							else
							{
								WidgetObj->SetVisibility(ESlateVisibility::Hidden);
							}
						}
					}
				}
			}
		}
	}
}

TArray<FString> UGolbalBPFunctionLibrary::IntListToStringList(const TArray<int32>& intlist)
{
	TArray<FString> strlist;
	for (auto item : intlist)
	{
		strlist.Add(FString::FromInt(item));
	}
	return strlist;
}

TArray<int32> UGolbalBPFunctionLibrary::StringListToIntList(const TArray<FString>& strlist)
{
	TArray<int32> intlist;
	for (auto item : strlist)
	{
		intlist.Add(FSTRING_TO_INT(item));
	}
	return intlist;
}

TArray<FString> UGolbalBPFunctionLibrary::FloatListToStringList(const TArray<float>& floatlist)
{
	TArray<FString> strlist;
	for (auto item : floatlist)
	{
		strlist.Add(FString::SanitizeFloat(item));
	}
	return strlist;
}

FVariant UGolbalBPFunctionLibrary::ListToFVariant(const TArray<int32>& intlist)
{
	FVariant arg;
	KBEngine::FVariantArray arr;
	for (auto item : intlist)
	{
		arr.Add(FVariant((int32)item));
	}
	arg = FVariant(arr);
	return arg;
}

FVariant UGolbalBPFunctionLibrary::ListToFVariant(const TArray<FString>& stringlist)
{
	FVariant arg;
	KBEngine::FVariantArray arr;
	for (auto item : stringlist)
	{
		arr.Add(FVariant(item));
	}
	arg = FVariant(arr);
	return arg;
}

int32 UGolbalBPFunctionLibrary::GetAbsItemOrder(int32 relorder, EKITBAGTYPE bagtype)
{
	int32 queststart = COMMON_BAG_START + COMMON_BAG_CAPACITY + COMMON_BAG_LOCK_CAPACITY;
	int32 crystalstart = queststart + QUEST_BAG_CAPACITY;
	int32 storestart = crystalstart + CRYSTAL_BAG_CAPACITY;
	int32 tongStoreStart = storestart + STORE_CAPACITY + STORE_LOCK_CAPACITY;
	int32 spaceCopyBagStart = tongStoreStart + TONG_CAPACITY;
	int32 spaceCopyYXLM1BagStart = spaceCopyBagStart + SPACE_COPY_BAG_CAPACITY;
	int32 spaceCopyYXLM2BagStart = spaceCopyYXLM1BagStart + SPACE_COPY_YXLM1_BAG_CAPACITY;
	int32 spaceCopyYXLM3BagStart = spaceCopyYXLM2BagStart + SPACE_COPY_YXLM_BAG_OTHER_CAPACITY;
	int32 spaceCopyYXLM4BagStart = spaceCopyYXLM3BagStart + SPACE_COPY_YXLM_BAG_OTHER_CAPACITY;
	int32 toolStoreStart = BAG_WORK_SHOP_LOCKERS_START;
	int32 tripodStoreStart = BAG_ALCHEMIST_LOCKERS_START;
	int32 TempEquipStart = UUECS3GameInstance::Instance->ConstDataBP->BAG_TEMP_EQUIP_START;
	switch (bagtype)
	{
	case EKITBAGTYPE::EQUIP:
		return relorder;
	case EKITBAGTYPE::COMMON:
		return relorder + COMMON_BAG_START;
	case EKITBAGTYPE::QUEST:
		return relorder + queststart;
	case EKITBAGTYPE::CRYSTAL:
		return relorder + crystalstart;
	case EKITBAGTYPE::STORE:
		return relorder + storestart;
	case EKITBAGTYPE::TONG_STORE:
		return relorder + tongStoreStart;
	case EKITBAGTYPE::SPACE_COPY_BAG:
		return relorder + spaceCopyBagStart;
	case EKITBAGTYPE::BAG_SPACE_COPY_YXLM1:
		return relorder + spaceCopyYXLM1BagStart;
	case EKITBAGTYPE::BAG_SPACE_COPY_YXLM2:
		return relorder + spaceCopyYXLM2BagStart;
	case EKITBAGTYPE::BAG_SPACE_COPY_YXLM3:
		return relorder + spaceCopyYXLM3BagStart;
	case EKITBAGTYPE::BAG_SPACE_COPY_YXLM4:
		return relorder + spaceCopyYXLM4BagStart;
	case EKITBAGTYPE::BAG_TOOL:
		return relorder + toolStoreStart;
	case EKITBAGTYPE::BAG_TRIPOD:
		return relorder + tripodStoreStart;
	case EKITBAGTYPE::BAG_TEMP_EQUIP:
		return relorder + TempEquipStart;
	default:
		return -1;
	}
}

EKITBAGTYPE UGolbalBPFunctionLibrary::GetBagTypeByAbsOrder(int32 absorder)
{
	int32 queststart = COMMON_BAG_START + COMMON_BAG_CAPACITY + COMMON_BAG_LOCK_CAPACITY;
	int32 crystalstart = queststart + QUEST_BAG_CAPACITY;
	int32 storestart = crystalstart + CRYSTAL_BAG_CAPACITY;
	int32 tongStoreStart = storestart + STORE_CAPACITY + STORE_LOCK_CAPACITY;
	int32 spaceCopyBagStart = tongStoreStart + TONG_CAPACITY;
	int32 spaceCopyYXLM1BagStart = spaceCopyBagStart + SPACE_COPY_BAG_CAPACITY;
	int32 spaceCopyYXLM2BagStart = spaceCopyYXLM1BagStart + SPACE_COPY_YXLM1_BAG_CAPACITY;
	int32 spaceCopyYXLM3BagStart = spaceCopyYXLM2BagStart + SPACE_COPY_YXLM_BAG_OTHER_CAPACITY;
	int32 spaceCopyYXLM4BagStart = spaceCopyYXLM3BagStart + SPACE_COPY_YXLM_BAG_OTHER_CAPACITY;
	int32 toolStoreStart = BAG_WORK_SHOP_LOCKERS_START;
	int32 tripodStoreStart = BAG_ALCHEMIST_LOCKERS_START;
	int32 AppeatranceStart = BAG_APPEARANCES_START;
	int32 TempEquipStart = UUECS3GameInstance::Instance->ConstDataBP->BAG_TEMP_EQUIP_START;
	if (absorder < COMMON_BAG_START)
	{
		return EKITBAGTYPE::EQUIP;
	}
	else if (absorder < queststart)
	{
		return EKITBAGTYPE::COMMON;
	}
	else if (absorder < crystalstart)
	{
		return EKITBAGTYPE::QUEST;
	}
	else if (absorder < storestart)
	{
		return EKITBAGTYPE::CRYSTAL;
	}
	else if (absorder < tongStoreStart)
	{
		return EKITBAGTYPE::STORE;
	}
	else if ( absorder < spaceCopyBagStart )
	{
		return EKITBAGTYPE::TONG_STORE;
	}
	else if(absorder < spaceCopyYXLM1BagStart)
	{
		return EKITBAGTYPE::SPACE_COPY_BAG;
	}
	else if (absorder < spaceCopyYXLM2BagStart)
	{
		return EKITBAGTYPE::BAG_SPACE_COPY_YXLM1;
	}
	else if (absorder < spaceCopyYXLM3BagStart)
	{
		return EKITBAGTYPE::BAG_SPACE_COPY_YXLM2;
	}
	else if (absorder < spaceCopyYXLM4BagStart)
	{
		return EKITBAGTYPE::BAG_SPACE_COPY_YXLM3;
	}
	else if (absorder < toolStoreStart)
	{
		return EKITBAGTYPE::BAG_SPACE_COPY_YXLM4;
	}
	else if (absorder < tripodStoreStart)
	{
		return EKITBAGTYPE::BAG_TOOL;
	}
	else if (absorder < AppeatranceStart)
	{
		return EKITBAGTYPE::BAG_TRIPOD;
	}
	else  if (absorder < TempEquipStart)
	{
		return EKITBAGTYPE::BAG_APPEARANCE;
	}
	else
	{
		return EKITBAGTYPE::BAG_TEMP_EQUIP;
	}
}

int32 UGolbalBPFunctionLibrary::GetRelOrderByAbsOrder(int32 absorder)
{
	int32 queststart = COMMON_BAG_START + COMMON_BAG_CAPACITY + COMMON_BAG_LOCK_CAPACITY;
	int32 crystalstart = queststart + QUEST_BAG_CAPACITY;
	int32 storestart = crystalstart + CRYSTAL_BAG_CAPACITY;
	int32 tongstorestart = storestart + STORE_CAPACITY + STORE_LOCK_CAPACITY;
	int32 spaceCopyBagStart = tongstorestart + TONG_CAPACITY;
	int32 spaceCopyYXLM1BagStart = spaceCopyBagStart + SPACE_COPY_BAG_CAPACITY;
	int32 spaceCopyYXLM2BagStart = spaceCopyYXLM1BagStart + SPACE_COPY_YXLM1_BAG_CAPACITY;
	int32 spaceCopyYXLM3BagStart = spaceCopyYXLM2BagStart + SPACE_COPY_YXLM_BAG_OTHER_CAPACITY;
	int32 spaceCopyYXLM4BagStart = spaceCopyYXLM3BagStart + SPACE_COPY_YXLM_BAG_OTHER_CAPACITY;
	int32 toolStoreStart = BAG_WORK_SHOP_LOCKERS_START;
	int32 tripodStoreStart = BAG_ALCHEMIST_LOCKERS_START;
	if (absorder < COMMON_BAG_START)
	{
		return absorder;
	}
	else if (absorder < queststart)
	{
		return absorder - COMMON_BAG_START;
	}
	else if (absorder < crystalstart)
	{
		return absorder - queststart;
	}
	else if (absorder < storestart)
	{
		return absorder - crystalstart;
	}
	else if(absorder < tongstorestart)
	{
		return absorder - storestart;
	}
	else if ( absorder < spaceCopyBagStart )
	{
		return absorder - tongstorestart;
	}
	else if(absorder < spaceCopyYXLM1BagStart) ///玩家副本专用背包策划定为8个
	{
		return absorder - spaceCopyBagStart;
	}
	else if (absorder < spaceCopyYXLM2BagStart)
	{
		return absorder - spaceCopyYXLM1BagStart;
	}
	else if (absorder < spaceCopyYXLM3BagStart)
	{
		return absorder - spaceCopyYXLM2BagStart;
	}
	else if (absorder < spaceCopyYXLM4BagStart)
	{
		return absorder - spaceCopyYXLM3BagStart;
	}
	else if (absorder < toolStoreStart)
	{
		return absorder - spaceCopyYXLM4BagStart;
	}
	else if (absorder < tripodStoreStart)
	{
		return absorder - toolStoreStart;
	}
	else
	{
		return absorder - tripodStoreStart;
	}

}

void UGolbalBPFunctionLibrary::GetBagTypeAndRelOrderByAbsOrder(const int32& absorder, int32& relorder, EKITBAGTYPE& bagtype)
{
	int32 queststart = COMMON_BAG_START + COMMON_BAG_CAPACITY + COMMON_BAG_LOCK_CAPACITY;
	int32 crystalstart = queststart + QUEST_BAG_CAPACITY;
	int32 storestart = crystalstart + CRYSTAL_BAG_CAPACITY;
	int32 tongstorestart = storestart + STORE_CAPACITY + STORE_LOCK_CAPACITY;
	int32 spaceCopyBagStart = tongstorestart + TONG_CAPACITY;
	int32 spaceCopyYXLM1BagStart = spaceCopyBagStart + SPACE_COPY_BAG_CAPACITY;
	int32 spaceCopyYXLM2BagStart = spaceCopyYXLM1BagStart + SPACE_COPY_YXLM1_BAG_CAPACITY;
	int32 spaceCopyYXLM3BagStart = spaceCopyYXLM2BagStart + SPACE_COPY_YXLM_BAG_OTHER_CAPACITY;
	int32 spaceCopyYXLM4BagStart = spaceCopyYXLM3BagStart + SPACE_COPY_YXLM_BAG_OTHER_CAPACITY;
	int32 toolStoreStart = BAG_WORK_SHOP_LOCKERS_START;
	int32 tripodStoreStart = BAG_ALCHEMIST_LOCKERS_START;
	int32 AppeatranceStart = BAG_APPEARANCES_START;
	int32 TempEquipStart = UUECS3GameInstance::Instance->ConstDataBP->BAG_TEMP_EQUIP_START;
	if (absorder < COMMON_BAG_START)
	{
		relorder = absorder;
		bagtype = EKITBAGTYPE::EQUIP;
	}
	else if (absorder < queststart)
	{
		relorder = absorder - COMMON_BAG_START;
		bagtype = EKITBAGTYPE::COMMON;
	}
	else if (absorder < crystalstart)
	{
		relorder = absorder - queststart;
		bagtype = EKITBAGTYPE::QUEST;
	}
	else if (absorder < storestart)
	{
		relorder = absorder - crystalstart;
		bagtype = EKITBAGTYPE::CRYSTAL;
	}
	else if (absorder < tongstorestart)
	{
		relorder = absorder - storestart;
		bagtype = EKITBAGTYPE::STORE;
	}
	else if (absorder < spaceCopyBagStart)
	{
		relorder = absorder - tongstorestart;
		bagtype = EKITBAGTYPE::TONG_STORE;
	}
	else if(absorder < spaceCopyYXLM1BagStart)
	{
		relorder = absorder - spaceCopyBagStart;
		bagtype = EKITBAGTYPE::SPACE_COPY_BAG;
	}
	else if (absorder < spaceCopyYXLM2BagStart)
	{
		relorder = absorder - spaceCopyYXLM1BagStart;
		bagtype = EKITBAGTYPE::BAG_SPACE_COPY_YXLM1;
	}
	else if (absorder < spaceCopyYXLM3BagStart)
	{
		relorder = absorder - spaceCopyYXLM2BagStart;
		bagtype = EKITBAGTYPE::BAG_SPACE_COPY_YXLM2;
	}
	else if (absorder < spaceCopyYXLM4BagStart)
	{
		relorder = absorder - spaceCopyYXLM3BagStart;
		bagtype = EKITBAGTYPE::BAG_SPACE_COPY_YXLM3;
	}
	else if (absorder < toolStoreStart)
	{
		relorder = absorder - spaceCopyYXLM4BagStart;
		bagtype = EKITBAGTYPE::BAG_SPACE_COPY_YXLM4;
	}
	else if (absorder < tripodStoreStart)
	{
		relorder = absorder - toolStoreStart;
		bagtype = EKITBAGTYPE::BAG_TOOL;
	}
	else if (absorder < AppeatranceStart)
	{
		relorder = absorder - tripodStoreStart;
		bagtype = EKITBAGTYPE::BAG_TRIPOD;
	}
	else if (absorder < TempEquipStart)
	{
		relorder = absorder - AppeatranceStart;
		bagtype = EKITBAGTYPE::BAG_APPEARANCE;
	}
	else
	{
		relorder = absorder - TempEquipStart;
		bagtype = EKITBAGTYPE::BAG_TEMP_EQUIP;
	}
}

FString UGolbalBPFunctionLibrary::GetChinese(const FString& rowname)
{
	if (IsValid(UGolbalBPFunctionLibrary::CfgManager()))
	{
		const UConfigTable* Table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_CHINESE);
		const FChinese* chinese = Table->GetRow<FChinese>(rowname);
		if (chinese)
		{
			return chinese->ChineseStr;
		}
	}
	return TEXT("");
}

FString UGolbalBPFunctionLibrary::GetEntityPropertyValue(const int32& entityid, const FString& propname)
{
	SCOPE_CYCLE_COUNTER(STAT_GetEntityPropertyValue);
	if ((!IsValid(UUECS3GameInstance::Instance)) || (UUECS3GameInstance::pKBEApp == nullptr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetEntityPropertyValue : Instance||pKBEApp!"));
		return TEXT("");
	}
	KBEngine::Entity* entity = UGolbalBPFunctionLibrary::FindEntity(entityid);
	if (entity != nullptr)
	{
		return entity->GetDefinedProperty(propname);
	}
	return TEXT("");
}

int32 UGolbalBPFunctionLibrary::GetIntPropertyValue(const int32& entityid, const FString& propname)
{
	SCOPE_CYCLE_COUNTER(STAT_GetIntPropertyValue);
	if ((!IsValid(UUECS3GameInstance::Instance)) || (UUECS3GameInstance::pKBEApp == nullptr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetIntPropertyValue : Instance||pKBEApp!"));
		return 0;
	}
	KBEngine::Entity* entity = FindEntity(entityid);
	//避免在角色选择时去获取一些玩家属性，存在一些问题
	if ((entity != nullptr) && (entity->ClassName() != TEXT("Account")))
	{
		FVariant propvalue = entity->GetDefinedProperty(propname);
		if (propvalue != FVariant(NULL))
		{
			//int32 type = propvalue.GetType();
			switch (propvalue.GetType())
			{
			case EVariantTypes::UInt8:
			{
				return int32(propvalue.GetValue<uint8>());
			}
			case EVariantTypes::UInt16:
			{
				return int32(propvalue.GetValue<uint16>());
			}
			case EVariantTypes::UInt32:
			{
				uint32 value = propvalue.GetValue<uint32>();
				//判断value > 2147483647，就崩溃
				check(value < 2147483648);
				return int32(propvalue.GetValue<uint32>());
			}
			case EVariantTypes::UInt64:
			{
				return int32(propvalue.GetValue<uint64>());
			}
			case EVariantTypes::Int8:
			{
				return int32(propvalue.GetValue<int8>());
			}
			case EVariantTypes::Int16:
			{
				return int32(propvalue.GetValue<int16>());
			}
			case EVariantTypes::Int32:
			{
				return int32(propvalue.GetValue<int32>());
			}
			default:
				check(false);
				break;
			}
		}
	}
	else
	{
		CS3_Warning(TEXT("can't find entity by entityid[%d]"), entityid);
	}
	return 0;
}

float UGolbalBPFunctionLibrary::GetFloatPropertyValue(const int32& entityid, const FString& propname)
{
	SCOPE_CYCLE_COUNTER(STAT_GetFloatPropertyValue);
	if ((!IsValid(UUECS3GameInstance::Instance)) || (UUECS3GameInstance::pKBEApp == nullptr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetFloatPropertyValue : Instance||pKBEApp!"));
		return 0;
	}
	KBEngine::Entity* entity = FindEntity(entityid);
	if (entity != nullptr && (entity->ClassName() != TEXT("Account")))
	{
		FVariant propvalue = entity->GetDefinedProperty(propname);
		if (propvalue != FVariant(NULL))
		{
			//int32 type = propvalue.GetType();
			switch (propvalue.GetType())
			{
			case EVariantTypes::Float:
			{
				return propvalue.GetValue<float>();
			}
			default:
				check(false);
				break;
			}
		}
	}
	else
	{
		CS3_Warning(TEXT("can't find entity by entityid[%d]"), entityid);
	}
	return 0;
}

double UGolbalBPFunctionLibrary::GetDoublePropertyValue(const int32& entityid, const FString& propname)
{
	SCOPE_CYCLE_COUNTER(STAT_GetDoublePropertyValue);
	if ((!IsValid(UUECS3GameInstance::Instance)) || (UUECS3GameInstance::pKBEApp == nullptr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetDoublePropertyValue : Instance||pKBEApp!"));
		return 0.0;
	}
	KBEngine::Entity* entity = FindEntity(entityid);
	if (entity != nullptr && (entity->ClassName() != TEXT("Account")))
	{
		FVariant propvalue = entity->GetDefinedProperty(propname);
		if (propvalue != FVariant(NULL))
		{
			//int32 type = propvalue.GetType();
			switch (propvalue.GetType())
			{
			case EVariantTypes::Double:
			{
				return propvalue.GetValue<double>();
			}
			default:
				check(false);
				break;
			}
		}
	}
	else
	{
		CS3_Warning(TEXT("can't find entity by entityid[%d]"), entityid);
	}
	return 0.0;
}

FString UGolbalBPFunctionLibrary::GetFStringPropertyValue(const int32& entityid, const FString& propname)
{
	SCOPE_CYCLE_COUNTER(STAT_GetFStringPropertyValue);
	if ((!IsValid(UUECS3GameInstance::Instance)) || (UUECS3GameInstance::pKBEApp == nullptr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetFStringPropertyValue : Instance||pKBEApp!"));
		return TEXT("");
	}
	KBEngine::Entity* entity = FindEntity(entityid);
	if (entity != nullptr && (entity->ClassName() != TEXT("Account")))
	{
		FVariant propvalue = entity->GetDefinedProperty(propname);
		if (propvalue != FVariant(NULL))
		{
			//int32 type = propvalue.GetType();
			switch (propvalue.GetType())
			{
			case EVariantTypes::String:
			case EVariantTypes::Widechar:
			{
				return propvalue.GetValue<FString>();
			}
			default:
				check(false);
				break;
			}
		}
	}
	else
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetFStringPropertyValue : entity!"));
	}
	return TEXT("");
}

KBEngine::Entity* UGolbalBPFunctionLibrary::FindEntity(const int32& entityid)
{
	SCOPE_CYCLE_COUNTER(STAT_FindEntity);
	if (UUECS3GameInstance::pKBEApp == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::FindEntity : pKBEApp!"));
		return nullptr;
	}
	return UUECS3GameInstance::pKBEApp->FindEntity(entityid);
}

GameObject* UGolbalBPFunctionLibrary::GetCS3PlayerEntity()
{
	if (UUECS3GameInstance::Instance == nullptr || UUECS3GameInstance::pKBEApp == nullptr)
	{
		CS3_Warning(TEXT("UGolbalBPFunctionLibrary::GetCS3PlayerEntity() Error: UUECS3GameInstance::Instance == nullptr || UUECS3GameInstance::pKBEApp == nullptr"));
		return nullptr;
	}
	
	return (GameObject*)UUECS3GameInstance::pKBEApp->Player();
}

AActor* UGolbalBPFunctionLibrary::GetActorByID(const int32& EntityID)
{
	SCOPE_CYCLE_COUNTER(STAT_GetActorByID);
	KBEngine::Entity* Entity = FindEntity(EntityID);
	if (Entity != nullptr)
	{
		return Entity->Actor();
	}
	return nullptr;
}


COMBAT_RELATION UGolbalBPFunctionLibrary::QueryRelationByEntityID(const int32 & EntityID, const int32& TargetID)
{
	KBEngine::Entity* Entity = FindEntity(EntityID);
	KBEngine::Entity* TargetEntity = FindEntity(TargetID);
	if (Entity != nullptr && TargetEntity != nullptr)
	{
		///转到entity判断关系
		return ((GameObject*)Entity)->QueryRelation(TargetEntity);
	}
	return COMBAT_RELATION::COMBAT_RELATION_NONE;
}


void UGolbalBPFunctionLibrary::GetAllActorsOfClassExt(TSubclassOf<AActor> ActorClass, TArray<AActor*>& outActor)
{
	if (UUECS3GameInstance::Instance)
	{
		const UWorld* Worldcontext = UUECS3GameInstance::Instance->GetWorld();
		UGameplayStatics::GetAllActorsOfClass(Worldcontext, ActorClass, outActor);
	}
}

void UGolbalBPFunctionLibrary::StatusMessage(const int32& statusID, const FString& args)
{
	int32 playerid = GetPlayerID();
	UCS3EntityInterface* BInterface = UGolbalBPFunctionLibrary::GetInterfaceByName(TEXT("StatusMessageInterface"), playerid);
	if (IsValid(BInterface))
	{
		UStatusMessageInterface* statusMessageInterface = Cast<UStatusMessageInterface>(BInterface);
		statusMessageInterface->statusMessage(statusID, args);
	}
}

int32 UGolbalBPFunctionLibrary::GetObjReferenceCount(UObject* Obj, TArray<UObject*>& OutReferredToObjects)
{
	if (!IsValid(Obj))
	{
		return -1;
	}

	TArray<UObject*> ReferredToObjects;				//req outer, ignore archetype, recursive, ignore transient
	FReferenceFinder ObjectReferenceCollector(ReferredToObjects, Obj, false, true, true, false);
	ObjectReferenceCollector.FindReferences(Obj);


	OutReferredToObjects.Append(ReferredToObjects);
	return OutReferredToObjects.Num();
}

bool UGolbalBPFunctionLibrary::CheckWorldTypeIsGame()
{
	if (!GEngine)
	{
		return false;
	}

	const TIndirectArray<FWorldContext> WorldContexts = GEngine->GetWorldContexts();
	for (const FWorldContext& Context : WorldContexts)
	{
		//CS3_Display(CS3DebugType::CL_Undefined, Context.World(), TEXT("CheckWorldTypeIsGame -> WorldType[%d]~"), (int32) Context.WorldType);
		if (((Context.WorldType == EWorldType::PIE)
			|| (Context.WorldType == EWorldType::Game))
			&& (Context.World() != NULL))
		{
			return true;
		}
	}
	return false;
}

void UGolbalBPFunctionLibrary::FilterProfessions(const TArray<int32> professions, const TArray<UItemBase*> &itemarray, TArray<UItemBase*>& result)
{
	const TArray<UItemBase*> temp = itemarray.FilterByPredicate([&](UItemBase* item)
	{
		if (item)
		{
			return item->IsMatchClasses(professions);
		}	
		return false;
	});
	result = temp;
}

void UGolbalBPFunctionLibrary::FilterEquipParts(const TArray<int32> equipparts, const TArray<UItemBase*> &itemarray, TArray<UItemBase*>& result)
{
	const TArray<UItemBase*> temp = itemarray.FilterByPredicate([&](UItemBase* item)
	{
		if (item)
		{
			return item->IsMatchEquipParts(equipparts);
		}
		return false;
	});
	result = temp;
}

void UGolbalBPFunctionLibrary::FilterLevels(const TArray<int32> levels, const TArray<UItemBase*> &itemarray, TArray<UItemBase*>& result)
{
	const TArray<UItemBase*> temp = itemarray.FilterByPredicate([&](UItemBase* item)
	{
		if (item)
		{
			return item->IsMatchLevels(levels);
		}
		return false;
	});
	result = temp;
}

void UGolbalBPFunctionLibrary::FilterQualities(const TArray<int32> qualities, const TArray<UItemBase*> &itemarray, TArray<UItemBase*>& result)
{
	const TArray<UItemBase*> temp = itemarray.FilterByPredicate([&](UItemBase* item)
	{
		if (item)
		{
			return item->IsMatchQualities(qualities);
		}
		return false;
	});
	result = temp;
}

int32 UGolbalBPFunctionLibrary::GetWeekDayByDate(const FDateTime Date)
{
	EDayOfWeek WeekDay = Date.GetDayOfWeek();
	return int32(WeekDay);
}

int64 UGolbalBPFunctionLibrary::GetFromUnixTimestamp(bool IsUTC /*= false*/)
{
	FDateTime DataTime = IsUTC ? FDateTime::UtcNow() : FDateTime::Now();
	return DataTime.ToUnixTimestamp();
}

FString UGolbalBPFunctionLibrary::GetRichTextMoney(int64 moneyValue, const FString & colorstr, bool IsBindMoney)
{
	FString TempColorStr = FString::Printf(TEXT("#%s"), *colorstr);
	FColor FontColor = FColor::FromHex(TempColorStr);
	TempColorStr = FString::Printf(TEXT("@F{fc=(%d,%d,%d,%d)}"), FontColor.R, FontColor.G, FontColor.B, FontColor.A);
	FString goldCoin = TEXT("@I{p=A5}");
	int64 gold = moneyValue;
	if(IsBindMoney)
	{
		goldCoin = TEXT("@I{p=A15}");
	}
	return TempColorStr + INT64_TO_FSTRING(gold) + goldCoin;
	
}

void UGolbalBPFunctionLibrary::SetCameraTargetArmLength(class USpringArmComponent* SpringArm, float LengthValue, bool bForce/* = false*/)
{
	//判断摄像机臂是否存在
	if (SpringArm)
	{
		float CurArmLength;
		float CameraArmLenMax;
		float CameraArmLenMin;
		const UUECS3GameInstance* GameInstance = UUECS3GameInstance::Instance;
		GameInstance->LocalDataSaveManager->LocalUserSettingData->GetCameraArmLenData(CameraArmLenMax, CameraArmLenMin);
		if (GameInstance && GameInstance->LocalDataSaveManager && GameInstance->LocalDataSaveManager->LocalUserSettingData&&!bForce)
		{
			//判断范围限制
			CurArmLength = FMath::Clamp(LengthValue, CameraArmLenMin, CameraArmLenMax);
		}
		else
		{
			//判断范围限制
			CurArmLength = FMath::Clamp(LengthValue, -100.0f, 2500.0f);
		}
		//设置臂长
		SpringArm->TargetArmLength = CurArmLength;
		APlayerCharacter* Player = Cast<APlayerCharacter>(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
// 		if (CurArmLength <= CameraArmLenMin + 100.0f)
// 		{
// 			Player->isOpenLookCamera = true;
// 		}
// 		else
// 		{
// 			Player->isOpenLookCamera = false;
// 		}
	}
}

void UGolbalBPFunctionLibrary::SetCameraSocketOffset(class USpringArmComponent* SpringArm, FVector OffsetValue)
{
	const UUECS3GameInstance* GameInstance = UUECS3GameInstance::Instance;
	//用户系统设置
	if (GameInstance && 
		GameInstance->LocalDataSaveManager&&
		GameInstance->LocalDataSaveManager->LocalUserSettingData)
	{
		//判断摄像机臂是否存在
		if (SpringArm)
		{
			//设置偏移				
			SpringArm->SocketOffset = FVector(-GameInstance->LocalDataSaveManager->LocalUserSettingData->VideoSettingData.CameraMaxLen, OffsetValue.Y, OffsetValue.Z);
		}
	}
	else
	{
		//判断摄像机臂是否存在
		if (SpringArm)
		{
			//设置偏移
			SpringArm->SocketOffset = OffsetValue;
		}
	}
}

void UGolbalBPFunctionLibrary::SetCameraFOV(UCameraComponent* CameraComponent, float Fov)
{
	const UUECS3GameInstance* GameInstance = UUECS3GameInstance::Instance;
	//用户系统设置
	if (GameInstance &&
		GameInstance->LocalDataSaveManager&&
		GameInstance->LocalDataSaveManager->LocalUserSettingData)
	{
		//判断摄像机是否存在
		if (CameraComponent)
		{
			//设置fov				
			CameraComponent->SetFieldOfView(GameInstance->LocalDataSaveManager->LocalUserSettingData->VideoSettingData.WideAngle);
		}
	}
	else
	{
		//判断摄像机是否存在
		if (CameraComponent)
		{
			//设置fov				
			CameraComponent->SetFieldOfView(Fov);
		}
	}
}

void UGolbalBPFunctionLibrary::AddCameraHiddenActor(AActor* InActor)
{
	ACS3PlayerController* PlayerController = GetCS3PlayerController();
	if (!IsValid(PlayerController)) return;
	PlayerController->HiddenActors.Add(InActor);
}

FRotator UGolbalBPFunctionLibrary::GetLookAtRotator(const FVector& StartLocation, const FVector& TargetLocation)
{
	FRotator LookRotation = UKismetMathLibrary::FindLookAtRotation(StartLocation, TargetLocation);
	float roll;
	float pitch;
	float yaw;
	UKismetMathLibrary::BreakRotator(LookRotation, roll, pitch, yaw);
	return UKismetMathLibrary::MakeRotator(0.0f, 0.0f, yaw);
}

void UGolbalBPFunctionLibrary::RecoverEntityRotator(const int32& EntityID)
{
	KBEngine::Entity* entity = FindEntity(EntityID);
	if (entity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::RecoverEntityRotator : entity!"));
		return;
	}
	AActor* Actor = entity->Actor();
	AServerCharacter* PlayerActor = GetCS3PlayerCharacter();
	if (IsValid(PlayerActor) && PlayerActor->GetSelfEntity() != nullptr)
	{
		if (IsValid(Actor))
		{
			Actor->SetActorRotation(FQuat::MakeFromEuler(entity->Direction()));
		}
	}



}

UClass* UGolbalBPFunctionLibrary::GetUClassByStr(const FString& Str)
{
	if (!IsValid(UGolbalBPFunctionLibrary::CfgManager())) return nullptr;
	const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_STRTOCLASS);
	FStrToClass* data = const_cast<FStrToClass*>(table->GetRow<FStrToClass>(Str));
	if (data == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetUClassByStr : data!"));
		check(0);
		return nullptr;
	}
	return data->GetTargetClass();
}

class ACS3PlayerController* UGolbalBPFunctionLibrary::GetCS3PlayerController()
{
	if (!IsValid(UUECS3GameInstance::Instance))
	{
		//CS3_Warning(TEXT("-->Null Pointer error:ACS3PlayerController* UGolbalBPFunctionLibrary::GetCS3PlayerController : Instance!"));
		return nullptr;
	}

	if ((UUECS3GameInstance::pKBEApp)&&(UUECS3GameInstance::Instance->CS3PC) && (IsValid(UUECS3GameInstance::Instance->CS3PC)))
	{
		return UUECS3GameInstance::Instance->CS3PC;
	}
	return (ACS3PlayerController *)UGameplayStatics::GetPlayerController(UUECS3GameInstance::Instance->GetWorld(), 0);
}

class AServerCharacter* UGolbalBPFunctionLibrary::GetCS3PlayerCharacter()
{

	if (!IsValid(UUECS3GameInstance::Instance))
	{
		CS3_Warning(TEXT("-->Null Pointer error: AServerCharacter* UGolbalBPFunctionLibrary::GetCS3PlayerController : Instance!"));
		return nullptr;
	}

	if (UUECS3GameInstance::pKBEApp)
	{
		KBEngine::Entity* Player = UUECS3GameInstance::pKBEApp->Player();
		if (Player)
		{
			AServerCharacter* PlayerCharacter = Cast<AServerCharacter>(Player->Actor());
			if (IsValid(PlayerCharacter))
			{
				return PlayerCharacter;
			}
		}
	}
	AServerCharacter* ServerCharacter = Cast<AServerCharacter>(UGameplayStatics::GetPlayerCharacter(UUECS3GameInstance::Instance->GetWorld(), 0));
	if (ServerCharacter)
	{
		return ServerCharacter;
	}
	else
	{
		return nullptr;
	}
}


FString UGolbalBPFunctionLibrary::StrToColorStr(const FString& inputstr, const FString& colorstr)
{
	if (inputstr.ToLower().StartsWith(TEXT("<text")) || inputstr.ToLower().StartsWith(TEXT("<img")))
	{
		return inputstr;
	}
	else
	{
		return FString::Printf(TEXT("<text color=\"#%s\">%s</text>"), *colorstr, *inputstr);
	}
}

TArray<AActor*> UGolbalBPFunctionLibrary::GetActorsInRange(UClass* Class /*= nullptr*/, float Range /*= 200.0f*/, FVector Pos /*= FVector::ZeroVector*/, bool IsSort /*= false*/)
{
	SCOPE_CYCLE_COUNTER(STAT_GetActorsInRange);
	
	static TArray<AActor*> ActorList;
	ActorList.Reset();

	if (!IsValid(UUECS3GameInstance::Instance))
	{
		return ActorList;
	}
	AActor* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(PlayerActor))
	{
		//CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetActorsInRange : PlayerActor!"));
		return ActorList;
	}
	if (UUECS3GameInstance::pKBEApp == nullptr || UUECS3GameInstance::pKBEApp->Entities() == nullptr)
	{
		//CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetActorsInRange :pKBEApp||pKBEApp->Entities()!"));
		return ActorList;
	}
	TMap<int32, KBEngine::Entity*> EntitiesMap = *UUECS3GameInstance::pKBEApp->Entities();
	for (auto& Elem : EntitiesMap)
	{
		KBEngine::Entity* Entity = Elem.Value;
		if (Entity != nullptr)
		{
			if (!Entity->Actor() || PlayerActor == Entity->Actor())
			{
				continue;
			}

			UObjectBase* ActorBase = (UObjectBase*)Entity->Actor();
			bool Result = false;
			int32 Index = GUObjectArray.ObjectToIndex(ActorBase);
			if (GUObjectArray.IsValidIndex(ActorBase))
			{
				// 判断一下找到的东西地址是否一致
				if (ActorBase == GUObjectArray.IndexToObject(Index)->Object)
				{
					Result = true;
				}
			}

			if (Result)
			{
				AActor* Actor = (AActor*)(ActorBase);

				float dist;
				if (Pos.Size() > 0)
				{
					dist = FVector::Dist(Pos, Actor->GetActorLocation());
				}
				else
				{
					dist = GetActorDistance(PlayerActor, Actor);
				}
				
				if (dist <= Range)
				{
					if (!IsValid(Class))
					{	
						ActorList.Add(Actor);
						
					}
					else if (Actor->GetClass()->IsChildOf(Class))
					{
						ActorList.Add(Actor);
					}
				}
				
			}
			else
			{
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("Actor is Invalid"));
			}
		}
	}

	if (IsSort)
	{
		SortActorByDistance(ActorList, PlayerActor);
	}
	return ActorList;
}

TArray<CS3Entity*> UGolbalBPFunctionLibrary::GetCS3EntitysInRange(FString ClassName, float Range, FVector Pos)
{
	static TArray<CS3Entity*> CS3EntityList;
	CS3EntityList.Reset();

	if (!IsValid(UUECS3GameInstance::Instance))
	{
		return CS3EntityList;
	}

	if (UUECS3GameInstance::pKBEApp == nullptr || UUECS3GameInstance::pKBEApp->Entities() == nullptr)
	{
		return CS3EntityList;
	}
	TMap<int32, KBEngine::Entity*> EntitiesMap = *UUECS3GameInstance::pKBEApp->Entities();
	for (auto& Elem : EntitiesMap)
	{
		KBEngine::Entity* Entity = Elem.Value;
		if (Entity != nullptr)
		{
			float dist;
			dist = FVector::Dist2D(Pos, Entity->Position());
			if (dist <= Range)
			{
				if (ClassName == "" || Entity->ClassName() == ClassName)
				{
					CS3EntityList.Add((CS3Entity*)Entity);

				}
			}

		}
	}

	return CS3EntityList;
}

bool UGolbalBPFunctionLibrary::IsInRectangle(FVector dstPos, FVector srcPos, float yaw, float width, float length)
{
	if (dstPos == srcPos)
	{
		return true;
	}
	FVector RDir = FVector(0.0, 0.0, 0.0);
	RDir.X = FMath::Sin(yaw);
	RDir.Z = FMath::Cos(yaw);

	//将朝向的角度转化成弧度
	FVector desDir = dstPos - srcPos;
	FVector desRDir;
	desRDir.X = desDir.X * PI / 180;
	desRDir.Y = desDir.Y * PI / 180;
	desRDir.Z = desDir.Z * PI / 180;
	desRDir.Normalize();
	float dp = FVector::DotProduct(RDir, desRDir);
	if (dp < -1.0)
	{
		dp = -1.0;
	}
	if (dp == 0.0 || dp > 1.0)
	{
		dp = 1;
	}
	float diffYaw = FMath::Acos(dp);
	float dist = FVector::Dist(srcPos, dstPos);
	if (abs(diffYaw) <= PI / 2 && abs(dist * FMath::Sin(diffYaw)) <= width / 2 && abs(dist * FMath::Cos(diffYaw)) <= length)
	{
		return true;
	}
	return false;
}

bool UGolbalBPFunctionLibrary::IsInSector(FVector dstPos, FVector srcPos, float yaw, float radius, float angle)
{
	if (dstPos == srcPos)
	{
		return true;
	}
	float dist = FVector::Dist(srcPos, dstPos);
	if (dist > radius)
	{
		return false;
	}
	
	float halfRAngle = angle * PI / 360;
	FVector RDir = FVector(0.0, 0.0, 0.0);
	RDir.X = FMath::Sin(yaw);
	RDir.Z = FMath::Cos(yaw);

	//将朝向的角度转化成弧度
	FVector desDir = dstPos - srcPos;
	FVector desRDir;
	desRDir.X = desDir.X * PI / 180;
	desRDir.Y = desDir.Y * PI / 180;
	desRDir.Z = desDir.Z * PI / 180;
	desRDir.Normalize();
	float dp = FVector::DotProduct(RDir, desRDir);
	if (dp < -1.0)
	{
		dp = -1.0;
	}
	if (dp == 0.0 || dp > 1.0)
	{
		dp = 1;
	}
	float rAngle = FMath::Acos(dp);
	if (rAngle <= halfRAngle)
	{
		return true;
	}
	return false;
}

bool UGolbalBPFunctionLibrary::IsPureAnsi(const FString& SourceString)
{
	if (SourceString.IsEmpty())
	{
		return true;
	}

	return FCString::IsPureAnsi(*SourceString);
}

int32 UGolbalBPFunctionLibrary::GetStringBytes(const FString& SourceString)
{
	int32 TotalBytes = 0;
	const WIDECHAR* Str = *SourceString;
	for (; *Str; Str++)
	{
		if (*Str > 0x7f)
		{
			TotalBytes+= 2;
		}
		else
		{
			TotalBytes += 1;
		}
	}
	return TotalBytes;
}

UTexture2D* UGolbalBPFunctionLibrary::GetIconBySkillID(int32 SkillId)
{
	if (!IsValid(UGolbalBPFunctionLibrary::SkillManager())) return nullptr;
	return UGolbalBPFunctionLibrary::SkillManager()->GetIconBySkillID(SkillId);

}

FString UGolbalBPFunctionLibrary::GetDescriptionBySkillID(int32 SkillId)
{
	if (!IsValid(UUECS3GameInstance::Instance->SkillManager)) return  TEXT("");
	USkillData* SkillData = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(SkillId);
	if (SkillData)
	{
		FString SkillDes = SkillData->GetDescription();
		return SkillDes;
	}
	else
	{
		return TEXT("");
	}
}

FString UGolbalBPFunctionLibrary::GetNameBySkillID(int32 SkillId)
{
	USkillData* SkillData = UUECS3GameInstance::Instance->SkillManager->GetSkillDataById(SkillId);
	if (SkillData)
	{
		FString SkillName = SkillData->GetSkillName();
		return SkillName;
	}
	else
	{
		return TEXT("");
	}
}

FString UGolbalBPFunctionLibrary::GetReplaceString(const FString& replaceString, const FString args /*= TEXT("")*/, FString SplitChar /*= TEXT("|")*/)
{
	//把提示信息中的参数用传入的参数进行填充
	FString MsgArgs = args;
	TArray<FStringFormatArg> ArgsArray;
	FString left, right;
	bool result = true;
	while (!MsgArgs.IsEmpty())
	{
		result = MsgArgs.Split(SplitChar, &left, &right, ESearchCase::Type::CaseSensitive);
		if (result)
		{
			MsgArgs = right;
			ArgsArray.Add(left);
		}
		else
		{
			ArgsArray.Add(MsgArgs);
			MsgArgs = TEXT("");
		}
	}
	FString infoMessage;
	if (ArgsArray.Num() > 0)
		infoMessage = FString::Format(*(replaceString), ArgsArray);
	else
		infoMessage = replaceString;
	return infoMessage;
}

FString UGolbalBPFunctionLibrary::Int64ToString(int64 moneyValue) {

	return INT64_TO_FSTRING(moneyValue);
}


int64 UGolbalBPFunctionLibrary::StringToInt64(const FString& moneyValue) {

	return FSTRING_TO_INT64(moneyValue);
}

int32 UGolbalBPFunctionLibrary::GetIntegerFieldByKey(const FString& SrcString, const FString& Key)
{
	int32 TempValue = -1;
	TSharedRef<TJsonReader<TCHAR>> JsonReader = TJsonReaderFactory<TCHAR>::Create(SrcString);
	TSharedPtr<FJsonObject> JsonParsed;
	bool isDeserialized = FJsonSerializer::Deserialize(JsonReader, JsonParsed);

	if (!SrcString.IsEmpty() && isDeserialized)
	{
		TempValue = JsonParsed->GetIntegerField(Key);
	}
	return TempValue;
}

FString UGolbalBPFunctionLibrary::GetFormatColorString(const FString& replaceString)
{
	///实现原理，首先拷贝一份,在每次替换{左边的为富文本，最后最后一个
	if (replaceString.IsEmpty()) return TEXT("");
	FString temp;
	temp = *replaceString;
	FString result;
	FString left, right;
	bool bIsFind = true;
	while (!temp.IsEmpty())
	{
		bIsFind = temp.Split(TEXT("{"), &left, &right, ESearchCase::Type::CaseSensitive);
		if (bIsFind)
		{
			temp = right;
			result.Append(StrToColorStr(left));
			result.Append(TEXT("{"));
			bool bIsFind1 = temp.Split(TEXT("}"), &left, &right, ESearchCase::Type::CaseSensitive);
			if (bIsFind1)
			{
				result.Append(left);
				result.Append(TEXT("}"));
				temp = right;
			}
		}
		else
		{	//处理最后一个右边字符串替换为富文本
			result.Append(StrToColorStr(temp));
			temp = TEXT("");
		}
	}

	return result;
}

FString UGolbalBPFunctionLibrary::ConvertRichTextToCommonText(FString InRichText)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->HyperlinkManager))
	{
		return UUECS3GameInstance::Instance->HyperlinkManager->ConvertRichTextToCommonText(InRichText);
	}
	return InRichText;
}

AActor* UGolbalBPFunctionLibrary::SpawnActorByConfig(UObject* WorldContextObject, const FString& ActorStr)
{
	UWorld* World = GEngine->GetWorldFromContextObjectChecked(WorldContextObject);
	if (IsValid(World) && IsValid(UGolbalBPFunctionLibrary::CfgManager()))
	{
		const UConfigTable* table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(
			CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_SPAWN_TRANSFORM);
		const FSpawnTransform* SpawnData = table->GetRow<FSpawnTransform>(ActorStr);
		AActor* SpawnActor = UGolbalBPFunctionLibrary::SpawnActor<AActor>(SpawnData->SpawnClass);
		if (IsValid(SpawnActor))
		{
			SpawnActor->SetActorTransform(SpawnData->Transform);
		}
		return SpawnActor;
	}
	return nullptr;
}

FVector UGolbalBPFunctionLibrary::GetMouseWorldPos()
{
	UWorld* World = UUECS3GameInstance::Instance->GetWorld();
	FVector2D ScreenPosition;
	APlayerController* PlayerController = World->GetFirstPlayerController();
	if (PlayerController && PlayerController->GetMousePosition(ScreenPosition.X, ScreenPosition.Y))
	{
		FHitResult TraceHitResult;
		FCollisionQueryParams TraceParams = FCollisionQueryParams(FName(TEXT("ComputeFloorDistSweep")), true);
		TraceParams.bTraceComplex = true;
		TraceParams.AddIgnoredActor(UGolbalBPFunctionLibrary::GetCS3PlayerCharacter());
		TArray<AActor*> AllActors = GetActorsInRange(nullptr, 8000.f);
		for (auto It = AllActors.CreateConstIterator(); It; ++It)
		{
			if (AllActors[It.GetIndex()]->GetClass()->IsChildOf(AMovingPlatformCharacter::StaticClass()))
			{
				continue;
			}
			TraceParams.AddIgnoredActor(AllActors[It.GetIndex()]);

		}

		PlayerController->GetHitResultAtScreenPosition(ScreenPosition, PlayerController->CurrentClickTraceChannel, TraceParams, TraceHitResult);
		if (TraceHitResult.bBlockingHit)
		{
			return TraceHitResult.ImpactPoint;
		}
	}
	return FVector::ZeroVector;
}

bool UGolbalBPFunctionLibrary::FindPathToLocation(const FVector& GoalPos)
{
	//UNavigationSystem *const NavSys = UUECS3GameInstance::Instance->GetWorld()->GetNavigationSystem();
	UNavigationSystemV1 *const NavSys = FNavigationSystem::GetCurrent<UNavigationSystemV1>(UUECS3GameInstance::Instance->GetWorld());
	APlayerController* PlayerController = UUECS3GameInstance::Instance->GetWorld()->GetFirstPlayerController();
	if (!IsValid(PlayerController))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::FindPathToLocation : PlayerController!"));
		return false;
	}
	const ANavigationData* NavData = NavSys->GetNavDataForProps(PlayerController->GetNavAgentPropertiesRef());
	if (!IsValid(NavData))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::FindPathToLocation : NavData!"));
		return false;
	}
	FPathFindingQuery Query(PlayerController, *NavData, PlayerController->GetNavAgentLocation(), GoalPos);
	FPathFindingResult Result = NavSys->FindPathSync(Query);
	if (Result.IsSuccessful()) return true;
	return false;
}

FString UGolbalBPFunctionLibrary::SetFontStyle(const FString& FontPath, const FString& FontType, const FString& FontSize, const FString& Color, const FString& ShadowColor, const FString& ShadowOffset)
{
	return TEXT("<text fontPath=") + FontPath + TEXT(" fontType=") + FontType + TEXT(" fontSize=") + FontSize + TEXT(" color=") + Color + TEXT(" shadowColor=") + ShadowColor + TEXT(" shadowOffset=") + ShadowOffset + TEXT(">");
}

UItemFactory* UGolbalBPFunctionLibrary::ItemFactory()
{
	return IsValid(UUECS3GameInstance::Instance) ? UUECS3GameInstance::Instance->ItemFactory : nullptr;
}

FString UGolbalBPFunctionLibrary::GetChatMsgColorString(const FString& MsgStr, const FString& ColorStr)
{
	///实现原理，首先拷贝一份,在每次替换{左边的为富文本，最后最后一个
	if (MsgStr.IsEmpty()) return TEXT("");
	FString temp;
	temp = *MsgStr;
	FString result;
	FString left, right;
	bool bIsFind = true;
	while (!temp.IsEmpty())
	{
		bIsFind = temp.Split(TEXT("<text"), &left, &right, ESearchCase::Type::CaseSensitive);
		if (bIsFind)
		{
			temp = right;
			result.Append(StrToColorStr(left, ColorStr));
			result.Append(TEXT("<text"));
			bool bIsFind1 = temp.Split(TEXT("</text>"), &left, &right, ESearchCase::Type::CaseSensitive);
			if (bIsFind1)
			{
				result.Append(left);
				result.Append(TEXT("</text>"));
				temp = right;
			}
		}
		else
		{	//处理最后一个右边字符串替换为富文本
			result.Append(StrToColorStr(temp, ColorStr));
			temp = TEXT("");
		}
	}
	return result;
}

TMap<int32, AActor*> UGolbalBPFunctionLibrary::LessTmap(TMap<int32, AActor*> Listmap)
{
	Listmap.KeySort(TLess<int32>());
	return Listmap;
}

FString UGolbalBPFunctionLibrary::GetFormatImgStr(const FString& replaceString, const FString& ColorStr)
{
	if (replaceString.IsEmpty()) return TEXT("");
	FString Temp;
	Temp = *replaceString;
	FString FormatResult;
	FString LeftStr, RightStr;
	bool bIsFindLeft = true;
	while (!Temp.IsEmpty())
	{
		bIsFindLeft = Temp.Split(TEXT("<img"), &LeftStr, &RightStr, ESearchCase::Type::CaseSensitive);
		if (bIsFindLeft)
		{
			Temp = RightStr;
			FString ColorLeftStr = StrToColorStr(LeftStr, ColorStr);
			FormatResult.Append(ColorLeftStr);
			bool bIsFindRight = Temp.Split(TEXT("/>"), &LeftStr, &RightStr, ESearchCase::Type::CaseSensitive);
			if (bIsFindRight)
			{
				FString ImgStr = TEXT("<img") + LeftStr + TEXT("/>");
				FormatResult.Append(ImgStr);
				Temp = RightStr;
			}
		}
		else
		{	//处理最后一个右边字符串替换为表情字符串
			FString ColorTempStr = StrToColorStr(Temp, ColorStr);
			FormatResult.Append(ColorTempStr);
			//			FormatResult.Append(Temp);
			Temp = TEXT("");
		}
	}
	return FormatResult;
}

float UGolbalBPFunctionLibrary::GetActorDistance(AActor* SrcActor, AActor* DstActor)
{
	if (!IsValid(SrcActor) || !IsValid(DstActor))
	{
		return MAX_flt;
	}
	AServerCharacter* SrcCharacter = Cast<AServerCharacter>(SrcActor);
	AServerCharacter* DstCharacter = Cast<AServerCharacter>(DstActor);
	if (!IsValid(SrcCharacter) || !IsValid(DstCharacter))
	{
		//CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetActorDistance : SrcCharacter||DstCharacter!"));
		return SrcActor->GetDistanceTo(DstActor);
	}
	else
	{
		GameObject* SrcEntity = (GameObject*)(SrcCharacter->GetSelfEntity());
		GameObject* DstEntity = (GameObject*)(DstCharacter->GetSelfEntity());
		if (SrcEntity == nullptr || DstEntity == nullptr)
		{
			//CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetActorDistance : SrcEntity||DstEntity!"));
			return SrcActor->GetDistanceTo(DstActor);
		}
		else
		{
			FVector SrcPosition = SrcEntity->Position();
			FVector DstPosition = DstEntity->Position();
			float Dis = FVector::Distance(SrcPosition, DstPosition);
			return Dis;
		}
	}
}

float UGolbalBPFunctionLibrary::GetActorDistanceByJump(AActor* SrcActor, AActor* DstActor)
{
	if (!IsValid(SrcActor) || !IsValid(DstActor))
	{
		return MAX_flt;
	}
	AServerCharacter* SrcCharacter = Cast<AServerCharacter>(SrcActor);
	AServerCharacter* DstCharacter = Cast<AServerCharacter>(DstActor);
	if (!IsValid(SrcCharacter) || !IsValid(DstCharacter))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetActorDistanceByJump : SrcCharacter||DstCharacter!"));
		return SrcActor->GetDistanceTo(DstActor);
	}

	GameObject* SrcEntity = (GameObject*)(SrcCharacter->GetSelfEntity());
	GameObject* DstEntity = (GameObject*)(DstCharacter->GetSelfEntity());
	if (SrcEntity == nullptr || DstEntity == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetActorDistanceByJump : SrcEntity||DstEntity!"));
		return SrcActor->GetDistanceTo(DstActor);
	}

	FVector SrcPosition = SrcEntity->Position();
	FVector DstPosition = DstEntity->Position();
	DstPosition.Z = SrcPosition.Z;
	float Dis = FVector::Distance(SrcPosition, DstPosition);
	return Dis;
}

FString& UGolbalBPFunctionLibrary::HandleLineFeeds(FString& Line)
{
	if (!Line.EndsWith(TEXT("\n")))
	{
		Line += TEXT("\n");
	}
	return Line;
}

void UGolbalBPFunctionLibrary::CheckFileInPathByPrefix(const FString& DirectoryPath, TArray<FString>& NameFix, const FString Prefix, TArray<FString>& NameAssets)
{
	FString SubPath = DirectoryPath;
	SubPath.RemoveFromStart("/Game");
	FString SearchPath = FPaths::GetPath(FPaths::GetProjectFilePath()) + "/Content" + SubPath;
	if (FPaths::DirectoryExists(SearchPath))
	{
		TArray<FString> outputs;
		FString SearchName = Prefix + "*";
		FFileManagerGeneric::Get().FindFilesRecursive(outputs, *SearchPath, *SearchName, true, false);
		for (FString file : outputs)
		{
			FString PackageName;
			bool ConvertResult = FPackageName::TryConvertFilenameToLongPackageName(file, PackageName);//如果存在一些冲突文件，比如BP_SkillBarListWidget.uasset.r9844，这个文件就不能转换成功，会引起崩溃，这里改用尝试转换的方法
			if (ConvertResult)
			{
				FString PackagePath = PackageName + TEXT(".")  + FPackageName::GetLongPackageAssetName(PackageName);
				NameFix.Add(PackagePath);
				NameAssets.Add(PackageName);
			}
		}
	}
}

bool UGolbalBPFunctionLibrary::CheckResourceFileIsExist(const FString& ResourceFile)
{
	FString NewResourceFile = ResourceFile;
	int32 NameStartIndex = INDEX_NONE;
	NewResourceFile.FindChar(TCHAR('\''), NameStartIndex);
	if (NameStartIndex != INDEX_NONE)
	{
		int32 NameEndIndex = INDEX_NONE;
		NewResourceFile.FindLastChar(TCHAR('\''), NameEndIndex);
		if (NameEndIndex > NameStartIndex)
		{
			NewResourceFile = NewResourceFile.Mid(NameStartIndex + 1, NameEndIndex - NameStartIndex - 1);
		}
		else
		{
			return false;
		}
	}
	if (!FPackageName::IsValidObjectPath(NewResourceFile))
	{
		return false;
	}
	FString PackageName = FPackageName::ObjectPathToPackageName(NewResourceFile);
	FString FilePath;
	// Try to convert this to a file path
	if (FPackageName::DoesPackageExist(PackageName, 0, &FilePath) == false)
	{
		return false;
	}

	// if that succeeded FilePath will be a relative path to a  file, if not just assume that's what we were given and proceed...
	if (IFileManager::Get().FileExists(*FilePath) == false)
	{
		return false;
	}

	const FAssetRegistryModule& AssetRegistryModule = FModuleManager::LoadModuleChecked<FAssetRegistryModule>(TEXT("AssetRegistry"));
	const FAssetData AssetData = AssetRegistryModule.Get().GetAssetByObjectPath(*ResourceFile);

	if (AssetData.IsValid())
	{
		return true;
	}
	return false;
}

FString UGolbalBPFunctionLibrary::GetServerIP()
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		return UUECS3GameInstance::Instance->GameDefault->ServerIPAddress;
	}
	else
	{
		return TEXT("127.0.0.1");
	}
}

FString UGolbalBPFunctionLibrary::ConvertKeysToKeyString(FInputKeyEvent keys)
{
	FString KeyString = "";
	bool BIsDoubleClick = false;
	for (auto & keydata : keys.KeyDatas)
	{
		if (keydata.IE == EINPUT_EVENT::IE_DoubleClick)
		{
			BIsDoubleClick = true;
		}
		if (keydata.Type == EINPUT_TYPE::IT_Action)
		{
			if (keydata.Ctrl)
			{
				KeyString = KeyString + TEXT("Ctrl+");
			}
			if (keydata.Shift)
			{
				KeyString = KeyString + TEXT("Shift+");
			}
			if (keydata.Alt)
			{
				KeyString = KeyString + TEXT("Alt+");
			}
			if (keydata.Cmd)
			{
				KeyString = KeyString + TEXT("Cmd+");
			}
			break;
		}
	}
	if (BIsDoubleClick)
	{
		KeyString = KeyString + TEXT("双击") + FNAME_TO_FSTRING(keys.Key.GetDisplayName());
	}
	else
	{
		KeyString = KeyString + FNAME_TO_FSTRING(keys.Key.GetDisplayName());
	}

	return KeyString;
}

FGROUPKEY_DATA UGolbalBPFunctionLibrary::ConvertKeysToGroupKey(TArray<FKey>Keys)
{
	///<将Keys转换成FGROUPKEY_DATA类型
	FGROUPKEY_DATA GroupKey;
	GroupKey.Shift = false;
	GroupKey.Ctrl = false;
	GroupKey.Alt = false;
	GroupKey.Cmd = false;
	GroupKey.DoubleClick = false;

	for (auto& dataKey : Keys)
	{
		if (FNAME_TO_FSTRING(dataKey.GetDisplayName()).Contains("Shift"))
		{
			GroupKey.Shift = true;
			continue;
		}
		if (FNAME_TO_FSTRING(dataKey.GetDisplayName()).Contains("Ctrl"))
		{
			GroupKey.Ctrl = true;
			continue;
		}
		if (FNAME_TO_FSTRING(dataKey.GetDisplayName()).Contains("Alt"))
		{
			GroupKey.Alt = true;
			continue;
		}
		if (FNAME_TO_FSTRING(dataKey.GetDisplayName()).Contains("Cmd"))
		{
			GroupKey.Cmd = true;
			continue;
		}
		if (dataKey.IsValid())
		{
		GroupKey.Key = dataKey;
		}		
	}
	return GroupKey;
}

float UGolbalBPFunctionLibrary::GetDeltaTime()
{
	return FApp::GetDeltaTime();
}

FString UGolbalBPFunctionLibrary::GetValidNumericInput(const FString& SourceString, int32 InMinValue/*= 0*/, int32 InMaxValue/*= 100*/)
{
	//判断是不是纯数字，IsNumeric包括正负号，小数点，数字，都会返回True
	if (SourceString.IsNumeric())
	{
		int32 tempValue = FSTRING_TO_INT(SourceString);
		return INT_TO_FSTRING(FMath::Clamp<int32>(tempValue, InMinValue, InMaxValue));
	}
	else
	{
		//剔除字符串最后一个元素
		int32 tempValidLength = SourceString.Len() - 1;
		return (tempValidLength >= 1 ? SourceString.Mid(0, tempValidLength) : FString());
	}
}

ALevelScriptActor* UGolbalBPFunctionLibrary::GetMainLevelActor()
{
	if (IsValid(UUECS3GameInstance::Instance))
	{
		UWorld* World = UUECS3GameInstance::Instance->GetWorld();
		if (IsValid(World))
		{
			return World->PersistentLevel->LevelScriptActor;
		}
	}
	return nullptr;
}

TArray<FVector> UGolbalBPFunctionLibrary::GetNavigateGuidPath(float GuideDistance /* = 300.0 */)
{
	TArray<FVector> NavigateGuidePathList;
	APlayerCharacter* Player = Cast<APlayerCharacter>(GetCS3PlayerCharacter());
	if (!IsValid(Player))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetNavigateGuidPath : Player!"));
		return NavigateGuidePathList;
	}
	else
	{
		TArray<FVector> PathList = Player->GetAutoNavPathPoints();
		if (PathList.Num() <= 1)
		{
			return NavigateGuidePathList;
		}
		else
		{
			NavigateGuidePathList = AnalysicsPathList(PathList, GuideDistance);
			return NavigateGuidePathList;
		}
	}

}

TArray<FVector2D> UGolbalBPFunctionLibrary::CreateSameIntervalPixels(const TArray<FVector2D>& InPixelList, float PixelDistance /*= 8.0*/)
{
	TArray<FVector2D> OutPointList;
	float tempDistance;
	FVector2D tempPoint;//用来做参考的点
	if (InPixelList.Num()>1)
	{
		tempPoint = InPixelList[0];
		OutPointList.Add(tempPoint);
		for (int32 i =1; i<InPixelList.Num(); i++ )
		{
			tempDistance = (InPixelList[i] - tempPoint).Size();//计算两点之间的距离
			//此处用while循环，因为距离可能不止一个间距，可能是2倍，或更多倍间距
			while (tempDistance >= PixelDistance)
			{
				//等间距插入点
				tempPoint = FMath::Vector2DInterpConstantTo(tempPoint, InPixelList[i], 1, PixelDistance);
				OutPointList.Add(tempPoint);
				tempDistance = (InPixelList[i] - tempPoint).Size();
			}
		}
		return OutPointList;
	}
	else
	{
		return InPixelList;
	}
}

float UGolbalBPFunctionLibrary::GetViewportScale()
{
	const FVector2D ViewportSize = GetViewportSize();
	const float ViewportScale = GetDefault<UUserInterfaceSettings>(UUserInterfaceSettings::StaticClass())->GetDPIScaleBasedOnSize(FIntPoint(ViewportSize.X, ViewportSize.Y));
	return ViewportScale;
}

FVector2D UGolbalBPFunctionLibrary::GetViewportSize()
{
	//获取窗口Size
	if (IsValid(GEngine->GameViewport) && GEngine->GameViewport->Viewport != nullptr)
	{
		const FVector2D ViewportSize = FVector2D(GEngine->GameViewport->Viewport->GetSizeXY());
		if (!ViewportSize.IsZero())
		{
			return ViewportSize;
		}
	}
	FString Resolution = TEXT("");
	//窗口Size获取不到，去系统配置表获取配置的分辨率
	ULocalUserSettingData* LocalUserSettingData = UUECS3GameInstance::Instance->LocalDataSaveManager->LocalUserSettingData;
	if (IsValid(LocalUserSettingData))
	{
		Resolution = LocalUserSettingData->VideoSettingData.Resolution;
	}
	if (Resolution.IsEmpty())
	{
		//窗口Size获取不到，系统配置表也获取不到配置的分辨率，去默认系统配置表获取默认分辨率
		const UConfigTable* SystemDefaultTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_SYSTEM_DEFAULT_DATA);
		if (IsValid(SystemDefaultTable))
		{
			FName RowID = TEXT("1");
			const FSYSTEM_DEFAULT_DATA* SystemData = SystemDefaultTable->GetRow<FSYSTEM_DEFAULT_DATA>(RowID);
			if (SystemData)
			{
				Resolution = SystemData->VideoData.Resolution;
			}
		}
	}
	if (!Resolution.IsEmpty())
	{
		TArray<FString> ResolutionArray = UGolbalBPFunctionLibrary::SplitString(Resolution, false, "x");
		if (ResolutionArray.Num() == 2)
		{
			float ResolutionX = FSTRING_TO_FLOAT(ResolutionArray[0]);
			float ResolutionY = FSTRING_TO_FLOAT(ResolutionArray[1]);
			return FVector2D(ResolutionX, ResolutionY);
		}
	}

	//都获取不到，写死默认，不会走到这里
	return FVector2D(1600.0f, 900.0f);
}

bool UGolbalBPFunctionLibrary::GetNPCPositionFromTable(FString DstSpaceName, FString NPCScriptID, FVector& NPCPosition)
{
	const UConfigTable* NPCPositionTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_NPC_POINT_DATAS);
	const FSPACE_NPC_ID_TO_POSITION* NPCPositionData = NPCPositionTable->GetRow<FSPACE_NPC_ID_TO_POSITION>(DstSpaceName);
	if (NPCPositionData != nullptr)
	{
		TArray<FNPC_ID_TO_POSITION> NPCIDToPositions = NPCPositionData->NPCIDToPositions;
		for (auto NPCIDToPosition : NPCIDToPositions)
		{
			FString NPCID = NPCIDToPosition.NPCID;
			if (NPCID.Equals(NPCScriptID))
			{
				NPCPosition = NPCIDToPosition.Position;
				return true;
			}
		}
	}
	return false;
}

bool UGolbalBPFunctionLibrary::GetNPCPositionFromTableWithNPCScriptID(FString NPCScriptID, FString& spaceScriptID, FVector& NPCPosition)
{
	const UConfigTable* NPCPositionTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_NPC_POINT_DATAS);
	TArray<FName>rowNames = NPCPositionTable->GetRowNames();
	for (auto rowName: rowNames)
	{
		const FSPACE_NPC_ID_TO_POSITION* NPCPositionData = NPCPositionTable->GetRow<FSPACE_NPC_ID_TO_POSITION>(rowName);

		if (NPCPositionData != nullptr)
		{
			TArray<FNPC_ID_TO_POSITION> NPCIDToPositions = NPCPositionData->NPCIDToPositions;
			for (auto NPCIDToPosition : NPCIDToPositions)
			{
				FString NPCID = NPCIDToPosition.NPCID;
				if (NPCID.Equals(NPCScriptID))
				{
					NPCPosition = NPCIDToPosition.Position;
					spaceScriptID = rowName.ToString();
					return true;
				}
			}
		}
	}
	return false;
}



FVector UGolbalBPFunctionLibrary::FStringToFVector(FString PosStr)
{
	FVector DstPos = FVector::ZeroVector;
	TArray<FString> SplitArray = SplitString(PosStr, false, TEXT(" "));
	if (SplitArray.Num() == 3)
	{
		DstPos.X = FSTRING_TO_FLOAT(*SplitArray[0]);
		DstPos.Y = FSTRING_TO_FLOAT(*SplitArray[1]);
		DstPos.Z = FSTRING_TO_FLOAT(*SplitArray[2]);
	}
	return DstPos;
}


bool UGolbalBPFunctionLibrary::IsAllChineseChar(FString MsgText)
{
	FRegexPattern ChinesePattern = FRegexPattern(TEXT("^[\u4e00-\u9FA5]+$"));
	FRegexMatcher ChineseMatcher(ChinesePattern, MsgText);
	if (ChineseMatcher.FindNext())
	{
		return true;
	}
	return false;
}

bool UGolbalBPFunctionLibrary::IsDigit(FString SourceString)
{
	if (SourceString.Contains(TEXT(".")) || SourceString.Contains(TEXT("-")))
	{
		return false;
	}
	else
	{
		return SourceString.IsNumeric();
	}
}

FString UGolbalBPFunctionLibrary::ConvertLinearColorToHex(FLinearColor InLinearColor)
{
	FColor Color = InLinearColor.ToFColor(true);//ToFColor使用了const修饰函数，直接return InLinearColor.ToFColor(true).ToHex(); 值不正确
	return Color.ToHex();
}

float UGolbalBPFunctionLibrary::GetMouseMoveSpeed()
{
	int32 MouseSpeed = 0;
	SystemParametersInfo(SPI_GETMOUSESPEED, 0, &MouseSpeed, 0);
	return (float)MouseSpeed / 10;
}

bool UGolbalBPFunctionLibrary::StringContains(const FString& source, const FString& target)
{
	if (source == "" || target == "")
		return false;

	bool contain = false;
	for (size_t i = 0; i < target.Len(); i++)
	{
		for (size_t j = 0; j < source.Len(); j++)
		{
			if (target[i] == source[j])
			{
				contain = true;
				break;
			}
		}
		if (contain)
			contain = false;
		else
			return false;
	}
	return true;
}

void UGolbalBPFunctionLibrary::RefreshHLString(const FString& CurStr, FString OldStr, const TArray<FString> RichTextStrs, const TArray<int32> RichTextIndex, const TArray<FString>InputBoxTextStrs, FChatHyperlinkData& ChatHyperlinkData)
{
	if (CurStr == "" || OldStr == "")
		return ;
	ChatHyperlinkData.ResultStr = CurStr;
	ChatHyperlinkData.RichTextStrs = RichTextStrs;
	ChatHyperlinkData.RichTextIndex = RichTextIndex;
	ChatHyperlinkData.InputBoxTextStrs = InputBoxTextStrs;
	///一样不需要改变
	if (!CurStr.Compare(OldStr))
		return ;

	int32 CurStartIndex = -1, CurEndIndex = -1;
	int32 OldStartIndex = -1, OldEndIndex = -1;
	bool IsAdd = CurStr.Len() < OldStr.Len() ? false : true;

	if (IsAdd)
	{
		for (size_t i = 0; i < CurStr.Len(); i++)
		{
			if (CurStartIndex < 0)
			{
				if (i < OldStr.Len())
				{
					if (CurStr[i] != OldStr[i])
					{
						CurStartIndex = i;
						OldStartIndex = CurStartIndex;
					}
					else
					{
						FString CurSubstring = UKismetStringLibrary::GetSubstring(CurStr, i, CurStr.Len() - i);
						int32 FindIndex = (CurSubstring.Len() > OldStr.Len()) ? UKismetStringLibrary::FindSubstring(CurSubstring, OldStr) : UKismetStringLibrary::FindSubstring(OldStr, CurSubstring);
						if (FindIndex > -1)
						{
							if (CurSubstring.Len() > OldStr.Len())
							{								
								if (FindIndex>0)
								{
									CurEndIndex = i + FindIndex - 1;
									OldStartIndex = -1;
									OldEndIndex = -1;
									CurStartIndex = i;
								}
								else
								{									
									CurEndIndex = i + OldStr.Len();
									OldStartIndex = OldStr.Len();
									OldEndIndex = OldStr.Len();
									CurStartIndex = CurEndIndex;
								}
							}
							else
							{								
								CurEndIndex = i - FindIndex - 1;
								if (CurEndIndex > 0)
								{
									OldStartIndex = -1;
									OldEndIndex = -1;
								}
								else
								{
									OldStartIndex = OldStr.Len();
									OldEndIndex = OldStr.Len();
								}
								CurStartIndex = CurEndIndex;
							}				
							
							break;
						}
					}
				}
				else
				{
					CurStartIndex = i;
					CurEndIndex = CurStr.Len() - 1;
					OldEndIndex = OldStr.Len();
					OldStartIndex = OldStr.Len();
					break;
				}
			}
			else
			{
				FString CurSubstring = UKismetStringLibrary::GetSubstring(CurStr, i, CurStr.Len() - i);
				int32 FindIndex = CurSubstring.Len() > (OldStr.Len() - OldStartIndex) ? UKismetStringLibrary::FindSubstring(CurSubstring, OldStr) : UKismetStringLibrary::FindSubstring(OldStr, CurSubstring, false,false, OldStartIndex);
				if (FindIndex > -1)
				{
					if (CurSubstring.Len() > (OldStr.Len()- OldStartIndex))
					{
						OldEndIndex = OldStartIndex;
						CurEndIndex = i + FindIndex - 1;
					}
					else if(CurSubstring.Len()< (OldStr.Len() - OldStartIndex))
					{
						CurEndIndex = i - 1;
						OldEndIndex = OldStartIndex + FindIndex;
					}
					else
					{
						OldEndIndex = OldStartIndex - 1;
						CurEndIndex = i - 1;
					}
					break;
				}
			}
		}
	}
	else
	{
		for (size_t i = 0; i < CurStr.Len(); i++)
		{
			if (CurStartIndex < 0)
			{
				if (CurStr[i] != OldStr[i])
				{
					CurStartIndex = i;
					OldStartIndex = CurStartIndex;
					FString CurSubstring = UKismetStringLibrary::GetSubstring(CurStr, i, CurStr.Len() - i);
					int32 FindIndex = UKismetStringLibrary::FindSubstring(OldStr, CurSubstring, false, false, i);
					if (FindIndex > -1)
					{
						OldEndIndex = FindIndex - 1;
						CurEndIndex = i;
						break;
					}
				}
				else
				{
					FString CurSubstring = UKismetStringLibrary::GetSubstring(CurStr, i, CurStr.Len() - i);
					int32 FindIndex = UKismetStringLibrary::FindSubstring(OldStr, CurSubstring);
					if (FindIndex > -1)
					{
						if (FindIndex > 0)
						{
							OldStartIndex = i;
							OldEndIndex = FindIndex - 1;
							CurStartIndex = -1;
							CurEndIndex = CurStartIndex;
						}
						else
						{
							CurEndIndex = CurStr.Len();
							OldEndIndex = CurSubstring.Len() + FindIndex;
							OldStartIndex = OldEndIndex;
							CurStartIndex = CurStr.Len();
						}
						break;
					}
				}
			}
			else
			{
				FString CurSubstring = UKismetStringLibrary::GetSubstring(CurStr, i, CurStr.Len() - i);
				int32 FindIndex = UKismetStringLibrary::FindSubstring(OldStr, CurSubstring, false, false, CurStartIndex);
				if (FindIndex > -1)
				{
					OldEndIndex = FindIndex - 1;
					CurEndIndex = i - 1;
					break;
				}
			}
		}
	}
	
	///<没有修改快捷键
	if (OldStartIndex == OldEndIndex && OldStartIndex == OldStr.Len())
		return;

	///<判断是否修改超链接
	if ((OldStartIndex < OldEndIndex) || (OldStartIndex != -1 && OldStartIndex == OldEndIndex)||(OldStartIndex == (OldEndIndex+1 )&&IsAdd))
	{
		int32 RichStartIndex = -1, RichEndIndex = -1;
		for (size_t i = 0; i < InputBoxTextStrs.Num() && i < RichTextIndex.Num(); i++)
		{
			int32 Len = RichTextIndex[i] + InputBoxTextStrs[i].Len() - 1;

			if ((RichStartIndex == -1) && OldStartIndex <= Len && (OldStartIndex> RichTextIndex[i]|| OldStartIndex== RichTextIndex[i]))
			{
				RichStartIndex = i;
			}
			if (OldEndIndex <= Len && (OldEndIndex > RichTextIndex[i] || OldEndIndex == RichTextIndex[i]))
			{
				RichEndIndex = i;
			}
			///<在该位置快捷键插入
			if (RichEndIndex == RichStartIndex && OldStartIndex == RichTextIndex[i] && IsAdd)
			{
				RichStartIndex = -1;
				RichEndIndex = -1;
			}
		}

		if (OldStartIndex == (OldEndIndex + 1) && IsAdd && RichStartIndex>-1&& RichStartIndex!= RichEndIndex)
		{
			RichStartIndex = -1;
			RichEndIndex = -1;
		}

		if (RichStartIndex > -1 || RichEndIndex > -1)
		{
			int32 RemoveNum = 0;
			for (size_t i = 0; i < InputBoxTextStrs.Num() && i < RichTextIndex.Num(); i++)
			{
				if (RichStartIndex == i)
				{
					///<删除当前Str 的CurStartIndex想左（OldStartIndex-RichTextIndex[i]）个字符
					///<右边需要判断是否CurEndIndex在(OldStartIndex- int32 Len = RichTextIndex[i] + InputBoxTextStrs[i].Len())范围内进行右边删除
					if ((OldStartIndex - RichTextIndex[i]) > 0)
					{
						int32 count = 0;
						for (size_t j = CurStartIndex - 1; count < (OldStartIndex - RichTextIndex[i]) && j >= (CurStartIndex - (OldStartIndex - RichTextIndex[i])); j--)
						{
							ChatHyperlinkData.ResultStr.RemoveAt(j);
							RemoveNum++;
							count++;
						}
					}
					if ((OldStartIndex == OldEndIndex && OldEndIndex != (RichTextIndex[i] + InputBoxTextStrs[i].Len() - 1)) || OldEndIndex < (RichTextIndex[i] + InputBoxTextStrs[i].Len()))
					{
						int32 count = 0;
						if (IsAdd)
						{
							for (size_t j = CurEndIndex; count < ((RichTextIndex[i] + InputBoxTextStrs[i].Len()) - OldEndIndex) && ((CurEndIndex + 1 - RemoveNum + count) < ChatHyperlinkData.ResultStr.Len() && (CurEndIndex + 1 - RemoveNum + count) > -1); j++)
							{
								ChatHyperlinkData.ResultStr.RemoveAt(CurEndIndex + 1 - RemoveNum + count);
								RemoveNum++;
								count++;
							}
						}
						else 
						{
							for (size_t j = CurEndIndex; count < ((RichTextIndex[i] + InputBoxTextStrs[i].Len() - 1) - OldEndIndex) && ((CurEndIndex - RemoveNum + count) < ChatHyperlinkData.ResultStr.Len() && (CurEndIndex - RemoveNum + count) > -1); j++)
							{
								ChatHyperlinkData.ResultStr.RemoveAt(CurEndIndex - RemoveNum + count);
								RemoveNum++;
								count++;
							}
						}
					}
				}
				if (RichEndIndex > -1 && RichStartIndex != RichEndIndex && i == RichEndIndex)
				{
					///<删除当前Str 的CurStartIndex想右（RichTextIndex[i] + RichTextStrs[i].Len()-OldEndIndex）个字符
					if (OldEndIndex < (RichTextIndex[i] + InputBoxTextStrs[i].Len()))
					{
						int32 count = 0;
						for (size_t j = CurEndIndex; count < ((RichTextIndex[i] + InputBoxTextStrs[i].Len() - 1) - OldEndIndex) && ((CurEndIndex - RemoveNum + count) < ChatHyperlinkData.ResultStr.Len() && (CurEndIndex - RemoveNum + count) > -1); j++)
						{
							ChatHyperlinkData.ResultStr.RemoveAt(CurEndIndex - RemoveNum + count);
							RemoveNum++;
							count++;
						}
					}
				}
			}

			int32 RemoveIndex = (RichStartIndex > -1) ? RichStartIndex : RichEndIndex;
			int32 Count = (RichEndIndex > -1 && RichStartIndex > -1) ? (RichEndIndex - RichStartIndex + 1) : 1;
			///<刷新富文本的索引下标
			int32 RefreshIndex = (RichEndIndex > -1) ? RichEndIndex : RichStartIndex;
			if (RefreshIndex > -1)
			{
				int32 Len = ChatHyperlinkData.ResultStr.Len() - OldStr.Len();
				for (int j = RichTextIndex.Num() - 1; (j > RichEndIndex && j < RichTextIndex.Num()); j++)
				{
					ChatHyperlinkData.RichTextIndex[j] += Len;
				}
			}
			///删除富文本数组保存的数据
			for (int32 i = RemoveIndex; i < (RemoveIndex+Count) && RemoveIndex < ChatHyperlinkData.RichTextIndex.Num(); i++)
			{
				ChatHyperlinkData.RichTextIndex.RemoveAt(RemoveIndex);
				ChatHyperlinkData.RichTextStrs.RemoveAt(RemoveIndex);
				ChatHyperlinkData.InputBoxTextStrs.RemoveAt(RemoveIndex);
			}
		}
		else
		{
			///<修改富文本数组保存的数据
			int32 RefreshIndex = -1;
			if (OldStartIndex == -1)
			{
				RefreshIndex = 0;
			}
			else if (OldStartIndex == OldStr.Len())
			{
				RefreshIndex = -1;
			}
			else
			{
				for (size_t i = 0; i < InputBoxTextStrs.Num() && i < RichTextIndex.Num(); i++)
				{
					if (OldStartIndex > (RichTextIndex[i]) + InputBoxTextStrs[i].Len() - 1)
					{
						RefreshIndex = i + 1;
					}
					else if (OldStartIndex == RichTextIndex[i] || OldStartIndex < RichTextIndex[i])
					{
						RefreshIndex = i;
					}
				}
			}
			if (RefreshIndex > -1)
			{
				///<刷新富文本的索引下标
				int32 Len = ChatHyperlinkData.ResultStr.Len() - OldStr.Len();
				for (int j = RefreshIndex; j < ChatHyperlinkData.RichTextIndex.Num(); j++)
				{
					ChatHyperlinkData.RichTextIndex[j] += Len;
				}
			}
		}
	}
	else
	{
		///<修改富文本数组保存的数据
		int32 RefreshIndex = -1;
		if (OldStartIndex==-1)
		{
			RefreshIndex = 0;
		}
		else if (OldStartIndex == OldStr.Len())
		{
			RefreshIndex = -1;
		}
		else
		{
			for (size_t i = 0; i < InputBoxTextStrs.Num() && i < RichTextIndex.Num(); i++)
			{
				if (OldStartIndex > RichTextIndex[i])
				{
					if (i==(InputBoxTextStrs.Num()-1))
					{
						if (OldStartIndex<(RichTextIndex[i]+ InputBoxTextStrs[i].Len()))
						{
							RefreshIndex = i;
						}
						else
						{
							RefreshIndex = -1;
						}						
					}
					else
					{
						RefreshIndex = i + 1;
					}					
				}
				else if (OldStartIndex == RichTextIndex[i])
				{
					RefreshIndex = i;
				}
			}
		}
		if (RefreshIndex>-1)
		{
			///<刷新富文本的索引下标
			int32 Len = ChatHyperlinkData.ResultStr.Len() - OldStr.Len();
			for (int j = RefreshIndex; j < ChatHyperlinkData.RichTextIndex.Num(); j++)
			{
				ChatHyperlinkData.RichTextIndex[j] += Len;
			}
		}		
	}
}

void UGolbalBPFunctionLibrary::MakeHLString(const FString & CurStr, FString & ResultStr, const TArray<FString> RichTextStrs, const TArray<int32> RichTextIndex, const TArray<FString> InputBoxTextStrs)
{
	int32 StartIndex = 0;
	for (size_t i = 0; i < InputBoxTextStrs.Num() && i < RichTextIndex.Num(); i++)
	{
		if (RichTextIndex[i] > 0 && StartIndex < RichTextIndex[i])
		{
			FString CurSubstring = UKismetStringLibrary::GetSubstring(CurStr, StartIndex, RichTextIndex[i] - StartIndex);
			ResultStr.Append(CurSubstring);
			StartIndex = RichTextIndex[i];
		}
		ResultStr.Append(RichTextStrs[i]);
		StartIndex += InputBoxTextStrs[i].Len();
		if (i == (InputBoxTextStrs.Num() - 1) && StartIndex < CurStr.Len())
		{
			FString EndSubstring = UKismetStringLibrary::GetSubstring(CurStr, StartIndex, CurStr.Len() - StartIndex);
			ResultStr.Append(EndSubstring);
		}
	}
}

void UGolbalBPFunctionLibrary::SetText(const FText& newText, UHorizonDialogueMsgTextBlock* pDialogueWidget)
{
	if (!IsValid(UUECS3GameInstance::Instance))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::SetText : Instance!"));
		return;
	}
	UTextParseManger* TempTextParseMgr = UUECS3GameInstance::Instance->TextParseMgr;
	if (!IsValid(TempTextParseMgr))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::SetText : TempTextParseMgr!"));
		return;
	}
	FString TransformStr = TempTextParseMgr->TransformText(newText.ToString());
	pDialogueWidget->SetText(FSTRING_TO_FTEXT(TransformStr));
	pDialogueWidget->RebuildDialogueMsgTextBlock();
}

AClientGameCharacter* UGolbalBPFunctionLibrary::CreateClientGameCharacter(FString ModelID, FString BPName)
{
	UClass *ClientActor = UGolbalBPFunctionLibrary::GetUClassByStr(BPName);
	AClientGameCharacter* ClientGameActor = UGolbalBPFunctionLibrary::SpawnActor<AClientGameCharacter>(ClientActor);
	if (IsValid(ClientGameActor))
	{
		ClientGameActor->GetAppearanceComponent()->CreateAppearance(ModelID);
		return ClientGameActor;
	}
	return nullptr;
}


bool UGolbalBPFunctionLibrary::GetSkillAssistUI()
{
	AServerCharacter* Character = GetCS3PlayerCharacter();
	
	if (IsValid(Character))
	{
		APlayerCharacter* PlayerCharacter = Cast<APlayerCharacter>(Character);
		if (IsValid(PlayerCharacter))
		{
			return PlayerCharacter->GetSkillAssistUi();
		}
	}
	return false;
}

class AActor* UGolbalBPFunctionLibrary::BeginDeferredActorSpawnFromClass(TSubclassOf<AActor> ActorClass, const FTransform& SpawnTransform, ESpawnActorCollisionHandlingMethod CollisionHandlingOverride /*= ESpawnActorCollisionHandlingMethod::AlwaysSpawn*/, AActor* Owner /*= nullptr*/)
{
	const UWorld* Worldcontext = UUECS3GameInstance::Instance->GetWorld();
	return UGameplayStatics::BeginDeferredActorSpawnFromClass(Worldcontext, ActorClass, SpawnTransform, CollisionHandlingOverride, Owner);
}

class AActor* UGolbalBPFunctionLibrary::FinishSpawningActor(AActor* Actor, const FTransform& SpawnTransform)
{
	return UGameplayStatics::FinishSpawningActor(Actor, SpawnTransform);
}

FAssetData UGolbalBPFunctionLibrary::CS3GetAssetDataByFilePath(const FString& PackagePath)
{
	const IAssetRegistry& Registry = FModuleManager::LoadModuleChecked<FAssetRegistryModule>("AssetRegistry").Get();
	return Registry.GetAssetByObjectPath(*PackagePath);
}

UMaterialInterface* UGolbalBPFunctionLibrary::GetFootMaterial()
{
	AServerCharacter* ServerCharacter = GetCS3PlayerCharacter();
	if (!IsValid(ServerCharacter)) return nullptr;
	APlayerCharacter* PlayerCharacter = (APlayerCharacter*)ServerCharacter;
	if (!IsValid(PlayerCharacter)) return nullptr;
	AServerCharacter* Target = PlayerCharacter->CurPlayerTarget;
	if (IsValid(Target))
	{
		int32 appearanceColor = GetIntPropertyValue(Target->EntityId, TEXT("appearanceColor"));
		bool tempIsGreen = true;
		//AppearanceColor 0:不改变颜色，1:绿色，2:红色
		if (appearanceColor>0)
		{
			switch (appearanceColor)
			{
			case 1:
				tempIsGreen = true;
				break;
			case 2:
				tempIsGreen = false;
				break;
			default:
				break;
			}
		}
		else
		{
			COMBAT_RELATION Relation = PlayerCharacter->QueryRelation(Target);
			if (Relation == COMBAT_RELATION::COMBAT_RELATION_ENEMY)
			{
				tempIsGreen = false;
			}
			else
			{
				tempIsGreen = true;
			}
		}
		//设置材质
		if (tempIsGreen)
		{
			UObject* MaterialObj = UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(FSoftObjectPath(TEXT("Material'/Game/Effects/TargetFootDecal/T_Ring047_D_greenMat.T_Ring047_D_GreenMat'")));
			if (MaterialObj)
			{
				return (UMaterialInterface*)MaterialObj;
			}
			else
			{
				return nullptr;
			}
		} 
		else
		{
			UObject* MaterialObj = UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(FSoftObjectPath(TEXT("Material'/Game/Effects/TargetFootDecal/T_Ring047_D_RedMat.T_Ring047_D_RedMat'")));
			if (MaterialObj)
			{
				return (UMaterialInterface*)MaterialObj;
			}
			else
			{
				return nullptr;
			}
		}
	}
	else
	{
		return nullptr;
	}
}

UObject* UGolbalBPFunctionLibrary::LoadObjectByAssetPath(TSoftObjectPtr<UObject> AssetPath)
{
	if (UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->ResourceManager)
	{
		return UUECS3GameInstance::Instance->ResourceManager->SynchronousLoad(AssetPath);
	}
	else
	{
		FStreamableManager StreamManager;
		return StreamManager.LoadSynchronous(AssetPath);
	}
}

FTimerHandle UGolbalBPFunctionLibrary::SetTimerbyEvent(UObject* Object, FTimerDynamicDelegate Delegate, float Time, bool bLooping, bool bReset)
{
	FTimerHandle Handle;

	if (UUECS3GameInstance::Instance)
	{
		if (bReset)
		{
			Handle = Object->GetWorld()->GetTimerManager().K2_FindDynamicTimerHandle(Delegate);
		}
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(Object, Handle, Delegate, Time, bLooping);
	}
	else
	{
		if (Object->GetWorld())
		{
			if (bReset)
			{
				Handle = Object->GetWorld()->GetTimerManager().K2_FindDynamicTimerHandle(Delegate);
			}
			
			Object->GetWorld()->GetTimerManager().SetTimer(Handle, Delegate, Time, bLooping);
		}
	}

	return Handle;
}

FTimerHandle UGolbalBPFunctionLibrary::SetTimerbyFunctionName(UObject* Object, FString FunctionName, float Time, bool bLooping)
{
	FName const FunctionFName(*FunctionName);

	if (!IsValid(Object))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::SetTimerbyFunctionName : Object is not valid!"));
		return FTimerHandle();
	}
	else
	{
		UFunction* const Func = Object->FindFunction(FunctionFName);
		if (Func)
		{
			if (Func->ParmsSize > 0)
			{
				// User passed in a valid function, but one that takes parameters
				// FTimerDynamicDelegate expects zero parameters and will choke on execution if it tries
				// to execute a mismatched function
				UE_LOG(LogBlueprintUserMessages, Warning, TEXT("SetTimer passed a function (%s) that expects parameters."), *FunctionName);
				return FTimerHandle();
			}
			else 
			{
				FTimerDynamicDelegate DynamicDelegate;
				DynamicDelegate.BindUFunction(Object, FunctionFName);
				FTimerHandle Handle;
				if (DynamicDelegate.IsBound())
				{
					const UWorld* const World = Object->GetWorld();
					if (IsValid(World))
					{
						Handle = World->GetTimerManager().K2_FindDynamicTimerHandle(DynamicDelegate);
						if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->CustomTimerManager))
						{
							UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(Object, Handle, DynamicDelegate, Time, bLooping);
						} 
						else
						{
							World->GetTimerManager().SetTimer(Handle, DynamicDelegate, Time, bLooping);
						}
					}
				}
				return Handle;
			}
		}
		else 
		{
			UE_LOG(LogBlueprintUserMessages, Warning, TEXT("SetTimer passed a function (%s) that invalid."), *FunctionName);
			return FTimerHandle();
		}
	}
}

UMaterialInstanceDynamic* UGolbalBPFunctionLibrary::CreateDMI(UPrimitiveComponent* Comp, int32 ElementIndex, class UMaterialInterface* SourceMaterial)
{
	if (SourceMaterial)
	{
		Comp->SetMaterial(ElementIndex, SourceMaterial);
	}

	UMaterialInterface* MaterialInstance = Comp->GetMaterial(ElementIndex);
	UMaterialInstanceDynamic* MID = Cast<UMaterialInstanceDynamic>(MaterialInstance);

	if (MaterialInstance && !MID)
	{	
		if (SourceMaterial)
			MID = UMaterialInstanceDynamic::Create(MaterialInstance, Comp, *SourceMaterial->GetName());
		else
			MID = UMaterialInstanceDynamic::Create(MaterialInstance, Comp, *MaterialInstance->GetName());
		Comp->SetMaterial(ElementIndex, MID);
	}

	return MID;
}

void UGolbalBPFunctionLibrary::CS3SetScalarParameterOnMaterials(UMeshComponent* Comp, FName ParameterName, float ParameterValue)
{

	TSortedMap<FName, TArray<int32>> MaterialParameterCache;

	const UWorld* World = Comp->GetWorld();
	const bool bHasMaterialResource = (World && World->WorldType != EWorldType::Inactive);
	const ERHIFeatureLevel::Type FeatureLevel = bHasMaterialResource ? World->FeatureLevel : ERHIFeatureLevel::Num;

	// Retrieve all used materials
	TArray<UMaterialInterface*> MaterialInterfaces = Comp->GetMaterials();
	int32 MaterialIndex = 0;
	for (UMaterialInterface* MaterialInterface : MaterialInterfaces)
	{
		UMaterial* Material = (IsValid(MaterialInterface)) ? MaterialInterface->GetMaterial() : nullptr;
		if (IsValid(Material))
		{
			//TArray<FName> OutParameterNames;
			TArray<FGuid> OutParameterIds;
			TArray<FMaterialParameterInfo> OutParameterInfo;

			//Material->GetAllScalarParameterNames(OutParameterNames, OutParameterIds);
			Material->GetAllScalarParameterInfo(OutParameterInfo, OutParameterIds);

			for (FMaterialParameterInfo Info : OutParameterInfo)
			{
				// Add or retrieve entry for this parameter name
				TArray<int32>& ParameterCache = MaterialParameterCache.FindOrAdd(Info.Name);
				// Add the corresponding material index
				ParameterCache.Add(MaterialIndex);
			}

			// Empty parameter names and ids
			OutParameterInfo.Reset();
			OutParameterIds.Reset();
		}

		++MaterialIndex;
	}

	if (TArray<int32>* ParameterCache = MaterialParameterCache.Find(ParameterName))
	{
		const TArray<int32>& MaterialIndices = *ParameterCache;
		int32 NameIndex = 0;
		
		// Loop over all the material indices and update set the parameter value on the corresponding materials		
		for (int32 TempMaterialIndex : MaterialIndices)
		{
			UMaterialInterface* MaterialInterface = Comp->GetMaterial(TempMaterialIndex);
			if (MaterialInterface)
			{
				//FString TmpName = MaterialInterface->GetName() + "_" + FString::FromInt(NameIndex);
				UMaterialInstanceDynamic* DynamicMaterial = Cast<UMaterialInstanceDynamic>(MaterialInterface);
				if (!IsValid(DynamicMaterial))
				{
					UMaterialInterface* MaterialInstance = Comp->GetMaterial(TempMaterialIndex);
					UMaterialInstanceDynamic* MID = Cast<UMaterialInstanceDynamic>(MaterialInstance);

					if (IsValid(MaterialInstance) && !MID)
					{
						MID = UMaterialInstanceDynamic::Create(MaterialInstance, Comp, *MaterialInterface->GetName());
						Comp->SetMaterial(TempMaterialIndex, MID);
						DynamicMaterial = MID;
						NameIndex++;
					}
				}
				DynamicMaterial->SetScalarParameterValue(ParameterName, ParameterValue);
			}
		}
	}
}

void UGolbalBPFunctionLibrary::CS3SetVectorParameterOnMaterials(UMeshComponent* Comp, FName ParameterName, FVector ParameterValue)
{
	TSortedMap<FName, TArray<int32>> MaterialParameterCache;

	const UWorld* World = Comp->GetWorld();
	// to set the default value for scalar params, we use a FMaterialResource, which means the world has to be rendering
	const bool bHasMaterialResource = (World && World->WorldType != EWorldType::Inactive);
	const ERHIFeatureLevel::Type FeatureLevel = bHasMaterialResource ? World->FeatureLevel : ERHIFeatureLevel::Num;

	TArray<UMaterialInterface*> MaterialInterfaces = Comp->GetMaterials();

	{
		int32 MaterialIndex = 0;
		for (UMaterialInterface* MaterialInterface : MaterialInterfaces)
		{
			UMaterial* Material = (IsValid(MaterialInterface)) ? MaterialInterface->GetMaterial() : nullptr;
			if (IsValid(Material))
			{
				//TArray<FName> OutParameterNames;
				TArray<FGuid> OutParameterIds;
				TArray<FMaterialParameterInfo> OutParameterInfo;

				//Material->GetAllScalarParameterNames(OutParameterNames, OutParameterIds);
				//Material->GetAllVectorParameterNames(OutParameterNames, OutParameterIds);

				Material->GetAllScalarParameterInfo(OutParameterInfo, OutParameterIds);
				Material->GetAllVectorParameterInfo(OutParameterInfo, OutParameterIds);

				for (FMaterialParameterInfo Info : OutParameterInfo)
				{
					// Add or retrieve entry for this parameter name
					TArray<int32>& ParameterCache = MaterialParameterCache.FindOrAdd(Info.Name);
					// Add the corresponding material index
					ParameterCache.Add(MaterialIndex);
				}
				++MaterialIndex;
			}
		}
	}

	if (TArray<int32>* ParameterCache = MaterialParameterCache.Find(ParameterName))
	{
		const TArray<int32>& MaterialIndices = *ParameterCache;
		int32 NameIndex = 0;

		// Loop over all the material indices and update set the parameter value on the corresponding materials		
		for (int32 MaterialIndex : MaterialIndices)
		{
			UMaterialInterface* MaterialInterface = Comp->GetMaterial(MaterialIndex);
			if (MaterialInterface)
			{
				//FString TmpName = MaterialInterface->GetName() + "_" + FString::FromInt(NameIndex);
				UMaterialInstanceDynamic* DynamicMaterial = Cast<UMaterialInstanceDynamic>(MaterialInterface);
				if (!IsValid(DynamicMaterial))
				{
					UMaterialInterface* MaterialInstance = Comp->GetMaterial(MaterialIndex);
					UMaterialInstanceDynamic* MID = Cast<UMaterialInstanceDynamic>(MaterialInstance);

					if (MaterialInstance && !MID)
					{
						MID = UMaterialInstanceDynamic::Create(MaterialInstance, Comp, *MaterialInterface->GetName());
						Comp->SetMaterial(MaterialIndex, MID);
						DynamicMaterial = MID;
						NameIndex++;
					}
				}
				DynamicMaterial->SetVectorParameterValue(ParameterName, ParameterValue);
			}
		}
	}
}

void UGolbalBPFunctionLibrary::CS3SetLinearParameterOnMaterials(UMeshComponent* Comp, FName ParameterName, FLinearColor ParameterValue)
{
	TSortedMap<FName, TArray<int32>> MaterialParameterCache;

	const UWorld* World = Comp->GetWorld();
	// to set the default value for scalar params, we use a FMaterialResource, which means the world has to be rendering
	const bool bHasMaterialResource = (World && World->WorldType != EWorldType::Inactive);
	const ERHIFeatureLevel::Type FeatureLevel = bHasMaterialResource ? World->FeatureLevel : ERHIFeatureLevel::Num;

	TArray<UMaterialInterface*> MaterialInterfaces = Comp->GetMaterials();

	{
		int32 MaterialIndex = 0;
		for (UMaterialInterface* MaterialInterface : MaterialInterfaces)
		{
			UMaterial* Material = (IsValid(MaterialInterface)) ? MaterialInterface->GetMaterial() : nullptr;
			if (IsValid(Material))
			{
				//TArray<FName> OutParameterNames;
				TArray<FGuid> OutParameterIds;
				TArray<FMaterialParameterInfo> OutParameterInfo;

				//Material->GetAllScalarParameterNames(OutParameterNames, OutParameterIds);
				//Material->GetAllVectorParameterNames(OutParameterNames, OutParameterIds);

				Material->GetAllScalarParameterInfo(OutParameterInfo, OutParameterIds);
				Material->GetAllVectorParameterInfo(OutParameterInfo, OutParameterIds);

				for (FMaterialParameterInfo Info : OutParameterInfo)
				{
					// Add or retrieve entry for this parameter name
					TArray<int32>& ParameterCache = MaterialParameterCache.FindOrAdd(Info.Name);
					// Add the corresponding material index
					ParameterCache.Add(MaterialIndex);
				}
				++MaterialIndex;
			}
		}
	}

	if (TArray<int32>* ParameterCache = MaterialParameterCache.Find(ParameterName))
	{
		const TArray<int32>& MaterialIndices = *ParameterCache;
		int32 NameIndex = 0;

		// Loop over all the material indices and update set the parameter value on the corresponding materials		
		for (int32 MaterialIndex : MaterialIndices)
		{
			UMaterialInterface* MaterialInterface = Comp->GetMaterial(MaterialIndex);
			if (MaterialInterface)
			{
				//FString TmpName = MaterialInterface->GetName() + "_" + FString::FromInt(NameIndex);
				UMaterialInstanceDynamic* DynamicMaterial = Cast<UMaterialInstanceDynamic>(MaterialInterface);
				if (!IsValid(DynamicMaterial))
				{
					UMaterialInterface* MaterialInstance = Comp->GetMaterial(MaterialIndex);
					UMaterialInstanceDynamic* MID = Cast<UMaterialInstanceDynamic>(MaterialInstance);

					if (MaterialInstance && !MID)
					{
						MID = UMaterialInstanceDynamic::Create(MaterialInstance, Comp, *MaterialInterface->GetName());
						Comp->SetMaterial(MaterialIndex, MID);
						DynamicMaterial = MID;
						NameIndex++;
					}
				}
				DynamicMaterial->SetVectorParameterValue(ParameterName, ParameterValue);
			}
		}
	}
}

class UPathFollowingComponent* UGolbalBPFunctionLibrary::InitNavigationControl(AController& Controller)
{
	AAIController* AsAIController = Cast<AAIController>(&Controller);
	UPathFollowingComponent* PathFollowingComp = nullptr;

	if (AsAIController)
	{
		PathFollowingComp = AsAIController->GetPathFollowingComponent();
	}
	else
	{
		PathFollowingComp = Controller.FindComponentByClass<UPathFollowingComponent>();
		if (!IsValid(PathFollowingComp))
		{
			PathFollowingComp = NewObject<UPathFollowingComponent>(&Controller);
			PathFollowingComp->RegisterComponentWithWorld(Controller.GetWorld());
			PathFollowingComp->Initialize();
		}				
	}

	return PathFollowingComp;
}

void UGolbalBPFunctionLibrary::CS3SetModelPart(class AGameCharacter* Actor, FString ModelID)
{
	if (IsValid(Actor)&& !ModelID.IsEmpty())
	{
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		auto ModelTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_MODEL);
		const FMODEL_DATA* ModelData = ModelTable->GetRow<FMODEL_DATA>(ModelID);

		for (FPartItem part : ModelData->PartArray)
		{
		 	UCfgManager* TempCfgManager = UUECS3GameInstance::Instance->CfgManager;
			auto ModelPartTable = TempCfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_PART_MODEL);
			const FMODEL_PART_DATA* OutModelPartData = ModelPartTable->GetRow<FMODEL_PART_DATA>(part.PartID);
			TSoftObjectPtr<UObject> LoadMesh = OutModelPartData->ModelPartPath;
			TWeakObjectPtr<AGameCharacter> DelayThisPtr(Actor);
			UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(Actor, LoadMesh.ToSoftObjectPath(),
				FStreamableDelegate::CreateLambda([DelayThisPtr, LoadMesh,part, ModelID]()
					{
						if (!DelayThisPtr.IsValid())
						{
							return;
						}
						AGameCharacter* ThisPtr = DelayThisPtr.Get();
						UObject* mesh = LoadMesh.Get();

						USkeletalMeshComponent* CoatMeshCpt = Cast<USkeletalMeshComponent>(ThisPtr->GetPartMeshComponent(part.posType));
						if (!IsValid(CoatMeshCpt))
						{
							return;
						}

						if (part.posType == MODEL_PART_TYPE::MODEL_PART_BODYS)
						{
							ThisPtr->GetMesh()->SetSkeletalMesh(Cast<USkeletalMesh>(mesh));
							CS3PlayModelAction(ThisPtr, ModelID, "Idle_Free");
						}
						else if (part.posType == MODEL_PART_TYPE::MODEL_PART_LWEAPON)
						{
							UStaticMeshComponent* staticMeshComponent = Cast<UStaticMeshComponent>(CoatMeshCpt);
							FName SockeName = ThisPtr->GetWeaponSockName(true);
							staticMeshComponent->SetStaticMesh(Cast<UStaticMesh>(mesh));
							staticMeshComponent->AttachToComponent(ThisPtr->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, SockeName);
						}
						else if (part.posType == MODEL_PART_TYPE::MODEL_PART_RWEAPON)
						{
							UStaticMeshComponent* staticMeshComponent = Cast<UStaticMeshComponent>(CoatMeshCpt);
							FName SockeName = ThisPtr->GetWeaponSockName(false);
							staticMeshComponent->SetStaticMesh(Cast<UStaticMesh>(mesh));
							staticMeshComponent->AttachToComponent(ThisPtr->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, SockeName);
						}
						else if (part.posType == MODEL_PART_TYPE::MODEL_PART_S_LWEAPON)
						{
							USkeletalMeshComponent* skeletalMeshComponent = Cast<USkeletalMeshComponent>(CoatMeshCpt);
							FName SockeName = ThisPtr->GetWeaponSockName(true);
							skeletalMeshComponent->RemoveAllClothingActors();
							skeletalMeshComponent->SetSkeletalMesh(Cast<USkeletalMesh>(mesh));
							skeletalMeshComponent->AttachToComponent(ThisPtr->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, SockeName);
						}
						else if (part.posType == MODEL_PART_TYPE::MODEL_PART_S_RWEAPON)
						{
							USkeletalMeshComponent* skeletalMeshComponent = Cast<USkeletalMeshComponent>(CoatMeshCpt);
							FName SockeName = ThisPtr->GetWeaponSockName(false);
							skeletalMeshComponent->RemoveAllClothingActors();
							skeletalMeshComponent->SetSkeletalMesh(Cast<USkeletalMesh>(mesh));
							skeletalMeshComponent->AttachToComponent(ThisPtr->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, SockeName);
						}
						else if (part.posType == MODEL_PART_TYPE::MODEL_PART_STATIC)
						{
							UStaticMeshComponent* staticMeshComponent = Cast<UStaticMeshComponent>(CoatMeshCpt);
							staticMeshComponent->SetStaticMesh(Cast<UStaticMesh>(mesh));
							staticMeshComponent->AttachToComponent(ThisPtr->GetMesh(), FAttachmentTransformRules::KeepRelativeTransform, TEXT("Default"));
						}
						else
						{
							CoatMeshCpt->SetSkeletalMesh(Cast<USkeletalMesh>(mesh));
						}
			}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_PLAYER, FVector(0, 0, 0));
		}
	}
}


void UGolbalBPFunctionLibrary::CS3PlayModelAction(class AGameCharacter* Target ,FString ModelID, FString ActionID)
{
	UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
	auto ModelTable = CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_MODEL);
	const FMODEL_DATA* ModelData = ModelTable->GetRow<FMODEL_DATA>(ModelID);
	const UDataTable* TableData = CfgManager->GetTableByPath(ModelData->ActionConfigPath)->GetBaseTable();
	for (auto object : TableData->GetRowMap())
	{
		FACTION_DATA* ActionData = (FACTION_DATA*)object.Value;
		FName TableRow = (FName)object.Key;
		if (FNAME_TO_FSTRING(TableRow).Equals(ActionID))
		{
			if (ActionData->AnimPath.ToSoftObjectPath().IsValid())
			{
				Target->GetMesh()->PlayAnimation(ActionData->AnimPath.Get(), true);
			}
		}
	}
}
void UGolbalBPFunctionLibrary::SetModelonLand(const UObject* Object, UCapsuleComponent* CapsuleComp, float ModelScale, float CheckHeight)
{
	if (IsValid(CapsuleComp)&&IsValid(CapsuleComp->GetOwner()))
	{
		FVector Offset = CapsuleComp->GetUpVector()*CheckHeight;
		FVector newPos(CapsuleComp->K2_GetComponentLocation());
		FHitResult HitOut(ForceInit);
		FCollisionQueryParams TraceParams = FCollisionQueryParams(FName(TEXT("ComputeFloorDistSweep")), true, CapsuleComp->GetOwner());
		TraceParams.bTraceComplex = false;
		//TraceParams.bTraceAsyncScene = false;
		TraceParams.bReturnPhysicalMaterial = false;
		TraceParams.bIgnoreTouches = true;
		// 开始进行测试地板
		UWorld* World = GEngine->GetWorldFromContextObject(Object, EGetWorldErrorMode::LogAndReturnNull);
		if (IsValid(World) && World->LineTraceSingleByChannel(HitOut, newPos + FVector(0.0f, 0.0f, 200.0f),
			newPos - Offset, ECC_GameTraceChannel10, TraceParams))
		{
			FVector Pos = newPos;
			Pos.Z = CapsuleComp->GetScaledCapsuleHalfHeight()*ModelScale + HitOut.Location.Z;
			CapsuleComp->SetWorldLocation(Pos);
		}
	}
}
TArray<AActor*> UGolbalBPFunctionLibrary::GetPlayersInRange(UClass* Class /*= nullptr*/, float Range /*= 200.0f*/, FVector Pos /*= FVector::ZeroVector*/)
{
	TArray<AActor*> ActorList;
	if (!IsValid(UUECS3GameInstance::Instance))
	{
		return ActorList;
	}
	AActor* PlayerActor = UGolbalBPFunctionLibrary::GetCS3PlayerCharacter();
	if (!IsValid(PlayerActor))
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetPlayersInRange : PlayerActor!"));
		return ActorList;
	}
	if (UUECS3GameInstance::pKBEApp == nullptr || UUECS3GameInstance::pKBEApp->Entities() == nullptr)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UGolbalBPFunctionLibrary::GetPlayersInRange :pKBEApp||pKBEApp->Entities()!"));
		return ActorList;
	}

	TMap<int32, KBEngine::Entity*> EntitiesMap = *UUECS3GameInstance::pKBEApp->Entities();
	for (auto& Elem : EntitiesMap)
	{
		KBEngine::Entity* Entity = Elem.Value;
		if (Entity != nullptr)
		{
			if (!Entity->IsPlayer())
			{
				continue;
			}

			if (!Entity->Actor())
			{
				continue;
			}

			UObjectBase* ActorBase = (UObjectBase*)Entity->Actor();
			bool Result = false;
			int32 Index = GUObjectArray.ObjectToIndex(ActorBase);
			if (GUObjectArray.IsValidIndex(ActorBase))
			{
				// 判断一下找到的东西地址是否一致
				if (ActorBase == GUObjectArray.IndexToObject(Index)->Object)
				{
					Result = true;
				}
			}

			if (Result)
			{
				AActor* Actor = (AActor*)(ActorBase);

				float dist;
				if (Pos.Size() > 0)
				{
					dist = FVector::Dist(Pos, Actor->GetActorLocation());
				}
				else
				{
					dist = GetActorDistance(PlayerActor, Actor);
				}
				if (dist <= Range)
				{
					if (!IsValid(Class))
					{
						ActorList.Add(Actor);
					}
					else if (Actor->GetClass()->IsChildOf(Class))
					{
						ActorList.Add(Actor);
					}
				}
			}
			else
			{
				CS3_Display(CS3DebugType::CL_Undefined, TEXT("Actor is Invalid"));
			}
		}
	}

	SortActorByDistance(ActorList, PlayerActor);
	return ActorList;
}

FString UGolbalBPFunctionLibrary::GetValidInputTxt(FString InputText, int32 LimitedLen, bool IsBlankInputValid)
{
	FString TempInputString = InputText;
	if (IsBlankInputValid)
	{
		if (TempInputString.Len() > LimitedLen)
		{
			FString SubValueStr = UKismetStringLibrary::GetSubstring(TempInputString, 0, TempInputString.Len()-1);
			TempInputString = SubValueStr;
		}
	}
	else
	{
		FString SubValueStr = UKismetStringLibrary::GetSubstring(TempInputString, TempInputString.Len() - 1, 1);
		if (SubValueStr.Equals(""))
		{
			SubValueStr = UKismetStringLibrary::GetSubstring(TempInputString, 0, TempInputString.Len() - 1);
			TempInputString = SubValueStr;
		}
		else
		{
			if (TempInputString.Len() > LimitedLen)
			{
				SubValueStr = UKismetStringLibrary::GetSubstring(TempInputString, 0, TempInputString.Len() - 1);
				TempInputString = SubValueStr;
			}
		}
	}
	return TempInputString;
}

bool UGolbalBPFunctionLibrary::IsValidInputText(FString InputText, FString InputTextName, int32 MinLen/* = 0*/, int32 MaxLen/* = 0*/, bool IsAllChinese/* = false*/, bool IsShield/* = true*/)
{
	//空字符
	if (InputText.IsEmpty())
	{
		if (MinLen == 0)
		{
			return true;
		}
		else
		{
			//{0}输入不能为空
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5801, InputTextName);
			return false;
		}
	}
	//中文汉字
	if (IsAllChinese && !IsAllChineseChar(InputText))
	{
		//{0}只能输入中文汉字
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(5699, InputTextName);
		return false;
	}
	//有字数上下限
	if (MinLen > 0 && MaxLen > 0)
	{
		if (IsLessLimitInputText(InputText, MinLen) || IsOverLimitInputText(InputText, MaxLen))
		{
			FString Args = InputTextName + TEXT("|") + INT_TO_FSTRING(MinLen) + TEXT("|") + INT_TO_FSTRING(MaxLen);
			if (IsAllChinese)
			{
				//{0}只能输入{1}-{2}个汉字，请重新输入
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(5697, Args);
			}
			else
			{
				//{0}只能输入{1}-{2}个字符，请重新输入
				UUECS3GameInstance::Instance->MessageManager->ShowMessage(5698, Args);
			}
			return false;
		}
	}
	//只有字数下限
	else if (MinLen > 0 && IsLessLimitInputText(InputText, MinLen))
	{
		FString Args = InputTextName + TEXT("|") + INT_TO_FSTRING(MinLen);
		if (IsAllChinese)
		{
			//{0}必须输入不少于{1}个汉字，请重新输入
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5802, Args);
		}
		else
		{
			//{0}必须输入不少于{1}个字符，请重新输入
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5803, Args);
		}
		return false;
	}
	//只有字数上限
	else if (MaxLen > 0 && IsOverLimitInputText(InputText, MaxLen))
	{
		FString Args = InputTextName + TEXT("|") + INT_TO_FSTRING(MaxLen);
		if (IsAllChinese)
		{
			//{0}最多只能输入{1}个汉字，请重新输入
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5804, Args);
		}
		else
		{
			//{0}最多只能输入{1}个字符，请重新输入
			UUECS3GameInstance::Instance->MessageManager->ShowMessage(5805, Args);
		}
		return false;
	}
	//屏蔽字
	if (IsShield && UUECS3GameInstance::Instance->TextShieldMgr->HasShieldText(InputText))
	{
		//您输入的内容中包含敏感词汇，请重新输入
		UUECS3GameInstance::Instance->MessageManager->ShowMessage(2530);
		return false;
	}
	return true;
}

bool UGolbalBPFunctionLibrary::IsOverLimitInputText(FString InputText, int32 LimitedLen)
{
	if (InputText.Len() > LimitedLen)
	{
		return true;
	}
	return false;
}

bool UGolbalBPFunctionLibrary::IsLessLimitInputText(FString InputText, int32 LimitedLen)
{
	if (InputText.Len() < LimitedLen)
	{
		return true;
	}
	return false;
}

FString UGolbalBPFunctionLibrary::ReplaceLineBreak(const FString& InStr)
{
	FString ReplaceStr = InStr;
	FString LineStr = "\r\n";
	FString NullStr = "";
	if (ReplaceStr.Contains(LineStr))
	{
		ReplaceStr.ReplaceInline(*LineStr, *NullStr);
	}
	return ReplaceStr;
}

FLinearColor UGolbalBPFunctionLibrary::GetItemNameColorByQuality(int32 Quality)
{
	bool IsSuccess;
	FCS3ItemQualityData ItemQualityData = GetItemQualityConfig(Quality, IsSuccess);
	if (IsSuccess)
	{
		FColor Color = ItemQualityData.QualityColor;
		return FLinearColor(Color);
	}
	else
	{
		return FLinearColor(1.0f, 1.0f, 1.0f, 1.0f);
	}
}

FString UGolbalBPFunctionLibrary::GetItemNameByQuality(const FString& ItemName, int32 Quality)
{
	if (ItemName != TEXT(""))
	{
		FLinearColor linearColor = GetItemNameColorByQuality(Quality);
		FString ColorStr = ConvertLinearColorToHex(linearColor);
		return FString::Printf(TEXT("<text color=\"#%s\">%s</text>"), *ColorStr, *ItemName);
	}
	return TEXT("");
}

FCS3ItemQualityData UGolbalBPFunctionLibrary::GetItemQualityConfig(int32 Quality, bool& IsSuccess)
{
	if (IsValid(UGolbalBPFunctionLibrary::CfgManager()))
	{
		const UConfigTable* Table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(
			CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ITEM_QUALITY_DATA);
		const FCS3ItemQualityData* ItemQualityData = Table->GetRow<FCS3ItemQualityData>(INT_TO_FSTRING(Quality));

		if (ItemQualityData)
		{
			IsSuccess = true;
			return *ItemQualityData;
		}
	}
	IsSuccess = false;
	return FCS3ItemQualityData();
}

FString UGolbalBPFunctionLibrary::GetEllipsisString(const FString& SourceString, int32 Length)
{
	if (SourceString.Len() > Length)
	{
		FString SubValueStr = UKismetStringLibrary::GetSubstring(SourceString, 0, Length);
		return SubValueStr.Append("...");
	}
	return SourceString;
}

FString UGolbalBPFunctionLibrary::GetEquipPartNameByPartType(MODEL_PART_TYPE PartType)
{
	if (IsValid(UGolbalBPFunctionLibrary::CfgManager()))
	{
		const UConfigTable* Table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(
			CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_EQUIP_NAME_DATA);
		const FChinese* chinese = Table->GetRow<FChinese>(FString::FromInt((int32)PartType));
		if (chinese)
		{
			return chinese->ChineseStr;
		}
	}
	return TEXT("");
}

FString UGolbalBPFunctionLibrary::GetHoverTips(const FString& StringValue)
{
	if (IsValid(UGolbalBPFunctionLibrary::CfgManager()))
	{
		const UConfigTable* Table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(
			CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_HOVER_TIPS_DATA);
		const FChinese* chinese = Table->GetRow<FChinese>(StringValue);
		if (chinese)
		{
			return chinese->ChineseStr;
		}
	}
	return TEXT("");
}
 
UTexture2D* UGolbalBPFunctionLibrary::GetTextrue2DByItemQuality(int32 Quality)
{
	bool IsSuccess;
	FCS3ItemQualityData ItemQualityData = GetItemQualityConfig(Quality, IsSuccess);
	if (IsSuccess)
	{
		UTexture2D* QualityTexture2D = Cast<UTexture2D>(
			UGolbalBPFunctionLibrary::LoadObjectByAssetPath(ItemQualityData.QualityTexturePath));
		return QualityTexture2D;
	}
	return nullptr;
}

FProfessionData UGolbalBPFunctionLibrary::GetPlayerSchoolData(int32 CampType, int32 ProfessionType)
{
	FProfessionData ProfessionData = FProfessionData();
	if (IsValid(UGolbalBPFunctionLibrary::CfgManager()))
	{
		UCfgManager* CfgManager = UUECS3GameInstance::Instance->CfgManager;
		const UDataTable* TableData = CfgManager->GetTableByType(
			CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_ROLE_PROFESSION_DATA)->GetBaseTable();
		for (auto it : TableData->GetRowMap())
		{
			FProfessionData* FindProfessionData = (FProfessionData*)it.Value;
			if (!FindProfessionData)
			{
				continue;
			}
			if (FindProfessionData->CampType == CampType && FindProfessionData->ProfessionType == ProfessionType)
			{
				ProfessionData = *FindProfessionData;
			}
		}
	}
	return ProfessionData;
}

FVector2D UGolbalBPFunctionLibrary::ConvertWorldLocationToMapPosition(FVector2D ActorLocation,
	FVector2D LevelOrignLocation, float Rate)
{
	FVector2D NewVector2D = ActorLocation - LevelOrignLocation;
	return NewVector2D / Rate;
}

bool UGolbalBPFunctionLibrary::ConvertWorldLocToSlotPos(FVector2D PointLocation, FVector2D MiniMapViewOrigin,
	FVector2D LevelOrignLocation, float Rate, float ZoomRate, FVector2D MiniMapViewSize, FVector2D PointTextureSize,FVector2D& ResultVector2D)
{
	FVector2D PointPos = ConvertWorldLocationToMapPosition(PointLocation, LevelOrignLocation, Rate);
	FVector2D tempDis = PointPos - MiniMapViewOrigin;//距离小地图可视原点的像素距离
	FVector2D tempPadding = tempDis * ZoomRate;
	if (tempPadding.X > PointTextureSize.X / 2 && tempPadding.X <(MiniMapViewSize.X - PointTextureSize.X / 2) && tempPadding.Y > PointTextureSize.Y / 2 && tempPadding.Y < (MiniMapViewSize.Y - PointTextureSize.Y / 2))
	{
		//绘制点在父控件上的像素位置
		ResultVector2D = tempPadding - PointTextureSize  / 2.0f;
		return true;
	}
	return false;
}

FRESULT_MAP_DATA UGolbalBPFunctionLibrary::GetMapData()
{
	FString SpaceScriptID = UGolbalBPFunctionLibrary::GetSpaceData(FString(TEXT("SPACE_SCRIPT_ID")));
	FRESULT_MAP_DATA ResultMapData = FRESULT_MAP_DATA();
	if (UGolbalBPFunctionLibrary::MapManager())
	{
		if (UGolbalBPFunctionLibrary::MapManager()->IsPlaneSpace(SpaceScriptID))
		{  
			SpaceScriptID = UGolbalBPFunctionLibrary::MapManager()->GetRelatedMapScriptID(SpaceScriptID);
		}

		const UConfigTable* Table = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(
			CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_TYPE_LEVELMAP);
		const FLEVEL_HASHMAP* LevelSpaceData = Table->GetRow<FLEVEL_HASHMAP>(SpaceScriptID);
		if (LevelSpaceData)
		{
			const UConfigTable* MinniMapTable = UGolbalBPFunctionLibrary::CfgManager()->GetTableByType(
				CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_MINIMAP_DATA);
			const FMINIMAP_DATA* MinniMapData = MinniMapTable->GetRow<FMINIMAP_DATA>(LevelSpaceData->LevelName);
			if (MinniMapData!= nullptr)
			{
				ResultMapData.LevelWorldOrign = MinniMapData->LevelOrign;
				ResultMapData.Rate = MinniMapData->LevelSize.X/MinniMapData->MiniMapSize.X;
				ResultMapData.MapUISize = MinniMapData->MiniMapSize;
				ResultMapData.HasMiniMapCfg = true;
				return ResultMapData;
			}
		}
		else
		{
			return ResultMapData;
		}
	}
	return ResultMapData;
	
}

FString UGolbalBPFunctionLibrary::ConvertDateTimeToNumberModelByType(FDateTime time, bool IsShowToday /*= false*/, int32 type /*= 0*/)
{
	FString tempString = TEXT("");
	FString tempYearStr = INT_TO_FSTRING(time.GetYear());
	FString tempMonthStr = time.GetMonth() < 10 ? ("0" + INT_TO_FSTRING(time.GetMonth())) : INT_TO_FSTRING(time.GetMonth());
	FString tempDayStr = time.GetDay() < 10 ? ("0" + INT_TO_FSTRING(time.GetDay())) : INT_TO_FSTRING(time.GetDay());
	FString tempHourStr = time.GetHour() < 10 ? ("0" + INT_TO_FSTRING(time.GetHour())) : INT_TO_FSTRING(time.GetHour());
	FString tempMinuteStr = time.GetMinute() < 10 ? ("0" + INT_TO_FSTRING(time.GetMinute())) : INT_TO_FSTRING(time.GetMinute());
	FString tempSecondStr = time.GetSecond() < 10 ? ("0" + INT_TO_FSTRING(time.GetSecond())) : INT_TO_FSTRING(time.GetSecond());
	if (IsValid(TimeManager()) && UKismetMathLibrary::NotEqual_DateTimeDateTime(TimeManager()->GetClientTime().GetDate(), time.GetDate()) || IsShowToday)
	{
		tempString = tempYearStr + "/" + tempMonthStr + "/" + tempDayStr;
	}
	switch (type)
	{
	case 1:
		return tempString + " " + tempHourStr + ":" + tempMinuteStr;
	case 2:
		return tempString + " " + tempHourStr;
	case 3:
		return tempString;
	default:
		return tempString + " " + tempHourStr + ":" + tempMinuteStr + ":" + tempSecondStr;
	}
}

FString UGolbalBPFunctionLibrary::ConvertSecondsToHourChineseModelByType(int64 SecondValue, int32 Type)
{
	FString NewTimeValueStr = "";
	FTimespan Timespan = UKismetMathLibrary::FromSeconds(SecondValue);
	FString HourCompany = TEXT("时");
	FString MinuteCompany = TEXT("分");
	FString SecondCompany = TEXT("秒");
	FString HourValueStr = INT_TO_FSTRING((Timespan.GetHours()+ Timespan.GetDays() * 24));
	FString MinutesValueStr = INT_TO_FSTRING(Timespan.GetMinutes());
	FString SecondsValueStr = INT_TO_FSTRING(Timespan.GetSeconds());
	//格式 xx分xx秒 || xx分
	if (Type == 3 || Type == 5)
	{
		MinutesValueStr = INT_TO_FSTRING(Timespan.GetMinutes() + (Timespan.GetHours() + Timespan.GetDays() * 24) * 60);
	}
	//格式 xx秒
	if (Type == 4)
	{
		SecondsValueStr = INT_TO_FSTRING(Timespan.GetSeconds() + (((Timespan.GetHours() + Timespan.GetDays() * 24) * 60 + Timespan.GetMinutes()) * 60));
	}
	if (HourValueStr.Len() <= 1)
	{
		HourValueStr.InsertAt(0, "0");
	}
	if (MinutesValueStr.Len() <= 1)
	{
		MinutesValueStr.InsertAt(0, "0");
	}
	if (SecondsValueStr.Len() <= 1)
	{
		SecondsValueStr.InsertAt(0, "0");
	}

	if (Type == 0)
	{
		NewTimeValueStr = HourValueStr + HourCompany;
	}
	else if ( Type == 1 )
	{
		NewTimeValueStr = HourValueStr + HourCompany + MinutesValueStr + MinuteCompany;
	}
	else if (Type == 2)
	{
		NewTimeValueStr = HourValueStr + HourCompany + MinutesValueStr + MinuteCompany + SecondsValueStr + SecondCompany;
	}
	else if (Type == 3)
	{
		NewTimeValueStr = MinutesValueStr + MinuteCompany + SecondsValueStr + SecondCompany;
	}
	else if (Type == 4)
	{
		NewTimeValueStr = SecondsValueStr + SecondCompany;
	}
	else if (Type == 5)
	{
		NewTimeValueStr = MinutesValueStr + MinuteCompany;
	}
	return NewTimeValueStr;
}

FString UGolbalBPFunctionLibrary::ConvertSecondsToHourColonModle(int32 TimeValue)
{
	int32 LocalTimeValue = TimeValue;
	int32 HourValue = TimeValue / 3600;
	int32 MinuteValue = (TimeValue % 3600) / 60;
	int32 SecondValue = (TimeValue % 3600) % 60;

	FString HourStr = FString::FromInt(HourValue);
	FString MinuteStr = FString::FromInt(MinuteValue);
	if (MinuteValue < 10)
	{
		FString AppedValue = "0";
		MinuteStr = AppedValue.Append(FString::FromInt(MinuteValue));
	}

	FString SecondStr = FString::FromInt(SecondValue);
	if (SecondValue < 10)
	{
		FString AppedValue = "0";
		SecondStr = AppedValue.Append(FString::FromInt(SecondValue));
	}

	FString TimeValueStr = "";
	if (TimeValue < 60)
	{
		FString AppedValue = "00:00:";
		TimeValueStr = AppedValue.Append(SecondStr);
	}
	else
	{
		if (TimeValue < 3600)
		{
			FString AppedValue1 = "00:";
			FString AppedValue2 = ":";
			TimeValueStr = AppedValue1 + MinuteStr + AppedValue2 + SecondStr;
		}
		else
		{
			FString AppedValue2 = ":";
			TimeValueStr = HourStr + AppedValue2 + MinuteStr + AppedValue2 + SecondStr;
		}
	}
	return TimeValueStr;
}

FString UGolbalBPFunctionLibrary::ConvertSecondsToMinuteColonModle(int32 TimeValue)
{
	int32 LocalTimeValue = TimeValue;
	int32 MinuteValue = TimeValue / 60;
	int32 SecondValue = TimeValue % 60;

	FString MinuteStr = FString::FromInt(MinuteValue);
	if (MinuteValue < 10)
	{
		FString AppedValue = "0";
		MinuteStr = AppedValue.Append(FString::FromInt(MinuteValue));
	}

	FString SecondStr = FString::FromInt(SecondValue);
	if (SecondValue < 10)
	{
		FString AppedValue = "0";
		SecondStr = AppedValue.Append(FString::FromInt(SecondValue));
	}

	FString TimeValueStr = "";
	if (TimeValue < 60)
	{
		FString AppedValue = "00:";
		TimeValueStr = AppedValue.Append(SecondStr);
	}
	else
	{
		FString AppedValue = ":";
		TimeValueStr = MinuteStr + AppedValue + SecondStr;
	}
	return TimeValueStr;
}

FString UGolbalBPFunctionLibrary::ConvertSecondsToDayChineseModel(float SecondValue)
{
	FString TempTimeStr = "";
	FTimespan Timespan = UKismetMathLibrary::FromSeconds(SecondValue);
	FString DayStr = TEXT("天");
	FString HourStr = TEXT("时");
	FString MinuteStr = TEXT("分");
	FString SecondStr = TEXT("秒");

	if (Timespan.GetDays() > 0)
	{
		TempTimeStr = TempTimeStr + INT_TO_FSTRING(Timespan.GetDays()) + DayStr;
	}
	if (Timespan.GetHours() > 0)
	{
		TempTimeStr = TempTimeStr + INT_TO_FSTRING(Timespan.GetHours()) + HourStr;
	}
	if (Timespan.GetMinutes() > 0)
	{
		TempTimeStr = TempTimeStr + INT_TO_FSTRING(Timespan.GetMinutes()) + MinuteStr;
	}
	if (Timespan.GetSeconds() > 0)
	{
		TempTimeStr = TempTimeStr + INT_TO_FSTRING(Timespan.GetSeconds()) + SecondStr;
	}
	return TempTimeStr;
}

bool UGolbalBPFunctionLibrary::GetPathByFileDialog(FString& OutPath, const FString& FileTypes)
{
#if WITH_EDITOR
	TArray<FString> OpenFilenames;
	IDesktopPlatform* DesktopPlatform = FDesktopPlatformModule::Get();
	bool bOpened = false;
	int32 FilterIndex = -1;

	if (DesktopPlatform)
	{
		const void* ParentWindowWindowHandle = FSlateApplication::Get().FindBestParentWindowHandleForDialogs(nullptr);

		bOpened = DesktopPlatform->OpenFileDialog(
			ParentWindowWindowHandle,
			TEXT("选择文件"),
			TEXT(""),
			TEXT(""),
			FileTypes,
			EFileDialogFlags::None,
			OpenFilenames,
			FilterIndex
		);
	}

	if (bOpened)
	{
		if (OpenFilenames.Num() > 0)
		{
			OutPath = OpenFilenames[0];
			return true;
		}
	}
#endif
	return false;
}

void UGolbalBPFunctionLibrary::ForceGC()
{
	GEngine->ForceGarbageCollection(true);
}

FString UGolbalBPFunctionLibrary::GetGameFrame()
{
	extern ENGINE_API float GAverageFPS;
	return FString::Printf(TEXT("%0.0f"), GAverageFPS);
}

bool UGolbalBPFunctionLibrary::SaveRenderTargetToFile(UTextureRenderTarget2D* rt, const FString& fileDestination)
{
	FTextureRenderTargetResource* rtResource = rt->GameThread_GetRenderTargetResource();
	FReadSurfaceDataFlags readPixelFlags(RCM_UNorm);

	TArray<FColor> outBMP;
	outBMP.AddUninitialized(rt->GetSurfaceWidth() * rt->GetSurfaceHeight());
	rtResource->ReadPixels(outBMP, readPixelFlags);

	for (FColor& color : outBMP)
		color.A = 255;

	FIntPoint destSize(rt->GetSurfaceWidth(), rt->GetSurfaceHeight());
	TArray<uint8> CompressedBitmap;
	FImageUtils::CompressImageArray(destSize.X, destSize.Y, outBMP, CompressedBitmap);
	bool imageSavedOk = FFileHelper::SaveArrayToFile(CompressedBitmap, *fileDestination);
	return imageSavedOk;

	return true;
}

class UTexture2D* UGolbalBPFunctionLibrary::GetTexture2DFromDiskFile(const FString& FilePath)
{
	TArray<uint8> RawFileData;
	UTexture2D* MyTexture = NULL;
	if (FFileHelper::LoadFileToArray(RawFileData, *FilePath /*"<path to file>"*/))
	{
		IImageWrapperModule& ImageWrapperModule = FModuleManager::LoadModuleChecked<IImageWrapperModule>(FName("ImageWrapper"));
		// Note: PNG format.  Other formats are supported
		TSharedPtr<IImageWrapper> ImageWrapper = ImageWrapperModule.CreateImageWrapper(EImageFormat::PNG);
		if (ImageWrapper.IsValid() && ImageWrapper->SetCompressed(RawFileData.GetData(), RawFileData.Num()))
		{
			const TArray<uint8>* UncompressedBGRA = NULL;
			if (ImageWrapper->GetRaw(ERGBFormat::BGRA, 8, UncompressedBGRA))
			{
				// Create the UTexture for rendering
				MyTexture = UTexture2D::CreateTransient(ImageWrapper->GetWidth(), ImageWrapper->GetHeight(), PF_B8G8R8A8);

				// Fill in the source data from the file
				void* TextureData = MyTexture->PlatformData->Mips[0].BulkData.Lock(LOCK_READ_WRITE);
				FMemory::Memcpy(TextureData, UncompressedBGRA->GetData(), UncompressedBGRA->Num());
				MyTexture->PlatformData->Mips[0].BulkData.Unlock();

				// Update the rendering resource from data.
				MyTexture->UpdateResource();
			}
		}
	}
	return MyTexture;
}
			
FVector2D UGolbalBPFunctionLibrary::GetMapTextureSizeByMip(UTexture2D* MapTexture, int32 MipIndex)
{
	FVector2D TextureSize = FVector2D(MapTexture->GetSizeX(), MapTexture->GetSizeY());
	int32 NumMips = MapTexture->GetNumMips();
	if (MapTexture&&(NumMips > MipIndex + 1))
	{
		MapTexture->LODBias = 0;
		///Mip数量小于12，即分辨率小于2048*2048则不需要缩放，取原始贴图
		if (NumMips < 12)
		{
			MipIndex = 0;
		}
		MapTexture->NumCinematicMipLevels = MipIndex;
		MapTexture->UpdateResource();
		const TIndirectArray<FTexture2DMipMap>& Texture2DMipMaps = MapTexture->GetPlatformMips();
		TextureSize = FVector2D(Texture2DMipMaps[MipIndex].SizeX, Texture2DMipMaps[MipIndex].SizeY);
	}
	return TextureSize;
}

TMap<int32, int32> UGolbalBPFunctionLibrary::SortTMapByKey(TMap<int32, int32> MapData)
{
	MapData.KeySort([](int32 A, int32 B) {
		return A < B; // sort keys in reverse
	});
	return MapData;
}

CONTROL_COMPILE_OPTIMIZE_END