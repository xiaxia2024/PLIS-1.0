# PLIS-1.0
Vuln Reasoning Engine（漏洞推理引擎）_Penetration Learning Intelligence System, 简称 PLIS

### demo.log输入内容
```
只需要“原始攻击日志”
1.Nmap 扫描
2.Gobuster / Feroxbuster / dirsearch 输出（可选）
3.错误回显、Payload 返回（可选）
4.Hydra、Netcat、CrackMapExec 等工具输出（可选）
5.自己执行命令的响应

在kali直接运行namp_parser.py执行demo.log
```

### PLIS 的架构是分层的
```
parser   →  rule_engine  →  reasoner  →  output
```
```
1.parser（解析器）
输入 log、nmap、gobuster 输出结构化 JSON：parsed_json = parser.parse()
2.rule_engine（规则引擎）
负责判定漏洞：rule_hits = RuleEngine().apply_rules(parsed_json)
3.reasoner（推理引擎）
它完全依赖 rule_engine 的结果 它只做一件事：解释 WHY
reasoner = Reasoner()
output = reasoner.build_machine_output(parsed_json, rule_hits)
```
