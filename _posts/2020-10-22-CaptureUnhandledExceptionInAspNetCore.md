---
title: Capture unhandled exception in asp.net core mvc
tags: [asp.net core]
---

Your action method may throw exception and you do not want to write try catch in each action method. Then you need an ExceptionFilterAttribute.

```csharp
public class IOExceptionFilterAttribute : ExceptionFilterAttribute
{
    public override void OnException(ExceptionContext context)
    {
        if (context.Exception != null && !context.ExceptionHandled)
        {
            var errorType = context.Exception.GetType().Name;
            var errorMessage = context.Exception.Message;
            var pd = new ProblemDetails()
            {
                Status = (int)HttpStatusCode.InternalServerError,
                Title = "InternalServerError",
                Detail = $"{errorType}:{errorMessage}"
            };
            var result = new ObjectResult(pd);
            result.StatusCode = (int)HttpStatusCode.InternalServerError;
            context.Result = result;
            context.ExceptionHandled = true;
        }
    }

    public override async Task OnExceptionAsync(ExceptionContext context)
    {
        this.OnException(context);
        await Task.CompletedTask;
    }
}
```
in Startup.cs

```csharp
public void ConfigureServices(IServiceCollection services)
{
    services.AddMvc(opt =>
    {                
        opt.Filters.Add<IOExceptionFilterAttribute>();
    });
}
```

Or you can put [IOExceptionFilter] on controller or action.

