// Fill out your copyright notice in the Description page of Project Settings.


#include "CS3Object.h"
#include "Manager/ResourceManager.h"
#include "Manager/CustomTimerManager.h"
#include "GameDevelop/CS3GameInstance.h"
#include "Util/CS3Debug.h"

const FString UCS3Object::GetFStringPropertyByKey(const FString& name)
{
	FName PropertyName = FName(*name, FNAME_Find);
	if (PropertyName.IsNone())
	{
		return TEXT("");
	}

	UStrProperty *Prop = FindField<UStrProperty>(this->GetClass(), PropertyName);
	if (IsValid(Prop))
	{
		return Prop->GetPropertyValue_InContainer(this);
	}
	else
	{
		return TEXT("");
	}
}


void UCS3Object::BeginDestroy()
{
	if (IsValid(this) && IsValid(UUECS3GameInstance::Instance))
	{
		UUECS3GameInstance::Instance->ClearObjectHandles(this);
	}
	Super::BeginDestroy();
}

UWorld* UCS3Object::GetWorld() const
{
	if (!UUECS3GameInstance::Instance)
	{
		return Super::GetWorld();
	}
	return UUECS3GameInstance::Instance->GetWorld();
}

void UCS3Object::CLIENT_SetFStringPropertyByKey(const FString & name, const FString & value)
{
	SetFStringPropertyByKey(name, value);
}

void UCS3Object::SetFStringPropertyByKey(const FString & name, const FString & value)
{
	FName PropertyName = FName(*name, FNAME_Find);
	if (PropertyName.IsNone())
	{
		return;
	}

	UStrProperty *Prop = FindField<UStrProperty>(this->GetClass(), PropertyName);
	if (IsValid(Prop))
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("Set FString arg[%s] value[%s]"), *name, *value);
		Prop->SetPropertyValue_InContainer(this, value);
		FString MethodName(TEXT("OnRep_") + name);
		CallFuncToBlue(MethodName, MethodName);
	}
}

const float UCS3Object::GetFloatPropertyByKey(const FString& name)
{
	FName PropertyName = FName(*name, FNAME_Find);
	if (PropertyName.IsNone())
	{
		return 0.0f;
	}

	UFloatProperty *Prop = FindField<UFloatProperty>(this->GetClass(), PropertyName);
	if (IsValid(Prop))
	{
		return Prop->GetPropertyValue_InContainer(this);
	}
	else
	{
		return 0.0f;
	}
}


void UCS3Object::CLIENT_SetFloatPropertyByKey(const FString& name, float value)
{
	SetFloatPropertyByKey(name, value);
}

void UCS3Object::SetFloatPropertyByKey(const FString& name, float value)
{
	FName PropertyName = FName(*name, FNAME_Find);
	if (PropertyName.IsNone())
	{
		return;
	}

	UFloatProperty *Prop = FindField<UFloatProperty>(this->GetClass(), PropertyName);
	if (IsValid(Prop))
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("Set FString arg[%s] value[%f]"), *name, value);
		Prop->SetPropertyValue_InContainer(this, value);
		FString MethodName(TEXT("OnRep_") + name);
		CallFuncToBlue(MethodName, MethodName);
	}
}

const int UCS3Object::GetIntPropertyByKey(const FString& name)
{
	FName PropertyName = FName(*name, FNAME_Find);
	if (PropertyName.IsNone())
	{
		return 0;
	}

	UIntProperty *Prop = FindField<UIntProperty>(this->GetClass(), PropertyName);
	if (IsValid(Prop))
	{
		return Prop->GetPropertyValue_InContainer(this);
	}
	else
	{
		return 0;
	}
}

void UCS3Object::CLIENT_SetIntPropertyByKey(const FString &name, int32 value)
{
	SetIntPropertyByKey(name, value);
}

void UCS3Object::SetIntPropertyByKey(const FString &name, int32 value)
{
	FName PropertyName = FName(*name, FNAME_Find);
	if (PropertyName.IsNone())
	{
		return;
	}

	UIntProperty *Prop = FindField<UIntProperty>(this->GetClass(), PropertyName);
	if (IsValid(Prop))
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("Set FString arg[%s] value[%d]"), *name, value);
		Prop->SetPropertyValue_InContainer(this, value);
		FString MethodName(TEXT("OnRep_") + name);
		CallFuncToBlue(MethodName, MethodName);
	}
}

void UCS3Object::CLIENT_SetBoolPropertyByKey(const FString& name, uint8 value)
{
	bool Value = (bool)value;
	SetBoolPropertyByKey(name, Value);
}

void UCS3Object::SetBoolPropertyByKey(const FString &name, bool value)
{
	FName PropertyName = FName(*name, FNAME_Find);
	if (PropertyName.IsNone())
	{
		return;
	}
	
	UBoolProperty *Prop = FindField<UBoolProperty>(this->GetClass(), PropertyName);
	if (IsValid(Prop))
	{
		CS3_Display(CS3DebugType::CL_Undefined, TEXT("Set FString arg[%s] value[%d]"), *name, value);
		Prop->SetPropertyValue_InContainer(this, value);
		FString MethodName(TEXT("OnRep_") + name);
		CallFuncToBlue(MethodName, MethodName);
	}
}

const int UCS3Object::GetBoolPropertyByKey(const FString& name)
{
	FName PropertyName = FName(*name, FNAME_Find);
	if (PropertyName.IsNone())
	{
		return 0;
	}

	UBoolProperty *Prop = FindField<UBoolProperty>(this->GetClass(), PropertyName);
	if (IsValid(Prop))
	{
		return Prop->GetPropertyValue_InContainer(this);
	}
	else
	{
		return 0;
	}
}


const FString UCS3Object::GetArgumentsString(const FVariant &val)
{
	if (val.GetType() == EVariantTypes::Float)
	{
		float value = val;
		return FString::SanitizeFloat(value);
	}
	else if (val.GetType() == EVariantTypes::UInt8)
	{
		int32 value = (int32)val.GetValue<UINT8>();
		return FString::FromInt(value);
	}
	else if (val.GetType() == EVariantTypes::UInt16)
	{
		int32 value = (int32)val.GetValue<UINT16>();
		return FString::FromInt(value);
	}
	else if (val.GetType() == EVariantTypes::UInt32)
	{
		int32 value = (int32)val.GetValue<UINT32>();
		return FString::FromInt(value);
	}
	else if (val.GetType() == EVariantTypes::Int8)
	{
		int32 value = (int32)val.GetValue<INT8>();
		return FString::FromInt(value);
	}
	else if (val.GetType() == EVariantTypes::Int16)
	{
		int32 value = (int32)val.GetValue<INT16>();
		return FString::FromInt(value);
	}
	else if (val.GetType() == EVariantTypes::Int32)
	{
		int32 value = val;
		return FString::FromInt(value);
	}
	else if (val.GetType() == EVariantTypes::String)
	{
		FString value = val;
		return value;
	}
	else if (val.GetType() == EVariantTypes::Vector)
	{
		FVector value = val;
		return *FString::Printf(TEXT("(x=%f,y=%f,z=%f)"), value.X, value.Y, value.Z);
	}
	else if (val.GetType() == static_cast<EVariantTypes>(KBEngine::EKBEVariantTypes::VariantArray))
	{
		FString ret = TEXT("(");
		KBEngine::FVariantArray value = val;
		for (int j = 0; j < value.Num(); j++)
		{
			if ((value[j]).GetType() == EVariantTypes::String)
			{
				if (j == 0)
				{
					ret = *FString::Printf(TEXT("%s\"%s\""), *ret, *GetArgumentsString(value[j]));
				}
				else
				{
					ret = *FString::Printf(TEXT("%s,\"%s\""), *ret, *GetArgumentsString(value[j]));
				}
			}
			else
			{
				if (j == 0)
				{
					ret = *FString::Printf(TEXT("%s%s"), *ret, *GetArgumentsString(value[j]));
				}
				else
				{
					ret = *FString::Printf(TEXT("%s,%s"), *ret, *GetArgumentsString(value[j]));
				}
			}
		}
		ret = *FString::Printf(TEXT("%s)"), *ret);
		return ret;
	}

	return TEXT("");
}


void UCS3Object::Parameter_FVariantToFString(const TArray<FVariant> &InParameter, FString &OutParameter)
{
	for (int i = 0; i < InParameter.Num(); i++)
	{
		FVariant Val = InParameter[i];
		switch (Val.GetType())
		{
		case EVariantTypes::Float:
		case EVariantTypes::UInt8:
		case EVariantTypes::UInt16:
		case EVariantTypes::UInt32:
		case EVariantTypes::Int8:
		case EVariantTypes::Int16:
		case EVariantTypes::Int32:
		{
			OutParameter = *FString::Printf(TEXT("%s %s"), *OutParameter, *GetArgumentsString(InParameter[i]));
			break;
		}
		case EVariantTypes::String:
		{
			FString value = InParameter[i];
			if ((i + 1) == InParameter.Num())
				OutParameter = *FString::Printf(TEXT("%s %s"), *OutParameter, *GetArgumentsString(InParameter[i]));
			else
				OutParameter = *FString::Printf(TEXT("%s \"%s\""), *OutParameter, *GetArgumentsString(InParameter[i]));
			break;
		}
		default:
			OutParameter = *FString::Printf(TEXT("%s %s"), *OutParameter, *GetArgumentsString(InParameter[i]));
			break;
		}
	}
}

void UCS3Object::CallFuncToBlue(const FString &name, const FString &Parameter)
{
	const FName Message = FName(*name, FNAME_Find);
	if (Message.IsNone())
	{
		return;
	}

	UFunction* Function = FindFunction(Message);
	if (NULL == Function)
	{
		return;
	}

	FOutputDeviceNull ar;
	CallFunctionByNameWithArguments(*Parameter, ar, NULL, true);
}

void UCS3Object::CallFuncToBlueArgs(const FString &name, const TArray<FVariant> &args)
{
	FString FStringParameter(name);
	CS3Entity::Parameter_FVariantToFString(args, FStringParameter);

	CallFuncToBlue(name, FStringParameter);
}

void UCS3Object::CallPropertyChangeToBlue(const FString &name, const FVariant &newVal, const FVariant &oldVal)
{
	auto SetProperty_Fun = [this](const TCHAR* PropertyName, const FVariant &Val) {
		switch (Val.GetType())
		{
		case EVariantTypes::Vector:
			break;
		case EVariantTypes::Float:
		{
			float value = Val.GetValue<float>();

			UFloatProperty *Prop = FindField<UFloatProperty>(GetClass(), PropertyName);
			if (Prop != NULL)
			{
				Prop->SetPropertyValue_InContainer(this, value);
			}
			break;
		}
		case EVariantTypes::UInt8:
		{
			int value = Val.GetValue<uint8>();

			UByteProperty *Prop = FindField<UByteProperty>(GetClass(), PropertyName);
			if (Prop != NULL)
			{
				Prop->SetPropertyValue_InContainer(this, value);
			}
			break;
		}
		case EVariantTypes::UInt16:
		{
			int value = Val.GetValue<uint16>();

			UIntProperty *Prop = FindField<UIntProperty>(this->GetClass(), PropertyName);
			if (Prop != NULL)
			{
				Prop->SetPropertyValue_InContainer(this, value);
			}

			break;
		}
		case EVariantTypes::UInt32:
		{
			int value = Val.GetValue<uint32>();

			UIntProperty *Prop = FindField<UIntProperty>(this->GetClass(), PropertyName);
			if (Prop != NULL)
			{
				Prop->SetPropertyValue_InContainer(this, value);
			}

			break;
		}
		case EVariantTypes::Int8:
		{
			int value = Val.GetValue<int8>();

			UByteProperty *Prop = FindField<UByteProperty>(this->GetClass(), PropertyName);
			if (Prop != NULL)
			{
				Prop->SetPropertyValue_InContainer(this, value);
			}

			break;
		}
		case EVariantTypes::Int16:
		{
			int value = Val.GetValue<int16>();

			UIntProperty *Prop = FindField<UIntProperty>(this->GetClass(), PropertyName);
			if (Prop != NULL)
			{
				Prop->SetPropertyValue_InContainer(this, value);
			}

			break;
		}
		case EVariantTypes::Int32:
		{
			int value = Val.GetValue<int32>();

			UIntProperty *Prop = FindField<UIntProperty>(this->GetClass(), PropertyName);
			if (Prop != NULL)
			{
				Prop->SetPropertyValue_InContainer(this, value);
			}

			break;
		}
		case EVariantTypes::String:
		{
			UStrProperty *Prop = FindField<UStrProperty>(this->GetClass(), PropertyName);
			if (Prop != NULL)
			{
				Prop->SetPropertyValue_InContainer(this, *Val.GetValue<FString>());
			}

			break;
		}
		}
	};

	SetProperty_Fun(*name, newVal);
	SetProperty_Fun(*(TEXT("old_") + name), oldVal);

	FString MethodName(TEXT("OnRep_") + name);
	CallFuncToBlue(MethodName, MethodName);
}


