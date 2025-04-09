using UnrealBuildTool;

public class ChuangshiEditor : ModuleRules
{
    public ChuangshiEditor(ReadOnlyTargetRules Target) : base(Target)
    {
        PublicDependencyModuleNames.AddRange(
                new string[] {
                    "Chuangshi",
                    "UnrealEd",
                    "Core",
                    "CoreUObject",
                    "Engine",
                    "InputCore",
                    "AnimGraph",
                    "AnimGraphRuntime",
                    "BlueprintGraph",
                    "Slate",
                    "SlateCore",
                    "MoviePlayer",
                    "Blutility",
                    "AssetRegistry",
                }
            );

        PublicIncludePaths.AddRange(
          new string[]{
                "ChuangshiEditor/Public"
          });

        PrivateIncludePaths.AddRange(
            new string[] {
        "ChuangshiEditor/Private"
    });
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
    }
}
