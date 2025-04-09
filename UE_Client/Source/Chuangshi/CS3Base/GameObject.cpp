
#include "GameObject.h"
#include "../Actor/ServerCharacter.h"
#include "Interface/GameObjectInterface.h"
#include "Kismet/GameplayStatics.h"
#include "GameData/GameDeFine.h"
#include "Manager/SpaceEntityRelationMgr.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "Util/CS3Debug.h"
CONTROL_COMPILE_OPTIMIZE_START

KBE_BEGIN_ENTITY_METHOD_MAP(GameObject, Supper)
KBE_END_ENTITY_METHOD_MAP()

KBE_BEGIN_ENTITY_PROPERTY_MAP(GameObject, Supper)
	DECLARE_PROPERTY_CHANGED_NOTIFY(flags, &GameObject::Set_flags, int64)
	DECLARE_PROPERTY_CHANGED_NOTIFY(appearanceColor, &GameObject::Set_appearanceColor, int32)
KBE_END_ENTITY_PROPERTY_MAP()

GameObject::GameObject()
{
}

GameObject::~GameObject()
{

}

void GameObject::Set_flags(const int64 &newValue, const int64 &oldValue)
{
	OnSet_flags(newValue, oldValue);
}

void GameObject::OnSet_flags(const int64 &newValue, const int64 &oldValue)
{

}

void GameObject::Set_appearanceColor(const int32 &newValue, const int32 &oldValue)
{
	if (IsValid(Actor()))
	{
		AServerCharacter* ServerActor = Cast<AServerCharacter>(Actor());

		if (IsValid(ServerActor))
		{
			ServerActor->OnAppearanceColorChanged(newValue);
		}
	}
}

UClass* GameObject::GetEntityModelClassAsset()
{
	return UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("GameCharacter"));
}

bool GameObject::IsPlayerID(int32 entityID)
{
	if (UUECS3GameInstance::pKBEApp == nullptr)
	{
		return false;
	}
	return entityID == UUECS3GameInstance::pKBEApp->Player()->ID();
}

void GameObject::Set_Position(const FVector& oldVal)
{
	if (!IsSyncServerPos())return;

	Supper::Set_Position(oldVal);

	AServerCharacter* ServerActor = Cast<AServerCharacter>(Actor());

	if (IsValid(ServerActor))
	{
		ServerActor->SetPosition(LocalPosition(), ParentID());
	}
	else
	{
		ServerSetPos = Position();
		//CS3_Warning(TEXT("--------------------2----GameObject::Set_Position---ServerSetPos.Z:%f"), ServerSetPos.Z);
	}

}
void GameObject::Set_Direction(const FVector& oldVal)
{
	NewCharacterDirection = FVector(0, 0, localDirection_.Z);
	if (!IsSyncServerPos())return;
	Supper::Set_Direction(oldVal);

	AServerCharacter* ServerActor = Cast<AServerCharacter>(Actor());

	if (IsValid(ServerActor))
	{
		ServerActor->SetDirection(LocalDirection(), ParentID());
	}
}

const FString& GameObject::GetActorName()
{
	return _fActorName;
}


//const FName& GameObject::GetCompontentName()
//{
//	return _fCompontentName;
//}

void GameObject::OnEnterWorld()
{
	Supper::OnEnterWorld();
}

void GameObject::OnLeaveWorld()
{
	Supper::OnLeaveWorld();
}

COMBAT_RELATION GameObject::QueryRelation(KBEngine::Entity* TargetEntity)
{
	if (ID() == TargetEntity->ID())
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}

	URelationBase* RelationIns = GetEntityRelationIns();
	if (!IsValid(RelationIns))
	{
		return COMBAT_RELATION::COMBAT_RELATION_NORMAL;
	}
	
	return RelationIns->GetRelation(this, TargetEntity);
}

URelationBase* GameObject::GetEntityRelationIns()
{
	ENTITY_TYPE_EXT EntityFlagExt = ENTITY_TYPE_EXT::ENTITY_FLAG_EXT_UNKNOWN;

	UGameObjectInterface * Interface = Interface_Cache.GameObjectInterface;
	if (IsValid(Interface))
	{
		EntityFlagExt = Interface->GetEntityFlagExt();
	}
	return UUECS3GameInstance::Instance->SpaceEntityRelationMgr->GetRelationIns(EntityFlagExt);
}

void GameObject::OnUpdateVolatileData()
{
	NewCharacterDirection = FVector(0, 0, localDirection_.Z);
	if (!IsSyncServerPos())return;
	Supper::OnUpdateVolatileData();
	if (IsValid(Actor()))
	{
		AServerCharacter* ServerActor = Cast<AServerCharacter>(Actor());
		if (IsValid(ServerActor))
		{
			ServerActor->onUpdateVolatileData(LocalPosition(), LocalDirection(), ParentID());
		}
	}
}

void GameObject::OnUpdateVolatileDataByParent()
{
	AServerCharacter* ServerActor = Cast<AServerCharacter>(Actor());

	if (IsValid(ServerActor))
	{
		ServerActor->OnUpdateVolatileDataByParent(LocalPosition(), LocalDirection(), ParentID());
	}
}

void GameObject::OnGotParentEntity()
{
	AServerCharacter* ServerActor = Cast<AServerCharacter>(Actor());

	if (IsValid(ServerActor))
	{
		ServerActor->OnGotParentEntity();
	}
}

void GameObject::OnLoseParentEntity()
{
	AServerCharacter* ServerActor = Cast<AServerCharacter>(Actor());

	if (IsValid(ServerActor))
	{
		ServerActor->OnLoseParentEntity();
	}
}

void VariantToStringFun(const FVariant& Data, FString& Out)
{
	switch (Data.GetType())
	{
	case EVariantTypes::String:		Out = Data.GetValue<FString>(); break;
	case EVariantTypes::Widechar:	Out = Data.GetValue<FString>(); break;
	default: check(false); break;
	}
}

void VariantToInt32Fun(const FVariant& Data, int32& Out)
{
	switch (Data.GetType())
	{
	case EVariantTypes::UInt8:	Out = static_cast<int32>(Data.GetValue<uint8>()); break;
	case EVariantTypes::UInt16:	Out = static_cast<int32>(Data.GetValue<uint16>()); break;
	case EVariantTypes::UInt32:
	{
		uint32 value = Data.GetValue<uint32>();
		check(value <= MAX_int32);
		Out = static_cast<int32>(value);
		break;
	}
	case EVariantTypes::UInt64:
	{
		uint64 value = Data.GetValue<uint64>();
		check(value <= MAX_int32);
		Out = static_cast<int32>(value);
		break;
	}
	case EVariantTypes::Int8:	Out = static_cast<int32>(Data.GetValue<int8>()); break;
	case EVariantTypes::Int16:	Out = static_cast<int32>(Data.GetValue<int16>()); break;
	case EVariantTypes::Int32:	Out = Data.GetValue<int32>(); break;
	default: check(false); break;
	}
}

bool GameObject::IsState(ENTITY_STATE EntityState)
{
	return false;
}

const FVector &GameObject::LocalDirection()
{
	if (IsDirectionSameToEntity)
	{
		return Supper::LocalDirection();
	}
	return NewCharacterDirection;
}


FAModelInfo GameObject::GetModelInfo()
{
	FAModelInfo AModelInfo;
	AModelInfo.BodyModel = (FString)GetDefinedProperty(TEXT("bodyModel"));
	AModelInfo.HeadModel = (FString)GetDefinedProperty(TEXT("headModel"));
	AModelInfo.SuitsModel = (FString)GetDefinedProperty(TEXT("suitsModel"));
	AModelInfo.HairModel = (FString)GetDefinedProperty(TEXT("hairModel"));
	AModelInfo.AdornModel = (FString)GetDefinedProperty(TEXT("adornModel"));
	AModelInfo.HeadAdornModel = (FString)GetDefinedProperty(TEXT("headAdornModel"));
	AModelInfo.FaceAdornModel = (FString)GetDefinedProperty(TEXT("faceAdornModel"));
	AModelInfo.BackAdornModel = (FString)GetDefinedProperty(TEXT("backAdornModel"));
	AModelInfo.WaistAdornModel = (FString)GetDefinedProperty(TEXT("waistAdornModel"));
	AModelInfo.HatModel = (FString)GetDefinedProperty(TEXT("hatModel"));
	AModelInfo.CoatModel = (FString)GetDefinedProperty(TEXT("coatModel"));
	AModelInfo.WristModel = (FString)GetDefinedProperty(TEXT("wristModel"));
	AModelInfo.GlovesModel = (FString)GetDefinedProperty(TEXT("handModel"));
	AModelInfo.WaistModel = (FString)GetDefinedProperty(TEXT("waistModel"));
	AModelInfo.PantsModel = (FString)GetDefinedProperty(TEXT("pantsModel"));
	AModelInfo.ShoesModel = (FString)GetDefinedProperty(TEXT("shoesModel"));
	AModelInfo.NecklaceModel = (FString)GetDefinedProperty(TEXT("necklaceModel"));
	AModelInfo.LringModel = (FString)GetDefinedProperty(TEXT("lringModel"));
	AModelInfo.RringModel = (FString)GetDefinedProperty(TEXT("rringModel"));
	AModelInfo.CloakModel = (FString)GetDefinedProperty(TEXT("cloakModel"));
	AModelInfo.FaBaoModel = (FString)GetDefinedProperty(TEXT("fabaoModel"));
	AModelInfo.WeaponModel = (FString)GetDefinedProperty(TEXT("weaponModel"));
	AModelInfo.SkeletalWeaponModel = (FString)GetDefinedProperty(TEXT("skeletalWeaponModel"));
	AModelInfo.bodyLightEffect = (FString)GetDefinedProperty(TEXT("bodyLightEffect"));
	return AModelInfo;
}

FString GameObject::GetPartIdByType(MODEL_PART_TYPE PartType)
{
	TArray<FString> PartIdArray = { "bodyModel","headModel","suitsModel","hairModel","adornModel","headAdornModel","faceAdornModel",
		"backAdornModel","waistAdornModel","Null","hatModel","coatModel","wristModel","handModel","waistModel","pantsModel","shoesModel",
		"necklaceModel" ,"lringModel","rringModel","Null","weaponModel" ,"Null","cloakModel","fabaoModel","Null" ,"Null","bodyLightEffect" };
	int32 Index = (int32)PartType - 10;
	if (!PartIdArray.IsValidIndex(Index))
	{
		return "";
	}
	FString PartIdName = PartIdArray[Index];
	FString ModePartId = (FString)GetDefinedProperty(PartIdName);
	return ModePartId;
}

void GameObject::BindActorToEntity(AServerCharacter* InServerCharacter, bool bHasBegunPlay /* = false */)
{
	Supper::BindActorToEntity(InServerCharacter, bHasBegunPlay);
	Actor(InServerCharacter);
	InServerCharacter->BindLinkEntity(this);
	if (!bHasBegunPlay)
	{
		FTransform SpawnTransform = FTransform();
		SpawnTransform.SetLocation(Position());
		SpawnTransform.SetRotation(FQuat::MakeFromEuler(Direction()));
		UGameplayStatics::FinishSpawningActor(InServerCharacter, SpawnTransform);		
	}
	SetEntityStatus(CS3EntityStatus::BindedActor);
	BindActorToInterface(InServerCharacter);

	InServerCharacter->OnBindToEntity();
	OnBindActorToEntity();

	CS3_Log(TEXT("GameObject::CreateCharacter End classname[%s],[%d]"), *ClassName(), ID());

	DealCacheMsgs();	
}

void GameObject::OnBindActorToEntity()
{
	int64 Flags = GetDefinedProperty(TEXT("flags")).GetValue<int64>();
	Set_flags(Flags, 0);

	CELL_onClientReady();
}

void GameObject::UnBindActorToEntity()
{
	CS3_Log(TEXT("CS3Entity::UnBindActorToEntity classname[%s],[%d]"), *ClassName(), ID());

	if (IsValid(Actor()))
	{
		AServerCharacter* ServerActor = Cast<AServerCharacter>(Actor());

		if (IsValid(ServerActor))
		{
			ServerActor->OnUnBindActorCallBack();
			ServerActor->BindLinkEntity(nullptr);
			Actor(nullptr);
			ServerActor->SetLifeSpan(0.1f);
			CS3_Log(TEXT("Destroy ServerCharacter EntityID[%d], Name[%s]"), ID(), *ClassName());
		}
	}
	else //正常情况不会走到这里，处理异常情况
	{
		CS3_Warning(TEXT("----------------CS3Entity::UnBindActorToEntity:error! entity.id:%d---------------------"), ID());
		Actor(nullptr);
	}
	SetEntityStatus(CS3EntityStatus::UnBindedActor);
}

void GameObject::CELL_onClientReady()
{
	KBEngine::FVariantArray Args;
	CellCall(TEXT("CELL_onClientReady"), Args);
}


void GameObject::CreateCharacter()
{
	CS3_Log(TEXT("GameObject::CreateCharacter Begin classname[%s],[%d]"), *ClassName(), ID());
	DoCreateCharacter();
}

CONTROL_COMPILE_OPTIMIZE_END
