---
title: Mediator pattern in asp.net core
tags: [asp.net core, mediator, pattern]
---

```csharp
[ScopedService(typeof(IMediator))]
public class Mediator : IMediator, IAsyncMediator
{
    private readonly IServiceProvider serviceProvider;
    public Mediator(IServiceProvider serviceProvider)
    {
        this.serviceProvider = serviceProvider;
    }

    public IActionResult Send<T>(T request)
    {
        var requestHandler = this.serviceProvider.GetRequiredService<IRequestHandler<T>>();
        return requestHandler.HandleRequest(request);
    }

    public async Task<IActionResult> SendAsync<T>(T request)
    {
        var requestHandler = this.serviceProvider.GetRequiredService<IAsyncRequestHandler<T>>();
        var result = await requestHandler.HandleRequestAsync(request);
        return result;
    }
}   
```

The **ScopedService** attribute is a part of AutoInjection utility i wrote. It helps to register this class in DependnecyInjection. But it is not essential in Mediator pattern.
