// 设计 PLIS 的最终 YAML schema

// 从这个 Case 反推一个“纯净 Scenario”

// 可执行联动规则 correlation_rules

//facts 环境状态

Case → Scenario → Rule
```
win_kiosk_escape_VulnEscape.yml
│   │      │            │
│   │      │            └─ 具体靶机名 / 实例名
│   │      └─ 攻击类型 / 技术点
│   └─ 场景 / 系统子域
└─ 平台 / OS / 大类
```

//machine：Machine Account（计算机账户）；computer account in Active Directory

```
Evidence
   ↓
Correlation Rules  
   ↓
Scenario Activated
   ↓
Action / Suggestion
```
