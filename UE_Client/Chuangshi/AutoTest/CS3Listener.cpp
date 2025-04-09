
#include "CS3Listener.h"
#include "Kismet/KismetSystemLibrary.h"


void CS3CreateListener::NotifyUObjectCreated(const class UObjectBase *Object, int32 Index)
{
	//FString Temp = UKismetSystemLibrary::GetPathName(Object);
	UE_LOG(LogTemp, Log, TEXT("Notify Create UObject[%d], Path->[%s]"), Index, *(Object->GetFName().ToString()));
}

void CS3DeleteListener::NotifyUObjectDeleted(const class UObjectBase *Object, int32 Index)
{
	//FString Temp = UKismetSystemLibrary::GetPathName(Object);
	UE_LOG(LogTemp, Log, TEXT("Notify Delete UObject[%d], Path->[%s]"), Index, *(Object->GetFName().ToString()));
}
