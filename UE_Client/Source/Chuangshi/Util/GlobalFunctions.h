#pragma once
#include "CoreMinimal.h"
#include <typeinfo>
#include "KBEngine.h"
#include "GameDevelop/CS3GameInstance.h"
#include "CS3Base/CS3Entity.h"

//#include "Templates/UnrealTemplate.h"

/*
global function
*/

using namespace std;

namespace CS3
{
	template <typename VAL>
	FString type_name(VAL val)
	{
		int status;
		char* real_name;
		real_name = abi::__cxa_demangle(typeid(VAL).name(), nullptr, nullptr, &status);
		FString s(real_name);
		free(real_name);
		real_name = nullptr;
		return s;
	}

	template <typename T>
	T GetEntity(int32 entityID)
	{
		KBEngine::Entity *e = UUECS3GameInstance::Instance->pKBEApp->FindEntity(entityID);
		if (e != nullptr)
		{
			return static_cast<T>(e);
		}
		return nullptr;
	}

	template <typename T>
	T* GetInterface(CS3Entity *entity)
	{
		if (entity == nullptr)
			return nullptr;

		for (auto it = entity->m_interfaceContainer.CreateConstIterator(); it; ++it)
		{
			if (T *re = Cast< T >(it->Value))
			{
				return re;
			}
		}
		return nullptr;
	}

	template <typename T>
	T* GetInterface(const int32 entityID)
	{
		CS3Entity *entity = GetEntity< CS3Entity* >(entityID);
		if (entity == nullptr)
			return nullptr;

		for (auto it = entity->m_interfaceContainer.CreateConstIterator(); it; ++it)
		{
			if(T *re = Cast< T >( it->Value))
			{
				return re;
			}
		}
		return nullptr;
	}

	template <typename T>
	T* GetInterface(const int32 entityID, const FString& name )
	{
		CS3Entity *entity = GetEntity< CS3Entity* >(entityID);
		if (entity == nullptr)
			return nullptr;

		if (entity->m_interfaceContainer.Contains( name ))
		{
			return StaticCast< T* >(entity->m_interfaceContainer[name]);
		}
		return nullptr;
	}
}