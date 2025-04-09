#include "CS3Debug.h"

FName KbeRpc_LogTypeName = FName(TEXT("KbeRpc"));

FName KbeProperty_LogTypeName = FName(TEXT("KbeProperty"));

void UCS3DebugLibrary::CS3_PrintString(UObject* WorldContextObject, const FString& InString, CS3DebugType Type, ELogCS3Verbosity CS3Verbosity, bool bPrintToScreen, float Duration)
{
#if !(UE_BUILD_SHIPPING || UE_BUILD_TEST)
	ELogVerbosity::Type LogVerbosity = ELogVerbosity::Display;
	switch (CS3Verbosity)
	{
	case ELogCS3Verbosity::Error:
		LogVerbosity = ELogVerbosity::Error;
		break;
	case ELogCS3Verbosity::Warning:
		LogVerbosity = ELogVerbosity::Warning;
		break;
	case ELogCS3Verbosity::Display:
		LogVerbosity = ELogVerbosity::Display;
		break;
	}

	if (!GetCS3DebugType(Type).IsSuppressed(LogVerbosity))
	{
		FString Prefix = GetNameSafe(WorldContextObject);
		FString PrefixString = FString::Printf(TEXT("%s: "), *Prefix) + InString;

		CS3_PrintString(nullptr, 0, Type, LogVerbosity, true, 60.f, (uint64)-1, TEXT("%s"), *PrefixString);
	}
#endif
}

const FColor& CS3Debug::GetVerbosityColor(ELogVerbosity::Type Verbosity)
{
	switch (Verbosity)
	{
	case ELogVerbosity::Fatal:
		return FColor::Red;
	case ELogVerbosity::Error:
		return FColor::Red;
	case ELogVerbosity::Warning:
		return FColor::Yellow;
	case ELogVerbosity::Display:
		return FColor::Cyan;
	case ELogVerbosity::Log:
		return FColor::Emerald;
	default:
		return FColor::Purple;
	}
}

const FString& CS3Debug::GetVerbosityString(ELogVerbosity::Type Verbosity)
{
	static FString Fatal{ TEXT("Fatal") };
	static FString Error{ TEXT("Error") };
	static FString Warning{ TEXT("Warning") };
	static FString Display{ TEXT("Display") };
	static FString Log{ TEXT("Log") };
	static FString Verbose{ TEXT("Verbose") };
	static FString VeryVerbose{ TEXT("VeryVerbose") };
	static FString Undefined{ TEXT("Undefined") };

	switch (Verbosity)
	{
	case ELogVerbosity::Fatal:
		return Fatal;
	case ELogVerbosity::Error:
		return Error;
	case ELogVerbosity::Warning:
		return Warning;
	case ELogVerbosity::Display:
		return Display;
	case ELogVerbosity::Log:
		return Log;
	case ELogVerbosity::Verbose:
		return Verbose;
	case ELogVerbosity::VeryVerbose:
		return VeryVerbose;
	default:
		return Undefined;
	}
}
