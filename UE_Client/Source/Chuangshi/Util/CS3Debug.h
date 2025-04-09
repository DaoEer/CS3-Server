/*
* 文件名称：CS3Debug.h
* 功能说明：调试相关工具
* 文件作者：yanjingxin
* 目前维护：yanjingxin
* 创建时间：2018-10-31
*/
#pragma once

#include "Logging/LogMacros.h"
#include "Containers/UnrealString.h"
#include "MultiLogSubsystem.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "CS3DebugType.h"
#include "CS3Debug.generated.h"
// -----------------------------------------编译期哈希字符串---------------------------
constexpr size_t HashString(char const* str, size_t seed)
{
	return 0 == *str ? seed : HashString(str + 1, seed ^ (*str + 0x9e3779b9 + (seed << 6) + (seed >> 2)));
}

template <size_t N>
struct EnsureConst
{
	static const size_t value = N;
};

#define ConstHashString(x) (EnsureConst<HashString(x, 0)>::value)

// -----------------------------------------基于UE4得日志框架----------------------------

// 只在蓝图中使用,c++中还是使用 ELogVerbosity::Error
UENUM(BlueprintType)
enum class ELogCS3Verbosity : uint8
{
	/**
	 * Prints an error to console (and log file).
	 * Commandlets and the editor collect and report errors. Error messages result in commandlet failure.
	 */
	Error,

	/**
	 * Prints a warning to console (and log file).
	 * Commandlets and the editor collect and report warnings. Warnings can be treated as an error.
	 */
	Warning,

	/** Prints a message to console (and log file) */
	Display,
};

UCLASS(meta = (ScriptName = "CS3DebugLibrary"))
class UCS3DebugLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()
public:
	// 使用参考 http://172.16.2.227/browse/CST-8863
	UFUNCTION(BlueprintCallable, meta = (WorldContext = "WorldContextObject", CallableWithoutWorldContext, Keywords = "log print", AdvancedDisplay = "4", DevelopmentOnly), Category = "Utilities|String")
	static void CS3_PrintString(UObject* WorldContextObject, const FString& InString, CS3DebugType Type, ELogCS3Verbosity Verbosity, bool bPrintToScreen = true, float Duration = 20.f);
	
	template <typename FmtType, typename... Types>
	static void CS3_PrintString(const ANSICHAR* File, int32 Line, CS3DebugType Type, ELogVerbosity::Type Verbosity, bool bPrintToScreen, float Duration, uint64 PrintToScreenKey, const FmtType& Fmt, Types... Args)
	{
#if !(UE_BUILD_SHIPPING || UE_BUILD_TEST)
		static_assert(TIsArrayOrRefOfType<FmtType, TCHAR>::Value, "Formatting string must be a TCHAR array.");
		static_assert(TAnd<TIsValidVariadicFunctionArg<Types>...>::Value, "Invalid argument(s) passed to FMsg::Logf");

#if !NO_LOGGING
		const FName& CategoryName = GetCS3DebugType(Type).GetCategoryName();
		if (Verbosity == ELogVerbosity::Fatal)
		{
			FMsg::Logf(File, Line, CategoryName, Verbosity, Fmt, Args...);
			_DebugBreakAndPromptForRemote();
			FDebug::AssertFailed("", File, Line, Fmt, Args...);
			CA_ASSUME(false);
		}
		else
		{
			if (bPrintToScreen && GEngine)
			{
				FString FinalDisplayString = FString::Printf(TEXT("%s: %s: "), *CategoryName.ToString(), *CS3Debug::GetVerbosityString(Verbosity)) + FString::Printf(Fmt, Args...);
				GEngine->AddOnScreenDebugMessage(PrintToScreenKey, Duration, CS3Debug::GetVerbosityColor(Verbosity), FinalDisplayString);
			}

			FMsg::Logf(File, Line, CategoryName, Verbosity, Fmt, Args...);
		}
#endif
#endif
	}
};

// 主要用于扩展CS3_DEBUG,不在其他地方用
// 使用参考 http://172.16.2.227/browse/CST-8863
#if NO_LOGGING
	#define LOG_CS3(CategoryName, Verbosity, Format, ...) \
	{ \
		static_assert(TIsArrayOrRefOfType<decltype(Format), TCHAR>::Value, "Formatting string must be a TCHAR array."); \
		if (ELogVerbosity::Verbosity == ELogVerbosity::Fatal) \
		{ \
			LowLevelFatalErrorHandler(UE_LOG_SOURCE_FILE(__FILE__), __LINE__, Format, ##__VA_ARGS__); \
			_DebugBreakAndPromptForRemote(); \
			FDebug::AssertFailed("", UE_LOG_SOURCE_FILE(__FILE__), __LINE__, Format, ##__VA_ARGS__); \
			UE_LOG_EXPAND_IS_FATAL(Verbosity, CA_ASSUME(false);, PREPROCESSOR_NOTHING) \
		} \
	}
#else
	#define LOG_CS3(DebugType, Verbosity, Format, ...) \
		{ \
			static_assert(TIsArrayOrRefOfType<decltype(Format), TCHAR>::Value, "Formatting string must be a TCHAR array."); \
			static_assert((ELogVerbosity::Verbosity & ELogVerbosity::VerbosityMask) < ELogVerbosity::NumVerbosity && ELogVerbosity::Verbosity > 0, "Verbosity must be constant and in range."); \
			CA_CONSTANT_IF((ELogVerbosity::Verbosity & ELogVerbosity::VerbosityMask) <= ELogVerbosity::COMPILED_IN_MINIMUM_VERBOSITY && (ELogVerbosity::Warning & ELogVerbosity::VerbosityMask) <= ELogVerbosity::All) \
			{ \
				UE_LOG_EXPAND_IS_FATAL(Verbosity, PREPROCESSOR_NOTHING, if (!GetCS3DebugType(DebugType).IsSuppressed(ELogVerbosity::Verbosity))) \
				{ \
					UE_LOG_EXPAND_IS_FATAL(Verbosity, \
						{ \
							UCS3DebugLibrary::CS3_PrintString(UE_LOG_SOURCE_FILE(__FILE__), __LINE__, DebugType, ELogVerbosity::Verbosity, true, 20.f, (uint64)-1, TEXT("%s: %s"), TEXT(__FUNCTION__), *FString::Printf(Format, __VA_ARGS__)); \
							_DebugBreakAndPromptForRemote(); \
							FDebug::AssertFailed("", UE_LOG_SOURCE_FILE(__FILE__), __LINE__, Format, ##__VA_ARGS__); \
							CA_ASSUME(false); \
						}, \
						{ \
							UCS3DebugLibrary::CS3_PrintString(nullptr, 0, DebugType, ELogVerbosity::Verbosity, true, 20.f, (uint64)-1, TEXT("%s(%d): %s"), TEXT(__FUNCTION__), __LINE__, *FString::Printf(Format, __VA_ARGS__)); \
						} \
					) \
				} \
			} \
		}
#endif

namespace CS3Debug
{
	const FColor& GetVerbosityColor(ELogVerbosity::Type Verbosity);
	const FString& GetVerbosityString(ELogVerbosity::Type Verbosity);
}

/*
	控制台命令
	UCS3ConsoleMgr::CS3_Debug(bool isDebug)
	UCS3ConsoleMgr::CS3_DebugByName(FString& CS3DebugTypeName, bool isDebug)
*/

// 调试日志。 一些系统调试时的日志。这个的日志量会很多，不同的系统都会有。
#define CS3_Display(CS3DebugType, msg, ...)	LOG_CS3(CS3DebugType, Display, msg, __VA_ARGS__);
// 重要流程输出。 一些重要系统的关键节点的日志输出。
#define CS3_Log(msg, ...)		LOG_CS3(CS3DebugType::CL_Log, Log, msg, __VA_ARGS__);
// 警告输出。 输出这个日志，不会崩溃，其用途可能是在 消耗比较高的检测，或者一些怀疑有错误使用的检测中。
#define CS3_Warning(msg, ...)	LOG_CS3(CS3DebugType::CL_Undefined, Warning, msg, __VA_ARGS__);
// 错误输出。 输出这个日志，后续就会崩溃。这种错误不能容忍，必须崩溃。
#define CS3_Fatal(msg, ...)		LOG_CS3(CS3DebugType::CL_Fatal, Fatal, msg, __VA_ARGS__);

// -----------------------------------------基于插件MultiLog得日志框架----------------------------
/*
	运行时设置日志等级 (默认日志等级是 EMultiLogLevel::Info)
	MultiLog.SetMultiLogLevel LogTypeName LogLevel

	MultiLogLevel::NoLog = -1
	MultiLogLevel::Error1 = 1
	MultiLogLevel::Warning = 2
	MultiLogLevel::Info = 3
	MultiLogLevel::DebugInfo = 4

	示例:
		MultiLog.SetMultiLogLevel KbeRpc 4
		MultiLog.SetMultiLogLevel KbeProperty 4
*/

/* kbe RPC调用日志 KbeRpc_LogTypeName = "KbeRpc" */
extern FName KbeRpc_LogTypeName;
#define KbeRpc_Error(msg, ...)		UMultiLogSubsystem::AddLog(KbeRpc_LogTypeName, EMultiLogLevel::Error1, msg, __VA_ARGS__);
#define KbeRpc_Warning(msg, ...)    UMultiLogSubsystem::AddLog(KbeRpc_LogTypeName, EMultiLogLevel::Warning, msg, __VA_ARGS__);
#define KbeRpc_Info(msg, ...)		UMultiLogSubsystem::AddLog(KbeRpc_LogTypeName, EMultiLogLevel::Info, msg, __VA_ARGS__);
#define KbeRpc_DebugInfo(msg, ...)  UMultiLogSubsystem::AddLog(KbeRpc_LogTypeName, EMultiLogLevel::DebugInfo, msg, __VA_ARGS__);
/* kbe Property变化日志 KbeProperty_LogTypeName = "KbeProperty" */
extern FName KbeProperty_LogTypeName;
#define KbeProperty_Error(msg, ...)		 UMultiLogSubsystem::AddLog(KbeProperty_LogTypeName, EMultiLogLevel::Error1, msg, __VA_ARGS__);
#define KbeProperty_Warning(msg, ...)    UMultiLogSubsystem::AddLog(KbeProperty_LogTypeName, EMultiLogLevel::Warning, msg, __VA_ARGS__);
#define KbeProperty_Info(msg, ...)		 UMultiLogSubsystem::AddLog(KbeProperty_LogTypeName, EMultiLogLevel::Info, msg, __VA_ARGS__);
#define KbeProperty_DebugInfo(msg, ...)  UMultiLogSubsystem::AddLog(KbeProperty_LogTypeName, EMultiLogLevel::DebugInfo, msg, __VA_ARGS__);

// -----------------------------------------------------编辑器模式禁用编译优化
#if WITH_EDITOR
#define CONTROL_COMPILE_OPTIMIZE_START __pragma(optimize("",off))
#define CONTROL_COMPILE_OPTIMIZE_END __pragma(optimize("",on))
#else
#define CONTROL_COMPILE_OPTIMIZE_START
#define CONTROL_COMPILE_OPTIMIZE_END
#endif