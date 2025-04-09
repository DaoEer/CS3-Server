// Fill out your copyright notice in the Description page of Project Settings.

using UnrealBuildTool;
using System.Collections.Generic;

public class ChuangshiEditorTarget : TargetRules
{
	public ChuangshiEditorTarget(TargetInfo Target):base(Target)
	{
		Type = TargetType.Editor;
        //bUseUnityBuild = false;
        ExtraModuleNames.AddRange( new string[] { "Chuangshi","ChuangshiEditor" } );
	}
}
