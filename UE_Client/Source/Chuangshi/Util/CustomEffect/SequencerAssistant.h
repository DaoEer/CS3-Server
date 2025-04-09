#pragma once
#include "Object.h"
#include "Components/SceneComponent.h"
#include "SequencerAssistant.generated.h"


DECLARE_DELEGATE(FStopHandleFunction);

UCLASS(Blueprintable)
class CHUANGSHI_API UStopDelegateStorageComponent : public USceneComponent
{
	GENERATED_BODY()
private:

	TMap<TTuple<UObject*, UObject*>, FStopHandleFunction> StateStorageMapping;
	bool ParticleNeedStop = false;
public:
	static UStopDelegateStorageComponent* CreateAndAttachToComponent(USceneComponent*);
	static bool CheckNeedStopNotify(UStopDelegateStorageComponent* UDSC) { return IsValid(UDSC) && UDSC->ParticleNeedStop; }
	template<typename CallableFunction>
	static bool AddStopHandleFunction(UStopDelegateStorageComponent* Input, UObject* IObj, UObject* ABase, CallableFunction&& CF)
	{
		if (IsValid(Input))
		{
			Input->AddStopHandleFunction(IObj, ABase, std::forward<CallableFunction>(CF));
			return true;
		}
		return false;
	}
	static UStopDelegateStorageComponent* Get(USceneComponent*);
	void SetParticleNeedStop(bool input) { ParticleNeedStop = input; }
	bool NeedStop() const { return ParticleNeedStop; }
	template<typename CallableFunction>
	void AddStopHandleFunction(UObject* IObj, UObject* ABase, CallableFunction&& CF)
	{
		FStopHandleFunction Bind;
		Bind.BindLambda(std::move(CF));
		this->StateStorageMapping.Add(TTuple<UObject*, UObject*>(IObj, ABase), std::move(Bind));
	}
	void StopAll();
	UStopDelegateStorageComponent();
};

