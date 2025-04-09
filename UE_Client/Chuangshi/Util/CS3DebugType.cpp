#include "CS3DebugType.h"

DEFINE_LOG_CATEGORY(CL_Undefined)
DEFINE_LOG_CATEGORY(CL_GM)
DEFINE_LOG_CATEGORY(CL_Log)
DEFINE_LOG_CATEGORY(CL_Fatal)
DEFINE_LOG_CATEGORY(CL_Entity)
DEFINE_LOG_CATEGORY(CL_Actor)
DEFINE_LOG_CATEGORY(CL_Interface)
DEFINE_LOG_CATEGORY(CL_Login)
DEFINE_LOG_CATEGORY(CL_Level)
DEFINE_LOG_CATEGORY(CL_Status)
DEFINE_LOG_CATEGORY(CL_UIMananger)

#if !NO_LOGGING
const FLogCategoryBase& GetCS3DebugType(CS3DebugType DebugType)
{
	switch (DebugType)
	{
	case CS3DebugType::CL_GM:
		return CL_GM;
	case CS3DebugType::CL_Log:
		return CL_Log;
	case CS3DebugType::CL_Fatal:
		return CL_Fatal;
	case CS3DebugType::CL_Entity:
		return CL_Entity;
	case CS3DebugType::CL_Actor:
		return CL_Actor;
	case CS3DebugType::CL_Interface:
		return CL_Interface;
	case CS3DebugType::CL_Login:
		return CL_Login;
	case CS3DebugType::CL_Level:
		return CL_Level;
	case CS3DebugType::CL_Status:
		return CL_Status;
	case CS3DebugType::CL_UIMananger:
		return CL_UIMananger;
	default:
		return CL_Undefined;
	}
}
#endif

