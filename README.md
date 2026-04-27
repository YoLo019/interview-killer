<div align="center">

# interview-killer

> 面向技术面试准备的 Codex Skill

[![Skill](https://img.shields.io/badge/skill-resume--interview--pack-0f766e)]()
[![Runtime](https://img.shields.io/badge/runtime-python%203-3776AB)]()
[![License](https://img.shields.io/badge/license-MIT-orange)]()

</div>

`interview-killer` 是一个给 Codex 用的面试题包生成 skill。

它不是通用题库生成器。它会读取你的简历、简历中对应的项目代码目录、你整理的面经、以及你自己的知识库，然后生成一份更贴近你真实背景的技术面试题包，包括主问题、回答骨架、展开回答、追问和追问简答。

它还会维护一个长期画像，并提供本地交互式反馈页。这样后续生成的题包可以逐步根据你的薄弱点、已掌握主题和最近练习情况做调整。

## 能做什么

- 基于四类输入生成高概率技术面试题包
  - 简历
  - 简历中对应的项目代码目录
  - 面经
  - 知识库
- 固定按五个部分组织输出
  - 项目深挖
  - 原理与方案对比
  - 系统设计与工程化追问
  - 经典八股补充
  - 热门 AI / Agent 题
- 将题包写入本地 Markdown 文件，方便复习
- 在 `.interview/` 下维护长期画像和反馈数据
- 支持 `weak`、`improving`、`mastered` 三类显式反馈
- 提供本地浏览器反馈页，支持按题包逐题标记

## 适用场景

适合这些情况：

- 想根据自己的简历和项目生成更像真实面试的问题
- 不想只练通用八股，想重点练项目深挖题
- 想把面经当作“面试官风格信号”，而不是直接搬运原题
- 想补充和自己技术栈相关的后端基础题
- 想额外加入热门 AI / Agent 相关问题，但避免每次都重复同一组三题
- 想让每次练习结果持续影响后续题包，而不是每次都从零开始

## 工作方式

这个 skill 会读取项目内的这些状态文件：

```text
.interview/profile.json
.interview/profile-memory.md
.interview/feedback.json
.interview/feedback.md
```

默认的资料优先级大致是：

1. 简历中的项目描述和职责
2. 简历对应的项目代码目录
3. 面经中的关注点、追问方式和提问风格
4. 你的显式反馈
5. 知识库
6. 长期画像
7. 内置的热门 AI / Agent 话题模板

其中面经只作为参考信号，不直接当作原题题库使用。

生成后的题包默认写入：

```text
interview-packs/pack-YYYYMMDD.md
```

回答点评默认写入：

```text
interview-packs/review-YYYYMMDD.md
```

## 快速开始

### 1. 安装或放置 skill

项目级用法：

```text
.agents/skills/resume-interview-pack/
```

也可以放到你自己的 Codex 全局 skills 目录里。

### 2. 创建候选人配置

在项目里创建：

```text
.interview/profile.json
```

最小示例：

```json
{
  "resume_path": "C:\\Users\\YourName\\resume.md",
  "projects": [
    {
      "name": "ProjectName",
      "path": "D:\\projects\\ProjectName"
    }
  ],
  "materials": {
    "interview_notes": [
      "C:\\Users\\YourName\\notes\\interview-notes.md"
    ],
    "knowledge_bases": [
      "C:\\Users\\YourName\\notes\\rag-kb.md"
    ]
  }
}
```

### 3. 让 Codex 生成题包

示例触发语句：

```text
根据我的简历和项目生成高概率面试题
```

```text
帮我整理项目深挖题和标准回答
```

```text
帮我补一些常问八股和热门 AI / Agent 题
```

### 4. 复盘并反馈

这个仓库还包含本地反馈服务：

- `scripts/review_server.py`

在原始工作区版本中，通常会配合这些启动器使用：

```text
review-pack.ps1
review-pack.cmd
启动题包反馈.cmd
```

反馈页支持：

- 选择某一份已生成题包
- 将每道题标记为 `weak`、`improving` 或 `mastered`
- 填写简短备注
- 将结果回写到 `.interview/feedback.json`、`.interview/feedback.md` 和 `.interview/profile-memory.md`

## 输出结构

每道题固定使用这套结构：

1. 问题
2. 考察点
3. 1 分钟回答骨架
4. 展开版参考答案
5. 可能追问
6. 追问简答
7. 为什么大概率会问

整体风格以“面试里能说出口”为目标，不写成知识库原文，也不写成文章腔。

## 热门 AI / Agent 题

第五部分不只是项目相关的 AI 题。

它还会覆盖这些方向：

- 平时如何使用 AI 提效
- 如何做 AI coding
- 如何验证 AI 生成结果
- LangChain、LangGraph、原生 SDK、MCP 这类方案如何选型
- 为什么选择当前使用的 AI 框架
- Agent 架构、工具调用、记忆、安全、权限、编排
- RAG 和 Agent 的边界
- Hermes、OpenClaw、CC 这类热门开源项目的浅层了解题

同时它会尽量避免连续两版题包重复同一组三个热门题，除非：

- 你明确要求某一类题
- 反馈里把该主题标记成了 `weak`

## 仓库结构

```text
interview-killer/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── answer-rubric.md
│   ├── fundamentals-topics.md
│   ├── hot-topics.md
│   ├── profile-schema.md
│   ├── question-template.md
│   └── scenario-layout.md
├── scripts/
│   └── review_server.py
├── README.md
├── .gitignore
└── LICENSE
```

## 说明

- 这个仓库只包含 skill 本体，不包含你的私有简历、项目资料和题包结果
- 不建议把自己的 `.interview/` 数据或 `interview-packs/` 结果提交到公开仓库
- 如果你的简历不是 Markdown 或纯文本，建议先转成可读文本后再使用

## License

MIT。见 [LICENSE](./LICENSE)。
