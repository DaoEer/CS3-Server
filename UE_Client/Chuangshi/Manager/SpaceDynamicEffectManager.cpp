
#include "SpaceDynamicEffectManager.h"
#include "ResourceManager.h"
#include "Interface/Role/RoleInterface.h"
#include "Actor/Scene/SceneCharacter.h"
#include "VisibleManager.h"
#include "EventManager.h"
#include "CustomTimerManager.h"
#include"Chuangshi.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "CfgManager.h"
#include "CS3Base/GameObject.h"

CONTROL_COMPILE_OPTIMIZE_START

void UBaseEffect::StartEffect(const FSPACEDYNAMICEFFECT_DATA* dictData)
{
	InitData(dictData);
}

void USkyEffect::InitData(const FSPACEDYNAMICEFFECT_DATA* dictData)
{
	if (dictData->Param1 == "Environment")
	{
		EffectType = ESKYEFFECTENUM::Environment;
	}
	else if (dictData->Param1 == "SkyMaterial")
	{
		EffectType = ESKYEFFECTENUM::SkyMaterial;
	}
	EffectName = dictData->Param2;
	if (dictData->Param3 == "")
	{
		EffectStartTime = -1;
	}
	else
	{
		EffectStartTime = FSTRING_TO_FLOAT(dictData->Param3);
	}
}

void USkyEffect::StartEffect(const FSPACEDYNAMICEFFECT_DATA* dictData)
{
	Supper::StartEffect(dictData);
	
	switch (EffectType)
	{
		case  ESKYEFFECTENUM::Environment :
		{
			if (!EffectName.IsEmpty())
			{
				OnTriggerDynamicEnvironmentEvent(EffectName, EffectStartTime);
			}
			break; 
		}
		case  ESKYEFFECTENUM::SkyMaterial:
		{
			if (!EffectName.IsEmpty())
			{
				OnTriggerSkyMaterialEvent(EffectName, EffectStartTime);
			}
			break;
		}
		default:
		{
			break;
		}
	};
}

void USkyEffect::DestroyEffect()
{
	Supper::DestroyEffect();
	if ((EffectType== ESKYEFFECTENUM::Environment)|| (EffectType == ESKYEFFECTENUM::SkyMaterial))
	{
		OnBackDynamicEnvironmentEvent();
	}
}

void USkyEffect::StopEffect()
{
	Supper::StopEffect();
}

void USkyEffect::OnTriggerDynamicEnvironmentEvent(FString BoxEnvironmentName, float BoxEffectStartTime)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->UUECS3GameInstance::Instance->GEventManager) && UUECS3GameInstance::Instance->GEventManager->OnTriggerDynamicEnvironmentEvent.IsBound())
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("------------------------- USkyEffect::OnTriggerDynamicEnvironmentEvent BoxEnvironmentName %s"), *BoxEnvironmentName);
		UUECS3GameInstance::Instance->GEventManager->OnTriggerDynamicEnvironmentEvent.Broadcast(BoxEnvironmentName, BoxEffectStartTime);
	}
}

void USkyEffect::OnTriggerSkyMaterialEvent(FString MaterialName, float MaterialEffectStartTime)
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->UUECS3GameInstance::Instance->GEventManager) && UUECS3GameInstance::Instance->GEventManager->OnTriggerSkyMaterialvent.IsBound())
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("------------------------- USkyEffect::OnTriggerSkyMaterialEvent MaterialName %s"),*MaterialName);
		UUECS3GameInstance::Instance->GEventManager->OnTriggerSkyMaterialvent.Broadcast(MaterialName, MaterialEffectStartTime);
	}
}

void USkyEffect::OnBackDynamicEnvironmentEvent()
{
	if (IsValid(UUECS3GameInstance::Instance) && IsValid(UUECS3GameInstance::Instance->UUECS3GameInstance::Instance->GEventManager) && UUECS3GameInstance::Instance->GEventManager->OnBackDynamicEnvironmentEvent.IsBound())
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("------------------------- USkyEffect::OnBackDynamicEnvironmentEvent"));
		UUECS3GameInstance::Instance->GEventManager->OnBackDynamicEnvironmentEvent.Broadcast();
	}
}

/**
*创建纯客户端entity效果，应用于桥、门
*/
void UCreateEntityEffect::InitData(const FSPACEDYNAMICEFFECT_DATA* dictData)
{
	UId = FSTRING_TO_INT(dictData->Param2);
}

void UCreateEntityEffect::StartEffect(const FSPACEDYNAMICEFFECT_DATA* dictData)
{
	Supper::StartEffect(dictData);
	CreateActor(dictData);
}

void UCreateEntityEffect::DestroyEffect()
{	
	if (IsValid(SceneActor))
	{
		if (IsValid(Cast<ASceneCharacter>(SceneActor)))
		{
			Cast<ASceneCharacter>(SceneActor)->OnBeginDestroyActor();
		}
		else
		{
			SceneActor->Destroy();
		}		
	}
	Supper::DestroyEffect();
}

void UCreateEntityEffect::StopEffect()
{
	Supper::StopEffect();
}

void UCreateEntityEffect::CreateActor(const FSPACEDYNAMICEFFECT_DATA* dictData)
{
	UUECS3GameInstance* GameInstance = UUECS3GameInstance::Instance;
	FCREATE_ENTITY_EFFECT_DATA entityData;
	GetActorData(dictData, entityData);
	if (GameInstance && entityData.ModelNumber != "")
	{
		UClass* ActorClass = UGolbalBPFunctionLibrary::GetUClassByStr(TEXT("BP_Scene"));
		if (!ActorClass)
		{
			CS3_Warning(TEXT("-->Null Pointer error:UCreateEntityEffect::CreateActor : ActorClass!"));
			return;
		}
		GameInstance->ResourceManager->RequestAsyncLoad(this, FStringAssetReference(ActorClass),
			FStreamableDelegate::CreateLambda([this, ActorClass, entityData]()
		{
			if (ActorClass)
			{
				ASceneCharacter* RetActor = UGolbalBPFunctionLibrary::SpawnActor<ASceneCharacter>(ActorClass, entityData.Pos, entityData.Direction);
				if (RetActor)
				{				
					RetActor->CreateActorData(entityData);
					SceneActor = RetActor;
					RetActor->SceneCreateApperanceOver.AddDynamic(this,&UCreateEntityEffect::SceneCreateApperanceOverEvent);
				}
			}
		}),RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_SPACE_EFFECT);
	}
}

void UCreateEntityEffect::GetActorData(const FSPACEDYNAMICEFFECT_DATA* dictData, FCREATE_ENTITY_EFFECT_DATA &entityData)
{
	TArray<FString> modelData = UGolbalBPFunctionLibrary::SplitString(dictData->Param1);
	entityData.ModelScale = 1.0f;
	entityData.CollisionType = TEXT("COLLISION_DEFAULT");
	entityData.ModelNumber = "";
	entityData.bAffectNavigation = false;
	if (modelData.Num() >= 1)
	{
		entityData.ModelNumber = modelData[0];
		if (modelData.Num() >= 2)
		{
			entityData.ModelScale = FSTRING_TO_FLOAT(modelData[1]);
		}
		if (modelData.Num() >= 3)
		{
			entityData.CollisionType = modelData[2];		
		}
		if (modelData.Num() >= 4)
		{
			entityData.bAffectNavigation = FSTRING_TO_INT(modelData[3]) == 1 ? true : false;
		}
		if (modelData.Num() >= 5)
		{
			entityData.bCameraCollision = FSTRING_TO_INT(modelData[4]) == 1 ? true : false;
		}
		if (modelData.Num() >= 6)
		{
			entityData.bVisibilityCollision = FSTRING_TO_INT(modelData[5]) == 1 ? true : false;
		}
	}

	//解析坐标和朝向
	TArray<FString> param1 = UGolbalBPFunctionLibrary::SplitString(dictData->Param3);
	if (param1.Num() > 1)
	{
		TArray<FString>posParam = UGolbalBPFunctionLibrary::SplitString(param1[0], false, ";");
		if (posParam.Num() > 2)
		{
			entityData.Pos.X = FSTRING_TO_FLOAT(posParam[0]);
			entityData.Pos.Y = FSTRING_TO_FLOAT(posParam[1]);
			entityData.Pos.Z = FSTRING_TO_FLOAT(posParam[2]);
		}
		TArray<FString>directionParam = UGolbalBPFunctionLibrary::SplitString(param1[1], false, ";");
		if (directionParam.Num() > 2)
		{
			entityData.Direction.Roll = FSTRING_TO_FLOAT(directionParam[0]);
			entityData.Direction.Pitch = FSTRING_TO_FLOAT(directionParam[1]);
			entityData.Direction.Yaw = FSTRING_TO_FLOAT(directionParam[2]);
		}
	}
	//解析动作ID和时间间隔
	entityData.bIsRandomAction = false;
	entityData.bIsRandomEffect = false;
	
	TArray<FString>param2 = UGolbalBPFunctionLibrary::SplitString(dictData->Param4);
	if (param2.Num() == 1)
	{
		entityData.ActionNames = UGolbalBPFunctionLibrary::SplitString(param2[0], false, ";");
	}
	else if (param2.Num() > 1)
	{
		entityData.ActionNames = UGolbalBPFunctionLibrary::SplitString(param2[0], false, ";");
		TArray<FString> param3 = UGolbalBPFunctionLibrary::SplitString(param2[1], false, ";");
		for (auto& v : param3)
		{
			entityData.ActionIntervals.Add(FSTRING_TO_FLOAT(v));
		}
		if (param2.Num() > 2)
		{
			entityData.bIsRandomAction =(FSTRING_TO_INT(param2[2]) == 0) ? false : true;
		}
	}
	TArray<FString>param5 = UGolbalBPFunctionLibrary::SplitString(dictData->Param5);
	if (param5.Num() == 1)
	{
		entityData.EffectIDs = UGolbalBPFunctionLibrary::SplitString(param5[0], false, ";");
	}
	else if (param5.Num() > 1)
	{
		entityData.EffectIDs = UGolbalBPFunctionLibrary::SplitString(param5[0], false, ";");
		TArray<FString> param6 = UGolbalBPFunctionLibrary::SplitString(param5[1], false, ";");
		for (auto& v : param6)
		{
			entityData.EffectIntervals.Add(FSTRING_TO_FLOAT(v));
		}
		if (param5.Num() > 2)
		{
			entityData.bIsRandomEffect = (FSTRING_TO_INT(param5[2]) == 0)? false : true;
		}
	}
}

void UCreateEntityEffect::SceneCreateApperanceOverEvent(AGameCharacter* SceneCharacter)
{
	if (IsValid(SceneCharacter) && CreateEntityOver.IsBound() && SceneCharacter == SceneActor)
	{
		CreateEntityOver.Broadcast(this);
	}
}

/**
*改变已有场景entity的效果
*/

void UChangeEntityEffect::InitData(const FSPACEDYNAMICEFFECT_DATA* dictData)
{
	UId = FSTRING_TO_INT(dictData->Param1);	
	GetActorData(dictData);
}

void UChangeEntityEffect::StartEffect(const FSPACEDYNAMICEFFECT_DATA* dictData)
{
	Supper::StartEffect(dictData);
	UCreateEntityEffect* effect= UUECS3GameInstance::Instance->SpaceDynamicEffectManager->GetCreateEntityEffectByUId(UId);
	
	if (IsValid(effect))
	{
		ASceneCharacter* SceneActor = Cast<ASceneCharacter>(effect->GetSceneCharacter());
		if (IsValid(SceneActor) && SceneActor->GetApperanceLoadingOver())
		{			
			SceneActor->SetActionData(entityData.ActionNames, entityData.ActionIntervals, entityData.bIsRandomAction);
			SceneActor->SetEffectData(entityData.EffectIDs, entityData.EffectIntervals, entityData.bIsRandomEffect);
		}
		else
		{
			effect->CreateEntityOver.AddDynamic(this, &UChangeEntityEffect::CreateEntityOverEvent);
		}
	}
}

void UChangeEntityEffect::DestroyEffect()
{	
	UCreateEntityEffect* effect = UUECS3GameInstance::Instance->SpaceDynamicEffectManager->GetCreateEntityEffectByUId(UId);
	if (IsValid(effect))
	{
		ASceneCharacter* SceneActor = Cast<ASceneCharacter>(effect->GetSceneCharacter());
		if (IsValid(SceneActor))
		{
			SceneActor->ClearActionData();
			SceneActor->ClearEffectData();
		}
	}
	UId = 0;
	Supper::DestroyEffect();
}

void UChangeEntityEffect::StopEffect()
{
	Supper::StopEffect();
}

void UChangeEntityEffect::GetActorData(const FSPACEDYNAMICEFFECT_DATA* dictData)
{
	TArray<FString>param1 = UGolbalBPFunctionLibrary::SplitString(dictData->Param2);
	if (param1.Num() == 1)
	{
		entityData.ActionNames = UGolbalBPFunctionLibrary::SplitString(param1[0], false, ";");
	}
	else if (param1.Num() > 1)
	{
		entityData.ActionNames = UGolbalBPFunctionLibrary::SplitString(param1[0], false, ";");
		TArray<FString> param2 = UGolbalBPFunctionLibrary::SplitString(param1[1], false, ";");
		for (auto& v : param2)
		{
			entityData.ActionIntervals.Add(FSTRING_TO_FLOAT(v));
		}
		if (param1.Num() > 2)
		{
			entityData.bIsRandomAction =(FSTRING_TO_INT(param1[2]) == 0) ? false : true;
		}
	}
	TArray<FString>param3 = UGolbalBPFunctionLibrary::SplitString(dictData->Param3);

	if (param3.Num() == 1)
	{
		entityData.EffectIDs = UGolbalBPFunctionLibrary::SplitString(param3[0], false, ";");
	}
	else if (param3.Num() > 1)
	{
		entityData.EffectIDs = UGolbalBPFunctionLibrary::SplitString(param3[0], false, ";");
		TArray<FString> param4 = UGolbalBPFunctionLibrary::SplitString(param3[1], false, ";");
		for (auto& v : param4)
		{
			entityData.EffectIntervals.Add(FSTRING_TO_FLOAT(v));
		}
		if (param3.Num() > 2)
		{
			entityData.bIsRandomEffect = (FSTRING_TO_INT(param3[2]) == 0) ? false : true;
		}
	}
}

void UChangeEntityEffect::CreateEntityOverEvent(UBaseEffect* InEffect)
{
	UCreateEntityEffect* effect = UUECS3GameInstance::Instance->SpaceDynamicEffectManager->GetCreateEntityEffectByUId(UId);
	if (IsValid(effect) && effect == InEffect)
	{
		ASceneCharacter* SceneActor = Cast<ASceneCharacter>(effect->GetSceneCharacter());
		if (SceneActor&& IsValid(SceneActor) && SceneActor->GetApperanceLoadingOver())
		{
			SceneActor->SetActionData(entityData.ActionNames, entityData.ActionIntervals, entityData.bIsRandomAction);
			SceneActor->SetEffectData(entityData.EffectIDs, entityData.EffectIntervals, entityData.bIsRandomEffect);
		}
	}
}

/**
*销毁已有场景entity
*/
void UDestroyEntityEffect::InitData(const FSPACEDYNAMICEFFECT_DATA* dictData)
{
	Count = 0;	
	cbids.Empty();
}

void UDestroyEntityEffect::StartEffect(const FSPACEDYNAMICEFFECT_DATA* dictData)
{
	Supper::StartEffect(dictData);
	TArray<FString> param1 = UGolbalBPFunctionLibrary::SplitString(dictData->Param1);
	TArray<FString> param2 = UGolbalBPFunctionLibrary::SplitString(dictData->Param2);
	TMap<int32, float> EntityDestroyInfos;
	float MaxDelayTime = 0.0f;
	for (int i = 0; i < param1.Num(); i++)
	{
		if (param2.Num() > i)
		{
			EntityDestroyInfos.Add(FSTRING_TO_INT(param1[i]), FSTRING_TO_FLOAT(param2[i]));
		}
		else
		{
			EntityDestroyInfos.Add(FSTRING_TO_INT(param1[i]), 0.0f);
		}
	}
	TArray<FString> ActionName = UGolbalBPFunctionLibrary::SplitString(dictData->Param3);
	TArray<FString>EffectName = UGolbalBPFunctionLibrary::SplitString(dictData->Param4);
	int index = 0;
	for (auto v: EntityDestroyInfos)
	{
		UBaseEffect* effect = UUECS3GameInstance::Instance->SpaceDynamicEffectManager->GetCreateEntityEffectByUId(v.Key);
		if (IsValid(effect))
		{
			UCreateEntityEffect* createEntityEffect = Cast<UCreateEntityEffect>(effect);
			if (IsValid(createEntityEffect)&& IsValid(createEntityEffect->GetSceneCharacter()))
			{
				ASceneCharacter*  SceneCharacter =Cast<ASceneCharacter>(createEntityEffect->GetSceneCharacter());
				if (IsValid(SceneCharacter))
				{
					if (ActionName.Num() > index)
					{
						SceneCharacter->SetDestroyAction(ActionName[index]);
					}
					if (EffectName.Num() > index)
					{
						SceneCharacter->SetDestroyEffect(EffectName[index]);
					}
				}				
			}
			index++;
			if (v.Value > 0)
			{
				if (MaxDelayTime<v.Value)
				{
					MaxDelayTime = v.Value;
				}
				FTimerHandle DelayHandle;
				TWeakObjectPtr<UDestroyEntityEffect> DelayThisPtr(this);
				int32 EntityUID = v.Key;
				UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayHandle,
					FTimerDelegate::CreateLambda([DelayThisPtr,EntityUID]() {
					if (DelayThisPtr.IsValid())
					{
						UDestroyEntityEffect* ThisPtr = DelayThisPtr.Get();
						UUECS3GameInstance::Instance->SpaceDynamicEffectManager->ClearEffectByUId(EntityUID);
						ThisPtr->Count++;
					}
				}), v.Value, false);
				cbids.Add(DelayHandle);
			}
			else
			{
				UUECS3GameInstance::Instance->SpaceDynamicEffectManager->ClearEffectByUId(v.Key);
			}
		}
	}
	if (MaxDelayTime>0.0f)
	{
		TWeakObjectPtr<UDestroyEntityEffect> DelayThisPtr(this);
		FTimerHandle DelayHandle;
		UUECS3GameInstance::Instance->CustomTimerManager->SetTimer(this, DelayHandle,
			FTimerDelegate::CreateLambda([DelayThisPtr]() {
			if (DelayThisPtr.IsValid()&&IsValid(DelayThisPtr.Get()))
			{
				UUECS3GameInstance::Instance->SpaceDynamicEffectManager->ClearEffectByEffect(DelayThisPtr.Get());
			}
		}), MaxDelayTime + 0.1f, false);
		cbids.Add(DelayHandle);
	}
	else
	{
		UUECS3GameInstance::Instance->SpaceDynamicEffectManager->ClearEffectByEffect(this);		
	}
}

void UDestroyEntityEffect::DestroyEffect()
{
	for (auto& v : cbids)
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(v);
	}
	cbids.Empty();
	Supper::DestroyEffect();
}

void UDestroyEntityEffect::StopEffect()
{
	Supper::StopEffect();
}


void UCreateEffectByScript::StartEffect(const FSPACEDYNAMICEFFECT_DATA * dictData)
{
	UClass* ActorClass = UGolbalBPFunctionLibrary::GetUClassByStr(dictData->Param1);
	if (!ActorClass)
	{
		CS3_Warning(TEXT("-->Null Pointer error:UCreateEffectByScript::CreateActor : %s!"),*dictData->Param1);
		return;
	}
	//解析坐标和朝向
	TArray<FString> param2 = UGolbalBPFunctionLibrary::SplitString(dictData->Param2);
	FVector Pos;
	FRotator Direction;
	if (param2.Num() > 1)
	{
		TArray<FString> posParam = UGolbalBPFunctionLibrary::SplitString(param2[0], false, ";");
		if (posParam.Num() > 2)
		{
			Pos.X = FSTRING_TO_FLOAT(posParam[0]);
			Pos.Y = FSTRING_TO_FLOAT(posParam[1]);
			Pos.Z = FSTRING_TO_FLOAT(posParam[2]);
		}
		TArray<FString> directionParam = UGolbalBPFunctionLibrary::SplitString(param2[1], false, ";");
		if (directionParam.Num() > 2)
		{
			Direction.Roll = FSTRING_TO_FLOAT(directionParam[0]);
			Direction.Pitch = FSTRING_TO_FLOAT(directionParam[1]);
			Direction.Yaw = FSTRING_TO_FLOAT(directionParam[2]);
		}
	}
	SceneActor = UGolbalBPFunctionLibrary::SpawnActor<ASceneCharacter>(ActorClass, Pos, Direction);
	if (IsValid(SceneActor))
	{
		SceneActor->InitEffectData(*dictData);
	}

}

void UCreateEffectByScript::DestroyEffect()
{
	if (IsValid(SceneActor))
	{
		if (IsValid(Cast<ASceneCharacter>(SceneActor)))
		{
			Cast<ASceneCharacter>(SceneActor)->OnBeginDestroyActor();
		}
		else
		{
			SceneActor->Destroy();
		}
	}
	Supper::DestroyEffect();
}


/**
* 根据服务器设置spaceData，客户端动态改变地图相关效果
*/
USpaceDynamicEffectManager::USpaceDynamicEffectManager()
{
	Effects.Reset();
	cbids.Reset();
}

USpaceDynamicEffectManager::~USpaceDynamicEffectManager()
{

}

USpaceDynamicEffectManager* USpaceDynamicEffectManager::GetInstance()
{
	cs3_checkNoReentry();

	return NewObject<USpaceDynamicEffectManager>();
}

void USpaceDynamicEffectManager::onEnterWorld()
{
	//AddAllEffect();

	int32 entityID = UGolbalBPFunctionLibrary::GetPlayerID();
	if (entityID > 0)
	{
		GameObject* CS3PlayerEntity = UGolbalBPFunctionLibrary::GetCS3PlayerEntity();
		if (CS3PlayerEntity == nullptr) return;

		URoleInterface* Interface = Cast<URoleInterface>(CS3PlayerEntity->Interface_Cache.GameObjectInterface);
		if (IsValid(Interface) && !Interface->SpaceDynamicEffectDelegate.IsAlreadyBound(this, &USpaceDynamicEffectManager::OnSpaceEffectChanged))
		{
			Interface->SpaceDynamicEffectDelegate.AddDynamic(this, &USpaceDynamicEffectManager::OnSpaceEffectChanged);
		}
	}
}

void USpaceDynamicEffectManager::onLeaveWorld()
{
	ClearAllCB();
}

void USpaceDynamicEffectManager::OnLeaveScenes()
{
	DelAllEffect();
}

void USpaceDynamicEffectManager::AddEffect(int32 effectID)
{
	if (Effects.Contains(effectID))return;
	const FSPACEDYNAMICEFFECT_DATA* dictData = GetSpaceDynamicEffectData(INT_TO_FSTRING(effectID));
	if (!dictData)
	{
		CS3_Warning(TEXT("-->Null Pointer error:USpaceDynamicEffectManager::AddEffect : dictData!"));
		return;
	}
	if (!dictData->ClassType.ToSoftObjectPath().IsValid())
	{
		CS3_Warning(TEXT("-->Null Pointer error:USpaceDynamicEffectManager::AddEffect : ClassType SoftObjectPath Is not Valid!"));
		return;
	}
	CS3_Display(CS3DebugType::CL_Undefined, TEXT("USpaceDynamicEffectManager::addEffect-->effectID[%d]"), effectID);
	
	UClass* _cls = LoadClass<UBaseEffect>(this, *(dictData->ClassType.ToString()));
	UBaseEffect* effect = NewObject<UBaseEffect>(this, _cls);
	if (effect)
	{
		Effects.Add(effectID, effect);
		effect->StartEffect(dictData);
	}
	
}

void USpaceDynamicEffectManager::AddAllEffect()
{
	if (KBEngine::Entity* Player = UUECS3GameInstance::Instance->pKBEApp->Player())
	{
		TArray<int32> effectList;
		TArray<FVariant> array = Player->GetDefinedProperty(TEXT("effectList")).GetValue<TArray<FVariant>>();
		for (int i = 0; i < array.Num(); i++)
		{
			effectList.Add(int32(array[i].GetValue<int32>()));
		}
	
		for (auto& effect : Effects)
		{
			UBaseEffect* BaseEffect = effect.Value;
			if (IsValid(BaseEffect))
			{
				BaseEffect->DestroyEffect();
			}
		}
		Effects.Reset();
		if (effectList.Num() > 0)
		{
			for (auto eid : effectList)
			{
				AddEffect(eid);
			}
		}
	}
}

void USpaceDynamicEffectManager::DelEffect(int32 effectID)
{
	if (Effects.Contains(effectID))
	{
		UBaseEffect* effect= Effects[effectID];
		if (IsValid(effect))
		{
			effect->StopEffect();
		}
		Effects.Remove(effectID);
	}
}

void USpaceDynamicEffectManager::ClearEffect(int32 effectID)
{
	if (Effects.Contains(effectID))
	{
		UBaseEffect* effect = Effects[effectID];
		if (IsValid(effect))
		{
			effect->DestroyEffect();
		}
		Effects.Remove(effectID);
	}
}

void USpaceDynamicEffectManager::DelAllEffect()
{
	for (auto i = Effects.CreateIterator(); i; ++i)
	{
		if (IsValid(i.Value()))
		{
			ClearEffect(i.Key());
		}
	}
	Effects.Reset();
}

void USpaceDynamicEffectManager::OnSpaceEffectChanged(TArray<int32> EffectList)
{
	if (KBEngine::Entity* Player = UUECS3GameInstance::Instance->pKBEApp->Player())
	{	
		//删除已经不存在的效果
		for (auto i = Effects.CreateIterator(); i; ++i)
		{
			if (IsValid(i.Value()))
			{
				if (!EffectList.Contains(i.Key()))
				{
					ClearEffect(i.Key());
				}
			}
		}
		//增加新的效果
		for (auto eid : EffectList)
		{
			AddEffect(eid);
		}
	}
}

UCreateEntityEffect* USpaceDynamicEffectManager::GetCreateEntityEffectByUId(int32 entityUId)
{
	if (Effects.Num()<1)return nullptr;
	for (auto& effect : Effects)
	{
		if (IsValid(effect.Value))
		{
			UCreateEntityEffect* BaseEffect = Cast<UCreateEntityEffect>(effect.Value);
			if (IsValid(BaseEffect))
			{
				if (BaseEffect->GetUId() == entityUId)
				{
					return BaseEffect;
				}
			}
		}
	}
	return nullptr;
}

void USpaceDynamicEffectManager::ClearEffectByUId(int32 entityUId)
{
	if (Effects.Num() < 1)return;
	TArray<int32>  TempClearEffectsID;
	for (auto& effect : Effects)
	{
		if (IsValid(effect.Value))
		{
			UChangeEntityEffect* BaseEffect = Cast<UChangeEntityEffect>(effect.Value);
			if (IsValid(BaseEffect))
			{
				if (BaseEffect->GetUId() == entityUId)
				{
					int32 Index= *(Effects.FindKey(BaseEffect));
					if (Index > -1)
					{
						TempClearEffectsID.Add(Index);
					}
				}
			}
			else
			{
				UCreateEntityEffect* TempBaseEffect = Cast<UCreateEntityEffect>(effect.Value);
				if (IsValid(TempBaseEffect))
				{
					if (TempBaseEffect->GetUId() == entityUId)
					{
						int32 Index = *(Effects.FindKey(TempBaseEffect));
						if (Index > -1)
						{
							TempClearEffectsID.Add(Index);
						}
					}
				}
			}
		}
	}
	for (auto& EffectsID : TempClearEffectsID)
	{
		ClearEffect(EffectsID);
	}
}

void USpaceDynamicEffectManager::ClearEffectByEffect(UBaseEffect* effect)
{
	if (IsValid(effect))
	{
		int32 effectId= GetEffectIDByEffect(effect);
		if (effectId>0)
		{
			ClearEffect(effectId);
		}
	}	
}

int32 USpaceDynamicEffectManager::GetEffectIDByEffect(UBaseEffect * effect)
{
	if (Effects.Num() < 1)return 0;
	if (!IsValid(effect))
	{
		CS3_Warning(TEXT("-->Null Pointer error:USpaceDynamicEffectManager::GetEffectIDByEffect: effect!"));
		return 0;
	}
	for (auto& t : Effects)
	{
		UBaseEffect* TempEffect = Cast<UBaseEffect>(t.Value);
		if (IsValid(TempEffect) && effect == TempEffect)
		{
			return (int32)t.Key;
		}
	}
	return 0;
}

void USpaceDynamicEffectManager::ClearAllCB()
{
	for (auto timer : cbids)
	{
		UUECS3GameInstance::Instance->CustomTimerManager->ClearTimer(timer);
	}
	cbids.Reset();
}

void USpaceDynamicEffectManager::UpdateModelVisible(TArray<FString> IgnoreUIDs)
{
	for (auto& effect : Effects)
	{
		if (IsValid(effect.Value))
		{
			UCreateEntityEffect* BaseEffect = Cast<UCreateEntityEffect>(effect.Value);
			if (IsValid(BaseEffect))
			{
				if (IgnoreUIDs.Num() > 0 && UGolbalBPFunctionLibrary::IsContainStr(INT_TO_FSTRING(BaseEffect->GetUId()), IgnoreUIDs))continue;

				AGameCharacter* GameCharacter = BaseEffect->GetSceneCharacter();
				if (IsValid(GameCharacter))
				{
					UUECS3GameInstance::Instance->VisibleManager->UpdateModelVisible(GameCharacter);
				}
			}
		}
	}
}

int32 USpaceDynamicEffectManager::GetSceneCharacterUID(AActor* Actor)
{
	AGameCharacter* SceneCharacter = Cast<AGameCharacter>(Actor);
	if (IsValid(SceneCharacter))
	{
		for (auto& effect : Effects)
		{
			if (IsValid(effect.Value))
			{
				UCreateEntityEffect* BaseEffect = Cast<UCreateEntityEffect>(effect.Value);
				if (IsValid(BaseEffect))
				{
					AGameCharacter* GameCharacter = BaseEffect->GetSceneCharacter();
					if (IsValid(GameCharacter)&& SceneCharacter == GameCharacter)
					{
						return BaseEffect->GetUId();
					}
				}
			}
		}
	}
	return 0;
}

const FSPACEDYNAMICEFFECT_DATA* USpaceDynamicEffectManager::GetSpaceDynamicEffectData(const FString& EffectsId)
{
	if (!(UUECS3GameInstance::Instance && UUECS3GameInstance::Instance->CfgManager))
	{
		CS3_Warning(TEXT("-->Null Pointer error:USpaceDynamicEffectManager::GetSpaceDynamicEffectData : (Instance && Instance->CfgManager)!"));
		return nullptr;
	}
	const FSPACEDYNAMICEFFECT_DATA* SpaceDynamicEffectData =
		UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CONFIG_SPACE_DYNAMIC_EFFECT)->GetRow<FSPACEDYNAMICEFFECT_DATA>(EffectsId);
	if (!SpaceDynamicEffectData) CS3_Warning(TEXT("-->Null Pointer error:USpaceDynamicEffectManager::GetSpaceDynamicEffectData : SpaceDynamicEffectData!"));

	return SpaceDynamicEffectData;
}

CONTROL_COMPILE_OPTIMIZE_END

