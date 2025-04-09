// Fill out your copyright notice in the Description page of Project Settings.

using UnrealBuildTool;

public class Chuangshi : ModuleRules
{
	public Chuangshi(ReadOnlyTargetRules Target) : base(Target)
    {
        PublicDependencyModuleNames.AddRange(new string[] {
            "Core",
            "CoreUObject",
            "MovieScene",
            "Engine",
            "InputCore",
            "KBEngine",
            "Json",
            "UMG",
            "LevelSequence",
            "Landscape",
            "AnimGraphRuntime",
            "JSONQuery",
            "JsonUtilities",
            "MoviePlayer",
            "Paper2D",
            "LoadVersionPak", 
            "HorizonUI",
            "LandSample",
            "AnimationEditorEX",
            "ApexDestruction",
            "AssetRegistry",
            "MediaAssets",
            "AIModule",
            "NavigationSystem",
            "Scene3DUI",
            "TransparentPrimitive",
            "QRcode",
            "Http",
            "MoviePlayer",
            "MultiLog",
            "SignificanceManager",
            "AIModule", 
            "GameplayTasks",
            "PreloadingPlugin",
            "GameplayTags",
            "AnimatedTexture",
        });

        if (Target.bBuildEditor) {
            PublicDependencyModuleNames.AddRange(new string[] {
                "UnrealEd",
                "DesktopPlatform",
                "LevelEditor"
            });
        }

        PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore"});

        bEnableExceptions = true;
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        // Uncomment if you are using Slate UI
        // PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });

        // Uncomment if you are using online features
        // PrivateDependencyModuleNames.Add("OnlineSubsystem");
        // if ((Target.Platform == UnrealTargetPlatform.Win32) || (Target.Platform == UnrealTargetPlatform.Win64))
        // {
        //		if (UEBuildConfiguration.bCompileSteamOSS == true)
        //		{
        //			DynamicallyLoadedModuleNames.Add("OnlineSubsystemSteam");
        //		}
        // }
    }
}
