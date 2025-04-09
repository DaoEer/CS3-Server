#include "GameData/AppearanceStyle/AppearanceStyle.h"
#include "Actor/GameCharacter.h"
#include "Engine/StreamableManager.h"
#include "Manager/ResourceManager.h"

DECLARE_CYCLE_STAT(TEXT("AppearanceStyleUtilities::ApplyAppearanceStyle"), STAT_ApplyAppearanceStyle, STATGROUP_AppearanceStyle);

void AppearanceStyleUtilities::ApplyAppearanceStyle(AGameCharacter& GameCharacter, const FAppearanceStyle& AppearanceStyle)
{
    SCOPE_CYCLE_COUNTER(STAT_ApplyAppearanceStyle);

    TArray<FStringAssetReference> Resources;
    for(const auto& MeshMaterial : AppearanceStyle.MeshMaterial)
    {
        Resources.Add(MeshMaterial.Material.ToSoftObjectPath());
    }

    if(UMeshComponent* MeshComponent = GameCharacter.GetPartMeshComponent(AppearanceStyle.ModelPartType))
    {
        TWeakObjectPtr<UMeshComponent> MeshComponentPtr(MeshComponent);
        UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(&GameCharacter, Resources,
            FStreamableDelegate::CreateLambda([MeshComponentPtr, AppearanceStyle]
            {
                if(MeshComponentPtr.IsValid())
                {
                    UMeshComponent* MeshComponent = MeshComponentPtr.Get();
                    for(const auto& Material : AppearanceStyle.MeshMaterial)
                    {
                        MeshComponent->SetMaterial(Material.ElementIndex, Material.Material.LoadSynchronous());
                    }

                    for(const auto& Parameter : AppearanceStyle.MeshMaterialParameter)
                    {
                        MeshComponent->SetScalarParameterValueOnMaterials(Parameter.ParameterName, Parameter.ParameterValue);
                    }
                }
            }),
            RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_OTHER_ENTITY,
            GameCharacter.GetActorLocation(),
            false);
    }
}
