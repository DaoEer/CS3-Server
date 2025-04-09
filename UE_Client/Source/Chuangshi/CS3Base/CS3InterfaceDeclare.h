#pragma once

#include <memory>
#include <type_traits>

#include "KBEngine.h"
#include "CS3EntityInterface.h"

//通过模板进行参数递归转换

class UCS3EntityInterface;

typedef KBEngine::FVariantArray FVariantArray;

template<size_t N>
struct CS3InterfaceMethodInvokerE {
	template<typename T>
	struct CS3InterfaceMethodInvoker {
		template<typename F, typename... A>
		static inline void Invoke( UCS3EntityInterface *eInterface, F && f, const FVariantArray &args, A &&... a)
		{
			typedef std::tuple_element<N - 1, T>::type VALUE_TYPE;
			VALUE_TYPE value;
			KBEngine::MethodArg<VALUE_TYPE>::Convert(value, std::forward<const FVariant>(args[N - 1]));
			CS3InterfaceMethodInvokerE<N - 1>::CS3InterfaceMethodInvoker<T>::Invoke(eInterface, std::forward<F>(f),
				args, value,
				std::forward<A>(a)...);
		}
	};
};

//专用模板，需要转换参数长度为0
template<>
struct CS3InterfaceMethodInvokerE<0> {
	template<typename T>
	struct CS3InterfaceMethodInvoker {
		template<typename F, typename... A>
		static inline void Invoke(UCS3EntityInterface *eInterface, F && f, const FVariantArray &args, A &&... a)
		{
			(eInterface->*std::forward<F>(f))(std::forward<A>(a)...);
		}
	};

};

//方法代理对象
class CS3InterfaceMethodProxy
{
public:
	virtual void Do(UCS3EntityInterface *eInterface, const FVariantArray &args) = 0;
};

typedef std::shared_ptr<CS3InterfaceMethodProxy> CS3InterfaceMethodProxyPtr;

template <class ... TYPES>
class CS3InterfaceMethodProxyV : public CS3InterfaceMethodProxy
{
public:
	typedef void (UCS3EntityInterface::*EMETHOD)(TYPES...);
	typedef std::tuple<typename std::decay<TYPES>::type...> TUPLE;

private:
	static const size_t _Mysize = sizeof...(TYPES);
	EMETHOD func;

public:
	CS3InterfaceMethodProxyV(EMETHOD pfn) : func(pfn) {}

	virtual void Do(UCS3EntityInterface *eInterface, const FVariantArray &args) override
	{
		if (args.Num() != _Mysize)
		{
			KBE_ERROR(TEXT("CS3InterfaceMethodProxy: args must takes %d arguments (%d given)"), _Mysize, args.Num());
			return;
		}

		CS3InterfaceMethodInvokerE<_Mysize>::CS3InterfaceMethodInvoker<TUPLE>::Invoke(eInterface, func, args);
	}
};


//属性代理对象
class CS3InterfacePropertyProxy
{
public:
	virtual void Do(UCS3EntityInterface *eInterface, const FVariant &newVal, const FVariant &oldVal) = 0;
};

typedef std::shared_ptr<CS3InterfacePropertyProxy> CS3InterfacePropertyProxyPtr;

template<class T>
class CS3InterfacePropertyProxyT : public CS3InterfacePropertyProxy
{
public:
	typedef void (UCS3EntityInterface::*PMETHOD)(const T &newVal, const T &oldVal);

private:
	PMETHOD func;

public:
	CS3InterfacePropertyProxyT(PMETHOD pfn) : func(pfn) {}

	virtual void Do(UCS3EntityInterface *eInterface, const FVariant &newVal, const FVariant &oldVal) override
	{
		T nval = newVal.GetValue<T>();
		T oval = oldVal.GetValue<T>();
		(eInterface->*func)(nval, oval);
	}
};



typedef TMap< FString, CS3InterfaceMethodProxyPtr> CS3_INTERFACE_METHOD_MAP;
typedef TMap< FString, CS3InterfacePropertyProxyPtr> CS3_INTERFACE_PROPERTY_MAP;


//eInterface接口定义宏
#define CS3_DECLARE_INTERFACE_MAP() \
public:\
	static CS3_INTERFACE_METHOD_MAP _thisMethodMap; \
	static CS3_INTERFACE_PROPERTY_MAP _thisPropertyMap; \
	static void InitMethodMap(); \
	static void InitPropertyMap();\
protected: \
	virtual void CallDefineMethod( const FString &name, const TArray<FVariant> &args ) override; \
	virtual void NotifyDefineProperty( const FString &name, const FVariant &newVal, const FVariant &oldVal ) override;


//外部方法绑定接口
#define CS3_BEGIN_INTERFACE_METHOD_MAP(theClass, baseClass) \
CS3_INTERFACE_METHOD_MAP theClass::_thisMethodMap;\
void theClass::CallDefineMethod( const FString &name, const TArray<FVariant> &args )\
{\
	auto methodProxyPtr = _thisMethodMap.Find(name);\
	if (methodProxyPtr)\
		( *methodProxyPtr )->Do(this, args);\
}\
void theClass::InitMethodMap() \
{ \
	baseClass::InitMethodMap();\
	if ( _thisMethodMap.Num() != 0 ) \
		return; \
	_thisMethodMap.Append( baseClass::_thisMethodMap );

#define CS3_END_INTERFACE_METHOD_MAP()\
}

#define CS3_DECLARE_INTERFACE_REMOTE_METHOD(name, func, ...) \
	_thisMethodMap.Add( TEXT(#name), CS3InterfaceMethodProxyPtr(new CS3InterfaceMethodProxyV<__VA_ARGS__>(static_cast<CS3InterfaceMethodProxyV<__VA_ARGS__>::EMETHOD>(func))) );


//外部属性绑定接口
#define CS3_BEGIN_INTERFACE_PROPERTY_MAP(theClass, baseClass) \
CS3_INTERFACE_PROPERTY_MAP theClass::_thisPropertyMap;\
void theClass::NotifyDefineProperty(const FString &name, const FVariant &newVal, const FVariant &oldVal) \
{ \
	auto propertyProxyPtr = _thisPropertyMap.Find(name); \
	if (propertyProxyPtr) \
		(*propertyProxyPtr)->Do(this, newVal, oldVal); \
} \
void theClass::InitPropertyMap() \
{ \
	baseClass::InitPropertyMap();\
	if ( _thisPropertyMap.Num() != 0 )\
		return; \
	_thisPropertyMap.Append(baseClass::_thisPropertyMap);

#define CS3_END_INTERFACE_PROPERTY_MAP() \
}

#define CS3_DECLARE_INTERFACE_PROPERTY_CHANGED_NOTIFY(name, func, T) \
	_thisPropertyMap.Add( TEXT(#name), CS3InterfacePropertyProxyPtr(new CS3InterfacePropertyProxyT<T>(static_cast<CS3InterfacePropertyProxyT<T>::PMETHOD>(func))));

