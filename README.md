# MaiFolderManager


 为AstroDX准备的，几乎一键化的文件夹整理与 Manifest 生成工具

## 概述

该工具用于整理指定工作目录中的文件夹结构，删除pv文件以缩减大小，并输出AstroDX可读的格式。它会：
1. 将 `mai` 文件夹复制为 `mai_i` 文件夹。
2. 删除 `mai_i` 中所有 `.mp4` 文件。
3. 为 `mai_i/collections` 中的每个文件夹生成 `manifest.json` 文件，其中包含该文件夹的子文件夹列表（`levelIds`）。
4. 根据需要将文件夹移动到 `levels` 或 `collections` 文件夹中。

此外，工具支持通过命令行参数指定工作目录.

## 依赖

该脚本使用 Python 的标准库，不需要额外安装其他依赖。

## 使用说明

### 如何组织文件夹
为了让脚本能够正确执行并生成期望的 manifest.json 文件，mai 文件夹中的内容应遵循类似以下的结构：
```bash
/work_d/
  ├── mai/
  │   ├── 收藏夹1/
  │   │   ├── 系ぎて/
  │   │   ├── PANDORA PARADOXXX/
  │   └── 收藏夹2/
  │       ├── Last Samurai/
  │       └── ウミユリ海底譚/

```
4.1 mai 文件夹的内容组织
mai 文件夹应包含多个子文件夹，每个子文件夹可以代表一个“集合”（collection）。示例如下：

### 1. 通过命令行运行

运行命令

```bash
python MaiFolderManager.py [directory]
```

- **`directory`**（可选）：要处理的工作目录。如果不指定，默认使用当前目录。
  
例如，如果你想处理 `/i/am/wmc` 目录，运行以下命令：

```bash
python MaiFolderManager.py /i/am/wmc
```

如果不指定目录，默认会使用当前工作目录：

```bash
python MaiFolderManager.py 
```

参数说明

- **`directory`**：工作目录，指定了需要整理的文件夹。如果省略此参数，脚本会在当前工作目录下执行。

### 2.直接运行py文件
脚本会在当前工作目录下执行。

## 错误处理

- 如果在工作目录中找不到 `mai` 文件夹，脚本会显示错误信息：
  
  ```bash
  The 'mai' folder does not exist in the specified directory: <directory>.
  ```

- 如果操作过程中出现其他问题，脚本会显示相关的错误消息。



## 注意事项

- 确保工作目录中存在 `mai` 文件夹，脚本才会继续执行。
- 脚本会修改工作目录中的文件和文件夹，请务必确认操作对象正确。

## TODO
 - [ ] 交互式/GUI式的操作
 - [ ] 输入文件夹不强制名为mai
 - [ ] 自定义输出文件夹名称

## 致谢
感谢cyanire的AstroDX-Tools为本项目提供了思路：
https://github.com/cyanire/AstroDX-Tools