#pragma once
#include "Logging/LogMacros.h"
#include "UObject/ObjectMacros.h"
#include "CS3DebugType.generated.h"

#define CS3DebugTypeName_Prefix "CL_"

DECLARE_LOG_CATEGORY_EXTERN(CL_Undefined, Warning, All)
DECLARE_LOG_CATEGORY_EXTERN(CL_GM, Warning, All)
DECLARE_LOG_CATEGORY_EXTERN(CL_Log, Log, All)
DECLARE_LOG_CATEGORY_EXTERN(CL_Fatal, Fatal, All)
DECLARE_LOG_CATEGORY_EXTERN(CL_Entity, Warning, All)
DECLARE_LOG_CATEGORY_EXTERN(CL_Actor, Warning, All)
DECLARE_LOG_CATEGORY_EXTERN(CL_Interface, Warning, All)
DECLARE_LOG_CATEGORY_EXTERN(CL_Login, Warning, All)
DECLARE_LOG_CATEGORY_EXTERN(CL_Level, Warning, All)
DECLARE_LOG_CATEGORY_EXTERN(CL_Status, Warning, All)
DECLARE_LOG_CATEGORY_EXTERN(CL_UIMananger, Warning, All)


UENUM(BlueprintType)
enum class CS3DebugType : uint8
{
	CL_Undefined,
	CL_GM,
	CL_Log,
	CL_Fatal,
	CL_Entity,
	CL_Actor,
	CL_Interface,
	CL_Login,
	CL_Level,
	CL_Status,
	CL_UIMananger,
};

#if !NO_LOGGING
const FLogCategoryBase& GetCS3DebugType(CS3DebugType DebugType);
#endif