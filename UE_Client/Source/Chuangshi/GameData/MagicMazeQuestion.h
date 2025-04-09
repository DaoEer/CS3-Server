#pragma once
#include "CoreMinimal.h"
#include "MagicMazeQuestion.generated.h"

USTRUCT(BlueprintType)
struct CHUANGSHI_API FMAGICMAZEQUESTION_RESULT_DATA
{
	GENERATED_USTRUCT_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		FString PlayerName;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Profession = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Right = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Error = 0;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
		int32 Time = 0;
};
