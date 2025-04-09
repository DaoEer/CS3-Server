#pragma once

#include "CoreMinimal.h"
#include "ModuleManager.h"
#include "UnrealEd.h"

//DECLARE_LOG_CATEGORY_EXTERN(Love4Editor, All, All)

class FLove4EditorModule : public IModuleInterface
{
public:
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
};