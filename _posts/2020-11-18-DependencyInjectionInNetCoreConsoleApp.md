---
title: Dependency Injection in .net core console app
tags: [.net core, DI]
---

This post is about how to use dependency injection in a .netcore console app.

```csharp
    class Program
    {
        public static void Main(string[] args)
        {
            var host = CreateHostBuilder(args).Build();
            using (var scope = host.Services.CreateScope())
            {
                var app = scope.ServiceProvider.GetRequiredService<ConsoleApp>();
                app.RunApp();
            }
        }
        public static IHostBuilder CreateHostBuilder(string[] args)
        {
            var host = Host.CreateDefaultBuilder(args)
                .ConfigureLogging(x =>
                {
                    x.AddProvider(new VsoLoggerProvider());
                    x.AddDebug();
                })
                .ConfigureServices(x => ConfigureServices(x, args));

            return host;
        }
        private static void ConfigureServices(
            IServiceCollection services,
            string[] args)
        {
            services.AddSingleton(x => new ConsoleArgv(args));
            services.AddSingleton<ConsoleApp>();
        }
    }

```
