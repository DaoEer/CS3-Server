#pragma once
#include <memory>
#include "CoreMinimal.h"
#include "CS3EntityInterface.h"

class CS3Entity;
class InterfaceDef;
class InterfaceDefPool;

typedef TMap< FString, UCS3EntityInterface* > INTERFACE_OBJECT_MAP;
typedef TMap<FString, std::shared_ptr<InterfaceDef> > INTERFACE_DEF_MAP;



class InterfaceDef
{
public:
	InterfaceDef() {};
	virtual ~InterfaceDef() {};
	virtual UCS3EntityInterface* Construct(CS3Entity* e) { return nullptr; }
};

template<class TT>
class InterfaceDefT:public InterfaceDef
{
public:
	InterfaceDefT() :InterfaceDef()
	{
		TT::InitMethodMap();
		TT::InitPropertyMap();
	};
	virtual ~InterfaceDefT() {};

	virtual UCS3EntityInterface* Construct(CS3Entity* e) override
	{  
		if (TT::GetBlueprintClassPath() == TEXT(""))
		{
			FString path = TT::GetClassPath();
			UClass* obj = LoadObject<UClass>(nullptr, *path);
			TT *Instance = (TT*)StaticConstructObject_Internal( obj );
			Instance->EntityID = e->ID();
			Instance->AddToRoot();
			Instance->InitBlueCB();
			return Instance;
		}
		return nullptr;
	}
};

#define DEF_INTERFACE_BEGIN( THIS_CLASS, SUPPER_CLASS ) \
	void THIS_CLASS::InitInterfaces() \
	{ \
		for (auto iter : GetDefInterfaces()) \
		{ \
			m_interfaceContainer.Add(iter.Key, iter.Value->Construct(this)); \
		} \
		InitInterfaceCache(); \
	} \
	const INTERFACE_DEF_MAP THIS_CLASS::GetDefInterfaces() \
	{ \
		INTERFACE_DEF_MAP thisInterfaces; \
		thisInterfaces.Append( SUPPER_CLASS::GetDefInterfaces() );

#define DEF_INTERFACE( INTERFACE )\
		if ( thisInterfaces.Contains( INTERFACE::GetName() ) ) \
			thisInterfaces.Remove( INTERFACE::GetName() ); \
		thisInterfaces.Add(	INTERFACE::GetName(), std::shared_ptr<InterfaceDef>( new InterfaceDefT< INTERFACE >() ) );

#define DEF_INTERFACE_END() \
		return thisInterfaces; \
	}

//entity接口定义宏
#define DEF_INTERFACE_CONTENT() \
	protected: \
		virtual const INTERFACE_DEF_MAP GetDefInterfaces() override;\
		virtual void InitInterfaces() override;

//entity接口定义宏
#define DEF_INTERFACE_CONTENT_BASE() \
	public: \
		static FString GetName() { return TEXT(""); }  \
		static FString GetBlueprintClassPath() { return TEXT(""); }  \
	protected: \
		virtual const INTERFACE_DEF_MAP GetDefInterfaces(){};\
		virtual void InitInterfaces(){};	
	