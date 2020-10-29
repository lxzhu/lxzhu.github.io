---
title: Output remote ip address in log4net
tags: [asp.net core, log4net]
---
This post records how do i output client ip in log4net in my asp.net core website.

First of all, you need a class to provide value for pattern string in pattern layout in log4net configuration file.

```csharp
namespace WebApplication1.LayoutConverters
{
    /// <summary>
    /// ClientIP will be registered into log4net configuration file to provide value for a pattern
    /// </summary>
    public class ClientIP : PatternLayoutConverter
    {
        public static IClientIPProvider ClientIPProvider { get; set; }
        protected override void Convert(TextWriter writer, 
            LoggingEvent loggingEvent)
        {
            IPAddress clientIP = null;
            if (ClientIPProvider != null)
                clientIP = ClientIPProvider.GetClientIP();
            if (clientIP == null)
                clientIP = new IPAddress(new byte[] { 0, 0, 0, 0 });
            writer.Write(clientIP.ToString());
        }
    }

    /// <summary>
    /// <see cref="ClientIP"/> has no context information. 
    /// It delegates <see cref="IClientIPProvider"/> to provide value 
    /// of client ip
    /// </summary>
    public interface IClientIPProvider
    {
        IPAddress GetClientIP();
    }

    /// <summary>
    /// HttpClientIPProvider get RemoteIPAddress from <see cref="HttpContext.Connection"/>
    /// </summary>
    public class HttpClientIPProvider : IClientIPProvider
    {
        private IHttpContextAccessor httpContextAccessor;
        public HttpClientIPProvider(IHttpContextAccessor httpContextAccessor)
        {
            this.httpContextAccessor = httpContextAccessor;
        }
        public IPAddress GetClientIP()
        {
            var context = this.httpContextAccessor.HttpContext;
            if (context == null) return new IPAddress(new byte[] { 0, 0, 0, 0 });
            return context.Connection.RemoteIpAddress;
        }
    }
}
```

In Startup.cs we set value for ClientIP.ClientIPProvider
```csharp
public void Configure(IApplicationBuilder app, 
          IWebHostEnvironment env, 
          IServiceProvider sp)
{
    ClientIP.ClientIPProvider = sp.GetService<IClientIPProvider>();
    ...
}
```

In Startup.cs we register HttpContextAccessor and IClientIPProvider
```csharp
public void ConfigureServices(IServiceCollection services)
{
            services.AddControllersWithViews();
            services.AddHttpContextAccessor();
            services.AddSingleton<IClientIPProvider, HttpClientIPProvider>();
}
```
In log4net.config, we config a new converter
```xml
<?xml version="1.0" encoding="utf-8" ?>
<log4net>
    <appender name="EverythingOnServer" type="log4net.Appender.RollingFileAppender">
        <lockingModel type="log4net.Appender.FileAppender+MinimalLock"/>
        <file type ="log4net.Util.PatternString"
             value="../logs/Everything.txt" />
        <datePattern value="-yyyy-MM-dd"/>
        <preserveLogFileNameExtension value="true"/>        
        <staticLogFileName value="false"/>
        <appendToFile value="true"/>
        <maxSizeRollBackups value="10"/>
        <maximumFileSize value="1MB"/>
        <layout type="log4net.Layout.PatternLayout">
            <converter>
                <name value="clientip"/>
                <type value="WebApplication1.LayoutConverters.ClientIP"/>
            </converter>
            <conversionPattern value="%newline[%date] [%thread] [%-5level] [%clientip] [%c] %message %newline"/>
        </layout>
    </appender>
    <root>
        <level value="All"/>
        <appender-ref ref="EverythingOnServer"/>
    </root>
</log4net>
```
