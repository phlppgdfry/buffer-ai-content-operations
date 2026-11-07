# 🏆 Official Buffer LinkedIn Capabilities Guide

Buffer officially verifies four key capabilities on LinkedIn. Rather than taking multiple-choice exams, these badges are unlocked by demonstrating practical usage of the Buffer platform and its developer ecosystem.

---

## The 4 Official Buffer Capabilities

| Badge | Title | Target Audience | Difficulty |
|---|---|---|---|
| 🥇 | **Building with the API** | Engineers, Automation Specialists, AI Developers | ⭐⭐⭐⭐⭐ |
| 🥈 | **Content Scheduling & Planning** | Social Media Managers, Marketers, Founders | ⭐⭐⭐ |
| 🥉 | **Community Management & Engagement** | Community Managers, Support Teams | ⭐⭐⭐ |
| 🏅 | **Instagram & LinkedIn Publisher** | Cross-platform creators, Content Ops | ⭐⭐⭐ |

---

## 1. How to Unlock: "Building with the API" 🥇

This is the most prestigious and technically valuable badge for software engineers, consultants, and business analysts. It proves you can integrate external platforms, build robust API automations, and connect AI workflows with business software.

### Step-by-Step Execution:

1. **Obtain your Buffer API Token**:
   - Log into your Buffer account at [buffer.com](https://buffer.com).
   - Navigate to [publish.buffer.com/settings/api](https://publish.buffer.com/settings/api).
   - Generate a new personal access token.

2. **Connect your LinkedIn Profile to Buffer**:
   - Go to Buffer Settings → Channels.
   - Click **Connect Channel** → Select **LinkedIn Profile** or **LinkedIn Company Page**.
   - Authenticate the LinkedIn OAuth connection.

3. **Run this Platform with Live API Calls**:
   ```bash
   cd ~/buffer-ai-content-operations
   
   # Set your token
   export BUFFER_API_KEY="buf_live_your_actual_token"
   
   # Discover your LinkedIn channel ID
   content-ops channels
   
   # Run a live draft dispatch for your project
   content-ops demo --live
   ```

4. **Verify Activity in Buffer**:
   - Open your Buffer dashboard at [publish.buffer.com](https://publish.buffer.com).
   - Open the **Drafts** tab on your LinkedIn channel.
   - You will see the structured post draft staged and ready!

5. **Claim the Capability**:
   - In Buffer, navigate to: **LinkedIn Channel → Settings → General**.
   - Click **Check for LinkedIn skills**.
   - Once Buffer registers your API mutation activity, **Building with the API** will be flagged as unlocked.
   - Select **Add to LinkedIn** to display it on your public profile!

---

## 2. How to Unlock: "Content Scheduling & Planning" 🥈

### Requirements:
- Schedule posts across multiple channels on the Buffer calendar.
- Use Queue timing slots.

### Execution:
- In Buffer, set up a recurring posting schedule (e.g., Monday & Thursday at 10:00 AM).
- Schedule at least 3 to 5 posts across multiple days using `mode: addToQueue`.

---

## 3. How to Unlock: "Community Management & Engagement" 🥉

### Requirements:
- Reply to comments and engage with audience interactions using Buffer's engagement features.

### Execution:
- Enable the Buffer Community/Engagement dashboard (or connect an inbox).
- Respond to comments or mentions through the Buffer interface.

---

## 4. How to Unlock: "Instagram & LinkedIn Publisher" 🏅

### Requirements:
- Concurrently publish content to both an Instagram account (Business or Creator) and a LinkedIn profile through Buffer.

### Execution:
- Connect an Instagram Business account alongside your LinkedIn profile in Buffer.
- Dispatch a multi-channel draft or post targeting both channels using the Buffer CLI or API.

---

## Important Platform Rules

- **One Badge at a Time on LinkedIn**: While you can unlock all four capabilities in your Buffer account, LinkedIn currently allows displaying **one primary capability badge** at a time on your headline/profile.
- **Persistence**: Once unlocked in Buffer, capabilities remain in your Buffer account. You can freely switch which badge LinkedIn displays.
- **Connection Retention**: Do not disconnect Buffer from LinkedIn, as the badge display relies on the active connected app partnership.
