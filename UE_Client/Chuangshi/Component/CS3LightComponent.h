// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Components/DirectionalLightComponent.h"
#if WITH_EDITOR
#include "SLevelViewport.h"
#endif // WITH_EDITOR
#include "CS3LightComponent.generated.h"


UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class CHUANGSHI_API UCS3LightComponent : public UActorComponent
{
	GENERATED_BODY()

public:	
	// Sets default values for this component's properties
	UCS3LightComponent();

protected:
	// Called when the game starts
	virtual void BeginPlay() override;

private:
	bool LightTag = true;
#if WITH_EDITOR
	SLevelViewport* ActiveLevelViewport;
#endif // WITH_EDITOR
public:	
	// Called every frame
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	UPROPERTY(VisibleAnywhere, BlueprintReadWrite)
		UDirectionalLightComponent* SceneLight;

	UFUNCTION(BlueprintCallable, Category = "Game|CS3Light")
		void CreateLight();

	void InitLightData();
};
