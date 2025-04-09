 
#include "CS3GlobalStyle.h" 

void FGlobalCS3Style::GetResources(TArray<const FSlateBrush*>& OutBrushes) const
{
}
const FName FGlobalCS3Style::TypeName = TEXT("FGlobalCS3Style");
const FName FGlobalCS3Style::GetTypeName() const
{
	return TypeName;
}

const FGlobalCS3Style& FGlobalCS3Style::GetDefault()
{
	static FGlobalCS3Style Default;
	return Default;
}

UCS3Style::UCS3Style(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
}
