# Monster Designer Guide (UGC) / 怪兽设计师指南

Agent Monster now allows players to design their own monsters! Your creations can be submitted to your repository and, if voted for by the community, added to the global **Egg Pool**.

代码怪兽现在允许玩家设计自己的怪兽！您的作品可以提交到您的仓库，如果通过社区投票，将被加入全球**孵化池**。

---

## 🎨 Design Workflow / 设计流程

### 1. Create a Design / 创建设计
Use the `monster_design` tool to define your monster's attributes.
使用 `monster_design` 工具定义您的怪兽属性。

**Example Prompt:**
> *"I want to design a monster named 'Cyber Dragon', type 'Logic', with HP 80, ATK 120, DEF 60, SPD 100."*
> *"我想设计一个名为 'Cyber Dragon' 的怪兽，属性为 'Logic'，数值为：HP 80, ATK 120, DEF 60, SPD 100。"*

### 2. Prepare for Submission / 准备提交
Once you are happy with the design, move it to your repository using `monster_submit_design`.
完成设计后，使用 `monster_submit_design` 将其移动到您的仓库目录。

**Example Prompt:**
> *"Submit my design for 'Cyber Dragon'."*
> *"提交我的 'Cyber Dragon' 设计。"*

This will move the file to `/designs/monsters/cyber_dragon.soul`.

### 3. Git Push to Your Fork / 提交到您的 Fork
Commit and push the design to **your own** GitHub fork (e.g., `https://github.com/YourName/agent-monster`).
将设计文件提交并推送到**您自己**的 GitHub Fork 仓库。

```bash
git add designs/monsters/cyber_dragon.soul
git commit -m "feat: design new monster Cyber Dragon"
git push origin main
```

### 4. Open a Pull Request / 发起合并请求 (PR)
To get your monster into the global pool, you must submit it to the main repository:
为了让您的怪兽进入全球孵化池，您需要将其提交给主仓库：

1. Go to your fork on GitHub.
2. Click **"Pull Request"** -> **"New Pull Request"**.
3. Target the base repository: `chengjia2016/agent-monster`.

### 5. Community Voting / 社区投票
Once your PR is open, the community can vote!
PR 开启后，社区成员即可开始投票！

- **How to vote**: Use the **Emoji Reactions** (e.g., 👍, ❤️) on the Pull Request.
- **投票方式**: 在 Pull Request 页面使用 **Emoji 回应** 进行投票。
- **Threshold**: Designs that receive enough positive reactions (e.g., > 10 👍) will be reviewed and merged.
- **阈值**: 获得足够正向回应的设计将被审核并合并。

### 6. Global Synchronization / 全局同步
- **Merge**: Once the PR is merged into `chengjia2016/agent-monster`, it officially enters the game's source code.
- **Judge Server**: The Judge Server automatically updates its registry from the main repository.
- **Hatching**: Your monster will now start appearing in eggs hatched by players all over the world!
- **同步**: 一旦 PR 被合并，设计将进入主仓库。裁判服务器会自动同步更新，您的怪兽将开始出现在全世界玩家孵化的蛋中！

---

## 📊 Design Constraints / 设计约束

To maintain balance, the sum of base stats (HP + ATK + DEF + SPD) should be reasonable. The Judge Server will validate these before integration.
为了保持平衡，基础属性的总和应保持在合理范围内。裁判服务器在集成前会进行数值校验。

**Start creating your monster legacy today!**
**今天就开始创造您的怪兽传奇吧！**
