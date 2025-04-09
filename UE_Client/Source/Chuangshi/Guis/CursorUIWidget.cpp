// Fill out your copyright notice in the Description page of Project Settings.


#include "CursorUIWidget.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Manager/ResourceManager.h"
#include "Manager/CustomCursorManager.h"
#include "KBEngine.h"
#include "Manager/CfgManager.h"
#include "GameData/EnumCsvDefine.h"
#include "GameData/CursorData.h"
#include "Util/CS3Debug.h"

void UCursorUIWidget::SetCursorTexture(FString CursorState)
{
	//获得数据
	auto CursorTable = UUECS3GameInstance::Instance->CfgManager->GetTableByType(CSV_CONFIG_TYPE_ENUM::CSV_CURSOR_DATAS);
	FCURSOR_DATA* CursorData = const_cast<FCURSOR_DATA*>(CursorTable->GetRow<FCURSOR_DATA>(CursorState));

	//判断数据存在
	if (nullptr != CursorData)
	{
		//判断是否已经加载到内存
		if (IsValid(CursorData->CursorTexture.Get()))
		{
			UpdataImage(CursorData->CursorTexture.Get(), CursorData->TextureSize);
		}
		else
		{
			TWeakObjectPtr<UCursorUIWidget> DelayThisPtr(this);
			UUECS3GameInstance::Instance->ResourceManager->RequestAsyncLoad(this, CursorData->CursorTexture.ToSoftObjectPath(),
				FStreamableDelegate::CreateLambda([DelayThisPtr, CursorData, CursorState]()
			{

				if (DelayThisPtr.IsValid())
				{
					UCursorUIWidget* DelayThis = DelayThisPtr.Get();
					if (IsValid(CursorData->CursorTexture.Get()))
					{
						if (UUECS3GameInstance::Instance->CustomCursorManager->CurrentCursorState().Equals(CursorState))
						{
							DelayThis->UpdataImage(CursorData->CursorTexture.Get(), CursorData->TextureSize);
						}
					}
				}
				else
				{
					CS3_Warning(TEXT("UCursorUIWidget::SetCursorTexture--CursorData->CursorTexture is Not Valid!"));
				}

			}), RESOURCE_LOAD_PRIORITY_TYPE::RESOURCE_LOAD_PRIORITY_TYPE_PLAYER);
		}
	}
}

void UCursorUIWidget::UpdataImage(UObject* Texture, FVector2D TextureSize)
{
	if (IsValid(CursorImage))
	{
		if (IsValid(Texture))
		{
			CursorImage->Brush.SetResourceObject(Texture);
			CursorImage->SetBrushSize(TextureSize);
		}
	}
}

