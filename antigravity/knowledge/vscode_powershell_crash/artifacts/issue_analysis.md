# VS Code PowerShell Extension Crash Analysis

## Symptoms
The primary symptom is the PowerShell extension (PowerShell Editor Services, PSES) language server crashing and closing the connection. This is often accompanied by an error log similar to:

```text
在 OmniSharp.Extensions.JsonRpc.RequestRouterBase`1.<<RouteNotification>g__InnerRoute|6_0>d.MoveNext()
--- 引发异常的上一位置中堆栈跟踪的末尾 ---
...
在 OmniSharp.Extensions.JsonRpc.DefaultRequestInvoker.<>c__DisplayClass11_0.<<RouteNotification>b__3>d.MoveNext() | Method='textDocument/didClose'
[info] Language service connection closed.
[info] [PSES] [Error] Connection to PowerShell Editor Services was closed.
```

## Root Causes
1.  **LSP Implementation Instability:** The `OmniSharp.Extensions.JsonRpc` library used by PSES can throw exceptions when handling `textDocument/didClose` notifications, especially under heavy load.
2.  **PowerShell 5.1 Limitations:** This instability is significantly more common when using the legacy **Windows PowerShell 5.1** (the default version on Windows). PowerShell 5.1's runtime engine handles the LSP message queue less efficiently than the .NET (Core) based PowerShell 7+.
3.  **High-Frequency File Operations:** Tools like Antigravity that automate terminal commands or rapidly open/close files can trigger "race conditions" in the LSP server's notification queue.
