

#include "ByHeadParse.h"
#include "Util/CS3Debug.h"
#include "Util/GolbalBPFunctionLibrary.h"
#include "GameDevelop/CS3GameInstance.h"
#include "CS3Base/CS3Entity.h"

UByHeadParse::UByHeadParse()
{
	EscapeText = TEXT("$by");
}

UByHeadParse::~UByHeadParse()
{

}

void UByHeadParse::FormatText(FString OriginText, TMap<FString, FString>& FormatInfo, FString& LeaveText, DefaultParse& DefaultParseInstance)
{
	StructSpecialFormatText ScopeFormatText = DefaultParseInstance.GetSpeicalFormatText(OriginText);
	if (ScopeFormatText.SpecialFormatText.IsEmpty())
	{
		LeaveText = ScopeFormatText.UnformattedText;
	}
	else
	{
		TArray<FString> TransList = UGolbalBPFunctionLibrary::SplitString(ScopeFormatText.SpecialFormatText, false, TEXT(","));
		FString SpecialText = TEXT("");
		KBEngine::Entity* Player = UUECS3GameInstance::pKBEApp->Player();

		if (!Player)
		{
			CS3_Warning(TEXT("-->Null Pointer error:UByHeadParse::FormatText : Player!"));
			return;
		}

		CS3Entity* pEntity_Player = (CS3Entity*)(Player);
		if (!pEntity_Player->IsPlayerRole())
		{
			CS3_Warning(TEXT("-->Null Pointer error:UByHeadParse::FormatText :pEntity_Player->IsPlayerRole()!"));
			return;
		}

		if (OriginText.StartsWith("sex"))
		{
			int32 Gender = Player->GetDefinedProperty(TEXT("gender")).GetValue<int32>();
			if (Gender - 1 < TransList.Num())
			{
				SpecialText = TransList[Gender - 1];
			}
		}
		else if (OriginText.StartsWith("class"))
		{
			int32 Profession = Player->GetDefinedProperty(TEXT("profession")).GetValue<int32>();
			if (Profession - 1 < TransList.Num())
			{
				SpecialText = TransList[Profession - 1];
			}
		}
		else if (OriginText.StartsWith("camp"))
		{
			int32 Camp = Player->GetDefinedProperty(TEXT("camp")).GetValue<int32>();
			if (Camp - 1 < TransList.Num())
			{
				SpecialText = TransList[Camp - 1];
			}
		}

		if (!SpecialText.IsEmpty())
		{
			LeaveText = SpecialText + ScopeFormatText.UnformattedText;
		}
	}
}

FString UByHeadParse::TransformText(FString OriginText, TMap<FString, FString>& AttrInfos, TMap<FString, FString>& LastAttrInfos)
{
	return TransformExtraText(OriginText, AttrInfos, LastAttrInfos);
}
