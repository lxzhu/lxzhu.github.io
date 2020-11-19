---
title: Mediator pattern in asp.net core
tags: [asp.net core, mediator, pattern]
---

This post is about how to use Mediator pattern in asp.net. It is not finished yet.

When a http request arrives an action method. The action method should get IMediator with [FromServices], and then construct an request, and send request to the its handler via Mediator.


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
