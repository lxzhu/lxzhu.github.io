---
title: Inject dependencies into attribute in asp.net core
tags: [asp.net core, attribute, dependency injection]
---

After you get familiar with dependency injection, you want to use it everywhere. But how do you use it in Attribute? 
This post is about how to use dependency injection in asp.net filter attribute. After you understand this, you can mimic
this IFilterFactory mode in other place.

The basic flow of this pattern is:
1. you have a class which inherits Attribute class, so it is an attribute. This class has to implement IFilterFactory
1. asp.net core code detect an attribute implements IFilterFactory, it invoke its CreateInstance method with IServiceProvider.

```csharp
///
/// This attribute class will create another attriubte which will do the actual work.
///
public class ClientInternetAddressRestrictionAttribute : Attribute, IFilterFactory
{
    public ClientInternetAddressRestrictionResponseType ResponseType { get; set; }
    public string ResponseMessage { get; set; }

    public bool IsReusable { get; set; }

    public ClientInternetAddressRestrictionAttribute(ClientInternetAddressRestrictionResponseType responseType
        = ClientInternetAddressRestrictionResponseType.Unauthorized, string responseMessage = null)
    {
        this.ResponseType = responseType;
        this.ResponseMessage = responseMessage;
    }

    public IFilterMetadata CreateInstance(IServiceProvider serviceProvider)
    {
        var config = serviceProvider.GetService<IAddressRangeConfiguration>();
        var loggerFactory = serviceProvider.GetService<ILoggerFactory>();
        return new ClientInternetAddressRestriction2Attribute(config, loggerFactory,
            this.ResponseType, this.ResponseMessage);
    }
}
```

```csharp
public class ClientInternetAddressRestriction2Attribute : ActionFilterAttribute
{
    private readonly ILogger logger;
    private const string sLocalHost = "::1";
    public ClientInternetAddressRestrictionResponseType ResponseType { get; set; }
    private IAddressRangeConfiguration addressRangeConfiguration;
    public string ResponseMessage { get; set; }
    private const string sDefaultMessage401 = "You are not authorized to access this endpoint. Please contact administrator.";
    private const string sDefaultMessage404 = "The endpoint does not exist. Please contact administrator.";
    public ClientInternetAddressRestriction2Attribute(
        IAddressRangeConfiguration addressRangeConfiguration,
        ILoggerFactory loggerFactory,
        ClientInternetAddressRestrictionResponseType responseType = ClientInternetAddressRestrictionResponseType.Unauthorized,
        String responseMessage = null)
    {
        this.logger = loggerFactory.CreateLogger<ClientInternetAddressRestriction2Attribute>();
        this.ResponseType = responseType;
        this.ResponseMessage = responseMessage;
        this.addressRangeConfiguration = addressRangeConfiguration;
    }

    /// <summary>
    /// Parse on list of IPRange. 
    /// AppSettings variable AdminSafeIPRangeList can be set to "*" to allow client regardless of client IP.
    /// If AppSettings variable AdminSafeIPRangeList is null or empty client is denied
    /// </summary>
    /// <param name="context"></param>
    public override void OnActionExecuting(ActionExecutingContext context)
    {
        if (context is null)
        {
            throw new ArgumentNullException(nameof(context));
        }
        var remoteIp = context.HttpContext.Connection.RemoteIpAddress;
        var isClientAllowed = this.addressRangeConfiguration.IsClientIPAllowed(remoteIp);
        if (!isClientAllowed)
        {
            context.Result = this.MakeActionResult();
            var method = context.HttpContext.Request.Method;
            var path = context.HttpContext.Request.Path;
            var querystring = context.HttpContext.Request.QueryString;
            var warning = $"{method} {path}?{querystring} from client {remoteIp} is denied since the client ip is not allowed.";
            this.logger.LogWarning(warning);
        }

        base.OnActionExecuting(context);
    }

    private ActionResult MakeActionResult()
    {
        switch (this.ResponseType)
        {
            case ClientInternetAddressRestrictionResponseType.Unauthorized:
                return Make401();
            case ClientInternetAddressRestrictionResponseType.NotFound:
                return Make404();
            default:
                return Make404();
        }
    }
    private ActionResult Make401()
    {
        var message = this.ResponseMessage;
        if (string.IsNullOrWhiteSpace(message))
            message = sDefaultMessage401;
        return new UnauthorizedObjectResult(message);
    }
    private ActionResult Make404()
    {
        var message = this.ResponseMessage;
        if (string.IsNullOrWhiteSpace(message))
            message = sDefaultMessage404;
        return new NotFoundObjectResult(message);
    }
}
```
